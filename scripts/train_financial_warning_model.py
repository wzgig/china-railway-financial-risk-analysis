"""Train baseline financial-risk warning models from the peer panel."""

from __future__ import annotations

import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


PANEL_CSV = Path("data/processed/peer_financial_panel.csv")
DATASET_CSV = Path("data/processed/warning_model_dataset.csv")
PREDICTIONS_CSV = Path("data/processed/china_railway_warning_predictions.csv")
METRICS_CSV = Path("outputs/tables/warning_model_metrics.csv")
IMPORTANCE_CSV = Path("outputs/tables/warning_model_feature_importance.csv")
LOGISTIC_MODEL = Path("outputs/models/financial_warning_logistic.joblib")
RF_MODEL = Path("outputs/models/financial_warning_random_forest.joblib")
DOC_OUTPUT = Path("docs/FINANCIAL_WARNING_MODEL.md")

FEATURE_COLUMNS = [
    "revenue_growth_pct",
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
    "log_revenue_100m",
    "log_total_assets_100m",
]


def decimal_value(value: object) -> Decimal:
    if value is None or value == "":
        return Decimal("0")
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return Decimal("0")


def pressure_label(row: dict[str, str]) -> tuple[int, int, str]:
    reasons: list[str] = []
    if decimal_value(row.get("parent_net_profit_growth_pct")) <= Decimal("-10"):
        reasons.append("归母净利润同比下降超过10%")
    if decimal_value(row.get("revenue_growth_pct")) <= Decimal("-5"):
        reasons.append("营业收入同比下降超过5%")
    if decimal_value(row.get("asset_liability_ratio_pct")) >= Decimal("75"):
        reasons.append("资产负债率不低于75%")
    if decimal_value(row.get("operating_cash_flow_to_revenue_pct")) <= Decimal("1"):
        reasons.append("经营现金流/营收不高于1%")
    if decimal_value(row.get("interest_coverage_proxy")) <= Decimal("2"):
        reasons.append("利息保障倍数代理不高于2")
    if decimal_value(row.get("current_ratio")) <= Decimal("1"):
        reasons.append("流动比率不高于1")
    score = len(reasons)
    return (1 if score >= 3 else 0), score, "；".join(reasons)


def load_panel() -> list[dict[str, str]]:
    if not PANEL_CSV.exists():
        raise FileNotFoundError(f"Missing {PANEL_CSV}; run scripts/collect_peer_financial_panel.py first")
    with PANEL_CSV.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_dataset(panel_rows: list[dict[str, str]]) -> pd.DataFrame:
    by_company: dict[str, dict[int, dict[str, str]]] = defaultdict(dict)
    for row in panel_rows:
        by_company[row["company_code"]][int(row["year"])] = row

    records: list[dict[str, object]] = []
    for company_code, yearly_rows in by_company.items():
        for feature_year in sorted(yearly_rows):
            label_year = feature_year + 1
            if label_year not in yearly_rows:
                continue
            current = yearly_rows[feature_year]
            future = yearly_rows[label_year]
            label, rule_score, reasons = pressure_label(future)
            record: dict[str, object] = {
                "company_code": company_code,
                "company_name": current["company_name"],
                "short_name": current["short_name"],
                "feature_year": feature_year,
                "label_year": label_year,
                "financial_pressure_label_next_year": label,
                "label_rule_score": rule_score,
                "label_reason": reasons,
            }
            for column in FEATURE_COLUMNS:
                if column == "log_revenue_100m":
                    record[column] = np.log1p(float(decimal_value(current.get("revenue_100m_rmb"))))
                elif column == "log_total_assets_100m":
                    record[column] = np.log1p(float(decimal_value(current.get("total_assets_estimated_100m_rmb"))))
                else:
                    record[column] = float(decimal_value(current.get(column)))
            records.append(record)

    return pd.DataFrame(records)


def model_specs() -> dict[str, Pipeline]:
    return {
        "logistic_regression": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=4,
                        min_samples_leaf=2,
                        class_weight="balanced",
                        random_state=42,
                    ),
                ),
            ]
        ),
    }


