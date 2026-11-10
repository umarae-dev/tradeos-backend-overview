# Zynost Public Intelligence Reference

> **Evidence first. AI second. A runnable open-source reference for deterministic crypto decision intelligence.**

Zynost turns fragmented market, derivatives, on-chain, security and macro observations into a structured evidence bundle before any optional language-model explanation is allowed to run.

This repository is **real executable source code**, not a documentation-only showcase. It contains a provider-agnostic 12-module evidence engine, deterministic consensus, FlowState regime analysis, Market Twin historical-analogue logic, public institutional-data adapters, a FastAPI endpoint, tests, Docker and CI.

**Production product:** https://zynost.com  
**Application:** https://app.zynost.com  
**License:** Apache-2.0  
**Python:** 3.11+  
**Public/private boundary:** [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md)  
**Release verification:** [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)

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
- [`src/providers/public_institutional.py`](src/providers/public_institutional.py) — keyless/public Deribit, CFTC and stablecoin-flow adapters;
- [`src/api/app.py`](src/api/app.py) — FastAPI `POST /analyze` endpoint;
- [`scripts/check_public_repo.py`](scripts/check_public_repo.py) — CI guard for forbidden sensitive files and obvious credential material.

Some modules are directly derived from production-safe implementation patterns; others are public reference implementations created so the repository can run independently. Exact production weights, prompts, provider credentials, commercial tuning and operational controls are intentionally not included.

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

On Windows PowerShell:

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

Then use:

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

The image starts the same public FastAPI service used by the local quick start.

---

## CI and public-source safety

The repository's GitHub Actions workflow checks the project on Python 3.11 and 3.12 and performs:

- public-repository secret/sensitive-file guard;
- Python compile check;
- import smoke test;
- Ruff static checks;
- pytest suite;
- executable reference example;
- independent Docker build.

The source-control defaults also ignore `.env`, private-key formats, local virtual environments and build artifacts. These checks reduce accidental disclosure risk, but they do not replace human review before publishing production-derived code.

See [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md) before a tagged release or hackathon submission.

---

## Evidence contract

Every module exposes explicit metadata rather than hiding uncertainty:

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

Unavailable data is represented as unavailable. It is not silently replaced with a neutral-looking measurement.

---

## Evidence roles: not every fact gets a vote

The public engine separates modules into three semantic roles:

- **directional** — may contribute to bullish/bearish posture;
- **context** — adds interpretation but does not automatically vote;
- **risk_gate** — can surface conditions that weaken/invalidate a thesis without pretending to predict direction.

This prevents generic keyword scoring where, for example, "high" network activity and "high" volatility are mistakenly treated as equivalent signals.

---

## Deterministic consensus

Consensus is calculated from the directional evidence subset using explicit coverage/strength weights. Context and risk-gate evidence remain visible in the output but do not become fake directional votes.

The public formulas are **reference defaults**. They are intentionally not represented as the exact proprietary production tuning used by Zynost.

---

## FlowState

FlowState combines observable evidence into higher-level market-condition dimensions such as:

- Fresh Capital;
- Leverage Dependency;
- Holder Pressure;
- Execution Quality;
- Supply Shock.

It then produces an interpretable regime such as Organic Accumulation, Leveraged Markup, Distribution into Strength, Liquidity Vacuum, Supply Overhang or Balanced Transition.

`build_flow_shift()` also compares consecutive states without requiring a language model.

---

## Market Twin

The public Market Twin reference performs point-in-time historical analogue matching. Its important safeguards include:

- current feature coverage requirements;
- robust scaling;
- historical anchors strictly before the current observation time;
- spacing between selected analogues;
- minimum analogue requirements;
- multi-horizon return distributions;
- adverse/favorable excursion reporting;
- explicit "collecting history" state instead of fabricated forecasts.

Historical analogues describe distributions. They are not guaranteed forecasts.

---

## Public institutional adapters

The repository includes a production-derived, keyless public-data module for:

- Deribit options summaries for BTC/ETH;
- official CFTC weekly positioning where supported;
- public stablecoin-supply flow data.

It includes bounded caching and failure handling. Provider failure returns unavailable data rather than invented evidence.

These adapters are optional; the core pipeline can be run entirely with caller-supplied observations and local fixtures.

---

## Public / private boundary

This repository is an intentionally scoped open-source extraction of reusable architecture from a wider commercial system.

### Public here

- evidence schemas and roles;
- deterministic public reference formulas;
- provider-agnostic evidence builder;
- deterministic consensus;
- FlowState reference implementation;
- Market Twin point-in-time matcher;
- public/keyless provider adapters;
- anomaly/thesis contracts;
- FastAPI interface;
- tests, Docker, CI and examples.

### Private production components

- production API/provider credentials;
- database credentials and user data;
- production prompts and model-routing configuration;
- proprietary production scoring/tuning;
- internal abuse/fraud thresholds;
- operational infrastructure and runbooks;
- private monitoring/configuration;
- commercial account, billing and entitlement systems.

These private components are **not required to compile, test, run or evaluate the public reference implementation**.

Read [`PUBLIC_PRIVATE_BOUNDARY.md`](PUBLIC_PRIVATE_BOUNDARY.md) for the precise disclosure model.

---

## Production lineage and provenance

This public repository was extracted after development of the wider Zynost production intelligence system. It does not fabricate or backdate public history to make the extraction appear older than it is.

[`PROVENANCE.md`](PROVENANCE.md) records the relationship between:

- existing production development;
- safely reusable production-derived modules;
- newly written OSS packaging/reference code;
- intentionally private commercial IP.

This lets reviewers evaluate the open-source component without confusing public-release history with product-development history.

---

## Security

Do not commit:

- API keys;
- database URLs/passwords;
- private keys or seed phrases;
- production signer material;
- user data;
- production prompts/tuning;
- internal abuse thresholds;
- infrastructure secrets.

The CI repository guard blocks common credential patterns and known sensitive filenames, and the PR template requires a public-source safety review for contributions.

See [`SECURITY.md`](SECURITY.md) for responsible reporting.

---

## Repository management

The public project includes:

- CODEOWNERS;
- CI on push/pull request plus manual dispatch;
- Dependabot for Python and GitHub Actions dependencies;
- public-safe bug and feature issue templates;
- a PR checklist that explicitly prevents proprietary production leakage;
- a release checklist for judge/reviewer verification.

This repository is managed as an independent OSS project rather than as a raw mirror of the private production backend.

---

## Related Zynost repositories

- [Zynost Pay overview](https://github.com/umarae-dev/zynost-pay-overview)
- [Zynost Paymaster overview](https://github.com/umarae-dev/zynost-paymaster-overview)
- [UQX BNB contracts overview](https://github.com/umarae-dev/uqx-bnb-contracts-overview)

---

## License

Apache License 2.0. See [`LICENSE`](LICENSE).

Zynost and UQX names, marks and branding are not granted as trademarks merely because source code is open source.

---

## Disclaimer

This project is research tooling. It does not guarantee future performance and is not financial advice. Security and market data can be incomplete; callers should preserve source provenance and treat unavailable coverage honestly.
