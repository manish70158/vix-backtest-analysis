## Why

The VIX backtest (V1-V6) established that VIX underestimates expiry-day ranges by ~25% and identified VIX intraday behavior as the only robust blowout predictor. However, pre-market prediction remains weak. FII/DII positioning data (futures + options net OI) is available daily and could provide a missing pre-market signal — correlating institutional flow direction with VIX blowout days and expiry-day movement patterns.

## What Changes

- Build a correlation analysis script that joins the FII/DII daily positioning data (`fii_dii_backtest_daily_results.csv`) with VIX expiry-day results (`vix_all_expiries_results_v6.csv`)
- Compute correlation metrics between FII/DII direction signals and: blowout occurrence, expiry-day range, move direction, and VIX accuracy
- Analyze whether FII positioning (futures net, call net, put net) on or before expiry day predicts whether VIX will underestimate
- Generate a combined results file with merged FII/DII + VIX features per expiry day
- Produce a summary report with correlation findings and actionable trading signals

## Capabilities

### New Capabilities
- `fii-dii-vix-correlation`: Correlation analysis between FII/DII institutional flow data and VIX expiry-day backtest results — joining on expiry dates, computing statistical correlations, and identifying whether institutional positioning improves blowout prediction

### Modified Capabilities

## Impact

- New Python script in `.claude/skills/nifty-expiry-vix-backtest/scripts/`
- New output CSV/JSON with merged correlation data (50 overlapping expiry days from Aug 2025 - Jul 2026)
- New summary markdown with correlation findings
- No changes to existing VIX backtest scripts or results
- Data dependency: requires both `fii_dii_backtest_daily_results.csv` and `vix_all_expiries_results_v6.csv` to be present
