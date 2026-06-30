"""Build a Gephi-ready risk network from risk events."""

from __future__ import annotations

import csv
import hashlib
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from xml.etree import ElementTree as ET


PREFERRED_EVENTS_CSV = Path("data/processed/risk_events_combined.csv")
FALLBACK_EVENTS_CSV = Path("data/interim/risk_events_official_seed.csv")
NODES_CSV = Path("data/processed/risk_nodes.csv")
EDGES_CSV = Path("data/processed/risk_edges.csv")
GEXF_OUTPUT = Path("outputs/gephi/china_railway_risk_network.gexf")
DOC_OUTPUT = Path("docs/RISK_NETWORK_PREVIEW.md")


def stable_node_id(node_type: str, label: str) -> str:
    digest = hashlib.sha1(f"{node_type}::{label}".encode("utf-8")).hexdigest()[:12]
    return f"{node_type}_{digest}"


def load_events() -> list[dict[str, str]]:
    events_path = PREFERRED_EVENTS_CSV if PREFERRED_EVENTS_CSV.exists() else FALLBACK_EVENTS_CSV
    if not events_path.exists():
        raise FileNotFoundError(
            f"Missing {events_path}; run scripts/build_official_risk_events.py first"
        )
    with events_path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def amount_weight(amount_rmb: str) -> Decimal:
    if not amount_rmb:
        return Decimal("1")
    amount_100m = Decimal(amount_rmb) / Decimal("100000000")
    if amount_100m >= Decimal("1000"):
        return Decimal("5")
    if amount_100m >= Decimal("500"):
        return Decimal("4")
    if amount_100m >= Decimal("100"):
        return Decimal("3")
    return Decimal("2")


def add_node(nodes: dict[str, dict[str, str]], node_type: str, label: str, **attrs: str) -> str:
    node_id = stable_node_id(node_type, label)
    if node_id not in nodes:
        node = {
            "node_id": node_id,
            "label": label,
            "node_type": node_type,
            "year": attrs.get("year", ""),
            "event_type": attrs.get("event_type", ""),
            "risk_type": attrs.get("risk_type", ""),
            "amount_rmb": attrs.get("amount_rmb", ""),
        }
        nodes[node_id] = node
    return node_id


