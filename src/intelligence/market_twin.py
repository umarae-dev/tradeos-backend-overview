from __future__ import annotations

from datetime import datetime, timedelta
import math
import statistics

MARKET_TWIN_FEATURES = (
    "change_4h", "change_24h", "change_7d", "momentum", "volatility",
    "recovery", "trend_efficiency", "range_position", "funding",
)
HORIZONS = {"4h": timedelta(hours=4), "24h": timedelta(hours=24), "7d": timedelta(days=7), "30d": timedelta(days=30)}
MIN_ANALOGUES = 30
MAX_ANALOGUES = 50
MIN_FEATURE_COVERAGE = 0.70


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        raise ValueError("empty values")
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def _robust_scales(rows: list[dict[str, float]]) -> dict[str, tuple[float, float]]:
    keys = sorted({key for row in rows for key in row})
    scales: dict[str, tuple[float, float]] = {}
    for key in keys:
        values = [row[key] for row in rows if key in row]
        if not values:
            continue
        median = statistics.median(values)
        iqr = _quantile(values, 0.75) - _quantile(values, 0.25) if len(values) >= 4 else 0
        scales[key] = (median, iqr or max(abs(median) * 0.1, 1.0))
    return scales


def _distance(current: dict[str, float], candidate: dict[str, float], scales: dict[str, tuple[float, float]]) -> tuple[float, float]:
    shared = [key for key in current if key in candidate and key in scales]
    coverage = len(shared) / max(1, len(current))
    if not shared:
        return math.inf, 0.0
    squared = [((current[k] - candidate[k]) / scales[k][1]) ** 2 for k in shared]
    return math.sqrt(sum(squared) / len(squared)), coverage


def scenario_definitions() -> list[dict]:
    return [
        {"name": "Base", "adjustments": {}, "description": "Current observed evidence without intervention."},
        {"name": "Confirmation", "adjustments": {"change_4h": 1.0, "momentum": 1.0, "recovery": 3.0, "funding": 0.01}, "description": "Spot momentum and recovery strengthen while leverage remains controlled."},
        {"name": "Stress", "adjustments": {"change_4h": -4.0, "momentum": -2.0, "volatility": 3.0, "funding": 0.08, "range_position": -20.0}, "description": "Momentum deteriorates while volatility and leverage stress rise."},
    ]


def _unavailable(reason: str, count: int, coverage: float) -> dict:
    return {
        "status": "collecting_history",
        "readiness": "collecting_history",
        "reason": reason,
        "analogue_count": count,
        "minimum_analogues": MIN_ANALOGUES,
        "feature_coverage": round(coverage, 2),
        "outcome_cone": {},
        "scenarios": scenario_definitions(),
    }


def match_market_twin(*, current_vector: dict[str, float], current_time: datetime, snapshots: list[dict], minimum_analogues: int = MIN_ANALOGUES) -> dict:
    """Point-in-time analogue matcher. Future observations never enter the feature vector."""
    current_vector = {k: v for k, v in current_vector.items() if k in MARKET_TWIN_FEATURES}
    history = [s for s in snapshots if s["observed_at"] < current_time and s.get("price")]
    feature_coverage = len(current_vector) / len(MARKET_TWIN_FEATURES)
    if feature_coverage < MIN_FEATURE_COVERAGE:
        return _unavailable("Current feature coverage is below 70%.", len(history), feature_coverage)

    scales = _robust_scales([s.get("features", {}) for s in history])
    ranked = []
    for snapshot in history:
        distance, coverage = _distance(current_vector, snapshot.get("features", {}), scales)
        if coverage >= MIN_FEATURE_COVERAGE and math.isfinite(distance):
            ranked.append((distance, coverage, snapshot))
    ranked.sort(key=lambda item: item[0])

    selected: list[tuple[float, float, dict]] = []
    for item in ranked:
        observed = item[2]["observed_at"]
        if any(abs((observed - existing[2]["observed_at"]).total_seconds()) < 30 * 24 * 3600 for existing in selected):
            continue
        selected.append(item)
        if len(selected) >= MAX_ANALOGUES:
            break

    if len(selected) < minimum_analogues:
        return _unavailable("Not enough independent point-in-time analogues yet.", len(selected), feature_coverage)

    ordered_history = sorted(history, key=lambda s: s["observed_at"])
    outcomes: dict[str, dict] = {}
    for label, delta in HORIZONS.items():
        returns: list[float] = []
        mae: list[float] = []
        mfe: list[float] = []
        for _, _, anchor in selected:
            target_time = anchor["observed_at"] + delta
            future = [s for s in ordered_history if anchor["observed_at"] < s["observed_at"] <= target_time]
            if not future or future[-1]["observed_at"] < target_time - delta * 0.15:
                continue
            start = float(anchor["price"])
            path = [(float(s["price"]) - start) / start * 100 for s in future if s.get("price")]
            if not path:
                continue
            returns.append(path[-1])
            mae.append(min(path))
            mfe.append(max(path))
        if len(returns) >= minimum_analogues:
            outcomes[label] = {
                "sample_size": len(returns),
                "median_return_pct": round(statistics.median(returns), 2),
                "p20_return_pct": round(_quantile(returns, 0.20), 2),
                "p80_return_pct": round(_quantile(returns, 0.80), 2),
                "median_adverse_excursion_pct": round(statistics.median(mae), 2),
                "median_favorable_excursion_pct": round(statistics.median(mfe), 2),
            }

    if not outcomes:
        return _unavailable("Analogues exist but do not yet have enough completed forward windows.", len(selected), feature_coverage)

    mean_distance = sum(item[0] for item in selected) / len(selected)
    return {
        "status": "available",
        "readiness": "operational",
        "analogue_count": len(selected),
        "feature_coverage": round(feature_coverage, 2),
        "sample_quality": "high" if mean_distance <= 1.0 else "medium",
        "mean_distance": round(mean_distance, 3),
        "outcome_cone": outcomes,
        "methodology": "Point-in-time, robust-scaled nearest regimes; no future data enters the feature vector.",
        "disclaimer": "Historical analogues describe a distribution, not a guaranteed forecast.",
    }
