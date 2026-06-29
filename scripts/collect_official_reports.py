"""Collect official China Railway periodic reports from public pages.

The script only downloads publicly linked PDF files from the official CREC
website and a manually specified rating report URL. It does not access logged-in
or restricted systems.
"""

from __future__ import annotations

import csv
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen


BASE_URL = "https://www.crec.cn"
LIST_PAGES = [
    "/web/tzzgx26/dqbg/ag46/index.html",
    "/web/tzzgx26/dqbg/ag46/daebd28d-2.html",
    "/web/tzzgx26/dqbg/ag46/daebd28d-3.html",
]

MANUAL_REPORTS = [
    {
        "period": "2025",
        "report_type": "rating",
        "title": "中国中铁股份有限公司2025年跟踪评级报告",
        "date": "2025-05-07",
        "source": "联合资信评估股份有限公司",
        "url": "https://www.lhratings.com/reports/B0411-P76587-2024-GZ2025.pdf",
        "filename": "2025_lianhe_rating_report.pdf",
    }
]

TARGETS = {
    "中国中铁2026年第一季度报告": ("2026Q1", "quarterly", "2026_q1_report.pdf"),
    "中国中铁2025年年度报告": ("2025", "annual", "2025_annual_report.pdf"),
    "中国中铁2024年年度报告": ("2024", "annual", "2024_annual_report.pdf"),
    "中国中铁2023年年度报告": ("2023", "annual", "2023_annual_report.pdf"),
    "中国中铁2022年年度报告": ("2022", "annual", "2022_annual_report.pdf"),
    "中国中铁2021年年度报告": ("2021", "annual", "2021_annual_report.pdf"),
}


def safe_url(url: str) -> str:
    parts = urlsplit(url)
    path = quote(parts.path, safe="/%")
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, parts.fragment))


def fetch_text(url: str) -> str:
    req = Request(
        safe_url(url),
        headers={"User-Agent": "Mozilla/5.0 financial-risk-course-project"},
    )
    with urlopen(req, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def fetch_binary(url: str) -> bytes:
    req = Request(
        safe_url(url),
        headers={"User-Agent": "Mozilla/5.0 financial-risk-course-project"},
    )
    with urlopen(req, timeout=60) as response:
        return response.read()


def clean_html(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()


def parse_list_pages() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    pattern = re.compile(
        r'<li class="clearfix"><a href="(?P<href>[^"]+)"[^>]*>'
        r"(?P<title>.*?)</a><span>(?P<date>[^<]+)</span></li>",
        re.IGNORECASE | re.DOTALL,
    )

    for page in LIST_PAGES:
        html = fetch_text(urljoin(BASE_URL, page))
        for match in pattern.finditer(html):
            title = clean_html(match.group("title"))
            if title not in TARGETS:
                continue
            period, report_type, filename = TARGETS[title]
            rows.append(
                {
                    "period": period,
                    "report_type": report_type,
                    "title": title,
                    "date": match.group("date").strip(),
                    "source": "中国中铁股份有限公司官网",
                    "url": urljoin(BASE_URL, match.group("href")),
                    "filename": filename,
                }
            )
    deduped = {row["filename"]: row for row in rows}
    return list(deduped.values())


def write_manifest(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["period", "report_type", "title", "date", "source", "url", "filename"]
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def download_reports(rows: list[dict[str, str]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for row in rows:
        target = output_dir / row["filename"]
        if target.exists() and target.stat().st_size > 0:
            print(f"skip existing: {target}")
            continue
        print(f"download: {row['title']} -> {target}")
        target.write_bytes(fetch_binary(row["url"]))
        time.sleep(1)


def main() -> int:
    rows = parse_list_pages() + MANUAL_REPORTS
    rows = sorted(rows, key=lambda item: (item["period"], item["report_type"]), reverse=True)
    manifest = Path("data/interim/official_reports_manifest.csv")
    write_manifest(rows, manifest)
    download_reports(rows, Path("data/raw/annual_reports"))
    print(f"wrote manifest: {manifest}")
    print(f"reports: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
