"""Collect peer-company financial panel data from Eastmoney HSF10.

The panel is used for the machine-learning warning baseline. It complements,
but does not replace, China Railway's official annual-report extraction.
"""

from __future__ import annotations

import csv
import json
import math
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

import requests


ACCESS_DATE = date.today().isoformat()
BASE_URL = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew"
RAW_OUTPUT = Path("data/interim/peer_financial_panel_raw.json")
OUTPUT_CSV = Path("data/processed/peer_financial_panel.csv")
DOC_OUTPUT = Path("docs/PEER_FINANCIAL_PANEL.md")
START_YEAR = 2021
END_YEAR = 2025

PEERS = [
    {"query_code": "SH601390", "stock_code": "601390", "company_name": "中国中铁股份有限公司", "short_name": "中国中铁"},
    {"query_code": "SH601186", "stock_code": "601186", "company_name": "中国铁建股份有限公司", "short_name": "中国铁建"},
    {"query_code": "SH601800", "stock_code": "601800", "company_name": "中国交通建设股份有限公司", "short_name": "中国交建"},
    {"query_code": "SH601668", "stock_code": "601668", "company_name": "中国建筑股份有限公司", "short_name": "中国建筑"},
    {"query_code": "SH601669", "stock_code": "601669", "company_name": "中国电力建设股份有限公司", "short_name": "中国电建"},
    {"query_code": "SH601868", "stock_code": "601868", "company_name": "中国能源建设股份有限公司", "short_name": "中国能建"},
    {"query_code": "SH600170", "stock_code": "600170", "company_name": "上海建工集团股份有限公司", "short_name": "上海建工"},
    {"query_code": "SH600820", "stock_code": "600820", "company_name": "上海隧道工程股份有限公司", "short_name": "隧道股份"},
    {"query_code": "SH600502", "stock_code": "600502", "company_name": "安徽建工集团股份有限公司", "short_name": "安徽建工"},
    {"query_code": "SH601117", "stock_code": "601117", "company_name": "中国化学工程股份有限公司", "short_name": "中国化学"},
    {"query_code": "SH601618", "stock_code": "601618", "company_name": "中国冶金科工股份有限公司", "short_name": "中国中冶"},
]

FIELDNAMES = [
    "company_code",
    "company_name",
    "short_name",
    "secu_code",
    "year",
    "notice_date",
    "source_url",
    "access_date",
    "revenue_100m_rmb",
    "revenue_growth_pct",
    "parent_net_profit_100m_rmb",
    "parent_net_profit_growth_pct",
    "operating_cash_flow_to_revenue_pct",
    "asset_liability_ratio_pct",
    "current_ratio",
    "quick_ratio",
    "cash_ratio",
    "gross_margin_pct",
    "net_profit_margin_pct",
    "roe_weighted_pct",
    "receivable_turnover_days",
    "inventory_turnover_days",
    "payable_turnover_days",
    "interest_coverage_proxy",
    "liability_100m_rmb",
    "total_assets_estimated_100m_rmb",
    "staff_num",
]


