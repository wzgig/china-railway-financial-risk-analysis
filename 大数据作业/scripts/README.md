# 脚本说明

后续脚本按流程编号，便于视频展示和最终交付。

| 脚本 | 作用 | 主要输入 | 主要输出 |
| --- | --- | --- | --- |
| `01_collect_public_sources.py` | 整理公开资料索引，检查 URL 可访问性 | `data/raw/source_manifest.csv` | `data/interim/source_check.csv` |
| `02_build_network_dataset.py` | 生成节点表、边表和数据字典 | 配置文件、来源清单 | `data/processed/nodes.csv`、`data/processed/edges.csv`、`data/processed/data_dictionary.csv` |
| `03_analyze_network.py` | 计算中心性、PageRank、社群、关键路径和阶段摘要 | `nodes.csv`、`edges.csv` | `outputs/tables/network_metrics.csv`、`outputs/tables/key_paths.csv`、`data/processed/stage_summary.csv` |
| `04_visualize_network.py` | 生成静态图和交互图 | 网络指标、节点表、边表 | `outputs/figures/*.png`、`outputs/network/value_network_interactive.html` |
| `05_build_report_assets.py` | 汇总图表目录和报告素材 | 指标表、图表 | `docs/图表目录.md` |

建议运行方式：

```powershell
cd 大数据作业
python -m pip install -r requirements.txt
python .\scripts\01_collect_public_sources.py
python .\scripts\02_build_network_dataset.py
python .\scripts\03_analyze_network.py
python .\scripts\04_visualize_network.py
```

当前已完成 01-04 脚本和第一版网络数据，可继续编写报告初稿、视频录制指南和交付整理脚本。
