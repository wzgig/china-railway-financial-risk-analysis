# -*- coding: utf-8 -*-
"""
用途：汇总网络指标、关键路径、阶段摘要和图表文件，生成报告写作素材。
输入：data/processed/*.csv，outputs/tables/*.csv，outputs/figures/*.png，outputs/network/*.html
输出：docs/图表目录.md，docs/结果摘要.md，docs/数据字典.md，
     outputs/tables/report_asset_index.csv，logs/05_build_report_assets.log
说明：本脚本只整理已生成结果，不改变节点、边和指标计算口径。
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"
NETWORK_DIR = PROJECT_ROOT / "outputs" / "network"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
LOG_DIR = PROJECT_ROOT / "logs"

METRICS_PATH = TABLE_DIR / "network_metrics.csv"
KEY_PATHS_PATH = TABLE_DIR / "key_paths.csv"
NETWORK_SUMMARY_PATH = TABLE_DIR / "network_summary.csv"
COMMUNITY_SUMMARY_PATH = TABLE_DIR / "community_summary.csv"
STAGE_SUMMARY_PATH = TABLE_DIR / "stage_summary.csv"
DATA_DICTIONARY_PATH = PROCESSED_DIR / "data_dictionary.csv"
NODES_PATH = PROCESSED_DIR / "nodes.csv"
EDGES_PATH = PROCESSED_DIR / "edges.csv"
SOURCE_CHECK_PATH = INTERIM_DIR / "source_check.csv"

FIGURE_INDEX_PATH = DOCS_DIR / "图表目录.md"
RESULT_SUMMARY_PATH = DOCS_DIR / "结果摘要.md"
DATA_DICTIONARY_DOC_PATH = DOCS_DIR / "数据字典.md"
ASSET_INDEX_PATH = TABLE_DIR / "report_asset_index.csv"
LOG_PATH = LOG_DIR / "05_build_report_assets.log"

FIGURE_ASSETS = [
    (
        "图1",
        "算电协同价值创造网络总图",
        FIGURE_DIR / "value_network_overview.png",
        "展示公司、平台、资源、能力、市场、客户和政策之间的整体连接。",
    ),
    (
        "图2",
        "PageRank 中心性排名图",
        FIGURE_DIR / "centrality_top_nodes.png",
        "识别网络中影响力靠前的节点，支撑关键节点解释。",
    ),
    (
        "图3",
        "2024-2027 阶段演化图",
        FIGURE_DIR / "stage_evolution.png",
        "展示战略阶段中节点、边和密度的累计变化。",
    ),
    (
        "图4",
        "社群结构网络图",
        FIGURE_DIR / "community_network.png",
        "展示价值网络中的资源调度、市场交易、算法能力和算力场景子网络。",
    ),
    (
        "图5",
        "成本机制与边类型映射图",
        FIGURE_DIR / "cost_mechanism_mapping.png",
        "把边类型与能源成本、调度成本、交易成本、协调成本等管理机制对应起来。",
    ),
    (
        "交互图",
        "算电协同价值网络交互 HTML",
        NETWORK_DIR / "value_network_interactive.html",
        "用于 3 分钟演示视频，支持悬停查看节点指标和边属性。",
    ),
]


def rel(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"缺少输入文件：{rel(path)}")
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")


def markdown_table(df: pd.DataFrame, columns: Iterable[str] | None = None) -> str:
    table = df[list(columns)].copy() if columns else df.copy()
    if table.empty:
        return "（无记录）"

    header = "| " + " | ".join(table.columns) + " |"
    sep = "| " + " | ".join("---" for _ in table.columns) + " |"
    rows = []
    for _, row in table.iterrows():
        values = [str(row[col]).replace("\n", "；") for col in table.columns]
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *rows])


def build_asset_index() -> pd.DataFrame:
    rows = []
    for asset_id, title, path, use in FIGURE_ASSETS:
        rows.append(
            {
                "asset_id": asset_id,
                "title": title,
                "path": rel(path),
                "exists": path.exists(),
                "report_use": use,
            }
        )
    return pd.DataFrame(rows)


def write_asset_index(asset_index: pd.DataFrame) -> None:
    lines = [
        "# 图表目录",
        "",
        "以下图表由 `scripts/04_visualize_network.py` 生成，图内不设置顶部标题；报告正文使用图注解释图意。",
        "",
        markdown_table(
            asset_index.rename(
                columns={
                    "asset_id": "编号",
                    "title": "标题",
                    "path": "文件路径",
                    "exists": "是否存在",
                    "report_use": "报告用途",
                }
            )
        ),
        "",
        "## 报告插图建议",
        "",
        "- 图1用于第三节说明整体网络结构，强调虚拟电厂平台在资源、算法、市场和客户之间的桥梁作用。",
        "- 图2用于第三节解释中心性结果，突出 `AI赋能虚拟电厂平台`、`工商业用户侧负荷`、`能源调度模型` 等节点。",
        "- 图3用于第四、五节说明 2024-2027 年战略从资源连接走向生态协同。",
        "- 图4用于解释社群结构和产业链供应链子网络。",
        "- 图5用于连接社会网络分析与成本管理洞察。",
        "- 交互图用于演示视频，展示节点悬停信息和边类型图例。",
        "",
    ]
    FIGURE_INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")
    asset_index.to_csv(ASSET_INDEX_PATH, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)


def write_result_summary(
    network_summary: pd.DataFrame,
    metrics: pd.DataFrame,
    key_paths: pd.DataFrame,
    stage_summary: pd.DataFrame,
    community_summary: pd.DataFrame,
) -> None:
    ns = network_summary.iloc[0].to_dict()
    top_metrics = metrics.sort_values("pagerank", ascending=False).head(10).copy()
    top_metrics = top_metrics[
        [
            "node_name",
            "node_type",
            "weighted_degree",
            "betweenness_centrality",
            "pagerank",
            "community",
            "interpretation",
        ]
    ]
    top_metrics.columns = ["节点", "类型", "加权度", "中介中心性", "PageRank", "社群", "解释"]

    path_table = key_paths[["path_id", "path_node_names", "path_length", "total_weight", "purpose"]].copy()
    path_table.columns = ["路径编号", "节点链条", "长度", "权重合计", "用途"]

    stage_table = stage_summary[
        [
            "stage",
            "stage_goal",
            "node_count",
            "edge_count",
            "density",
            "new_edge_count",
            "key_nodes",
        ]
    ].copy()
    stage_table.columns = ["阶段", "目标", "累计节点", "累计边", "密度", "新增边", "关键节点"]

    community_table = community_summary.copy()
    community_table.columns = ["社群", "节点数", "主导节点类型", "关键节点", "平均 PageRank", "平均加权度"]

    lines = [
        "# 结果摘要",
        "",
        "本摘要用于报告第三节、第四节和视频解说脚本。所有网络指标均基于 `nodes.csv` 与 `edges.csv` 计算，边权重表示相对重要性，不代表真实交易金额、合同规模或收入占比。",
        "",
        "## 一、整体网络",
        "",
        f"- 节点数：{ns['node_count']}；边数：{ns['edge_count']}。",
        f"- 有向网络密度：{ns['density_directed']}；无向网络密度：{ns['density_undirected']}。",
        f"- 平均边权重：{ns['average_weight']}；官方或公司披露支撑的边占比：{ns['official_or_company_edge_share']}；结构化模拟边占比：{ns['simulated_edge_share']}。",
        f"- 最大弱连通分量包含 {ns['largest_weak_component_size']} 个节点，说明第一版网络能够形成完整价值链展示；最大强连通分量包含 {ns['largest_strong_component_size']} 个节点，说明平台、市场和反馈机制之间已经形成较多回路。",
        "",
        "## 二、中心性结果",
        "",
        markdown_table(top_metrics),
        "",
        "## 三、关键价值创造路径",
        "",
        markdown_table(path_table),
        "",
        "## 四、2024-2027 阶段摘要",
        "",
        markdown_table(stage_table),
        "",
        "## 五、社群摘要",
        "",
        markdown_table(community_table),
        "",
        "## 六、可直接写入报告的管理含义",
        "",
        "- `AI赋能虚拟电厂平台` 的 PageRank 和中介中心性均居前，说明它不是单纯的信息系统，而是资源聚合、调度协调、市场交易和客户服务之间的关键接口。",
        "- `工商业用户侧负荷` 排名靠前，表明需求侧柔性资源是算电协同价值创造的基础，价值来源不只在能源供给侧，也在用户可调节能力。",
        "- `能源调度模型`、`工业负荷模型` 等能力节点进入高影响力节点，说明算法模型承担把气象、电价、设备和负荷数据转化为调度策略的功能。",
        "- `AIDC/智算客户`、`数据中心/AIDC负荷` 和 `零碳园区能源平台` 构成 2025 年后扩展的算力场景，反映低碳、稳定、可追溯用能需求正在成为新价值端点。",
        "- 2024-2027 年阶段网络边数从 31 条增加到 85 条，说明价值网络由基础资源连接，逐步转向市场交易、收益分配和生态闭环。",
        "- 成本管理的重点可概括为能源成本、调度成本、交易成本、协调成本、绿色合规成本和收益分配六类机制。",
        "",
    ]
    RESULT_SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_data_dictionary_doc(
    dictionary: pd.DataFrame,
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    source_check: pd.DataFrame,
) -> None:
    node_fields = dictionary.loc[dictionary["table_name"] == "nodes"].copy()
    edge_fields = dictionary.loc[dictionary["table_name"] == "edges"].copy()
    node_fields = node_fields[["field_name", "data_type", "definition", "allowed_values"]]
    edge_fields = edge_fields[["field_name", "data_type", "definition", "allowed_values"]]
    node_fields.columns = ["字段", "类型", "含义", "取值说明"]
    edge_fields.columns = ["字段", "类型", "含义", "取值说明"]

    node_evidence = nodes["evidence_level"].value_counts().rename_axis("证据等级").reset_index(name="节点数")
    edge_evidence = edges["evidence_level"].value_counts().rename_axis("证据等级").reset_index(name="边数")
    edge_type = edges["edge_type"].value_counts().rename_axis("边类型").reset_index(name="边数")
    sources = source_check[
        ["source_id", "source_name", "publisher", "publish_date", "reachable", "citation_label"]
    ].copy()
    sources.columns = ["来源编号", "来源名称", "发布机构", "发布日期", "链接可访问", "引用标签"]

    lines = [
        "# 数据字典",
        "",
        "本说明对应 `data/processed/nodes.csv`、`data/processed/edges.csv` 和 `data/processed/data_dictionary.csv`。数据由公开资料约束下的结构化网络建模生成，公开资料与模拟关系均通过证据等级字段区分。",
        "",
        "## 一、节点表字段",
        "",
        markdown_table(node_fields),
        "",
        "## 二、边表字段",
        "",
        markdown_table(edge_fields),
        "",
        "## 三、节点证据等级分布",
        "",
        markdown_table(node_evidence),
        "",
        "## 四、边证据等级分布",
        "",
        markdown_table(edge_evidence),
        "",
        "## 五、边类型分布",
        "",
        markdown_table(edge_type),
        "",
        "## 六、来源索引",
        "",
        markdown_table(sources),
        "",
        "## 七、使用边界",
        "",
        "- `weight` 为 1-5 分相对重要性评分，用于网络计算，不代表真实交易金额、收入占比、合同规模或市场份额。",
        "- `simulated` 表示根据公开事实和产业链逻辑补充的结构化关系，报告中应作为情景建模结果而非公司披露事实。",
        "- 第一版网络用于课程作业的社会网络分析与场景决策解说，若用于正式投资、审计或经营决策，需要进一步接入真实交易、负荷和市场报价数据。",
        "",
    ]
    DATA_DICTIONARY_DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_log(asset_index: pd.DataFrame) -> None:
    lines = [
        f"运行时间：{datetime.now():%Y-%m-%d %H:%M:%S}",
        f"图表资产数量：{len(asset_index)}",
        f"缺失资产：{asset_index.loc[~asset_index['exists'], 'path'].tolist()}",
        f"输出文件：{rel(FIGURE_INDEX_PATH)}；{rel(RESULT_SUMMARY_PATH)}；{rel(DATA_DICTIONARY_DOC_PATH)}；{rel(ASSET_INDEX_PATH)}",
    ]
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    metrics = read_csv(METRICS_PATH)
    key_paths = read_csv(KEY_PATHS_PATH)
    network_summary = read_csv(NETWORK_SUMMARY_PATH)
    community_summary = read_csv(COMMUNITY_SUMMARY_PATH)
    stage_summary = read_csv(STAGE_SUMMARY_PATH)
    dictionary = read_csv(DATA_DICTIONARY_PATH)
    nodes = read_csv(NODES_PATH)
    edges = read_csv(EDGES_PATH)
    source_check = read_csv(SOURCE_CHECK_PATH)

    for column in ["weighted_degree", "betweenness_centrality", "pagerank"]:
        metrics[column] = metrics[column].astype(float)

    asset_index = build_asset_index()
    write_asset_index(asset_index)
    write_result_summary(network_summary, metrics, key_paths, stage_summary, community_summary)
    write_data_dictionary_doc(dictionary, nodes, edges, source_check)
    write_log(asset_index)

    missing = asset_index.loc[~asset_index["exists"], "path"].tolist()
    print(f"已生成：{rel(FIGURE_INDEX_PATH)}")
    print(f"已生成：{rel(RESULT_SUMMARY_PATH)}")
    print(f"已生成：{rel(DATA_DICTIONARY_DOC_PATH)}")
    print(f"已生成：{rel(ASSET_INDEX_PATH)}")
    if missing:
        print(f"提示：以下图表资产不存在：{missing}")


if __name__ == "__main__":
    main()
