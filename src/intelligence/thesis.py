from __future__ import annotations

from typing import Any


def _module_map(bundle: dict) -> dict[str, dict]:
    return {module["name"]: module for module in bundle.get("modules", [])}


def _metric(modules: dict[str, dict], module: str, key: str, default: Any = None) -> Any:
    return modules.get(module, {}).get("metrics", {}).get(key, default)


def build_anomalies(bundle: dict) -> list[dict]:
    """Surface deterministic conflicts without invoking an LLM."""
    modules = _module_map(bundle)
    anomalies: list[dict] = []
    change = float(bundle.get("market", {}).get("change_24h_pct") or 0)
    imbalance = _metric(modules, "order_flow", "imbalance_pct")
    funding = _metric(modules, "leverage", "funding_rate_pct")
    security = modules.get("security", {})

    if imbalance is not None and change * float(imbalance) < -25:
        anomalies.append({
            "type": "price_flow_divergence",
            "severity": "high",
            "detail": "Price direction conflicts with resting order-book pressure.",
        })
    if funding is not None and abs(float(funding)) > 0.08:
        anomalies.append({
            "type": "funding_extreme",
            "severity": "high",
            "detail": "Perpetual funding is outside the reference neutral zone.",
        })
    if security.get("classification") == "elevated_flags":
        anomalies.append({
            "type": "security_gate",
            "severity": "high",
            "detail": "Observable contract/network controls require additional review.",
        })
    return anomalies


def build_thesis(bundle: dict, consensus: dict, flow_state: dict) -> dict:
    """Build a bounded deterministic thesis contract for downstream UI/AI explanation."""
    modules = _module_map(bundle)
    technical = modules.get("technical", {}).get("metrics", {})
    support = technical.get("support_level")
    resistance = technical.get("resistance_level")

    confirmation = []
    invalidation = []
    if resistance is not None:
        confirmation.append(f"Sustained acceptance above {resistance}")
    else:
        confirmation.append("Resistance confirmation unavailable")
    if support is not None:
        invalidation.append(f"Sustained loss of {support}")
    else:
        invalidation.append("Support invalidation unavailable")

    confirmation.append("Directional evidence remains aligned without leverage-stress escalation.")
    invalidation.append("Price/order-flow conflict persists while risk gates worsen.")

    return {
        "posture": consensus.get("posture"),
        "posture_score": consensus.get("posture_score"),
        "regime": flow_state.get("regime"),
        "summary": (
            f"Reference posture is {consensus.get('posture')} with FlowState "
            f"regime {flow_state.get('regime')}."
        ),
        "confirmation": confirmation,
        "invalidation": invalidation,
        "horizon": bundle.get("horizon"),
        "disclaimer": "Evidence conditions are research context, not an instruction to trade.",
    }
