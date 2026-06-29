"""Build a resilience-oriented risk management scorecard."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


FINANCIAL_CSV = Path("data/processed/financial_risk_indicators.csv")
FEATURES_CSV = Path("data/processed/model_features_china_railway.csv")
CENTRALITY_CSV = Path("data/processed/risk_network_centrality.csv")

SCORES_CSV = Path("data/processed/resilience_scores.csv")
TABLE_CSV = Path("outputs/tables/resilience_scores.csv")
LOCAL_RADAR = Path("outputs/figures/resilience_radar_2025.png")
PAGES_RADAR = Path("docs/assets/figures/resilience_radar_2025.png")
LOCAL_TREND = Path("outputs/figures/resilience_score_trend.png")
PAGES_TREND = Path("docs/assets/figures/resilience_score_trend.png")
DOC_OUTPUT = Path("docs/RESILIENCE_RISK_MANAGEMENT_MODEL.md")

DIMENSION_COLUMNS = [
    "financial_buffer_score",
    "operating_buffer_score",
    "governance_credit_buffer_score",
    "network_resilience_score",
]

DIMENSION_LABELS = {
    "financial_buffer_score": "财务缓冲",
    "operating_buffer_score": "经营缓冲",
    "governance_credit_buffer_score": "治理信用缓冲",
    "network_resilience_score": "网络韧性",
}

ACTION_BY_DIMENSION = {
    "financial_buffer_score": "滚动现金流预测、优化债务期限结构、提高利息覆盖与经营现金流安全垫。",
    "operating_buffer_score": "压实项目毛利、结算和回款责任，控制合同资产和应收账款占用。",
    "governance_credit_buffer_score": "对高严重度诉讼、执行、处罚和候选样本建立逐条复核与闭环整改台账。",
    "network_resilience_score": "降低高中心性子公司和事件节点风险暴露，优先处理跨年份、跨风险类型的桥接节点。",
}


def configure_matplotlib() -> None:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 120


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}; run the upstream scripts first")


def to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def minmax_score(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    values = to_numeric(series)
    valid = values.dropna()
    if valid.empty:
        return pd.Series(50.0, index=series.index)
    min_value = valid.min()
    max_value = valid.max()
    if np.isclose(max_value, min_value):
        scores = pd.Series(50.0, index=series.index)
    else:
        scores = (values - min_value) / (max_value - min_value) * 100
        if not higher_is_better:
            scores = 100 - scores
    return scores.fillna(50.0).clip(lower=0, upper=100)


def weighted_average(frame: pd.DataFrame, weights: dict[str, float]) -> pd.Series:
    total_weight = sum(weights.values())
    output = pd.Series(0.0, index=frame.index)
    for column, weight in weights.items():
        output += frame[column] * weight
    return output / total_weight


def load_inputs() -> pd.DataFrame:
    for path in (FINANCIAL_CSV, FEATURES_CSV, CENTRALITY_CSV):
        require_file(path)

    financial = pd.read_csv(FINANCIAL_CSV, encoding="utf-8-sig")
    features = pd.read_csv(FEATURES_CSV, encoding="utf-8-sig")
    centrality = pd.read_csv(CENTRALITY_CSV, encoding="utf-8-sig")

    financial["year"] = to_numeric(financial["year"]).astype(int)
    features["year"] = to_numeric(features["year"]).astype(int)

    year_centrality = centrality[centrality["node_type"] == "year"].copy()
    year_centrality["year"] = to_numeric(year_centrality["label"])
    year_centrality = year_centrality[year_centrality["year"].between(2021, 2025)]
    year_centrality["year"] = year_centrality["year"].astype(int)
    year_centrality = year_centrality[
        [
            "year",
            "weighted_degree",
            "betweenness_centrality",
            "pagerank",
        ]
    ].rename(
        columns={
            "weighted_degree": "year_weighted_degree",
            "betweenness_centrality": "year_betweenness_centrality",
            "pagerank": "year_pagerank",
        }
    )

    merged = financial.merge(features, on="year", how="left", suffixes=("", "_feature"))
    merged = merged.merge(year_centrality, on="year", how="left")
    merged = merged.sort_values("year").reset_index(drop=True)
    return merged


def build_scores(data: pd.DataFrame) -> pd.DataFrame:
    scores = data.copy()

    scores["financial_cashflow_component"] = minmax_score(scores["operating_cash_flow_to_revenue_pct"], True)
    scores["financial_leverage_component"] = minmax_score(scores["asset_liability_ratio_pct"], False)
    scores["financial_interest_component"] = minmax_score(scores["interest_coverage"], True)
    scores["financial_cash_interest_component"] = minmax_score(scores["cash_interest_coverage"], True)
    scores["financial_buffer_score"] = weighted_average(
        scores,
        {
            "financial_cashflow_component": 0.25,
            "financial_leverage_component": 0.25,
            "financial_interest_component": 0.25,
            "financial_cash_interest_component": 0.25,
        },
    )

    scores["operating_revenue_growth_component"] = minmax_score(scores["revenue_growth_pct"], True)
    scores["operating_profit_growth_component"] = minmax_score(scores["net_profit_parent_growth_pct"], True)
    scores["operating_receivable_component"] = minmax_score(scores["accounts_receivable_to_assets_pct"], False)
    scores["operating_contract_asset_component"] = minmax_score(scores["contract_assets_to_assets_pct"], False)
    scores["operating_buffer_score"] = weighted_average(
        scores,
        {
            "operating_revenue_growth_component": 0.25,
            "operating_profit_growth_component": 0.25,
            "operating_receivable_component": 0.25,
            "operating_contract_asset_component": 0.25,
        },
    )

    external_amount = to_numeric(scores["litigation_like_amount_rmb"]).fillna(0) + to_numeric(
        scores["execution_like_amount_rmb"]
    ).fillna(0)
    scores["governance_external_amount_log"] = np.log1p(external_amount)
    scores["governance_rating_support_component"] = 85.0
    scores["governance_high_severity_component"] = minmax_score(scores["high_severity_event_count"], False)
    scores["governance_external_amount_component"] = minmax_score(scores["governance_external_amount_log"], False)
    scores["governance_compliance_component"] = minmax_score(scores["compliance_event_count"], False)
    evidence_uncertainty = to_numeric(scores["event_count_candidate"]).fillna(0) + to_numeric(
        scores["event_count_verify"]
    ).fillna(0)
    scores["governance_evidence_quality_component"] = minmax_score(evidence_uncertainty, False)
    scores["governance_credit_buffer_score"] = weighted_average(
        scores,
        {
            "governance_rating_support_component": 0.25,
            "governance_high_severity_component": 0.25,
            "governance_external_amount_component": 0.20,
            "governance_compliance_component": 0.15,
            "governance_evidence_quality_component": 0.15,
        },
    )

    scores["network_event_count_component"] = minmax_score(scores["event_count_all"], False)
    scores["network_high_severity_component"] = minmax_score(scores["high_severity_event_count"], False)
    scores["network_weighted_degree_component"] = minmax_score(scores["year_weighted_degree"], False)
    scores["network_betweenness_component"] = minmax_score(scores["year_betweenness_centrality"], False)
    scores["network_pagerank_component"] = minmax_score(scores["year_pagerank"], False)
    scores["network_resilience_score"] = weighted_average(
        scores,
        {
            "network_event_count_component": 0.20,
            "network_high_severity_component": 0.20,
            "network_weighted_degree_component": 0.20,
            "network_betweenness_component": 0.20,
            "network_pagerank_component": 0.20,
        },
    )

    scores["composite_resilience_score"] = weighted_average(
        scores,
        {
            "financial_buffer_score": 0.25,
            "operating_buffer_score": 0.25,
            "governance_credit_buffer_score": 0.25,
            "network_resilience_score": 0.25,
        },
    )
    scores["resilience_level"] = scores["composite_resilience_score"].apply(resilience_level)
    scores["weakest_dimension"] = scores[DIMENSION_COLUMNS].idxmin(axis=1).map(DIMENSION_LABELS)
    scores["priority_action"] = scores[DIMENSION_COLUMNS].idxmin(axis=1).map(ACTION_BY_DIMENSION)

    return scores


def resilience_level(score: float) -> str:
    if score >= 75:
        return "较强缓冲"
    if score >= 65:
        return "中等偏强"
    if score >= 55:
        return "承压可控"
    if score >= 45:
        return "重点修复"
    return "低位修复"


def output_columns() -> list[str]:
    return [
        "year",
        "financial_buffer_score",
        "operating_buffer_score",
        "governance_credit_buffer_score",
        "network_resilience_score",
        "composite_resilience_score",
        "resilience_level",
        "weakest_dimension",
        "priority_action",
        "financial_cashflow_component",
        "financial_leverage_component",
        "financial_interest_component",
        "financial_cash_interest_component",
        "operating_revenue_growth_component",
        "operating_profit_growth_component",
        "operating_receivable_component",
        "operating_contract_asset_component",
        "governance_high_severity_component",
        "governance_external_amount_component",
        "governance_compliance_component",
        "governance_evidence_quality_component",
        "network_event_count_component",
        "network_weighted_degree_component",
        "network_betweenness_component",
        "network_pagerank_component",
        "event_count_all",
        "high_severity_event_count",
        "year_weighted_degree",
        "year_betweenness_centrality",
        "year_pagerank",
    ]


def write_score_tables(scores: pd.DataFrame) -> None:
    rounded = scores[output_columns()].copy()
    for column in rounded.select_dtypes(include=[np.number]).columns:
        if column != "year":
            rounded[column] = rounded[column].round(2)

    for path in (SCORES_CSV, TABLE_CSV):
        path.parent.mkdir(parents=True, exist_ok=True)
        rounded.to_csv(path, index=False, encoding="utf-8-sig")


def draw_trend(scores: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(11, 6))
    palette = {
        "composite_resilience_score": "#1f4e79",
        "financial_buffer_score": "#2ca02c",
        "operating_buffer_score": "#ff7f0e",
        "governance_credit_buffer_score": "#9467bd",
        "network_resilience_score": "#d62728",
    }
    labels = {
        "composite_resilience_score": "综合韧性",
        "financial_buffer_score": "财务缓冲",
        "operating_buffer_score": "经营缓冲",
        "governance_credit_buffer_score": "治理信用缓冲",
        "network_resilience_score": "网络韧性",
    }
    for column, color in palette.items():
        linewidth = 3 if column == "composite_resilience_score" else 1.8
        alpha = 1.0 if column == "composite_resilience_score" else 0.82
        ax.plot(scores["year"], scores[column], marker="o", linewidth=linewidth, alpha=alpha, color=color, label=labels[column])
    ax.axhspan(0, 55, color="#f3d6d6", alpha=0.35, linewidth=0)
    ax.axhspan(55, 65, color="#f5e9bd", alpha=0.35, linewidth=0)
    ax.axhspan(65, 100, color="#d9ead3", alpha=0.35, linewidth=0)
    ax.set_title("中国中铁 2021-2025 年风险韧性评分趋势", fontsize=15, fontweight="bold")
    ax.set_ylabel("评分（0-100，越高表示缓冲能力越强）")
    ax.set_ylim(0, 100)
    ax.set_xticks(scores["year"])
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend(ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.11))
    fig.tight_layout()
    for path in (LOCAL_TREND, PAGES_TREND):
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def draw_radar(scores: pd.DataFrame) -> None:
    latest = scores.sort_values("year").iloc[-1]
    columns = DIMENSION_COLUMNS
    labels = [DIMENSION_LABELS[column] for column in columns]
    values = [float(latest[column]) for column in columns]
    values_closed = values + values[:1]
    threshold = [60.0 for _ in columns]
    threshold_closed = threshold + threshold[:1]
    angles = np.linspace(0, 2 * np.pi, len(columns), endpoint=False).tolist()
    angles_closed = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})
    ax.plot(angles_closed, threshold_closed, color="#8c8c8c", linewidth=1.2, linestyle="--", label="60 分管理阈值")
    ax.plot(angles_closed, values_closed, color="#1f4e79", linewidth=2.6, label=f"{int(latest['year'])} 年")
    ax.fill(angles_closed, values_closed, color="#1f4e79", alpha=0.18)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_title("2025 年风险韧性四维雷达图", fontsize=15, fontweight="bold", pad=22)
    ax.legend(loc="upper right", bbox_to_anchor=(1.22, 1.14), frameon=False)
    fig.tight_layout()
    for path in (LOCAL_RADAR, PAGES_RADAR):
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "|" + "|".join("---" for _ in fields) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(row[field] for field in fields) + " |")
    return lines


def write_markdown(scores: pd.DataFrame) -> None:
    display = scores[
        [
            "year",
            "financial_buffer_score",
            "operating_buffer_score",
            "governance_credit_buffer_score",
            "network_resilience_score",
            "composite_resilience_score",
            "resilience_level",
            "weakest_dimension",
        ]
    ].copy()
    for column in DIMENSION_COLUMNS + ["composite_resilience_score"]:
        display[column] = display[column].map(lambda value: f"{value:.1f}")
    display["year"] = display["year"].astype(int).astype(str)
    display_rows = display.rename(
        columns={
            "year": "年份",
            "financial_buffer_score": "财务缓冲",
            "operating_buffer_score": "经营缓冲",
            "governance_credit_buffer_score": "治理信用缓冲",
            "network_resilience_score": "网络韧性",
            "composite_resilience_score": "综合得分",
            "resilience_level": "等级",
            "weakest_dimension": "最弱维度",
        }
    ).to_dict(orient="records")

    latest = scores.sort_values("year").iloc[-1]
    weakest_column = scores[DIMENSION_COLUMNS].idxmin(axis=1).iloc[-1]
    strongest_column = scores[DIMENSION_COLUMNS].idxmax(axis=1).iloc[-1]
    latest_year = int(latest["year"])
    latest_score = float(latest["composite_resilience_score"])
    latest_level = latest["resilience_level"]

    lines = [
        "# 弹性风险管理模型：风险缓冲能力评分",
        "",
        "生成脚本：`scripts/build_resilience_model.py`",
        "",
        "## 模型定位",
        "",
        "- 本模型对应课程要求中的“弹性风险管理模型”，用于判断企业风险缓冲能力。",
        "- 它是管理评分表，不是违约概率模型；机器学习预警结果见 `docs/FINANCIAL_WARNING_MODEL.md`。",
        "- 评分使用 2021-2025 年官方财务指标、文本/事件特征和风险图谱年度中心性，所有输入均由前序脚本生成；分值表示样本期内的相对缓冲强弱。",
        "",
        "## 输出文件",
        "",
        "- 评分表：`data/processed/resilience_scores.csv`",
        "- 报告表格副本：`outputs/tables/resilience_scores.csv`",
        "- 2025 年雷达图：`docs/assets/figures/resilience_radar_2025.png`",
        "- 年度趋势图：`docs/assets/figures/resilience_score_trend.png`",
        "",
        "## 四维评分口径",
        "",
        "所有指标先按 2021-2025 年样本做 0-100 标准化，越高表示缓冲能力越强；对资产负债率、应收账款占比、合同资产占比、事件数、中心性等风险暴露型变量取反向得分。首年缺少同比增速时，相关增长项按 50 分中性处理。",
        "",
        "| 维度 | 主要输入 | 管理含义 |",
        "|---|---|---|",
        "| 财务缓冲 | 经营现金流/营业收入、资产负债率、利息保障倍数、现金利息保障倍数 | 衡量债务覆盖、现金流安全垫和杠杆压力 |",
        "| 经营缓冲 | 营收增速、归母净利润增速、应收账款占总资产、合同资产占总资产 | 衡量业务增长、利润修复和资产占用压力 |",
        "| 治理信用缓冲 | 外部信用支持基准、严重事件数、诉讼/执行金额、合规事件、证据不确定性 | 衡量央企信用缓冲、事件治理和外部风险复核压力 |",
        "| 网络韧性 | 年度事件数、严重事件数、年份节点加权度、中介中心性、PageRank | 衡量风险事件在图谱中的集中度和传导中枢程度 |",
        "",
        "## 年度评分结果",
        "",
    ]
    lines.extend(
        markdown_table(
            display_rows,
            ["年份", "财务缓冲", "经营缓冲", "治理信用缓冲", "网络韧性", "综合得分", "等级", "最弱维度"],
        )
    )

    lines.extend(
        [
            "",
            "## 图表",
            "",
            "![2025 年风险韧性四维雷达图](assets/figures/resilience_radar_2025.png)",
            "",
            "![风险韧性评分趋势](assets/figures/resilience_score_trend.png)",
            "",
            "## 结果解释",
            "",
            f"- {latest_year} 年综合韧性得分为 {latest_score:.1f}，等级为“{latest_level}”。",
            f"- {latest_year} 年最强维度为“{DIMENSION_LABELS[strongest_column]}”，最弱维度为“{DIMENSION_LABELS[weakest_column]}”。",
            "- 从趋势看，2021-2022 年受益于较低杠杆和较少外部事件，综合韧性相对较高；2024-2025 年受盈利下行、合同资产和应收账款占用、严重事件数增加影响，韧性评分进入承压区间。",
            "- 网络韧性在 2023 年后明显走弱，主要因为外部风险样本使年份节点、合规/流动性节点和若干执行/诉讼事件的桥接作用增强。",
            "",
            "## 管理动作映射",
            "",
            "| 触发情形 | 建议动作 |",
            "|---|---|",
            "| 财务缓冲低于 55 分 | 建立月度现金流滚动预测，压降高成本短债，设置利息覆盖和经营现金流预警阈值 |",
            "| 经营缓冲低于 55 分 | 对合同资产、应收账款和低毛利项目做穿透式台账，按业主类型和账龄设回款责任 |",
            "| 治理信用缓冲低于 55 分 | 对诉讼、执行、处罚和候选样本逐条复核，形成整改、披露和责任追踪闭环 |",
            "| 网络韧性低于 55 分 | 优先治理高中心性子公司、年份和风险事件节点，降低单点风险向集团层面传导的可能 |",
            "",
            "## 解释边界",
            "",
            "- 评分使用公开数据和课程项目规则，适合风险管理优先级排序，不构成投资建议或信用评级意见。",
            "- 治理信用缓冲中的外部信用支持基准用于表示央企背景和评级稳定性带来的缓冲，不代表未来信用状态不会变化。",
            "- 部分执行和企查查样本仍为 `candidate` 或 `verify` 状态；若后续完成逐条复核，应重新运行图谱和本模型。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_summary(scores: pd.DataFrame) -> None:
    latest = scores.sort_values("year").iloc[-1]
    print(f"wrote {SCORES_CSV}")
    print(f"wrote {TABLE_CSV}")
    print(f"wrote {LOCAL_RADAR}")
    print(f"wrote {PAGES_RADAR}")
    print(f"wrote {LOCAL_TREND}")
    print(f"wrote {PAGES_TREND}")
    print(f"wrote {DOC_OUTPUT}")
    print(
        "latest resilience score: "
        f"{int(latest['year'])} {latest['composite_resilience_score']:.2f} {latest['resilience_level']}"
    )


def main() -> int:
    configure_matplotlib()
    data = load_inputs()
    scores = build_scores(data)
    write_score_tables(scores)
    draw_radar(scores)
    draw_trend(scores)
    write_markdown(scores)
    print_summary(scores)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
