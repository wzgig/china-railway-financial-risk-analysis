# 风险图谱预览

生成脚本：`scripts/build_risk_network.py`

## 输出文件

- 本地节点表：`data/processed/risk_nodes.csv`
- 本地边表：`data/processed/risk_edges.csv`
- Gephi 文件：`outputs/gephi/china_railway_risk_network.gexf`

## 网络规模

- 节点数：36
- 边数：78

## 节点类型

| 类型 | 数量 |
|---|---:|
| company | 1 |
| event | 17 |
| related_party | 2 |
| risk_type | 5 |
| source | 6 |
| year | 5 |

## 边类型

| 类型 | 数量 |
|---|---:|
| classified_as | 17 |
| evidenced_by | 17 |
| involves | 17 |
| occurred_in | 17 |
| related_to | 10 |

## 加权度最高节点

| 节点 | 类型 | 加权度 |
|---|---|---:|
| 中国中铁股份有限公司 | company | 60.00 |
| compliance | risk_type | 15.00 |
| OF2024-CONTRACT-ASSET asset_quality_signal | event | 11.00 |
| solvency | risk_type | 11.00 |
| OF2025-CONTRACT-ASSET asset_quality_signal | event | 11.00 |
| OF2021-GUARANTEE guarantee | event | 10.00 |
| organizational_propagation | risk_type | 10.00 |
| OF2022-GUARANTEE guarantee | event | 10.00 |
| OF2023-GUARANTEE guarantee | event | 10.00 |
| OF2024-PROFIT financial_pressure | event | 10.00 |

## 解释边界

- 当前图谱只使用官方披露种子事件，主要用于验证字段、节点和边权重设计。
- 后续加入裁判文书、执行信息和企业风险样本后，节点中心性和社群划分才适合作为正式结论。
- Gephi 导入时建议使用 `weight` 作为边权重，并按 `node_type` 设置颜色。
