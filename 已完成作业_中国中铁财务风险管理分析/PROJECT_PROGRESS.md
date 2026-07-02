# 项目进度记录

本文件只记录课程项目的重要阶段、产物、验证结果和剩余工作，便于后续复核与终稿整理。

## 2026-06-29 项目建档与公开仓库

- 整理课程要求，形成 `PROJECT_REQUIREMENTS.md`、`COURSE_PAPER_TASK_PLAN.md`、`COURSE_PAPER_DETAILED_OUTLINE.md`。
- 建立数据、脚本、报告、图表和视频材料目录。
- 创建公开仓库：<https://github.com/wzgig/china-railway-financial-risk-analysis>。
- 配置 GitHub Pages：<https://wzgig.github.io/china-railway-financial-risk-analysis/>。
- 原始课程材料、格式模板和年报 PDF 保留在本地，不纳入公开仓库。

## 2026-06-29 文献与格式准备

- 提取格式模板中的结构要求，形成 `docs/FORMAT_TEMPLATE_NOTES.md`。
- 完成参考文献库整理，输出 `paper/references.ris`、`paper/references.enw`、`paper/references.bib` 和 `paper/references_gbt7714.md`。
- 更新 `SOURCES.md`、`LITERATURE_SEARCH_RECORD.md`、`EVIDENCE_MATRIX.md` 和 `CORE_LITERATURE_NOTES.md`。
- 写出第一版 Markdown 草稿 `paper/draft.md`。

## 2026-06-29 官方报告与财务指标

- 编写 `scripts/collect_official_reports.py`，归档 2021-2025 年年报、2026 年一季报和 2025 年评级报告。
- 编写 `scripts/extract_financial_indicators.py`，整理 2021-2025 年财务风险指标。
- 生成 `data/processed/financial_risk_indicators.csv` 和 `docs/FINANCIAL_RISK_INDICATORS.md`。
- 主要观察：2023 年后营业收入和归母净利润下降，资产负债率上升，合同资产和应收账款占总资产比例提高。

## 2026-06-29 文本风险指标

- 编写 `scripts/extract_risk_text_corpus.py`，抽取年报风险语料初筛片段。
- 编写 `scripts/build_text_risk_index.py`，用种子词和 jieba 权重计算年度文本风险指标。
- 编写 `scripts/build_word2vec_risk_terms.py`，训练 Word2Vec 模型并扩展风险词典。
- 生成 `docs/RISK_TEXT_CORPUS_SUMMARY.md`、`docs/TEXT_RISK_INDEX.md` 和 `docs/WORD2VEC_RISK_TERMS.md`。
- 主要观察：偿债风险、组织传导风险、营运风险和市场风险是年报文本中的高关注类别。

## 2026-06-29 风险事件与图谱

- 编写 `scripts/create_risk_event_template.py`，建立风险事件采集字段。
- 编写 `scripts/build_official_risk_events.py`，形成 17 条官方披露风险事件种子样本。
- 编写 `scripts/build_external_risk_events.py`，补充 11 条司法、执行和企查查扩展样本。
- 编写 `scripts/build_risk_network.py`，生成节点表、边表和 Gephi GEXF 文件。
- 合并事件表共 28 条事件；风险图谱扩展到 77 个节点、133 条边。
- 执行和企查查部分记录仍保留 `candidate` 或 `verify` 状态，终稿前需要继续复核。

## 2026-06-29 图表与 Gephi 中心性

- 编写 `scripts/build_report_figures.py`，生成财务趋势、文本风险热力图、风险词图和风险矩阵。
- 编写 `scripts/analyze_risk_network.py`，计算加权度、中介中心性、PageRank 和 Louvain 社群。
- 生成增强版 Gephi 文件、中心性表和 `docs/assets/figures/risk_network_gephi_style.png`。
- 主要观察：合规风险和流动性风险是当前事件样本中的核心风险类型，若干诉讼执行节点具有较强桥接作用。

## 2026-06-29 机器学习预警模型