def decimal_value(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return None


def decimal_text(value: Decimal | None, places: str = "0.0001") -> str:
    if value is None:
        return ""
    return str(value.quantize(Decimal(places)))


def ratio_to_pct(value: Decimal | None) -> Decimal | None:
    if value is None:
        return None
    return value * Decimal("100")


def amount_to_100m(value: Decimal | None) -> Decimal | None:
    if value is None:
        return None
    return value / Decimal("100000000")


def fetch_company(peer: dict[str, str]) -> list[dict[str, Any]]:
    params = {"type": "1", "code": peer["query_code"]}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://emweb.securities.eastmoney.com/",
    }
    response = requests.get(BASE_URL, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    payload = response.json()
    rows = payload.get("data") or []
    if not rows:
        raise ValueError(f"No rows returned for {peer['query_code']}")
    return rows


def normalize_row(peer: dict[str, str], raw: dict[str, Any]) -> dict[str, str] | None:
    year = int(raw["REPORT_YEAR"])
    if year < START_YEAR or year > END_YEAR:
        return None

    revenue = decimal_value(raw.get("TOTALOPERATEREVE"))
    profit = decimal_value(raw.get("PARENTNETPROFIT"))
    liability = decimal_value(raw.get("LIABILITY"))
    debt_ratio = decimal_value(raw.get("ZCFZL"))
    total_assets = None
    if liability is not None and debt_ratio not in (None, Decimal("0")):
        total_assets = liability / (debt_ratio / Decimal("100"))

    source_url = f"{BASE_URL}?type=1&code={peer['query_code']}"
    return {
        "company_code": peer["stock_code"],
        "company_name": peer["company_name"],
        "short_name": peer["short_name"],
        "secu_code": raw.get("SECUCODE", ""),
        "year": str(year),
        "notice_date": str(raw.get("NOTICE_DATE", ""))[:10],
        "source_url": source_url,
        "access_date": ACCESS_DATE,
        "revenue_100m_rmb": decimal_text(amount_to_100m(revenue), "0.01"),
        "revenue_growth_pct": decimal_text(decimal_value(raw.get("TOTALOPERATEREVETZ"))),
        "parent_net_profit_100m_rmb": decimal_text(amount_to_100m(profit), "0.01"),
        "parent_net_profit_growth_pct": decimal_text(decimal_value(raw.get("PARENTNETPROFITTZ"))),
        "operating_cash_flow_to_revenue_pct": decimal_text(ratio_to_pct(decimal_value(raw.get("JYXJLYYSR")))),
        "asset_liability_ratio_pct": decimal_text(debt_ratio),
        "current_ratio": decimal_text(decimal_value(raw.get("LD"))),
        "quick_ratio": decimal_text(decimal_value(raw.get("SD"))),
        "cash_ratio": decimal_text(decimal_value(raw.get("CASH_RATIO"))),
        "gross_margin_pct": decimal_text(decimal_value(raw.get("XSMLL"))),
        "net_profit_margin_pct": decimal_text(decimal_value(raw.get("XSJLL"))),
        "roe_weighted_pct": decimal_text(decimal_value(raw.get("ROEJQ"))),
        "receivable_turnover_days": decimal_text(decimal_value(raw.get("YSZKZZTS"))),
        "inventory_turnover_days": decimal_text(decimal_value(raw.get("CHZZTS"))),
        "payable_turnover_days": decimal_text(decimal_value(raw.get("PAYABLE_TDAYS"))),
        "interest_coverage_proxy": decimal_text(decimal_value(raw.get("INTEREST_COVERAGE_RATIO"))),
        "liability_100m_rmb": decimal_text(amount_to_100m(liability), "0.01"),
        "total_assets_estimated_100m_rmb": decimal_text(amount_to_100m(total_assets), "0.01"),
        "staff_num": str(raw.get("STAFF_NUM") or ""),
    }


def write_raw(raw_payloads: dict[str, list[dict[str, Any]]]) -> None:
    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    RAW_OUTPUT.write_text(json.dumps(raw_payloads, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(rows: list[dict[str, str]]) -> None:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def field_average(rows: list[dict[str, str]], field: str) -> str:
    values = []
    for row in rows:
        value = decimal_value(row.get(field))
        if value is not None and math.isfinite(float(value)):
            values.append(value)
    if not values:
        return ""
    return decimal_text(sum(values) / Decimal(len(values)))


def write_markdown(rows: list[dict[str, str]]) -> None:
    latest_rows = [row for row in rows if row["year"] == str(END_YEAR)]
    companies = sorted({row["short_name"] for row in rows})
    lines = [
        "# 同业上市建筑企业财务面板",
        "",
        "复现脚本：`scripts/collect_peer_financial_panel.py`",
        "",
        "## 数据来源与边界",
        "",
        f"- 数据来源：东方财富 HSF10 财务分析接口 `{BASE_URL}`。",
        f"- 访问日期：{ACCESS_DATE}。",
        f"- 样本期：{START_YEAR}-{END_YEAR} 年报。",
        f"- 样本公司：{len(companies)} 家建筑工程类 A 股上市公司。",
        "- 本数据用于机器学习预警基线模型；中国中铁核心结论仍优先使用官方年报抽取数据。",
        "- 东方财富口径中的利息保障倍数与公司年报债券章节口径可能不同，因此在模型中命名为 `interest_coverage_proxy`。",
        "",
        "## 样本规模",
        "",
        f"- 年度记录：{len(rows)} 条",
        f"- 公司数量：{len(companies)} 家",
        "",
        "## 公司清单",
        "",
        "| 股票代码 | 公司简称 | 公司全称 |",
        "|---|---|---|",
    ]
    for peer in PEERS:
        lines.append(f"| {peer['stock_code']} | {peer['short_name']} | {peer['company_name']} |")

    lines.extend(
        [
            "",
            f"## {END_YEAR} 年核心指标预览",
            "",
            "| 公司 | 营收增速(%) | 归母净利增速(%) | 资产负债率(%) | 经营现金流/营收(%) | 流动比率 | 利息保障倍数代理 |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in latest_rows:
        lines.append(
            "| {short_name} | {rev_g} | {profit_g} | {debt} | {ocf} | {current} | {interest} |".format(
                short_name=row["short_name"],
                rev_g=row["revenue_growth_pct"],
                profit_g=row["parent_net_profit_growth_pct"],
                debt=row["asset_liability_ratio_pct"],
                ocf=row["operating_cash_flow_to_revenue_pct"],
                current=row["current_ratio"],
                interest=row["interest_coverage_proxy"],
            )
        )

    lines.extend(
        [
            "",
            "## 2025 年样本均值",
            "",
            "| 指标 | 均值 |",
            "|---|---:|",
            f"| 营收增速(%) | {field_average(latest_rows, 'revenue_growth_pct')} |",
            f"| 归母净利增速(%) | {field_average(latest_rows, 'parent_net_profit_growth_pct')} |",
            f"| 资产负债率(%) | {field_average(latest_rows, 'asset_liability_ratio_pct')} |",
            f"| 经营现金流/营收(%) | {field_average(latest_rows, 'operating_cash_flow_to_revenue_pct')} |",
            f"| 流动比率 | {field_average(latest_rows, 'current_ratio')} |",
            f"| 利息保障倍数代理 | {field_average(latest_rows, 'interest_coverage_proxy')} |",
            "",
            "## 后续用途",
            "",
            "- `data/processed/peer_financial_panel.csv` 是训练财务风险预警基线模型的输入。",
            "- 模型标签使用下一年度压力规则构造，避免用未来数据作为当期特征。",
            "- 后续若能获得同业司法、执行和文本风险数据，可在该面板基础上继续追加事件和文本特征。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    raw_payloads: dict[str, list[dict[str, Any]]] = {}
    rows: list[dict[str, str]] = []
    for peer in PEERS:
        raw_rows = fetch_company(peer)
        raw_payloads[peer["query_code"]] = raw_rows
        for raw in raw_rows:
            normalized = normalize_row(peer, raw)
            if normalized is not None:
                rows.append(normalized)

    rows.sort(key=lambda row: (row["company_code"], row["year"]))
    write_raw(raw_payloads)
    write_csv(rows)
    write_markdown(rows)
    print(f"wrote {OUTPUT_CSV} ({len(rows)} rows)")
    print(f"wrote {RAW_OUTPUT}")
    print(f"wrote {DOC_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
