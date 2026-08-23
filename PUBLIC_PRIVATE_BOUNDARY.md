# Public / Private Boundary

This repository is the open-source reference implementation of Zynost's evidence-first crypto decision-intelligence architecture.

## Public in this repository

- provider-agnostic 12-module evidence contract;
- deterministic evidence normalization;
- semantic role separation: directional, context and risk-gate evidence;
- deterministic consensus;
- FlowState reference regime engine;
- Market Twin point-in-time analogue matching reference;
- anomaly and thesis-condition layers;
- keyless/public institutional-data adapters;
- FastAPI reference API;
- tests, examples, Docker and CI.

## Private in the commercial production system

- production scoring/tuning and internal thresholds;
- production prompts and model orchestration;
- paid/private data-provider credentials and routing;
- user/account/billing systems;
- proprietary reliability and operational policy;
- abuse/fraud controls;
- private infrastructure, monitoring and runbooks;
- database credentials, API keys, secrets and user data.

## Reproducibility rule

The private components are not required to install, run, test or evaluate the public reference implementation. The public package uses explicit reference defaults where production tuning is proprietary.

This boundary is intentional: open source should be useful and independently executable without pretending that a commercial production backend has no private operational or proprietary layer.
