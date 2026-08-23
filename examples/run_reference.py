from pprint import pprint

from src.intelligence.pipeline import run_reference_analysis


observations = {
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

pprint(run_reference_analysis(observations), sort_dicts=False)
