"""Build a financial-risk indicator dataset from official annual reports.

The current version uses values verified from the annual report tables and
keeps source checks against local PDF text extracted by `pdftotext`.
Amounts disclosed in the reports are in thousand RMB; this script outputs
RMB 100 million for readability.
"""

from __future__ import annotations

import csv
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


RAW_DIR = Path("data/raw/annual_reports")
TEXT_DIR = Path("data/interim/annual_report_text")
PROCESSED_DIR = Path("data/processed")
DOCS_DIR = Path("docs")

REPORT_FILES = {
    2025: RAW_DIR / "2025_annual_report.pdf",
    2024: RAW_DIR / "2024_annual_report.pdf",
    2023: RAW_DIR / "2023_annual_report.pdf",
    2022: RAW_DIR / "2022_annual_report.pdf",
    2021: RAW_DIR / "2021_annual_report.pdf",
}


@dataclass(frozen=True)
class IndicatorInput:
    year: int
    revenue_thousand: int
    net_profit_parent_thousand: int
    net_profit_parent_ex_nonrecurring_thousand: int
    operating_cash_flow_thousand: int
    equity_parent_thousand: int
    total_assets_thousand: int
    asset_liability_ratio_pct: float
    accounts_receivable_thousand: int
    contract_assets_thousand: int
    interest_coverage: float
    cash_interest_coverage: float
    ebitda_interest_coverage: float
    source_note: str


INDICATORS = [
    IndicatorInput(
        year=2025,
        revenue_thousand=1_090_626_001,
        net_profit_parent_thousand=22_891_703,
        net_profit_parent_ex_nonrecurring_thousand=17_664_407,
        operating_cash_flow_thousand=28_771_766,
        equity_parent_thousand=371_062_821,
        total_assets_thousand=2_470_580_585,
        asset_liability_ratio_pct=78.12,
        accounts_receivable_thousand=288_877_597,
        contract_assets_thousand=366_844_960,
        interest_coverage=2.98,
        cash_interest_coverage=3.24,
        ebitda_interest_coverage=4.18,
        source_note="2025 annual report; 2025 bond section; management discussion asset analysis",
    ),
    IndicatorInput(
        year=2024,
        revenue_thousand=1_157_439_041,
        net_profit_parent_thousand=27_886_745,
        net_profit_parent_ex_nonrecurring_thousand=24_325_141,
        operating_cash_flow_thousand=28_051_091,
        equity_parent_thousand=354_714_424,
        total_assets_thousand=2_256_413_630,
        asset_liability_ratio_pct=77.39,
        accounts_receivable_thousand=246_194_352,
        contract_assets_thousand=333_119_548,
        interest_coverage=3.17,
        cash_interest_coverage=3.09,
        ebitda_interest_coverage=4.04,
        source_note="2025 annual report and 2024 annual report restated tables",
    ),
    IndicatorInput(
        year=2023,
        revenue_thousand=1_260_841_083,
        net_profit_parent_thousand=33_482_775,
        net_profit_parent_ex_nonrecurring_thousand=30_872_445,
        operating_cash_flow_thousand=38_363_495,
        equity_parent_thousand=332_533_508,
        total_assets_thousand=1_829_439_189,
        asset_liability_ratio_pct=74.86,
        accounts_receivable_thousand=156_851_816,
        contract_assets_thousand=234_190_925,
        interest_coverage=3.73,
        cash_interest_coverage=3.78,
        ebitda_interest_coverage=4.53,
        source_note="2025, 2024 and 2023 annual report restated tables",
    ),
    IndicatorInput(
        year=2022,
        revenue_thousand=1_151_501_114,
        net_profit_parent_thousand=31_272_886,
        net_profit_parent_ex_nonrecurring_thousand=28_246_828,
        operating_cash_flow_thousand=43_551_945,
        equity_parent_thousand=301_205_054,
        total_assets_thousand=1_613_282_322,
        asset_liability_ratio_pct=73.77,
        accounts_receivable_thousand=122_237_789,
        contract_assets_thousand=169_734_586,
        interest_coverage=3.82,
        cash_interest_coverage=4.40,
        ebitda_interest_coverage=4.58,
        source_note="2024 and 2023 annual report restated tables",
    ),
    IndicatorInput(
        year=2021,
        revenue_thousand=1_070_417_452,
        net_profit_parent_thousand=27_617_610,
        net_profit_parent_ex_nonrecurring_thousand=25_914_204,
        operating_cash_flow_thousand=13_069_466,
        equity_parent_thousand=275_248_367,
        total_assets_thousand=1_361_830_150,
        asset_liability_ratio_pct=73.68,
        accounts_receivable_thousand=122_120_354,
        contract_assets_thousand=149_141_915,
        interest_coverage=4.09,
        cash_interest_coverage=2.81,
        ebitda_interest_coverage=4.99,
        source_note="2023 and 2022 annual report restated/comparative tables",
    ),
]

