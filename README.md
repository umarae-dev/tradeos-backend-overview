# Zynost — AI Decision Intelligence for Crypto

> **Evidence first. AI second. One decision-ready view instead of another wall of noisy signals.**

Zynost is a crypto decision-intelligence platform designed to turn fragmented market information into a structured, auditable research view.

The current production architecture does **not** ask one language model to look at a chart and invent a conclusion. It first builds a deterministic evidence layer from live/public market data, measures data quality and coverage, derives institutional-style lenses from that evidence, and only then offers an on-demand AI **Decision Brief** that explains the case in human language.

**Live:** https://zynost.com  
**App:** https://app.zynost.com  
**Backend:** Python / FastAPI / PostgreSQL

---

## The problem

A crypto trader can already find price, charts, funding, news, project data, order books and on-chain metrics in dozens of places.

The harder problem is deciding:

- which evidence actually matters now;
- whether different signals agree or conflict;
- whether a move is spot-led or leverage-led;
- whether liquidity is strong enough to trust the move;
- whether supply/security risk invalidates the apparent setup;
- whether current conditions resemble historical regimes;
- what would confirm or invalidate the thesis.

Zynost is built around that decision layer.

---

## Current production architecture

```text
Live / public market data
        │
        ▼
Deterministic Evidence Engine
        │
        ├── Technical
        ├── Price Structure
        ├── Liquidity
        ├── Order Flow
        ├── Leverage
        ├── Risk
        ├── News Context
        ├── Macro
        ├── Project Data
        ├── Security
        ├── On-chain
        └── Derivatives / Institutional Context
        │
        ▼
Coverage + Data Quality
        │
        ▼
Deterministic Consensus
        │
        ├── FlowState / market regime
        ├── Institutional lenses
        ├── Anomaly detection
        ├── Thesis tracker
        └── Market Twin
        │
        ▼
Optional AI Decision Brief
        │
        ▼
Follow-up Explain session
```

The important design decision is the boundary in the middle:

> **The language model interprets a bounded evidence context; it is not the source of the market numbers.**

---

## 12 evidence modules

The production evidence bundle currently organizes market information into twelve modules.

| Module | What it answers |
|---|---|
| **Technical** | What is short-horizon momentum doing and where are observed support/resistance levels? |
| **Price Structure** | Is the sampled swing structure trending, ranging or deteriorating? |
| **Liquidity** | Is turnover deep enough for cleaner execution or unusually thin? |
| **Order Flow** | Is live resting liquidity bid-dominant, ask-dominant or balanced? |
| **Leverage** | Is perpetual funding controlled or showing crowding stress? |
| **Risk** | How large is the observed volatility/range relative to current price? |
| **News Context** | Is there meaningful recent source coverage around the asset? |
| **Macro** | What does broad crypto risk appetite currently look like? |
| **Project** | What can be verified from public supply / market metadata? |
| **Security** | Are observable contract/network risk flags present? |
| **On-chain** | What network activity is actually available for the asset? |
| **Derivatives** | What can options, positioning and broader capital-flow data add? |

Each module carries its own:

- status;
- classification;
- directional role or risk/context role;
- strength;
- data-quality label;
- coverage score;
- observation timestamp;
- source class;
- raw decision-relevant metrics.

Unavailable evidence is marked unavailable instead of being replaced with a fabricated neutral value.

---

## Evidence roles — not every fact gets a vote

A common analytics mistake is treating every metric as if it were bullish or bearish.

Zynost separates evidence into different roles:

- **Directional** evidence can contribute to market direction;
- **Context** evidence informs the interpretation but does not automatically vote;
- **Risk gates** can weaken a thesis without pretending to predict direction.

For example, high network activity and high volatility both contain the word "high", but they do not mean the same thing. The production engine maps stance at the module level rather than using generic keyword scoring.

---

## Deterministic Full Scan

A paid Full Scan builds the evidence bundle and institutional layers **without requiring an LLM call for the market calculations themselves**.

The result contains:

- evidence modules;
- deterministic consensus;
- coverage score;
- institutional FlowState;
- regime shift relative to a prior scan where available;
- premium institutional lenses;
- anomalies;
- thesis confirmation/invalidation conditions;
- Market Twin historical analogue analysis;
- an optional Decision Brief entry point.

This separation matters for reproducibility: re-reading the same stored evidence does not require asking an AI model to recalculate the market.

---

## FlowState — describing the market regime

Zynost derives a higher-level **FlowState** from multiple observable dimensions rather than reducing everything to a single indicator.

Current dimensions include concepts such as:

- **Fresh Capital** — capital-flow and order-book pressure;
- **Leverage Dependency** — how dependent the move appears to be on leveraged positioning;
- **Holder Pressure** — observable concentration / positioning pressure where coverage exists;
- **Execution Quality** — turnover depth plus order-book conditions;
- **Supply Shock** — circulating-supply availability and observable mint/supply controls.

These dimensions are combined into an interpretable regime such as accumulation, leveraged markup, distribution, liquidity stress or a balanced transition.

The system also compares a user's latest Full Scan against their previous one and can surface a material **Flow Shift** when the regime or a major dimension changes enough to matter.

---

## Institutional lenses

Where reliable public data is available, Zynost adds premium lenses that are usually missing from basic retail crypto dashboards.

Examples include:

- **Options Risk Surface** — options open-interest balance and implied-volatility context;
- **Leverage Stress Radar** — funding and open-interest crowding;
- **Absorption & Exhaustion Monitor** — price versus order-flow disagreement;
- **Institutional Positioning Lens** — official positioning data where available;
- **Cross-Market Dislocation Engine** — divergence between asset price, system liquidity and macro risk appetite.

These lenses fail honestly when the required public coverage does not exist for an asset.

---

## Market Twin — historical regimes, not a fake forecast

For supported assets with sufficient stored history, **Market Twin** compares the current evidence vector with prior point-in-time regimes.

Instead of saying "AI predicts +12%", it asks a more defensible question:

> **When the market previously looked most similar to this, what distribution of outcomes followed?**

The current implementation:

- uses only evidence available at each historical point in time;
- excludes future information from the feature vector;
- requires sufficient feature coverage;
- spaces historical anchors to reduce near-duplicate samples;
- requires a meaningful number of independent analogues before calling the result operational;
- reports distributions across multiple horizons rather than one guaranteed target;
- includes adverse and favorable excursion information;
- exposes Base / Confirmation / Stress scenario comparisons.

Full-quality Market Twin calibration currently begins with **BTC and ETH** while history accumulates.

If there is not enough clean history, the product says it is still collecting history instead of manufacturing a forecast.

See [`METHODOLOGY.md`](METHODOLOGY.md) for the public methodology boundary.

---

## Optional AI Decision Brief

After a Full Scan is complete, a user can request a language-specific **Decision Brief**.

The AI receives a bounded decision context built from the stored evidence layers, including:

- market state;
- coverage;
- evidence modules;
- consensus;
- FlowState;
- Flow Shift;
- institutional lenses;
- anomalies;
- thesis tracker;
- Market Twin where available.

The Decision Brief then produces a human-readable synthesis such as:

- bull case;
- bear case;
- skeptic/risk check;
- confidence;
- explanation grounded in the supplied evidence.

The production service deliberately removes credentials and user PII from this decision context.

A separate **Explain** agent can then answer follow-up questions against the same evidence instead of starting from an ungrounded blank prompt.

---

## Public institutional data layer

Zynost combines ordinary market data with selected public institutional-style sources where coverage permits.

Examples currently include:

- multi-exchange price/candle data;
- public order books;
- perpetual futures / funding information;
- public options-market summaries for supported assets;
- official weekly positioning data where available;
- public stablecoin-supply flow data;
- project and supply metadata;
- security scans / native-network observations;
- on-chain activity;
- public news feeds;
- broad crypto sentiment/macro context.

Provider failure does not silently turn into invented evidence. Optional sources can degrade to unavailable while the rest of the evidence bundle remains usable.

---

## Data quality and coverage are part of the product

A professional research system should communicate what it **doesn't know**.

Zynost therefore attaches coverage and quality metadata to the evidence instead of hiding missing providers behind a polished score.

This is important for long-tail assets where:

- derivatives may not exist;
- institutional positioning may not be available;
- contract metadata may be incomplete;
- on-chain coverage may differ by network;
- historical analogue data may not yet be sufficient.

A smaller but honest evidence set is preferable to a confident-looking hallucination.

---

## Reproducibility and stored evidence

Full Scans persist their evidence context and signed analysis outputs so decision-relevant results can be traced back to the evidence that produced them.

The architecture also separates:

- immutable evidence;
- deterministic interpretation layers;
- optional language-model synthesis.

That makes it possible to improve presentation and deterministic layers without rewriting the original market observations or charging the user for another model call.

---

## Relationship to the broader Zynost ecosystem

```text
Zynost Intelligence
       │
       ├──────────── decision context
       ▼
Zynost Wallet
       │
       ├──────────── merchant / developer payments
       ▼
Zynost Pay
       │
       ▼
Zynost Paymaster ───── BNB Smart Chain
       │
       ▼
UQX ecosystem
```

Zynost Intelligence is the research and decision layer. Wallet and payment products are separate execution/custody surfaces with their own security boundaries.

The long-term direction is to let intelligence improve user understanding and transaction safety **without turning AI into an unrestricted custodian of funds**.

---

## Stack

Python · FastAPI · PostgreSQL / async SQLAlchemy · background workers · multi-source public market-data services · deterministic evidence formulas · Anthropic Claude for bounded on-demand synthesis

---

## Production vs. public repository boundary

This repository is a **public architecture and methodology overview**, not the production backend.

### Public here

- product architecture;
- evidence-module model;
- data-quality philosophy;
- deterministic-vs-AI boundary;
- institutional intelligence concepts;
- Market Twin methodology at a safe high level;
- relationship to the wider Zynost ecosystem.

### Kept private

- production source code;
- agent prompts;
- internal operational configuration;
- API credentials and provider keys;
- database credentials;
- proprietary implementation details and tuning;
- abuse-prevention controls;
- user data;
- production monitoring/runbooks.

No API key, private key, database credential or user-private information should ever be committed to this repository.

---

## Important product principle

Zynost is **decision intelligence**, not an automatic promise of profit.

The system is designed to make evidence easier to evaluate, surface disagreement and risk, and show what would confirm or invalidate a thesis. Historical analogues and AI explanations are research tools, not guarantees of future market performance.

---

## Status

**Active production development.**

The backend currently includes the evidence-first Full Scan architecture, deterministic institutional layers, Market Twin history matching, on-demand Decision Brief synthesis and follow-up evidence-grounded explanation flows.

For the public methodology boundary, see [`METHODOLOGY.md`](METHODOLOGY.md).  
For responsible security reporting, see [`SECURITY.md`](SECURITY.md).
