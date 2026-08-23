from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.intelligence.pipeline import run_reference_analysis


app = FastAPI(
    title="Zynost Public Intelligence Reference",
    version="1.0.0",
    description="Deterministic, evidence-first crypto intelligence reference implementation.",
)


class AnalysisRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    horizon: str = Field(default="swing", max_length=20)
    observed_at: str | None = None
    market: dict = Field(default_factory=dict)
    price_structure: dict = Field(default_factory=dict)
    liquidity: dict = Field(default_factory=dict)
    order_flow: dict = Field(default_factory=dict)
    leverage: dict = Field(default_factory=dict)
    risk: dict = Field(default_factory=dict)
    news_context: dict = Field(default_factory=dict)
    macro: dict = Field(default_factory=dict)
    project: dict = Field(default_factory=dict)
    security: dict = Field(default_factory=dict)
    on_chain: dict = Field(default_factory=dict)
    derivatives: dict = Field(default_factory=dict)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "zynost-public-intelligence-reference"}


@app.post("/analyze")
def analyze(payload: AnalysisRequest) -> dict:
    data = payload.model_dump(exclude_none=True)
    return run_reference_analysis(data)
