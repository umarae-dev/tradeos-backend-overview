from src.evidence.consensus import deterministic_consensus
from src.intelligence.flow_state import build_flow_state


bundle = {
    "market": {"change_24h_pct": 2.4},
    "modules": [
        {"name": "technical", "role": "directional", "status": "available", "classification": "bullish", "stance": "bullish", "coverage": 1.0, "strength": 75, "metrics": {}},
        {"name": "price_structure", "role": "directional", "status": "available", "classification": "uptrend", "stance": "bullish", "coverage": 1.0, "strength": 70, "metrics": {}},
        {"name": "liquidity", "role": "directional", "status": "available", "classification": "deep", "stance": "bullish", "coverage": 0.9, "strength": 65, "metrics": {"volume_to_mcap_pct": 6.2}},
        {"name": "order_flow", "role": "directional", "status": "available", "classification": "bid_dominant", "stance": "bullish", "coverage": 0.9, "strength": 68, "metrics": {"imbalance_pct": 11.0}},
        {"name": "leverage", "role": "directional", "status": "available", "classification": "controlled", "stance": "neutral", "coverage": 0.85, "strength": 55, "metrics": {"funding_rate_pct": 0.01}},
        {"name": "derivatives", "role": "directional", "status": "available", "classification": "balanced", "stance": "neutral", "coverage": 0.8, "strength": 50, "metrics": {"stablecoin_flow": {"change_7d_pct": 0.5}}},
        {"name": "risk", "role": "risk_gate", "status": "available", "classification": "medium", "stance": "neutral", "coverage": 1.0, "strength": 60, "metrics": {}},
        {"name": "security", "role": "risk_gate", "status": "available", "classification": "no_critical_flag_observed", "stance": "neutral", "coverage": 0.9, "strength": 55, "metrics": {}},
        {"name": "project", "role": "context", "status": "available", "classification": "established", "stance": "neutral", "coverage": 0.75, "strength": 60, "metrics": {"circulating_supply": 80, "max_supply": 100}},
    ],
}

print("Consensus:")
print(deterministic_consensus(bundle))
print("\nFlowState:")
print(build_flow_state(bundle))
