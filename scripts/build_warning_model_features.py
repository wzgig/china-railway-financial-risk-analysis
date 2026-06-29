"""Build a yearly feature table for the warning-model stage.

The current repository only has one firm's 2021-2025 annual observations, so
this script prepares model-ready features and a transparent rule label instead
of pretending to train a statistically reliable machine-learning model.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


FINANCIAL_CSV = Path("data/processed/financial_risk_indicators.csv")
TEXT_INDEX_CSV = Path("data/processed/text_risk_index_word2vec_by_year.csv")
EVENTS_CSV = Path("data/processed/risk_events_combined.csv")
OUTPUT_CSV = Path("data/processed/model_features_china_railway.csv")
DOC_OUTPUT = Path("docs/MODEL_FEATURE_TABLE.md")


TEXT_CATEGORIES = [
    "liquidity",
    "solvency",
    "operation",
    "profitability",
    "project",
    "compliance",
    "market",
    "organizational_propagation",
]


def decimal_value(value: str | None) -> Decimal:
    if value is None or value == "":
        return Decimal("0")
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return Decimal("0")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_text_features(rows: list[dict[str, str]]) -> dict[str, dict[str, Decimal]]:
    features: dict[str, dict[str, Decimal]] = defaultdict(lambda: defaultdict(Decimal))
    for row in rows:
        year = row["year"]
        category = row["risk_category"]
        score = decimal_value(row.get("combined_text_risk_score"))
        features[year]["text_risk_score_total"] += score
        if category in TEXT_CATEGORIES:
            features[year][f"text_{category}_score"] = score
    return features


def build_event_features(rows: list[dict[str, str]]) -> dict[str, dict[str, Decimal]]:
    features: dict[str, dict[str, Decimal]] = defaultdict(lambda: defaultdict(Decimal))
    for row in rows:
        year = row["year"]
        amount = decimal_value(row.get("amount_rmb"))
        source_type = row["source_type"]
        status = row["evidence_status"]
        event_type = row["event_type"]
        risk_type = row["risk_type"]
        severity = decimal_value(row.get("severity_score"))

        features[year]["event_count_all"] += Decimal("1")
        features[year][f"event_count_{status}"] += Decimal("1")
        features[year][f"{source_type}_event_count"] += Decimal("1")
        features[year]["event_amount_rmb_all"] += amount
        features[year][f"{source_type}_amount_rmb"] += amount
        features[year][f"{risk_type}_event_count"] += Decimal("1")
        if event_type in {"execution_case", "dishonest_judgment_debtor", "restricted_consumption"}:
            features[year]["execution_like_event_count"] += Decimal("1")
            features[year]["execution_like_amount_rmb"] += amount
        if event_type in {"civil_litigation", "litigation_contingency"}:
            features[year]["litigation_like_event_count"] += Decimal("1")
            features[year]["litigation_like_amount_rmb"] += amount
        if severity >= Decimal("4"):
            features[year]["high_severity_event_count"] += Decimal("1")
    return features


def pressure_rule(row: dict[str, str]) -> tuple[int, int, str]:
    reasons: list[str] = []
    if decimal_value(row.get("asset_liability_ratio_pct")) >= Decimal("77"):
        reasons.append("资产负债率不低于77%")
    if decimal_value(row.get("net_profit_parent_growth_pct")) <= Decimal("-10"):
        reasons.append("归母净利润同比下降超过10%")
    interest_coverage = decimal_value(row.get("interest_coverage"))
    if interest_coverage and interest_coverage <= Decimal("3.2"):
        reasons.append("利息保障倍数不高于3.2")
    if decimal_value(row.get("contract_assets_to_assets_pct")) >= Decimal("14"):
        reasons.append("合同资产占总资产比例不低于14%")
    if decimal_value(row.get("event_count_all")) >= Decimal("4"):
        reasons.append("年度风险事件样本不少于4条")
    if decimal_value(row.get("execution_like_amount_rmb")) >= Decimal("10000000"):
        reasons.append("执行类金额不低于1000万元")
    score = len(reasons)
    return (1 if score >= 2 else 0), score, "；".join(reasons)


def quantize_text(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.0001")))


def quantize_amount(value: Decimal) -> str:
    return str(value.quantize(Decimal("1")))


def build_features() -> list[dict[str, str]]:
    financial_rows = read_csv(FINANCIAL_CSV)
    text_features = build_text_features(read_csv(TEXT_INDEX_CSV))
    event_features = build_event_features(read_csv(EVENTS_CSV))
    rows: list[dict[str, str]] = []

    for financial in financial_rows:
        year = financial["year"]
        row: dict[str, str] = {
            "company_code": "601390",
            "company_name": "中国中铁股份有限公司",
            "year": year,
            "revenue_growth_pct": financial.get("revenue_growth_pct", ""),
            "net_profit_parent_growth_pct": financial.get("net_profit_parent_growth_pct", ""),
            "operating_cash_flow_to_revenue_pct": financial.get("operating_cash_flow_to_revenue_pct", ""),
            "asset_liability_ratio_pct": financial.get("asset_liability_ratio_pct", ""),
            "accounts_receivable_to_assets_pct": financial.get("accounts_receivable_to_assets_pct", ""),
            "contract_assets_to_assets_pct": financial.get("contract_assets_to_assets_pct", ""),
            "interest_coverage": financial.get("interest_coverage", ""),
            "cash_interest_coverage": financial.get("cash_interest_coverage", ""),
        }

        for key, value in sorted(text_features.get(year, {}).items()):
            row[key] = quantize_text(value)
        for category in TEXT_CATEGORIES:
            row.setdefault(f"text_{category}_score", "0.0000")
        row.setdefault("text_risk_score_total", "0.0000")

        for key, value in sorted(event_features.get(year, {}).items()):
            if key.endswith("_amount_rmb"):
                row[key] = quantize_amount(value)
            else:
                row[key] = str(int(value))
        for key in [
            "event_count_all",
            "event_count_core",
            "event_count_candidate",
            "event_count_verify",
            "wenshu_event_count",
            "execution_event_count",
            "qcc_event_count",
            "execution_like_event_count",
            "litigation_like_event_count",
            "high_severity_event_count",
        ]:
            row.setdefault(key, "0")
        for key in [
            "event_amount_rmb_all",
            "wenshu_amount_rmb",
            "execution_amount_rmb",
            "qcc_amount_rmb",
            "execution_like_amount_rmb",
            "litigation_like_amount_rmb",
        ]:
            row.setdefault(key, "0")

        label, score, reasons = pressure_rule(row)
        row["financial_pressure_label"] = str(label)
        row["financial_pressure_rule_score"] = str(score)
        row["label_reason"] = reasons
        rows.append(row)

    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for field in row:
            if field not in seen:
                fieldnames.append(field)
                seen.add(field)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    lines = [
        "# 机器学习预警模型特征表",
        "",
        "生成脚本：`scripts/build_warning_model_features.py`",
        "",
        "## 当前定位",
        "",
        "- 当前表只覆盖中国中铁 2021-2025 年年度观测，用于定义机器学习模型字段、标签规则和后续同业面板接入方式。",
        "- 单公司 5 个年度样本不足以训练可靠机器学习模型；下一步应把同业建筑上市公司按同一字段补齐后再训练。",
        "- `financial_pressure_label` 是透明规则标签，不是模型预测结果。",
        "",
        "## 输出文件",
        "",
        "- 本地特征表：`data/processed/model_features_china_railway.csv`",
        "",
        "## 标签规则",
        "",
        "年度满足以下条件中的至少两项时，标记为财务压力样本：资产负债率不低于 77%、归母净利润同比下降超过 10%、利息保障倍数不高于 3.2、合同资产占总资产比例不低于 14%、年度风险事件样本不少于 4 条、执行类金额不低于 1000 万元。",
        "",
        "## 年度样本预览",
        "",
        "| 年份 | 资产负债率(%) | 归母净利增速(%) | 利息保障倍数 | 事件数 | 执行类金额(元) | 文本风险总分 | 标签 | 标签原因 |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {year} | {debt} | {profit} | {interest} | {events} | {exec_amount} | {text_score} | {label} | {reason} |".format(
                year=row["year"],
                debt=row["asset_liability_ratio_pct"],
                profit=row["net_profit_parent_growth_pct"],
                interest=row["interest_coverage"],
                events=row["event_count_all"],
                exec_amount=row["execution_like_amount_rmb"],
                text_score=row["text_risk_score_total"],
                label=row["financial_pressure_label"],
                reason=row["label_reason"] or "未触发两项以上规则",
            )
        )

    lines.extend(
        [
            "",
            "## 下一步机器学习安排",
            "",
            "1. 采集同业上市建筑企业 2021-2025 年财务指标，并复用本表字段。",
            "2. 将司法、执行、企查查样本按主体映射到同业公司年度，生成事件特征。",
            "3. 使用时间切分训练 Logistic Regression 和 Random Forest，报告 F1、Recall、AUC 与特征重要性。",
            "4. 将训练好的模型回代中国中铁，输出年度风险等级和主要驱动因素。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows = build_features()
    write_csv(rows)
    write_markdown(rows)
    print(f"wrote {OUTPUT_CSV} ({len(rows)} rows)")
    print(f"wrote {DOC_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
