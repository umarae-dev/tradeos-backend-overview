# GoroAI / TradeOS — AI Trading Intelligence Backend

The backend powering GoroAI, a multi-agent AI system that analyzes crypto markets across technicals, on-chain data, sentiment, news, macro conditions, and portfolio risk — then produces structured, explainable trade plans.

**Live app:** https://app.zynost.com

## What it does

- Runs a panel of specialized AI agents (technical analysis, liquidity, smart-money structure, on-chain intelligence, sentiment, news, macro, risk management, a "skeptic" agent that challenges other agents' conclusions, and a final judge that synthesizes a verdict).
- Tracks system-generated trade plans against real market outcomes for transparent, auditable performance history.
- Handles authentication, subscriptions/credits, portfolio tracking, watchlists, and alerts.
- Accepts payment via Zynost Pay (its own non-custodial gateway) for Pro subscriptions.

## Stack

FastAPI · PostgreSQL (SQLAlchemy async) · Anthropic Claude (agent reasoning) · multi-source market data aggregation (CEX + on-chain + news)

## Status

In active production use, serving live trading intelligence to real users.

---

This repository is a public overview of a closed-source production system. The actual agent prompts, scoring logic, and backend source are not published — the same practice trading/fintech platforms generally follow to protect their core methodology.
