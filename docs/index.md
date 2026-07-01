---
layout: default
title: 中国中铁财务风险管理分析
description: 风险图谱、文本指标与机器学习预警的课程项目材料
---

# 中国中铁财务风险管理分析

本项目围绕中国中铁财务风险管理，设计一套从风险识别、风险传导、风险评估到风险预警的完整分析流程。项目使用公开披露文件、司法与企业风险信息、文本分析、Gephi 风险图谱和机器学习模型，服务于课程报告与 3 分钟展示视频。

## 项目目标

- 分析中国中铁经营特征及财务风险生成机制。
- 整理裁判文书、执行信息、企业风险与公告数据。
- 构建风险图谱，识别风险传导路径和关键节点。
- 用种子词、Word2Vec 和 jieba 构建描述性风险指标。
- 训练财务风险预警模型，输出风险等级和驱动因素。
- 制作约 3 分钟视频展示“风险传导 -> 风险评估 -> 风险预警”。

## 方法路线

```text
公开数据采集
  -> 主体与事件清洗
  -> 风险图谱构建
  -> 文本风险指标
  -> 财务风险预警模型
  -> 弹性风险管理评分
  -> 报告与视频展示
```

## 核心文档

- [草稿版报告](https://github.com/wzgig/china-railway-financial-risk-analysis/blob/main/paper/draft.md)
- [Word 草稿](https://github.com/wzgig/china-railway-financial-risk-analysis/blob/main/paper/course_paper_draft.docx)
- [PDF 预览稿](https://github.com/wzgig/china-railway-financial-risk-analysis/blob/main/paper/course_paper_draft.pdf)
- [GB/T 7714 参考文献清单](https://github.com/wzgig/china-railway-financial-risk-analysis/blob/main/paper/references_gbt7714.md)
- [官方报告下载清单](OFFICIAL_REPORTS_MANIFEST.md)
- [初始财务指标表](FINANCIAL_INDICATORS_INITIAL.md)
- [财务风险指标数据集](FINANCIAL_RISK_INDICATORS.md)
- [年报文本风险语料初筛](RISK_TEXT_CORPUS_SUMMARY.md)
- [文本风险指标计算结果](TEXT_RISK_INDEX.md)
- [Word2Vec 风险词扩充结果](WORD2VEC_RISK_TERMS.md)
- [风险事件采集模板](RISK_EVENT_COLLECTION_TEMPLATE.md)
- [官方披露风险事件种子样本](OFFICIAL_RISK_EVENTS_SAMPLE.md)
- [司法/执行/企查查扩展样本](EXTERNAL_RISK_EVENTS_SAMPLE.md)
- [风险图谱预览](RISK_NETWORK_PREVIEW.md)
- [Gephi 最终导图与中心性解释](RISK_NETWORK_CENTRALITY.md)
- [机器学习预警特征表](MODEL_FEATURE_TABLE.md)
- [同业财务面板](PEER_FINANCIAL_PANEL.md)
- [财务风险预警基线模型](FINANCIAL_WARNING_MODEL.md)
- [弹性风险管理模型](RESILIENCE_RISK_MANAGEMENT_MODEL.md)
- [图表目录](FIGURES_CATALOG.md)
- [格式模板提取记录](FORMAT_TEMPLATE_NOTES.md)
- [风险指标框架](RISK_INDICATOR_FRAMEWORK.md)
- [数据字典](DATA_DICTIONARY.md)
- [视频分镜脚本](VIDEO_STORYBOARD.md)
- [视频制作说明](VIDEO_PRODUCTION_GUIDE.md)

完整仓库地址：<https://github.com/wzgig/china-railway-financial-risk-analysis>

## 合规说明

项目优先使用官方披露与可复核公开资料。对需要登录、验证码、付费或权限限制的平台，不绕过限制；若平台限制自动化抓取，则采用人工检索、合法导出或样本化记录，再用 Python 进行结构化清洗和分析。
