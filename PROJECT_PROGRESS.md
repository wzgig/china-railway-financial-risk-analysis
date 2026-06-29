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
  - 未发现常见密钥、GitHub token、邮箱、手机号等敏感字符串。
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
