# 3 分钟视频录制指南：风险传导、风险评估与风险预警

本指南用于录制“中国中铁风险传导 -> 风险评估 -> 风险预警”的 3 分钟左右展示视频。视频重点不是逐行讲代码，而是证明项目已经形成完整的数据处理链条：公开数据进入项目，经 Python 清洗和建模，形成 Gephi 风险图谱、风险评估图表和机器学习预警结果。

## 一、视频主线

建议把视频标题定为：

> 中国中铁财务风险管理分析：从公开数据到风险图谱与预警模型

视频只讲三件事：

1. 风险传导：公开披露、司法执行和企业风险线索如何转成事件表，再转成 Gephi 节点、边和中心性结果。
2. 风险评估：财务指标、年报文本、事件矩阵和网络中心性如何共同判断风险重点。
3. 风险预警：同业财务面板如何训练基线模型，并回代中国中铁形成 2026 年前瞻观察结果。

视频中可以强调的结果数字：

- 公开报告归档：7 份，包括 2021-2025 年年报、2026 年一季报、2025 年跟踪评级报告。
- 风险事件：合并后 28 条，其中官方披露 17 条，司法/执行/企查查扩展样本 11 条。
- 风险图谱：77 个节点、133 条边。
- 高中心性风险类型：合规风险、流动性风险位于风险类型节点前列。
- 2025 年财务压力：营业收入同比 -5.77%，归母净利润同比 -17.91%，资产负债率 78.12%，利息保障倍数 2.98。
- 2025 年文本风险：偿债风险、组织传导风险、市场风险、营运风险、流动性风险得分靠前。
- 预警模型：Logistic Regression 和 Random Forest 测试集 F1 均为 0.8235。
- 中国中铁 2026 年观察：Logistic 概率 0.9780，Random Forest 概率 0.9037。
- 弹性管理：2025 年综合韧性得分 33.11，等级为“低位修复”，最弱维度为经营缓冲。

## 二、录制前打开的窗口

建议开 4 个窗口，录制时按顺序切换：

1. 浏览器
   - GitHub Pages 项目页：`https://wzgig.github.io/china-railway-financial-risk-analysis/`
   - 中国中铁官网：`https://www.crec.cn/`
   - 中国中铁定期报告页：`https://www.crec.cn/web/tzzgx26/dqbg/ag46/index.html`
   - 上交所 601390 公告页：`https://www.sse.com.cn/assortment/stock/list/info/announcement/index.shtml?productId=601390`
   - 巨潮资讯：`https://www.cninfo.com.cn/`
   - 东方财富 HSF10 接口示例：`https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=1&code=SH601390`
   - 裁判文书网入口：`https://wenshu.court.gov.cn/`
   - 企查查入口：`https://www.qcc.com/`
2. VS Code
   - 重点打开 `scripts/collect_official_reports.py`
   - 重点打开 `scripts/build_external_risk_events.py`
   - 重点打开 `scripts/build_risk_network.py`
   - 重点打开 `scripts/analyze_risk_network.py`
   - 重点打开 `scripts/train_financial_warning_model.py`
3. PowerShell 终端
   - 当前目录：`D:\Qiuhua Wang\个人资料\闲鱼\知世`
4. 图片或 PDF 预览
   - `docs/assets/figures/risk_network_gephi_style.png`
   - `docs/assets/figures/financial_trends.png`
   - `docs/assets/figures/text_risk_heatmap.png`
   - `docs/assets/figures/risk_event_matrix.png`
   - `docs/assets/figures/resilience_radar_2025.png`
   - `paper/course_paper_formatted.pdf`

## 三、合法采集展示方式

视频里可以展示“爬取”，但要讲清楚合规边界：

- 可以现场运行 `scripts/collect_official_reports.py`，因为它只访问中国中铁官网公开页面和公开 PDF 链接。
- 可以现场运行 `scripts/collect_peer_financial_panel.py`，因为它访问东方财富公开 HSF10 财务分析接口，用于同业财务面板。
- 不建议现场爬裁判文书网、执行信息公开网或企查查。视频中只展示这些网站入口、检索对象和本项目的结构化样本脚本，说明没有绕过登录、验证码、付费墙或权限限制。
- 对司法/执行/企查查部分，建议展示 `scripts/build_external_risk_events.py` 和 `docs/EXTERNAL_RISK_EVENTS_SAMPLE.md`，说明样本来自公开法院 PDF、公开报道转引和平台公开摘要，`candidate`、`verify` 样本在正式使用前仍需逐条复核。

