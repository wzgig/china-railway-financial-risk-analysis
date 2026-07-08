# -*- coding: utf-8 -*-
"""
用途：生成协鑫能科算电协同社会网络的报告图和交互网络图。
输入：data/processed/nodes.csv，data/processed/edges.csv，outputs/tables/network_metrics.csv，
     outputs/tables/stage_summary.csv
输出：outputs/figures/value_network_overview.png，
     outputs/figures/centrality_top_nodes.png，
     outputs/figures/stage_evolution.png，
     outputs/figures/community_network.png，
     outputs/figures/cost_mechanism_mapping.png，
     outputs/figures/data_type_distribution.png，
     outputs/figures/evidence_level_distribution.png，
     outputs/figures/stage_increment_distribution.png，
     outputs/network/value_network_interactive.html
说明：报告图内部不放标题，标题和解释应写在报告图注中。
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"
NETWORK_DIR = PROJECT_ROOT / "outputs" / "network"

NODES_PATH = PROCESSED_DIR / "nodes.csv"
EDGES_PATH = PROCESSED_DIR / "edges.csv"
METRICS_PATH = TABLE_DIR / "network_metrics.csv"
STAGE_SUMMARY_PATH = TABLE_DIR / "stage_summary.csv"

OVERVIEW_PATH = FIGURE_DIR / "value_network_overview.png"
CENTRALITY_PATH = FIGURE_DIR / "centrality_top_nodes.png"
STAGE_EVOLUTION_PATH = FIGURE_DIR / "stage_evolution.png"
COMMUNITY_PATH = FIGURE_DIR / "community_network.png"
COST_MAPPING_PATH = FIGURE_DIR / "cost_mechanism_mapping.png"
DATA_TYPE_DISTRIBUTION_PATH = FIGURE_DIR / "data_type_distribution.png"
EVIDENCE_DISTRIBUTION_PATH = FIGURE_DIR / "evidence_level_distribution.png"
STAGE_INCREMENT_PATH = FIGURE_DIR / "stage_increment_distribution.png"
INTERACTIVE_PATH = NETWORK_DIR / "value_network_interactive.html"

FONT_FAMILY = "Microsoft YaHei"

NODE_TYPE_COLORS = {
    "company": "#D55E00",
    "platform": "#0072B2",
    "resource": "#009E73",
    "capability": "#CC79A7",
    "market": "#E69F00",
    "customer": "#56B4E9",
    "policy": "#6A5ACD",
    "partner": "#7F7F7F",
}

NODE_TYPE_LABELS = {
    "company": "公司",
    "platform": "平台",
    "resource": "资源",
    "capability": "能力",
    "market": "市场",
    "customer": "客户",
    "policy": "政策",
    "partner": "伙伴",
}

EDGE_TYPE_COLORS = {
    "energy_supply": "#2CA02C",
    "data_flow": "#17BECF",
    "dispatch": "#1F77B4",
    "market_trade": "#FF7F0E",
    "technology_collaboration": "#9467BD",
    "policy_constraint": "#8C564B",
    "value_share": "#D62728",
}

EDGE_TYPE_LABELS = {
    "energy_supply": "能源供给",
    "data_flow": "数据流动",
    "dispatch": "调度控制",
    "market_trade": "市场交易",
    "technology_collaboration": "技术协同",
    "policy_constraint": "政策约束",
    "value_share": "价值分配",
}

EVIDENCE_LABELS = {
    "official": "官方政策",
    "company": "公司披露",
    "industry": "行业逻辑",
    "media": "媒体公开",
    "simulated": "结构化模拟",
}


def setup_style() -> None:
    plt.rcParams["font.family"] = FONT_FAMILY
    plt.rcParams["font.sans-serif"] = [
        FONT_FAMILY,
        "SimHei",
        "Noto Sans CJK SC",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    sns.set_theme(
        style="whitegrid",
        font=FONT_FAMILY,
        rc={
            "font.family": FONT_FAMILY,
            "font.sans-serif": [FONT_FAMILY, "SimHei", "Noto Sans CJK SC", "DejaVu Sans"],
            "axes.unicode_minus": False,
        },
    )


def read_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    for path in [NODES_PATH, EDGES_PATH, METRICS_PATH, STAGE_SUMMARY_PATH]:
        if not path.exists():
            raise FileNotFoundError(f"缺少输入文件：{path.relative_to(PROJECT_ROOT)}")
    nodes = pd.read_csv(NODES_PATH, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    edges = pd.read_csv(EDGES_PATH, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    metrics = pd.read_csv(METRICS_PATH, dtype={"node_id": str}, keep_default_na=False, encoding="utf-8-sig")
    stage_summary = pd.read_csv(STAGE_SUMMARY_PATH, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    edges["weight"] = edges["weight"].astype(float)
    for column in ["weighted_degree", "pagerank", "betweenness_centrality"]:
        metrics[column] = metrics[column].astype(float)
    for column in ["node_count", "edge_count", "density", "average_weight", "new_node_count", "new_edge_count"]:
        stage_summary[column] = stage_summary[column].astype(float)
    return nodes, edges, metrics, stage_summary


def build_graph(nodes: pd.DataFrame, edges: pd.DataFrame) -> nx.DiGraph:
    graph = nx.DiGraph()
    for row in nodes.to_dict(orient="records"):
        graph.add_node(row["node_id"], **row)
    for row in edges.to_dict(orient="records"):
        graph.add_edge(row["source"], row["target"], **row)
    return graph


def stable_layout(graph: nx.Graph) -> dict[str, tuple[float, float]]:
    return nx.spring_layout(graph, seed=42, k=0.72, iterations=180, weight="weight")


def label_nodes(metrics: pd.DataFrame, limit: int = 12) -> set[str]:
    top_weight = set(metrics.sort_values("weighted_degree", ascending=False).head(limit)["node_id"])
    top_between = set(metrics.sort_values("betweenness_centrality", ascending=False).head(6)["node_id"])
    return top_weight | top_between


def save_figure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def plot_overview(graph: nx.DiGraph, metrics: pd.DataFrame) -> None:
    undirected = graph.to_undirected()
    pos = stable_layout(undirected)
    label_set = label_nodes(metrics, limit=10)

    plt.figure(figsize=(13, 9))
    for edge_type, group_edges in pd.DataFrame([attrs for _, _, attrs in graph.edges(data=True)]).groupby("edge_type"):
        edgelist = [(row["source"], row["target"]) for _, row in group_edges.iterrows()]
        widths = [0.6 + float(graph[u][v]["weight"]) * 0.35 for u, v in edgelist]
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=edgelist,
            width=widths,
            alpha=0.22,
            edge_color=EDGE_TYPE_COLORS.get(edge_type, "#999999"),
            arrows=False,
        )

    for node_type, color in NODE_TYPE_COLORS.items():
        node_ids = [node for node, attrs in graph.nodes(data=True) if attrs.get("node_type") == node_type]
        if not node_ids:
            continue
        sizes = []
        for node_id in node_ids:
            pagerank = float(metrics.loc[metrics["node_id"] == node_id, "pagerank"].iloc[0])
            sizes.append(360 + pagerank * 12000)
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=node_ids,
            node_color=color,
            node_size=sizes,
            alpha=0.92,
            linewidths=0.8,
            edgecolors="white",
            label=node_type,
        )

    labels = {node_id: graph.nodes[node_id]["node_name"] for node_id in label_set if node_id in graph.nodes}
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8, font_family=FONT_FAMILY)
    plt.axis("off")
    plt.legend(loc="lower left", frameon=True, fontsize=9, ncol=2)
    save_figure(OVERVIEW_PATH)


def plot_centrality(metrics: pd.DataFrame) -> None:
    top = metrics.sort_values("pagerank", ascending=False).head(12).sort_values("pagerank")
    colors = [NODE_TYPE_COLORS.get(t, "#999999") for t in top["node_type"]]

    plt.figure(figsize=(10.5, 7))
    bars = plt.barh(top["node_name"], top["pagerank"], color=colors, alpha=0.88)
    plt.xlabel("PageRank")
    plt.ylabel("")
    for bar, value in zip(bars, top["pagerank"]):
        plt.text(value + 0.001, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center", fontsize=8)
    sns.despine(left=True, bottom=False)
    save_figure(CENTRALITY_PATH)


def plot_stage_evolution(stage_summary: pd.DataFrame) -> None:
    stage_summary = stage_summary.sort_values("stage")
    fig, ax1 = plt.subplots(figsize=(11, 6.5))
    ax2 = ax1.twinx()

    ax1.plot(stage_summary["stage"], stage_summary["node_count"], marker="o", linewidth=2.4, label="累计节点数", color="#0072B2")
    ax1.plot(stage_summary["stage"], stage_summary["edge_count"], marker="s", linewidth=2.4, label="累计边数", color="#D55E00")
    ax2.bar(stage_summary["stage"], stage_summary["density"], alpha=0.25, color="#009E73", label="网络密度")

    ax1.set_xlabel("阶段")
    ax1.set_ylabel("节点/边数量")
    ax2.set_ylabel("网络密度")
    ax1.grid(True, axis="y", alpha=0.25)

    lines, labels = ax1.get_legend_handles_labels()
    bars, bar_labels = ax2.get_legend_handles_labels()
    ax1.legend(lines + bars, labels + bar_labels, loc="upper left", frameon=True)

    for _, row in stage_summary.iterrows():
        ax1.text(row["stage"], row["edge_count"] + 1.2, f"+{int(row['new_edge_count'])}边", ha="center", fontsize=8)

    save_figure(STAGE_EVOLUTION_PATH)


def plot_community(graph: nx.DiGraph, metrics: pd.DataFrame) -> None:
    undirected = graph.to_undirected()
    pos = stable_layout(undirected)
    communities = sorted(metrics["community"].unique())
    palette = sns.color_palette("tab10", n_colors=max(len(communities), 3)).as_hex()
    community_color = {community: palette[i % len(palette)] for i, community in enumerate(communities)}
    metric_map = metrics.set_index("node_id")
    label_set = label_nodes(metrics, limit=9)

    plt.figure(figsize=(13, 9))
    nx.draw_networkx_edges(undirected, pos, width=0.8, alpha=0.18, edge_color="#666666")
    for community in communities:
        node_ids = metrics.loc[metrics["community"] == community, "node_id"].tolist()
        sizes = [330 + float(metric_map.loc[node_id, "weighted_degree"]) * 13 for node_id in node_ids]
        nx.draw_networkx_nodes(
            undirected,
            pos,
            nodelist=node_ids,
            node_size=sizes,
            node_color=community_color[community],
            alpha=0.9,
            linewidths=0.8,
            edgecolors="white",
            label=f"社群 {community}",
        )
    labels = {node_id: graph.nodes[node_id]["node_name"] for node_id in label_set if node_id in graph.nodes}
    nx.draw_networkx_labels(undirected, pos, labels=labels, font_size=8, font_family=FONT_FAMILY)
    plt.axis("off")
    plt.legend(loc="lower left", frameon=True, fontsize=9, ncol=2)
    save_figure(COMMUNITY_PATH)


def plot_cost_mapping(edges: pd.DataFrame) -> None:
    pivot = (
        edges.pivot_table(
            index="cost_mechanism",
            columns="edge_type",
            values="weight",
            aggfunc="sum",
            fill_value=0,
        )
        .reindex(
            [
                "能源成本",
                "调度成本",
                "交易成本",
                "协调成本",
                "柔性成本",
                "绿色合规成本",
                "运维成本",
                "收益分配",
            ]
        )
        .fillna(0)
    )

    plt.figure(figsize=(12, 6.8))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        cmap="YlGnBu",
        linewidths=0.5,
        cbar_kws={"label": "权重合计"},
    )
    plt.xlabel("边类型")
    plt.ylabel("成本机制")
    save_figure(COST_MAPPING_PATH)


def label_counts(series: pd.Series, labels: dict[str, str]) -> pd.DataFrame:
    counts = series.value_counts().rename_axis("raw_label").reset_index(name="count")
    counts["label"] = counts["raw_label"].map(labels).fillna(counts["raw_label"])
    return counts.sort_values("count", ascending=True)


def plot_data_type_distribution(nodes: pd.DataFrame, edges: pd.DataFrame) -> None:
    node_counts = label_counts(nodes["node_type"], NODE_TYPE_LABELS)
    edge_counts = label_counts(edges["edge_type"], EDGE_TYPE_LABELS)

    fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))
    axes[0].barh(
        node_counts["label"],
        node_counts["count"],
        color=[NODE_TYPE_COLORS.get(t, "#777777") for t in node_counts["raw_label"]],
        alpha=0.9,
    )
    axes[0].set_xlabel("节点数")
    axes[0].set_ylabel("")
    axes[0].grid(axis="x", alpha=0.25)
    for y, value in enumerate(node_counts["count"]):
        axes[0].text(value + 0.15, y, str(value), va="center", fontsize=9)

    axes[1].barh(
        edge_counts["label"],
        edge_counts["count"],
        color=[EDGE_TYPE_COLORS.get(t, "#777777") for t in edge_counts["raw_label"]],
        alpha=0.9,
    )
    axes[1].set_xlabel("边数")
    axes[1].set_ylabel("")
    axes[1].grid(axis="x", alpha=0.25)
    for y, value in enumerate(edge_counts["count"]):
        axes[1].text(value + 0.15, y, str(value), va="center", fontsize=9)

    sns.despine(left=True, bottom=False)
    save_figure(DATA_TYPE_DISTRIBUTION_PATH)


def plot_evidence_distribution(nodes: pd.DataFrame, edges: pd.DataFrame) -> None:
    evidence = pd.concat(
        [
            nodes["evidence_level"].value_counts().rename("节点数"),
            edges["evidence_level"].value_counts().rename("边数"),
        ],
        axis=1,
    ).fillna(0)
    evidence = evidence.reindex([key for key in EVIDENCE_LABELS if key in evidence.index]).fillna(0)
    evidence.index = [EVIDENCE_LABELS.get(value, value) for value in evidence.index]

    ax = evidence.plot(
        kind="bar",
        figsize=(11, 6.4),
        color=["#0072B2", "#D55E00"],
        alpha=0.88,
        width=0.72,
    )
    ax.set_xlabel("证据等级")
    ax.set_ylabel("数量")
    ax.tick_params(axis="x", rotation=0)
    ax.grid(axis="y", alpha=0.25)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3, fontsize=9)
    sns.despine(left=False, bottom=False)
    save_figure(EVIDENCE_DISTRIBUTION_PATH)


def plot_stage_increment(stage_summary: pd.DataFrame) -> None:
    stage_summary = stage_summary.sort_values("stage")
    x = range(len(stage_summary))
    width = 0.34
    fig, ax1 = plt.subplots(figsize=(11, 6.4))
    ax2 = ax1.twinx()

    bars_node = ax1.bar(
        [idx - width / 2 for idx in x],
        stage_summary["new_node_count"],
        width=width,
        label="新增节点数",
        color="#0072B2",
        alpha=0.86,
    )
    bars_edge = ax1.bar(
        [idx + width / 2 for idx in x],
        stage_summary["new_edge_count"],
        width=width,
        label="新增边数",
        color="#D55E00",
        alpha=0.86,
    )
    line = ax2.plot(
        list(x),
        stage_summary["average_weight"],
        marker="o",
        linewidth=2.2,
        color="#009E73",
        label="平均边权重",
    )

    ax1.set_xticks(list(x))
    ax1.set_xticklabels(stage_summary["stage"])
    ax1.set_xlabel("阶段")
    ax1.set_ylabel("新增节点/边数量")
    ax2.set_ylabel("平均边权重")
    ax1.grid(axis="y", alpha=0.25)
    ax1.bar_label(bars_node, fmt="%.0f", padding=3, fontsize=9)
    ax1.bar_label(bars_edge, fmt="%.0f", padding=3, fontsize=9)
    handles, labels = ax1.get_legend_handles_labels()
    line_handles, line_labels = ax2.get_legend_handles_labels()
    ax1.legend(handles + line_handles, labels + line_labels, loc="upper right", frameon=True)
    save_figure(STAGE_INCREMENT_PATH)


def make_edge_trace(graph: nx.DiGraph, pos: dict[str, tuple[float, float]], edge_type: str, color: str) -> go.Scatter:
    edge_x: list[float | None] = []
    edge_y: list[float | None] = []
    hover_text: list[str | None] = []

    for source, target, attrs in graph.edges(data=True):
        if attrs.get("edge_type") != edge_type:
            continue
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        text = (
            f"{graph.nodes[source]['node_name']} → {graph.nodes[target]['node_name']}<br>"
            f"类型：{attrs['edge_type']}<br>"
            f"权重：{attrs['weight']}<br>"
            f"阶段：{attrs['stage']}<br>"
            f"场景：{attrs['scenario']}<br>"
            f"机制：{attrs['cost_mechanism']}"
        )
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        hover_text += [text, text, None]

    return go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=1.2, color=color),
        opacity=0.38,
        hoverinfo="text",
        text=hover_text,
        name=edge_type,
    )


def plot_interactive(graph: nx.DiGraph, metrics: pd.DataFrame) -> None:
    NETWORK_DIR.mkdir(parents=True, exist_ok=True)
    pos = stable_layout(graph.to_undirected())
    metric_map = metrics.set_index("node_id")

    traces: list[go.Scatter] = []
    for edge_type, color in EDGE_TYPE_COLORS.items():
        if any(attrs.get("edge_type") == edge_type for _, _, attrs in graph.edges(data=True)):
            traces.append(make_edge_trace(graph, pos, edge_type, color))

    node_x = []
    node_y = []
    node_size = []
    node_color = []
    node_text = []
    node_labels = []
    for node_id, attrs in graph.nodes(data=True):
        x, y = pos[node_id]
        row = metric_map.loc[node_id]
        node_x.append(x)
        node_y.append(y)
        node_size.append(18 + float(row["pagerank"]) * 260)
        node_color.append(NODE_TYPE_COLORS.get(attrs["node_type"], "#999999"))
        node_labels.append(attrs["node_name"] if int(row["weighted_degree_rank"]) <= 10 else "")
        node_text.append(
            f"{attrs['node_name']}（{attrs['node_type']}）<br>"
            f"阶段：{attrs['stage']}<br>"
            f"价值角色：{attrs['value_role']}<br>"
            f"成本角色：{attrs['cost_role']}<br>"
            f"加权度：{row['weighted_degree']:.2f}<br>"
            f"中介中心性：{row['betweenness_centrality']:.4f}<br>"
            f"PageRank：{row['pagerank']:.4f}<br>"
            f"社群：{row['community']}<br>"
            f"证据等级：{attrs['evidence_level']}"
        )

    traces.append(
        go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            marker=dict(size=node_size, color=node_color, line=dict(color="white", width=1.2)),
            text=node_labels,
            textposition="top center",
            textfont=dict(size=11, color="#222222"),
            hoverinfo="text",
            hovertext=node_text,
            name="nodes",
        )
    )

    fig = go.Figure(data=traces)
    fig.update_layout(
        title=None,
        showlegend=True,
        hovermode="closest",
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.75)"),
    )
    fig.write_html(INTERACTIVE_PATH, include_plotlyjs="cdn", full_html=True)


def main() -> None:
    setup_style()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    NETWORK_DIR.mkdir(parents=True, exist_ok=True)

    nodes, edges, metrics, stage_summary = read_inputs()
    graph = build_graph(nodes, edges)

    plot_overview(graph, metrics)
    plot_centrality(metrics)
    plot_stage_evolution(stage_summary)
    plot_community(graph, metrics)
    plot_cost_mapping(edges)
    plot_data_type_distribution(nodes, edges)
    plot_evidence_distribution(nodes, edges)
    plot_stage_increment(stage_summary)
    plot_interactive(graph, metrics)

    print(f"已生成：{OVERVIEW_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{CENTRALITY_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{STAGE_EVOLUTION_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{COMMUNITY_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{COST_MAPPING_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{DATA_TYPE_DISTRIBUTION_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{EVIDENCE_DISTRIBUTION_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{STAGE_INCREMENT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"已生成：{INTERACTIVE_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
