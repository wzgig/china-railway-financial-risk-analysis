# 项目进度记录

## 2026-06-29

- 操作者：Codex
- 目标：读取项目要求，建立课程项目规划与目录骨架。
- 已读资料：
  - 本地课程要求截图。
  - 本地课程要求 Markdown，该文件存在编码乱码。
  - 本地 `course-paper-workflow` skill 及其 `quality_gates.md`。
- 已完成：
  - 整理可读版要求到 `PROJECT_REQUIREMENTS.md`。
  - 创建项目目录：`docs/`、`data/`、`scripts/`、`configs/`、`outputs/`、`paper/` 等。
  - 创建详细任务计划、来源记录、检索记录、证据矩阵、报告大纲、方法和工具规划。
  - 初步查验中国中铁公开披露渠道、司法数据入口和企查查入口。
- 技能与插件：
  - 已使用本地 `course-paper-workflow`。
  - 当前阶段无需下载额外 skill 或插件。
- 验证：
  - 当前目录不是 Git 仓库，`git status` 返回 `fatal: not a git repository`。
  - 尚未运行数据脚本或模型验证。
- 下一步：
  - 补充截止日期和格式要求。
  - 下载年报、公告、评级报告等公开文件。
  - 确定司法和企业风险数据的合规获取方式。

## 2026-06-29 GitHub 发布准备

- 操作者：Codex
- 目标：将项目整理为公开 GitHub 仓库并发布 GitHub Pages。
- 已完成：
  - 将原始课程截图和乱码 Markdown 加入 `.gitignore`，仅保留整理后的公开要求文本。
  - 准备 GitHub Pages 首页和仓库发布配置。
- 隐私检查：
  - 未发现常见密钥、GitHub token、电子联络方式等敏感字符串。
  - 原始课程材料保留在本地，不纳入公开仓库。

## 2026-06-29 GitHub 发布完成

- 操作者：Codex
- 目标：创建公开 GitHub 仓库、推送项目并启用 GitHub Pages。
- 已完成：
  - 初始化 Git 仓库并创建首个提交：`docs: scaffold financial risk analysis project`。
  - 创建公开仓库：`https://github.com/wzgig/china-railway-financial-risk-analysis`。
  - 推送 `main` 分支到远程 `origin`。
  - 设置仓库主页：`https://wzgig.github.io/china-railway-financial-risk-analysis/`。
  - 配置 GitHub Pages 从 `main` 分支的 `/docs` 目录发布。
  - 设置仓库 topics：`financial-risk`、`china-railway`、`gephi`、`machine-learning`、`text-mining`、`course-project`。
- 验证：
  - `git diff --cached --check` 通过。
  - GitHub Pages API 返回 `source.branch=main`、`source.path=/docs`、`https_enforced=true`。
  - Pages 发布状态在配置后进入 `building`。

## 2026-06-29 文献与草稿准备

- 操作者：Codex
- 用户补充：
  - 截止日期为 2026-07-10。
  - 已上传长沙理工大学本科毕业设计（论文）撰写规范样张。
  - 当前阶段先做前期准备和草稿，暂不生成 Word。
  - 参考文献按期刊论文质量标准检索整理，并输出 EndNote 可导入文件和国标格式清单。
- 已完成：
  - 使用 LibreOffice 提取 `.doc` 模板文本，整理结构要点到 `docs/FORMAT_TEMPLATE_NOTES.md`。
  - 更新 `COURSE_PAPER_TASK_PLAN.md`、`configs/project_config.yaml`、`SOURCES.md`、`LITERATURE_SEARCH_RECORD.md`、`EVIDENCE_MATRIX.md`。
  - 检索并整理官方披露、评级报告、财务困境预警、机器学习、文本分析、Gephi 和 ERM 核心文献。
  - 生成 `paper/references.ris`、`paper/references.enw`、`paper/references.bib`、`paper/references_gbt7714.md`。
  - 完成草稿版报告 `paper/draft.md`。
- 合规与隐私：
  - 原始模板 `.doc` 加入 `.gitignore`，不纳入公开仓库。
  - 不绕过司法或商业平台访问限制。
