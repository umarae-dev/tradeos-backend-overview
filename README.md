# Zynost — AI Trading Intelligence Backend

**Trade with a real edge.**

Zynost is a decision-intelligence platform for crypto traders. Instead of asking a single AI model to eyeball a chart and guess, a query fans out across a panel of specialist agents — each one constrained to a narrow, well-defined job and a strict JSON schema — and the disagreements between them get argued out before a verdict ever reaches the user.

**Live:** https://app.zynost.com

## The panel, not a single model

Eleven specialist agents look at a coin from angles that don't overlap: technical structure (trend, momentum, support/resistance from real precomputed swing levels — the agent narrates them, it doesn't invent them), liquidity (volume-to-market-cap, as an execution-risk read), smart-money structure (order-flow-style liquidity-sweep patterns, tempered against real order-book imbalance and futures open interest), on-chain activity, macro sentiment (Fear & Greed as market-wide context, never coin-specific), breaking news, project fundamentals, portfolio concentration, and — for coins with a real contract to inspect — a security scan for mint-authority abuse, honeypot patterns, and holder concentration.

## The part most single-agent tools skip: someone has to argue back

Every one of those signals gets handed to a **Skeptic** agent whose only job is to find contradictions and overlooked risk in the *other* agents' actual numeric outputs, not just their tone. Its objection, plus the underlying signals, go to a **Judge** agent that synthesizes one final bull case, bear case, risk summary, and confidence level — grounded in cited numbers, not vibes. Nothing gets averaged into a mushy consensus; the disagreement itself is part of the output.

## Grading our own homework, honestly

Every trade candidate the system generates — including the ones filtered out before a user ever sees them — gets logged with its entry, stop, target, and the real signal values that produced it. A background job checks each one against live price and marks it win, loss, or expired. A live win-rate only gets shown once at least 20 trades have actually resolved; before that, it says so plainly instead of showing a misleadingly confident number. The one documented backtest we publish internally — 45% win rate, +0.13R per trade, across 180 days and 201 trades — exists specifically because order-book and DEX-liquidity signals have no free historical dataset to backtest against normally, so forward-tracking against real outcomes is the honest substitute, not a shortcut.

## Where the data actually comes from

Live prices and volume come from four centralized exchanges (Binance, KuCoin, Gate.io, MEXC) via direct exchange APIs, plus Binance's perpetual futures market for funding rate and open interest. Coins with no exchange listing still get covered through DEX pool activity across six chains (Ethereum, BSC, Solana, Base, Arbitrum, Polygon). On-chain network activity comes from mempool.space for Bitcoin and a multi-chain block-explorer aggregator for ten more networks. News is pulled and matched to specific coins, not just keyword-matched. Contract security scans run across eight EVM chains. Nothing here is a single point of failure for "the data."

## Stack

FastAPI · PostgreSQL (async SQLAlchemy) · Anthropic Claude for agent reasoning · a multi-source market-data layer spanning CEX, DEX, on-chain, and news APIs

## Status

In active production use, serving live trading intelligence to real, paying users.

---

This repository is a public overview of a closed-source production system. The actual agent prompts, scoring logic, and backend source aren't published here — the same practice trading and fintech platforms generally follow to protect their core methodology.
