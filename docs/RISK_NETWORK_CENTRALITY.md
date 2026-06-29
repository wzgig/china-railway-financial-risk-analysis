# Gephi 最终导图与中心性解释

生成脚本：`scripts/analyze_risk_network.py`

## 输出文件

- 增强版 Gephi 文件：`outputs/gephi/china_railway_risk_network_enhanced.gexf`
- 节点中心性表：`data/processed/risk_network_centrality.csv`
- 社群摘要表：`data/processed/risk_network_communities.csv`
- Top 中心性表：`outputs/tables/risk_network_top_centrality.csv`
- 报告导图：`docs/assets/figures/risk_network_gephi_style.png`

## 网络规模

- 节点数：77
- 边数：133

### 节点类型

| 节点类型 | 数量 |
|---|---:|
| company | 9 |
| event | 28 |
| related_party | 13 |
| risk_type | 7 |
| source | 14 |
| year | 6 |

### 边类型

| 边类型 | 数量 |
|---|---:|
| classified_as | 28 |
| evidenced_by | 28 |
| involves | 28 |
| occurred_in | 28 |
| related_to | 21 |

## 导图预览

![风险图谱中心性导图](assets/figures/risk_network_gephi_style.png)

## 加权度最高节点

| label | node_type | community | weighted_degree | pagerank |
|---|---|---|---|---|
| 中国中铁股份有限公司 | company | 4 | 60.0000 | 0.008699 |
| compliance | risk_type | 2 | 29.0000 | 0.051004 |
| liquidity | risk_type | 1 | 24.0000 | 0.051289 |
| OF2024-CONTRACT-ASSET asset_quality_signal | event | 4 | 11.0000 | 0.009316 |
| solvency | risk_type | 5 | 11.0000 | 0.023679 |
| OF2025-CONTRACT-ASSET asset_quality_signal | event | 4 | 11.0000 | 0.009316 |
| EX2026-QCC-TUNNEL-23EXEC execution_case | event | 1 | 11.0000 | 0.011657 |
| EX2026-QCC-TUNNEL-EXEC execution_case | event | 1 | 11.0000 | 0.011657 |
| OF2021-GUARANTEE guarantee | event | 4 | 10.0000 | 0.009316 |
| organizational_propagation | risk_type | 4 | 10.0000 | 0.024409 |

## 中介中心性最高节点

| label | node_type | community | betweenness_centrality | weighted_degree |
|---|---|---|---|---|
| 中国中铁股份有限公司 | company | 4 | 0.317592 | 60.0000 |
| compliance | risk_type | 2 | 0.285370 | 29.0000 |
| 2023 | year | 1 | 0.270188 | 8.0000 |
| liquidity | risk_type | 1 | 0.133582 | 24.0000 |
| 2024 | year | 3 | 0.132014 | 6.0000 |
| EX2025-EXEC-3J-BRIDGE execution_case | event | 1 | 0.120939 | 10.0000 |
| EX2026-QCC-TUNNEL-PENALTY administrative_penalty | event | 2 | 0.116149 | 9.0000 |
| OF2024-LITIGATION litigation_contingency | event | 2 | 0.106938 | 8.0000 |
| 2025 | year | 5 | 0.106280 | 7.0000 |
| EX2024-WENSHU-LN-1533 civil_litigation | event | 3 | 0.103158 | 8.0000 |

## PageRank 最高节点

| label | node_type | community | pagerank | weighted_degree |
|---|---|---|---|---|
| liquidity | risk_type | 1 | 0.051289 | 24.0000 |
| compliance | risk_type | 2 | 0.051004 | 29.0000 |
| organizational_propagation | risk_type | 4 | 0.024409 | 10.0000 |
| solvency | risk_type | 5 | 0.023679 | 11.0000 |
| 2023 | year | 1 | 0.022879 | 8.0000 |
| operation | risk_type | 4 | 0.019256 | 8.0000 |
| profitability | risk_type | 4 | 0.019117 | 8.0000 |
| 2025 | year | 5 | 0.018907 | 7.0000 |
| 2024 | year | 3 | 0.017733 | 6.0000 |
| 集团内子公司、房地产项目购房业主等 | related_party | 4 | 0.016554 | 5.0000 |

## 中心性解释

- 加权度刻画节点与风险事件、风险类型、年份、来源之间的总体连接强度。中国中铁股份有限公司加权度最高，说明当前样本仍以母公司官方披露和合并事件为主。
- 合规风险和流动性风险在风险类型节点中更靠前，说明诉讼、执行、限制消费和供应链付款类事件已经成为图谱中的主要外部风险线索。
- 中介中心性较高的节点连接多个事件、年份和风险类型，适合解释风险传导中的桥接作用；若子公司或相关方节点中介中心性上升，应作为后续复核重点。
- PageRank 更偏向识别被高权重事件指向的稳定核心节点，适合与加权度共同判断关键风险类别。

## Gephi 布局建议

1. 在 Gephi 中打开 `outputs/gephi/china_railway_risk_network_enhanced.gexf`。
2. `Appearance -> Nodes -> Partition` 按 `node_type` 着色。
3. `Appearance -> Nodes -> Ranking` 按 `weighted_degree` 或 `pagerank` 调整节点大小。
4. 布局可先用 `ForceAtlas2`，勾选 `LinLog mode` 与 `Prevent overlap`；稳定后再用 `Label Adjust`。
5. 统计面板中重点查看 `weighted_degree`、`betweenness_centrality`、`pagerank` 与 `community` 字段。

## 解释边界

- 图谱使用官方披露、司法、执行和企查查扩展样本的合并事件表。
- 当前执行和企查查部分样本仍有 `candidate` 或 `verify` 状态，中心性结果用于课程报告的风险线索解释，不应作为法律事实或投资结论。
- 后续若补充更多逐条核验事件，应重新运行 `build_risk_network.py` 和本脚本。