- 下一步：
  - 下载 2021-2025 年报全文，抽取可比财务指标。
  - 合规采集风险事件样本。
  - 生成风险图谱节点边表和文本风险词典。

## 2026-06-29 官方报告采集

- 操作者：Codex
- 目标：按照项目规划完成第一批官方披露文件采集。
- 已完成：
  - 新增脚本 `scripts/collect_official_reports.py`。
  - 从中国中铁官网解析定期报告页，下载 2021-2025 年年度报告和 2026Q1 报告。
  - 下载联合资信 2025 年跟踪评级报告。
  - 生成本地清单 `data/interim/official_reports_manifest.csv`。
  - 将可公开的来源清单写入 `docs/OFFICIAL_REPORTS_MANIFEST.md`。
- 本地原始文件：
  - `data/raw/annual_reports/2021_annual_report.pdf`
  - `data/raw/annual_reports/2022_annual_report.pdf`
  - `data/raw/annual_reports/2023_annual_report.pdf`
  - `data/raw/annual_reports/2024_annual_report.pdf`
  - `data/raw/annual_reports/2025_annual_report.pdf`
  - `data/raw/annual_reports/2026_q1_report.pdf`
  - `data/raw/annual_reports/2025_lianhe_rating_report.pdf`
- 验证：
  - PDF 文件均已下载且大小非零。
  - `python -m py_compile .\scripts\collect_official_reports.py` 通过。
- 下一步：
  - 从年报 PDF 抽取财务指标和风险披露文本。

## 2026-06-29 初始财务指标整理

- 操作者：Codex
- 目标：从官方年报中抽取中国中铁 2021-2025 年主要会计数据。
- 已完成：
  - 使用 `pdfplumber` 读取 2025、2024、2023、2022 年报 PDF。
  - 定位“近三年主要会计数据和财务指标”表。
  - 整理 `docs/FINANCIAL_INDICATORS_INITIAL.md`，包含营业收入、归母净利润、扣非归母净利润、经营活动现金流量净额、归母净资产和总资产。
- 验证：
  - `pdfplumber` 和 `pandas` 可用。
  - 指标均来自公开年报原文表格。
- 下一步：
  - 抽取合同资产、应收账款、短期债务、有息债务、利息保障倍数和担保承诺。

## 2026-06-29 财务风险指标与文本语料前处理

- 操作者：Codex
- 用户要求：
  - 若已有记录每次工作和后续目标的文件，则继续使用，不重复创建。
  - 按规划继续下一步工作。
- 文件判断：
  - 已有 `PROJECT_PROGRESS.md` 用于记录每次工作内容、验证和下一步目标，因此未另建重复文件。
- 已完成：
  - 新增 `scripts/extract_financial_indicators.py`，从官方年报整理 2021-2025 年财务风险指标。
  - 生成本地结构化数据 `data/processed/financial_risk_indicators.csv`。
  - 生成公开摘要 `docs/FINANCIAL_RISK_INDICATORS.md`。
  - 新增 `configs/risk_seed_terms.json`，覆盖流动性、偿债、营运、盈利、项目、合规、市场、组织传导风险。
  - 新增 `scripts/extract_risk_text_corpus.py`，从年报文本缓存抽取风险种子词命中片段。
  - 生成本地中间语料 `data/interim/risk_text_corpus_seed_matches.csv`。
  - 生成公开摘要 `docs/RISK_TEXT_CORPUS_SUMMARY.md`。
  - 更新 README 和 GitHub Pages 首页入口。
- 主要结果：
  - 财务指标显示：2023 年后营业收入和归母净利润连续下降；资产负债率从 2021 年 73.68% 上升到 2025 年 78.12%；利息保障倍数从 2021 年 4.09 下降到 2025 年 2.98。
  - 文本语料初筛命中 34,840 条种子词片段，可用于后续 jieba 分词、Word2Vec 扩词和风险词频权重计算。
- 验证：
  - `python -m py_compile .\scripts\collect_official_reports.py .\scripts\extract_financial_indicators.py .\scripts\extract_risk_text_corpus.py` 通过。
  - 财务指标脚本来源校验显示 2021-2025 年关键披露词均能在年报文本中找到。
