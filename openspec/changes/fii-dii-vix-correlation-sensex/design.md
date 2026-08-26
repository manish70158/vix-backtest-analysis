## Context

See proposal.md for motivation. The existing Sensex VIX backtest covers 318 expiry days (Jun 2020 - Jul 2026, 6 years). The FII/DII dataset covers 256 trading days (Aug 2025 - Aug 2026). The overlap is 46 Sensex expiry days — smaller than Nifty's 50-day overlap, and notably the blowout rate in this overlap period is only 8.7% (4 out of 46 days) compared to the full 23.9% base rate across all 318 expiries. This low blowout count in the overlap severely limits subgroup analysis.

Key data characteristics:
- FII/DII data contains daily net OI positions (futures index net, call net, put net) plus categorical direction signals for FII, DII, Pro traders, and Clients
- Sensex VIX expiry data contains per-expiry OHLC, VIX levels, predicted vs actual range, blowout classification, and move direction
- Both datasets use date as the join key (ISO format YYYY-MM-DD)
- FII/DII data tracks Nifty positioning — correlation with Sensex is indirect but high due to index co-movement (~0.95 correlation between Nifty and Sensex)
- Sensex expiry days differ from Nifty (BSE schedule: Friday pre-2025, Tuesday Jan-Sep 2025, Thursday from Sep 2025)

## Goals / Non-Goals

**Goals:**
- Determine if FII/DII positioning adds predictive power for Sensex expiry-day blowouts beyond the 23.9% base rate
- Identify specific FII/DII conditions that correlate with larger-than-expected Sensex expiry moves
- Compare Sensex correlation results with existing Nifty findings to assess whether the relationship is index-specific or market-wide
- Produce reusable merged dataset for further exploration
- Quantify the lift (if any) of FII-based rules as pre-market signals for Sensex

**Non-Goals:**
- Building a live trading system or alert mechanism (that's a separate change)
- Backtesting P&L of FII-based strategies (future work, requires options pricing data)
- Modifying existing Sensex VIX backtest scripts or results
- Extending the FII/DII dataset backward (data only starts Aug 2025)
- Creating Sensex-specific FII/DII data (institutional data is Nifty-based; we use it as a proxy)

## Decisions

### Decision 1: Join strategy — same-day only vs T-1 lookback

**Choice**: Include BOTH same-day FII data AND T-1 (previous trading day) FII data.

**Rationale**: Same logic as Nifty analysis — FII daily data reflects end-of-day positions. On Sensex expiry day, the morning positioning is from previous close. So T-1 FII data is what's actually "known" before expiry open. Same-day data confirms whether FII was active during expiry. Both views are informative.

### Decision 2: Market direction alignment

**Choice**: Use Sensex's own open-close direction from `vix_sensex_6y_results.csv` (derived from actual_open_close_pct sign) rather than the Nifty-based Market_Direction from FII/DII data.

**Rationale**: While Nifty and Sensex are ~95% correlated, on individual days they can diverge (especially around BSE-specific expiry dynamics). Using Sensex's actual direction for `fii_direction_matches_market` ensures we measure FII signal accuracy against the correct index.

### Decision 3: Derived features to compute

**Choice**: Compute these derived signals from raw FII data:
- `fii_pcr`: FII put-call ratio = fii_put_net / abs(fii_call_net)
- `fii_net_sentiment`: Combined = fii_fut_idx_net + fii_call_net - fii_put_net (higher = more bullish)
- `fii_put_change`: Day-over-day change in fii_put_net (building puts = fear)
- `fii_direction_matches_sensex`: Boolean — did FII direction match actual Sensex direction?
- `consensus_count`: How many of FII/DII/Pro/Client agree on direction

**Rationale**: Same as Nifty analysis. Raw net OI values are regime-dependent (absolute levels shift over time). Ratios and changes are more comparable across periods. The key difference is measuring direction accuracy against Sensex rather than Nifty.

### Decision 4: Statistical methods

**Choice**: Use Pearson correlation for numeric-numeric, point-biserial for numeric-binary, chi-squared for categorical-categorical, and simple conditional probability tables for practical trading rules.

**Rationale**: With n=46 and only 4 blowouts, parametric tests will have very low power. Report correlations with p-values and clearly flag the small blowout sample. Emphasize practical findings over statistical significance. Consider using the broader "diff_pct > 0" condition (any underperformance) alongside strict blowout classification to increase effective sample size.

### Decision 5: Output location

**Choice**: All Sensex-related scripts and outputs consolidated in `sensex-analysis/` directory at project root.

**Rationale**: Keeps all Sensex analysis artifacts (data files, scripts, summaries) in one place rather than scattered across project root and skills directories. The directory contains: VIX backtest results, FII correlation data, participant-wise daily data, and all analysis scripts.

### Decision 7: Separate FII and PRO data

**Choice**: Fetch participant-wise OI data with separate columns for FII, PRO, DII, and Client from NSE archives (`fao_participant_oi_DDMMYYYY.csv`).

**Rationale**: NSDL only provides aggregated "FPI" data. The NSE participant-wise OI archive provides granular breakdowns for all 4 participant categories (FII, Proprietary, DII, Client) with separate futures and options positions. This allows independent analysis of FII vs PRO positioning signals.

### Decision 8: BSE India data access

**Choice**: Use NSE participant-wise OI archives as the primary data source. BSE India's API is inaccessible programmatically.

**Rationale**: BSE India (api.bseindia.com) is protected by Akamai WAF that blocks all programmatic access — Python requests, tls_client, curl, and headless Playwright all get denied. NSE's participant-wise OI data covers the same institutional positioning (FII F&O activity is market-wide, not exchange-specific) and is freely accessible at `archives.nseindia.com`.

### Decision 6: Comparison with Nifty results

**Choice**: Include a dedicated comparison section in the summary report showing Sensex vs Nifty correlation findings side-by-side.

**Rationale**: The primary value-add of this analysis (beyond replicating Nifty) is determining whether FII/DII correlations are consistent across indices or index-specific. A direct comparison makes this actionable.

## Risks / Trade-offs

- **[Very small blowout sample]** Only 4 blowouts in 46 overlap days (8.7% vs 23.9% base rate) — individual signal vs blowout cross-tabs may have 0-2 cases per cell → Mitigation: Also analyze continuous outcomes (actual_range_pct, diff_pct) and use "above median range" as an alternative binary target
- **[Proxy data]** FII/DII positioning is Nifty-based, not Sensex-specific — institutional flow may not reflect Sensex-specific dynamics → Mitigation: Acknowledge this limitation; Nifty-Sensex correlation is ~95% so proxy is reasonable
- **[Different expiry schedule]** Sensex expiry days (Tue/Thu) may not coincide with Nifty's Thursday expiry, meaning FII positioning may be less relevant on non-Nifty-expiry days → Mitigation: Flag whether each Sensex expiry is also a Nifty expiry day and analyze separately
- **[Regime dependency]** FII net OI levels shifted significantly over the period → Mitigation: Use ratios and changes rather than absolute levels
- **[No causation]** Even strong correlation doesn't mean FII causes blowouts → Mitigation: Frame findings as "associated with" not "predicts"
