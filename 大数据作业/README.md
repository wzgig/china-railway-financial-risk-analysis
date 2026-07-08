# 大数据作业：协鑫能科算电协同价值创造网络分析

本项目围绕协鑫能科（002015）“电力+算力”业务，构建产业链供应链价值创造网络，使用社会网络分析方法解释算电协同场景下的价值创造路径、成本管理机制、战略演化和动态能力链条。

## 作业要求

- 代码脚本：`.py` 或 `.ipynb`，覆盖数据模拟/加载、网络构建、指标计算、可视化。
- 数据集：`.csv`，至少包含边列表文件和必要的节点属性文件。
- 分析报告：5000-8000 字，包含引言、数据来源与处理、社会网络分析过程、成本管理洞察、局限性与改进方向。
- 演示视频：3 分钟内，展示交互网络图与关键发现。

## 当前项目结构

```text
configs/        字段规范、节点类型、边类型、权重口径
data/raw/       原始资料与公开披露文件索引
data/interim/   中间清洗结果
data/processed/ 最终节点表、边表和指标表
docs/           需求拆解、网络建模方案、报告结构、方法说明
logs/           运行记录
notebooks/      探索性分析笔记
outputs/        图表、网络文件、交互网页、视频素材
paper/          报告草稿和最终报告
scripts/        可复现脚本
交付/           最终提交包
```

## 可复现运行顺序

```powershell
cd "<知世项目目录>\大数据作业"
python -m pip install -r requirements.txt
python .\scripts\01_collect_public_sources.py
python .\scripts\02_build_network_dataset.py
python .\scripts\03_analyze_network.py
python .\scripts\04_visualize_network.py
python .\scripts\05_build_report_assets.py
python .\scripts\07_build_report_docx.py
python .\scripts\06_package_delivery.py
```

运行后会生成公开来源检查、节点表、边表、数据字典、中心性指标、关键路径、阶段摘要、静态网络图、交互 HTML、报告素材说明、Word 报告和最终交付目录。

## 已生成成果

### 数据集

- `data/interim/source_check.csv`：公开来源可访问性与引用索引。
- `data/processed/nodes.csv`：协鑫能科算电协同网络节点表，共 38 个节点。
- `data/processed/edges.csv`：协鑫能科算电协同网络边表，共 85 条边。
- `data/processed/data_dictionary.csv`：节点表和边表字段说明。
- `data/processed/stage_summary.csv`：2024-2027 阶段累计网络摘要。
- `docs/数据字典.md`：面向报告正文的数据字典说明。

### 指标表

- `outputs/tables/network_metrics.csv`：度数、加权度、度中心性、中介中心性、接近中心性、PageRank 和社群编号。
- `outputs/tables/key_paths.csv`：7 条价值创造关键路径。
- `outputs/tables/stage_summary.csv`：阶段网络规模、密度、新增节点和新增边。
- `outputs/tables/network_summary.csv`：整体网络规模、密度、证据等级占比和连通分量。
- `outputs/tables/community_summary.csv`：社群规模、主导节点类型和关键节点。
- `outputs/tables/report_asset_index.csv`：报告图表与交互图索引。

### 图表与交互文件

- `outputs/figures/value_network_overview.png`：算电协同价值创造网络总图。
- `outputs/figures/centrality_top_nodes.png`：PageRank 中心性排名图。
- `outputs/figures/stage_evolution.png`：2024-2027 阶段演化图。
- `outputs/figures/community_network.png`：社群结构网络图。
- `outputs/figures/cost_mechanism_mapping.png`：成本机制与边类型映射图。
- `outputs/figures/data_type_distribution.png`：节点类型与边类型分布图。
- `outputs/figures/evidence_level_distribution.png`：节点与边证据等级分布图。
- `outputs/figures/stage_increment_distribution.png`：阶段新增节点与边分布图。
- `outputs/network/value_network_interactive.html`：可用于演示视频的交互网络图。

### 报告、说明与交付

- `paper/协鑫能科算电协同价值创造网络分析报告.md`：5000-8000 字分析报告初稿，覆盖引言、数据来源与处理、社会网络分析过程、成本管理洞察、动态能力链条、局限性与结论。
- `paper/协鑫能科算电协同价值创造网络分析报告.docx`：以中国中铁财务风险管理分析最终版 Word 样式为模板生成的 Word 报告。
- `docs/图表目录.md`：报告图件和交互网络图目录。
- `docs/结果摘要.md`：关键指标、关键路径、阶段摘要和管理含义。
- `docs/任务完成度复盘.md`：逐项对照老师要求和提示知识点的完成度检查表。
- `docs/视频录制指南.md`：3 分钟内场景决策解说视频分镜和口播稿。
- `交付/`：由 `scripts/06_package_delivery.py` 生成的最终提交包，分为报告、代码、数据、说明、视频五类，其中 `交付/报告/` 同时包含 Markdown 和 Word 报告。

## 数据边界说明

- `source_manifest.csv` 和 `source_check.csv` 记录公开资料来源，节点和边均保留 `source_id` 或 `evidence_source`。
- `evidence_level` 区分 `official`、`company`、`industry`、`media`、`simulated`。
- 边权重为 1-5 分的相对重要性，不代表真实交易金额、合同规模或收入占比。
- 结构化模拟边用于补足产业链供应链逻辑，报告中应明确其模拟属性。

## 当前状态

- 已完成任务要求读取与拆解。
- 已评估中铁作业经验的可复用部分。
- 已建立项目文件夹、数据目录、输出目录、交付目录和基础配置文件。
- 已完成 `scripts/01_collect_public_sources.py` 至 `scripts/04_visualize_network.py`。
- 已生成第一版节点表、边表、中心性指标表、关键路径、阶段摘要、8 张静态图和交互网络图。
- 已完成 `scripts/05_build_report_assets.py`，生成图表目录、结果摘要和数据字典说明。
- 已完成 `scripts/06_package_delivery.py`，用于整理最终提交包。
- 已完成报告初稿和视频录制指南。
- 已完成 `scripts/07_build_report_docx.py`，以中铁最终版 Word 样式为模板生成本作业 Word 报告。
- 已完成任务完成度复盘，并对报告进行一轮去模板化语言打磨。
- 下一步可按视频指南录制 3 分钟以内演示视频，并将视频文件放入 `交付/视频/` 后提交课程平台。
