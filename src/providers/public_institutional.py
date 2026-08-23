"""Keyless/public institutional data adapters with bounded caches and honest failure.

This module is copied from the production provider layer because it contains
only public/keyless data access and no Zynost credentials or private provider
configuration.
"""

from __future__ import annotations

import asyncio
import csv
import io
import time
from typing import Awaitable, Callable

import httpx


_CACHE: dict[str, tuple[float, dict | None]] = {}
_FAILURES: dict[str, tuple[int, float]] = {}


async def _cached(
    key: str,
    ttl: int,
    loader: Callable[[], Awaitable[dict | None]],
) -> dict | None:
    cached = _CACHE.get(key)
    if cached and time.monotonic() - cached[0] < ttl:
        return cached[1]
    failures, opened_at = _FAILURES.get(key, (0, 0.0))
    if failures >= 3 and time.monotonic() - opened_at < 120:
        return None
    try:
        value = await loader()
    except Exception:
        _FAILURES[key] = (failures + 1, time.monotonic())
        return None
    _FAILURES.pop(key, None)
    _CACHE[key] = (time.monotonic(), value)
    return value


async def fetch_deribit_options(symbol: str) -> dict | None:
    symbol = symbol.upper()
    if symbol not in {"BTC", "ETH"}:
        return None

    async def _load() -> dict | None:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                "https://www.deribit.com/api/v2/public/get_book_summary_by_currency",
                params={"currency": symbol, "kind": "option"},
            )
            response.raise_for_status()
        rows = response.json().get("result") or []
        if not rows:
            return None
        call_oi = put_oi = weighted_iv = iv_weight = 0.0
        for row in rows:
            name = str(row.get("instrument_name") or "")
            oi = float(row.get("open_interest") or 0)
            iv = float(row.get("mark_iv") or 0)
            if name.endswith("-C"):
                call_oi += oi
            elif name.endswith("-P"):
                put_oi += oi
            if iv > 0 and oi > 0:
                weighted_iv += iv * oi
                iv_weight += oi
        total = call_oi + put_oi
        return {
            "put_call_open_interest_ratio": round(put_oi / call_oi, 4) if call_oi else None,
            "call_open_interest": round(call_oi, 4),
            "put_open_interest": round(put_oi, 4),
            "total_open_interest": round(total, 4),
            "weighted_mark_iv_pct": round(weighted_iv / iv_weight, 2) if iv_weight else None,
            "contracts_observed": len(rows),
            "source_class": "public_options_venue",
        }

    return await _cached(f"deribit:{symbol}", 300, _load)


async def fetch_cftc_positioning(symbol: str) -> dict | None:
    """Weekly official financial-futures COT; currently BTC/ETH where present."""
    symbol = symbol.upper()
    if symbol not in {"BTC", "ETH"}:
        return None

    async def _load() -> dict | None:
        async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
            response = await client.get("https://www.cftc.gov/dea/newcot/FinFutWk.txt")
            response.raise_for_status()
        rows = list(csv.reader(io.StringIO(response.text)))
        needle = "BITCOIN" if symbol == "BTC" else "ETHER"
        row = next((r for r in rows if r and needle in r[0].upper()), None)
        if row is None or len(row) < 17:
            return None

        def _number(index: int) -> int | None:
            try:
                return int(row[index].replace(",", "").strip())
            except (ValueError, IndexError):
                return None

        dealer_long, dealer_short = _number(8), _number(9)
        asset_long, asset_short = _number(11), _number(12)
        if all(v is None for v in (dealer_long, dealer_short, asset_long, asset_short)):
            return None
        return {
            "dealer_net": (dealer_long - dealer_short) if dealer_long is not None and dealer_short is not None else None,
            "asset_manager_net": (asset_long - asset_short) if asset_long is not None and asset_short is not None else None,
            "report_date": row[2].strip() if len(row) > 2 else None,
            "source_class": "official_regulator_weekly",
        }

    return await _cached(f"cftc:{symbol}", 6 * 3600, _load)


async def fetch_stablecoin_flow() -> dict | None:
    async def _load() -> dict | None:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get("https://stablecoins.llama.fi/stablecoincharts/all")
            response.raise_for_status()
        rows = response.json()
        if not isinstance(rows, list) or len(rows) < 8:
            return None

        def _total(row: dict) -> float:
            value = row.get("totalCirculatingUSD") or row.get("totalCirculating") or {}
            if isinstance(value, dict):
                value = value.get("peggedUSD") or sum(float(v or 0) for v in value.values())
            return float(value or 0)

        current = _total(rows[-1])
        prior = _total(rows[-8])
        return {
            "total_usd": round(current, 2),
            "change_7d_pct": round((current - prior) / prior * 100, 3) if prior else None,
            "source_class": "public_stablecoin_aggregator",
        }

    return await _cached("stablecoin:all", 1800, _load)


async def gather_public_institutional_data(symbol: str) -> dict:
    options, positioning, stablecoins = await asyncio.gather(
        fetch_deribit_options(symbol),
        fetch_cftc_positioning(symbol),
        fetch_stablecoin_flow(),
    )
    return {"options": options, "positioning": positioning, "stablecoins": stablecoins}
