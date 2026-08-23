from src.intelligence.pipeline import run_reference_analysis


def _sample():
    return {
        "symbol": "BNB",
        "horizon": "swing",
        "market": {
            "current_price": 800,
            "change_24h_pct": 2.5,
            "momentum_pct": 1.2,
            "support_level": 760,
            "resistance_level": 825,
        },
        "price_structure": {"trend": "uptrend"},
        "liquidity": {"volume_to_mcap_pct": 6.0},
        "order_flow": {"imbalance_pct": 12.0},
        "leverage": {"funding_rate_pct": 0.01, "open_interest": 100},
        "risk": {"volatility_7d_pct": 4.0},
        "news_context": {"headline_count": 5},
        "macro": {"fear_greed_label": "greed", "fear_greed_value": 67},
        "project": {"market_cap_rank": 5, "circulating_supply": 80, "max_supply": 100},
        "security": {"is_honeypot": False, "owner_can_change_balance": False},
        "on_chain": {"network_activity": "high", "transactions_24h": 1000000},
        "derivatives": {
            "options": {"put_call_open_interest_ratio": 0.8},
            "stablecoin_flow": {"change_7d_pct": 0.4},
        },
    }


def test_pipeline_builds_all_twelve_modules():
    result = run_reference_analysis(_sample())
    assert result["symbol"] == "BNB"
    assert len(result["evidence"]["modules"]) == 12
    assert result["consensus"]["evidence_total"] == 12
    assert result["public_reference"] is True


def test_context_and_risk_gates_do_not_become_directional_votes():
    result = run_reference_analysis(_sample())
    roles = {m["name"]: m["role"] for m in result["evidence"]["modules"]}
    assert roles["news_context"] == "context"
    assert roles["project"] == "context"
    assert roles["risk"] == "risk_gate"
    assert roles["security"] == "risk_gate"


def test_missing_data_remains_explicitly_unavailable():
    result = run_reference_analysis({"symbol": "TEST", "market": {"current_price": 1}})
    modules = {m["name"]: m for m in result["evidence"]["modules"]}
    assert modules["order_flow"]["status"] == "unavailable"
    assert modules["derivatives"]["status"] == "unavailable"
    assert result["consensus"]["unavailable_count"] > 0


def test_security_flags_surface_as_anomaly_not_directional_prediction():
    data = _sample()
    data["security"]["is_honeypot"] = True
    result = run_reference_analysis(data)
    assert any(item["type"] == "security_gate" for item in result["anomalies"])
    security = next(m for m in result["evidence"]["modules"] if m["name"] == "security")
    assert security["role"] == "risk_gate"
    assert security["stance"] == "neutral"
