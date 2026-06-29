# Skills、插件与工具规划

## 本次已用

| 能力 | 来源 | 用途 | 是否需要安装 |
|---|---|---|---|
| `course-paper-workflow` | 本地 skill | 课程项目规划、来源记录、质量门槛 | 否 |

## 当前判断

本阶段只需要整理要求、规划路线和创建项目结构，本地已有 skill 足够，不需要上网下载额外 skill 或插件。

## 后续可按需启用

| 阶段 | 可用 skill 或插件 | 用途 |
|---|---|---|
| 文献和引用 | `citation-management`、`bib-search-citation` | 检索文献、生成引用、维护 BibTeX |
| 数据脚本 | `python-testing-patterns`、`debugging-strategies` | 测试和调试清洗、建模脚本 |
| 网页交互 | `playwright`、`browser:control-in-app-browser` | 测试本地页面、合法自动化公开页面 |
| 报告排版 | `pdf`、`table-generation`、`course-paper-workflow` | DOCX/PDF 检查、表格生成 |
| 视频旁白 | `speech` | 生成 3 分钟旁白音频 |
| 部署或在线展示 | `cloudflare-deploy`、`vercel-deploy`、`netlify-deploy` | 只有需要网页展示时才使用 |

## Python 软件包建议

见 `requirements.txt`。先不自动安装，等进入脚本开发阶段再安装，避免污染环境。

## 外部软件建议

| 工具 | 用途 | 说明 |
|---|---|---|
| Gephi | 风险图谱可视化 | 必需或强烈建议 |
| Excel/WPS | 人工校对数据 | 用于检查导出表 |
| 剪映/CapCut/PowerPoint | 3 分钟视频制作 | 用图表、录屏和旁白即可 |
| LibreOffice/Pandoc | 报告格式转换 | 若需要从 Markdown 生成 DOCX/PDF |

## 合规边界

- 不绕过验证码、登录、付费、权限或反爬机制。
- 商业平台数据以人工导出、合法接口或授权访问为主。
- 爬虫脚本只用于公开、允许访问的数据，且设置合理频率。
- 报告中需要说明数据完整性限制。