现场可运行的采集演示命令：

```powershell
python .\scripts\collect_official_reports.py
python .\scripts\collect_peer_financial_panel.py
```

如果网络不稳定，不要在视频里等待。可以直接展示已有结果：

```powershell
Get-ChildItem .\data\raw\annual_reports
Import-Csv .\data\interim\official_reports_manifest.csv | Select-Object period,report_type,filename
Import-Csv .\data\processed\peer_financial_panel.csv | Select-Object -First 5 company_code,short_name,year,revenue_growth_pct,asset_liability_ratio_pct
```

## 四、3 分钟时间轴

### 0:00-0:15 标题与任务回顾

画面：
- 打开 `PROJECT_REQUIREMENTS.md` 或 GitHub Pages 首页。
- 指向第 6 项视频要求：“风险传导 -> 风险评估 -> 风险预警”。

旁白：
> 本项目围绕中国中铁财务风险管理展开，视频展示完整技术路线：公开数据采集，风险事件结构化，Gephi 风险传导图谱，文本与财务风险评估，以及机器学习预警模型。

### 0:15-0:40 公开数据与采集展示

画面：
- 浏览器切到中国中铁官网、定期报告页或上交所公告页。
- VS Code 展示 `scripts/collect_official_reports.py` 中的 `BASE_URL`、`LIST_PAGES`、`TARGETS`。
- 终端运行或展示结果：

```powershell
python .\scripts\collect_official_reports.py
Import-Csv .\data\interim\official_reports_manifest.csv | Select-Object period,report_type,filename
```

功能说明：
- `collect_official_reports.py`：从中国中铁公开报告页面归档年报、一季报，并补充评级报告。
- 输出：`data/raw/annual_reports/` 和 `data/interim/official_reports_manifest.csv`。

旁白：
> 数据入口首先来自公司官网、上交所和巨潮等公开披露渠道。本项目用 Python 归档 7 份报告，形成可追溯的报告清单，为后续财务指标、文本语料和官方风险事件提供来源。

### 0:40-1:05 风险事件与合规采集边界

画面：
- 浏览器快速展示裁判文书网入口、企查查入口，不登录、不绕过验证码。
- VS Code 展示 `scripts/build_external_risk_events.py` 顶部说明和 `evidence_status` 字段。
- 打开 `docs/EXTERNAL_RISK_EVENTS_SAMPLE.md` 或终端展示：

```powershell
python .\scripts\build_official_risk_events.py
python .\scripts\build_external_risk_events.py
Import-Csv .\data\processed\risk_events_combined.csv | Group-Object source_type
```

功能说明：
- `build_official_risk_events.py`：从年报、财务指标和评级报告生成 17 条官方披露风险事件。
- `build_external_risk_events.py`：整理 11 条司法、执行、企查查扩展样本，并标记 `core`、`candidate`、`verify`。
- 输出：`data/interim/risk_events_official_seed.csv`、`data/interim/risk_events_external_sample.csv`、`data/processed/risk_events_combined.csv`。

旁白：
> 外部风险事件不做违规批量抓取。对于裁判文书、执行信息和企查查，本项目采用公开页面、公开 PDF 和合法可复核线索，统一录入事件表，并保留证据状态，避免把未复核线索直接当作法律事实。

### 1:05-1:35 风险传导图谱

画面：
- VS Code 展示 `scripts/build_risk_network.py` 的节点设计：`company`、`event`、`risk_type`、`year`、`source`、`related_party`。
- 终端运行：

```powershell
python .\scripts\build_risk_network.py
python .\scripts\analyze_risk_network.py
Import-Csv .\data\processed\risk_network_centrality.csv | Select-Object -First 8 label,node_type,weighted_degree,betweenness_centrality,pagerank
```

- 打开 `docs/assets/figures/risk_network_gephi_style.png`。

功能说明：
- `build_risk_network.py`：把 28 条事件转成节点表、边表和 GEXF。
- `analyze_risk_network.py`：计算加权度、中介中心性、PageRank、Louvain 社群，并生成报告图。
- 输出：`data/processed/risk_nodes.csv`、`data/processed/risk_edges.csv`、`outputs/gephi/china_railway_risk_network_enhanced.gexf`、`docs/assets/figures/risk_network_gephi_style.png`。

