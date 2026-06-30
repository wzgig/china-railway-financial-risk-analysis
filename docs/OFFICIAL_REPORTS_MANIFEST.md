# 官方报告下载清单

生成日期：2026-06-29

下载脚本：`scripts/collect_official_reports.py`

本清单只记录公开来源和本地文件名；PDF 原始文件保存在 `data/raw/annual_reports/`，不纳入公开仓库。

| 期间 | 类型 | 标题 | 日期 | 来源 | 本地文件名 | URL |
|---|---|---|---|---|---|---|
| 2026Q1 | 季度报告 | 中国中铁2026年第一季度报告 | 2026-04-30 | 中国中铁股份有限公司官网 | `2026_q1_report.pdf` | https://www.crec.cn/web/attachDir/2026/05/2026050909092597013.pdf |
| 2025 | 年度报告 | 中国中铁2025年年度报告 | 2026-03-31 | 中国中铁股份有限公司官网 | `2025_annual_report.pdf` | https://www.crec.cn/web/attachDir/2026/03/2026033108390191131.pdf |
| 2025 | 跟踪评级 | 中国中铁股份有限公司2025年跟踪评级报告 | 2025-05-07 | 联合资信评估股份有限公司 | `2025_lianhe_rating_report.pdf` | https://www.lhratings.com/reports/B0411-P76587-2024-GZ2025.pdf |
| 2024 | 年度报告 | 中国中铁2024年年度报告 | 2025-03-29 | 中国中铁股份有限公司官网 | `2024_annual_report.pdf` | https://www.crec.cn/web/fileDir/resource/cms/article/10090220/10287887/2025-019%20%E4%B8%AD%E5%9B%BD%E4%B8%AD%E9%93%812024%E5%B9%B4%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A.pdf |
| 2023 | 年度报告 | 中国中铁2023年年度报告 | 2024-03-29 | 中国中铁股份有限公司官网 | `2023_annual_report.pdf` | https://www.crec.cn/web/fileDir/resource/cms/article/10090220/10269301/2024-10%20%E4%B8%AD%E5%9B%BD%E4%B8%AD%E9%93%812023%E5%B9%B4%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A.pdf |
| 2022 | 年度报告 | 中国中铁2022年年度报告 | 2023-03-31 | 中国中铁股份有限公司官网 | `2022_annual_report.pdf` | https://www.crec.cn/web/fileDir/resource/cms/article/10090220/10247328/%E4%B8%AD%E5%9B%BD%E4%B8%AD%E9%93%812022%E5%B9%B4%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A.pdf |
| 2021 | 年度报告 | 中国中铁2021年年度报告 | 2022-03-31 | 中国中铁股份有限公司官网 | `2021_annual_report.pdf` | https://www.crec.cn/web/fileDir/resource/cms/article/10090220/10193023/%E4%B8%AD%E5%9B%BD%E4%B8%AD%E9%93%812021%E5%B9%B4%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A%EF%BC%88A%E8%82%A1%E4%B8%AD%E6%96%87%E7%AE%80%E4%BD%93%EF%BC%89.pdf |

## 校验记录

- 已下载文件数量：7。
- `python -m py_compile .\scripts\collect_official_reports.py` 通过。
- 原始 PDF 文件不提交到公开仓库，后续抽取结果和图表再按需要选择是否公开。