- 编写 `scripts/collect_peer_financial_panel.py`，采集 11 家建筑工程类上市公司 2021-2025 年财务面板。
- 编写 `scripts/train_financial_warning_model.py`，训练 Logistic Regression 和 Random Forest 财务预警基线模型。
- 生成 `docs/PEER_FINANCIAL_PANEL.md`、`docs/FINANCIAL_WARNING_MODEL.md`、模型评估表和中国中铁预测表。
- 测试集 F1 为 0.8235；中国中铁 2025 年特征对应 2026 年压力观察概率较高。
- 使用边界：模型是小样本财务指标基线模型，不能替代正式信用评级或投资判断。

## 2026-06-29 弹性风险管理模型

- 编写 `scripts/build_resilience_model.py`，构建财务缓冲、经营缓冲、治理信用缓冲和网络韧性四维评分。
- 生成 `docs/RESILIENCE_RISK_MANAGEMENT_MODEL.md`、`docs/assets/figures/resilience_radar_2025.png` 和 `docs/assets/figures/resilience_score_trend.png`。
- 2025 年综合韧性得分为 33.1，等级为“低位修复”；治理信用缓冲较强，经营缓冲和财务缓冲是主要短板。
- 课程选做项“弹性风险管理模型”已具备报告段落、评分表和图表。

## 2026-06-30 公开材料文字整理

- 精简公开材料中的过程性表述和过度模板化标题。
- 删除与研究内容无关的工具规划文档，减少公开材料中的过程痕迹。
- 将公开说明中的脚本说明改为复现口径，强化研究可复现性而不是过程展示感。
- 调整 README、任务计划、项目要求、来源清单、报告草稿和 Pages 索引，提高文档的正式研究记录感。

## 2026-06-30 报告草稿排版与视频材料

- 编写 `scripts/build_course_paper_docx.py`，从 `paper/draft.md` 和 `paper/references_gbt7714.md` 生成 Word/PDF 草稿。
- 生成 `paper/course_paper_draft.docx` 和 `paper/course_paper_draft.pdf`，并对首页、摘要页、图表页、弹性模型页和参考文献页进行渲染检查。
- 修正草稿中的图题编号、弹性评分表述、正文对齐、参考文献悬挂缩进和表格转换溢出问题。
- 扩充 `docs/VIDEO_STORYBOARD.md`，形成 3 分钟展示视频的时间轴、旁白稿和素材清单。
- 更新 `scripts/README.md`、`paper/README.md` 和 `COURSE_REQUIREMENTS_AUDIT.md`，使公开说明与当前成果一致。

## 2026-07-01 外部样本复核与视频制作准备

- 复核司法、执行和企查查扩展样本，更新 `scripts/build_external_risk_events.py` 和 `docs/EXTERNAL_RISK_EVENTS_SAMPLE.md`。
- 外部扩展样本仍为 11 条；证据状态调整为 `core` 2 条、`candidate` 7 条、`verify` 2 条。
- 每日经济新闻、维基文库转载裁判文书、新浪财经/经济参考网转载信息和财中社企查查转载信息均已记录复核边界；对需要登录、验证码或权限限制的平台不绕过限制。
- 新增 `docs/VIDEO_PRODUCTION_GUIDE.md`，说明 3 分钟视频的录制节奏、真人旁白路线和自动旁白路线。
- 编写 `scripts/build_video_deck.py`，生成本地 PPT 草稿 `outputs/video/china_railway_risk_3min_deck.pptx`。
- 本机检测到 PowerPoint 和中文系统语音，可继续制作自动旁白版视频；正式提交建议优先采用真人旁白。

## 2026-07-01 学校样张格式化 Word 版本

- 复核 `长沙理工大学本科毕业设计（论文）撰写规范样张.doc` 的页眉、页脚、摘要、目录、正文标题、图题和参考文献格式。
- 编写 `scripts/build_template_formatted_paper.py`，将 `paper/draft.md` 和 `paper/references_gbt7714.md` 生成为样张风格的 Word/PDF。
- 生成 `paper/course_paper_formatted.docx` 和 `paper/course_paper_formatted.pdf`，正文页码按“第 X 页 共 20 页”显示。
- 修正参考文献条目被合并、文末编号被上标化的问题；参考文献现按顺序编码制独立成段。
- 渲染检查目录页、正文第一页、结论页和参考文献页，页眉校名图、A4 页面、标题层级和正文页脚显示正常。
- `python -m py_compile scripts/build_template_formatted_paper.py` 通过；`pdfinfo` 显示格式稿为 24 页 A4；公开材料过程词扫描无命中。
- 更新 `docs/FORMAT_TEMPLATE_NOTES.md`、`paper/README.md`、`scripts/README.md` 和 `SOURCES.md`。

