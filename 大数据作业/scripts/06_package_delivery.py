# -*- coding: utf-8 -*-
"""
用途：整理最终提交包，将报告、代码、数据、图表、交互网络和视频录制说明复制到交付目录。
输入：paper/报告.md，scripts/*.py，configs/*，data/*，outputs/*，docs/*
输出：交付/报告，交付/代码，交付/数据，交付/说明，交付/视频
说明：本脚本只复制和生成交付说明，不删除用户自行放入交付目录的文件。
"""

from __future__ import annotations

import csv
import shutil
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DELIVERY_DIR = PROJECT_ROOT / "交付"
REPORT_DIR = DELIVERY_DIR / "报告"
CODE_DIR = DELIVERY_DIR / "代码"
DATA_DIR = DELIVERY_DIR / "数据"
INFO_DIR = DELIVERY_DIR / "说明"
VIDEO_DIR = DELIVERY_DIR / "视频"
VIDEO_ASSET_DIR = VIDEO_DIR / "演示素材"
FIGURE_DELIVERY_DIR = INFO_DIR / "图表"
NETWORK_DELIVERY_DIR = INFO_DIR / "交互网络"
LOG_DIR = PROJECT_ROOT / "logs"

REPORT_PATH = PROJECT_ROOT / "paper" / "协鑫能科算电协同价值创造网络分析报告.md"
VIDEO_GUIDE_PATH = PROJECT_ROOT / "docs" / "视频录制指南.md"
FILE_LIST_PATH = INFO_DIR / "文件清单.md"
RUN_GUIDE_PATH = INFO_DIR / "运行说明.md"
VIDEO_README_PATH = VIDEO_DIR / "README.md"
DELIVERY_MANIFEST_PATH = INFO_DIR / "delivery_manifest.csv"
LOG_PATH = LOG_DIR / "06_package_delivery.log"
TEXT_SUFFIXES = {".csv", ".json", ".md", ".py", ".txt"}


