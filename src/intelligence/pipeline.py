from __future__ import annotations

from typing import Any

from src.evidence.builder import build_reference_bundle
from src.evidence.consensus import deterministic_consensus
from .flow_state import build_flow_state
from .thesis import build_anomalies, build_thesis


def run_reference_analysis(observations: dict[str, Any]) -> dict[str, Any]:
    """Run the complete public deterministic Zynost reference pipeline."""
    bundle = build_reference_bundle(observations)
    consensus = deterministic_consensus(bundle)
    flow_state = build_flow_state(bundle)
    anomalies = build_anomalies(bundle)
    thesis = build_thesis(bundle, consensus, flow_state)

    return {
        "symbol": bundle["symbol"],
        "horizon": bundle["horizon"],
        "observed_at": bundle["observed_at"],
        "evidence": bundle,
        "consensus": consensus,
        "flow_state": flow_state,
        "anomalies": anomalies,
        "thesis": thesis,
        "disclaimer": "Research tooling only. No output is a guarantee of future performance or financial advice.",
        "public_reference": True,
    }