SOURCE_CHECK_TERMS = {
    2025: ["1,090,626,001", "78.12", "288,877,597", "366,844,960", "利息保障倍数"],
    2024: ["1,157,439,041", "77.39", "246,194,352", "333,119,548", "利息保障倍数"],
    2023: ["1,260,841,083", "74.86", "156,851,816", "234,190,925", "利息保障倍数"],
    2022: ["1,151,501,114", "73.77", "122,237,789", "169,734,586", "利息保障倍数"],
    2021: ["1,070,417,452", "73.68", "122,120,354", "149,141,915", "利息保障倍数"],
}


def amount_to_100m(thousand_rmb: int) -> float:
    return round(thousand_rmb / 100_000, 2)


def pct(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator * 100, 2)


def ensure_text_cache() -> list[str]:
    TEXT_DIR.mkdir(parents=True, exist_ok=True)
    messages: list[str] = []
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        return ["pdftotext not found; source text cache was not regenerated"]

    for year, pdf_path in REPORT_FILES.items():
        txt_path = TEXT_DIR / f"{year}_annual_report.txt"
        if not pdf_path.exists():
            messages.append(f"missing PDF for {year}: {pdf_path}")
            continue
        subprocess.run(
            [pdftotext, "-layout", "-enc", "UTF-8", str(pdf_path), str(txt_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        messages.append(f"generated text cache for {year}: {txt_path}")
    return messages


def verify_source_terms() -> list[str]:
    messages: list[str] = []
    for year, terms in SOURCE_CHECK_TERMS.items():
        txt_path = TEXT_DIR / f"{year}_annual_report.txt"
        if not txt_path.exists():
            messages.append(f"{year}: missing text cache")
            continue
        text = txt_path.read_text(encoding="utf-8", errors="replace")
        missing = [term for term in terms if term not in text]
        if missing:
            messages.append(f"{year}: missing terms {missing}")
        else:
            messages.append(f"{year}: all source terms found")
    return messages


def build_rows() -> list[dict[str, str | int | float]]:
    by_year = {item.year: item for item in INDICATORS}
    rows: list[dict[str, str | int | float]] = []
    for item in sorted(INDICATORS, key=lambda row: row.year):
        previous = by_year.get(item.year - 1)
        revenue_100m = amount_to_100m(item.revenue_thousand)
        net_profit_100m = amount_to_100m(item.net_profit_parent_thousand)
        operating_cash_flow_100m = amount_to_100m(item.operating_cash_flow_thousand)
        total_assets_100m = amount_to_100m(item.total_assets_thousand)

        revenue_growth = ""
        net_profit_growth = ""
        total_assets_growth = ""
        if previous:
            revenue_growth = pct(item.revenue_thousand - previous.revenue_thousand, previous.revenue_thousand)
            net_profit_growth = pct(
                item.net_profit_parent_thousand - previous.net_profit_parent_thousand,
                previous.net_profit_parent_thousand,
            )
            total_assets_growth = pct(
                item.total_assets_thousand - previous.total_assets_thousand,
                previous.total_assets_thousand,
            )

        rows.append(
            {
                "year": item.year,
                "revenue_100m_rmb": revenue_100m,
                "revenue_growth_pct": revenue_growth,
                "net_profit_parent_100m_rmb": net_profit_100m,
                "net_profit_parent_growth_pct": net_profit_growth,
                "net_profit_parent_ex_nonrecurring_100m_rmb": amount_to_100m(
                    item.net_profit_parent_ex_nonrecurring_thousand
                ),
                "operating_cash_flow_100m_rmb": operating_cash_flow_100m,
                "operating_cash_flow_to_revenue_pct": pct(
                    item.operating_cash_flow_thousand,
                    item.revenue_thousand,
                ),
                "equity_parent_100m_rmb": amount_to_100m(item.equity_parent_thousand),
                "total_assets_100m_rmb": total_assets_100m,
                "total_assets_growth_pct": total_assets_growth,
                "asset_liability_ratio_pct": item.asset_liability_ratio_pct,
                "accounts_receivable_100m_rmb": amount_to_100m(item.accounts_receivable_thousand),
                "accounts_receivable_to_assets_pct": pct(
                    item.accounts_receivable_thousand,
                    item.total_assets_thousand,
                ),
                "contract_assets_100m_rmb": amount_to_100m(item.contract_assets_thousand),
                "contract_assets_to_assets_pct": pct(item.contract_assets_thousand, item.total_assets_thousand),
                "interest_coverage": item.interest_coverage,
                "cash_interest_coverage": item.cash_interest_coverage,
                "ebitda_interest_coverage": item.ebitda_interest_coverage,
                "source_files": f"{item.year}_annual_report.pdf",
                "source_note": item.source_note,
            }
        )
    return rows


def write_csv(rows: list[dict[str, str | int | float]]) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output = PROCESSED_DIR / "financial_risk_indicators.csv"
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return output


def write_markdown(rows: list[dict[str, str | int | float]], source_messages: list[str]) -> Path:
    output = DOCS_DIR / "FINANCIAL_RISK_INDICATORS.md"
    headers = [
        "年份",
        "营业收入",
        "收入增速",
        "归母净利润",
        "归母净利增速",
        "经营现金流",
        "资产负债率",
        "应收账款/总资产",
        "合同资产/总资产",
        "利息保障倍数",
    ]
    keys = [
        "year",
        "revenue_100m_rmb",
        "revenue_growth_pct",
        "net_profit_parent_100m_rmb",
        "net_profit_parent_growth_pct",
        "operating_cash_flow_100m_rmb",
        "asset_liability_ratio_pct",
        "accounts_receivable_to_assets_pct",
        "contract_assets_to_assets_pct",
        "interest_coverage",
    ]

    def fmt(value: object) -> str:
        return "" if value == "" else str(value)

    lines = [
        "# 中国中铁财务风险指标数据集",
        "",
        "复现脚本：`scripts/extract_financial_indicators.py`",
        "",
        "单位说明：金额单位为亿元人民币；比例单位为 `%`；利息保障倍数为倍。",
        "",
        "## 指标表",
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row[key]) for key in keys) + " |")

    lines.extend(
        [
            "",
            "## 初步风险观察",
            "",
            "1. 2023 年后营业收入连续下降，2025 年收入较 2024 年下降，规模扩张动能转弱。",
            "2. 归母净利润从 2023 年的 334.83 亿元下降到 2025 年的 228.92 亿元，盈利压力明显。",
            "3. 资产负债率从 2021 年的 73.68% 上升至 2025 年的 78.12%，债务和流动性管理压力上升。",
            "4. 应收账款和合同资产占总资产比例较高，说明回款、结算和资产质量是后续风险评估重点。",
            "5. 利息保障倍数由 2021 年的 4.09 降至 2025 年的 2.98，需结合债券期限、融资成本和现金流继续跟踪。",
            "",
            "## 数据口径",
            "",
            "- 主要会计数据优先采用最新年报中的追溯调整或重述口径。",
            "- 2021-2022 年部分数据使用后续年报中的比较期重述值，以保持可比性。",
            "- 原始 PDF 保存在 `data/raw/annual_reports/`，结构化 CSV 输出到 `data/processed/financial_risk_indicators.csv`。",
            "",
            "## 来源校验",
            "",
        ]
    )
    for message in source_messages:
        lines.append(f"- {message}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def main() -> int:
    cache_messages = ensure_text_cache()
    verification_messages = verify_source_terms()
    rows = build_rows()
    csv_path = write_csv(rows)
    md_path = write_markdown(rows, cache_messages + verification_messages)
    print(f"wrote {csv_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
