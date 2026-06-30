# 官方披露风险事件种子样本

复现脚本：`scripts/build_official_risk_events.py`

## 样本口径

- 本表仅来自中国中铁年报、财务指标整理结果和联合资信跟踪评级报告。
- 该样本用于搭建风险图谱结构，不替代裁判文书、执行信息或企业风险平台的逐条事件核验。
- 金额均按人民币元进入本地 CSV；下表为便于阅读换算为亿元。

## 样本摘要

| 事件ID | 年份 | 事件类型 | 风险类型 | 金额(亿元) | 摘要 |
|---|---:|---|---|---:|---|
| OF2021-GUARANTEE | 2021 | guarantee | organizational_propagation | 1533.90 | 年报披露对外实际担保、房地产按揭担保和差额补足承诺，最大风险敞口约1533.90亿元。 |
| OF2021-LITIGATION | 2021 | litigation_contingency | compliance | 52.56 | 年报或有事项披露，已发生但尚不符合负债确认条件的未决诉讼年末诉讼标的金额约52.56亿元。 |
| OF2022-GUARANTEE | 2022 | guarantee | organizational_propagation | 1545.18 | 年报披露对外实际担保、房地产按揭担保和差额补足承诺，最大风险敞口约1545.18亿元。 |
| OF2022-LITIGATION | 2022 | litigation_contingency | compliance | 51.16 | 年报或有事项披露，已发生但尚不符合负债确认条件的未决诉讼年末诉讼标的金额约51.16亿元。 |
| OF2023-GUARANTEE | 2023 | guarantee | organizational_propagation | 1333.75 | 年报披露对外实际担保、房地产按揭担保和差额补足承诺，最大风险敞口约1333.75亿元。 |
| OF2023-LITIGATION | 2023 | litigation_contingency | compliance | 43.27 | 年报或有事项披露，已发生但尚不符合负债确认条件的未决诉讼年末诉讼标的金额约43.27亿元。 |
| OF2024-CONTRACT-ASSET | 2024 | asset_quality_signal | operation | 3331.20 | 年报资产分析显示，合同资产约3331.2亿元，占总资产14.76%，回款和资产质量需要跟踪。 |
| OF2024-GUARANTEE | 2024 | guarantee | organizational_propagation | 836.12 | 年报披露对外实际担保、房地产按揭担保和差额补足承诺，最大风险敞口约836.12亿元。 |
| OF2024-LITIGATION | 2024 | litigation_contingency | compliance | 25.76 | 年报或有事项披露，已发生但尚不符合负债确认条件的未决诉讼年末诉讼标的金额约25.76亿元。 |
| OF2024-PROFIT | 2024 | financial_pressure | profitability | 278.87 | 年报主要指标显示，营业收入同比-8.2%、归母净利润同比-16.71%，盈利下行进入风险样本。 |
| OF2024-SOLVENCY | 2024 | financial_pressure | solvency |  | 年报债券章节显示，资产负债率为77.39%，利息保障倍数为3.17，作为偿债压力预警信号。 |
| OF2025-CONTRACT-ASSET | 2025 | asset_quality_signal | operation | 3668.45 | 年报资产分析显示，合同资产约3668.45亿元，占总资产14.85%，回款和资产质量需要跟踪。 |
| OF2025-GUARANTEE | 2025 | guarantee | organizational_propagation | 426.92 | 年报披露对外实际担保、房地产按揭担保和差额补足承诺，最大风险敞口约426.92亿元。 |
| OF2025-LITIGATION | 2025 | litigation_contingency | compliance | 17.53 | 年报或有事项披露，已发生但尚不符合负债确认条件的未决诉讼年末诉讼标的金额约17.53亿元。 |
| OF2025-PROFIT | 2025 | financial_pressure | profitability | 228.92 | 年报主要指标显示，营业收入同比-5.77%、归母净利润同比-17.91%，盈利下行进入风险样本。 |
| OF2025-RATING | 2025 | rating_action | solvency |  | 联合资信维持主体及相关债项AAA/稳定，同时提示PPP项目运营及回款、应收账款、合同资产、存货和长期应收款资金占用、短期偿债指标弱化等关注点。 |
| OF2025-SOLVENCY | 2025 | financial_pressure | solvency |  | 年报债券章节显示，资产负债率为78.12%，利息保障倍数为2.98，作为偿债压力预警信号。 |

## 后续用法

- 本地完整事件表：`data/interim/risk_events_official_seed.csv`，不纳入公开仓库。
- 后续可将人工核验的司法、执行、公告和企业风险事件追加到同一字段结构。
- 图谱脚本会把 `company_name`、`event_id`、`risk_type`、`year`、`related_party` 转换为节点，并按影响程度与概率评分生成边权重。