旁白：
> 风险传导部分把“公司、事件、风险类型、年份、来源和相关方”连成网络。最终形成 77 个节点、133 条边。中心性结果显示，合规风险和流动性风险是当前样本中较核心的风险类型，诉讼、执行和子公司事件承担了桥接作用。

### 1:35-2:00 风险评估：财务、文本与事件矩阵

画面：
- 打开 `financial_trends.png`、`text_risk_heatmap.png`、`risk_event_matrix.png`。
- VS Code 简短展示：
  - `scripts/extract_financial_indicators.py`
  - `scripts/build_text_risk_index.py`
  - `scripts/build_word2vec_risk_terms.py`
  - `scripts/build_report_figures.py`

建议终端展示：

```powershell
python .\scripts\extract_financial_indicators.py
python .\scripts\build_text_risk_index.py
python .\scripts\build_word2vec_risk_terms.py
python .\scripts\build_report_figures.py
```

功能说明：
- `extract_financial_indicators.py`：整理 2021-2025 年收入、利润、现金流、负债率、合同资产、应收账款和利息保障倍数。
- `build_text_risk_index.py`：用种子词和 jieba 权重计算文本风险指标。
- `build_word2vec_risk_terms.py`：用 Word2Vec 扩展风险词典并生成扩展文本风险指标。
- `build_report_figures.py`：生成财务趋势、文本热力图、风险词图和事件矩阵。

旁白：
> 风险评估部分使用多源指标交叉验证。2025 年中国中铁营业收入和归母净利润下行，资产负债率升至 78.12%，利息保障倍数降至 2.98。文本层面，偿债风险和组织传导风险得分较高；事件矩阵则把发生概率和影响程度结合起来，识别高优先级风险。

### 2:00-2:35 风险预警模型

画面：
- 浏览器展示东方财富 HSF10 接口示例，说明同业财务面板来源。
- VS Code 展示：
  - `scripts/collect_peer_financial_panel.py`
  - `scripts/train_financial_warning_model.py`
- 终端展示：

```powershell
python .\scripts\collect_peer_financial_panel.py
python .\scripts\train_financial_warning_model.py
Import-Csv .\outputs\tables\warning_model_metrics.csv
Import-Csv .\data\processed\china_railway_warning_predictions.csv
```

功能说明：
- `collect_peer_financial_panel.py`：采集 11 家建筑工程类上市公司 2021-2025 年财务面板，共 55 条记录。
- `train_financial_warning_model.py`：构造下一年度财务压力标签，训练 Logistic Regression 和 Random Forest。
- 输出：`data/processed/warning_model_dataset.csv`、`outputs/models/financial_warning_*.joblib`、`outputs/tables/warning_model_metrics.csv`、`data/processed/china_railway_warning_predictions.csv`、`docs/FINANCIAL_WARNING_MODEL.md`。

旁白：
> 预警模型部分不是用单家公司硬训练，而是引入 11 家同业上市公司面板。模型在测试集上的 F1 为 0.8235。回代中国中铁后，2025 年特征对应 2026 年观察概率较高，Logistic 为 0.9780，Random Forest 为 0.9037，提示后续仍应关注盈利修复、债务覆盖和现金回款。

### 2:35-2:50 弹性风险管理结果

画面：
- 打开 `resilience_radar_2025.png` 和 `resilience_score_trend.png`。
- VS Code 展示 `scripts/build_resilience_model.py` 的四个维度字段。

运行命令：

```powershell
python .\scripts\build_resilience_model.py
Import-Csv .\data\processed\resilience_scores.csv | Select-Object -Last 1
```

功能说明：
- `build_resilience_model.py`：从财务缓冲、经营缓冲、治理信用缓冲、网络韧性四个维度评价风险缓冲能力。
- 输出：`data/processed/resilience_scores.csv`、`docs/assets/figures/resilience_radar_2025.png`、`docs/assets/figures/resilience_score_trend.png`。

旁白：
> 弹性风险管理模型用于解释企业能否吸收风险冲击。2025 年综合韧性得分为 33.11，处于低位修复区间，其中经营缓冲最弱，说明管理重点应回到项目毛利、结算、回款和合同资产压降。

### 2:50-3:00 总结与交付物

画面：
- 打开 `outputs/video/china_railway_risk_3min_deck.pptx` 或 `paper/course_paper_formatted.pdf`。
- 展示 GitHub Pages 或 `docs/FIGURES_CATALOG.md`。

