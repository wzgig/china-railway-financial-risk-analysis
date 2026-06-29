# 数据字典

## `risk_events.csv`

| 字段 | 类型 | 说明 |
|---|---|---|
| event_id | string | 风险事件唯一编号 |
| source_type | string | 数据来源，如 annual_report、wenshu、execution、qcc |
| source_name | string | 平台、文书、公告或报告名称 |
| source_url | string | 原始链接或本地文件路径 |
| access_date | date | 访问或下载日期 |
| search_keyword | string | 检索关键词 |
| company_name | string | 涉及主体标准名称 |
| company_role | string | 原告、被告、被执行人、担保方、发行人等 |
| related_party | string | 对手方或相关主体 |
| subsidiary_flag | boolean | 是否子公司 |
| event_date | date | 事件日期 |
| year | int | 年份 |
| province | string | 省份 |
| city | string | 城市 |
| event_type | string | 诉讼、执行、处罚、担保、评级关注等 |
| risk_type | string | 流动性、偿债、营运、合规、项目、市场等 |
| cause | string | 案由或事件原因 |
| amount_rmb | float | 涉及金额，人民币元 |
| summary | string | 事件摘要 |
| severity_score | float | 影响程度得分 |
| probability_score | float | 发生概率得分 |
| evidence_status | string | core、candidate、verify、exclude |
| notes | string | 复核、去重或证据边界说明 |

## `risk_nodes.csv`

| 字段 | 类型 | 说明 |
|---|---|---|
| node_id | string | 节点唯一编号 |
| label | string | 节点显示名称 |
| node_type | string | company、risk_event、risk_type、region、counterparty、time |
| year | int | 年份，可为空 |
| weight | float | 节点权重 |
| group | string | 社群或分组 |

## `risk_edges.csv`

| 字段 | 类型 | 说明 |
|---|---|---|
| source | string | 起点 node_id |
| target | string | 终点 node_id |
| edge_type | string | involved_in、classified_as、located_in、co_occurs、controls |
| weight | float | 边权重 |
| year | int | 年份 |
| evidence | string | 支撑来源 |

## `risk_network_centrality.csv`

| 字段 | 类型 | 说明 |
|---|---|---|
| node_id | string | 节点唯一编号 |
| label | string | 节点显示名称 |
| node_type | string | 节点类型 |
| community | int | Louvain 社群编号 |
| weighted_degree | float | 加权度，反映连接强度 |
| in_strength | float | 入边加权强度 |
| out_strength | float | 出边加权强度 |
| degree_centrality | float | 度中心性 |
| betweenness_centrality | float | 中介中心性 |
| closeness_centrality | float | 接近中心性 |
| pagerank | float | PageRank 中心性 |

## `model_features.csv`

| 字段 | 类型 | 说明 |
|---|---|---|
| company_code | string | 股票代码或公司编号 |
| company_name | string | 公司名称 |
| year | int | 年份 |
| debt_asset_ratio | float | 资产负债率 |
| current_ratio | float | 流动比率 |
| cash_to_short_debt | float | 现金短债比 |
| operating_cash_flow | float | 经营现金流净额 |
| roe | float | 净资产收益率 |
| gross_margin | float | 毛利率 |
| ar_turnover | float | 应收账款周转率 |
| litigation_count | int | 诉讼事件数 |
| execution_amount | float | 执行金额 |
| text_risk_score | float | 文本风险综合得分 |
| network_centrality | float | 风险网络中心性 |
| label | int | 风险标签，0/1 或等级编码 |

## `peer_financial_panel.csv`

| 字段 | 类型 | 说明 |
|---|---|---|
| company_code | string | 股票代码 |
| company_name | string | 公司全称 |
| short_name | string | 公司简称 |
| year | int | 年报年份 |
| revenue_growth_pct | float | 营业收入同比增速 |
| parent_net_profit_growth_pct | float | 归母净利润同比增速 |
| operating_cash_flow_to_revenue_pct | float | 经营现金流净额/营业收入 |
| asset_liability_ratio_pct | float | 资产负债率 |
| current_ratio | float | 流动比率 |
| quick_ratio | float | 速动比率 |
| cash_ratio | float | 现金比率 |
| gross_margin_pct | float | 毛利率 |
| net_profit_margin_pct | float | 销售净利率 |
| roe_weighted_pct | float | 加权净资产收益率 |
| interest_coverage_proxy | float | 东方财富口径利息保障倍数代理变量 |

## `warning_model_dataset.csv`

| 字段 | 类型 | 说明 |
|---|---|---|
| feature_year | int | 特征年份 |
| label_year | int | 标签年份，即下一年 |
| financial_pressure_label_next_year | int | 下一年度财务压力规则标签 |
| label_rule_score | int | 触发压力规则数量 |
| label_reason | string | 标签触发原因 |
