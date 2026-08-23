from __future__ import annotations

from typing import Final

EVIDENCE_ROLES: Final[dict[str, str]] = {
    "technical": "directional",
    "price_structure": "directional",
    "liquidity": "directional",
    "order_flow": "directional",
    "leverage": "directional",
    "derivatives": "directional",
    "macro": "directional",
    "news_context": "context",
    "project": "context",
    "on_chain": "context",
    "risk": "risk_gate",
    "security": "risk_gate",
}


def evidence_role(module_name: str) -> str:
    """Return the public semantic role for an evidence module."""
    return EVIDENCE_ROLES.get(module_name, "context")


def stance_from_classification(module_name: str, classification: str, *, available: bool = True) -> str:
    """Reference stance mapping.

    This deliberately demonstrates the Zynost principle that module semantics
    matter: the same adjective must not be interpreted globally across market,
    risk and network data. Production tuning remains private.
    """
    if not available or classification == "unavailable":
        return "unavailable"
    if evidence_role(module_name) != "directional":
        return "neutral"

    normalized = classification.lower().strip()
    bullish = {
        "technical": {"bullish"},
        "price_structure": {"uptrend"},
        "liquidity": {"deep"},
        "order_flow": {"bid_dominant"},
        "macro": {"greed"},
        "derivatives": {"call_heavy"},
    }
    bearish = {
        "technical": {"bearish"},
        "price_structure": {"downtrend"},
        "liquidity": {"thin"},
        "order_flow": {"ask_dominant"},
        "leverage": {"stretched"},
        "macro": {"fear", "extreme_fear", "fearful"},
        "derivatives": {"defensive"},
    }

    if normalized in bullish.get(module_name, set()):
        return "bullish"
    if normalized in bearish.get(module_name, set()):
        return "bearish"
    return "neutral"
