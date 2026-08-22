# Zynost Intelligence — Public Methodology

This document explains the public methodology boundary of Zynost Intelligence. It is intentionally detailed enough to describe how the system approaches evidence and uncertainty without publishing proprietary prompts, production credentials, internal tuning, or operational secrets.

## 1. Evidence before synthesis

Zynost separates market observation from natural-language interpretation.

The evidence layer is assembled from live/public market, derivatives, project, security, on-chain, macro and news sources. Deterministic formulas turn those observations into structured modules with explicit classifications, coverage and data-quality metadata.

A language model is not permitted to become the source of market measurements simply because it can describe them fluently.

## 2. Module-level semantics

Not every metric is treated as a directional signal.

Modules have explicit roles:

- directional;
- context;
- risk gate.

A classification is interpreted inside the meaning of its own module. A value such as "high" cannot be globally translated into bullish or bearish without knowing what it describes.

## 3. Honest unavailable states

Optional upstream data can fail or simply not exist for an asset.

When reliable coverage is unavailable, Zynost marks that evidence unavailable rather than silently replacing it with a fabricated score. Coverage and quality therefore become part of the output itself.

## 4. Point-in-time integrity

Historical-comparison features are constructed from information available at the historical observation time. Future outcomes are used only after the historical anchor has been selected.

This separation is intended to prevent look-ahead leakage in Market Twin analogue matching.

## 5. Market Twin

Market Twin compares the current market vector with prior regimes using robust-scaled distance over a bounded feature set.

The public design principles are:

- sufficient current feature coverage is required;
- candidate snapshots must predate the current observation;
- historical anchors are spaced apart to reduce near-duplicate outcome windows;
- a minimum sample of independent analogues is required before the feature is considered operational;
- outcomes are expressed as distributions rather than a guaranteed target;
- downside and upside path statistics are included where sufficient history exists;
- scenario adjustments are re-run through the same historical matcher instead of being converted directly into predicted prices.

The exact production feature weights, internal tuning and operational datasets are not published here.

## 6. FlowState and institutional lenses

The institutional layer combines observable market dimensions such as capital flow, leverage, liquidity/execution quality, supply conditions and positioning into higher-level research views.

These views are deterministic transformations of the evidence bundle. They do not rely on an LLM to invent a regime label from prose.

A later scan can be compared against a prior owner-scoped scan to detect a material regime or dimension shift.

## 7. AI Decision Brief boundary

The Decision Brief is generated only after the evidence and deterministic layers exist.

The model receives a bounded context containing decision-relevant fields, not raw credentials, user PII or unrestricted production state.

Its role is synthesis and explanation: bull case, bear case, skeptic/risk check, confidence and user-facing language.

## 8. Reproducibility

Decision-relevant evidence is persisted with analysis runs. This allows deterministic layers to be re-derived from stored evidence and lets presentation evolve without rewriting the original observations.

## 9. Limitations

Zynost does not claim that historical analogues guarantee future outcomes. Public provider coverage can be incomplete, particularly for long-tail assets. Market microstructure can change, regimes can break, and security or project metadata can be stale or unavailable.

Research output should therefore be interpreted as structured evidence, not a promise of profit or an instruction to trade.
