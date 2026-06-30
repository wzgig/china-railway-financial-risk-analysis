# 风险事件采集合规模板

复现脚本：`scripts/create_risk_event_template.py`

版本：`2026-06-29`

## 合规边界

仅使用公开、授权或人工合法导出的数据；不绕过登录、验证码、付费墙、robots 限制或平台访问频率限制。

- 中国裁判文书网、执行信息公开网、企查查等平台如需登录、验证码、授权或付费，不绕过限制。
- 若平台不支持批量导出，采用人工检索、样本化记录或授权导出，再用 Python 清洗。
- 不采集或公开自然人证件编号、联系方式、详细居住地址等个人敏感信息。
- 原始截图、导出表和 PDF 保留本地，公开仓库只保留字段说明、脚本和脱敏摘要。

## 本地模板

`data/interim/risk_event_collection_template.csv` 已生成。该文件是本地中间模板，不纳入公开仓库。

## 字段说明

| 字段 | 必填 | 说明 |
|---|---|---|
| `event_id` | 是 | 事件唯一编号，例如 EV2025-0001 |
| `source_type` | 是 | 来源类型：wenshu/execution/qcc/annual_report/announcement/rating_report/manual_check |
| `source_name` | 是 | 平台名称或文件名称 |
| `source_url` | 否 | 原始链接或本地来源文件路径 |
| `access_date` | 是 | YYYY-MM-DD |
| `search_keyword` | 否 | 检索使用的关键词 |
| `company_name` | 是 | 标准化后的公司或子公司名称 |
| `company_role` | 否 | 主体角色，例如被告、原告、被执行人、担保方、发行人等 |
| `related_party` | 否 | 对手方、债权人、法院、发行人或项目公司 |
| `event_type` | 是 | 事件类型，使用 schema 中的 event_types |
| `risk_type` | 是 | 风险类型，使用 schema 中的 risk_types |
| `event_date` | 否 | 事件日期，精确日期未知时可填年份 |
| `year` | 是 | 事件年份 |
| `province` | 否 | 省份或区域 |
| `city` | 否 | 城市 |
| `case_no` | 否 | 案号或公告编号 |
| `cause` | 否 | 案由或事件原因 |
| `amount_rmb` | 否 | 涉及金额，单位为人民币元 |
| `summary` | 是 | 事实摘要，避免加入无法核验的判断 |
| `severity_score` | 否 | 影响程度评分 1-5，模型完善前可人工赋值 |
| `probability_score` | 否 | 发生概率评分 1-5，模型完善前可人工赋值 |
| `evidence_status` | 是 | 证据状态：core/candidate/verify/exclude |
| `notes` | 否 | 局限、人工复核或去重说明 |

## 推荐检索主体

- 中国中铁股份有限公司
- 中铁一局集团有限公司
- 中铁二局集团有限公司
- 中铁三局集团有限公司
- 中铁四局集团有限公司
- 中铁五局集团有限公司
- 中铁六局集团有限公司
- 中铁七局集团有限公司
- 中铁八局集团有限公司
- 中铁十局集团有限公司
- 中铁建工集团有限公司
- 中铁大桥局集团有限公司
- 中铁隧道局集团有限公司
- 中铁电气化局集团有限公司

## 推荐检索词

- 司法事件：`中国中铁 建设工程施工合同纠纷`、`中国中铁 买卖合同纠纷`、`中铁四局 执行`。
- 执行信息：主体名称 + `被执行人`、`失信被执行人`、`限制消费`、`终本案件`。
- 企业风险：主体名称 + `行政处罚`、`经营异常`、`司法协助`、`股权冻结`、`环保处罚`、`安全生产处罚`。

## 与 Gephi 图谱的衔接

- `company_name` 生成公司节点。
- `related_party` 生成交易对手或法院节点。
- `event_type` 和 `risk_type` 生成风险事件与风险类别节点。
- `province`、`city` 生成地区节点。
- `amount_rmb`、`severity_score`、`probability_score` 可转为边权重。
