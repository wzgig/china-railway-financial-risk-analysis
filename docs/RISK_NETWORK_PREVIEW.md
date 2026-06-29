# 风险图谱预览

生成脚本：`scripts/build_risk_network.py`

## 输出文件

- 本地节点表：`data/processed/risk_nodes.csv`
- 本地边表：`data/processed/risk_edges.csv`
- Gephi 文件：`outputs/gephi/china_railway_risk_network.gexf`

## 网络规模

- 节点数：77
- 边数：133

## 节点类型

| 类型 | 数量 |
|---|---:|
| company | 9 |
| event | 28 |
| related_party | 13 |
| risk_type | 7 |
| source | 14 |
| year | 6 |

## 边类型

| 类型 | 数量 |
|---|---:|
| classified_as | 28 |
| evidenced_by | 28 |
| involves | 28 |
| occurred_in | 28 |
| related_to | 21 |

## 加权度最高节点

| 节点 | 类型 | 加权度 |
|---|---|---:|
| 中国中铁股份有限公司 | company | 60.00 |
| compliance | risk_type | 29.00 |
| liquidity | risk_type | 24.00 |
| OF2024-CONTRACT-ASSET asset_quality_signal | event | 11.00 |
| solvency | risk_type | 11.00 |
| OF2025-CONTRACT-ASSET asset_quality_signal | event | 11.00 |
| EX2026-QCC-TUNNEL-23EXEC execution_case | event | 11.00 |
| EX2026-QCC-TUNNEL-EXEC execution_case | event | 11.00 |
| OF2021-GUARANTEE guarantee | event | 10.00 |
| organizational_propagation | risk_type | 10.00 |

## 解释边界

- 当前图谱优先使用官方披露、司法、执行和企查查扩展样本的合并事件表。
- 其中候选和待复核样本仍需人工复核，节点中心性只能作为课程阶段性风险线索。
- Gephi 导入时建议使用 `weight` 作为边权重，并按 `node_type` 设置颜色。