- 下一步：
  - 对风险文本语料进行 jieba 分词和停用词清理，计算年度风险类别词频权重。
  - 准备司法、执行、企查查风险事件的合规采集模板。

## 2026-06-29 文本风险指数与事件模板整理

- 操作者：Codex
- 目标：按既定规划完成文本风险指标初步计算，并建立后续司法、执行和企业风险事件的合规采集模板。
- 已完成：
  - 新增 `configs/stopwords_zh.txt`，用于中文分词和关键词抽取停用词控制。
  - 新增 `scripts/build_text_risk_index.py`，对 2021-2025 年年报文本进行 jieba 分词、TF-IDF 风格关键词抽取和风险种子词命中统计。
  - 生成本地数据 `data/processed/text_risk_index_by_year.csv` 和 `data/processed/text_risk_terms_by_year.csv`。
  - 生成公开摘要 `docs/TEXT_RISK_INDEX.md`。
  - 新增 `configs/risk_event_schema.json` 和 `scripts/create_risk_event_template.py`，规范风险事件字段、事件类型、风险类型和合规边界。
  - 生成本地模板 `data/interim/risk_event_collection_template.csv`。
  - 生成公开说明 `docs/RISK_EVENT_COLLECTION_TEMPLATE.md`。
  - 更新 `paper/draft.md`，将文本风险指数的主要发现写入“初步风险识别”部分。
  - 更新 `SOURCES.md` 和 `EVIDENCE_MATRIX.md`，补充本轮脚本、配置、数据摘要和证据条目。
- 主要结果：
  - 文本风险指数显示，偿债风险在 2021、2022、2024、2025 年为综合文本风险得分最高类别。
  - 组织传导风险在各年度概率代理得分持续较高，提示子公司、联营、合营、担保等组织网络因素需要进入后续图谱。
  - 2025 年高权重词包括“债券”“子公司”“投资”“项目”“负债”“减值”“债务”“利息”“担保”。
- 合规说明：
  - 风险事件模板仅用于公开、授权或人工合法导出数据的标准化录入。
  - 不绕过裁判文书网、执行信息公开网、企查查等平台的登录、验证码、付费或访问频率限制。
- 验证：
  - `git -c core.longpaths=true diff --check` 通过，仅提示 Windows 换行转换。
  - `python -m py_compile` 检查 5 个数据脚本通过。
  - 使用 `course-paper-workflow` 自带 preflight 对拟公开提交文件建立临时审计目录，结果为 `errors=0 warnings=0`。
  - 直接对完整项目目录运行 preflight 会扫描已忽略的年报全文缓存和中间语料，产生大量公开年报联系人、格式词和长数字链接误报；这些文件不纳入公开仓库。
- 下一步：
  - 对公开披露中的诉讼、担保、评级关注事项先做一批可复核样本事件。
  - 在事件样本基础上生成 Gephi 节点表、边表和 GEXF 风险图谱。
  - 为财务指标和文本风险指数生成可直接用于报告的图表。

## 2026-06-29 官方风险事件种子与图谱预览

- 操作者：Codex
- 目标：先用官方披露生成可复核风险事件种子样本，并验证 Gephi 图谱输入格式。
- 已完成：
  - 扩展 `configs/risk_event_schema.json`，增加 `financial_pressure`、`asset_quality_signal`、`litigation_contingency` 等官方披露事件类型。
  - 新增 `scripts/build_official_risk_events.py`，从 2021-2025 年财务指标、年报或有事项和联合资信 2025 跟踪评级报告生成官方披露风险事件。
  - 生成本地事件表 `data/interim/risk_events_official_seed.csv`。
  - 生成公开摘要 `docs/OFFICIAL_RISK_EVENTS_SAMPLE.md`。
  - 新增 `scripts/build_risk_network.py`，将风险事件转换为节点表、边表和 Gephi GEXF 文件。
  - 生成本地 `data/processed/risk_nodes.csv`、`data/processed/risk_edges.csv` 和 `outputs/gephi/china_railway_risk_network.gexf`。
  - 生成公开摘要 `docs/RISK_NETWORK_PREVIEW.md`。
  - 更新 README、GitHub Pages 首页、`SOURCES.md` 和 `EVIDENCE_MATRIX.md`。
