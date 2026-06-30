"""Analyze the risk network and create Gephi-ready outputs."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


NODES_CSV = Path("data/processed/risk_nodes.csv")
EDGES_CSV = Path("data/processed/risk_edges.csv")
CENTRALITY_CSV = Path("data/processed/risk_network_centrality.csv")
COMMUNITY_CSV = Path("data/processed/risk_network_communities.csv")
TOP_CENTRALITY_CSV = Path("outputs/tables/risk_network_top_centrality.csv")
ENHANCED_GEXF = Path("outputs/gephi/china_railway_risk_network_enhanced.gexf")
LOCAL_FIGURE = Path("outputs/figures/risk_network_gephi_style.png")
PAGES_FIGURE = Path("docs/assets/figures/risk_network_gephi_style.png")
DOC_OUTPUT = Path("docs/RISK_NETWORK_CENTRALITY.md")

NODE_TYPE_COLORS = {
    "company": "#1f77b4",
    "event": "#d62728",
    "risk_type": "#ff7f0e",
    "year": "#7f7f7f",
    "source": "#2ca02c",
    "related_party": "#9467bd",
}

NODE_TYPE_LABELS = {
    "company": "主体",
    "event": "风险事件",
    "risk_type": "风险类型",
    "year": "年份",
    "source": "证据来源",
    "related_party": "相关方",
}


def configure_matplotlib() -> None:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 120


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_graph() -> nx.DiGraph:
    nodes = read_csv(NODES_CSV)
    edges = read_csv(EDGES_CSV)
    graph = nx.DiGraph()
    for node in nodes:
        graph.add_node(
            node["node_id"],
            label=node["label"],
            node_type=node["node_type"],
            year=node.get("year", ""),
            event_type=node.get("event_type", ""),
            risk_type=node.get("risk_type", ""),
            amount_rmb=node.get("amount_rmb", ""),
        )
    for edge in edges:
        graph.add_edge(
            edge["source"],
            edge["target"],
            weight=float(edge["weight"] or 1),
            edge_type=edge["edge_type"],
            event_id=edge.get("event_id", ""),
            source_label=edge.get("source_label", ""),
            target_label=edge.get("target_label", ""),
        )
    return graph


def undirected_strength_graph(graph: nx.DiGraph) -> nx.Graph:
    undirected = nx.Graph()
    for node, attrs in graph.nodes(data=True):
        undirected.add_node(node, **attrs)
    for source, target, attrs in graph.edges(data=True):
        weight = float(attrs.get("weight", 1))
        if undirected.has_edge(source, target):
            undirected[source][target]["weight"] += weight
        else:
            undirected.add_edge(source, target, weight=weight)
    return undirected


def community_map(undirected: nx.Graph) -> dict[str, int]:
    communities = nx.algorithms.community.louvain_communities(undirected, weight="weight", seed=42)
    mapping: dict[str, int] = {}
    for community_id, members in enumerate(communities, start=1):
        for node in members:
            mapping[node] = community_id
    return mapping


def centrality_rows(graph: nx.DiGraph) -> tuple[list[dict[str, str]], dict[str, int]]:
    undirected = undirected_strength_graph(graph)
    communities = community_map(undirected)
    weighted_degree = dict(undirected.degree(weight="weight"))
    degree_centrality = nx.degree_centrality(undirected)
    betweenness = nx.betweenness_centrality(undirected, weight=None, normalized=True)
    closeness = nx.closeness_centrality(undirected)
    pagerank = nx.pagerank(graph, weight="weight")
    in_strength = dict(graph.in_degree(weight="weight"))
    out_strength = dict(graph.out_degree(weight="weight"))

    rows: list[dict[str, str]] = []
    for node_id, attrs in graph.nodes(data=True):
        rows.append(
            {
                "node_id": node_id,
                "label": attrs.get("label", ""),
                "node_type": attrs.get("node_type", ""),
                "community": str(communities.get(node_id, 0)),
                "weighted_degree": f"{weighted_degree.get(node_id, 0):.4f}",
                "in_strength": f"{in_strength.get(node_id, 0):.4f}",
                "out_strength": f"{out_strength.get(node_id, 0):.4f}",
                "degree_centrality": f"{degree_centrality.get(node_id, 0):.6f}",
                "betweenness_centrality": f"{betweenness.get(node_id, 0):.6f}",
                "closeness_centrality": f"{closeness.get(node_id, 0):.6f}",
                "pagerank": f"{pagerank.get(node_id, 0):.6f}",
            }
        )
    rows.sort(key=lambda row: float(row["weighted_degree"]), reverse=True)
    return rows, communities


def write_csv_outputs(rows: list[dict[str, str]], graph: nx.DiGraph) -> None:
    CENTRALITY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with CENTRALITY_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    community_counts = Counter(row["community"] for row in rows)
    community_types: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        community_types[row["community"]][row["node_type"]] += 1
    community_rows = []
    for community, count in sorted(community_counts.items(), key=lambda item: int(item[0])):
        community_rows.append(
            {
                "community": community,
                "node_count": str(count),
                "type_mix": "; ".join(f"{key}:{value}" for key, value in sorted(community_types[community].items())),
            }
        )
    COMMUNITY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with COMMUNITY_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["community", "node_count", "type_mix"])
        writer.writeheader()
        writer.writerows(community_rows)

    top_rows = rows[:15]
    TOP_CENTRALITY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with TOP_CENTRALITY_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(top_rows[0].keys()))
        writer.writeheader()
        writer.writerows(top_rows)

    for row in rows:
        node_id = row["node_id"]
        for key, value in row.items():
            if key == "node_id":
                continue
            graph.nodes[node_id][key] = value
    ENHANCED_GEXF.parent.mkdir(parents=True, exist_ok=True)
    nx.write_gexf(graph, ENHANCED_GEXF)


def label_for_plot(label: str) -> str:
    replacements = {
        "organizational_propagation": "组织传导",
        "compliance": "合规",
        "liquidity": "流动性",
        "solvency": "偿债",
        "operation": "营运",
        "profitability": "盈利",
        "asset_quality_signal": "资产质量",
        "financial_pressure": "财务压力",
        "litigation_contingency": "未决诉讼",
        "execution_case": "执行案件",
    }
    for old, new in replacements.items():
        label = label.replace(old, new)
    if len(label) > 18:
        return label[:17] + "…"
    return label


def draw_network(graph: nx.DiGraph, rows: list[dict[str, str]]) -> None:
    undirected = undirected_strength_graph(graph)
    weights = [float(data.get("weight", 1)) for _, _, data in undirected.edges(data=True)]
    pos = nx.spring_layout(undirected, seed=12, weight="weight", k=0.95, iterations=300)

    row_by_id = {row["node_id"]: row for row in rows}
    weighted_values = [float(row_by_id[node]["weighted_degree"]) for node in undirected.nodes]
    min_weight, max_weight = min(weighted_values), max(weighted_values)
    denominator = max(max_weight - min_weight, 1)

    node_sizes = [
        90 + 1100 * (float(row_by_id[node]["weighted_degree"]) - min_weight) / denominator
        for node in undirected.nodes
    ]
    node_colors = [
        NODE_TYPE_COLORS.get(undirected.nodes[node].get("node_type", ""), "#999999")
        for node in undirected.nodes
    ]

    fig, ax = plt.subplots(figsize=(13, 9))
    nx.draw_networkx_edges(
        undirected,
        pos,
        ax=ax,
        width=[0.35 + min(weight, 5) * 0.24 for weight in weights],
        alpha=0.22,
        edge_color="#5A5A5A",
    )
    nx.draw_networkx_nodes(
        undirected,
        pos,
        ax=ax,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.9,
        linewidths=0.8,
        edgecolors="white",
    )

    top_label_nodes = set()
    for key in ("weighted_degree", "betweenness_centrality", "pagerank"):
        top_label_nodes.update(
            row["node_id"]
            for row in sorted(rows, key=lambda item: float(item[key]), reverse=True)[:8]
        )
    labels = {
        node: label_for_plot(undirected.nodes[node].get("label", ""))
        for node in top_label_nodes
        if node in undirected
    }
    nx.draw_networkx_labels(undirected, pos, labels=labels, font_size=8, ax=ax)

    legend_handles = [
        plt.Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=color,
            markersize=9,
            label=NODE_TYPE_LABELS.get(node_type, node_type),
        )
        for node_type, color in NODE_TYPE_COLORS.items()
        if any(undirected.nodes[node].get("node_type") == node_type for node in undirected.nodes)
    ]
    ax.legend(handles=legend_handles, loc="lower left", frameon=False, ncol=2)
    ax.set_title("中国中铁风险图谱中心性导图", fontsize=16, fontweight="bold")
    ax.text(
        0.01,
        0.12,
        "节点大小=加权度；颜色=节点类型；标签=加权度/中介中心性/PageRank较高节点",
        transform=ax.transAxes,
        fontsize=9,
        color="#555555",
    )
    ax.axis("off")
    fig.tight_layout()
    LOCAL_FIGURE.parent.mkdir(parents=True, exist_ok=True)
    PAGES_FIGURE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(LOCAL_FIGURE, dpi=220, bbox_inches="tight")
    fig.savefig(PAGES_FIGURE, dpi=220, bbox_inches="tight")
    plt.close(fig)


def markdown_table(rows: list[dict[str, str]], limit: int, fields: list[str]) -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "|" + "|".join("---" for _ in fields) + "|"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(row[field] for field in fields) + " |")
    return lines


def write_markdown(rows: list[dict[str, str]], graph: nx.DiGraph) -> None:
    type_counts = Counter(nx.get_node_attributes(graph, "node_type").values())
    edge_type_counts = Counter(data.get("edge_type", "") for _, _, data in graph.edges(data=True))
    top_weighted = sorted(rows, key=lambda row: float(row["weighted_degree"]), reverse=True)
    top_betweenness = sorted(rows, key=lambda row: float(row["betweenness_centrality"]), reverse=True)
    top_pagerank = sorted(rows, key=lambda row: float(row["pagerank"]), reverse=True)

    lines = [
        "# Gephi 最终导图与中心性解释",
        "",
        "复现脚本：`scripts/analyze_risk_network.py`",
        "",
        "## 复现产物",
        "",
        "- 增强版 Gephi 文件：`outputs/gephi/china_railway_risk_network_enhanced.gexf`",
        "- 节点中心性表：`data/processed/risk_network_centrality.csv`",
        "- 社群摘要表：`data/processed/risk_network_communities.csv`",
        "- Top 中心性表：`outputs/tables/risk_network_top_centrality.csv`",
        "- 报告导图：`docs/assets/figures/risk_network_gephi_style.png`",
        "",
        "## 网络规模",
        "",
        f"- 节点数：{graph.number_of_nodes()}",
        f"- 边数：{graph.number_of_edges()}",
        "",
        "### 节点类型",
        "",
        "| 节点类型 | 数量 |",
        "|---|---:|",
    ]
    for node_type, count in sorted(type_counts.items()):
        lines.append(f"| {node_type} | {count} |")

    lines.extend(["", "### 边类型", "", "| 边类型 | 数量 |", "|---|---:|"])
    for edge_type, count in sorted(edge_type_counts.items()):
        lines.append(f"| {edge_type} | {count} |")

    lines.extend(
        [
            "",
            "## 导图预览",
            "",
            "![风险图谱中心性导图](assets/figures/risk_network_gephi_style.png)",
            "",
            "## 加权度最高节点",
            "",
        ]
    )
    lines.extend(markdown_table(top_weighted, 10, ["label", "node_type", "community", "weighted_degree", "pagerank"]))

    lines.extend(["", "## 中介中心性最高节点", ""])
    lines.extend(markdown_table(top_betweenness, 10, ["label", "node_type", "community", "betweenness_centrality", "weighted_degree"]))

    lines.extend(["", "## PageRank 最高节点", ""])
    lines.extend(markdown_table(top_pagerank, 10, ["label", "node_type", "community", "pagerank", "weighted_degree"]))

    lines.extend(
        [
            "",
            "## 中心性解释",
            "",
            "- 加权度刻画节点与风险事件、风险类型、年份、来源之间的总体连接强度。中国中铁股份有限公司加权度最高，说明该样本仍以母公司官方披露和合并事件为主。",
            "- 合规风险和流动性风险在风险类型节点中更靠前，说明诉讼、执行、限制消费和供应链付款类事件已经成为图谱中的主要外部风险线索。",
            "- 中介中心性较高的节点连接多个事件、年份和风险类型，适合解释风险传导中的桥接作用；若子公司或相关方节点中介中心性上升，应作为后续复核重点。",
            "- PageRank 更偏向识别被高权重事件指向的稳定核心节点，适合与加权度共同判断关键风险类别。",
            "",
            "## Gephi 布局建议",
            "",
            "1. 在 Gephi 中打开 `outputs/gephi/china_railway_risk_network_enhanced.gexf`。",
            "2. `Appearance -> Nodes -> Partition` 按 `node_type` 着色。",
            "3. `Appearance -> Nodes -> Ranking` 按 `weighted_degree` 或 `pagerank` 调整节点大小。",
            "4. 布局可先用 `ForceAtlas2`，勾选 `LinLog mode` 与 `Prevent overlap`；稳定后再用 `Label Adjust`。",
            "5. 统计面板中重点查看 `weighted_degree`、`betweenness_centrality`、`pagerank` 与 `community` 字段。",
            "",
            "## 使用边界",
            "",
            "- 图谱使用官方披露、司法、执行和企查查扩展样本的合并事件表。",
            "- 当前执行和企查查部分样本仍有 `candidate` 或 `verify` 状态，中心性结果用于课程报告的风险线索解释，不应作为法律事实或投资结论。",
            "- 后续若补充更多逐条核验事件，应重新运行 `build_risk_network.py` 和本脚本。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    configure_matplotlib()
    graph = build_graph()
    rows, _ = centrality_rows(graph)
    write_csv_outputs(rows, graph)
    draw_network(graph, rows)
    write_markdown(rows, graph)
    print(f"wrote {CENTRALITY_CSV} ({len(rows)} rows)")
    print(f"wrote {COMMUNITY_CSV}")
    print(f"wrote {TOP_CENTRALITY_CSV}")
    print(f"wrote {ENHANCED_GEXF}")
    print(f"wrote {LOCAL_FIGURE}")
    print(f"wrote {PAGES_FIGURE}")
    print(f"wrote {DOC_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
