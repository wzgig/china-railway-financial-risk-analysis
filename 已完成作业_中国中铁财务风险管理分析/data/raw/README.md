# 原始数据目录

此目录只放未经清洗的原始资料。建议按来源分类保存，并在 `SOURCES.md` 中登记来源、访问日期和用途。

## 子目录

- `annual_reports/`：年报、季报、公告、评级报告。
- `legal_cases/`：裁判文书检索导出或手工整理文件。
- `execution/`：执行信息、失信或限制消费记录。
- `qcc/`：企查查或同类平台合法导出的企业风险信息。

## 命名建议

```text
2025_crec_annual_report.pdf
2026q1_crec_quarterly_report.pdf
2021_2025_crec_financial_indicators_manual.xlsx
2026-06-29_wenshu_search_crec_sample.xlsx
2026-06-29_qcc_crec_risk_export.xlsx
```

## 注意

- 不保存账号、密码、Cookie 或绕过限制得到的数据。
- 如果文件包含个人信息，先做脱敏再进入可提交版本。
- 原始文件不要直接改动，清洗结果放入 `data/interim/` 或 `data/processed/`。
