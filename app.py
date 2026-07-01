"""FastAPI 服务：Gemini Gem 通过 Function Calling 调用本接口。"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from engine.metrics import compute_all
from engine.diagnosis import run_rules, cross_check, final_view
from engine.report import render_one_pager

app = FastAPI(title="三表穿透分析 API", version="2.0")


class AnalyzeRequest(BaseModel):
    company: str
    years: List[int]
    data: Dict[str, Any]
    industry_benchmark: Optional[Dict[str, Any]] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    metrics = compute_all(req.data, req.years)
    risks = run_rules(metrics)
    cross_notes = cross_check(metrics, req.data)
    verdict = final_view(risks)
    report_md = render_one_pager(req.company, metrics, risks, cross_notes, verdict)
    return {
        "company": req.company,
        "scorecard": metrics,
        "risks": risks,
        "cross_check": cross_notes,
        "final_view": verdict,
        "report_markdown": report_md,
    }