def probability(model: Pipeline, frame: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(frame)[:, 1]
    return np.zeros(len(frame))


def evaluate_model(name: str, model: Pipeline, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, str]:
    pred = model.predict(x_test)
    prob = probability(model, x_test)
    labels = sorted(set(y_test.tolist()) | set(pred.tolist()))
    matrix = confusion_matrix(y_test, pred, labels=[0, 1])
    auc = ""
    if len(set(y_test.tolist())) > 1:
        auc = f"{roc_auc_score(y_test, prob):.4f}"
    return {
        "model": name,
        "test_rows": str(len(y_test)),
        "accuracy": f"{accuracy_score(y_test, pred):.4f}",
        "precision": f"{precision_score(y_test, pred, zero_division=0):.4f}",
        "recall": f"{recall_score(y_test, pred, zero_division=0):.4f}",
        "f1": f"{f1_score(y_test, pred, zero_division=0):.4f}",
        "roc_auc": auc,
        "confusion_matrix_0_1": matrix.tolist().__repr__(),
        "labels_seen": ",".join(str(label) for label in labels),
    }


def feature_importance(name: str, model: Pipeline) -> list[dict[str, str]]:
    if name == "logistic_regression":
        coefficients = model.named_steps["model"].coef_[0]
        return [
            {
                "model": name,
                "feature": feature,
                "importance": f"{coef:.6f}",
                "rank_abs": "",
                "importance_type": "standardized_coefficient",
            }
            for feature, coef in zip(FEATURE_COLUMNS, coefficients)
        ]
    forest = model.named_steps["model"]
    return [
        {
            "model": name,
            "feature": feature,
            "importance": f"{value:.6f}",
            "rank_abs": "",
            "importance_type": "gini_importance",
        }
        for feature, value in zip(FEATURE_COLUMNS, forest.feature_importances_)
    ]


def write_rows(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_china_predictions(panel_rows: list[dict[str, str]], models: dict[str, Pipeline]) -> list[dict[str, str]]:
    china_rows = sorted(
        [row for row in panel_rows if row["company_code"] == "601390"],
        key=lambda row: int(row["year"]),
    )
    records = []
    for row in china_rows:
        feature_year = int(row["year"])
        if feature_year < 2024:
            continue
        features = {}
        for column in FEATURE_COLUMNS:
            if column == "log_revenue_100m":
                features[column] = np.log1p(float(decimal_value(row.get("revenue_100m_rmb"))))
            elif column == "log_total_assets_100m":
                features[column] = np.log1p(float(decimal_value(row.get("total_assets_estimated_100m_rmb"))))
            else:
                features[column] = float(decimal_value(row.get(column)))
        frame = pd.DataFrame([features], columns=FEATURE_COLUMNS)
        output = {
            "company_code": row["company_code"],
            "company_name": row["company_name"],
            "feature_year": str(feature_year),
            "target_year": str(feature_year + 1),
            "note": "2024 row predicts known 2025 pressure; 2025 row is a forward-looking 2026 watch score.",
        }
        for name, model in models.items():
            prob = float(probability(model, frame)[0])
            pred = int(model.predict(frame)[0])
            output[f"{name}_probability"] = f"{prob:.4f}"
            output[f"{name}_prediction"] = str(pred)
        records.append(output)
    return records


def write_markdown(dataset: pd.DataFrame, metrics: list[dict[str, str]], importances: list[dict[str, str]], predictions: list[dict[str, str]]) -> None:
    label_counts = dataset["financial_pressure_label_next_year"].value_counts().sort_index().to_dict()
    train_rows = dataset[dataset["feature_year"] <= 2023]
    test_rows = dataset[dataset["feature_year"] == 2024]

    top_rf = [
        row
        for row in sorted(
            [item for item in importances if item["model"] == "random_forest"],
            key=lambda item: float(item["importance"]),
            reverse=True,
        )[:8]
    ]

    lines = [
        "# 机器学习财务风险预警基线模型",
        "",
        "生成脚本：`scripts/train_financial_warning_model.py`",
        "",
        "## 模型定位",
        "",
        "- 当前模型是课程级财务指标基线模型，使用同业上市建筑企业财务面板训练。",
        "- 标签为下一年度财务压力规则标签，不等同于真实违约、信用评级下调或投资建议。",
        "- 中国中铁的文本风险指标和风险事件样本已在前序文档中构建，本模型先完成同业财务基线，后续可扩展为财务+文本+事件融合模型。",
        "",
        "## 样本设计",
        "",
        f"- 监督样本：{len(dataset)} 条，来自 11 家公司 2021-2024 年特征和 2022-2025 年下一年标签。",
        f"- 训练集：{len(train_rows)} 条，特征年份 2021-2023。",
        f"- 测试集：{len(test_rows)} 条，特征年份 2024，预测 2025 年压力标签。",
        f"- 标签分布：0 类 {label_counts.get(0, 0)} 条，1 类 {label_counts.get(1, 0)} 条。",
        "",
        "## 标签规则",
        "",
        "下一年度若满足以下 6 项中的至少 3 项，记为财务压力样本：归母净利润同比下降超过 10%、营业收入同比下降超过 5%、资产负债率不低于 75%、经营现金流/营收不高于 1%、利息保障倍数代理不高于 2、流动比率不高于 1。",
        "",
        "## 测试集表现",
        "",
        "| 模型 | Accuracy | Precision | Recall | F1 | ROC-AUC | 混淆矩阵[[TN,FP],[FN,TP]] |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in metrics:
        lines.append(
            f"| {row['model']} | {row['accuracy']} | {row['precision']} | {row['recall']} | {row['f1']} | {row['roc_auc']} | {row['confusion_matrix_0_1']} |"
        )

    lines.extend(["", "## 随机森林主要特征", "", "| 排名 | 特征 | 重要性 |", "|---:|---|---:|"])
    for idx, row in enumerate(top_rf, start=1):
        lines.append(f"| {idx} | {row['feature']} | {row['importance']} |")

    lines.extend(
        [
            "",
            "## 中国中铁预测结果",
            "",
            "| 特征年份 | 目标年份 | Logistic 概率 | Logistic 预测 | Random Forest 概率 | Random Forest 预测 |",
            "|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in predictions:
        lines.append(
            "| {feature_year} | {target_year} | {lp} | {lpred} | {rfp} | {rfpred} |".format(
                feature_year=row["feature_year"],
                target_year=row["target_year"],
                lp=row["logistic_regression_probability"],
                lpred=row["logistic_regression_prediction"],
                rfp=row["random_forest_probability"],
                rfpred=row["random_forest_prediction"],
            )
        )

    lines.extend(
        [
            "",
            "## 解释边界",
            "",
            "- 样本量较小，测试集仅 11 条，指标只能说明课程项目流程已经闭环。",
            "- 标签是规则构造结果，后续应结合评级调整、违约事件、审计意见或更多企业风险事件进行校准。",
            "- 当前模型只使用财务指标训练；文本和事件指标已为中国中铁个案准备，暂未扩展到所有同业公司。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    panel_rows = load_panel()
    dataset = build_dataset(panel_rows)
    DATASET_CSV.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(DATASET_CSV, index=False, encoding="utf-8-sig")

    train = dataset[dataset["feature_year"] <= 2023]
    test = dataset[dataset["feature_year"] == 2024]
    x_train = train[FEATURE_COLUMNS]
    y_train = train["financial_pressure_label_next_year"]
    x_test = test[FEATURE_COLUMNS]
    y_test = test["financial_pressure_label_next_year"]

    fitted_models: dict[str, Pipeline] = {}
    metrics: list[dict[str, str]] = []
    importances: list[dict[str, str]] = []
    for name, model in model_specs().items():
        model.fit(x_train, y_train)
        fitted_models[name] = model
        metrics.append(evaluate_model(name, model, x_test, y_test))
        importances.extend(feature_importance(name, model))

    # Refit final models on all supervised rows before scoring the latest case row.
    final_models = model_specs()
    for name, model in final_models.items():
        model.fit(dataset[FEATURE_COLUMNS], dataset["financial_pressure_label_next_year"])
        fitted_models[name] = model

    LOGISTIC_MODEL.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(fitted_models["logistic_regression"], LOGISTIC_MODEL)
    joblib.dump(fitted_models["random_forest"], RF_MODEL)

    predictions = build_china_predictions(panel_rows, fitted_models)
    write_rows(METRICS_CSV, metrics, list(metrics[0].keys()))
    write_rows(
        IMPORTANCE_CSV,
        importances,
        ["model", "feature", "importance", "rank_abs", "importance_type"],
    )
    write_rows(PREDICTIONS_CSV, predictions, list(predictions[0].keys()))
    write_markdown(dataset, metrics, importances, predictions)

    print(f"wrote {DATASET_CSV} ({len(dataset)} rows)")
    print(f"wrote {METRICS_CSV}")
    print(f"wrote {IMPORTANCE_CSV}")
    print(f"wrote {PREDICTIONS_CSV}")
    print(f"wrote {LOGISTIC_MODEL}")
    print(f"wrote {RF_MODEL}")
    print(f"wrote {DOC_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
