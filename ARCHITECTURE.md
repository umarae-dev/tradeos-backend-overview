# Zynost Intelligence Architecture

## Category

Zynost is a **digital-asset decision-intelligence system**.

The core architectural rule is:

> **Evidence first. Computation second. Synthesis on demand.**

The open-source reference is intentionally useful without a language model, production database, commercial account, paid provider, user identity or private Zynost credential.

## Production system at a glance

The private production backend is broader than this public extraction. Its current product architecture can be understood as five connected layers:

```text
1. MARKET FABRIC
   ├─ multi-exchange prices + OHLCV
   ├─ futures funding / open interest
   ├─ order books
   ├─ CEX market discovery
   ├─ DEX discovery
   ├─ on-chain network statistics
   ├─ token security
   ├─ news / macro / project metadata
   └─ public institutional sources
            │
            ▼
2. EVIDENCE ENGINE
   ├─ Technical
   ├─ Price Structure
   ├─ Liquidity
   ├─ Order Flow
   ├─ Leverage
   ├─ Risk
   ├─ News Context
   ├─ Macro
   ├─ Project
   ├─ Security
   ├─ On-chain
   └─ Derivatives
            │
            ▼
3. DETERMINISTIC INTELLIGENCE
   ├─ semantic evidence roles
   ├─ weighted consensus
   ├─ Institutional Lenses
   ├─ FlowState
   ├─ FlowShift
   ├─ Market Twin
   ├─ Opportunity Radar
   ├─ Trade Blueprint
   ├─ Token Risk / Security Postmortem
   └─ portfolio + performance metrics
            │
            ▼
4. SYNTHESIS LAYER
   ├─ Decision Brief
   └─ connected Explain / Zynost Voice sessions
            │
            ▼
5. USER WORKFLOW
   research → discover → inspect → plan → monitor → review
```

The public repository focuses on the reusable evidence, consensus, FlowState, Market Twin and institutional-reference architecture. It does **not** pretend to be a mirror of every private production feature.

## Public reference data flow

```text
Public / caller-supplied observations
             │
             ▼
      Evidence Builder
             │
             ├─ Technical
             ├─ Price Structure
             ├─ Liquidity
             ├─ Order Flow
             ├─ Leverage
             ├─ Risk
             ├─ News Context
             ├─ Macro
             ├─ Project
             ├─ Security
             ├─ On-chain
             └─ Derivatives
             │
             ▼
    Semantic Evidence Roles
      ├─ directional
      ├─ context
      └─ risk_gate
             │
             ▼
  Deterministic Consensus
             │
       ┌─────┴──────────────┐
       ▼                    ▼
   FlowState             Anomalies
       │                    │
       └─────────┬──────────┘
                 ▼
          Thesis Contract
                 │
                 ▼
      API / UI / optional synthesis
```

## Why the 12 modules are not “12 votes”

The evidence contract explicitly separates **direction**, **context** and **risk gates**.

Directional modules can contribute to posture. Context modules can improve interpretation without automatically becoming bullish or bearish. Risk gates can weaken or invalidate a thesis without pretending to predict direction.

This prevents an architecture where every available fact is flattened into a generic sentiment vote.

## Package map

### `src/evidence/`

- `model.py` — provider-agnostic evidence schema.
- `roles.py` — semantic roles and stance mapping.
- `builder.py` — deterministic 12-module reference bundle builder.
- `consensus.py` — weighted deterministic posture aggregation.

### `src/providers/`

- `public_institutional.py` — public Deribit options, CFTC positioning and stablecoin-flow adapters with bounded caching and failure handling.

### `src/intelligence/`

- `flow_state.py` — regime dimensions and drift comparison.
- `market_twin.py` — point-in-time historical analogue matching reference.
- `thesis.py` — anomalies plus bounded confirmation/invalidation conditions.
- `pipeline.py` — end-to-end public analysis orchestration.

### `src/api/`

- `app.py` — FastAPI `/health` and `/analyze` endpoints.

## Production capability map

The following names describe the current commercial system but are **not all implemented in this public repository**:

### Evidence Engine

The source-driven Full Scan contract. It normalizes independent observations into explicit modules with coverage and data-quality metadata.

### Opportunity Radar

The production discovery pipeline historically named `System Planned Trade`. It periodically scans meaningful movers in both directions, applies liquidity and confirmation evidence, and keeps different confidence/validation scopes separate:

- Confirmed;
- Emerging;
- Extreme Watch;
- Early Activity.

### Order Book Radar

Repeated multi-exchange order-book observations used to measure wall persistence, pulled-wall context, spread and nearby market depth. It is deliberately framed as persistence intelligence rather than tick-by-tick order-lifecycle surveillance.

### Trade Blueprint

Deterministic planning logic derived from market candles, ATR, pivot/support-resistance structure, trend and volatility/exhaustion checks. Narrative synthesis does not modify its calculated prices.

### FlowState / FlowShift

A five-dimension market-regime model plus material-change comparison between owner-scoped scans.

### Market Twin

Point-in-time historical analogue matching that produces outcome distributions rather than a guaranteed price target. Production full-quality calibration is initially focused on BTC and ETH while wider history accumulates.

### Institutional Lenses

A structured layer for options risk surface, leverage stress, absorption/exhaustion, official positioning and cross-market dislocation when source coverage permits.

### Decision Brief

An on-demand structured explanation over a bounded, already-computed decision context. Its responsibility is synthesis — not market measurement.

## Model-call boundary

A production **Full Scan core can complete with zero language-model calls**. The evidence bundle, deterministic consensus, FlowState, Institutional Lenses and Market Twin are formed first.

A model is requested later only for features that explicitly need natural-language synthesis or user-specific explanation, such as a Decision Brief, Explain session, selected coaching workflows or other bounded narrative tasks.

That distinction is important: “uses AI” is not the same architectural claim as “asks AI to calculate the market.”

## Trust boundaries

The public deterministic evidence layer requires no LLM.

In the commercial backend, stored analysis outputs and reports can also carry integrity signatures so downstream consumers can reject content that fails verification before treating it as trusted synthesis context.

The public package requires no access to:

- Zynost production databases;
- user or billing systems;
- provider secrets;
- commercial model routing;
- proprietary tuning;
- operational runbooks.

## Failure philosophy

Missing coverage remains missing.

Provider failures and unsupported evidence are represented explicitly as unavailable rather than silently converted into neutral-looking or synthetic measurements.

## Validation philosophy

Historical validation is scoped to the exact formula, universe, sample and target configuration that was tested. Newer signal families do not automatically inherit an older result.

Signals without an appropriate historical time series are better evaluated through forward tracking than through an invented backtest.

## Security and privacy

No production credentials, user PII, wallet secrets, signer material, infrastructure secrets or private operational runbooks belong in this repository.

See [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md) and [`SECURITY.md`](SECURITY.md).
