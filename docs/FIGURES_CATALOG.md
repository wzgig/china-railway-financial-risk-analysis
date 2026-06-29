# 图表目录

生成脚本：`scripts/build_report_figures.py`

## 可用于报告的图表

| 图表 | 文件 | 报告用途 |
|---|---|---|
| 财务风险趋势 | `docs/assets/figures/financial_trends.png` | 支撑财务指标趋势、盈利下行、资产负债率和利息保障倍数分析 |
| 文本风险热力图 | `docs/assets/figures/text_risk_heatmap.png` | 支撑文本风险指标和风险类别排序 |
| 2025 高权重风险词 | `docs/assets/figures/top_2025_risk_terms.png` | 支撑文本风险词典和年报风险语境解释 |
| 官方事件风险矩阵 | `docs/assets/figures/risk_event_matrix.png` | 支撑风险发生概率与影响程度二维评估 |

## 预览

![财务风险趋势](assets/figures/financial_trends.png)

![文本风险热力图](assets/figures/text_risk_heatmap.png)

![2025 高权重风险词](assets/figures/top_2025_risk_terms.png)

![官方事件风险矩阵](assets/figures/risk_event_matrix.png)

## 解释边界

- 图表基于公开年报、评级报告和本地脚本整理结果生成。
- 当前风险矩阵使用官方披露种子事件，后续加入司法、执行和企业风险样本后应重新生成。
- `outputs/figures/` 保存本地作图副本；`docs/assets/figures/` 用于 GitHub Pages 展示。