- 主要结果：
  - 生成 17 条官方披露风险事件种子样本。
  - 种子图谱包含 36 个节点、78 条边。
  - 当前加权度最高的实体节点为中国中铁股份有限公司，风险类型中合规风险、偿债风险和组织传导风险较突出。
- 验证：
  - `python .\scripts\build_official_risk_events.py` 成功生成事件表和公开摘要。
  - `python .\scripts\build_risk_network.py` 成功生成节点表、边表、GEXF 和公开预览。
  - `python -m py_compile` 检查新增脚本通过。
  - 使用临时公开审计目录运行 `course-paper-workflow` preflight，结果为 `errors=0 warnings=0`。
- 下一步：
  - 人工核验并补充裁判文书、执行信息和企业风险平台样本。
  - 用新增事件样本重新计算图谱中心性和社群结构。
  - 生成财务指标趋势图、文本风险热力图和风险矩阵图。

## 2026-06-29 报告图表素材生成

- 操作者：Codex
- 目标：将财务指标、文本风险指标和官方风险事件样本转成报告可用图表。
- 已完成：
  - 新增 `scripts/build_report_figures.py`。
  - 生成财务趋势图、文本风险热力图、2025 年高权重风险词图和官方事件风险矩阵图。
  - 本地图表副本输出到 `outputs/figures/`。
  - GitHub Pages 图表输出到 `docs/assets/figures/`。
  - 生成公开图表目录 `docs/FIGURES_CATALOG.md`。
  - 更新 README、GitHub Pages 首页、`SOURCES.md` 和 `EVIDENCE_MATRIX.md`。
- 验证：
  - `python .\scripts\build_report_figures.py` 成功生成 4 张 PNG 和图表目录。
  - 已检查财务趋势图、文本热力图、风险词条图和风险矩阵图，中文字体正常，矩阵标签已做错位处理。
  - `python -m py_compile`、`git diff --check` 和临时公开目录 preflight 均通过。
- 下一步：
  - 将图表结论写入 `paper/draft.md` 的实证分析段落。
  - 补充司法、执行和企业风险样本后重跑风险矩阵与图谱。
  - 准备模型特征表和机器学习预警样本设计。

## 2026-06-29 完成度回顾与 Word2Vec 扩词补强

- 操作者：Codex
- 用户要求：
  - 回顾目前所有工作，判断是否已经完成期末任务要求。
  - 若当前阶段未完全完成，则对目前工作进行提升。
- 完成度判断：
  - 当前项目可作为阶段性过程材料提交，但还不能作为完整期末作业提交。
  - 已完成前期准备、官方数据整理、参考文献、文本种子指标、官方风险事件种子、图谱预览和报告图表。
  - 仍缺机器学习预警模型、司法/执行/企查查扩展样本、最终 Word/PDF 和 3 分钟视频。
- 已完成：
  - 新增 `COURSE_REQUIREMENTS_AUDIT.md`，逐条审计六项期末任务完成度。
  - 更新 `PROJECT_REQUIREMENTS.md`，补入截止日期和模板状态，修正早期“截止日期未提供”的过时表述。
  - 安装并使用 `gensim`，补齐 Word2Vec 扩词能力。
  - 新增 `scripts/build_word2vec_risk_terms.py`，从 2021-2025 年年报文本训练 Word2Vec 模型。
  - 生成 `configs/risk_terms_expanded.json`、本地候选词明细和扩展文本风险指数。
  - 生成公开摘要 `docs/WORD2VEC_RISK_TERMS.md`。
  - 更新 `paper/draft.md`，加入财务趋势、文本风险、Word2Vec 扩词、官方风险事件矩阵和图谱预览结论。
  - 更新 README、GitHub Pages 首页、`SOURCES.md` 和 `EVIDENCE_MATRIX.md`。
