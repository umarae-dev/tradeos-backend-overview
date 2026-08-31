# Zynost Intelligence — Public Methodology

This document explains the public methodology boundary of Zynost Intelligence. It is detailed enough to describe how the system handles evidence, uncertainty and synthesis without publishing proprietary prompts, credentials, commercial tuning or operational secrets.

## 1. Evidence before synthesis

Zynost separates **market observation**, **deterministic computation** and **natural-language synthesis**.

The evidence layer is assembled from market, derivatives, project, security, on-chain, macro, news and institutional sources. Deterministic formulas turn those observations into structured modules with explicit classifications, roles, coverage, strength and data-quality metadata.

A language model is not permitted to become the source of a market measurement simply because it can describe that measurement fluently.

In the current production architecture, the Full Scan core can complete its evidence bundle, deterministic consensus, FlowState, Institutional Lenses and Market Twin with **zero model calls**. Language-model synthesis is a separate, on-demand step.

## 2. Twelve-module evidence contract

The production evidence contract currently organizes observations into twelve core modules:

1. Technical
2. Price Structure
3. Liquidity
4. Order Flow
5. Leverage
6. Risk
7. News Context
8. Macro
9. Project
10. Security
11. On-chain
12. Derivatives

The public reference mirrors that conceptual structure without claiming that every public formula or weight equals the private production tuning.

## 3. Module-level semantics

Not every metric is treated as a directional signal.

Modules have explicit roles:

- **directional** — can contribute to the bullish/bearish posture;
- **context** — improves interpretation without becoming an automatic vote;
- **risk gate** — can weaken or invalidate a thesis without pretending to predict direction.

A classification is interpreted inside its own module. A value such as `high` cannot be globally translated into bullish or bearish without knowing what it describes.

## 4. Coverage-aware unavailable states

Optional upstream data can fail or simply not exist for an asset.

When defensible coverage is unavailable, Zynost marks that evidence unavailable rather than silently replacing it with a fabricated score. Coverage and quality therefore become part of the output itself.

This matters for long-tail assets, recently listed markets, tokenized instruments and chain-specific evidence where a source may not apply.

## 5. Deterministic consensus

Consensus is calculated from the eligible directional evidence subset. Coverage and signal strength contribute to weighting, while context and risk-gate modules remain separately inspectable.

The purpose is not to manufacture a precise confidence number from every fact. It is to produce a reproducible posture from the evidence that is actually directional while preserving uncertainty around the rest.

## 6. Market Twin and point-in-time integrity

Historical-comparison features are constructed from information available at the historical observation time. Future outcomes are used only after the historical anchor has been selected.

This separation is intended to prevent look-ahead leakage.

Market Twin compares the current market vector with prior regimes using robust-scaled distance over a bounded feature set. Its design principles include:

- sufficient current feature coverage;
- candidate snapshots strictly before the current observation;
- spacing between selected analogues to reduce near-duplicate outcome windows;
- a minimum sample of independent analogues;
- outcomes expressed as distributions rather than guaranteed targets;
- adverse and favorable path statistics where sufficient history exists;
- scenario adjustments re-run through the same matcher instead of being converted directly into predicted prices.

Production full-quality Market Twin coverage is initially calibrated for BTC and ETH while additional independent history accumulates for broader assets.

## 7. FlowState and FlowShift

FlowState transforms available evidence into higher-level market-condition dimensions such as:

- Fresh Capital;
- Leverage Dependency;
- Holder Pressure;
- Execution Quality;
- Supply Shock.

Those dimensions can resolve into interpretable regimes such as Organic Accumulation, Leveraged Markup, Distribution into Strength, Liquidity Vacuum, Supply Overhang or Balanced Transition.

FlowShift compares a later owner-scoped scan with the previous state and records a material regime or dimension change without requiring a language-model call.

## 8. Institutional Lenses

The commercial intelligence layer can expose structured research lenses around:

- options risk surface;
- leverage stress;
- absorption and exhaustion;
- official institutional positioning;
- cross-market dislocation.

These lenses are deterministic transformations of source evidence. A model is not asked to invent the underlying funding, options, positioning or flow measurements.

## 9. Opportunity discovery and validation separation

The production Opportunity Radar combines market discovery with confirmation evidence. Different output tiers deliberately carry different validation claims.

A historically validated configuration should keep its own methodology, universe, sample and assumptions. Newer order-book, DEX, open-interest or composite signals must not inherit that historical result simply because they now participate in a broader product.

Where a signal does not have an appropriate historical time series, forward tracking is the more defensible validation path.

This is why production concepts such as Confirmed, Emerging, Extreme Watch and Early Activity remain separate rather than being blended into one universal confidence score.

## 10. Trade Blueprint boundary

The production Trade Blueprint uses market-derived values such as OHLCV candles, ATR, pivot/support-resistance structure, trend direction and volatility/exhaustion checks to produce entry, stop and target zones.

Natural-language explanation can describe those levels. It is not allowed to overwrite or improvise them.

## 11. Decision Brief boundary

The Decision Brief is generated only after the evidence and deterministic layers already exist.

The synthesis model receives a bounded decision context containing decision-relevant fields rather than raw credentials, user PII or unrestricted production state.

Its role is to communicate:

- decision posture;
- bull case;
- bear case;
- skeptic/contradiction check;
- risk gates;
- FlowState and institutional context;
- Market Twin context;
- confirmation conditions;
- invalidation conditions;
- what would change the view;
- a simpler explanation in the requested language.

That boundary is intentionally different from asking a model to predict a market from scratch.

## 12. Evidence integrity and reproducibility

Decision-relevant evidence is persisted with analysis runs in the commercial system. Deterministic layers can therefore be re-derived from stored evidence without rewriting the original observations.

Stored downstream outputs can also carry integrity signatures so another synthesis layer can reject content that does not verify before using it as evidence.

## 13. Limitations

Zynost does not claim that historical analogues guarantee future outcomes. Provider coverage can be incomplete, particularly for long-tail assets. Market microstructure can change, regimes can break, token metadata can become stale, and a resting order can disappear between observations.

Research output should therefore be interpreted as structured decision evidence and uncertainty — not a promise of profit or an instruction to trade.
