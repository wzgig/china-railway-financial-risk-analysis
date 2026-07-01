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

## 当前完成度判断

- 已基本完成：经营特征与风险机制、风险事件采集与图谱、文本风险指标、Word2Vec 扩词、机器学习预警模型、弹性风险管理模型、完整 Markdown 草稿、Word/PDF 草稿、主要报告图表和视频 PPT 草稿。
- 尚需完成：最终封面信息与目录校对、3 分钟视频成片、少数企查查汇总样本逐条导出复核。

## 验证记录

- Python 脚本均已通过 `py_compile` 检查。
- 主要脚本已能生成对应数据、图表和公开说明。
- `git diff --check` 通过，仅有 Windows 换行提示。
- 公开目录预检只剩巨潮资讯 PDF URL 数字编号误报，不属于个人信息。
