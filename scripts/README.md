# 脚本复现说明

脚本按研究流程组织，主要用于把公开资料整理为财务指标、文本指标、风险图谱、预警模型结果和报告图表。运行前建议先确认 `requirements.txt` 中的依赖已安装，并保留 `configs/project_config.yaml` 的默认路径。

## 数据与指标

| 脚本 | 用途 | 主要输出 |
|---|---|---|
| `collect_official_reports.py` | 归档中国中铁年报、季报和评级报告 | `data/raw/annual_reports/`、`data/interim/official_reports_manifest.csv` |
| `extract_financial_indicators.py` | 整理 2021-2025 年财务风险指标 | `data/processed/financial_risk_indicators.csv`、`docs/FINANCIAL_RISK_INDICATORS.md` |
| `extract_risk_text_corpus.py` | 抽取年报风险语料命中片段 | `data/interim/risk_text_corpus_seed_matches.csv`、`docs/RISK_TEXT_CORPUS_SUMMARY.md` |
| `build_text_risk_index.py` | 计算种子词文本风险指数 | `data/processed/text_risk_index_by_year.csv`、`docs/TEXT_RISK_INDEX.md` |
| `build_word2vec_risk_terms.py` | 训练 Word2Vec 并扩展风险词典 | `configs/risk_terms_expanded.json`、`docs/WORD2VEC_RISK_TERMS.md` |

## 风险事件与图谱

| 脚本 | 用途 | 主要输出 |
|---|---|---|
| `create_risk_event_template.py` | 生成风险事件采集字段模板 | `data/interim/risk_event_collection_template.csv` |
| `build_official_risk_events.py` | 生成官方披露风险事件种子样本 | `data/interim/risk_events_official_seed.csv`、`docs/OFFICIAL_RISK_EVENTS_SAMPLE.md` |
| `build_external_risk_events.py` | 整理司法、执行、企业风险扩展样本 | `data/interim/risk_events_external_sample.csv`、`data/processed/risk_events_combined.csv` |
| `build_risk_network.py` | 构建 Gephi 节点、边和 GEXF 文件 | `data/processed/risk_nodes.csv`、`data/processed/risk_edges.csv`、`outputs/gephi/china_railway_risk_network.gexf` |
| `analyze_risk_network.py` | 计算中心性、社群并生成报告导图 | `data/processed/risk_network_centrality.csv`、`docs/RISK_NETWORK_CENTRALITY.md` |

## 预警模型与报告输出

| 脚本 | 用途 | 主要输出 |
|---|---|---|
| `build_report_figures.py` | 生成报告图表 | `outputs/figures/`、`docs/assets/figures/`、`docs/FIGURES_CATALOG.md` |
| `build_warning_model_features.py` | 合并年度预警特征并构造规则标签 | `data/processed/model_features_china_railway.csv`、`docs/MODEL_FEATURE_TABLE.md` |
| `collect_peer_financial_panel.py` | 采集同业建筑上市公司财务面板 | `data/processed/peer_financial_panel.csv`、`docs/PEER_FINANCIAL_PANEL.md` |
| `train_financial_warning_model.py` | 训练 Logistic Regression 和 Random Forest 基线模型 | `outputs/models/`、`outputs/tables/`、`docs/FINANCIAL_WARNING_MODEL.md` |
| `build_resilience_model.py` | 构建弹性风险管理四维评分和图表 | `data/processed/resilience_scores.csv`、`docs/RESILIENCE_RISK_MANAGEMENT_MODEL.md` |
| `build_course_paper_docx.py` | 从 Markdown 草稿生成 DOCX/PDF 草稿 | `paper/course_paper_draft.docx`、`paper/course_paper_draft.pdf` |

## 运行约束

- 原始年报、课程截图和格式模板只保留在本地，不进入公开仓库。
- 对需要登录、验证码、付费或权限限制的平台，只记录合法检索或导出结果，不绕过平台限制。
- `outputs/` 和 `data/processed/` 下的大部分生成文件默认不纳入版本库，公开展示图表放在 `docs/assets/figures/`。
