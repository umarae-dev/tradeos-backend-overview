from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .model import EvidenceModule, unavailable_module
from .roles import evidence_role, stance_from_classification


# These thresholds are intentionally public reference defaults, not the
# proprietary production tuning used by Zynost. They make the OSS package
# independently runnable and auditable without exposing commercial IP.
REFERENCE_THRESHOLDS = {
    "momentum_pct": 0.5,
    "order_imbalance_pct": 8.0,
    "funding_stretched_pct": 0.08,
    "volatility_high_pct": 8.0,
    "liquidity_deep_turnover_pct": 5.0,
}

MODULE_NAMES = (
    "technical",
    "price_structure",
    "liquidity",
    "order_flow",
    "leverage",
    "risk",
    "news_context",
    "macro",
    "project",
    "security",
    "on_chain",
    "derivatives",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _available(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (dict, list, tuple, set, str)):
        return bool(value)
    return True


def _module(
    *,
    name: str,
    metrics: dict[str, Any] | None,
    classification: str,
    coverage: float,
    strength: float,
    source_class: str,
    explanation: str,
    observed_at: str,
) -> EvidenceModule:
    if not metrics or coverage <= 0:
        return unavailable_module(name=name, role=evidence_role(name), observed_at=observed_at)
    stance = stance_from_classification(name, classification, available=True)
    return EvidenceModule(
        name=name,
        role=evidence_role(name),
        status="available",
        classification=classification,
        stance=stance,
        coverage=round(max(0.0, min(1.0, coverage)), 2),
        strength=round(max(0.0, min(100.0, strength)), 1),
        source_class=source_class,
        observed_at=observed_at,
        metrics=metrics,
        explanation=explanation,
    )


def build_reference_bundle(observations: dict[str, Any]) -> dict[str, Any]:
    """Normalize public observations into Zynost's 12-module evidence contract.

    The builder is deterministic and provider-agnostic. Callers may feed it
    exchange data, BNB Chain data, stored fixtures, or their own adapters.
    Missing evidence is explicitly marked unavailable rather than fabricated.
    """
    symbol = str(observations.get("symbol") or "UNKNOWN").upper().strip()
    horizon = str(observations.get("horizon") or "swing")
    observed_at = str(observations.get("observed_at") or _now())
    market = dict(observations.get("market") or {})

    momentum = market.get("momentum_pct")
    technical_metrics = {
        key: market[key]
        for key in (
            "current_price",
            "change_4h_pct",
            "change_24h_pct",
            "change_7d_pct",
            "momentum_pct",
            "support_level",
            "resistance_level",
            "trend_efficiency_pct",
            "range_position_pct",
        )
        if market.get(key) is not None
    }
    if momentum is None:
        technical_classification = "balanced"
    elif float(momentum) > REFERENCE_THRESHOLDS["momentum_pct"]:
        technical_classification = "bullish"
    elif float(momentum) < -REFERENCE_THRESHOLDS["momentum_pct"]:
        technical_classification = "bearish"
    else:
        technical_classification = "balanced"

    structure = dict(observations.get("price_structure") or {})
    structure_classification = str(structure.get("trend") or "ranging")

    liquidity = dict(observations.get("liquidity") or {})
    turnover = liquidity.get("volume_to_mcap_pct")
    if turnover is None:
        liquidity_classification = "unknown"
    elif float(turnover) >= REFERENCE_THRESHOLDS["liquidity_deep_turnover_pct"]:
        liquidity_classification = "deep"
    elif float(turnover) <= 1.0:
        liquidity_classification = "thin"
    else:
        liquidity_classification = "moderate"

    order_flow = dict(observations.get("order_flow") or {})
    imbalance = order_flow.get("imbalance_pct")
    if imbalance is None:
        order_classification = "balanced"
    elif float(imbalance) > REFERENCE_THRESHOLDS["order_imbalance_pct"]:
        order_classification = "bid_dominant"
    elif float(imbalance) < -REFERENCE_THRESHOLDS["order_imbalance_pct"]:
        order_classification = "ask_dominant"
    else:
        order_classification = "balanced"

    leverage = dict(observations.get("leverage") or {})
    funding = leverage.get("funding_rate_pct")
    if funding is None:
        leverage_classification = "controlled"
    elif abs(float(funding)) >= REFERENCE_THRESHOLDS["funding_stretched_pct"]:
        leverage_classification = "stretched"
    elif float(funding) < -0.03:
        leverage_classification = "short_heavy"
    else:
        leverage_classification = "controlled"

    risk = dict(observations.get("risk") or {})
    volatility = risk.get("volatility_7d_pct", market.get("volatility_7d_pct"))
    if volatility is None:
        risk_classification = "unknown"
    elif float(volatility) >= REFERENCE_THRESHOLDS["volatility_high_pct"]:
        risk_classification = "high"
    elif float(volatility) >= 3.0:
        risk_classification = "medium"
    else:
        risk_classification = "low"
    if volatility is not None:
        risk.setdefault("volatility_7d_pct", volatility)

    news = dict(observations.get("news_context") or {})
    headline_count = int(news.get("headline_count") or 0)
    news_classification = "active" if headline_count >= 4 else "quiet"

    macro = dict(observations.get("macro") or {})
    macro_classification = str(macro.get("fear_greed_label") or "neutral").lower().replace(" ", "_")

    project = dict(observations.get("project") or {})
    rank = project.get("market_cap_rank")
    project_classification = "established" if rank is not None and int(rank) <= 100 else "developing"

    security = dict(observations.get("security") or {})
    critical_flags = sum(
        1
        for key in ("is_honeypot", "owner_can_change_balance", "transfer_pausable")
        if security.get(key) is True
    )
    security_classification = "elevated_flags" if critical_flags else "no_critical_flag_observed"

    on_chain = dict(observations.get("on_chain") or {})
    onchain_classification = str(on_chain.get("network_activity") or "observed")

    derivatives = dict(observations.get("derivatives") or {})
    pcr = (derivatives.get("options") or {}).get("put_call_open_interest_ratio")
    if pcr is None:
        derivatives_classification = "balanced"
    elif float(pcr) < 0.75:
        derivatives_classification = "call_heavy"
    elif float(pcr) > 1.1:
        derivatives_classification = "defensive"
    else:
        derivatives_classification = "balanced"

    modules = [
        _module(
            name="technical",
            metrics=technical_metrics or None,
            classification=technical_classification,
            coverage=1.0 if technical_metrics else 0.0,
            strength=65.0 if momentum is not None else 45.0,
            source_class="public_market_observation",
            explanation="Short-horizon price and momentum context from caller-supplied public observations.",
            observed_at=observed_at,
        ),
        _module(
            name="price_structure",
            metrics=structure or None,
            classification=structure_classification,
            coverage=0.9 if structure else 0.0,
            strength=65.0 if structure else 0.0,
            source_class="public_price_structure",
            explanation="Observed swing structure is kept separate from raw momentum.",
            observed_at=observed_at,
        ),
        _module(
            name="liquidity",
            metrics=liquidity or None,
            classification=liquidity_classification,
            coverage=0.9 if liquidity else 0.0,
            strength=65.0 if turnover is not None else 40.0,
            source_class="public_volume_and_market_cap",
            explanation="Turnover and liquidity depth are evaluated as execution context.",
            observed_at=observed_at,
        ),
        _module(
            name="order_flow",
            metrics=order_flow or None,
            classification=order_classification,
            coverage=0.9 if order_flow else 0.0,
            strength=min(90.0, 45.0 + abs(float(imbalance or 0))),
            source_class="public_order_book_snapshot",
            explanation="Top-book imbalance is a snapshot of resting liquidity, not a forecast.",
            observed_at=observed_at,
        ),
        _module(
            name="leverage",
            metrics=leverage or None,
            classification=leverage_classification,
            coverage=0.85 if leverage else 0.0,
            strength=min(90.0, 45.0 + abs(float(funding or 0)) * 300),
            source_class="public_perpetual_futures",
            explanation="Funding and open-interest context identify leverage crowding risk.",
            observed_at=observed_at,
        ),
        _module(
            name="risk",
            metrics=risk or None,
            classification=risk_classification,
            coverage=1.0 if risk else 0.0,
            strength=min(90.0, 40.0 + float(volatility or 0) * 4),
            source_class="public_market_risk",
            explanation="Observed volatility is treated as a risk gate rather than a directional vote.",
            observed_at=observed_at,
        ),
        _module(
            name="news_context",
            metrics=news or None,
            classification=news_classification,
            coverage=0.75 if news else 0.0,
            strength=min(80.0, 35.0 + headline_count * 5),
            source_class="public_news_context",
            explanation="News is context evidence and does not automatically vote on price direction.",
            observed_at=observed_at,
        ),
        _module(
            name="macro",
            metrics=macro or None,
            classification=macro_classification,
            coverage=0.8 if macro else 0.0,
            strength=60.0 if macro else 0.0,
            source_class="public_macro_sentiment",
            explanation="Broad risk appetite is represented separately from asset-specific evidence.",
            observed_at=observed_at,
        ),
        _module(
            name="project",
            metrics=project or None,
            classification=project_classification,
            coverage=0.75 if project else 0.0,
            strength=60.0 if project else 0.0,
            source_class="public_project_metadata",
            explanation="Supply and rank metadata provide context without pretending to score team quality.",
            observed_at=observed_at,
        ),
        _module(
            name="security",
            metrics=security or None,
            classification=security_classification,
            coverage=0.9 if security else 0.0,
            strength=90.0 if critical_flags else 55.0,
            source_class="public_security_observation",
            explanation="Observable contract or network controls are treated as risk gates.",
            observed_at=observed_at,
        ),
        _module(
            name="on_chain",
            metrics=on_chain or None,
            classification=onchain_classification,
            coverage=0.7 if on_chain else 0.0,
            strength=55.0 if on_chain else 0.0,
            source_class="public_on_chain_observation",
            explanation="On-chain activity adds context only when reliable coverage is available.",
            observed_at=observed_at,
        ),
        _module(
            name="derivatives",
            metrics=derivatives or None,
            classification=derivatives_classification,
            coverage=0.8 if derivatives else 0.0,
            strength=60.0 if derivatives else 0.0,
            source_class="public_derivatives_and_positioning",
            explanation="Options, positioning and capital-flow evidence complement spot-market observations.",
            observed_at=observed_at,
        ),
    ]

    return {
        "symbol": symbol,
        "horizon": horizon,
        "observed_at": observed_at,
        "market": market,
        "modules": [module.to_dict() for module in modules],
        "formula_version": "public-evidence-1.0.0",
        "boundary": "reference_defaults_not_production_tuning",
    }
