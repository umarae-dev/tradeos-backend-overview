from __future__ import annotations

from .roles import evidence_role, stance_from_classification


def _clamp(value: float, lower: float = 0.0, upper: float = 100.0) -> float:
    return max(lower, min(upper, value))


def deterministic_consensus(bundle: dict) -> dict:
    """Public deterministic consensus implementation.

    Directional evidence votes on posture. Context and risk-gate modules remain
    visible without being incorrectly converted into directional votes.
    """
    modules = bundle.get("modules", [])
    available = [m for m in modules if m.get("status") == "available"]
    directional = [m for m in available if (m.get("role") or evidence_role(m.get("name", ""))) == "directional"]
    context = [m for m in available if (m.get("role") or evidence_role(m.get("name", ""))) == "context"]
    risk_gates = [m for m in available if (m.get("role") or evidence_role(m.get("name", ""))) == "risk_gate"]

    stances = [
        m.get("stance")
        or stance_from_classification(
            m.get("name", ""),
            m.get("classification", ""),
            available=True,
        )
        for m in directional
    ]
    bulls = stances.count("bullish")
    bears = stances.count("bearish")

    weights = [
        max(
            0.05,
            float(m.get("coverage") or 0)
            * max(0.25, float(m.get("strength") or 0) / 100),
        )
        for m in directional
    ]
    signed = [1 if stance == "bullish" else -1 if stance == "bearish" else 0 for stance in stances]

    posture_score = 50.0
    if weights:
        posture_score += 50 * sum(value * weight for value, weight in zip(signed, weights)) / sum(weights)
    posture_score = round(_clamp(posture_score), 1)
    posture = "bullish" if posture_score >= 58 else "bearish" if posture_score <= 42 else "neutral"

    directional_confidence = (
        sum(float(m.get("strength") or 0) * float(m.get("coverage") or 0) for m in directional)
        / max(1, len(directional))
    )

    return {
        "evidence_available": len(available),
        "evidence_total": len(modules),
        "directional_sources": len(directional),
        "context_sources": len(context),
        "risk_gates": len(risk_gates),
        "bullish_count": bulls,
        "bearish_count": bears,
        "neutral_count": max(0, len(directional) - bulls - bears),
        "unavailable_count": max(0, len(modules) - len(available)),
        "posture": posture,
        "posture_score": posture_score,
        "confidence": round(directional_confidence, 1),
        "formula_version": "public-consensus-1.0.0",
    }
