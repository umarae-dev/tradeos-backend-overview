from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Literal

EvidenceRole = Literal["directional", "context", "risk_gate"]
EvidenceStatus = Literal["available", "unavailable"]
EvidenceStance = Literal["bullish", "bearish", "neutral", "unavailable"]


@dataclass(frozen=True)
class EvidenceModule:
    """Public, provider-agnostic representation of one decision-evidence module.

    This schema mirrors the shape used by the Zynost evidence-first architecture
    without exposing production provider credentials, proprietary thresholds or
    private tuning.
    """

    name: str
    role: EvidenceRole
    status: EvidenceStatus
    classification: str
    stance: EvidenceStance
    coverage: float
    strength: float | None
    source_class: str
    observed_at: str
    metrics: dict[str, Any]
    explanation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def unavailable_module(*, name: str, role: EvidenceRole, observed_at: str) -> EvidenceModule:
    """Return an explicit unavailable module rather than fabricating a neutral signal."""
    return EvidenceModule(
        name=name,
        role=role,
        status="unavailable",
        classification="unavailable",
        stance="unavailable",
        coverage=0.0,
        strength=None,
        source_class="unavailable",
        observed_at=observed_at,
        metrics={},
        explanation="Reliable public coverage is not available for this module.",
    )