可运行：

```powershell
python .\scripts\build_video_deck.py
python .\scripts\build_template_formatted_paper.py
```

旁白：
> 最终，项目形成了从公开数据采集、风险事件结构化、图谱传导识别、风险评估、机器学习预警到弹性管理建议的完整闭环。报告、图表、模型结果和视频 PPT 都可以由脚本复现。

## 五、建议展示的代码文件

| 展示优先级 | 代码文件 | 展示重点 | 主要输出 |
|---:|---|---|---|
| 1 | `scripts/collect_official_reports.py` | 公开报告页面、目标报告、下载清单 | `official_reports_manifest.csv`、年报 PDF |
| 2 | `scripts/build_external_risk_events.py` | 司法/执行/企查查样本、证据状态、合规边界 | `risk_events_external_sample.csv`、`risk_events_combined.csv` |
| 3 | `scripts/build_risk_network.py` | 事件如何变成节点、边和 GEXF | `risk_nodes.csv`、`risk_edges.csv`、`china_railway_risk_network.gexf` |
| 4 | `scripts/analyze_risk_network.py` | 加权度、中介中心性、PageRank、Louvain 社群 | 中心性表、增强 GEXF、风险网络图 |
| 5 | `scripts/build_text_risk_index.py` | 种子词、jieba 权重、文本风险得分 | `text_risk_index_by_year.csv` |
| 6 | `scripts/build_word2vec_risk_terms.py` | Word2Vec 扩词、扩展风险词典 | `risk_terms_expanded.json`、扩展文本指标 |
| 7 | `scripts/collect_peer_financial_panel.py` | 同业面板采集、东方财富接口 | `peer_financial_panel.csv` |
| 8 | `scripts/train_financial_warning_model.py` | 标签规则、Logistic、Random Forest、预测概率 | 模型文件、指标表、预测表 |
| 9 | `scripts/build_resilience_model.py` | 四维缓冲评分 | 韧性评分表、雷达图、趋势图 |
| 10 | `scripts/build_report_figures.py` | 报告图表统一生成 | 7 张报告图 |

## 六、完整复现命令

如果要在视频前完整重跑项目，可按以下顺序执行。录屏时不建议全部运行，只选关键脚本展示即可。

```powershell
python .\scripts\collect_official_reports.py
python .\scripts\extract_financial_indicators.py
python .\scripts\extract_risk_text_corpus.py
python .\scripts\build_text_risk_index.py
python .\scripts\build_word2vec_risk_terms.py
python .\scripts\create_risk_event_template.py
python .\scripts\build_official_risk_events.py
python .\scripts\build_external_risk_events.py
python .\scripts\build_risk_network.py
python .\scripts\analyze_risk_network.py
python .\scripts\build_report_figures.py
python .\scripts\build_warning_model_features.py
python .\scripts\collect_peer_financial_panel.py
python .\scripts\train_financial_warning_model.py
python .\scripts\build_resilience_model.py
python .\scripts\build_video_deck.py
```

## 七、录屏时的取舍

3 分钟内不要展示所有代码细节。推荐只现场运行 4 段：

1. `collect_official_reports.py`：证明公开数据能进项目。
2. `build_external_risk_events.py`：证明风险事件结构统一，并说明合规边界。
3. `build_risk_network.py` + `analyze_risk_network.py`：证明风险传导图谱可复现。
4. `train_financial_warning_model.py`：证明预警模型可复现，并展示概率结果。

其余脚本用图片和输出文件带过。视频重点放在“数据如何流动”和“结果如何解释”，不要停留在安装依赖、打开文件夹或等待下载。

## 八、屏幕录制注意事项

- 不展示账号、Cookie、浏览器个人信息、下载目录里的私人文件。
- 企查查、裁判文书网、执行信息公开网只展示入口和合规说明，不录制登录、验证码或付费页面。
- 如果网络不稳定，直接展示已经生成的 CSV、Markdown、图表和 PDF。
- 每个终端命令只保留最后 2-3 行输出即可，避免观众看不清。
- 图表展示优先使用 `docs/assets/figures/` 下的最终图，不展示 `outputs/` 下的重复副本。
- 结尾一定回到完整闭环：公开数据 -> 事件表 -> 图谱中心性 -> 风险评估 -> 预警概率 -> 管理建议。

