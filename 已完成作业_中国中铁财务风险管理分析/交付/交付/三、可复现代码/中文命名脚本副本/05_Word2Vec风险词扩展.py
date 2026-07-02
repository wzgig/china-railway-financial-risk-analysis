"""Expand risk terms with Word2Vec and build expanded text-risk indicators."""

from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import jieba
import jieba.analyse
from gensim.models import Word2Vec


SEED_CONFIG = Path("configs/risk_seed_terms.json")
EXPANDED_CONFIG = Path("configs/risk_terms_expanded.json")
STOPWORDS_PATH = Path("configs/stopwords_zh.txt")
TEXT_DIR = Path("data/interim/annual_report_text")
MODEL_PATH = Path("outputs/models/annual_report_word2vec.model")
TERMS_CSV = Path("data/processed/word2vec_risk_terms.csv")
INDEX_CSV = Path("data/processed/text_risk_index_word2vec_by_year.csv")
TERM_YEAR_CSV = Path("data/processed/text_risk_terms_word2vec_by_year.csv")
DOC_PATH = Path("docs/WORD2VEC_RISK_TERMS.md")

CATEGORY_HINTS = {
    "liquidity": ["现金", "流动", "资金", "融资", "筹资", "偿付", "本息", "到期", "收支", "还款"],
    "solvency": ["债", "借款", "利息", "兑付", "偿债", "负债", "本金", "票面", "抵押", "短期", "长期", "定息", "浮息", "筹措"],
    "operation": ["应收", "合同", "存货", "周转", "结算", "减值", "坏账", "账龄", "跌价", "预收", "库存", "变现", "准备", "阶段"],
    "profitability": ["利润", "毛利", "成本", "亏损", "费用", "价格", "下滑", "盈利", "收益", "分配"],
    "project": ["项目", "工期", "质量", "安全", "分包", "索赔", "履约", "进度", "验收", "施工", "奖励"],
    "compliance": ["诉讼", "仲裁", "处罚", "执行", "合规", "环保", "安全生产", "纠纷", "未决", "判决", "败诉", "立案", "整改", "体系", "操守"],
    "market": ["市场", "房地产", "汇率", "海外", "竞争", "政策", "投资", "需求", "本位币", "折算", "即期", "无风险", "激烈"],
    "organizational_propagation": ["子公司", "担保", "关联", "差额", "集团", "控股", "联营", "合营", "贷款", "额度", "支付现金", "支持"],
}


