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
cd "D:\Qiuhua Wang\个人资料\闲鱼\知世\大数据作业"
python -m pip install -r requirements.txt
python .\scripts\01_collect_public_sources.py
python .\scripts\02_build_network_dataset.py
python .\scripts\03_analyze_network.py
python .\scripts\04_visualize_network.py
```

运行后会生成公开来源检查、节点表、边表、数据字典、中心性指标、关键路径、阶段摘要、静态网络图和交互 HTML。

## 已生成成果

### 数据集

- `data/interim/source_check.csv`：公开来源可访问性与引用索引。
- `data/processed/nodes.csv`：协鑫能科算电协同网络节点表，共 38 个节点。
- `data/processed/edges.csv`：协鑫能科算电协同网络边表，共 85 条边。
- `data/processed/data_dictionary.csv`：节点表和边表字段说明。
- `data/processed/stage_summary.csv`：2024-2027 阶段累计网络摘要。

### 指标表

- `outputs/tables/network_metrics.csv`：度数、加权度、度中心性、中介中心性、接近中心性、PageRank 和社群编号。
- `outputs/tables/key_paths.csv`：7 条价值创造关键路径。
- `outputs/tables/stage_summary.csv`：阶段网络规模、密度、新增节点和新增边。
- `outputs/tables/network_summary.csv`：整体网络规模、密度、证据等级占比和连通分量。
- `outputs/tables/community_summary.csv`：社群规模、主导节点类型和关键节点。

### 图表与交互文件

- `outputs/figures/value_network_overview.png`：算电协同价值创造网络总图。
- `outputs/figures/centrality_top_nodes.png`：PageRank 中心性排名图。
- `outputs/figures/stage_evolution.png`：2024-2027 阶段演化图。
- `outputs/figures/community_network.png`：社群结构网络图。
- `outputs/figures/cost_mechanism_mapping.png`：成本机制与边类型映射图。
- `outputs/network/value_network_interactive.html`：可用于演示视频的交互网络图。

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
- 已生成第一版节点表、边表、中心性指标表、关键路径、阶段摘要、静态图和交互网络图。
- 下一步重点是基于指标表撰写 5000-8000 字报告初稿，并补充视频录制指南。
