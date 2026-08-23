# Architecture

## Goal

The public Zynost intelligence reference demonstrates the core design principle used by the production system:

> Evidence first. AI second.

The open-source package is intentionally useful without any language model, database, paid provider, user account or Zynost production credential.

## Data flow

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
             ├──────────────┐
             ▼              ▼
        FlowState       Anomalies
             │              │
             └──────┬───────┘
                    ▼
             Thesis Contract
                    │
                    ▼
       API / UI / optional AI
```

## Package map

### `src/evidence/`

- `model.py` — provider-agnostic evidence schema.
- `roles.py` — module semantic roles and stance mapping.
- `builder.py` — 12-module deterministic reference bundle builder.
- `consensus.py` — weighted deterministic posture aggregation.

### `src/providers/`

- `public_institutional.py` — keyless/public Deribit options, CFTC positioning and stablecoin-flow adapters with bounded caching and failure handling.

### `src/intelligence/`

- `flow_state.py` — deterministic regime dimensions and drift comparison.
- `market_twin.py` — point-in-time historical analogue matching reference.
- `thesis.py` — anomalies plus bounded confirmation/invalidation conditions.
- `pipeline.py` — end-to-end public analysis orchestration.

### `src/api/`

- `app.py` — FastAPI `/health` and `/analyze` endpoints.

## Trust boundaries

The deterministic evidence layer does not require an LLM. Optional AI in the commercial product consumes bounded evidence produced by this layer rather than inventing market measurements itself.

The public package also does not require access to the Zynost production database, user system, billing system, provider secrets or proprietary tuning.

## Failure philosophy

Missing data remains missing. Provider failures are represented as unavailable coverage and should not be silently converted into neutral or synthetic values.

## Security and privacy

No production credentials, user PII, wallet keys, internal infrastructure secrets or private operational runbooks belong in this repository. See `PUBLIC_PRIVATE_BOUNDARY.md` and `SECURITY.md`.