def load_json(path: Path) -> dict[str, dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


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
        texts[int(match.group("year"))] = path.read_text(encoding="utf-8", errors="replace")
    if not texts:
        raise FileNotFoundError(f"No annual report text files found in {TEXT_DIR}")
    return texts


def prepare_jieba(config: dict[str, dict[str, object]]) -> None:
    for meta in config.values():
        for term in meta["terms"]:
            jieba.add_word(str(term), freq=200000)


def valid_token(token: str, stopwords: set[str]) -> bool:
    token = token.strip()
    if len(token) < 2 or len(token) > 12:
        return False
    if token in stopwords:
        return False
    if token.isdigit():
        return False
    if re.fullmatch(r"[A-Za-z0-9_.%-]+", token):
        return False
    if re.search(r"\d{4}", token):
        return False
    return True


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    return [token for token in jieba.lcut(text) if valid_token(token, stopwords)]


def build_sentences(texts: dict[int, str], stopwords: set[str]) -> list[list[str]]:
    sentences: list[list[str]] = []
    splitter = re.compile(r"[。！？；;\n\r]+")
    for text in texts.values():
        for segment in splitter.split(text):
            tokens = tokenize(segment, stopwords)
            if len(tokens) >= 5:
                sentences.append(tokens)
    return sentences


def train_model(sentences: list[list[str]]) -> Word2Vec:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    model = Word2Vec(
        sentences=sentences,
        vector_size=100,
        window=5,
        min_count=3,
        workers=2,
        sg=1,
        epochs=30,
        seed=20260629,
    )
    model.save(str(MODEL_PATH))
    return model


def count_mentions_by_term(texts: dict[int, str], terms: set[str]) -> Counter[str]:
    joined = "\n".join(texts.values())
    return Counter({term: joined.count(term) for term in terms})


def looks_category_relevant(category: str, candidate: str) -> bool:
    return any(hint in candidate for hint in CATEGORY_HINTS.get(category, []))


def expand_terms(
    config: dict[str, dict[str, object]],
    model: Word2Vec,
    texts: dict[int, str],
    stopwords: set[str],
) -> tuple[dict[str, dict[str, object]], list[dict[str, object]]]:
    all_seed_terms = {str(term) for meta in config.values() for term in meta["terms"]}
    raw_candidates: set[str] = set()
    rows: list[dict[str, object]] = []
    expanded: dict[str, dict[str, object]] = {}

    for category, meta in config.items():
        label = str(meta["label"])
        seed_terms = [str(term) for term in meta["terms"]]
        category_candidates: dict[str, dict[str, object]] = {}

        for seed in seed_terms:
            if seed not in model.wv:
                continue
            for candidate, similarity in model.wv.most_similar(seed, topn=40):
                if candidate in all_seed_terms or not valid_token(candidate, stopwords):
                    continue
                if not looks_category_relevant(category, candidate):
                    continue
                raw_candidates.add(candidate)
                current = category_candidates.get(candidate)
                if current is None or float(similarity) > float(current["similarity"]):
                    category_candidates[candidate] = {
                        "source_seed": seed,
                        "similarity": round(float(similarity), 4),
                    }

        mention_counts = count_mentions_by_term(texts, set(category_candidates))
        selected = []
        for candidate, data in sorted(
            category_candidates.items(),
            key=lambda item: (float(item[1]["similarity"]), mention_counts[item[0]]),
            reverse=True,
        ):
            if mention_counts[candidate] < 3:
                continue
            selected.append(candidate)
            rows.append(
                {
                    "risk_category": category,
                    "risk_label": label,
                    "source_seed": data["source_seed"],
                    "candidate_term": candidate,
                    "similarity": data["similarity"],
                    "corpus_mentions": mention_counts[candidate],
                    "status": "candidate",
                }
            )
            if len(selected) >= 12:
                break

        expanded[category] = {
            "label": label,
            "seed_terms": seed_terms,
            "word2vec_terms": selected,
            "terms": seed_terms + selected,
        }

    return expanded, rows


def extract_weights(text: str, stopwords: set[str]) -> dict[str, float]:
    tags = jieba.analyse.extract_tags(text, topK=800, withWeight=True)
    return {term: float(weight) for term, weight in tags if valid_token(term, stopwords)}


def normalize_scores(rows: list[dict[str, object]], key: str, output_key: str) -> None:
    by_year: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_year[int(row["year"])].append(row)
    for group in by_year.values():
        max_value = max(float(row[key]) for row in group) or 1.0
        for row in group:
            row[output_key] = round(float(row[key]) / max_value * 100, 2)


def build_expanded_index(
    expanded: dict[str, dict[str, object]],
    texts: dict[int, str],
    stopwords: set[str],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    index_rows: list[dict[str, object]] = []
    term_rows: list[dict[str, object]] = []

    for year, raw_text in sorted(texts.items()):
        text = re.sub(r"\s+", " ", raw_text)
        tokens = tokenize(text, stopwords)
        token_counts = Counter(tokens)
        total_tokens = sum(token_counts.values()) or 1
        weights = extract_weights(text, stopwords)

        for category, meta in expanded.items():
            label = str(meta["label"])
            terms = [str(term) for term in meta["terms"]]
            seed_count = len(meta["seed_terms"])
            w2v_count = len(meta["word2vec_terms"])
            exact_counts = Counter({term: text.count(term) for term in terms})
            mentions = sum(exact_counts.values())
            token_count = sum(token_counts.get(term, 0) for term in terms)
            weight_sum = sum(weights.get(term, 0.0) for term in terms)
            mentions_per_10k = mentions / total_tokens * 10000

            index_rows.append(
                {
                    "year": year,
                    "risk_category": category,
                    "risk_label": label,
                    "seed_terms": seed_count,
                    "word2vec_terms": w2v_count,
                    "total_terms": len(terms),
                    "exact_mentions": mentions,
                    "token_count": token_count,
                    "mentions_per_10k_tokens": round(mentions_per_10k, 4),
                    "jieba_weight_sum": round(weight_sum, 6),
                    "log_weighted_text_risk": round(math.log1p(mentions) * (1 + weight_sum), 6),
                }
            )

            for term in terms:
                term_rows.append(
                    {
                        "year": year,
                        "risk_category": category,
                        "risk_label": label,
                        "term": term,
                        "term_source": "seed" if term in meta["seed_terms"] else "word2vec",
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
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_expanded_config(expanded: dict[str, dict[str, object]]) -> None:
    EXPANDED_CONFIG.write_text(json.dumps(expanded, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(
    expanded: dict[str, dict[str, object]],
    candidate_rows: list[dict[str, object]],
    index_rows: list[dict[str, object]],
    sentence_count: int,
) -> Path:
    years = sorted({int(row["year"]) for row in index_rows})
    categories = sorted(expanded)
    labels = {category: str(expanded[category]["label"]) for category in categories}
    by_year_cat = {(int(row["year"]), str(row["risk_category"])): row for row in index_rows}

    lines = [
        "# Word2Vec 风险词扩充结果",
        "",
        "复现脚本：`scripts/build_word2vec_risk_terms.py`",
        "",
        "## 方法",
        "",
        f"- 语料：2021-2025 年中国中铁年报文本，切分得到 {sentence_count} 个训练句段。",
        "- 模型：`gensim.models.Word2Vec`，skip-gram，`vector_size=100`，`window=5`，`min_count=3`，`epochs=30`。",
        "- 扩词：以人工种子词为入口提取相似词，过滤停用词、短词、纯数字英文词和低频词，每类最多保留 12 个候选词。",
        "- 解释：候选词是课程分析用扩展词典，进入最终论文前仍需人工复核语义噪声。",
        "",
        "## 各风险类别扩展词",
        "",
        "| 风险类别 | 种子词数量 | Word2Vec 候选词 |",
        "|---|---:|---|",
    ]
    for category in categories:
        meta = expanded[category]
        lines.append(
            f"| {meta['label']} | {len(meta['seed_terms'])} | "
            + "、".join(str(term) for term in meta["word2vec_terms"])
            + " |"
        )

    lines.extend(
        [
            "",
            "## 扩展词典年度综合文本风险得分",
            "",
            "| 年份 | " + " | ".join(labels[category] for category in categories) + " |",
            "|---|" + "|".join(["---:"] * len(categories)) + "|",
        ]
    )
    for year in years:
        values = [
            str(by_year_cat[(year, category)]["combined_text_risk_score"])
            for category in categories
        ]
        lines.append(f"| {year} | " + " | ".join(values) + " |")

    lines.extend(["", "## 高相似度候选词示例", "", "| 风险类别 | 种子词 | 候选词 | 相似度 | 语料命中 |", "|---|---|---|---:|---:|"])
    for row in sorted(candidate_rows, key=lambda item: (str(item["risk_category"]), -float(item["similarity"])))[:40]:
        lines.append(
            f"| {row['risk_label']} | {row['source_seed']} | {row['candidate_term']} | "
            f"{row['similarity']} | {row['corpus_mentions']} |"
        )

    lines.extend(
        [
            "",
            "## 复现产物",
            "",
            "- 扩展词典：`configs/risk_terms_expanded.json`。",
            "- 候选词明细：`data/processed/word2vec_risk_terms.csv`，本地生成，不纳入公开仓库。",
            "- 扩展文本风险指数：`data/processed/text_risk_index_word2vec_by_year.csv`，本地生成，不纳入公开仓库。",
            "- 扩展词年度明细：`data/processed/text_risk_terms_word2vec_by_year.csv`，本地生成，不纳入公开仓库。",
            "",
            "## 使用边界",
            "",
            "- 年报语料属于单公司公开披露文本，模型学到的是披露语境相似性，不等同于真实风险因果关系。",
            "- Word2Vec 候选词可能包含行业中性词，正式报告引用前需人工筛选。",
            "- 扩展指数用于与种子词指数互相校验，不单独作为风险概率结论。",
        ]
    )
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return DOC_PATH


def main() -> int:
    config = load_json(SEED_CONFIG)
    stopwords = load_stopwords()
    prepare_jieba(config)
    texts = load_texts()
    sentences = build_sentences(texts, stopwords)
    if len(sentences) < 100:
        raise ValueError("Word2Vec corpus is too small after tokenization")
    model = train_model(sentences)
    expanded, candidate_rows = expand_terms(config, model, texts, stopwords)
    write_expanded_config(expanded)
    index_rows, term_rows = build_expanded_index(expanded, texts, stopwords)
    write_csv(TERMS_CSV, candidate_rows)
    write_csv(INDEX_CSV, index_rows)
    write_csv(TERM_YEAR_CSV, term_rows)
    doc_path = write_markdown(expanded, candidate_rows, index_rows, len(sentences))
    print(f"wrote {EXPANDED_CONFIG}")
    print(f"wrote {TERMS_CSV} ({len(candidate_rows)} candidates)")
    print(f"wrote {INDEX_CSV}")
    print(f"wrote {TERM_YEAR_CSV}")
    print(f"wrote {MODEL_PATH}")
    print(f"wrote {doc_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
