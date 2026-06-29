# 来源与资料记录

访问日期：2026-06-29

## 本地资料

| 编号 | 来源 | 类型 | 用途 | 状态 |
|---|---|---|---|---|
| L1 | 本地课程要求截图 | 课程要求截图 | 提取项目六项要求 | 已使用，原始截图不纳入公开仓库 |
| L2 | 本地课程要求 Markdown | Markdown | 原始要求文件，但编码乱码 | 保留本地原件，不纳入公开仓库 |
| L3 | 本地 `course-paper-workflow` skill | 本地工作流 | 课程论文项目规划、来源记录、质量门槛 | 已使用 |

## 已查验公开来源

| 编号 | 来源 | 链接 | 用途 | 备注 |
|---|---|---|---|---|
| W1 | 中国中铁官网 | https://www.crec.cn/ | 公司公告、投资者关系、年报与公告入口 | 官方来源 |
| W2 | 上海证券交易所公司公告，中国中铁 601390 | https://www.sse.com.cn/assortment/stock/list/info/announcement/index.shtml?productId=601390 | 年报、季报、公告、风险持续评估报告 | 官方披露渠道 |
| W3 | 上交所公告摘要，中国中铁 601390 | https://www.sse.com.cn/assortment/stock/list/info/summary/index.shtml?COMPANY_CODE=601390 | 快速确认公告日期和标题 | 官方披露渠道 |
| W4 | 巨潮资讯，中国中铁 2025 年年度报告摘要 | https://www.cninfo.com.cn/ | 年度报告摘要，辅助财务数据确认 | 具体 PDF 链接见本地下载清单，需下载全文或从上交所读取全文 |
| W5 | 巨潮资讯，中国中铁 2026 年第一季度报告 | https://dataclouds.cninfo.com.cn/shgonggao/hsomarket/2026/20260429/39a45b3f8b7e45438af2722d179f54a3.PDF | 最新季度观察 | 不纳入年度模型主样本 |
| W6 | 中国裁判文书网 | https://wenshu.court.gov.cn/ | 裁判文书检索 | 需要遵守注册、登录、检索限制 |
| W7 | 人民法院在线服务/司法公开入口 | https://cjdh.court.gov.cn/ | 执行信息与司法公开相关入口 | 需人工确认具体查询模块 |
| W8 | 企查查 | https://www.qcc.com/ | 企业工商与风险信息查询 | 商业平台，需遵守平台规则 |

## 计划补充来源

| 类型 | 目标来源 | 计划用途 |
|---|---|---|
| 年报全文 | 中国中铁官网、上交所、巨潮资讯 | 财务指标、风险披露文本、诉讼担保信息 |
| 信用评级 | 上交所债券公告、评级机构官网 | 债务风险、评级关注因素 |
| 同业数据 | 上交所、深交所、巨潮资讯 | 机器学习训练样本 |
| 司法数据 | 中国裁判文书网、人民法院公开入口 | 诉讼、执行、案由、金额、地区 |
| 企业风险 | 企查查或同类平台合法导出 | 行政处罚、经营异常、股权冻结、司法协助 |
| 学术文献 | CNKI、万方、Google Scholar、学校数据库 | 财务风险预警、文本风险指标、复杂网络风险传导方法 |

## 本轮新增核心文献与标准

| 编号 | 来源 | 链接 | 用途 | 状态 |
|---|---|---|---|---|
| R1 | 中国中铁股份有限公司 2025 年年度报告摘要 | https://www.cninfo.com.cn/ | 最新年度经营、财务和债券信息 | core；具体 PDF 链接见本地下载清单 |
| R2 | 中国中铁股份有限公司 2024 年年度报告 | https://www.crec.cn/web/fileDir/resource/cms/article/10090220/10287887/2025-019%20%E4%B8%AD%E5%9B%BD%E4%B8%AD%E9%93%812024%E5%B9%B4%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A.pdf | 财务附注、合同资产、信用风险和流动性风险 | core |
| R3 | 联合资信 2025 年跟踪评级报告 | https://www.lhratings.com/reports/B0411-P76587-2024-GZ2025.pdf | 信用评级、外部风险评价 | core |
| R4 | GB/T 7714-2025 官方标准信息 | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | 参考文献格式依据 | core |
| R5 | Crossref DOI 元数据 | https://api.crossref.org/ | 校验英文期刊、会议论文 DOI 与元数据 | core |

## 本轮生成的引用文件

| 文件 | 用途 |
|---|---|
| `paper/references.ris` | EndNote 可直接导入的 RIS 文件 |
| `paper/references.enw` | EndNote tagged import 备选文件 |
| `paper/references.bib` | BibTeX/LaTeX/Typst 可用参考文献库 |
| `paper/references_gbt7714.md` | GB/T 7714 顺序编码制参考文献清单 |