- 主要结果：
  - 年报文本切分得到 26,875 个 Word2Vec 训练句段。
  - 语义过滤后保留 62 个候选扩展词。
  - 扩展指数与种子词指数方向一致，仍显示偿债风险、组织传导风险、营运风险和市场风险为高关注类别。
- 验证：
  - `python .\scripts\build_word2vec_risk_terms.py` 成功生成扩展词典、候选词明细、扩展文本风险指数和公开摘要。
  - `python -m py_compile` 覆盖 9 个脚本通过。
  - `git diff --check` 通过，仅提示 Windows 换行转换。
  - 临时公开目录 preflight 结果为 `errors=0 warnings=0`。
- 下一步：
  - 构建机器学习预警模型和特征重要性结果。
  - 继续合规补充司法、执行和企业风险样本。
  - 准备最终 Word/PDF 和 3 分钟视频。

## 2026-06-29 司法/执行/企查查扩展样本与模型特征表

- 操作者：Codex
- 用户要求：
  - 按流程优先补充缺失的司法、执行、企查查扩展样本。
  - 后续进行机器学习财务风险预警模型。
- 已完成：
  - 使用本地 `course-paper-workflow` skill 对齐课程论文工作流。
  - 新增 `scripts/build_external_risk_events.py`，将公开法院 PDF、公开裁判文书转载、执行信息报道和企查查公开报道转引数据整理为标准风险事件。
  - 生成本地扩展事件表 `data/interim/risk_events_external_sample.csv`，共 11 条事件。
  - 生成本地合并事件表 `data/processed/risk_events_combined.csv`，共 28 条事件。
  - 生成公开摘要 `docs/EXTERNAL_RISK_EVENTS_SAMPLE.md`，明确 `core`、`candidate`、`verify` 三类证据状态和合规边界。
  - 修改 `scripts/build_risk_network.py`，图谱脚本优先读取合并事件表，缺失时回退到官方披露种子表。
  - 重跑风险图谱，生成 77 个节点、133 条边的节点表、边表和 GEXF。
  - 新增 `scripts/build_warning_model_features.py`，合并财务指标、Word2Vec 文本指标和风险事件聚合特征。
  - 生成本地模型特征表 `data/processed/model_features_china_railway.csv`，共 5 个年度观测。
  - 生成公开摘要 `docs/MODEL_FEATURE_TABLE.md`，说明规则标签和后续同业面板建模安排。
  - 更新 `paper/draft.md`、README、GitHub Pages 首页、`SOURCES.md`、`LITERATURE_SEARCH_RECORD.md`、`EVIDENCE_MATRIX.md`、`COURSE_REQUIREMENTS_AUDIT.md`、`docs/DATA_DICTIONARY.md` 和 `scripts/README.md`。
- 主要结果：
  - 外部样本构成：司法样本 3 条、执行样本 5 条、企查查样本 3 条。
  - 证据状态：`core` 2 条、`candidate` 5 条、`verify` 4 条。
  - 合并图谱规模从 36 节点/78 边扩展到 77 节点/133 边。
  - 年度特征表中，2023 年主要由事件数量和执行类金额触发财务压力规则，2024-2025 年由盈利下滑、杠杆水平、利息保障倍数、合同资产占比和事件数量共同触发。
- 合规说明：
  - 未绕过裁判文书网、执行信息公开网或企查查的登录、验证码、付费或访问频率限制。
  - 企查查汇总型记录和媒体转引执行记录进入最终报告前需要人工复核和去重。
- 验证：
  - `python -m py_compile .\scripts\build_external_risk_events.py .\scripts\build_risk_network.py .\scripts\build_warning_model_features.py` 通过。
  - `python .\scripts\build_external_risk_events.py` 成功生成 11 条外部样本和 28 条合并事件。
  - `python .\scripts\build_risk_network.py` 成功生成 77 节点、133 边图谱输入。
  - `python .\scripts\build_warning_model_features.py` 成功生成 5 行年度模型特征表。
  - 使用 `course-paper-workflow` preflight 在临时公开审计目录运行，出现 2 个误报：均为巨潮资讯 PDF URL 中的长数字文件编号，不是个人信息。
