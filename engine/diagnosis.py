"""三表联动诊断与规则触发。"""
from __future__ import annotations
from typing import Dict, Any, List


def _trend_up(series: List[float]) -> bool:
    vals = [v for v in series if v is not None]
    return len(vals) >= 2 and vals[-1] > vals[0]


def _series(metrics: Dict[str, Any], key: str) -> List[float]:
    return [metrics[y].get(key) for y in sorted(metrics.keys())]


def run_rules(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    risks: List[Dict[str, Any]] = []
    yrs = sorted(metrics.keys())
    if not yrs:
        return risks
    last = metrics[yrs[-1]]

    # R1 四高
    if all([
        (last.get("cash_ratio") or 0) >= 0.20,
        (last.get("debt_ratio") or 0) >= 0.25,
        (last.get("fin_exp_ratio") or 0) >= 0.02,
        (last.get("cip_ratio") or 0) >= 0.10,
    ]):
        risks.append({"id": "R1_four_high", "level": "high",
                      "evidence": f"{yrs[-1]}: 高现金+高负债+高财务费用+高在建工程并存"})

    # R2 失血式增长
    cc = _series(metrics, "cash_conversion")[-2:]
    if len(cc) == 2 and all(v is not None and v < 0.8 for v in cc):
        risks.append({"id": "R2_bleeding_growth", "level": "high",
                      "evidence": f"获现率连续<0.8: {cc}"})

    # R3 纸面利润
    cpm = _series(metrics, "core_profit_margin")
    if len(cpm) >= 2 and cpm[0] is not None and cpm[-1] is not None and cpm[-1] < cpm[0]:
        nr = last.get("non_recurring_ratio")
        if nr is not None and nr >= 0.30:
            risks.append({"id": "R3_paper_profit", "level": "medium",
                          "evidence": f"核心利润率下行且非经常性损益占比{round(nr,2)}"})

    # R4 渠道压货
    if _trend_up(_series(metrics, "ar_to_rev")) and _trend_up(_series(metrics, "inv_to_cogs")):
        if (last.get("cash_conversion") or 1) < 1:
            risks.append({"id": "R4_channel_stuffing", "level": "medium",
                          "evidence": "应收/收入与存货/成本双升且获现率<1"})

    # R5 商誉
    if (last.get("goodwill_to_equity") or 0) >= 0.30 and (last.get("goodwill_to_core_profit") or 0) >= 3.0:
        risks.append({"id": "R5_goodwill_risk", "level": "high",
                      "evidence": f"商誉/净资产{round(last.get('goodwill_to_equity'),2)}，商誉/核心利润高"})

    # R6 分红再融资错配
    if (last.get("dividend_payout") or 0) >= 0.50:
        risks.append({"id": "R6_capital_mismatch", "level": "medium",
                      "evidence": f"分红率{round(last.get('dividend_payout'),2)}，需核对同期再融资"})

    # R7 减值不足
    cov = last.get("ar_provision_coverage")
    if cov is not None and cov < 0.30:
        risks.append({"id": "R7_provision_insufficient", "level": "high",
                      "evidence": f"2年以上应收坏账覆盖率仅{round(cov,2)}"})

    return risks


def cross_check(metrics: Dict[str, Any], data: Dict[str, Any]) -> List[str]:
    notes = []
    yrs = sorted(metrics.keys())
    if len(yrs) < 2:
        return notes
    rev = [data[y].get("revenue") for y in yrs]
    ta = [data[y].get("total_assets") for y in yrs]
    np = [data[y].get("net_profit") for y in yrs]
    cfo = [data[y].get("cfo") for y in yrs]

    if ta[-1] and ta[0] and rev[-1] and rev[0] and ta[-1] > ta[0] and rev[-1] <= rev[0]:
        notes.append("资产增长但收入未增 → 资产配置效率低或存在闲置。")
    if rev[-1] and rev[0] and np[-1] and np[0] and rev[-1] > rev[0] and np[-1] <= np[0]:
        notes.append("收入增长但利润未增 → 成本费用失控或价格战让利。")
    if np[-1] and np[0] and cfo[-1] and cfo[0] and np[-1] > np[0] and cfo[-1] <= cfo[0]:
        notes.append("利润增长但经营现金流未增 → 收款质量差，警惕无现金危机。")
    return notes


def final_view(risks: List[Dict[str, Any]]) -> str:
    highs = sum(1 for r in risks if r["level"] == "high")
    mids = sum(1 for r in risks if r["level"] == "medium")
    if highs >= 2:
        return "回避"
    if highs == 1:
        return "谨慎"
    if mids >= 2:
        return "观察"
    return "稳健"
