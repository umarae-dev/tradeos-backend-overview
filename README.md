# Zynost Public Intelligence Reference

> **Evidence first. Computation second. Synthesis on demand.**

Zynost is a **digital-asset decision-intelligence system** that turns fragmented market, derivatives, on-chain, security, macro and institutional observations into a structured evidence contract before any optional language-model explanation is requested.

This repository is an **executable open-source reference**, not a documentation-only showcase. It contains a provider-agnostic 12-module evidence engine, semantic evidence roles, deterministic consensus, FlowState regime analysis, Market Twin historical-analogue logic, public institutional-data adapters, FastAPI, tests, Docker and CI.

**Product:** https://zynost.com  
**Application:** https://app.zynost.com  
**License:** Apache-2.0  
**Python:** 3.11+  
**Public/private boundary:** [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md)  
**Release verification:** [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)

---

## Why Zynost exists

Digital-asset markets do not suffer from a shortage of data. They suffer from fragmentation.

A researcher may need to reconcile:

- price structure and momentum;
- market depth and order flow;
- leverage and derivatives positioning;
- news and macro context;
- token/project metadata;
- contract or network risk;
- on-chain activity;
- institutional positioning and capital-flow context;
- historical analogues;
- uncertainty and missing coverage.

The harder problem is deciding **which evidence is directional, which is context, which is a risk gate, and what should remain explicitly unavailable**.

The public reference demonstrates Zynost's architectural answer without asking a language model to manufacture market measurements.

---

## Zynost production architecture

The commercial system is broader than this repository. At a high level:

```text
Market / Chain / Security / Institutional Sources
                       │
                       ▼
              12-Module Evidence Engine
                       │
                       ▼
            Semantic Evidence Roles
          directional / context / risk_gate
                       │
                       ▼
              Deterministic Consensus
                       │
          ┌────────────┼───────────────┐
          ▼            ▼               ▼
      FlowState   Institutional     Market Twin
                    Lenses
          │            │               │
          └────────────┴───────┬───────┘
                               ▼
                       Decision Context
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
          Product Workflows           On-demand synthesis
      discovery / planning / risk     Decision Brief / Explain
```

The production Full Scan core can form its evidence bundle, deterministic consensus, FlowState, Institutional Lenses and Market Twin **without a language-model call**. Natural-language synthesis is requested later only when the user asks for a Decision Brief or another explicitly narrative workflow.

That distinction is central to Zynost's positioning: **AI can explain the evidence; it does not become the source of the evidence.**

---

## The 12 evidence modules

The canonical evidence contract currently organizes observations into:

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

Each module exposes metadata such as:

```json
{
  "name": "order_flow",
  "role": "directional",
  "status": "available",
  "classification": "bid_dominant",
  "stance": "bullish",
  "coverage": 0.9,
  "strength": 64.0,
  "source_class": "public_order_book_snapshot",
  "metrics": {
    "imbalance_pct": 11.2
  }
}
```

Unavailable data remains unavailable. It is not silently converted into a neutral-looking synthetic number.

---

## Not every fact gets a vote

Zynost separates evidence into three semantic roles:

- **directional** — may contribute to bullish/bearish posture;
- **context** — improves interpretation without automatically voting;
- **risk_gate** — can weaken or invalidate a thesis without pretending to predict direction.

This avoids generic keyword scoring where, for example, `high` network activity and `high` volatility would be treated as equivalent signals.

---

## Deterministic consensus

Consensus is calculated from eligible directional evidence using explicit coverage/strength weighting. Context and risk-gate modules remain visible but do not become artificial directional votes.

The formulas in this public repository are reference defaults. They are **not represented as the exact proprietary production tuning** used by the commercial product.

---

## FlowState

FlowState turns observed evidence into higher-level market-condition dimensions:

- Fresh Capital;
- Leverage Dependency;
- Holder Pressure;
- Execution Quality;
- Supply Shock.

Those dimensions can resolve into interpretable regimes such as Organic Accumulation, Leveraged Markup, Distribution into Strength, Liquidity Vacuum, Supply Overhang or Balanced Transition.

`build_flow_shift()` compares consecutive states without requiring a language model.

---

## Market Twin

Market Twin performs point-in-time historical analogue matching.

Its key safeguards include:

- minimum current feature coverage;
- historical anchors strictly before the current observation;
- robust scaling;
- spacing between selected analogues;
- minimum independent sample requirements;
- multi-horizon outcome distributions;
- adverse/favorable excursion reporting;
- an explicit `collecting_history` state when evidence is insufficient.

Historical analogues describe a distribution. They are not guaranteed forecasts.

In the commercial product, full-quality calibration is initially focused on BTC and ETH while independent history accumulates for broader assets.

---

## Public institutional adapters

The reference includes public/keyless adapters for:

- Deribit options summaries for BTC/ETH;
- official CFTC weekly positioning where supported;
- stablecoin-supply flow context.

Adapters use bounded caching and failure handling. Provider failure returns unavailable evidence rather than invented measurements.

---

## Commercial capabilities beyond this public package

The wider Zynost product also contains production workflows that are intentionally not mirrored in full here, including:

