# Zynost Public Intelligence Reference

> **Evidence first. AI second. A runnable open-source reference for deterministic crypto decision intelligence.**

Zynost turns fragmented market, derivatives, on-chain, security and macro observations into a structured evidence bundle before any optional language-model explanation is allowed to run.

This repository is **real executable source code**, not a documentation-only showcase. It contains a provider-agnostic 12-module evidence engine, deterministic consensus, FlowState regime analysis, Market Twin historical-analogue logic, public institutional-data adapters, a FastAPI endpoint, tests, Docker and CI.

**Production product:** https://zynost.com  
**Application:** https://app.zynost.com  
**License:** Apache-2.0  
**Python:** 3.11+  
**Public/private boundary:** [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md)

---

## Why this exists

Crypto traders already have access to charts, order books, funding rates, news, token metadata and on-chain data. The harder problem is deciding:

- which evidence matters now;
- which evidence is directional versus merely contextual;
- whether leverage or liquidity weakens an apparent move;
- whether risk/security conditions invalidate a thesis;
- what is unavailable and therefore should **not** be fabricated;
- what would confirm or invalidate a market view.

The public reference demonstrates the architecture Zynost uses to solve that problem without asking an LLM to invent market measurements.

---

## What is actually open source

```text
Public / caller-supplied observations
             │
             ▼
      12-Module Evidence Builder
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
       Evidence Roles
     directional / context / risk_gate
             │
             ▼
    Deterministic Consensus
             │
       ┌─────┴──────────┐
       ▼                ▼
   FlowState         Anomalies
       │                │
       └───────┬────────┘
               ▼
         Thesis Contract
               │
               ▼
       API / UI / optional AI
```

### Included code

- [`src/evidence/builder.py`](src/evidence/builder.py) — deterministic 12-module evidence construction;
- [`src/evidence/model.py`](src/evidence/model.py) — provider-agnostic evidence schema;
- [`src/evidence/roles.py`](src/evidence/roles.py) — directional/context/risk-gate semantics;
- [`src/evidence/consensus.py`](src/evidence/consensus.py) — weighted deterministic posture;
- [`src/intelligence/flow_state.py`](src/intelligence/flow_state.py) — deterministic market-regime layer;
- [`src/intelligence/market_twin.py`](src/intelligence/market_twin.py) — point-in-time historical analogue matcher;
- [`src/intelligence/thesis.py`](src/intelligence/thesis.py) — anomalies and confirmation/invalidation conditions;
- [`src/intelligence/pipeline.py`](src/intelligence/pipeline.py) — end-to-end public pipeline;
- [`src/providers/public_institutional.py`](src/providers/public_institutional.py) — keyless Deribit/CFTC/stablecoin adapters;
- [`src/api/app.py`](src/api/app.py) — FastAPI `/health` and `/analyze` endpoints.

The public provider module is adapted from a safe/keyless production provider layer. It contains no Zynost API credentials or private provider configuration.

---

## Quick start

### Option A — local Python

```bash
git clone https://github.com/umarae-dev/tradeos-backend-overview.git
cd tradeos-backend-overview

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

python examples/run_reference.py
pytest -q
```

The deterministic reference example requires **no API key, database or model credential**.

### Option B — API

```bash
uvicorn src.api.app:app --reload
```

Then:

```text
GET  /health
POST /analyze
```

`POST /analyze` accepts structured observations and returns:

- normalized evidence bundle;
- evidence availability/coverage;
- deterministic consensus;
- FlowState;
- anomalies;
- bounded thesis conditions.

### Option C — Docker

```bash
docker build -t zynost-public-intelligence .
docker run --rm -p 8000:8000 zynost-public-intelligence
```

---

## Evidence semantics: not every fact gets a vote

A common analytics mistake is converting every data point into bullish/bearish sentiment.

Zynost separates evidence into three roles:

| Role | Meaning |
|---|---|
| **Directional** | May contribute to market posture |
| **Context** | Helps interpretation but does not automatically vote |
| **Risk gate** | Can weaken a thesis without pretending to predict direction |

For example, high network activity and high volatility both contain the word "high", but they do not mean the same thing. The role contract prevents generic keyword scoring from corrupting the consensus.

---

## Honest missing-data behavior

Missing evidence is not silently turned into a neutral signal.

If a provider or observation is unavailable, the module remains explicitly:

```json
{
  "status": "unavailable",
  "coverage": 0.0,
  "stance": "unavailable"
}
```

That behavior is tested. It matters especially for long-tail assets where options, institutional positioning, contract metadata or on-chain coverage may not exist.

