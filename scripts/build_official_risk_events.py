"""Build a seed risk-event table from official disclosures.

The output is intentionally conservative: it uses annual-report financial
signals, annual-report contingent items, and the public rating report only.
Legal/commercial platform data should be appended later through the compliant
collection template.
"""

from __future__ import annotations

import csv
import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path


SCHEMA_PATH = Path("configs/risk_event_schema.json")
FINANCIAL_CSV = Path("data/processed/financial_risk_indicators.csv")
TEXT_DIR = Path("data/interim/annual_report_text")
OUTPUT_CSV = Path("data/interim/risk_events_official_seed.csv")
DOC_OUTPUT = Path("docs/OFFICIAL_RISK_EVENTS_SAMPLE.md")
ACCESS_DATE = "2026-06-29"
RMB_1000_YI = Decimal(100_000_000_000)
RMB_500_YI = Decimal(50_000_000_000)
RMB_100_YI = Decimal(10_000_000_000)


def load_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def schema_fields(schema: dict[str, object]) -> list[str]:
    return [field["name"] for field in schema["fields"]]


def decimal_or_none(value: str | None) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def amount_from_100m(value: str | Decimal | None) -> str:
    dec = decimal_or_none(str(value)) if value is not None else None
    if dec is None:
        return ""
    return str(int(dec * Decimal("100000000")))


def amount_from_thousand(value: str) -> str:
    return str(int(value.replace(",", "")) * 1000)


def amount_to_100m_text(amount_rmb: str) -> str:
    if not amount_rmb:
        return ""
    value = Decimal(amount_rmb) / Decimal("100000000")
    return f"{value.quantize(Decimal('0.01'))}"


def base_event(event_id: str, year: int, event_type: str, risk_type: str) -> dict[str, str]:
    return {
        "event_id": event_id,
        "source_type": "annual_report",
        "source_name": f"中国中铁{year}年年度报告",
        "source_url": f"data/raw/annual_reports/{year}_annual_report.pdf",
        "access_date": ACCESS_DATE,
        "search_keyword": "中国中铁 年度报告 风险",
        "company_name": "中国中铁股份有限公司",
        "company_role": "issuer",
        "related_party": "",
        "event_type": event_type,
        "risk_type": risk_type,
        "event_date": f"{year}-12-31",
        "year": str(year),
        "province": "",
        "city": "",
        "case_no": "",
        "cause": "",
        "amount_rmb": "",
        "summary": "",
        "severity_score": "3",
        "probability_score": "3",
        "evidence_status": "core",
        "notes": "Official annual-report seed event; verify before using as final legal-event evidence.",
    }


def severity_from_amount(amount_rmb: str) -> str:
    if not amount_rmb:
        return "2"
    amount = Decimal(amount_rmb)
    if amount >= RMB_1000_YI:
        return "5"
    if amount >= RMB_500_YI:
        return "4"
    if amount >= RMB_100_YI:
        return "3"
    return "2"


