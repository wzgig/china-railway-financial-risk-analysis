# -*- coding: utf-8 -*-
"""
用途：整理公开资料来源清单，检查 URL 可访问性，生成后续建模可引用的来源索引。
输入：data/raw/source_manifest.csv
输出：data/interim/source_check.csv，logs/01_collect_public_sources.log
说明：链接检查结果只用于记录资料可追溯性；网络不可达不代表来源无效。
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "source_manifest.csv"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
LOG_DIR = PROJECT_ROOT / "logs"
OUTPUT_PATH = INTERIM_DIR / "source_check.csv"
LOG_PATH = LOG_DIR / "01_collect_public_sources.log"

REQUIRED_COLUMNS = [
    "source_id",
    "source_name",
    "source_type",
    "publisher",
    "publish_date",
    "access_date",
    "url",
    "used_for",
    "evidence_level",
    "note",
]


def ensure_directories() -> None:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def read_manifest() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"找不到来源清单：{RAW_PATH.relative_to(PROJECT_ROOT)}")

    df = pd.read_csv(RAW_PATH, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"source_manifest.csv 缺少字段：{', '.join(missing)}")

    if df["source_id"].duplicated().any():
        duplicates = df.loc[df["source_id"].duplicated(), "source_id"].tolist()
        raise ValueError(f"source_id 存在重复：{duplicates}")

    return df[REQUIRED_COLUMNS].copy()


def check_url(url: str, timeout: int = 12) -> dict[str, Any]:
    url = (url or "").strip()
    if not url:
        return {
            "url_domain": "",
            "http_status": "",
            "reachable": False,
            "content_type": "",
            "final_url": "",
            "check_message": "missing_url",
        }

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return {
            "url_domain": parsed.netloc,
            "http_status": "",
            "reachable": False,
            "content_type": "",
            "final_url": url,
            "check_message": "invalid_url",
        }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0 Safari/537.36"
        )
    }

    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout, headers=headers)
        if response.status_code in {403, 405} or response.status_code >= 500:
            response = requests.get(url, allow_redirects=True, timeout=timeout, headers=headers, stream=True)

        status = int(response.status_code)
        return {
            "url_domain": urlparse(response.url).netloc or parsed.netloc,
            "http_status": status,
            "reachable": 200 <= status < 400,
            "content_type": response.headers.get("content-type", ""),
            "final_url": response.url,
            "check_message": "ok" if 200 <= status < 400 else f"http_{status}",
        }
    except requests.RequestException as exc:
        return {
            "url_domain": parsed.netloc,
            "http_status": "",
            "reachable": False,
            "content_type": "",
            "final_url": url,
            "check_message": exc.__class__.__name__,
        }


def build_source_check(df: pd.DataFrame) -> pd.DataFrame:
    checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    records: list[dict[str, Any]] = []

    for row in df.to_dict(orient="records"):
        result = check_url(row["url"])
        citation_parts = [row["publisher"], row["source_name"], row["publish_date"]]
        citation_label = "，".join(part for part in citation_parts if part)
        records.append(
            {
                **row,
                **result,
                "checked_at": checked_at,
                "citation_label": citation_label,
                "modeling_use": row["used_for"],
            }
        )

    return pd.DataFrame(records)


def write_log(source_check: pd.DataFrame) -> None:
    total = len(source_check)
    reachable = int(source_check["reachable"].sum()) if total else 0
    by_level = source_check["evidence_level"].value_counts().to_dict()
    lines = [
        f"运行时间：{datetime.now():%Y-%m-%d %H:%M:%S}",
        f"来源数量：{total}",
        f"可访问链接：{reachable}",
        f"证据等级分布：{by_level}",
        "说明：链接检查受网络环境影响，失败项需在报告中按来源清单继续保留可追溯编号。",
    ]
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_directories()
    manifest = read_manifest()
    source_check = build_source_check(manifest)
    source_check.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig",
        quoting=csv.QUOTE_MINIMAL,
    )
    write_log(source_check)

    print(f"已生成：{OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"来源数量：{len(source_check)}；可访问：{int(source_check['reachable'].sum())}")


if __name__ == "__main__":
    main()