- 下一步：
  - 对 `candidate` 和 `verify` 样本进行人工复核、截图/导出留痕和事件级去重。
  - 采集同业上市建筑企业 2021-2025 年财务指标，按当前特征表扩展为面板数据。
  - 训练 Logistic Regression 和 Random Forest 预警模型，输出 F1、Recall、AUC、特征重要性和中国中铁预测结果。

## 2026-06-29 同业面板与财务预警基线模型

- 操作者：Codex
- 用户要求：
  - 按照规划进度继续下一步工作。
- 已完成：
  - 使用本地 `course-paper-workflow` skill 对齐课程论文工作流。
  - 新增 `scripts/collect_peer_financial_panel.py`，通过东方财富 HSF10 财务分析接口采集同业上市建筑企业 2021-2025 年年报财务指标。
  - 生成本地同业面板 `data/processed/peer_financial_panel.csv`，覆盖 11 家公司、55 条年度记录。
  - 生成公开摘要 `docs/PEER_FINANCIAL_PANEL.md`，说明样本公司、数据口径和 2025 年指标预览。
  - 新增 `scripts/train_financial_warning_model.py`，构造下一年度财务压力规则标签，并训练 Logistic Regression 和 Random Forest 基线模型。
  - 生成本地监督学习数据 `data/processed/warning_model_dataset.csv`，共 44 条样本。
  - 生成本地模型文件 `outputs/models/financial_warning_logistic.joblib` 和 `outputs/models/financial_warning_random_forest.joblib`。
  - 生成本地评估表 `outputs/tables/warning_model_metrics.csv`、特征重要性表 `outputs/tables/warning_model_feature_importance.csv` 和中国中铁预测表 `data/processed/china_railway_warning_predictions.csv`。
  - 生成公开摘要 `docs/FINANCIAL_WARNING_MODEL.md`。
  - 更新 `paper/draft.md`、README、GitHub Pages 首页、`SOURCES.md`、`LITERATURE_SEARCH_RECORD.md`、`EVIDENCE_MATRIX.md`、`COURSE_REQUIREMENTS_AUDIT.md`、`docs/DATA_DICTIONARY.md`、`docs/MODEL_FEATURE_TABLE.md` 和 `scripts/README.md`。
- 主要结果：
  - 同业样本包括中国中铁、中国铁建、中国交建、中国建筑、中国电建、中国能建、上海建工、隧道股份、安徽建工、中国化学和中国中冶。
  - 监督样本标签分布为 0 类 22 条、1 类 22 条。
  - 测试集为 2024 年特征预测 2025 年压力标签，共 11 条样本。
  - Logistic Regression 和 Random Forest 测试集 F1 均为 0.8235，Recall 均为 0.7000。
  - 随机森林重要特征靠前的是现金比率、资产负债率、流动比率、毛利率、营业收入规模和利息保障倍数代理。
  - 中国中铁 2025 年特征对应 2026 年前瞻压力概率：Logistic Regression 为 0.9780，Random Forest 为 0.9037，两个模型均给出压力预警。
- 解释边界：
  - 东方财富 HSF10 为二级财经数据源；中国中铁核心财务结论仍以官方年报抽取数据为准。
  - 当前模型是小样本财务指标基线模型，标签是规则构造结果，不等同于违约、评级下调或投资建议。
  - 同业文本和事件特征尚未完整接入机器学习模型。
- 验证：
  - `python -m py_compile .\scripts\collect_peer_financial_panel.py .\scripts\train_financial_warning_model.py` 通过。
  - `python .\scripts\collect_peer_financial_panel.py` 成功生成 55 条同业年度记录。
  - `python .\scripts\train_financial_warning_model.py` 成功生成 44 条监督学习样本、模型文件、指标表、特征重要性表和公开摘要。
  - 使用 `course-paper-workflow` preflight 在临时公开审计目录运行，剩余 2 个误报：均为巨潮资讯 PDF URL 中的长数字文件编号，不是个人信息。
- 下一步：
  - 生成或整理模型相关图表，视篇幅纳入报告。
  - 对执行和企查查候选样本继续复核去重。
  - 准备 Gephi 最终导图、Word/PDF 输出和 3 分钟视频。
