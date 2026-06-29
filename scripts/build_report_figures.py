"""Generate report-ready figures for the course paper and GitHub Pages."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


FINANCIAL_CSV = Path("data/processed/financial_risk_indicators.csv")
TEXT_INDEX_CSV = Path("data/processed/text_risk_index_by_year.csv")
TEXT_TERMS_CSV = Path("data/processed/text_risk_terms_by_year.csv")
EVENTS_CSV = Path("data/interim/risk_events_official_seed.csv")
OUTPUT_DIR = Path("outputs/figures")
PAGES_FIGURE_DIR = Path("docs/assets/figures")
CATALOG_PATH = Path("docs/FIGURES_CATALOG.md")

RISK_COLORS = {
    "liquidity": "#4C78A8",
    "solvency": "#F58518",
    "operation": "#54A24B",
    "profitability": "#B279A2",
    "project": "#E45756",
    "compliance": "#72B7B2",
    "market": "#EECA3B",
    "organizational_propagation": "#9D755D",
}


def configure_matplotlib() -> None:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 120


def require_inputs() -> None:
    paths = [FINANCIAL_CSV, TEXT_INDEX_CSV, TEXT_TERMS_CSV, EVENTS_CSV]
    missing = [path for path in paths if not path.exists()]
    if missing:
        names = ", ".join(str(path) for path in missing)
        raise FileNotFoundError(f"Missing input files: {names}")


def save_figure(fig: plt.Figure, filename: str) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PAGES_FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    local_path = OUTPUT_DIR / filename
    pages_path = PAGES_FIGURE_DIR / filename
    fig.tight_layout()
    fig.savefig(local_path, dpi=180, bbox_inches="tight")
    fig.savefig(pages_path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return local_path, pages_path


def build_financial_trends(financial: pd.DataFrame) -> tuple[Path, Path]:
    years = financial["year"].astype(int)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    axes[0].bar(years, financial["revenue_100m_rmb"], color="#4C78A8", alpha=0.72, label="营业收入")
    ax0b = axes[0].twinx()
    ax0b.plot(years, financial["net_profit_parent_100m_rmb"], color="#E45756", marker="o", linewidth=2.4, label="归母净利润")
    ax0b.plot(years, financial["operating_cash_flow_100m_rmb"], color="#54A24B", marker="s", linewidth=2.4, label="经营现金流")
    axes[0].set_title("规模、利润与现金流")
    axes[0].set_ylabel("营业收入（亿元）")
    ax0b.set_ylabel("利润/现金流（亿元）")
    axes[0].set_xticks(years)
    axes[0].grid(axis="y", alpha=0.25)
    lines0, labels0 = axes[0].get_legend_handles_labels()
    lines1, labels1 = ax0b.get_legend_handles_labels()
    axes[0].legend(lines0 + lines1, labels0 + labels1, loc="upper left", frameon=False)

    axes[1].plot(years, financial["asset_liability_ratio_pct"], color="#F58518", marker="o", linewidth=2.4, label="资产负债率")
    axes[1].plot(years, financial["contract_assets_to_assets_pct"], color="#B279A2", marker="s", linewidth=2.4, label="合同资产/总资产")
    axes[1].plot(years, financial["accounts_receivable_to_assets_pct"], color="#72B7B2", marker="^", linewidth=2.4, label="应收账款/总资产")
    ax1b = axes[1].twinx()
    ax1b.plot(years, financial["interest_coverage"], color="#E45756", marker="D", linewidth=2.4, label="利息保障倍数")
    axes[1].set_title("杠杆、资产占用与偿债覆盖")
    axes[1].set_ylabel("比例（%）")
    ax1b.set_ylabel("倍")
    axes[1].set_xticks(years)
    axes[1].grid(axis="y", alpha=0.25)
    lines2, labels2 = axes[1].get_legend_handles_labels()
    lines3, labels3 = ax1b.get_legend_handles_labels()
    axes[1].legend(lines2 + lines3, labels2 + labels3, loc="upper left", frameon=False)

    fig.suptitle("中国中铁 2021-2025 年财务风险趋势", fontsize=15, fontweight="bold")
    return save_figure(fig, "financial_trends.png")


def build_text_heatmap(text_index: pd.DataFrame) -> tuple[Path, Path]:
    pivot = text_index.pivot_table(index="risk_label", columns="year", values="combined_text_risk_score")
    pivot = pivot.loc[pivot[2025].sort_values(ascending=False).index]
    fig, ax = plt.subplots(figsize=(9, 5.6))
    image = ax.imshow(pivot.values, cmap="YlOrRd", vmin=60, vmax=100, aspect="auto")
    ax.set_xticks(range(len(pivot.columns)), labels=[str(col) for col in pivot.columns])
    ax.set_yticks(range(len(pivot.index)), labels=pivot.index)
    ax.set_title("年报文本风险综合得分热力图", fontsize=14, fontweight="bold")
    for row_idx in range(pivot.shape[0]):
        for col_idx in range(pivot.shape[1]):
            value = pivot.iloc[row_idx, col_idx]
            ax.text(col_idx, row_idx, f"{value:.1f}", ha="center", va="center", fontsize=8, color="#2F2F2F")
    cbar = fig.colorbar(image, ax=ax, shrink=0.86)
    cbar.set_label("综合文本风险得分")
    return save_figure(fig, "text_risk_heatmap.png")


def build_top_terms_chart(text_terms: pd.DataFrame) -> tuple[Path, Path]:
    subset = text_terms[(text_terms["year"] == 2025) & (text_terms["jieba_weight"] > 0)].copy()
    subset = subset.sort_values("jieba_weight", ascending=False).head(12).sort_values("jieba_weight")
    colors = [RISK_COLORS.get(category, "#4C78A8") for category in subset["risk_category"]]
    labels = [f"{term}（{risk_label}）" for term, risk_label in zip(subset["term"], subset["risk_label"])]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(labels, subset["jieba_weight"], color=colors, alpha=0.82)
    ax.set_title("2025 年高权重风险种子词", fontsize=14, fontweight="bold")
    ax.set_xlabel("jieba TF-IDF 风格权重")
    ax.grid(axis="x", alpha=0.25)
    return save_figure(fig, "top_2025_risk_terms.png")


def read_events() -> list[dict[str, str]]:
    with EVENTS_CSV.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_risk_event_matrix(events: list[dict[str, str]]) -> tuple[Path, Path]:
    fig, ax = plt.subplots(figsize=(8.5, 6.2))
    annotation_counts: dict[tuple[float, float], int] = {}
    offsets = [(0.04, 0.08), (0.04, -0.13), (-0.5, 0.08), (-0.5, -0.13), (0.04, 0.26), (-0.5, 0.26)]

    def short_label(event_id: str) -> str:
        return (
            event_id.replace("OF", "")
            .replace("CONTRACT-ASSET", "CA")
            .replace("GUARANTEE", "GUA")
            .replace("LITIGATION", "LIT")
            .replace("SOLVENCY", "SOLV")
            .replace("PROFIT", "PROF")
        )

    for risk_type in sorted({event["risk_type"] for event in events}):
        group = [event for event in events if event["risk_type"] == risk_type]
        x_values = [Decimal(event["probability_score"]) for event in group]
        y_values = [Decimal(event["severity_score"]) for event in group]
        sizes = []
        for event in group:
            amount = Decimal(event["amount_rmb"] or "0") / Decimal("100000000")
            sizes.append(float(min(max(amount / Decimal("3"), Decimal("60")), Decimal("720"))))
        ax.scatter(
            [float(x) for x in x_values],
            [float(y) for y in y_values],
            s=sizes,
            color=RISK_COLORS.get(risk_type, "#4C78A8"),
            alpha=0.72,
            edgecolor="white",
            linewidth=0.8,
            label=risk_type,
        )
        for event, x_value, y_value in zip(group, x_values, y_values):
            if Decimal(event["severity_score"]) >= Decimal("4") or event["event_type"] == "rating_action":
                key = (float(x_value), float(y_value))
                offset = offsets[annotation_counts.get(key, 0) % len(offsets)]
                annotation_counts[key] = annotation_counts.get(key, 0) + 1
                ha = "left" if offset[0] > 0 else "right"
                ax.annotate(
                    short_label(event["event_id"]),
                    (float(x_value) + offset[0], float(y_value) + offset[1]),
                    fontsize=6.5,
                    ha=ha,
                    bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none", "alpha": 0.72},
                )

    ax.axvline(3.5, color="#333333", linewidth=1, alpha=0.5)
    ax.axhline(3.5, color="#333333", linewidth=1, alpha=0.5)
    ax.set_xlim(0.8, 5.3)
    ax.set_ylim(0.8, 5.3)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel("发生概率评分")
    ax.set_ylabel("影响程度评分")
    ax.set_title("官方披露风险事件矩阵", fontsize=14, fontweight="bold")
    ax.grid(alpha=0.2)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), frameon=False)
    return save_figure(fig, "risk_event_matrix.png")


def write_catalog() -> Path:
    lines = [
        "# 图表目录",
        "",
        "生成脚本：`scripts/build_report_figures.py`",
        "",
        "## 可用于报告的图表",
        "",
        "| 图表 | 文件 | 报告用途 |",
        "|---|---|---|",
        "| 财务风险趋势 | `docs/assets/figures/financial_trends.png` | 支撑财务指标趋势、盈利下行、资产负债率和利息保障倍数分析 |",
        "| 文本风险热力图 | `docs/assets/figures/text_risk_heatmap.png` | 支撑文本风险指标和风险类别排序 |",
        "| 2025 高权重风险词 | `docs/assets/figures/top_2025_risk_terms.png` | 支撑文本风险词典和年报风险语境解释 |",
        "| 官方事件风险矩阵 | `docs/assets/figures/risk_event_matrix.png` | 支撑风险发生概率与影响程度二维评估 |",
        "",
        "## 预览",
        "",
        "![财务风险趋势](assets/figures/financial_trends.png)",
        "",
        "![文本风险热力图](assets/figures/text_risk_heatmap.png)",
        "",
        "![2025 高权重风险词](assets/figures/top_2025_risk_terms.png)",
        "",
        "![官方事件风险矩阵](assets/figures/risk_event_matrix.png)",
        "",
        "## 解释边界",
        "",
        "- 图表基于公开年报、评级报告和本地脚本整理结果生成。",
        "- 当前风险矩阵使用官方披露种子事件，后续加入司法、执行和企业风险样本后应重新生成。",
        "- `outputs/figures/` 保存本地作图副本；`docs/assets/figures/` 用于 GitHub Pages 展示。",
    ]
    CATALOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return CATALOG_PATH


def main() -> int:
    configure_matplotlib()
    require_inputs()
    financial = pd.read_csv(FINANCIAL_CSV)
    text_index = pd.read_csv(TEXT_INDEX_CSV)
    text_terms = pd.read_csv(TEXT_TERMS_CSV)
    events = read_events()

    outputs = [
        build_financial_trends(financial),
        build_text_heatmap(text_index),
        build_top_terms_chart(text_terms),
        build_risk_event_matrix(events),
    ]
    catalog = write_catalog()
    for local_path, pages_path in outputs:
        print(f"wrote {local_path}")
        print(f"wrote {pages_path}")
    print(f"wrote {catalog}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