- **Opportunity Radar** — CEX + DEX market discovery with separate Confirmed, Emerging, Extreme Watch and Early Activity tiers;
- **Order Book Radar** — multi-exchange resting-wall persistence, pulled-wall context, spread and nearby depth;
- **Trade Blueprint** — deterministic ATR and market-structure based entry, stop and target zones;
- **Token Risk Intelligence** and deeper Security Postmortem workflows;
- **Whale Flow Intelligence** as supporting transfer context on selected networks;
- **On-Chain Intelligence** across supported major networks;
- **Portfolio Intelligence**, performance review and trading-psychology workflows;
- **Decision Brief** — bounded, on-demand structured synthesis;
- **Zynost Voice / Explain** — connected questions over a completed owner-scoped analysis.

These names describe the commercial product. Their absence from this public extraction should not be interpreted as a claim that every private implementation has been open-sourced.

---

## Included code

- [`src/evidence/builder.py`](src/evidence/builder.py) — deterministic 12-module evidence construction;
- [`src/evidence/model.py`](src/evidence/model.py) — provider-agnostic evidence schema;
- [`src/evidence/roles.py`](src/evidence/roles.py) — directional/context/risk-gate semantics;
- [`src/evidence/consensus.py`](src/evidence/consensus.py) — weighted deterministic posture;
- [`src/intelligence/flow_state.py`](src/intelligence/flow_state.py) — market-regime reference layer;
- [`src/intelligence/market_twin.py`](src/intelligence/market_twin.py) — point-in-time historical analogue matcher;
- [`src/intelligence/thesis.py`](src/intelligence/thesis.py) — anomalies and confirmation/invalidation conditions;
- [`src/intelligence/pipeline.py`](src/intelligence/pipeline.py) — end-to-end public pipeline;
- [`src/providers/public_institutional.py`](src/providers/public_institutional.py) — public Deribit, CFTC and stablecoin-flow adapters;
- [`src/api/app.py`](src/api/app.py) — FastAPI `POST /analyze` endpoint;
- [`scripts/check_public_repo.py`](scripts/check_public_repo.py) — public-source guard for forbidden sensitive files and obvious credential material.

Some modules are directly derived from production-safe implementation patterns; others are independent public reference implementations created so this repository can run without private infrastructure.

---

## Quick start

### 1. Clone

```bash
git clone https://github.com/umarae-dev/tradeos-backend-overview.git
cd tradeos-backend-overview
```

### 2. Create an environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install

```bash
pip install -e ".[dev]"
```

### 4. Run the reference analysis

```bash
python examples/run_reference.py
```

### 5. Run tests

```bash
pytest -q
```

### 6. Start the API

```bash
uvicorn src.api.app:app --reload
```

Endpoints:

```text
GET  /health
POST /analyze
```

The deterministic reference pipeline requires no private Zynost credential.

---

## Docker

```bash
docker build -t zynost-public-intelligence .
docker run --rm -p 8000:8000 zynost-public-intelligence
```

---

## CI and public-source safety

GitHub Actions verifies the project on supported Python versions and performs:

- sensitive-file / credential-pattern guard;
- Python compile check;
- import smoke test;
- Ruff static checks;
- pytest suite;
- executable reference example;
- Docker build.

The checks reduce accidental disclosure risk but do not replace human review before publishing production-derived code.

---

## Public / private boundary

### Public here

- evidence schemas and semantic roles;
- deterministic reference formulas;
- provider-agnostic evidence builder;
- deterministic consensus;
- FlowState reference implementation;
- Market Twin point-in-time matcher;
- public/keyless provider adapters;
- anomaly/thesis contracts;
- FastAPI interface;
- tests, Docker, CI and examples.

### Private production components

- production credentials and provider configuration;
- production databases and user data;
- commercial prompts and model-routing configuration;
- proprietary scoring/tuning;
- abuse/fraud controls;
- operational infrastructure and runbooks;
- billing, entitlement and account systems;
- private implementation details of wider commercial capabilities.

These private components are not required to compile, test or evaluate the public reference.

Read [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md) for the precise disclosure model.

---

## Production lineage and provenance

This public repository was extracted after development of the wider Zynost production intelligence system. Public-release dates therefore represent the open-source publication timeline, not the beginning of product development.

[`PROVENANCE.md`](PROVENANCE.md) records the distinction between:

- existing production development;
- safely reusable production-derived modules;
- independently written OSS packaging/reference code;
- intentionally private commercial IP.

---

## Security

Do not commit:

- API keys;
- database URLs or passwords;
- wallet private keys or seed phrases;
- production signer material;
- user data;
- private prompts or tuning;
- internal abuse thresholds;
- infrastructure secrets.

See [`SECURITY.md`](SECURITY.md) for responsible reporting.

---

## Related Zynost repositories

- [Zynost Pay overview](https://github.com/umarae-dev/zynost-pay-overview)
- [Zynost Paymaster overview](https://github.com/umarae-dev/zynost-paymaster-overview)
- [UQX app overview](https://github.com/umarae-dev/uqx-app-overview)
- [UQX BNB contracts overview](https://github.com/umarae-dev/uqx-bnb-contracts-overview)

---

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

Zynost and UQX names, marks and branding are not granted as trademarks merely because source code is open source.

---

## Disclaimer

This project is research tooling. It does not guarantee future performance and is not financial advice. Market, security and provider coverage can be incomplete; callers should preserve source provenance and treat unavailable evidence explicitly.
