# 中国中铁财务风险指标数据集

复现脚本：`scripts/extract_financial_indicators.py`

单位说明：金额单位为亿元人民币；比例单位为 `%`；利息保障倍数为倍。

## 指标表

| 年份 | 营业收入 | 收入增速 | 归母净利润 | 归母净利增速 | 经营现金流 | 资产负债率 | 应收账款/总资产 | 合同资产/总资产 | 利息保障倍数 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2021 | 10704.17 |  | 276.18 |  | 130.69 | 73.68 | 8.97 | 10.95 | 4.09 |
| 2022 | 11515.01 | 7.57 | 312.73 | 13.24 | 435.52 | 73.77 | 7.58 | 10.52 | 3.82 |
| 2023 | 12608.41 | 9.5 | 334.83 | 7.07 | 383.63 | 74.86 | 8.57 | 12.8 | 3.73 |
| 2024 | 11574.39 | -8.2 | 278.87 | -16.71 | 280.51 | 77.39 | 10.91 | 14.76 | 3.17 |
| 2025 | 10906.26 | -5.77 | 228.92 | -17.91 | 287.72 | 78.12 | 11.69 | 14.85 | 2.98 |

## 初步风险观察

1. 2023 年后营业收入连续下降，2025 年收入较 2024 年下降，规模扩张动能转弱。
2. 归母净利润从 2023 年的 334.83 亿元下降到 2025 年的 228.92 亿元，盈利压力明显。
3. 资产负债率从 2021 年的 73.68% 上升至 2025 年的 78.12%，债务和流动性管理压力上升。
4. 应收账款和合同资产占总资产比例较高，说明回款、结算和资产质量是后续风险评估重点。
5. 利息保障倍数由 2021 年的 4.09 降至 2025 年的 2.98，需结合债券期限、融资成本和现金流继续跟踪。

## 数据口径

- 主要会计数据优先采用最新年报中的追溯调整或重述口径。
- 2021-2022 年部分数据使用后续年报中的比较期重述值，以保持可比性。
- 原始 PDF 保存在 `data/raw/annual_reports/`，结构化 CSV 输出到 `data/processed/financial_risk_indicators.csv`。

## 来源校验

- generated text cache for 2025: data\interim\annual_report_text\2025_annual_report.txt
- generated text cache for 2024: data\interim\annual_report_text\2024_annual_report.txt
- generated text cache for 2023: data\interim\annual_report_text\2023_annual_report.txt
- generated text cache for 2022: data\interim\annual_report_text\2022_annual_report.txt
- generated text cache for 2021: data\interim\annual_report_text\2021_annual_report.txt
- 2025: all source terms found
- 2024: all source terms found
- 2023: all source terms found
- 2022: all source terms found
- 2021: all source terms found
