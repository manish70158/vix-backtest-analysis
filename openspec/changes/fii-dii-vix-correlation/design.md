## Context

See proposal.md for motivation. The existing VIX backtest (v6) covers 109 expiry days (Jun 2024 - Jul 2026). The FII/DII dataset covers 243 trading days (Aug 2025 - Aug 2026). The overlap is 50 expiry days — sufficient for directional analysis but not for high-confidence statistical significance on subgroups.

Key data characteristics:
- FII/DII data contains daily net OI positions (futures index net, call net, put net) plus categorical direction signals for FII, DII, Pro traders, and Clients
- VIX expiry data contains per-expiry OHLC, VIX levels, predicted vs actual range, blowout classification, and move direction
- Both datasets use date as the join key (ISO format YYYY-MM-DD)

## Goals / Non-Goals

**Goals:**
- Determine if FII/DII positioning adds predictive power for expiry-day blowouts beyond the 22% base rate
- Identify specific FII/DII conditions that correlate with larger-than-expected expiry moves
- Produce reusable merged dataset for further exploration
- Quantify the lift (if any) of FII-based rules as pre-market signals

**Non-Goals:**
- Building a live trading system or alert mechanism (that's a separate change)
- Backtesting P&L of FII-based strategies (future work, requires options pricing data)
- Modifying existing VIX backtest scripts or results
- Extending the FII/DII dataset backward (data only starts Aug 2025)

## Decisions

### Decision 1: Join strategy — same-day only vs T-1 lookback

**Choice**: Include BOTH same-day FII data AND T-1 (previous trading day) FII data.

**Rationale**: FII daily data reflects end-of-day positions. On expiry day, the morning positioning is from previous close. So T-1 FII data is what's actually "known" before expiry open. Same-day data confirms whether FII was active during expiry. Both views are informative.

**Alternative considered**: Same-day only — simpler, but misses the pre-market signal angle which is the primary motivation.

### Decision 2: Derived features to compute

**Choice**: Compute these derived signals from raw FII data:
- `fii_pcr`: FII put-call ratio = fii_put_net / abs(fii_call_net)
- `fii_net_sentiment`: Combined = fii_fut_idx_net + fii_call_net - fii_put_net (higher = more bullish)
- `fii_put_change`: Day-over-day change in fii_put_net (building puts = fear)
- `fii_direction_matches_market`: Boolean — did FII direction match actual market direction?
- `consensus_count`: How many of FII/DII/Pro/Client agree on direction

**Rationale**: Raw net OI values are regime-dependent (absolute levels shift over time). Ratios and changes are more comparable across periods.

### Decision 3: Statistical methods

**Choice**: Use Pearson correlation for numeric-numeric, point-biserial for numeric-binary, chi-squared for categorical-categorical, and simple conditional probability tables for practical trading rules.

**Rationale**: With n=50, parametric tests are borderline. Report correlations with p-values so the user can judge significance. Emphasize practical lift (blowout rate under condition vs baseline) over statistical purity.

### Decision 4: Output location

**Choice**: Script in `.claude/skills/nifty-expiry-vix-backtest/scripts/`, outputs in project root alongside existing VIX results.

**Rationale**: Follows existing project convention — v1-v6 scripts are in skills/scripts, output CSV/JSON in project root.

## Risks / Trade-offs

- **[Small sample]** 50 overlapping days may be too few for robust subgroup analysis (e.g., "FII Bearish + blowout" may have only 3-5 cases) → Mitigation: Report sample sizes with every finding, flag n<10 as unreliable
- **[Regime dependency]** FII net OI levels shifted significantly over the period (range: -87K to -279K for futures) → Mitigation: Use ratios and changes rather than absolute levels
- **[Survivorship bias]** FII direction is derived from thresholds that may be tuned to this period → Mitigation: Use raw numeric values for correlation, categorical only for cross-tabs
- **[No causation]** Even strong correlation doesn't mean FII causes blowouts — could be coincidental or both driven by same underlying factor → Mitigation: Frame findings as "associated with" not "predicts"
