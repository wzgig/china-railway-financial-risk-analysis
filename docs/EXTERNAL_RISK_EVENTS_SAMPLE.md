# 司法/执行/企查查扩展风险事件样本

复现脚本：`scripts/build_external_risk_events.py`

## 样本口径

- 扩展样本只使用公开法院 PDF、公开裁判文书转载、新闻报道转引的执行信息和公开报道转引的企查查汇总指标。
- 对裁判文书网、执行信息公开网和企查查，不绕过登录、验证码、付费墙或批量访问限制。
- `core` 可作为较强样本；`candidate` 和 `verify` 仅用于探索性样本与图谱结构验证，正式结论前必须人工复核。
- 企查查汇总型记录可能与逐条执行案件重复，进入机器学习特征前需要按主体、日期、案号和金额去重。

## 样本规模

- 外部扩展事件：11 条
- 合并后事件：28 条

### 来源类型

| 来源类型 | 数量 |
|---|---:|
| execution | 5 |
| qcc | 3 |
| wenshu | 3 |

### 证据状态

| 状态 | 数量 |
|---|---:|
| candidate | 5 |
| core | 2 |
| verify | 4 |

### 年份分布

| 年份 | 数量 |
|---|---:|
| 2023 | 6 |
| 2024 | 1 |
| 2025 | 1 |
| 2026 | 3 |

### 风险类型

| 风险类型 | 数量 |
|---|---:|
| compliance | 4 |
| liquidity | 6 |
| project | 1 |

## 样本摘要

| 事件ID | 来源 | 年份 | 主体 | 事件类型 | 风险类型 | 金额(亿元) | 证据状态 | 摘要 |
|---|---|---:|---|---|---|---:|---|---|
| EX2023-WENSHU-SH-230 | wenshu | 2023 | 中铁上海工程局集团有限公司 | civil_litigation | compliance | 0.0094 | core | 上海铁路运输法院判决中铁上海工程局集团有限公司支付货款、运费等约93.80万元，反映供应链结算争议。 |
| EX2023-WENSHU-SH-496 | wenshu | 2023 | 中铁上海工程局集团有限公司 | civil_litigation | compliance | 0.0069 | core | 上海铁路运输法院判决中铁上海工程局集团有限公司承担约69.22万元货款及相关费用，补充供应链付款类司法样本。 |
| EX2024-WENSHU-LN-1533 | wenshu | 2024 | 中铁九局集团有限公司 | civil_litigation | project | 0.0243 | candidate | 二审维持一审关于支付工程款约242.68万元及利息的结果，体现项目结算和分包争议风险。 |
| EX2023-EXEC-GZ-417 | execution | 2023 | 中铁广州工程局集团第三工程有限公司 | dishonest_judgment_debtor | compliance | 0.0953 | candidate | 公开报道援引执行信息显示，该公司因工程款、案件受理费、保全费、担保费等约952.99万元被列入失信被执行人样本。 |
| EX2023-EXEC-TUNNEL-3-LIMIT | execution | 2023 | 中铁隧道集团三处有限公司 | restricted_consumption | liquidity | 0.0051 | candidate | 报道披露该公司在国内非涉外仲裁裁决执行中被出具限制消费令，报道列明两笔租赁欠款合计约51.20万元。 |
| EX2023-EXEC-10J-2-LIMIT | execution | 2023 | 中铁十局集团第二工程有限公司 | restricted_consumption | liquidity |  | verify | 报道披露供应商申请执行买卖合同纠纷后，法院对中铁十局二公司及法定代表人出具限制消费令，体现材料款拖欠和执行压力。 |
| EX2023-EXEC-6J-ROADBRIDGE | execution | 2023 | 中铁六局集团路桥建设有限公司 | execution_case | liquidity | 0.0646 | candidate | 公开报道援引执行信息显示，该公司2023年1月新增3条被执行人信息，执行标的合计646.31万元。 |
| EX2025-EXEC-3J-BRIDGE | execution | 2025 | 中铁三局集团桥隧工程有限公司 | execution_case | liquidity | 0.1360 | candidate | 公开报道援引天眼查显示，该公司新增两条被执行人信息，执行金额分别约42.67万元和1319万元，合计约1360万元。 |
| EX2026-QCC-TUNNEL-PENALTY | qcc | 2026 | 中铁隧道局集团有限公司 | administrative_penalty | compliance | 0.0460 | verify | 财中社报道援引企查查数据称，中铁隧道局拥有26条行政处罚记录，罚款总额超过460万元。 |
| EX2026-QCC-TUNNEL-EXEC | qcc | 2026 | 中铁隧道局集团有限公司 | execution_case | liquidity | 1.3000 | verify | 财中社报道援引企查查数据称，截至2026年2月14日，中铁隧道局存在29条被执行人信息，被执行总金额约1.3亿元。 |
| EX2026-QCC-TUNNEL-23EXEC | qcc | 2026 | 中铁隧道局集团有限公司 | execution_case | liquidity | 0.9458 | verify | 报道称2026年1月13日至2月10日不到40天内，中铁隧道局累计新增23起执行案件，总执行标的约9458万元。 |

## 进入图谱和模型的处理方式

- 图谱脚本优先读取 `data/processed/risk_events_combined.csv`，若该文件不存在则回退到官方披露种子事件。
- 机器学习特征表应按年度聚合事件数量、执行金额、司法金额、企查查汇总金额和高严重度事件数。
- 2026 年事件可作为最新监测样本，不应直接用于 2021-2025 年年度模型训练标签。
- `verify` 样本进入最终报告前，要替换为逐条人工导出或官方平台复核记录。
