"""将计算结果渲染为一页报告。"""
from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path

try:
    from jinja2 import Template
except ImportError:
    Template = None


def render_one_pager(company: str, metrics: Dict[str, Any],
                     risks: List[Dict[str, Any]], cross_notes: List[str],
                     verdict: str) -> str:
    tpl_path = Path(__file__).resolve().parent.parent / "templates" / "one_pager.md.j2"
    text = tpl_path.read_text(encoding="utf-8")
    ctx = {
        "company": company,
        "years": sorted(metrics.keys()),
        "metrics": metrics,
        "risks": risks,
        "cross_notes": cross_notes,
        "verdict": verdict,
    }
    if Template:
        return Template(text).render(**ctx)
    # 无 jinja2 时的降级渲染
    lines = [f"# {company} 三表穿透分析", f"最终判断: {verdict}", "", "## 风险清单"]
    for r in risks:
        lines.append(f"- [{r['level']}] {r['id']}: {r['evidence']}")
    lines += ["", "## 三表勾稽"] + [f"- {n}" for n in cross_notes]
    return "\n".join(lines)
