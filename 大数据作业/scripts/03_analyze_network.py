# -*- coding: utf-8 -*-
"""
用途：计算协鑫能科算电协同社会网络指标、社群、关键路径和阶段摘要。
输入：data/processed/nodes.csv，data/processed/edges.csv
输出：outputs/tables/network_metrics.csv，outputs/tables/key_paths.csv，
     outputs/tables/network_summary.csv，outputs/tables/community_summary.csv，
     data/processed/stage_summary.csv，outputs/tables/stage_summary.csv
说明：最短路径使用 1/weight 作为距离，表示权重越高关系越强、路径距离越短。
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

import networkx as nx
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
NODES_PATH = PROCESSED_DIR / "nodes.csv"
EDGES_PATH = PROCESSED_DIR / "edges.csv"
METRICS_PATH = TABLE_DIR / "network_metrics.csv"
KEY_PATHS_PATH = TABLE_DIR / "key_paths.csv"
NETWORK_SUMMARY_PATH = TABLE_DIR / "network_summary.csv"
COMMUNITY_SUMMARY_PATH = TABLE_DIR / "community_summary.csv"
STAGE_SUMMARY_PROCESSED_PATH = PROCESSED_DIR / "stage_summary.csv"
STAGE_SUMMARY_OUTPUT_PATH = TABLE_DIR / "stage_summary.csv"

STAGE_ORDER = {"all": 0, "2024": 2024, "2025": 2025, "2026": 2026, "2027": 2027}
STAGE_GOALS = {
    "2024": "资源连接与虚拟电厂基础能力形成",
    "2025": "算电协同、绿色数据中心与零碳园区场景扩展",
    "2026": "市场交易、收益优化与成本精细化",
    "2027": "生态协同、价值共享与动态能力闭环",
}


def read_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not NODES_PATH.exists():
        raise FileNotFoundError(f"请先运行 02 脚本生成：{NODES_PATH.relative_to(PROJECT_ROOT)}")
    if not EDGES_PATH.exists():
        raise FileNotFoundError(f"请先运行 02 脚本生成：{EDGES_PATH.relative_to(PROJECT_ROOT)}")

    nodes = pd.read_csv(NODES_PATH, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    edges = pd.read_csv(EDGES_PATH, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    edges["weight"] = edges["weight"].astype(float)
    return nodes, edges


def build_graph(nodes: pd.DataFrame, edges: pd.DataFrame) -> nx.DiGraph:
    graph = nx.DiGraph()
    for row in nodes.to_dict(orient="records"):
        graph.add_node(row["node_id"], **row)

    for row in edges.to_dict(orient="records"):
        weight = float(row["weight"])
        attrs = dict(row)
        attrs["weight"] = weight
        attrs["distance"] = 1 / weight
        graph.add_edge(
            row["source"],
            row["target"],
            **attrs,
        )

    return graph


def build_undirected_graph(graph: nx.DiGraph) -> nx.Graph:
    undirected = nx.Graph()
    for node_id, attrs in graph.nodes(data=True):
        undirected.add_node(node_id, **attrs)

    for source, target, attrs in graph.edges(data=True):
        weight = float(attrs.get("weight", 1))
        if undirected.has_edge(source, target):
            undirected[source][target]["weight"] += weight
            undirected[source][target]["distance"] = 1 / undirected[source][target]["weight"]
        else:
            undirected.add_edge(source, target, weight=weight, distance=1 / weight)

    return undirected


def detect_communities(undirected: nx.Graph) -> dict[str, int]:
    if undirected.number_of_nodes() == 0:
        return {}

    try:
        import community as community_louvain  # type: ignore

        return community_louvain.best_partition(undirected, weight="weight", random_state=42)
    except Exception:
        communities = nx.algorithms.community.greedy_modularity_communities(undirected, weight="weight")
        mapping: dict[str, int] = {}
        for community_id, members in enumerate(communities):
            for node_id in members:
                mapping[node_id] = community_id
        return mapping


def make_interpretation(row: pd.Series) -> str:
    node_type = row["node_type"]
    name = row["node_name"]
    weighted_rank = int(row["weighted_degree_rank"])
    betweenness_rank = int(row["betweenness_rank"])
    pagerank_rank = int(row["pagerank_rank"])

    if weighted_rank <= 5 and betweenness_rank <= 5:
        return f"{name}同时具备高连接强度和桥梁作用，是跨资源、算法、市场和客户的关键协调节点。"
    if pagerank_rank <= 5:
        return f"{name}在整体网络中影响力靠前，可作为价值创造路径的重点解释对象。"
    if node_type == "policy":
        return f"{name}主要提供政策约束和规则输入，影响算电协同网络的演化方向。"
    if node_type == "capability":
        return f"{name}承担数据转化为调度或收益决策的能力节点功能。"
    if node_type == "market":
        return f"{name}承担交易或价值分配功能，连接调节能力和收益结果。"
    if node_type == "customer":
        return f"{name}体现需求侧价值共创，是网络收益回流的重要端点。"
    return f"{name}在网络中承担{row['value_role']}角色，支撑{row['cost_role']}管理。"


def calculate_metrics(nodes: pd.DataFrame, edges: pd.DataFrame, graph: nx.DiGraph) -> pd.DataFrame:
    undirected = build_undirected_graph(graph)
    communities = detect_communities(undirected)

    degree = dict(graph.degree())
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())
    weighted_degree = dict(graph.degree(weight="weight"))
    weighted_in_degree = dict(graph.in_degree(weight="weight"))
    weighted_out_degree = dict(graph.out_degree(weight="weight"))
    degree_centrality = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph, weight="distance", normalized=True)
    closeness = nx.closeness_centrality(graph, distance="distance")
    pagerank = nx.pagerank(graph, weight="weight")

    rows = []
    for row in nodes.to_dict(orient="records"):
        node_id = row["node_id"]
        rows.append(
            {
                **row,
                "degree": degree.get(node_id, 0),
                "in_degree": in_degree.get(node_id, 0),
                "out_degree": out_degree.get(node_id, 0),
                "weighted_degree": round(weighted_degree.get(node_id, 0), 4),
                "weighted_in_degree": round(weighted_in_degree.get(node_id, 0), 4),
                "weighted_out_degree": round(weighted_out_degree.get(node_id, 0), 4),
                "degree_centrality": round(degree_centrality.get(node_id, 0), 6),
                "betweenness_centrality": round(betweenness.get(node_id, 0), 6),
                "closeness_centrality": round(closeness.get(node_id, 0), 6),
                "pagerank": round(pagerank.get(node_id, 0), 6),
                "community": communities.get(node_id, -1),
            }
        )

    metrics = pd.DataFrame(rows)
    metrics["weighted_degree_rank"] = metrics["weighted_degree"].rank(ascending=False, method="min").astype(int)
    metrics["betweenness_rank"] = metrics["betweenness_centrality"].rank(ascending=False, method="min").astype(int)
    metrics["pagerank_rank"] = metrics["pagerank"].rank(ascending=False, method="min").astype(int)
    metrics["interpretation"] = metrics.apply(make_interpretation, axis=1)

    ordered_columns = [
        "node_id",
        "node_name",
        "node_type",
        "stage",
        "value_role",
        "cost_role",
        "evidence_level",
        "source_id",
        "degree",
        "in_degree",
        "out_degree",
        "weighted_degree",
        "weighted_in_degree",
        "weighted_out_degree",
        "degree_centrality",
        "betweenness_centrality",
        "closeness_centrality",
        "pagerank",
        "weighted_degree_rank",
        "betweenness_rank",
        "pagerank_rank",
        "community",
        "interpretation",
        "note",
    ]
    return metrics[ordered_columns].sort_values(["pagerank_rank", "weighted_degree_rank", "node_id"])


def path_weight(graph: nx.DiGraph, path: list[str]) -> float:
    return sum(float(graph[path[i]][path[i + 1]]["weight"]) for i in range(len(path) - 1))


def path_edge_types(graph: nx.DiGraph, path: list[str]) -> str:
    return " -> ".join(str(graph[path[i]][path[i + 1]]["edge_type"]) for i in range(len(path) - 1))


def node_names(graph: nx.DiGraph, path: Iterable[str]) -> list[str]:
    return [str(graph.nodes[node_id]["node_name"]) for node_id in path]


def calculate_key_paths(graph: nx.DiGraph) -> pd.DataFrame:
    path_specs = [
        ("P001", "N005", "N030", "清洁能源到智算客户的低碳供能路径"),
        ("P002", "N020", "N030", "政策目标到智算客户价值主张的传导路径"),
        ("P003", "N007", "N024", "储能资源进入辅助服务市场的调节收益路径"),
        ("P004", "N011", "N036", "气象数据到调节收益分成的算法转化路径"),
        ("P005", "N001", "N037", "公司战略到绿色溢价机制的价值提升路径"),
        ("P006", "N032", "N027", "设备数据接入到需求响应市场的流程支撑路径"),
        ("P007", "N021", "N030", "绿色数据中心政策到智算客户需求的约束路径"),
    ]

    rows = []
    for path_id, source, target, purpose in path_specs:
        try:
            path = nx.shortest_path(graph, source=source, target=target, weight="distance")
            names = node_names(graph, path)
            rows.append(
                {
                    "path_id": path_id,
                    "source": source,
                    "source_name": graph.nodes[source]["node_name"],
                    "target": target,
                    "target_name": graph.nodes[target]["node_name"],
                    "path_node_ids": " -> ".join(path),
                    "path_node_names": " -> ".join(names),
                    "path_length": len(path) - 1,
                    "total_weight": round(path_weight(graph, path), 4),
                    "edge_types": path_edge_types(graph, path),
                    "purpose": purpose,
                    "interpretation": f"{purpose}：{'、'.join(names)}构成可解释链条。",
                    "status": "ok",
                }
            )
        except nx.NetworkXNoPath:
            rows.append(
                {
                    "path_id": path_id,
                    "source": source,
                    "source_name": graph.nodes[source]["node_name"],
                    "target": target,
                    "target_name": graph.nodes[target]["node_name"],
                    "path_node_ids": "",
                    "path_node_names": "",
                    "path_length": "",
                    "total_weight": "",
                    "edge_types": "",
                    "purpose": purpose,
                    "interpretation": "当前方向性网络中不存在可达路径，可在报告中作为网络边界说明。",
                    "status": "no_path",
                }
            )

    return pd.DataFrame(rows)


def stage_value(stage: str) -> int:
    return STAGE_ORDER.get(str(stage), 9999)


def is_in_cumulative_stage(stage: str, year: int) -> bool:
    value = stage_value(stage)
    return value == 0 or value <= year


def calculate_stage_summary(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base_node_ids = set(nodes.loc[nodes["stage"] == "all", "node_id"])
    previous_nodes = set()
    previous_edges = set()

    for year_label in ["2024", "2025", "2026", "2027"]:
        year = int(year_label)
        cumulative_edges = edges.loc[edges["stage"].apply(lambda x: is_in_cumulative_stage(x, year))].copy()
        cumulative_edge_keys = set(zip(cumulative_edges["source"], cumulative_edges["target"], cumulative_edges["edge_type"]))
        endpoint_nodes = set(cumulative_edges["source"]) | set(cumulative_edges["target"])
        staged_nodes = set(nodes.loc[nodes["stage"].apply(lambda x: is_in_cumulative_stage(x, year)), "node_id"])
        active_nodes = base_node_ids | staged_nodes | endpoint_nodes

        stage_edges = edges.loc[edges["stage"] == year_label].copy()
        stage_node_ids = (set(stage_edges["source"]) | set(stage_edges["target"]) | set(nodes.loc[nodes["stage"] == year_label, "node_id"])) - previous_nodes
        new_edges = cumulative_edge_keys - previous_edges

        subgraph = nx.DiGraph()
        for _, row in nodes.loc[nodes["node_id"].isin(active_nodes)].iterrows():
            subgraph.add_node(row["node_id"], **row.to_dict())
        for _, row in cumulative_edges.iterrows():
            subgraph.add_edge(row["source"], row["target"], weight=float(row["weight"]))

        weighted_degree = dict(subgraph.degree(weight="weight"))
        top_nodes = sorted(weighted_degree, key=weighted_degree.get, reverse=True)[:3]
        top_node_names = "；".join(str(subgraph.nodes[node_id]["node_name"]) for node_id in top_nodes)
        scenario_mix = "；".join(
            f"{scenario}:{count}" for scenario, count in stage_edges["scenario"].value_counts().head(4).items()
        )

        rows.append(
            {
                "stage": year_label,
                "stage_goal": STAGE_GOALS[year_label],
                "node_count": subgraph.number_of_nodes(),
                "edge_count": subgraph.number_of_edges(),
                "density": round(nx.density(subgraph), 6) if subgraph.number_of_nodes() > 1 else 0,
                "average_weight": round(float(cumulative_edges["weight"].mean()), 4) if len(cumulative_edges) else 0,
                "new_node_count": len(stage_node_ids),
                "new_edge_count": len(new_edges),
                "key_nodes": top_node_names,
                "stage_scenario_mix": scenario_mix,
                "interpretation": f"{year_label} 年重点为{STAGE_GOALS[year_label]}，关键节点集中在{top_node_names}。",
            }
        )

        previous_nodes = active_nodes
        previous_edges = cumulative_edge_keys

    return pd.DataFrame(rows)


def calculate_network_summary(graph: nx.DiGraph, edges: pd.DataFrame) -> pd.DataFrame:
    undirected = build_undirected_graph(graph)
    summary = {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "density_directed": round(nx.density(graph), 6),
        "density_undirected": round(nx.density(undirected), 6),
        "average_weight": round(float(edges["weight"].mean()), 4),
        "official_or_company_edge_share": round(float(edges["evidence_level"].isin(["official", "company"]).mean()), 4),
        "simulated_edge_share": round(float((edges["evidence_level"] == "simulated").mean()), 4),
        "largest_weak_component_size": len(max(nx.weakly_connected_components(graph), key=len)),
        "largest_strong_component_size": len(max(nx.strongly_connected_components(graph), key=len)),
    }
    return pd.DataFrame([summary])


def calculate_community_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for community_id, group in metrics.groupby("community"):
        top = group.sort_values("pagerank", ascending=False).head(3)
        rows.append(
            {
                "community": community_id,
                "node_count": len(group),
                "dominant_node_types": "；".join(f"{k}:{v}" for k, v in group["node_type"].value_counts().head(3).items()),
                "top_nodes": "；".join(top["node_name"].tolist()),
                "avg_pagerank": round(float(group["pagerank"].mean()), 6),
                "avg_weighted_degree": round(float(group["weighted_degree"].mean()), 4),
            }
        )
    return pd.DataFrame(rows).sort_values("node_count", ascending=False)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    nodes, edges = read_inputs()
    graph = build_graph(nodes, edges)

    metrics = calculate_metrics(nodes, edges, graph)
    key_paths = calculate_key_paths(graph)
    stage_summary = calculate_stage_summary(nodes, edges)
    network_summary = calculate_network_summary(graph, edges)
    community_summary = calculate_community_summary(metrics)

    write_csv(metrics, METRICS_PATH)
    write_csv(key_paths, KEY_PATHS_PATH)
    write_csv(stage_summary, STAGE_SUMMARY_PROCESSED_PATH)
    write_csv(stage_summary, STAGE_SUMMARY_OUTPUT_PATH)
    write_csv(network_summary, NETWORK_SUMMARY_PATH)
    write_csv(community_summary, COMMUNITY_SUMMARY_PATH)

    print(f"已生成：{METRICS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{KEY_PATHS_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{STAGE_SUMMARY_PROCESSED_PATH.relative_to(PROJECT_ROOT)}")
    print(f"网络规模：{graph.number_of_nodes()} 个节点，{graph.number_of_edges()} 条边")


if __name__ == "__main__":
    main()
