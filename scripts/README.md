# 脚本规划

建议按以下顺序逐步创建脚本：

| 顺序 | 脚本 | 用途 | 输入 | 输出 |
|---|---|---|---|---|
| 01 | `collect_annual_reports.py` | 整理年报和公告下载清单 | `SOURCES.md` | `data/raw/annual_reports/` |
| 02 | `parse_financial_tables.py` | 抽取或录入财务指标 | 年报、手工表 | `data/processed/financial_indicators.csv` |
| 03 | `clean_risk_events.py` | 清洗司法、执行、企查查风险事件 | `data/raw/` | `data/processed/risk_events.csv` |
| 04 | `build_risk_network.py` | 构建 Gephi 节点边表和 GEXF | `risk_events.csv` | `risk_nodes.csv`、`risk_edges.csv`、`.gexf` |
| 05 | `build_text_risk_index.py` | 分词、扩词、计算文本风险指标 | 文本语料 | `text_risk_scores.csv` |
| 06 | `train_warning_model.py` | 训练财务风险预警模型 | `model_features.csv` | `outputs/models/` |
| 07 | `make_figures.py` | 统一生成报告图表 | 处理后数据 | `outputs/figures/` |

## 当前已实现脚本

| 脚本 | 用途 | 输出 |
|---|---|---|
| `collect_official_reports.py` | 下载中国中铁年报、季报和评级报告 | `data/raw/annual_reports/`、`data/interim/official_reports_manifest.csv` |
| `extract_financial_indicators.py` | 整理 2021-2025 年财务风险指标 | `data/processed/financial_risk_indicators.csv`、`docs/FINANCIAL_RISK_INDICATORS.md` |
| `extract_risk_text_corpus.py` | 抽取年报风险语料命中片段 | `data/interim/risk_text_corpus_seed_matches.csv`、`docs/RISK_TEXT_CORPUS_SUMMARY.md` |
| `build_text_risk_index.py` | 计算种子词文本风险指数 | `data/processed/text_risk_index_by_year.csv`、`docs/TEXT_RISK_INDEX.md` |
| `build_word2vec_risk_terms.py` | 训练 Word2Vec 并扩展风险词典 | `configs/risk_terms_expanded.json`、`docs/WORD2VEC_RISK_TERMS.md` |
| `create_risk_event_template.py` | 生成合规风险事件采集模板 | `data/interim/risk_event_collection_template.csv` |
| `build_official_risk_events.py` | 生成官方披露风险事件种子样本 | `data/interim/risk_events_official_seed.csv`、`docs/OFFICIAL_RISK_EVENTS_SAMPLE.md` |
| `build_external_risk_events.py` | 生成司法、执行、企查查扩展样本并合并事件表 | `data/interim/risk_events_external_sample.csv`、`data/processed/risk_events_combined.csv`、`docs/EXTERNAL_RISK_EVENTS_SAMPLE.md` |
| `build_risk_network.py` | 基于合并事件表构建 Gephi 节点、边和 GEXF | `data/processed/risk_nodes.csv`、`data/processed/risk_edges.csv`、`outputs/gephi/china_railway_risk_network.gexf` |
| `analyze_risk_network.py` | 计算中心性、社群和增强版 Gephi 文件，并生成报告导图 | `data/processed/risk_network_centrality.csv`、`outputs/gephi/china_railway_risk_network_enhanced.gexf`、`docs/RISK_NETWORK_CENTRALITY.md` |
| `build_report_figures.py` | 生成报告图表 | `outputs/figures/`、`docs/assets/figures/`、`docs/FIGURES_CATALOG.md` |
| `build_warning_model_features.py` | 生成机器学习预警模型年度特征表和规则标签 | `data/processed/model_features_china_railway.csv`、`docs/MODEL_FEATURE_TABLE.md` |
| `collect_peer_financial_panel.py` | 采集同业建筑上市公司 2021-2025 年财务面板 | `data/processed/peer_financial_panel.csv`、`docs/PEER_FINANCIAL_PANEL.md` |
| `train_financial_warning_model.py` | 训练 Logistic Regression 和 Random Forest 财务预警基线模型 | `outputs/models/`、`outputs/tables/`、`docs/FINANCIAL_WARNING_MODEL.md` |
| `build_resilience_model.py` | 构建弹性风险管理四维评分、雷达图和趋势图 | `data/processed/resilience_scores.csv`、`outputs/tables/resilience_scores.csv`、`docs/RESILIENCE_RISK_MANAGEMENT_MODEL.md` |

## 开发规则

- 每个脚本都读取 `configs/project_config.yaml`。
- 每个输出文件都保留生成日期和数据来源。
- 不在脚本中硬编码个人账号、密码或 Cookie。
- 对动态网站只做合规访问，不绕过验证码和权限。