## 本轮生成的数据与脚本

| 文件 | 类型 | 用途 | 状态 |
|---|---|---|---|
| `scripts/extract_financial_indicators.py` | Python 脚本 | 从官方年报整理 2021-2025 财务风险指标，生成 CSV 和公开摘要 | 已运行 |
| `data/processed/financial_risk_indicators.csv` | 结构化数据 | 建模和图表使用的财务风险指标表 | 本地生成，不纳入公开仓库 |
| `docs/FINANCIAL_RISK_INDICATORS.md` | 公开摘要 | 展示财务风险指标、初步观察和来源校验 | 已生成 |
| `configs/risk_seed_terms.json` | 配置文件 | 文本风险指标的种子词集 | 已创建 |
| `scripts/extract_risk_text_corpus.py` | Python 脚本 | 从年报文本缓存抽取风险种子词命中片段 | 已运行 |
| `data/interim/risk_text_corpus_seed_matches.csv` | 中间数据 | 年报风险语料初筛明细 | 本地生成，不纳入公开仓库 |
| `docs/RISK_TEXT_CORPUS_SUMMARY.md` | 公开摘要 | 展示年度风险类别命中次数和高频种子词 | 已生成 |
| `configs/stopwords_zh.txt` | 配置文件 | jieba 分词和关键词抽取的中文停用词 | 已创建 |
| `scripts/build_text_risk_index.py` | Python 脚本 | 计算 2021-2025 年年报文本风险类别得分和高权重词 | 已运行 |
| `data/processed/text_risk_index_by_year.csv` | 结构化数据 | 年度风险类别综合得分和概率代理得分 | 本地生成，不纳入公开仓库 |
| `data/processed/text_risk_terms_by_year.csv` | 结构化数据 | 年度高权重风险词、权重和命中次数 | 本地生成，不纳入公开仓库 |
| `docs/TEXT_RISK_INDEX.md` | 公开摘要 | 展示文本风险指标计算方法、年度结果和解释边界 | 已生成 |
| `configs/risk_event_schema.json` | 配置文件 | 风险事件字段、事件类型、风险类型和合规边界 | 已创建 |
| `scripts/create_risk_event_template.py` | Python 脚本 | 生成司法、执行、企查查和公告风险事件采集模板 | 已运行 |
| `data/interim/risk_event_collection_template.csv` | 中间模板 | 风险事件人工或合法导出数据的标准录入表 | 本地生成，不纳入公开仓库 |
| `docs/RISK_EVENT_COLLECTION_TEMPLATE.md` | 公开说明 | 展示字段说明、检索主体、检索词和 Gephi 衔接方式 | 已生成 |
| `scripts/build_official_risk_events.py` | Python 脚本 | 从官方年报、财务指标和评级报告生成风险事件种子表 | 已运行 |
| `data/interim/risk_events_official_seed.csv` | 中间数据 | 官方披露风险事件种子样本 | 本地生成，不纳入公开仓库 |
| `docs/OFFICIAL_RISK_EVENTS_SAMPLE.md` | 公开摘要 | 展示官方披露风险事件样本、金额和解释边界 | 已生成 |
| `scripts/build_risk_network.py` | Python 脚本 | 将风险事件表转为节点表、边表和 Gephi GEXF | 已运行 |
| `data/processed/risk_nodes.csv` | 结构化数据 | Gephi 节点表 | 本地生成，不纳入公开仓库 |
| `data/processed/risk_edges.csv` | 结构化数据 | Gephi 边表 | 本地生成，不纳入公开仓库 |
| `outputs/gephi/china_railway_risk_network.gexf` | 图谱文件 | Gephi 可导入风险图谱 | 本地生成，不纳入公开仓库 |
| `docs/RISK_NETWORK_PREVIEW.md` | 公开摘要 | 展示官方披露种子网络的节点、边和加权度预览 | 已生成 |
| `scripts/build_report_figures.py` | Python 脚本 | 生成财务趋势、文本风险热力图、风险词和风险矩阵图 | 已运行 |
| `outputs/figures/*.png` | 本地图表 | 报告插图本地副本 | 本地生成，不纳入公开仓库 |
| `docs/assets/figures/*.png` | 公开图表 | GitHub Pages 可展示图表 | 已生成 |
| `docs/FIGURES_CATALOG.md` | 公开摘要 | 展示图表用途、预览和解释边界 | 已生成 |

## 来源使用原则

1. 优先使用官方披露和可复核文件。
2. 搜索结果摘要只能用于发现线索，不能直接作为论文证据。
3. 商业平台数据必须记录访问日期、检索词、导出方式和字段说明。
4. 对于登录、验证码、付费或权限限制内容，不绕过限制。
5. 每个图表和模型结论都要能追溯到本文件中的来源或本地原始数据。