---

## Deterministic consensus

The public consensus engine:

1. considers only available evidence;
2. separates directional evidence from context/risk gates;
3. weights directional evidence by coverage and strength;
4. produces an inspectable posture score;
5. reports available/unavailable counts;
6. does not require an LLM call.

Production tuning remains proprietary; public thresholds/defaults are intentionally explicit and independently runnable.

---

## FlowState

FlowState compresses several market dimensions into an interpretable regime layer. The public reference includes dimensions around:

- fresh capital / flow pressure;
- leverage dependency;
- holder/positioning pressure;
- execution quality;
- supply conditions.

It can classify regimes such as Organic Accumulation, Leveraged Markup, Distribution into Strength, Liquidity Vacuum, Supply Overhang or Balanced Transition and compare the current state with a prior snapshot.

---

## Market Twin

The reference Market Twin module asks a bounded historical question:

> **When prior point-in-time evidence looked most similar to the current evidence, what distribution of outcomes followed?**

The implementation:

- restricts features to observations known at the historical timestamp;
- excludes future information from the feature vector;
- requires minimum feature coverage;
- uses robust scaling;
- spaces analogue anchors to reduce near-duplicate windows;
- reports distributions instead of a guaranteed target;
- can return `collecting_history` instead of manufacturing a forecast.

See [`METHODOLOGY.md`](METHODOLOGY.md).

---

## Public institutional adapters

The keyless provider module currently demonstrates:

- Deribit public options summaries for BTC/ETH;
- CFTC official weekly positioning where available;
- public stablecoin supply-flow data;
- bounded caches;
- basic circuit-breaker/failure behavior;
- honest `None` degradation when reliable data is unavailable.

The deterministic core does not depend on these adapters; callers can provide their own observations or BNB-specific/on-chain providers.

---

## Tests and CI

The repository includes tests for core public invariants including:

- 12-module bundle construction;
- context/risk roles staying out of directional votes;
- unavailable evidence remaining unavailable;
- security flags surfacing as risk anomalies;
- consensus behavior;
- FlowState behavior;
- Market Twin/reference behavior.

GitHub Actions runs lint and tests on Python 3.11 and 3.12 for pushes and pull requests.

```bash
pytest -q
ruff check src tests
```

---

## Public vs production

This repository is deliberately useful on its own, but it is not a dump of Zynost's commercial backend.

### Public

- evidence contracts;
- deterministic reference builder;
- consensus;
- FlowState reference;
- Market Twin reference;
- public/keyless provider adapters;
- anomalies/thesis contracts;
- API, tests, examples, Docker and CI.

### Private production IP / operations

- exact production scoring/tuning;
- proprietary prompts/model orchestration;
- paid/private provider credentials and routing;
- user/account/billing systems;
- abuse/fraud controls;
- private reliability/operational policies;
- infrastructure/runbooks;
- secrets and user data.

**Private components are not required to run or evaluate this repository.** See [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md).

---

## Provenance

This public project is extracted/adapted from an existing private production codebase rather than fabricated as an isolated demo. The public repository preserves real public commit dates and does not backdate history.

See [`PROVENANCE.md`](PROVENANCE.md) for the development lineage and extraction boundary.

---

## Repository map

```text
.
├── .github/workflows/ci.yml
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── METHODOLOGY.md
├── PROVENANCE.md
├── PUBLIC_PRIVATE_BOUNDARY.md
├── SECURITY.md
├── pyproject.toml
├── examples/
│   └── run_reference.py
├── src/
│   ├── api/
│   ├── evidence/
│   ├── intelligence/
│   └── providers/
└── tests/
```

---

## Relationship to the Zynost ecosystem

```text
Zynost Intelligence
       │
       ├──── structured evidence / decision context
       ▼
Wallet and execution surfaces
       │
       ▼
Zynost Pay / Paymaster
       │
       ▼
BNB Smart Chain
```

The long-term goal is to let evidence improve user understanding and transaction safety while preserving explicit user authorization and self-custody boundaries.

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Contributions should preserve the evidence-first architecture, explicit missing-data semantics and deterministic/AI separation.

---

## Security

Do not commit credentials, private keys, user data or production infrastructure secrets. See [`SECURITY.md`](SECURITY.md).

---

## License

Apache License 2.0. The license covers this public repository; Zynost names, logos and commercial production systems remain separate from the code license.

---

## Disclaimer

This repository provides research and software infrastructure. It does not guarantee market outcomes and is not financial advice.