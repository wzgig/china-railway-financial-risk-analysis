"""Compute jieba-based textual risk indicators from annual report text.

Outputs:
- data/processed/text_risk_index_by_year.csv
- data/processed/text_risk_terms_by_year.csv
- docs/TEXT_RISK_INDEX.md
"""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import jieba
import jieba.analyse


CONFIG_PATH = Path("configs/risk_seed_terms.json")
STOPWORDS_PATH = Path("configs/stopwords_zh.txt")
TEXT_DIR = Path("data/interim/annual_report_text")
PROCESSED_DIR = Path("data/processed")
DOCS_DIR = Path("docs")


def load_config() -> dict[str, dict[str, object]]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_stopwords() -> set[str]:
    if not STOPWORDS_PATH.exists():
        return set()
    return {
        line.strip()
        for line in STOPWORDS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def load_texts() -> dict[int, str]:
    texts: dict[int, str] = {}
    for path in sorted(TEXT_DIR.glob("*_annual_report.txt")):
        match = re.match(r"(?P<year>\d{4})_annual_report\.txt", path.name)
        if not match:
            continue
        year = int(match.group("year"))
        text = path.read_text(encoding="utf-8", errors="replace")
        texts[year] = re.sub(r"\s+", " ", text)
    return texts


def prepare_jieba(config: dict[str, dict[str, object]]) -> None:
    for meta in config.values():
        for term in meta["terms"]:
            jieba.add_word(str(term), freq=200000)


def valid_token(token: str, stopwords: set[str]) -> bool:
    token = token.strip()
    if len(token) < 2:
        return False
    if token in stopwords:
        return False
    if token.isdigit():
        return False
    if re.fullmatch(r"[A-Za-z0-9_.%-]+", token):
        return False
    return True


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    return [token for token in jieba.lcut(text) if valid_token(token, stopwords)]


def extract_weights(text: str, stopwords: set[str]) -> dict[str, float]:
    tags = jieba.analyse.extract_tags(text, topK=500, withWeight=True)
    return {
        term: float(weight)
        for term, weight in tags
        if valid_token(term, stopwords)
    }


def count_exact_mentions(text: str, terms: list[str]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for term in terms:
        counts[term] = text.count(term)
    return counts


def normalize_scores(rows: list[dict[str, object]], key: str, output_key: str) -> None:
    by_year: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_year[int(row["year"])].append(row)
    for group in by_year.values():
        max_value = max(float(row[key]) for row in group) or 1.0
        for row in group:
            row[output_key] = round(float(row[key]) / max_value * 100, 2)


def build_indexes(
    config: dict[str, dict[str, object]],
    texts: dict[int, str],
    stopwords: set[str],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    index_rows: list[dict[str, object]] = []
    term_rows: list[dict[str, object]] = []

    for year, text in sorted(texts.items()):
        tokens = tokenize(text, stopwords)
        token_counts = Counter(tokens)
        total_tokens = sum(token_counts.values()) or 1
        weights = extract_weights(text, stopwords)

        for category, meta in config.items():
            label = str(meta["label"])
            seed_terms = [str(term) for term in meta["terms"]]
            exact_counts = count_exact_mentions(text, seed_terms)
            category_mentions = sum(exact_counts.values())
            category_token_count = sum(token_counts.get(term, 0) for term in seed_terms)
            category_weight = sum(weights.get(term, 0.0) for term in seed_terms)
            mentions_per_10k = category_mentions / total_tokens * 10000

            index_rows.append(
                {
                    "year": year,
                    "risk_category": category,
                    "risk_label": label,
                    "total_tokens": total_tokens,
                    "seed_terms": len(seed_terms),
                    "seed_exact_mentions": category_mentions,
                    "seed_token_count": category_token_count,
                    "mentions_per_10k_tokens": round(mentions_per_10k, 4),
                    "jieba_weight_sum": round(category_weight, 6),
                    "log_weighted_text_risk": round(math.log1p(category_mentions) * (1 + category_weight), 6),
                }
            )

            for term in seed_terms:
                term_rows.append(
                    {
                        "year": year,
                        "risk_category": category,
                        "risk_label": label,
                        "term": term,
                        "exact_mentions": exact_counts[term],
                        "jieba_token_count": token_counts.get(term, 0),
                        "jieba_weight": round(weights.get(term, 0.0), 6),
                    }
                )

    normalize_scores(index_rows, "mentions_per_10k_tokens", "probability_proxy_score")
    normalize_scores(index_rows, "jieba_weight_sum", "text_weight_score")
    normalize_scores(index_rows, "log_weighted_text_risk", "combined_text_risk_score")
    return index_rows, term_rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(index_rows: list[dict[str, object]], term_rows: list[dict[str, object]]) -> Path:
    output = DOCS_DIR / "TEXT_RISK_INDEX.md"
    years = sorted({int(row["year"]) for row in index_rows})
    labels = {str(row["risk_category"]): str(row["risk_label"]) for row in index_rows}
    categories = sorted(labels)
    by_year_cat = {
        (int(row["year"]), str(row["risk_category"])): row
        for row in index_rows
    }

    lines = [
        "# 文本风险指标计算结果",
        "",
        "复现脚本：`scripts/build_text_risk_index.py`",
        "",
        "方法：对 2021-2025 年年报文本进行 jieba 分词，使用 `jieba.analyse.extract_tags(..., withWeight=True)` 获取 TF-IDF 风格权重，并结合种子词精确命中次数构造文本风险代理指标。",
        "",
        "## 年度风险类别综合文本风险得分",
        "",
        "| 年份 | " + " | ".join(labels[category] for category in categories) + " |",
        "| --- | " + " | ".join(["---:"] * len(categories)) + " |",
    ]
    for year in years:
        values = [
            str(by_year_cat[(year, category)]["combined_text_risk_score"])
            for category in categories
        ]
        lines.append(f"| {year} | " + " | ".join(values) + " |")

    lines.extend(
        [
            "",
            "## 年度风险类别概率代理得分",
            "",
            "概率代理得分按同一年内各风险类别 `每万词命中次数` 归一化到 0-100。",
            "",
            "| 年份 | " + " | ".join(labels[category] for category in categories) + " |",
            "| --- | " + " | ".join(["---:"] * len(categories)) + " |",
        ]
    )
    for year in years:
        values = [
            str(by_year_cat[(year, category)]["probability_proxy_score"])
            for category in categories
        ]
        lines.append(f"| {year} | " + " | ".join(values) + " |")

    top_terms = sorted(
        term_rows,
        key=lambda row: (int(row["year"]), -float(row["jieba_weight"]), -int(row["exact_mentions"])),
    )
    lines.extend(["", "## 每年高权重风险种子词", ""])
    for year in years:
        year_terms = [
            row
            for row in top_terms
            if int(row["year"]) == year and (float(row["jieba_weight"]) > 0 or int(row["exact_mentions"]) > 0)
        ][:12]
        rendered = "；".join(
            f"{row['term']}({row['risk_label']}，权重 {row['jieba_weight']}，命中 {row['exact_mentions']})"
            for row in year_terms
        )
        lines.append(f"- {year}：{rendered}")

    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "- 文本风险指标反映年报披露语境中的风险关注度，不等同于实际损失概率。",
            "- `combined_text_risk_score` 是课程分析用代理变量，后续应与财务指标、司法事件和图谱中心性共同解释。",
            "- 种子词后续可用 Word2Vec 扩充，并由人工复核噪声词。",
        ]
    )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def main() -> int:
    config = load_config()
    stopwords = load_stopwords()
    prepare_jieba(config)
    texts = load_texts()
    if not texts:
        raise SystemExit("No annual report text cache found. Run extract_financial_indicators.py first.")

    index_rows, term_rows = build_indexes(config, texts, stopwords)
    write_csv(PROCESSED_DIR / "text_risk_index_by_year.csv", index_rows)
    write_csv(PROCESSED_DIR / "text_risk_terms_by_year.csv", term_rows)
    md_path = write_markdown(index_rows, term_rows)
    print("wrote data/processed/text_risk_index_by_year.csv")
    print("wrote data/processed/text_risk_terms_by_year.csv")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
