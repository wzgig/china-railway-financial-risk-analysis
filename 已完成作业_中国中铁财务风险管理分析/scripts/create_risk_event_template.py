"""Create a compliant risk event collection template."""

from __future__ import annotations

import csv
import json
from pathlib import Path


SCHEMA_PATH = Path("configs/risk_event_schema.json")
INTERIM_OUTPUT = Path("data/interim/risk_event_collection_template.csv")
DOC_OUTPUT = Path("docs/RISK_EVENT_COLLECTION_TEMPLATE.md")


def load_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def write_csv_template(schema: dict[str, object]) -> Path:
    INTERIM_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [field["name"] for field in schema["fields"]]
    sample_row = {
        "event_id": "EV2025-0001",
        "source_type": "manual_check",
        "source_name": "example only",
        "source_url": "",
        "access_date": "2026-06-29",
        "search_keyword": "中国中铁",
        "company_name": "中国中铁股份有限公司",
        "company_role": "issuer",
        "related_party": "",
        "event_type": "rating_action",
        "risk_type": "solvency",
        "event_date": "2025-05-07",
        "year": "2025",
        "province": "",
        "city": "",
        "case_no": "",
        "cause": "跟踪评级",
        "amount_rmb": "",
        "summary": "示例行：请删除后再录入真实数据。",
        "severity_score": "2",
        "probability_score": "2",
        "evidence_status": "exclude",
        "notes": "Template example; not evidence.",
    }
    with INTERIM_OUTPUT.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(sample_row)
    return INTERIM_OUTPUT


def write_markdown(schema: dict[str, object]) -> Path:
    fields = schema["fields"]
    lines = [
        "# 风险事件采集合规模板",
        "",
        "复现脚本：`scripts/create_risk_event_template.py`",
        "",
        f"版本：`{schema['version']}`",
        "",
        "## 合规边界",
        "",
        f"{schema['compliance_note']}",
        "",
        "- 中国裁判文书网、执行信息公开网、企查查等平台如需登录、验证码、授权或付费，不绕过限制。",
        "- 若平台不支持批量导出，采用人工检索、样本化记录或授权导出，再用 Python 清洗。",
        "- 不采集或公开自然人证件编号、联系方式、详细居住地址等个人敏感信息。",
        "- 原始截图、导出表和 PDF 保留本地，公开仓库只保留字段说明、脚本和脱敏摘要。",
        "",
        "## 本地模板",
        "",
        "`data/interim/risk_event_collection_template.csv` 已生成。该文件是本地中间模板，不纳入公开仓库。",
        "",
        "## 字段说明",
        "",
        "| 字段 | 必填 | 说明 |",
        "|---|---|---|",
    ]
    for field in fields:
        required = "是" if field["required"] else "否"
        lines.append(f"| `{field['name']}` | {required} | {field['description']} |")

    lines.extend(
        [
            "",
            "## 推荐检索主体",
            "",
            "- 中国中铁股份有限公司",
            "- 中铁一局集团有限公司",
            "- 中铁二局集团有限公司",
            "- 中铁三局集团有限公司",
            "- 中铁四局集团有限公司",
            "- 中铁五局集团有限公司",
            "- 中铁六局集团有限公司",
            "- 中铁七局集团有限公司",
            "- 中铁八局集团有限公司",
            "- 中铁十局集团有限公司",
            "- 中铁建工集团有限公司",
            "- 中铁大桥局集团有限公司",
            "- 中铁隧道局集团有限公司",
            "- 中铁电气化局集团有限公司",
            "",
            "## 推荐检索词",
            "",
            "- 司法事件：`中国中铁 建设工程施工合同纠纷`、`中国中铁 买卖合同纠纷`、`中铁四局 执行`。",
            "- 执行信息：主体名称 + `被执行人`、`失信被执行人`、`限制消费`、`终本案件`。",
            "- 企业风险：主体名称 + `行政处罚`、`经营异常`、`司法协助`、`股权冻结`、`环保处罚`、`安全生产处罚`。",
            "",
            "## 与 Gephi 图谱的衔接",
            "",
            "- `company_name` 生成公司节点。",
            "- `related_party` 生成交易对手或法院节点。",
            "- `event_type` 和 `risk_type` 生成风险事件与风险类别节点。",
            "- `province`、`city` 生成地区节点。",
            "- `amount_rmb`、`severity_score`、`probability_score` 可转为边权重。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return DOC_OUTPUT


def main() -> int:
    schema = load_schema()
    csv_path = write_csv_template(schema)
    doc_path = write_markdown(schema)
    print(f"wrote {csv_path}")
    print(f"wrote {doc_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