def build_network(events: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    nodes: dict[str, dict[str, str]] = {}
    edges: list[dict[str, str]] = []

    def add_edge(source: str, target: str, source_label: str, target_label: str, edge_type: str, weight: Decimal, event_id: str) -> None:
        edges.append(
            {
                "edge_id": f"e{len(edges) + 1}",
                "source": source,
                "target": target,
                "source_label": source_label,
                "target_label": target_label,
                "edge_type": edge_type,
                "weight": str(weight.quantize(Decimal("0.01"))),
                "event_id": event_id,
            }
        )

    for event in events:
        company_label = event["company_name"]
        event_label = f"{event['event_id']} {event['event_type']}"
        risk_label = event["risk_type"]
        year_label = event["year"]

        company_id = add_node(nodes, "company", company_label)
        event_id = add_node(
            nodes,
            "event",
            event_label,
            year=event["year"],
            event_type=event["event_type"],
            risk_type=event["risk_type"],
            amount_rmb=event["amount_rmb"],
        )
        risk_id = add_node(nodes, "risk_type", risk_label)
        year_id = add_node(nodes, "year", year_label)
        source_id = add_node(nodes, "source", event["source_name"])

        severity = Decimal(event.get("severity_score") or "1")
        probability = Decimal(event.get("probability_score") or "1")
        amount_based = amount_weight(event.get("amount_rmb", ""))

        add_edge(company_id, event_id, company_label, event_label, "involves", max(severity, amount_based), event["event_id"])
        add_edge(event_id, risk_id, event_label, risk_label, "classified_as", probability, event["event_id"])
        add_edge(event_id, year_id, event_label, year_label, "occurred_in", Decimal("1"), event["event_id"])
        add_edge(event_id, source_id, event_label, event["source_name"], "evidenced_by", Decimal("1"), event["event_id"])

        if event.get("related_party"):
            party_label = event["related_party"]
            party_id = add_node(nodes, "related_party", party_label)
            add_edge(event_id, party_id, event_label, party_label, "related_to", Decimal("1"), event["event_id"])

    return list(nodes.values()), edges


def write_csv_outputs(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> None:
    NODES_CSV.parent.mkdir(parents=True, exist_ok=True)
    EDGES_CSV.parent.mkdir(parents=True, exist_ok=True)
    with NODES_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_id", "label", "node_type", "year", "event_type", "risk_type", "amount_rmb"])
        writer.writeheader()
        writer.writerows(nodes)
    with EDGES_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["edge_id", "source", "target", "source_label", "target_label", "edge_type", "weight", "event_id"])
        writer.writeheader()
        writer.writerows(edges)


def write_gexf(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> None:
    GEXF_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ET.register_namespace("", "http://www.gexf.net/1.2draft")
    gexf = ET.Element("{http://www.gexf.net/1.2draft}gexf", {"version": "1.2"})
    meta = ET.SubElement(gexf, "{http://www.gexf.net/1.2draft}meta", {"lastmodifieddate": "2026-06-29"})
    ET.SubElement(meta, "{http://www.gexf.net/1.2draft}creator").text = "scripts/build_risk_network.py"
    graph = ET.SubElement(gexf, "{http://www.gexf.net/1.2draft}graph", {"mode": "static", "defaultedgetype": "directed"})
    node_el = ET.SubElement(graph, "{http://www.gexf.net/1.2draft}nodes")
    for node in nodes:
        ET.SubElement(node_el, "{http://www.gexf.net/1.2draft}node", {"id": node["node_id"], "label": node["label"]})
    edge_el = ET.SubElement(graph, "{http://www.gexf.net/1.2draft}edges")
    for edge in edges:
        ET.SubElement(
            edge_el,
            "{http://www.gexf.net/1.2draft}edge",
            {
                "id": edge["edge_id"],
                "source": edge["source"],
                "target": edge["target"],
                "label": edge["edge_type"],
                "weight": edge["weight"],
            },
        )
    ET.ElementTree(gexf).write(GEXF_OUTPUT, encoding="utf-8", xml_declaration=True)


def write_markdown(nodes: list[dict[str, str]], edges: list[dict[str, str]]) -> None:
    node_type_counts = Counter(node["node_type"] for node in nodes)
    edge_type_counts = Counter(edge["edge_type"] for edge in edges)
    weighted_degree: defaultdict[str, Decimal] = defaultdict(Decimal)
    labels = {node["node_id"]: node["label"] for node in nodes}
    types = {node["node_id"]: node["node_type"] for node in nodes}
    for edge in edges:
        weight = Decimal(edge["weight"])
        weighted_degree[edge["source"]] += weight
        weighted_degree[edge["target"]] += weight
    top_nodes = sorted(weighted_degree.items(), key=lambda item: item[1], reverse=True)[:10]

    lines = [
        "# 风险图谱预览",
        "",
        "复现脚本：`scripts/build_risk_network.py`",
        "",
        "## 复现产物",
        "",
        "- 本地节点表：`data/processed/risk_nodes.csv`",
        "- 本地边表：`data/processed/risk_edges.csv`",
        "- Gephi 文件：`outputs/gephi/china_railway_risk_network.gexf`",
        "",
        "## 网络规模",
        "",
        f"- 节点数：{len(nodes)}",
        f"- 边数：{len(edges)}",
        "",
        "## 节点类型",
        "",
        "| 类型 | 数量 |",
        "|---|---:|",
    ]
    for node_type, count in sorted(node_type_counts.items()):
        lines.append(f"| {node_type} | {count} |")

    lines.extend(["", "## 边类型", "", "| 类型 | 数量 |", "|---|---:|"])
    for edge_type, count in sorted(edge_type_counts.items()):
        lines.append(f"| {edge_type} | {count} |")

    lines.extend(["", "## 加权度最高节点", "", "| 节点 | 类型 | 加权度 |", "|---|---|---:|"])
    for node_id, degree in top_nodes:
        lines.append(f"| {labels[node_id]} | {types[node_id]} | {degree.quantize(Decimal('0.01'))} |")

    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "- 当前图谱优先使用官方披露、司法、执行和企查查扩展样本的合并事件表。",
            "- 其中候选和待复核样本仍需人工复核，节点中心性只能作为课程阶段性风险线索。",
            "- Gephi 导入时建议使用 `weight` 作为边权重，并按 `node_type` 设置颜色。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    events = load_events()
    nodes, edges = build_network(events)
    write_csv_outputs(nodes, edges)
    write_gexf(nodes, edges)
    write_markdown(nodes, edges)
    print(f"wrote {NODES_CSV} ({len(nodes)} nodes)")
    print(f"wrote {EDGES_CSV} ({len(edges)} edges)")
    print(f"wrote {GEXF_OUTPUT}")
    print(f"wrote {DOC_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