## 2026-07-01 报告终稿化润色

- 对 `paper/draft.md` 进行终稿化改写，重点压缩过程性说明，强化研究问题、指标逻辑、图谱解释、模型结果和管理建议之间的衔接。
- 删除正文中的“课程研究”“候选/待复核”“candidate/verify”“可能”等不适合终稿呈现的表达，改为证据权重、研究边界和管理含义的正式表述。
- 同步生成 `paper/course_paper_formatted.docx`、`paper/course_paper_formatted.pdf`、`paper/course_paper_draft.docx` 和 `paper/course_paper_draft.pdf`。
- 渲染检查摘要页、目录页、正文首页、结论页和参考文献页，格式稿为 23 页 A4，正文页脚显示为“第 X 页 共 19 页”。
- 将图谱段落中偏过程化的 GEXF/导图生成表述改为网络测度解释，突出加权度、中介中心性、PageRank 和 Louvain 社群划分的分析含义。

## 2026-07-01 报告图件版式优化

- 调整 `scripts/build_report_figures.py`、`scripts/analyze_risk_network.py` 和 `scripts/build_resilience_model.py`，去除图件顶部的内部题名，保留坐标轴、图例、色标和必要的节点说明。
- 重新生成 `docs/assets/figures/` 下的 7 张报告图件，并同步刷新 `docs/FIGURES_CATALOG.md`。
- 重新生成 `paper/course_paper_draft.docx`、`paper/course_paper_draft.pdf`、`paper/course_paper_formatted.docx` 和 `paper/course_paper_formatted.pdf`，确保 Word/PDF 嵌入的图件与最新图像一致。
- 正式 PDF 为 23 页 A4；已渲染第 11-18 页并检查图 1 至图 7，图内顶部无独立题名，图题均位于图下方图注位置。
- `python -m py_compile` 和 `git diff --check` 已通过；当前仓库未包含 `scripts/course_paper_preflight.py`，课程预检脚本无法执行。

## 2026-07-01 视频录屏流程梳理

- 新增 `docs/VIDEO_RECORDING_GUIDE_3MIN_WORKFLOW.md`，将 3 分钟展示视频拆分为公开数据采集、风险事件结构化、风险图谱、风险评估、机器学习预警和弹性管理六个录制段落。
- 明确视频中建议展示的网站入口、代码文件、终端命令、关键输出和旁白重点，区分可现场运行的公开采集脚本与只做入口展示的司法/执行/企查查平台。
- 将录制指南加入 `docs/index.md`，便于从 GitHub Pages 项目页进入。

## 2026-07-02 最终交付包整理

- 在 `交付/中国中铁财务风险管理分析_最终交付包_20260702/` 下整理最终报告、展示视频、演示材料、中文命名代码副本、配置文件、数据表、模型文件、Gephi 文件、公开报告 PDF、图表、参考文献和项目说明。
- 交付包保留最终版 `知世.doc`、`知世.pdf` 和完整展示视频，同时纳入分段录制素材、PPT、EndNote 文件、GB/T 7714 参考文献和 Python 依赖清单。
- 新增交付说明、环境安装与运行说明、代码文件说明与运行顺序，便于提交后复核项目结构与复现路径。

## 当前完成度判断

- 已基本完成：经营特征与风险机制、风险事件采集与图谱、文本风险指标、Word2Vec 扩词、机器学习预警模型、弹性风险管理模型、完整 Markdown 草稿、学校样张格式化 Word/PDF、主要报告图表和视频 PPT 草稿。
- 尚需完成：最终封面个人信息、3 分钟视频成片、少数企查查汇总样本逐条导出复核。

## 验证记录

- Python 脚本均已通过 `py_compile` 检查。
- 主要脚本已能生成对应数据、图表和公开说明。
- `git diff --check` 通过，仅有 Windows 换行提示。
- 公开目录预检只剩巨潮资讯 PDF URL 数字编号误报，不属于个人信息。