def build_financial_signal_events() -> list[dict[str, str]]:
    if not FINANCIAL_CSV.exists():
        raise FileNotFoundError(f"Missing {FINANCIAL_CSV}")

    events: list[dict[str, str]] = []
    with FINANCIAL_CSV.open("r", newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            year = int(row["year"])
            revenue_growth = decimal_or_none(row.get("revenue_growth_pct"))
            profit_growth = decimal_or_none(row.get("net_profit_parent_growth_pct"))
            debt_ratio = decimal_or_none(row.get("asset_liability_ratio_pct"))
            interest_coverage = decimal_or_none(row.get("interest_coverage"))
            contract_assets_ratio = decimal_or_none(row.get("contract_assets_to_assets_pct"))

            if revenue_growth is not None and profit_growth is not None and (revenue_growth < 0 or profit_growth < 0):
                event = base_event(f"OF{year}-PROFIT", year, "financial_pressure", "profitability")
                event["cause"] = "营业收入或归母净利润同比下降"
                event["amount_rmb"] = amount_from_100m(row.get("net_profit_parent_100m_rmb"))
                event["summary"] = (
                    f"年报主要指标显示，营业收入同比{revenue_growth}%、"
                    f"归母净利润同比{profit_growth}%，盈利下行进入风险样本。"
                )
                event["severity_score"] = "4" if profit_growth <= Decimal("-15") else "3"
                event["probability_score"] = "4"
                events.append(event)

            if year >= 2024 and debt_ratio is not None and debt_ratio >= Decimal("77"):
                event = base_event(f"OF{year}-SOLVENCY", year, "financial_pressure", "solvency")
                event["cause"] = "资产负债率较高且利息保障倍数下降"
                event["summary"] = (
                    f"年报债券章节显示，资产负债率为{debt_ratio}%，"
                    f"利息保障倍数为{interest_coverage}，作为偿债压力预警信号。"
                )
                event["severity_score"] = "4"
                event["probability_score"] = "4"
                events.append(event)

            if year >= 2024 and contract_assets_ratio is not None and contract_assets_ratio >= Decimal("14"):
                event = base_event(f"OF{year}-CONTRACT-ASSET", year, "asset_quality_signal", "operation")
                event["cause"] = "应收账款和合同资产占用较高"
                event["amount_rmb"] = amount_from_100m(row.get("contract_assets_100m_rmb"))
                event["summary"] = (
                    f"年报资产分析显示，合同资产约{row.get('contract_assets_100m_rmb')}亿元，"
                    f"占总资产{contract_assets_ratio}%，回款和资产质量需要跟踪。"
                )
                event["severity_score"] = "4"
                event["probability_score"] = "4"
                events.append(event)

    return events


def extract_first_amount(text: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.S)
        if match:
            return amount_from_thousand(match.group(1))
    return ""


def build_contingency_events() -> list[dict[str, str]]:
    events: list[dict[str, str]] = []
    litigation_pattern = r"未决诉讼\s+([\d,]+)"
    guarantee_patterns = [
        r"对外实际担保和差额补足承诺金额为人民币\s*([\d,]+)\s*千元",
        r"表外的最大信用风险敞口为履行财务担保及差额补足承诺所需支付的最大金额人民币\s*([\d,]+)\s*千元",
        r"最大金额人民币\s*([\d,]+)\s*千元",
    ]

    for year in range(2021, 2026):
        text_path = TEXT_DIR / f"{year}_annual_report.txt"
        if not text_path.exists():
            continue
        text = text_path.read_text(encoding="utf-8", errors="replace")

        litigation_amount = extract_first_amount(text, [litigation_pattern])
        if litigation_amount:
            event = base_event(f"OF{year}-LITIGATION", year, "litigation_contingency", "compliance")
            event["related_party"] = "客户、分包商、供应商等"
            event["company_role"] = "reporting_group"
            event["cause"] = "重大未决诉讼仲裁形成的或有负债"
            event["amount_rmb"] = litigation_amount
            event["summary"] = (
                f"年报或有事项披露，已发生但尚不符合负债确认条件的未决诉讼"
                f"年末诉讼标的金额约{amount_to_100m_text(litigation_amount)}亿元。"
            )
            event["severity_score"] = severity_from_amount(litigation_amount)
            event["probability_score"] = "3"
            events.append(event)

        guarantee_amount = extract_first_amount(text, guarantee_patterns)
        if guarantee_amount:
            event = base_event(f"OF{year}-GUARANTEE", year, "guarantee", "organizational_propagation")
            event["related_party"] = "集团内子公司、房地产项目购房业主等"
            event["company_role"] = "guarantor_or_support_provider"
            event["cause"] = "对外实际担保和差额补足承诺"
            event["amount_rmb"] = guarantee_amount
            event["summary"] = (
                f"年报披露对外实际担保、房地产按揭担保和差额补足承诺，"
                f"最大风险敞口约{amount_to_100m_text(guarantee_amount)}亿元。"
            )
            event["severity_score"] = severity_from_amount(guarantee_amount)
            event["probability_score"] = "2"
            events.append(event)

    return events


def build_rating_event() -> dict[str, str]:
    event = base_event("OF2025-RATING", 2025, "rating_action", "solvency")
    event.update(
        {
            "source_type": "rating_report",
            "source_name": "联合资信：中国中铁股份有限公司2025年跟踪评级报告",
            "source_url": "https://www.lhratings.com/reports/B0411-P76587-2024-GZ2025.pdf",
            "event_date": "2025-05-07",
            "search_keyword": "中国中铁 2025 跟踪评级",
            "cause": "主体及相关债项评级维持AAA/稳定",
            "summary": (
                "联合资信维持主体及相关债项AAA/稳定，同时提示PPP项目运营及回款、"
                "应收账款、合同资产、存货和长期应收款资金占用、短期偿债指标弱化等关注点。"
            ),
            "severity_score": "2",
            "probability_score": "3",
            "notes": "Rating action is credit-support evidence and a source of risk concerns, not a default event.",
        }
    )
    return event


def validate_events(events: list[dict[str, str]], schema: dict[str, object]) -> None:
    allowed_event_types = set(schema["event_types"])
    allowed_risk_types = set(schema["risk_types"])
    required_fields = [field["name"] for field in schema["fields"] if field["required"]]
    for event in events:
        missing = [field for field in required_fields if not event.get(field)]
        if missing:
            raise ValueError(f"{event.get('event_id')} missing required fields: {missing}")
        if event["event_type"] not in allowed_event_types:
            raise ValueError(f"{event['event_id']} has invalid event_type {event['event_type']}")
        if event["risk_type"] not in allowed_risk_types:
            raise ValueError(f"{event['event_id']} has invalid risk_type {event['risk_type']}")


def write_events_csv(events: list[dict[str, str]], fields: list[str]) -> Path:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(events)
    return OUTPUT_CSV


def write_markdown(events: list[dict[str, str]]) -> Path:
    lines = [
        "# 官方披露风险事件种子样本",
        "",
        "生成脚本：`scripts/build_official_risk_events.py`",
        "",
        "## 样本边界",
        "",
        "- 本表仅来自中国中铁年报、财务指标整理结果和联合资信跟踪评级报告。",
        "- 当前样本用于搭建风险图谱结构，不替代裁判文书、执行信息或企业风险平台的逐条事件核验。",
        "- 金额均按人民币元进入本地 CSV；下表为便于阅读换算为亿元。",
        "",
        "## 样本摘要",
        "",
        "| 事件ID | 年份 | 事件类型 | 风险类型 | 金额(亿元) | 摘要 |",
        "|---|---:|---|---|---:|---|",
    ]
    for event in events:
        lines.append(
            "| {event_id} | {year} | {event_type} | {risk_type} | {amount} | {summary} |".format(
                event_id=event["event_id"],
                year=event["year"],
                event_type=event["event_type"],
                risk_type=event["risk_type"],
                amount=amount_to_100m_text(event["amount_rmb"]) or "",
                summary=event["summary"],
            )
        )

    lines.extend(
        [
            "",
            "## 后续用法",
            "",
            "- 本地完整事件表：`data/interim/risk_events_official_seed.csv`，不纳入公开仓库。",
            "- 下一步可将人工核验的司法、执行、公告和企业风险事件追加到同一字段结构。",
            "- 图谱脚本会把 `company_name`、`event_id`、`risk_type`、`year`、`related_party` 转换为节点，并按影响程度与概率评分生成边权重。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return DOC_OUTPUT


def main() -> int:
    schema = load_schema()
    events = build_financial_signal_events()
    events.extend(build_contingency_events())
    events.append(build_rating_event())
    events.sort(key=lambda event: (event["year"], event["event_id"]))
    validate_events(events, schema)
    csv_path = write_events_csv(events, schema_fields(schema))
    doc_path = write_markdown(events)
    print(f"wrote {csv_path} ({len(events)} events)")
    print(f"wrote {doc_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
