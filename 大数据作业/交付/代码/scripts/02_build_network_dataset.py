# -*- coding: utf-8 -*-
"""
用途：依据公开资料和结构化模拟规则，生成协鑫能科算电协同社会网络数据集。
输入：configs/network_schema.json，data/raw/source_manifest.csv，data/interim/source_check.csv（可选）
输出：data/processed/nodes.csv，data/processed/edges.csv，data/processed/data_dictionary.csv
说明：边权重表示网络中的相对重要性，不代表真实交易金额或收入占比。
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "configs" / "network_schema.json"
RAW_SOURCE_PATH = PROJECT_ROOT / "data" / "raw" / "source_manifest.csv"
SOURCE_CHECK_PATH = PROJECT_ROOT / "data" / "interim" / "source_check.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
NODES_PATH = PROCESSED_DIR / "nodes.csv"
EDGES_PATH = PROCESSED_DIR / "edges.csv"
DICTIONARY_PATH = PROCESSED_DIR / "data_dictionary.csv"


def load_schema() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"找不到 schema：{CONFIG_PATH.relative_to(PROJECT_ROOT)}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_source_ids() -> set[str]:
    source_path = SOURCE_CHECK_PATH if SOURCE_CHECK_PATH.exists() else RAW_SOURCE_PATH
    if not source_path.exists():
        raise FileNotFoundError("找不到 data/raw/source_manifest.csv 或 data/interim/source_check.csv")
    return set(pd.read_csv(source_path, dtype=str, keep_default_na=False, encoding="utf-8-sig")["source_id"])


def node(
    node_id: str,
    node_name: str,
    node_type: str,
    stage: str,
    value_role: str,
    cost_role: str,
    evidence_level: str,
    source_id: str,
    note: str,
) -> dict[str, str]:
    return {
        "node_id": node_id,
        "node_name": node_name,
        "node_type": node_type,
        "stage": stage,
        "value_role": value_role,
        "cost_role": cost_role,
        "evidence_level": evidence_level,
        "source_id": source_id,
        "note": note,
    }


def edge(
    source: str,
    target: str,
    edge_type: str,
    weight: int,
    stage: str,
    scenario: str,
    cost_mechanism: str,
    value_outcome: str,
    evidence_source: str,
    evidence_level: str,
    note: str,
) -> dict[str, Any]:
    return {
        "source": source,
        "target": target,
        "edge_type": edge_type,
        "weight": weight,
        "stage": stage,
        "scenario": scenario,
        "cost_mechanism": cost_mechanism,
        "value_outcome": value_outcome,
        "evidence_source": evidence_source,
        "evidence_level": evidence_level,
        "note": note,
    }


def build_nodes() -> list[dict[str, str]]:
    return [
        node("N001", "协鑫能科", "company", "all", "ecosystem_orchestrator", "coordination_cost", "company", "S001", "公司核心主体，承接电力与算力协同战略"),
        node("N002", "AI赋能虚拟电厂平台", "platform", "all", "dispatcher", "dispatch_cost", "company", "S004", "连接资源、负荷、算法和市场的调度平台"),
        node("N003", "能源交易平台", "platform", "2024", "market_connector", "transaction_cost", "company", "S002", "支撑电力交易、绿电交易和辅助服务收益"),
        node("N004", "零碳园区能源平台", "platform", "2025", "scenario_operator", "coordination_cost", "simulated", "S002", "面向园区综合能源和低碳服务的场景节点"),
        node("N005", "清洁能源资源", "resource", "all", "resource_holder", "energy_cost", "official", "S005", "绿电供给和低碳算力的基础资源"),
        node("N006", "热电联产资源", "resource", "2024", "resource_holder", "energy_cost", "company", "S002", "公司能源资产与稳定供能能力的组成部分"),
        node("N007", "新型储能", "resource", "2025", "flexibility_buffer", "flexibility_cost", "industry", "S005", "提升调节能力并降低峰谷波动成本"),
        node("N008", "充换电与可调负荷", "resource", "2024", "flexible_load", "flexibility_cost", "company", "S002", "来自充换电和终端侧的可调节资源"),
        node("N009", "工商业用户侧负荷", "resource", "2024", "demand_flexibility", "coordination_cost", "industry", "S006", "需求响应和虚拟电厂调节的关键负荷"),
        node("N010", "数据中心/AIDC负荷", "resource", "2025", "computing_load", "energy_cost", "industry", "S007", "算力增长带来的高可靠低碳用能需求"),
        node("N011", "气象数据资源", "resource", "2024", "data_input", "coordination_cost", "company", "S004", "用于预测新能源出力和负荷波动"),
        node("N012", "设备运行数据", "resource", "2024", "data_input", "operation_cost", "company", "S004", "用于设备状态监测和调度评估"),
        node("N013", "电价与市场数据", "resource", "2024", "data_input", "transaction_cost", "company", "S004", "用于现货和辅助服务收益优化"),
        node("N014", "政策与碳约束数据", "policy", "2024", "rule_input", "green_compliance_cost", "official", "S005", "用于反映电力市场化、绿电和低碳约束"),
        node("N015", "工业负荷模型", "capability", "2024", "load_forecaster", "dispatch_cost", "company", "S004", "识别工业侧可调节能力"),
        node("N016", "分布式能源负荷预测模型", "capability", "2024", "resource_forecaster", "dispatch_cost", "company", "S004", "预测分布式资源和负荷曲线"),
        node("N017", "能源调度模型", "capability", "all", "optimization_engine", "dispatch_cost", "company", "S004", "把数据转化为虚拟电厂调度决策"),
        node("N018", "收益优化模型", "capability", "2026", "revenue_optimizer", "transaction_cost", "company", "S004", "平衡电力交易、辅助服务和需求响应收益"),
        node("N019", "算法评估模型", "capability", "2026", "model_governance", "coordination_cost", "company", "S004", "评估算法稳定性和场景适配性"),
        node("N020", "新型电力系统行动方案（2024-2027年）", "policy", "2024", "policy_driver", "green_compliance_cost", "official", "S005", "2024-2027 战略阶段的政策背景"),
        node("N021", "数据中心绿色低碳政策", "policy", "2025", "policy_driver", "green_compliance_cost", "official", "S007", "推动算力中心与绿电资源协同"),
        node("N022", "电力市场化改革规则", "policy", "2024", "market_rule", "transaction_cost", "official", "S006", "影响现货、辅助服务和需求响应市场机制"),
        node("N023", "电力现货市场", "market", "2024", "price_signal", "transaction_cost", "official", "S006", "提供价格信号和交易收益空间"),
        node("N024", "辅助服务市场", "market", "2024", "flexibility_market", "transaction_cost", "official", "S006", "将调节能力转化为市场收益"),
        node("N025", "绿电交易市场", "market", "2025", "green_premium_market", "green_compliance_cost", "official", "S005", "支撑绿色电力消费和低碳溢价"),
        node("N026", "碳交易与绿证市场", "market", "2026", "carbon_value_market", "green_compliance_cost", "industry", "S005", "把碳约束转化为合规与价值证明"),
        node("N027", "需求响应市场", "market", "2024", "demand_response_market", "flexibility_cost", "official", "S006", "释放用户侧负荷调节价值"),
        node("N028", "工业用户", "customer", "2024", "demand_owner", "energy_cost", "industry", "S006", "参与需求响应并获得节能收益"),
        node("N029", "园区客户", "customer", "2025", "scenario_customer", "coordination_cost", "simulated", "S002", "零碳园区和综合能源服务需求主体"),
        node("N030", "AIDC/智算客户", "customer", "2025", "computing_customer", "energy_cost", "industry", "S007", "需要稳定、低碳和可追溯电力供应"),
        node("N031", "公共机构客户", "customer", "2026", "public_customer", "green_compliance_cost", "industry", "S005", "公共低碳治理和能效管理需求主体"),
        node("N032", "设备供应商", "partner", "2024", "technology_supplier", "operation_cost", "simulated", "S004", "支撑设备数据采集和储能等硬件能力"),
        node("N033", "算力生态伙伴", "partner", "2025", "computing_partner", "coordination_cost", "industry", "S007", "连接算力需求、能源服务和客户场景"),
        node("N034", "地方能源平台", "partner", "2025", "local_coordinator", "coordination_cost", "industry", "S006", "支撑地方资源接入和市场规则落地"),
        node("N035", "节能收益共享机制", "market", "2026", "value_share_rule", "revenue_share", "simulated", "S006", "将节能和削峰收益在客户与平台间分配"),
        node("N036", "调节收益分成机制", "market", "2026", "value_share_rule", "revenue_share", "simulated", "S006", "将辅助服务和需求响应收益转化为合作激励"),
        node("N037", "绿色溢价机制", "market", "2027", "green_value_rule", "green_compliance_cost", "simulated", "S007", "支撑绿电、绿证和低碳算力价值证明"),
        node("N038", "安全合规与运维流程", "capability", "2027", "process_innovation", "operation_cost", "simulated", "S004", "通过流程创新降低运维和协同风险"),
    ]


def build_edges() -> list[dict[str, Any]]:
    return [
        edge("N020", "N001", "policy_constraint", 5, "2024", "战略规划", "绿色合规成本", "明确 2024-2027 新型电力系统转型方向", "S005", "official", "官方行动方案形成战略外部约束"),
        edge("N020", "N002", "policy_constraint", 4, "2024", "虚拟电厂", "调度成本", "提升新型电力系统调节能力", "S005", "official", "虚拟电厂承担灵活性资源聚合"),
        edge("N022", "N003", "policy_constraint", 5, "2024", "电力交易", "交易成本", "推动平台接入市场化交易规则", "S006", "official", "市场规则影响交易平台价值"),
        edge("N022", "N023", "policy_constraint", 5, "2024", "电力现货", "交易成本", "形成价格信号和风险管理需求", "S006", "official", "现货市场提供价格发现机制"),
        edge("N022", "N024", "policy_constraint", 4, "2024", "辅助服务", "交易成本", "释放灵活调节资源收益", "S006", "official", "辅助服务连接储能和可调负荷"),
        edge("N022", "N027", "policy_constraint", 4, "2024", "需求响应", "柔性成本", "扩大用户侧调节价值", "S006", "official", "需求响应是用户侧协同入口"),
        edge("N021", "N010", "policy_constraint", 4, "2025", "AIDC", "绿色合规成本", "推动数据中心低碳用能", "S007", "official", "政策回应算力与绿电协同"),
        edge("N021", "N030", "policy_constraint", 4, "2025", "AIDC", "绿色合规成本", "增强智算客户绿电消费约束", "S007", "official", "客户低碳需求受到政策强化"),
        edge("N014", "N017", "data_flow", 4, "2024", "算法调度", "绿色合规成本", "将政策与碳约束转化为调度规则", "S005", "official", "政策数据进入调度模型"),
        edge("N001", "N002", "technology_collaboration", 5, "all", "虚拟电厂", "协调成本", "公司通过平台组织资源和市场", "S004", "company", "核心主体与平台能力连接"),
        edge("N001", "N003", "technology_collaboration", 4, "2024", "电力交易", "交易成本", "公司通过交易平台连接市场", "S002", "company", "能源服务业务与市场交易协同"),
        edge("N001", "N004", "technology_collaboration", 3, "2025", "零碳园区", "协调成本", "拓展综合能源服务场景", "S002", "simulated", "园区场景为结构化模拟关系"),
        edge("N001", "N017", "technology_collaboration", 5, "all", "算法调度", "调度成本", "把模型能力嵌入公司运营", "S004", "company", "投资者关系记录支撑模型能力"),
        edge("N001", "N033", "technology_collaboration", 4, "2025", "AIDC", "协调成本", "连接算力生态和能源服务", "S007", "industry", "算力生态关系为行业逻辑补充"),
        edge("N001", "N034", "technology_collaboration", 3, "2025", "地方协同", "协调成本", "推动地方资源和市场规则落地", "S006", "industry", "地方能源平台用于解释区域协同"),
        edge("N001", "N032", "technology_collaboration", 3, "2024", "设备接入", "运维成本", "支撑设备数据采集与储能接入", "S004", "simulated", "设备供应关系为结构化模拟"),
        edge("N005", "N002", "energy_supply", 5, "all", "虚拟电厂", "能源成本", "为平台提供清洁电力资源池", "S005", "official", "清洁能源是低碳供给基础"),
        edge("N006", "N002", "energy_supply", 4, "2024", "能源服务", "能源成本", "提供稳定电热联供资源", "S002", "company", "公司能源资产支持基础供能"),
        edge("N007", "N002", "dispatch", 4, "2025", "虚拟电厂", "调度成本", "提高削峰填谷和调节能力", "S005", "industry", "储能增强平台灵活性"),
        edge("N008", "N002", "dispatch", 4, "2024", "虚拟电厂", "柔性成本", "形成充换电可调负荷池", "S002", "company", "充换电负荷可参与调节"),
        edge("N009", "N002", "dispatch", 4, "2024", "需求响应", "协调成本", "聚合工商业可调节负荷", "S006", "industry", "工商业负荷是需求响应基础"),
        edge("N010", "N002", "dispatch", 3, "2025", "AIDC", "能源成本", "将数据中心负荷纳入协同调度", "S007", "industry", "AIDC 负荷用于场景扩展"),
        edge("N005", "N004", "energy_supply", 4, "2025", "零碳园区", "能源成本", "降低园区低碳用能成本", "S005", "industry", "清洁能源与园区低碳场景连接"),
        edge("N007", "N004", "energy_supply", 3, "2025", "零碳园区", "柔性成本", "增强园区峰谷调节能力", "S005", "industry", "储能支持园区稳定用能"),
        edge("N009", "N004", "dispatch", 3, "2025", "零碳园区", "协调成本", "实现园区可调负荷管理", "S006", "simulated", "园区负荷调节为模拟连接"),
        edge("N010", "N004", "energy_supply", 3, "2025", "AIDC", "能源成本", "服务园区内算力负荷", "S007", "simulated", "AIDC 园区供能为结构化模拟"),
        edge("N011", "N016", "data_flow", 4, "2024", "算法调度", "调度成本", "提升分布式能源和负荷预测精度", "S004", "company", "气象数据进入预测模型"),
        edge("N012", "N016", "data_flow", 4, "2024", "算法调度", "运维成本", "把设备状态纳入预测过程", "S004", "company", "设备运行数据进入模型"),
        edge("N013", "N018", "data_flow", 4, "2026", "收益优化", "交易成本", "支撑现货和辅助服务收益判断", "S004", "company", "电价数据服务收益模型"),
        edge("N009", "N015", "data_flow", 4, "2024", "需求响应", "协调成本", "识别工业负荷可调节窗口", "S004", "company", "工业负荷模型需要用户负荷数据"),
        edge("N010", "N015", "data_flow", 3, "2025", "AIDC", "能源成本", "识别算力负荷的稳定供能需求", "S007", "industry", "AIDC 负荷纳入模型场景"),
        edge("N008", "N015", "data_flow", 3, "2024", "充换电", "柔性成本", "识别充换电负荷弹性", "S002", "company", "充换电负荷进入工业负荷建模"),
        edge("N012", "N019", "data_flow", 3, "2026", "算法治理", "运维成本", "评估模型和设备运行稳定性", "S004", "company", "设备数据用于算法评估"),
        edge("N016", "N017", "technology_collaboration", 4, "2024", "算法调度", "调度成本", "预测结果进入能源调度模型", "S004", "company", "预测与调度模型串联"),
        edge("N015", "N017", "technology_collaboration", 4, "2024", "需求响应", "调度成本", "将可调负荷识别结果转化为调度策略", "S004", "company", "工业负荷模型支撑调度"),
        edge("N017", "N002", "dispatch", 5, "all", "虚拟电厂", "调度成本", "输出虚拟电厂调度指令", "S004", "company", "调度模型是平台智能化核心"),
        edge("N018", "N003", "technology_collaboration", 4, "2026", "收益优化", "交易成本", "把收益评估结果用于交易策略", "S004", "company", "收益模型连接交易平台"),
        edge("N019", "N017", "technology_collaboration", 3, "2026", "算法治理", "协调成本", "改进调度模型稳定性和可解释性", "S004", "company", "算法评估反馈调度模型"),
        edge("N002", "N008", "dispatch", 4, "2024", "虚拟电厂", "柔性成本", "调度充换电负荷削峰填谷", "S002", "company", "平台对可调负荷进行控制"),
        edge("N002", "N009", "dispatch", 5, "2024", "需求响应", "协调成本", "组织工商业用户参与需求响应", "S006", "industry", "平台聚合用户侧负荷"),
        edge("N002", "N007", "dispatch", 4, "2025", "虚拟电厂", "调度成本", "通过储能平滑负荷波动", "S005", "industry", "储能接受平台调度"),
        edge("N002", "N023", "market_trade", 4, "2024", "电力现货", "交易成本", "根据价格信号优化购售电策略", "S006", "official", "平台连接现货市场"),
        edge("N002", "N024", "market_trade", 5, "2024", "辅助服务", "交易成本", "将调节能力转化为辅助服务收益", "S006", "official", "辅助服务是灵活性价值变现入口"),
        edge("N002", "N027", "market_trade", 5, "2024", "需求响应", "柔性成本", "组织负荷侧参与响应获得收益", "S006", "official", "需求响应收益反哺客户"),
        edge("N003", "N023", "market_trade", 4, "2024", "电力现货", "交易成本", "降低价格波动中的交易摩擦", "S006", "official", "交易平台对接现货市场"),
        edge("N003", "N025", "market_trade", 5, "2025", "绿电交易", "绿色合规成本", "为算力和园区客户匹配绿电", "S005", "official", "绿电市场服务低碳需求"),
        edge("N003", "N026", "market_trade", 4, "2026", "碳交易", "绿色合规成本", "形成低碳权益和合规证明", "S005", "industry", "碳与绿证市场支持绿色价值"),
        edge("N003", "N024", "market_trade", 3, "2026", "辅助服务", "交易成本", "沉淀调节收益结算能力", "S006", "industry", "交易平台扩展辅助服务"),
        edge("N004", "N029", "energy_supply", 4, "2025", "零碳园区", "能源成本", "为园区客户提供综合能源服务", "S002", "simulated", "园区平台与客户连接为模拟关系"),
        edge("N004", "N030", "energy_supply", 3, "2025", "AIDC", "能源成本", "为园区内智算负荷提供低碳供能", "S007", "simulated", "零碳园区承接算力场景"),
        edge("N005", "N030", "energy_supply", 4, "2025", "AIDC", "绿色合规成本", "支撑智算客户低碳稳定用能", "S007", "industry", "清洁能源直接支撑算力客户"),
        edge("N007", "N030", "energy_supply", 3, "2025", "AIDC", "柔性成本", "提高算力负荷用能可靠性", "S007", "industry", "储能缓冲算力负荷波动"),
        edge("N030", "N010", "data_flow", 4, "2025", "AIDC", "能源成本", "将算力需求转化为可预测负荷", "S007", "industry", "客户需求形成数据中心负荷"),
        edge("N029", "N009", "data_flow", 3, "2025", "零碳园区", "协调成本", "园区客户负荷进入需求响应管理", "S006", "simulated", "园区需求数据用于负荷聚合"),
        edge("N028", "N009", "data_flow", 4, "2024", "需求响应", "协调成本", "工业用户提供可调负荷数据", "S006", "industry", "工业用户是负荷响应主体"),
        edge("N031", "N009", "data_flow", 2, "2026", "公共机构", "绿色合规成本", "公共机构低碳治理进入负荷管理", "S005", "simulated", "公共机构场景为补充连接"),
        edge("N002", "N028", "dispatch", 4, "2024", "需求响应", "协调成本", "向工业用户输出调节策略", "S006", "industry", "平台连接工业客户"),
        edge("N002", "N029", "dispatch", 3, "2025", "零碳园区", "协调成本", "向园区客户输出能源管理策略", "S002", "simulated", "平台管理园区客户需求"),
        edge("N002", "N030", "dispatch", 3, "2025", "AIDC", "能源成本", "为智算客户提供稳定低碳用能安排", "S007", "industry", "算电协同面向智算客户"),
        edge("N002", "N031", "dispatch", 2, "2026", "公共机构", "绿色合规成本", "提供公共低碳能源管理", "S005", "simulated", "公共机构为扩展场景"),
        edge("N023", "N036", "value_share", 3, "2026", "电力现货", "收益分配", "把价差管理收益纳入分成机制", "S006", "industry", "现货收益进入价值分配"),
        edge("N024", "N036", "value_share", 4, "2026", "辅助服务", "收益分配", "辅助服务收益在平台和资源间分配", "S006", "industry", "调节收益需要分成机制"),
        edge("N027", "N035", "value_share", 5, "2026", "需求响应", "收益分配", "将响应收益反馈给用户侧负荷", "S006", "official", "需求响应收益反哺用户"),
        edge("N025", "N037", "value_share", 4, "2027", "绿电交易", "绿色合规成本", "形成绿色用能溢价和品牌价值", "S005", "official", "绿电交易支撑绿色溢价"),
        edge("N026", "N037", "value_share", 3, "2027", "碳交易", "绿色合规成本", "把碳合规和绿证转化为价值证明", "S005", "industry", "碳与绿证增强可追溯价值"),
        edge("N035", "N028", "value_share", 4, "2026", "需求响应", "收益分配", "工业用户获得节能和响应收益", "S006", "industry", "价值共享增强客户参与意愿"),
        edge("N035", "N029", "value_share", 4, "2026", "零碳园区", "收益分配", "园区客户分享节能收益", "S002", "simulated", "节能收益共享为模拟机制"),
        edge("N036", "N001", "value_share", 4, "2026", "辅助服务", "收益分配", "公司获得调节服务和平台运营收益", "S006", "industry", "收益分成反哺公司能力建设"),
        edge("N036", "N028", "value_share", 3, "2026", "需求响应", "收益分配", "工业用户获得调节收益分成", "S006", "industry", "负荷侧收益分配机制"),
        edge("N037", "N030", "value_share", 4, "2027", "AIDC", "绿色合规成本", "智算客户获得低碳算力价值证明", "S007", "simulated", "绿色溢价与算力客户连接"),
        edge("N037", "N001", "value_share", 3, "2027", "绿电交易", "绿色合规成本", "公司获得绿色服务溢价和客户粘性", "S007", "simulated", "绿色价值回流公司"),
        edge("N032", "N012", "technology_collaboration", 3, "2024", "设备接入", "运维成本", "提升设备运行数据采集质量", "S004", "simulated", "设备供应商支撑数据采集"),
        edge("N032", "N007", "technology_collaboration", 3, "2025", "储能接入", "柔性成本", "支撑储能设备建设和运维", "S005", "simulated", "设备供应商支撑储能能力"),
        edge("N033", "N030", "technology_collaboration", 5, "2025", "AIDC", "协调成本", "把算力需求导入能源服务场景", "S007", "industry", "算力生态伙伴连接客户需求"),
        edge("N033", "N018", "technology_collaboration", 4, "2026", "收益优化", "交易成本", "将算力需求特征纳入收益模型", "S007", "industry", "算力生态反馈交易收益模型"),
        edge("N033", "N004", "technology_collaboration", 3, "2025", "零碳园区", "协调成本", "共同建设算电协同场景", "S007", "simulated", "生态伙伴与园区平台连接"),
        edge("N034", "N002", "dispatch", 3, "2025", "地方协同", "协调成本", "协助地方资源接入虚拟电厂", "S006", "industry", "地方平台降低资源协调成本"),
        edge("N034", "N025", "market_trade", 3, "2025", "绿电交易", "绿色合规成本", "连接区域绿电供给和客户需求", "S005", "industry", "地方平台支撑绿电交易"),
        edge("N034", "N023", "market_trade", 3, "2025", "电力现货", "交易成本", "提供区域市场价格和交易入口", "S006", "industry", "地方市场规则影响交易"),
        edge("N034", "N004", "technology_collaboration", 3, "2025", "零碳园区", "协调成本", "推动区域园区综合能源管理", "S006", "simulated", "地方平台支撑园区服务"),
        edge("N012", "N038", "data_flow", 3, "2027", "流程创新", "运维成本", "把设备数据沉淀为运维流程", "S004", "company", "数据化运维流程降低风险"),
        edge("N019", "N038", "technology_collaboration", 3, "2027", "算法治理", "运维成本", "用算法评估结果改进流程", "S004", "company", "模型治理反馈流程创新"),
        edge("N038", "N002", "technology_collaboration", 3, "2027", "虚拟电厂", "协调成本", "提升平台安全合规和运维效率", "S004", "simulated", "流程创新反哺平台运营"),
        edge("N038", "N001", "value_share", 2, "2027", "流程创新", "协调成本", "降低跨主体协同和运维风险", "S004", "simulated", "流程创新产生内部管理价值"),
        edge("N018", "N036", "value_share", 4, "2026", "收益优化", "收益分配", "将收益模型结果映射到分成规则", "S004", "company", "收益优化模型支撑价值共享"),
    ]


def validate_nodes(nodes: pd.DataFrame, schema: dict[str, Any], source_ids: set[str]) -> None:
    required = schema["nodes"]["required_columns"]
    missing = [col for col in required if col not in nodes.columns]
    if missing:
        raise ValueError(f"nodes.csv 缺少字段：{missing}")

    valid_types = set(schema["nodes"]["node_type_values"])
    invalid_types = sorted(set(nodes["node_type"]) - valid_types)
    if invalid_types:
        raise ValueError(f"节点类型不在 schema 中：{invalid_types}")

    valid_evidence = set(schema["nodes"]["evidence_level_values"])
    invalid_evidence = sorted(set(nodes["evidence_level"]) - valid_evidence)
    if invalid_evidence:
        raise ValueError(f"节点证据等级不在 schema 中：{invalid_evidence}")

    if nodes["node_id"].duplicated().any():
        raise ValueError("node_id 存在重复")

    missing_sources = sorted(set(nodes["source_id"]) - source_ids)
    if missing_sources:
        raise ValueError(f"节点引用了不存在的来源编号：{missing_sources}")


def validate_edges(edges: pd.DataFrame, nodes: pd.DataFrame, schema: dict[str, Any], source_ids: set[str]) -> None:
    required = schema["edges"]["required_columns"]
    missing = [col for col in required if col not in edges.columns]
    if missing:
        raise ValueError(f"edges.csv 缺少字段：{missing}")

    node_ids = set(nodes["node_id"])
    missing_nodes = sorted((set(edges["source"]) | set(edges["target"])) - node_ids)
    if missing_nodes:
        raise ValueError(f"边表引用了不存在的节点：{missing_nodes}")

    valid_types = set(schema["edges"]["edge_type_values"])
    invalid_types = sorted(set(edges["edge_type"]) - valid_types)
    if invalid_types:
        raise ValueError(f"边类型不在 schema 中：{invalid_types}")

    low, high = schema["edges"]["weight_range"]
    if not edges["weight"].between(low, high).all():
        bad = edges.loc[~edges["weight"].between(low, high), ["source", "target", "weight"]]
        raise ValueError(f"边权重超出范围：{bad.to_dict(orient='records')}")

    valid_evidence = set(schema["nodes"]["evidence_level_values"])
    invalid_evidence = sorted(set(edges["evidence_level"]) - valid_evidence)
    if invalid_evidence:
        raise ValueError(f"边证据等级不在 schema 中：{invalid_evidence}")

    missing_sources = sorted(set(edges["evidence_source"]) - source_ids)
    if missing_sources:
        raise ValueError(f"边引用了不存在的来源编号：{missing_sources}")


def build_data_dictionary(nodes: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("nodes", "node_id", "string", "节点唯一编号", "N001-N999"),
        ("nodes", "node_name", "string", "节点中文名称", "自由文本"),
        ("nodes", "node_type", "category", "节点类型", "company/platform/resource/capability/market/customer/policy/partner"),
        ("nodes", "stage", "category", "节点首次或主要对应阶段", "all/2024/2025/2026/2027"),
        ("nodes", "value_role", "category", "价值创造角色", "资源、调度、市场连接、客户需求、价值分配等角色"),
        ("nodes", "cost_role", "category", "成本管理角色", "energy_cost/dispatch_cost/transaction_cost/coordination_cost 等"),
        ("nodes", "evidence_level", "category", "节点证据等级", "official/company/industry/media/simulated"),
        ("nodes", "source_id", "string", "节点主要来源编号", "对应 source_manifest.csv 的 source_id"),
        ("nodes", "note", "string", "节点说明", "说明公开资料依据或模拟边界"),
        ("edges", "source", "string", "起点节点编号", "必须存在于 nodes.node_id"),
        ("edges", "target", "string", "终点节点编号", "必须存在于 nodes.node_id"),
        ("edges", "edge_type", "category", "关系类型", "energy_supply/data_flow/dispatch/market_trade/technology_collaboration/policy_constraint/value_share"),
        ("edges", "weight", "integer", "相对重要性权重", "1-5，非真实交易金额"),
        ("edges", "stage", "category", "关系对应阶段", "all/2024/2025/2026/2027"),
        ("edges", "scenario", "category", "业务场景", "虚拟电厂/绿电交易/AIDC/零碳园区等"),
        ("edges", "cost_mechanism", "category", "成本管理机制", "能源成本/调度成本/交易成本/协调成本/绿色合规成本/收益分配等"),
        ("edges", "value_outcome", "string", "价值结果", "稳定供能、调节收益、绿色溢价、客户粘性等"),
        ("edges", "evidence_source", "string", "边关系证据来源编号", "对应 source_manifest.csv 的 source_id"),
        ("edges", "evidence_level", "category", "边关系证据等级", "official/company/industry/media/simulated"),
        ("edges", "note", "string", "边关系说明", "说明公开资料依据、行业逻辑或模拟边界"),
    ]

    dictionary = pd.DataFrame(rows, columns=["table_name", "field_name", "data_type", "definition", "allowed_values"])
    used_columns = {
        "nodes": set(nodes.columns),
        "edges": set(edges.columns),
    }
    dictionary["is_in_dataset"] = dictionary.apply(
        lambda row: row["field_name"] in used_columns[row["table_name"]],
        axis=1,
    )
    return dictionary


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    schema = load_schema()
    source_ids = load_source_ids()

    nodes = pd.DataFrame(build_nodes())
    edges = pd.DataFrame(build_edges())
    edges["weight"] = edges["weight"].astype(int)

    validate_nodes(nodes, schema, source_ids)
    validate_edges(edges, nodes, schema, source_ids)

    dictionary = build_data_dictionary(nodes, edges)

    nodes.to_csv(NODES_PATH, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
    edges.to_csv(EDGES_PATH, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)
    dictionary.to_csv(DICTIONARY_PATH, index=False, encoding="utf-8-sig", quoting=csv.QUOTE_MINIMAL)

    print(f"已生成：{NODES_PATH.relative_to(PROJECT_ROOT)}（{len(nodes)} 个节点）")
    print(f"已生成：{EDGES_PATH.relative_to(PROJECT_ROOT)}（{len(edges)} 条边）")
    print(f"已生成：{DICTIONARY_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
