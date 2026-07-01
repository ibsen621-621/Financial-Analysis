"""指标计算引擎：所有口径集中在此，禁止散落到别处。"""
from __future__ import annotations
from typing import Dict, Any


def _g(d: Dict[str, Any], key: str, default: float = 0.0) -> float:
    v = d.get(key)
    return float(v) if v is not None else default


def core_profit(y: Dict[str, Any]) -> float:
    return (
        _g(y, "revenue")
        - _g(y, "cogs")
        - _g(y, "taxes_surcharges")
        - _g(y, "selling_exp")
        - _g(y, "admin_exp")
        - _g(y, "rd_exp")
        - _g(y, "operating_interest_exp")
        + _g(y, "other_income")
    )


def safe_div(a: float, b: float):
    return a / b if b not in (0, 0.0, None) else None


def compute_year(y: Dict[str, Any]) -> Dict[str, Any]:
    rev = _g(y, "revenue")
    cp = core_profit(y)
    gross = rev - _g(y, "cogs")

    return {
        "core_profit": round(cp, 4),
        "core_profit_margin": safe_div(cp, rev),
        "gross_margin": safe_div(gross, rev),
        "cash_conversion": safe_div(_g(y, "cfo"), cp),
        "cfo_to_net_profit": safe_div(_g(y, "cfo"), _g(y, "net_profit")),
        "selling_exp_ratio": safe_div(_g(y, "selling_exp"), rev),
        "admin_exp_ratio": safe_div(_g(y, "admin_exp"), rev),
        "rd_exp_ratio": safe_div(_g(y, "rd_exp"), rev),
        "ar_to_rev": safe_div(_g(y, "ar"), rev),
        "inv_to_cogs": safe_div(_g(y, "inventory"), _g(y, "cogs")),
        "cash_ratio": safe_div(_g(y, "cash"), _g(y, "total_assets")),
        "debt_ratio": safe_div(_g(y, "short_debt") + _g(y, "long_debt"), _g(y, "total_assets")),
        "fin_exp_ratio": safe_div(_g(y, "financial_exp"), rev),
        "cip_ratio": safe_div(_g(y, "cip"), _g(y, "total_assets")),
        "goodwill_to_equity": safe_div(_g(y, "goodwill"), _g(y, "total_equity")),
        "goodwill_to_core_profit": safe_div(_g(y, "goodwill"), cp),
        "op_vs_inv_assets": safe_div(_g(y, "operating_assets"), _g(y, "investing_assets")),
        "ap_vs_inventory": safe_div(_g(y, "ap"), _g(y, "inventory")),
        "capex_intensity": safe_div(_g(y, "capex"), rev),
        "dividend_payout": safe_div(_g(y, "dividend_paid"), _g(y, "net_profit")),
        "non_recurring_ratio": safe_div(_g(y, "non_recurring_pnl"), _g(y, "net_profit")),
        "ar_provision_coverage": safe_div(_g(y, "ar_provision"), _g(y, "ar_aging_over_2y")),
    }


def compute_all(data: Dict[str, Any], years) -> Dict[str, Any]:
    out = {}
    for yr in years:
        key = str(yr)
        if key in data:
            out[key] = compute_year(data[key])
    return out
