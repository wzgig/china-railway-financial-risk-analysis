"""Extract seed-term risk text snippets from annual report text caches."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


CONFIG_PATH = Path("configs/risk_seed_terms.json")
TEXT_DIR = Path("data/interim/annual_report_text")
INTERIM_DIR = Path("data/interim")
DOCS_DIR = Path("docs")


def normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line).strip()


def load_terms() -> dict[str, dict[str, object]]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def iter_text_lines() -> list[tuple[int, str, int, str]]:
    rows: list[tuple[int, str, int, str]] = []
    for path in sorted(TEXT_DIR.glob("*_annual_report.txt")):
        match = re.match(r"(?P<year>\d{4})_annual_report\.txt", path.name)
        if not match:
            continue
        year = int(match.group("year"))
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line_no, line in enumerate(lines, start=1):
            clean = normalize_line(line)
            if len(clean) >= 8:
                rows.append((year, path.name, line_no, clean))
    return rows


def extract_snippets(
    terms_config: dict[str, dict[str, object]],
    text_rows: list[tuple[int, str, int, str]],
) -> list[dict[str, str | int]]:
    output: list[dict[str, str | int]] = []
    seen: set[tuple[int, str, int, str, str]] = set()
    for year, source_file, line_no, line in text_rows:
        for category, meta in terms_config.items():
            label = str(meta["label"])
            for term in meta["terms"]:
                term = str(term)
                if term in line:
                    key = (year, source_file, line_no, category, term)
                    if key in seen:
                        continue
                    seen.add(key)
                    output.append(
                        {
                            "year": year,
                            "source_file": source_file,
                            "line_no": line_no,
                            "risk_category": category,
                            "risk_label": label,
                            "matched_term": term,
                            "snippet": line[:280],
                        }
                    )
    return output


def write_snippets(rows: list[dict[str, str | int]]) -> Path:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    output = INTERIM_DIR / "risk_text_corpus_seed_matches.csv"
    fieldnames = [
        "year",
        "source_file",
        "line_no",
        "risk_category",
        "risk_label",
        "matched_term",
        "snippet",
    ]
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output


def build_summary(rows: list[dict[str, str | int]]) -> str:
    by_year_category: dict[int, Counter[str]] = defaultdict(Counter)
    by_category_term: dict[str, Counter[str]] = defaultdict(Counter)
    label_by_category: dict[str, str] = {}

    for row in rows:
        year = int(row["year"])
        category = str(row["risk_category"])
        label = str(row["risk_label"])
        term = str(row["matched_term"])
        by_year_category[year][category] += 1
        by_category_term[category][term] += 1
        label_by_category[category] = label

    categories = sorted(label_by_category)
    years = sorted(by_year_category)
    lines = [
        "# 年报文本风险语料初筛摘要",
        "",
        "复现脚本：`scripts/extract_risk_text_corpus.py`",
        "",
        "本文件基于 `configs/risk_seed_terms.json` 的种子词，在 2021-2025 年年报文本缓存中抽取命中片段。它是后续 jieba 分词、Word2Vec 扩词和风险词频权重计算的前置语料，不等同于最终风险得分。",
        "",
        "## 年度-风险类别命中次数",
        "",
        "| 年份 | " + " | ".join(label_by_category[category] for category in categories) + " |",
        "| --- | " + " | ".join(["---:"] * len(categories)) + " |",
    ]
    for year in years:
        counts = [str(by_year_category[year][category]) for category in categories]
        lines.append(f"| {year} | " + " | ".join(counts) + " |")

    lines.extend(["", "## 高频种子词", ""])
    for category in categories:
        label = label_by_category[category]
        top_terms = by_category_term[category].most_common(8)
        rendered = "；".join(f"{term}({count})" for term, count in top_terms)
        lines.append(f"- {label}：{rendered}")

    lines.extend(
        [
            "",
            "## 使用说明",
            "",
            "- 命中次数受年报篇幅和排版影响，只能作为语料覆盖度参考。",
            "- 后续需要使用 jieba 分词、停用词清理和 Word2Vec 相似词扩充，形成更稳健的风险词典。",
            "- 最终风险评估应结合财务指标、事件数据和图谱中心性，避免只用文本频次下结论。",
        ]
    )
    return "\n".join(lines) + "\n"


def write_summary(rows: list[dict[str, str | int]]) -> Path:
    output = DOCS_DIR / "RISK_TEXT_CORPUS_SUMMARY.md"
    output.write_text(build_summary(rows), encoding="utf-8")
    return output


def main() -> int:
    terms_config = load_terms()
    text_rows = iter_text_lines()
    snippets = extract_snippets(terms_config, text_rows)
    snippets_path = write_snippets(snippets)
    summary_path = write_summary(snippets)
    print(f"wrote {snippets_path}")
    print(f"wrote {summary_path}")
    print(f"matches: {len(snippets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
