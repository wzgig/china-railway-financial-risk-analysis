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

## 开发规则

- 每个脚本都读取 `configs/project_config.yaml`。
- 每个输出文件都保留生成日期和数据来源。
- 不在脚本中硬编码个人账号、密码或 Cookie。
- 对动态网站只做合规访问，不绕过验证码和权限。
