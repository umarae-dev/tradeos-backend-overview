from __future__ import annotations

from typing import Any


def _clamp(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 1)


def _module_map(bundle: dict) -> dict[str, dict]:
    return {m["name"]: m for m in bundle.get("modules", [])}


def _metric(modules: dict[str, dict], module: str, key: str, default: Any = None) -> Any:
    return modules.get(module, {}).get("metrics", {}).get(key, default)


def build_flow_state(bundle: dict) -> dict:
    """Public FlowState reference derived from Zynost's deterministic regime layer."""
    modules = _module_map(bundle)
    imbalance = float(_metric(modules, "order_flow", "imbalance_pct", 0) or 0)
    turnover = float(_metric(modules, "liquidity", "volume_to_mcap_pct", 0) or 0)
    funding = float(_metric(modules, "leverage", "funding_rate_pct", 0) or 0)
    stable = ((_metric(modules, "derivatives", "stablecoin_flow", {}) or {}).get("change_7d_pct"))
    holder = _metric(modules, "security", "top_10_holder_concentration_pct")
    mintable = _metric(modules, "security", "is_mintable")
    circulating = _metric(modules, "project", "circulating_supply")
    maximum = _metric(modules, "project", "max_supply")
    total = _metric(modules, "project", "total_supply")
    positioning = _metric(modules, "derivatives", "institutional_positioning", {}) or {}

    dimensions: list[dict] = []

    fresh_coverage = 0.0
    fresh_score = 50 + imbalance * 0.45
    if stable is not None:
        fresh_score += float(stable) * 10
        fresh_coverage += 0.55
    if modules.get("order_flow", {}).get("status") == "available":
        fresh_coverage += 0.45
    dimensions.append({
        "name": "Fresh Capital",
        "score": _clamp(fresh_score) if fresh_coverage >= 0.45 else None,
        "coverage": round(fresh_coverage, 2),
    })

    leverage_coverage = 0.85 if modules.get("leverage", {}).get("status") == "available" else 0.0
    leverage_score = _clamp(
        25 + abs(funding) * 500
        + (25 if modules.get("leverage", {}).get("classification") == "stretched" else 0)
    )
    dimensions.append({
        "name": "Leverage Dependency",
        "score": leverage_score if leverage_coverage else None,
        "coverage": leverage_coverage,
    })

    holder_basis = "top_holder_concentration"
    if holder is not None:
        holder_score = float(holder)
        holder_coverage = 0.75
    else:
        asset_manager = positioning.get("asset_manager_net")
        dealer = positioning.get("dealer_net")
        gross = abs(float(asset_manager or 0)) + abs(float(dealer or 0))
        if gross:
            holder_score = 50 + (-float(asset_manager or 0) / gross) * 30
            holder_coverage = 0.55
            holder_basis = "official_positioning_pressure_proxy"
        else:
            holder_score = None
            holder_coverage = 0.0
            holder_basis = "unavailable"
    dimensions.append({
        "name": "Holder Pressure",
        "score": _clamp(holder_score) if holder_score is not None else None,
        "coverage": holder_coverage,
        "basis": holder_basis,
    })

    execution_coverage = (
        float(modules.get("liquidity", {}).get("coverage") or 0) * 0.5
        + float(modules.get("order_flow", {}).get("coverage") or 0) * 0.5
    )
    execution_score = _clamp(30 + min(turnover, 12) * 4 + max(-20, min(20, imbalance)) * 0.5)
    dimensions.append({
        "name": "Execution Quality",
        "score": execution_score if execution_coverage >= 0.45 else None,
        "coverage": round(execution_coverage, 2),
    })

    supply_coverage = 0.0
    supply_score = 50.0
    if circulating is not None and maximum:
        supply_score = float(circulating) / float(maximum) * 100
        supply_coverage += 0.7
    elif circulating is not None and total:
        available_ratio = float(circulating) / float(total) * 100
        supply_score = 50 + (available_ratio - 50) * 0.4
        supply_coverage += 0.55
    if mintable is not None:
        supply_score -= 20 if mintable else 0
        supply_coverage += 0.3
    dimensions.append({
        "name": "Supply Shock",
        "score": _clamp(supply_score) if supply_coverage >= 0.5 else None,
        "coverage": round(supply_coverage, 2),
    })

    scores = {d["name"]: d["score"] for d in dimensions if d["score"] is not None}
    fresh = scores.get("Fresh Capital", 50)
    leverage = scores.get("Leverage Dependency", 50)
    holder_pressure = scores.get("Holder Pressure", 50)
    execution = scores.get("Execution Quality", 50)
    supply = scores.get("Supply Shock", 50)
    trend = modules.get("price_structure", {}).get("classification")
    change = float(bundle.get("market", {}).get("change_24h_pct") or 0)

    if fresh >= 60 and leverage < 55 and trend == "uptrend":
        regime = "Organic Accumulation"
    elif leverage >= 65 and change > 0:
        regime = "Leveraged Markup"
    elif holder_pressure >= 65 and change > 0:
        regime = "Distribution into Strength"
    elif execution < 35:
        regime = "Liquidity Vacuum"
    elif supply < 40:
        regime = "Supply Overhang"
    else:
        regime = "Balanced Transition"

    available = [d for d in dimensions if d["score"] is not None]
    coverage = sum(d["coverage"] for d in dimensions) / len(dimensions)
    return {
        "regime": regime,
        "score": round(sum(d["score"] for d in available) / len(available), 1) if available else None,
        "coverage": round(coverage, 2),
        "dimensions": dimensions,
        "status": "available" if coverage >= 0.55 else "partial",
        "formula_version": "public-flowstate-1.0.0",
    }


def build_flow_shift(current: dict, previous: dict | None) -> dict:
    if not previous or not previous.get("dimensions"):
        return {
            "status": "baseline",
            "changed": False,
            "regime_from": None,
            "regime_to": current.get("regime"),
            "largest_dimension_shift": None,
        }

    previous_dimensions = {
        item.get("name"): item.get("score")
        for item in previous.get("dimensions", [])
        if item.get("score") is not None
    }
    shifts = []
    for item in current.get("dimensions", []):
        score = item.get("score")
        prior = previous_dimensions.get(item.get("name"))
        if score is None or prior is None:
            continue
        shifts.append({
            "name": item.get("name"),
            "from": round(float(prior), 1),
            "to": round(float(score), 1),
            "delta": round(float(score) - float(prior), 1),
        })

    largest = max(shifts, key=lambda item: abs(item["delta"])) if shifts else None
    regime_changed = previous.get("regime") != current.get("regime")
    material_dimension_shift = bool(largest and abs(largest["delta"]) >= 12)
    changed = regime_changed or material_dimension_shift
    return {
        "status": "shift_detected" if changed else "stable",
        "changed": changed,
        "regime_from": previous.get("regime"),
        "regime_to": current.get("regime"),
        "largest_dimension_shift": largest,
    }
