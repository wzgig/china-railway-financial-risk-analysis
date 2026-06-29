"""Build compliant external risk-event samples.

The rows below are curated from public court PDFs, public legal-text mirrors,
execution-information news reports, and QCC-cited public reports. They are not
bulk-scraped platform data. Execution and QCC rows are marked as candidate or
verify when the original platform requires manual confirmation.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path


SCHEMA_PATH = Path("configs/risk_event_schema.json")
OFFICIAL_EVENTS_CSV = Path("data/interim/risk_events_official_seed.csv")
EXTERNAL_EVENTS_CSV = Path("data/interim/risk_events_external_sample.csv")
COMBINED_EVENTS_CSV = Path("data/processed/risk_events_combined.csv")
DOC_OUTPUT = Path("docs/EXTERNAL_RISK_EVENTS_SAMPLE.md")
ACCESS_DATE = "2026-06-29"


def load_schema() -> dict[str, object]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def schema_fields(schema: dict[str, object]) -> list[str]:
    return [field["name"] for field in schema["fields"]]


def event(**kwargs: str) -> dict[str, str]:
    base = {
        "event_id": "",
        "source_type": "",
        "source_name": "",
        "source_url": "",
        "access_date": ACCESS_DATE,
        "search_keyword": "",
        "company_name": "",
        "company_role": "",
        "related_party": "",
        "event_type": "",
        "risk_type": "",
        "event_date": "",
        "year": "",
        "province": "",
        "city": "",
        "case_no": "",
        "cause": "",
        "amount_rmb": "",
        "summary": "",
        "severity_score": "2",
        "probability_score": "3",
        "evidence_status": "candidate",
        "notes": "",
    }
    base.update(kwargs)
    return base


def build_external_events() -> list[dict[str, str]]:
    return [
        event(
            event_id="EX2023-WENSHU-SH-230",
            source_type="wenshu",
            source_name="上海铁路运输法院民事判决书（2023）沪7101民初230号",
            source_url="https://www.hshfy.sh.cn/shfy/web/flws2pdf.jsp?pa=adGFoPaOoMjAyM6Opu6Y3MTAxw%2FGz9TIzMLrFJndzeGg9MSZ3c2xiPcPxysLF0L72yukPdcssz",
            search_keyword="中铁上海工程局 买卖合同纠纷 （2023）沪7101民初230号",
            company_name="中铁上海工程局集团有限公司",
            company_role="defendant",
            related_party="河北通力金属制品有限公司",
            event_type="civil_litigation",
            risk_type="compliance",
            event_date="2023-04-26",
            year="2023",
            province="上海",
            city="上海",
            case_no="（2023）沪7101民初230号",
            cause="买卖合同纠纷",
            amount_rmb="938036.20",
            summary="上海铁路运输法院判决中铁上海工程局集团有限公司支付货款、运费等约93.80万元，反映供应链结算争议。",
            severity_score="2",
            probability_score="3",
            evidence_status="core",
            notes="法院公开 PDF，可作为司法样本；金额按判决披露的付款义务整理。",
        ),
        event(
            event_id="EX2023-WENSHU-SH-496",
            source_type="wenshu",
            source_name="上海铁路运输法院民事判决书（2023）沪7101民初496号",
            source_url="https://www.hshfy.sh.cn/shfy/web/flws2pdf.jsp?pa=adGFoPaOoMjAyM6Opu6Y3MTAxw%2FGz9TQ5NrrFJndzeGg9MSZ3c2xiPcPxysLF0L72yukPdcssz",
            search_keyword="中铁上海工程局 买卖合同纠纷 （2023）沪7101民初496号",
            company_name="中铁上海工程局集团有限公司",
            company_role="defendant",
            related_party="江苏诚鑫达供应链管理有限公司",
            event_type="civil_litigation",
            risk_type="compliance",
            event_date="2023-06-28",
            year="2023",
            province="上海",
            city="上海",
            case_no="（2023）沪7101民初496号",
            cause="买卖合同纠纷",
            amount_rmb="692215.45",
            summary="上海铁路运输法院判决中铁上海工程局集团有限公司承担约69.22万元货款及相关费用，补充供应链付款类司法样本。",
            severity_score="2",
            probability_score="3",
            evidence_status="core",
            notes="法院公开 PDF，可作为司法样本；最终论文引用时需再次打开 PDF 复核。",
        ),
        event(
            event_id="EX2024-WENSHU-LN-1533",
            source_type="wenshu",
            source_name="辽宁省朝阳市中级人民法院二审判决书（2024）辽13民终1533号",
            source_url="https://zh.wikisource.org/wiki/%E4%B8%AD%E9%93%81%E4%B9%9D%E5%B1%80%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E4%B8%8E%E8%BE%BD%E5%AE%81%E5%8D%8E%E5%B1%95%E5%B8%82%E6%94%BF%E5%B7%A5%E7%A8%8B%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%BB%BA%E8%AE%BE%E5%B7%A5%E7%A8%8B%E6%96%BD%E5%B7%A5%E5%90%88%E5%90%8C%E7%BA%A0%E7%BA%B7%E4%BA%8C%E5%AE%A1%E5%88%A4%E5%86%B3%E4%B9%A6",
            search_keyword="中铁九局 辽宁华展 建设工程施工合同纠纷 二审判决",
            company_name="中铁九局集团有限公司",
            company_role="appellant_defendant",
            related_party="辽宁华展市政工程有限公司",
            event_type="civil_litigation",
            risk_type="project",
            event_date="2024-08-02",
            year="2024",
            province="辽宁",
            city="朝阳",
            case_no="（2024）辽13民终1533号",
            cause="建设工程施工合同纠纷",
            amount_rmb="2426785.19",
            summary="二审维持一审关于支付工程款约242.68万元及利息的结果，体现项目结算和分包争议风险。",
            severity_score="2",
            probability_score="3",
            evidence_status="candidate",
            notes="维基文库转载裁判文书，原始裁判文书网页面可能需要人工登录复核。",
        ),
        event(
            event_id="EX2023-EXEC-GZ-417",
            source_type="execution",
            source_name="每日经济新闻转引中国执行信息公开网",
            source_url="https://www.nbd.com.cn/articles/2024-04-10/3321035.html",
            search_keyword="中铁广州工程局集团第三工程有限公司 （2023）桂1425执417号",
            company_name="中铁广州工程局集团第三工程有限公司",
            company_role="dishonest_judgment_debtor",
            related_party="陕西康力建工有限公司；天等县人民法院",
            event_type="dishonest_judgment_debtor",
            risk_type="compliance",
            event_date="2023",
            year="2023",
            province="广西",
            city="崇左",
            case_no="（2023）桂1425执417号",
            cause="工程款及相关费用未履行",
            amount_rmb="9529917.62",
            summary="公开报道援引执行信息显示，该公司因工程款、案件受理费、保全费、担保费等约952.99万元被列入失信被执行人样本。",
            severity_score="3",
            probability_score="4",
            evidence_status="candidate",
            notes="报道含中国执行信息公开网截图；最终使用前应在执行平台或法院文书中人工复核。",
        ),
        event(
            event_id="EX2023-EXEC-TUNNEL-3-LIMIT",
            source_type="execution",
            source_name="每日经济新闻调查报道",
            source_url="https://www.nbd.com.cn/articles/2024-04-10/3321035.html",
            search_keyword="中铁隧道集团三处有限公司 限制消费令 国内非涉外仲裁裁决",
            company_name="中铁隧道集团三处有限公司",
            company_role="restricted_consumption_subject",
            related_party="深圳市柳空压缩机有限公司等五家公司；深圳市南山区人民法院",
            event_type="restricted_consumption",
            risk_type="liquidity",
            event_date="2023-11-01",
            year="2023",
            province="广东",
            city="深圳",
            case_no="未披露",
            cause="租赁合同与仲裁裁决未履行",
            amount_rmb="512000",
            summary="报道披露该公司在国内非涉外仲裁裁决执行中被出具限制消费令，报道列明两笔租赁欠款合计约51.20万元。",
            severity_score="2",
            probability_score="4",
            evidence_status="candidate",
            notes="金额为报道披露的两笔租赁欠款合计，不代表全部执行标的；需平台复核。",
        ),
        event(
            event_id="EX2023-EXEC-10J-2-LIMIT",
            source_type="execution",
            source_name="每日经济新闻调查报道",
            source_url="https://www.nbd.com.cn/articles/2024-04-10/3321035.html",
            search_keyword="中铁十局集团第二工程有限公司 限制消费令 买卖合同纠纷",
            company_name="中铁十局集团第二工程有限公司",
            company_role="restricted_consumption_subject",
            related_party="新野县安鑫商贸有限公司；郑州市金水区人民法院",
            event_type="restricted_consumption",
            risk_type="liquidity",
            event_date="2023-11-11",
            year="2023",
            province="河南",
            city="郑州",
            case_no="未披露",
            cause="买卖合同纠纷执行未履行",
            amount_rmb="",
            summary="报道披露供应商申请执行买卖合同纠纷后，法院对中铁十局二公司及法定代表人出具限制消费令，体现材料款拖欠和执行压力。",
            severity_score="2",
            probability_score="4",
            evidence_status="verify",
            notes="报道中金额为访谈估算区间，未录入结构化金额；需法院或执行平台复核。",
        ),
        event(
            event_id="EX2023-EXEC-6J-ROADBRIDGE",
            source_type="execution",
            source_name="中国质量新闻网/新浪财经转引中国执行信息公开网",
            source_url="https://finance.sina.cn/2023-01-31/detail-imyeancp0172215.d.html?vt=4",
            search_keyword="中铁六局集团路桥建设有限公司 2023年1月 被执行人 6463056",
            company_name="中铁六局集团路桥建设有限公司",
            company_role="judgment_debtor",
            related_party="玉溪市红塔区人民法院等",
            event_type="execution_case",
            risk_type="liquidity",
            event_date="2023-01-31",
            year="2023",
            province="云南",
            city="玉溪",
            case_no="（2023）云0402执170号等",
            cause="被执行人信息新增",
            amount_rmb="6463056",
            summary="公开报道援引执行信息显示，该公司2023年1月新增3条被执行人信息，执行标的合计646.31万元。",
            severity_score="3",
            probability_score="4",
            evidence_status="candidate",
            notes="报道列出至少一个案号及法院；其余两条需人工补齐。",
        ),
        event(
            event_id="EX2025-EXEC-3J-BRIDGE",
            source_type="execution",
            source_name="经济参考网/新浪财经转引天眼查",
            source_url="https://finance.sina.com.cn/stock/relnews/cn/2025-05-09/doc-inevxzxu7563170.shtml",
            search_keyword="中铁三局集团桥隧工程有限公司 新增 被执行人 1360万元",
            company_name="中铁三局集团桥隧工程有限公司",
            company_role="judgment_debtor",
            related_party="四川省成都市中级人民法院",
            event_type="execution_case",
            risk_type="liquidity",
            event_date="2025-05-09",
            year="2025",
            province="四川",
            city="成都",
            case_no="未披露",
            cause="新增两条被执行人信息",
            amount_rmb="13600000",
            summary="公开报道援引天眼查显示，该公司新增两条被执行人信息，执行金额分别约42.67万元和1319万元，合计约1360万元。",
            severity_score="3",
            probability_score="4",
            evidence_status="candidate",
            notes="数据来自公开报道转引的企业风险平台，案件细节尚未披露；需执行平台复核。",
        ),
        event(
            event_id="EX2026-QCC-TUNNEL-PENALTY",
            source_type="qcc",
            source_name="财中社转引企查查",
            source_url="https://m.caizhongshe.cn/article-7332928644422008550.html",
            search_keyword="中铁隧道局 企查查 行政处罚 460万",
            company_name="中铁隧道局集团有限公司",
            company_role="penalized_entity",
            related_party="行政监管部门",
            event_type="administrative_penalty",
            risk_type="compliance",
            event_date="2026-02-14",
            year="2026",
            province="",
            city="",
            case_no="未披露",
            cause="行政处罚记录汇总",
            amount_rmb="4600000",
            summary="财中社报道援引企查查数据称，中铁隧道局拥有26条行政处罚记录，罚款总额超过460万元。",
            severity_score="2",
            probability_score="4",
            evidence_status="verify",
            notes="企查查汇总指标，非逐条处罚明细；需授权导出或人工逐条复核后进入最终结论。",
        ),
        event(
            event_id="EX2026-QCC-TUNNEL-EXEC",
            source_type="qcc",
            source_name="财中社转引企查查",
            source_url="https://m.caizhongshe.cn/article-7332928644422008550.html",
            search_keyword="中铁隧道局 企查查 被执行人 1.3亿元",
            company_name="中铁隧道局集团有限公司",
            company_role="judgment_debtor",
            related_party="多地法院",
            event_type="execution_case",
            risk_type="liquidity",
            event_date="2026-02-14",
            year="2026",
            province="",
            city="",
            case_no="未披露",
            cause="被执行人信息汇总",
            amount_rmb="130000000",
            summary="财中社报道援引企查查数据称，截至2026年2月14日，中铁隧道局存在29条被执行人信息，被执行总金额约1.3亿元。",
            severity_score="4",
            probability_score="4",
            evidence_status="verify",
            notes="企查查汇总指标，可能与逐条执行案件重复；后续需去重并核验明细。",
        ),
        event(
            event_id="EX2026-QCC-TUNNEL-23EXEC",
            source_type="qcc",
            source_name="财中社转引企查查",
            source_url="https://m.caizhongshe.cn/article-7332928644422008550.html",
            search_keyword="中铁隧道局 40天 23起 执行 9458万元",
            company_name="中铁隧道局集团有限公司",
            company_role="judgment_debtor",
            related_party="天津市滨海新区人民法院；聊城市东昌府区人民法院等",
            event_type="execution_case",
            risk_type="liquidity",
            event_date="2026-02-10",
            year="2026",
            province="天津；山东",
            city="天津；聊城",
            case_no="（2026）津0116执2886号；（2026）鲁1502执2000号等",
            cause="短期内新增多起强制执行案件",
            amount_rmb="94580000",
            summary="报道称2026年1月13日至2月10日不到40天内，中铁隧道局累计新增23起执行案件，总执行标的约9458万元。",
            severity_score="4",
            probability_score="4",
            evidence_status="verify",
            notes="与企查查汇总被执行金额存在重叠风险；建模前需做事件级去重。",
        ),
    ]


def validate_events(events: list[dict[str, str]], schema: dict[str, object]) -> None:
    allowed_source_types = set(schema["source_types"])
    allowed_event_types = set(schema["event_types"])
    allowed_risk_types = set(schema["risk_types"])
    required_fields = [field["name"] for field in schema["fields"] if field["required"]]
    for item in events:
        missing = [field for field in required_fields if not item.get(field)]
        if missing:
            raise ValueError(f"{item.get('event_id')} missing required fields: {missing}")
        if item["source_type"] not in allowed_source_types:
            raise ValueError(f"{item['event_id']} has invalid source_type {item['source_type']}")
        if item["event_type"] not in allowed_event_types:
            raise ValueError(f"{item['event_id']} has invalid event_type {item['event_type']}")
        if item["risk_type"] not in allowed_risk_types:
            raise ValueError(f"{item['event_id']} has invalid risk_type {item['risk_type']}")


def read_events(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def amount_to_100m_text(amount: str) -> str:
    if not amount:
        return ""
    try:
        value = Decimal(amount) / Decimal("100000000")
    except InvalidOperation:
        return ""
    return f"{value.quantize(Decimal('0.0001'))}"


def write_markdown(external: list[dict[str, str]], combined: list[dict[str, str]]) -> None:
    source_counts = Counter(row["source_type"] for row in external)
    status_counts = Counter(row["evidence_status"] for row in external)
    year_counts = Counter(row["year"] for row in external)
    risk_counts = Counter(row["risk_type"] for row in external)

    lines = [
        "# 司法/执行/企查查扩展风险事件样本",
        "",
        "生成脚本：`scripts/build_external_risk_events.py`",
        "",
        "## 样本边界",
        "",
        "- 本轮补充只使用公开法院 PDF、公开裁判文书转载、新闻报道转引的执行信息和公开报道转引的企查查汇总指标。",
        "- 对裁判文书网、执行信息公开网和企查查，不绕过登录、验证码、付费墙或批量访问限制。",
        "- `core` 可作为较强样本；`candidate` 和 `verify` 仅用于课程过程样本与图谱结构验证，正式结论前必须人工复核。",
        "- 企查查汇总型记录可能与逐条执行案件重复，进入机器学习特征前需要按主体、日期、案号和金额去重。",
        "",
        "## 样本规模",
        "",
        f"- 外部扩展事件：{len(external)} 条",
        f"- 合并后事件：{len(combined)} 条",
        "",
        "### 来源类型",
        "",
        "| 来源类型 | 数量 |",
        "|---|---:|",
    ]
    for key, value in sorted(source_counts.items()):
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "### 证据状态", "", "| 状态 | 数量 |", "|---|---:|"])
    for key, value in sorted(status_counts.items()):
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "### 年份分布", "", "| 年份 | 数量 |", "|---|---:|"])
    for key, value in sorted(year_counts.items()):
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "### 风险类型", "", "| 风险类型 | 数量 |", "|---|---:|"])
    for key, value in sorted(risk_counts.items()):
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## 样本摘要",
            "",
            "| 事件ID | 来源 | 年份 | 主体 | 事件类型 | 风险类型 | 金额(亿元) | 证据状态 | 摘要 |",
            "|---|---|---:|---|---|---|---:|---|---|",
        ]
    )
    for row in external:
        lines.append(
            "| {event_id} | {source_type} | {year} | {company_name} | {event_type} | {risk_type} | {amount} | {status} | {summary} |".format(
                event_id=row["event_id"],
                source_type=row["source_type"],
                year=row["year"],
                company_name=row["company_name"],
                event_type=row["event_type"],
                risk_type=row["risk_type"],
                amount=amount_to_100m_text(row["amount_rmb"]),
                status=row["evidence_status"],
                summary=row["summary"],
            )
        )

    lines.extend(
        [
            "",
            "## 进入图谱和模型的处理方式",
            "",
            "- 图谱脚本优先读取 `data/processed/risk_events_combined.csv`，若该文件不存在则回退到官方披露种子事件。",
            "- 机器学习特征表应按年度聚合事件数量、执行金额、司法金额、企查查汇总金额和高严重度事件数。",
            "- 2026 年事件可作为最新监测样本，不应直接用于 2021-2025 年年度模型训练标签。",
            "- `verify` 样本进入最终报告前，要替换为逐条人工导出或官方平台复核记录。",
        ]
    )
    DOC_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    schema = load_schema()
    fields = schema_fields(schema)
    external = build_external_events()
    validate_events(external, schema)

    official = read_events(OFFICIAL_EVENTS_CSV)
    combined_by_id: dict[str, dict[str, str]] = {}
    for row in official + external:
        combined_by_id[row["event_id"]] = {field: row.get(field, "") for field in fields}
    combined = sorted(combined_by_id.values(), key=lambda row: (row["year"], row["event_id"]))
    validate_events(combined, schema)

    write_csv(EXTERNAL_EVENTS_CSV, external, fields)
    write_csv(COMBINED_EVENTS_CSV, combined, fields)
    write_markdown(external, combined)

    print(f"wrote {EXTERNAL_EVENTS_CSV} ({len(external)} external events)")
    print(f"wrote {COMBINED_EVENTS_CSV} ({len(combined)} combined events)")
    print(f"wrote {DOC_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