def rel(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def ensure_dirs() -> None:
    for path in [
        REPORT_DIR,
        CODE_DIR,
        DATA_DIR,
        INFO_DIR,
        VIDEO_DIR,
        VIDEO_ASSET_DIR,
        FIGURE_DELIVERY_DIR,
        NETWORK_DELIVERY_DIR,
        LOG_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def normalize_text_file(path: Path) -> None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return

    text = path.read_text(encoding="utf-8-sig")
    encoding = "utf-8-sig" if path.suffix.lower() == ".csv" else "utf-8"
    path.write_text(text.rstrip() + "\n", encoding=encoding)


def copy_file(source: Path, destination: Path, records: list[dict[str, str]], required: bool = True) -> None:
    if not source.exists():
        if required:
            raise FileNotFoundError(f"缺少交付源文件：{rel(source)}")
        records.append({"source": rel(source), "destination": "", "status": "missing_optional"})
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    normalize_text_file(destination)
    records.append({"source": rel(source), "destination": rel(destination), "status": "copied"})


def copy_many(pattern: str, destination_dir: Path, records: list[dict[str, str]], required: bool = True) -> None:
    matches = sorted(PROJECT_ROOT.glob(pattern))
    if required and not matches:
        raise FileNotFoundError(f"没有匹配到交付源文件：{pattern}")
    for source in matches:
        if source.is_file():
            copy_file(source, destination_dir / source.name, records, required=required)


def write_run_guide() -> None:
    lines = [
        "# 运行说明",
        "",
        "本交付包对应协鑫能科（002015）算电协同价值创造网络分析课程作业。若需要从源码复现结果，请在项目根目录运行以下命令：",
        "",
        "```powershell",
        'cd "<知世项目目录>\\大数据作业"',
        "python -m pip install -r requirements.txt",
        "python .\\scripts\\01_collect_public_sources.py",
        "python .\\scripts\\02_build_network_dataset.py",
        "python .\\scripts\\03_analyze_network.py",
        "python .\\scripts\\04_visualize_network.py",
        "python .\\scripts\\05_build_report_assets.py",
        "python .\\scripts\\06_package_delivery.py",
        "```",
        "",
        "## 目录说明",
        "",
        "- `报告/`：分析报告 Markdown 文件。",
        "- `代码/`：复现流程需要的 Python 脚本、配置文件和依赖清单。",
        "- `数据/`：节点表、边表、数据字典、阶段摘要、中心性指标表、关键路径表和来源检查表。",
        "- `说明/`：图表目录、结果摘要、数据字典说明、项目 README、数据来源记录和运行说明。",
        "- `说明/图表/`：报告可插入的 PNG 图件。",
        "- `说明/交互网络/`：交互 HTML 网络图。",
        "- `视频/`：3 分钟解说视频录制指南和演示素材。实际视频文件如 `.mp4` 按根目录 `.gitignore` 规则保留本地，不提交 Git。",
        "",
        "## 数据边界",
        "",
        "- 边权重是 1-5 分的相对重要性，不代表真实交易金额、合同规模或收入占比。",
        "- `evidence_level=simulated` 的节点或边属于公开事实约束下的结构化模拟，报告中不能写成公司已披露交易。",
        "- 交互 HTML 引用 Plotly CDN，离线环境下若无法显示，可改用 `outputs/figures/` 中的静态图。",
        "",
    ]
    RUN_GUIDE_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_video_readme() -> None:
    lines = [
        "# 视频交付说明",
        "",
        "本目录用于放置 3 分钟内场景决策解说视频及录制素材。",
        "",
        "当前已提供：",
        "",
        "- `视频录制指南.md`：180 秒解说分镜、画面顺序和口播要点。",
        "- `演示素材/value_network_interactive.html`：可交互网络图，用于视频中展示节点和边。",
        "- `演示素材/*.png`：中心性、阶段演化、社群结构和成本机制图。",
        "",
        "实际录制出的 `.mp4` 文件体积通常较大，根目录 `.gitignore` 已默认不提交视频文件。提交课程平台时，可将视频文件放在本目录后与交付包一起上传。",
        "",
    ]
    VIDEO_README_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_file_list(records: list[dict[str, str]]) -> None:
    delivered = [record for record in records if record["status"] in {"copied", "created"}]
    missing = [record for record in records if record["status"].startswith("missing")]

    lines = [
        "# 文件清单",
        "",
        f"生成时间：{datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        f"已交付文件数：{len(delivered)}",
        "",
        "| 来源 | 交付位置 | 状态 |",
        "| --- | --- | --- |",
    ]
    for record in records:
        lines.append(f"| {record['source']} | {record['destination']} | {record['status']} |")

    if missing:
        lines.extend(["", "## 缺失或可选文件", ""])
        for record in missing:
            lines.append(f"- {record['source']}：{record['status']}")

    FILE_LIST_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with DELIVERY_MANIFEST_PATH.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["source", "destination", "status"])
        writer.writeheader()
        writer.writerows(records)


def write_log(records: list[dict[str, str]]) -> None:
    copied_count = sum(1 for record in records if record["status"] == "copied")
    lines = [
        f"运行时间：{datetime.now():%Y-%m-%d %H:%M:%S}",
        f"复制文件数：{copied_count}",
        f"交付目录：{rel(DELIVERY_DIR)}",
        f"清单文件：{rel(FILE_LIST_PATH)}",
    ]
    LOG_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ensure_dirs()
    records: list[dict[str, str]] = []

    copy_file(REPORT_PATH, REPORT_DIR / REPORT_PATH.name, records)

    copy_many("scripts/*.py", CODE_DIR / "scripts", records)
    copy_file(PROJECT_ROOT / "scripts" / "README.md", CODE_DIR / "scripts" / "README.md", records)
    copy_many("configs/*", CODE_DIR / "configs", records)
    copy_file(PROJECT_ROOT / "requirements.txt", CODE_DIR / "requirements.txt", records)

    copy_many("data/raw/*.csv", DATA_DIR / "raw", records)
    copy_many("data/interim/*.csv", DATA_DIR / "interim", records)
    copy_many("data/processed/*.csv", DATA_DIR / "processed", records)
    copy_many("outputs/tables/*.csv", DATA_DIR / "tables", records)

    copy_many("outputs/figures/*.png", FIGURE_DELIVERY_DIR, records)
    copy_many("outputs/network/*.html", NETWORK_DELIVERY_DIR, records)
    copy_many("outputs/figures/*.png", VIDEO_ASSET_DIR, records)
    copy_many("outputs/network/*.html", VIDEO_ASSET_DIR, records)

    for source in [
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "任务要求.md",
        PROJECT_ROOT / "工作记录.md",
        PROJECT_ROOT / "数据来源记录.md",
        PROJECT_ROOT / "完整执行规划.md",
        PROJECT_ROOT / "docs" / "图表目录.md",
        PROJECT_ROOT / "docs" / "结果摘要.md",
        PROJECT_ROOT / "docs" / "数据字典.md",
        PROJECT_ROOT / "docs" / "视频录制指南.md",
    ]:
        copy_file(source, INFO_DIR / source.name, records)

    copy_file(VIDEO_GUIDE_PATH, VIDEO_DIR / "视频录制指南.md", records)

    write_run_guide()
    write_video_readme()
    records.append({"source": "generated", "destination": rel(RUN_GUIDE_PATH), "status": "created"})
    records.append({"source": "generated", "destination": rel(VIDEO_README_PATH), "status": "created"})

    write_file_list(records)
    write_log(records)

    print(f"已整理交付目录：{rel(DELIVERY_DIR)}")
    print(f"已生成：{rel(FILE_LIST_PATH)}")
    print(f"已生成：{rel(RUN_GUIDE_PATH)}")


if __name__ == "__main__":
    main()
