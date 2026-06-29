# 中国中铁财务风险管理分析项目

本目录用于完成“中国中铁财务风险管理分析”课程项目，目标是形成一套可复现的分析流程：经营特征分析、风险数据采集、风险图谱、文本风险指标、机器学习预警模型、可选风险缓冲能力评价，以及约 3 分钟展示视频。

GitHub Pages 项目页：<https://wzgig.github.io/china-railway-financial-risk-analysis/>

公开仓库：<https://github.com/wzgig/china-railway-financial-risk-analysis>

## 项目主线

1. 经营特征与风险生成机制：从工程建筑行业、央企属性、基建周期、项目垫资、应收款、债务结构、境外业务和子公司网络解释风险来源。
2. 风险事件数据：围绕裁判文书、执行信息、企查查或同类企业信息平台，整理涉诉、执行、行政处罚、经营异常、担保、股权质押等事件。
3. 风险图谱：构造“主体-子公司-地区-风险事件-风险类别-时间”的网络，导出 Gephi 可读文件并识别风险传导路径。
4. 文本风险指标：以年报、公告、裁判文书、风险事件文本为语料，用种子词和 Word2Vec 扩充风险词典，用 jieba 计算词频权重。
5. 财务风险预警：将财务指标、文本风险指标和事件风险指标合并，训练机器学习模型并解释关键变量。
6. 视频展示：用 3 分钟讲清“风险传导 -> 风险评估 -> 风险预警”的流程、图谱和结论。

## 目录结构

```text
.
├─ PROJECT_REQUIREMENTS.md          # 从截图整理出的可读要求
├─ COURSE_PAPER_TASK_PLAN.md        # 详细执行计划
├─ PROJECT_PROGRESS.md              # 项目进度记录
├─ SOURCES.md                       # 资料来源与检索记录
├─ LITERATURE_SEARCH_RECORD.md      # 文献与数据检索记录模板
├─ EVIDENCE_MATRIX.md               # 证据矩阵模板
├─ COURSE_PAPER_DETAILED_OUTLINE.md # 报告详细大纲
├─ docs/                            # 方法、数据字典、工具规划、视频脚本
├─ data/raw/                        # 原始数据，保留下载或导出文件
├─ data/interim/                    # 清洗中间结果
├─ data/processed/                  # 建模与作图最终数据
├─ notebooks/                       # 探索性分析
├─ scripts/                         # 可复现脚本
├─ configs/                         # 项目配置
├─ outputs/                         # 图谱、图表、模型、表格、视频材料
└─ paper/                           # 报告正文、参考文献和最终稿
```

## 推荐运行路线

1. 先补齐教师要求：截止日期、格式模板、参考文献数量、提交文件类型。
2. 下载并归档年报、季报、公告、信用评级报告等公开文件到 `data/raw/annual_reports/`。
3. 合规获取司法和企业风险数据，原始导出放入 `data/raw/legal_cases/`、`data/raw/execution/`、`data/raw/qcc/`。
4. 编写清洗脚本，生成 `data/processed/risk_events.csv`、`risk_edges.csv`、`risk_nodes.csv`。
5. 导出 `outputs/gephi/china_railway_risk_network.gexf` 并在 Gephi 中完成布局、社区发现和中心性分析。
6. 构建文本风险词典和词频指标，输出风险热力图、风险矩阵和年度趋势。
7. 训练风险预警模型，输出模型性能、特征重要性和中国中铁风险预测结果。
8. 完成报告、图表、视频脚本和最终视频。

## 当前阶段产物

- 草稿版报告：[paper/draft.md](paper/draft.md)
- GB/T 7714 参考文献清单：[paper/references_gbt7714.md](paper/references_gbt7714.md)
- EndNote RIS 文件：[paper/references.ris](paper/references.ris)
- 官方报告下载清单：[docs/OFFICIAL_REPORTS_MANIFEST.md](docs/OFFICIAL_REPORTS_MANIFEST.md)
- 初始财务指标表：[docs/FINANCIAL_INDICATORS_INITIAL.md](docs/FINANCIAL_INDICATORS_INITIAL.md)
- 财务风险指标数据集：[docs/FINANCIAL_RISK_INDICATORS.md](docs/FINANCIAL_RISK_INDICATORS.md)
- 年报文本风险语料初筛：[docs/RISK_TEXT_CORPUS_SUMMARY.md](docs/RISK_TEXT_CORPUS_SUMMARY.md)
- 文本风险指标计算结果：[docs/TEXT_RISK_INDEX.md](docs/TEXT_RISK_INDEX.md)
- 风险事件采集模板：[docs/RISK_EVENT_COLLECTION_TEMPLATE.md](docs/RISK_EVENT_COLLECTION_TEMPLATE.md)
- 官方披露风险事件种子样本：[docs/OFFICIAL_RISK_EVENTS_SAMPLE.md](docs/OFFICIAL_RISK_EVENTS_SAMPLE.md)
- 风险图谱预览：[docs/RISK_NETWORK_PREVIEW.md](docs/RISK_NETWORK_PREVIEW.md)
- 图表目录：[docs/FIGURES_CATALOG.md](docs/FIGURES_CATALOG.md)
- 格式模板提取记录：[docs/FORMAT_TEMPLATE_NOTES.md](docs/FORMAT_TEMPLATE_NOTES.md)

## 技能与插件判断

当前已使用本地 `course-paper-workflow` skill 做课程项目规划，不需要额外下载新的 skill 或插件。后续若进入具体阶段，可按需使用本地已有能力：

- 文献与引用：`citation-management`、`bib-search-citation`。
- Python 测试与调试：`python-testing-patterns`、`debugging-strategies`。
- 表格与论文排版：`table-generation`、`pdf`、`course-paper-workflow`。
- 本地网页或交互测试：`playwright`、`browser:control-in-app-browser`。
- 视频旁白：`speech`，仅在需要生成配音时使用。
