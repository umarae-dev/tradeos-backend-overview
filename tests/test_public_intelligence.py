from datetime import datetime, timedelta, timezone

from src.evidence.consensus import deterministic_consensus
from src.evidence.roles import stance_from_classification
from src.intelligence.flow_state import build_flow_shift
from src.intelligence.market_twin import match_market_twin


def test_context_and_risk_modules_do_not_fake_directional_votes():
    bundle = {
        "modules": [
            {"name": "technical", "role": "directional", "status": "available", "classification": "bullish", "stance": "bullish", "coverage": 1.0, "strength": 80},
            {"name": "security", "role": "risk_gate", "status": "available", "classification": "elevated_flags", "coverage": 1.0, "strength": 90},
            {"name": "news_context", "role": "context", "status": "available", "classification": "active", "coverage": 0.8, "strength": 50},
        ]
    }
    result = deterministic_consensus(bundle)
    assert result["directional_sources"] == 1
    assert result["risk_gates"] == 1
    assert result["context_sources"] == 1
    assert result["bullish_count"] == 1
    assert result["bearish_count"] == 0


def test_module_semantics_are_not_global_keyword_scoring():
    assert stance_from_classification("technical", "bullish") == "bullish"
    assert stance_from_classification("security", "elevated_flags") == "neutral"
    assert stance_from_classification("on_chain", "high") == "neutral"


def test_flow_shift_detects_large_dimension_change():
    previous = {"regime": "Balanced Transition", "dimensions": [{"name": "Fresh Capital", "score": 40}]}
    current = {"regime": "Balanced Transition", "dimensions": [{"name": "Fresh Capital", "score": 60}]}
    result = build_flow_shift(current, previous)
    assert result["changed"] is True
    assert result["largest_dimension_shift"]["delta"] == 20.0


def test_market_twin_rejects_future_only_history():
    now = datetime.now(timezone.utc)
    current = {
        "change_4h": 1.0,
        "change_24h": 2.0,
        "change_7d": 3.0,
        "momentum": 1.0,
        "volatility": 2.0,
        "recovery": 1.0,
        "trend_efficiency": 50.0,
        "range_position": 60.0,
        "funding": 0.01,
    }
    snapshots = [
        {"observed_at": now + timedelta(days=1), "price": 100, "features": current}
    ]
    result = match_market_twin(current_vector=current, current_time=now, snapshots=snapshots, minimum_analogues=1)
    assert result["status"] == "collecting_history"
    assert result["analogue_count"] == 0
