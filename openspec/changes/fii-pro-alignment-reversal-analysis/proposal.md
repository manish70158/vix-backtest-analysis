## Why

We have 1,482 daily rows of Nifty intraday data (Aug 2020–Aug 2026) with T+1 FII and PRO participant views (`fii_view`, `pro_view`) and intraday direction patterns (`move_direction`: "Down to Up" or "Top to Down"). When FII and PRO align on the same directional view (both bullish or both bearish), the market may initially move in that direction in the first half but then reverse in the second half. Understanding this alignment-then-reversal behavior has direct trading implications for managing intraday positions around institutional consensus days.

## What Changes

- Create a new `fii-pro-alignment-analysis/` folder in the project root to house the analysis script, output CSV, and markdown report.
- Build a Python analysis script that:
  - Reads `vix_fii_t1_intraday_daily_results.csv`
  - Classifies FII and PRO views into bullish/bearish/neutral buckets
  - Identifies "alignment days" where both FII and PRO share the same directional bias (both bullish or both bearish)
  - For each alignment day, determines: did the first-half move match the aligned direction? Did the second half reverse?
  - Classifies close outcome as "Worked and Remained" (close validated the aligned view) or "Reversed by Close" (close opposed the aligned view)
  - Uses `move_direction` ("Down to Up" = bearish first half → bullish second half; "Top to Down" = bullish first half → bearish second half) plus `intraday_high_pct` and `intraday_low_pct` for magnitude
  - Computes win/reversal rates, close-outcome rates, average magnitudes, breakdown by alignment type (bullish vs bearish), expiry vs non-expiry, and VIX regime
- Generate a detailed CSV with per-day alignment classification and reversal flags
- Generate a markdown report with summary statistics, tables, and key findings

## Capabilities

### New Capabilities
- `fii-pro-alignment-reversal`: Analysis of market behavior when FII and PRO participants align on the same directional view — specifically whether the market follows through or reverses intraday, and whether the close ultimately validates the aligned direction ("Worked and Remained").

### Modified Capabilities
(none)

## Impact

- New folder: `fii-pro-alignment-analysis/`
- New files: analysis Python script, results CSV, markdown report
- Reads from existing: `vix_fii_t1_intraday_daily_results.csv`
- Dependencies: Python 3, pandas, no new external packages
