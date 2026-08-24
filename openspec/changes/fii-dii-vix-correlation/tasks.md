## 1. Data Loading and Merge

- [x] 1.1 Create script `correlate_fii_dii_vix.py` in `.claude/skills/nifty-expiry-vix-backtest/scripts/` that loads both CSVs with proper error handling if files are missing. Verify: script runs without error and prints row counts for both DataFrames.
- [x] 1.2 Implement inner join on date column between FII/DII data and VIX expiry results. Verify: merged DataFrame has exactly 50 rows (the known overlap) with all columns from both sources preserved.
- [x] 1.3 Add T-1 lookback — for each expiry date, also attach the previous trading day's FII/DII data as `t1_fii_fut_idx_net`, `t1_fii_call_net`, `t1_fii_put_net`, `t1_FII_Direction`. Verify: T-1 columns populated for at least 49/50 rows (first row may be NaN).

## 2. Derived Features

- [x] 2.1 Compute `fii_pcr` (fii_put_net / abs(fii_call_net)), `fii_net_sentiment` (fii_fut_idx_net + fii_call_net - fii_put_net), and `fii_put_change` (day-over-day change in fii_put_net). Verify: all three columns present with no unexpected NaN beyond first row.
- [x] 2.2 Compute `is_blowout` binary column from vix_accuracy, `fii_direction_matches_market` boolean, and `consensus_count` (number of FII/DII/Pro/Client matching market direction). Verify: is_blowout matches count of "Underestimated" rows; consensus_count ranges 0-4.

## 3. Correlation Analysis

- [x] 3.1 Compute Pearson and point-biserial correlations between each FII numeric signal (fii_fut_idx_net, fii_call_net, fii_put_net, fii_pcr, fii_net_sentiment, fii_put_change) and is_blowout, actual_range_pct. Include p-values. Verify: correlation matrix printed with all values between -1 and 1, p-values between 0 and 1.
- [x] 3.2 Compute same correlations using T-1 FII data (pre-market observable signals). Verify: separate correlation table for T-1 signals printed.
- [x] 3.3 Build cross-tabulation of FII_Direction × is_blowout, DII_Direction × is_blowout, and consensus conditions × is_blowout. Report count, percentage, and blowout rate per cell. Verify: all contingency tables have row/column totals summing to 50.

## 4. Predictive Rule Testing

- [x] 4.1 Test FII-based blowout prediction rules: (a) FII_Direction == "Bearish", (b) fii_pcr above median, (c) fii_put_change > 0 (puts increasing), (d) T-1 FII_Direction == "Bearish". For each, report: triggers, blowout rate, lift vs 22% base, sample size. Verify: lift values computed correctly (rule_blowout_rate / 0.22).
- [x] 4.2 Test combination rules: (a) FII Bearish + VIX < 14, (b) fii_pcr above 75th percentile, (c) consensus_count >= 3 matching one direction. Report same metrics. Verify: combination rules produce non-empty subsets.
- [x] 4.3 Compare FII signals vs the validated VIX intraday signal (vix_change > 0.5 → 59% blowout). Report whether any FII pre-market signal approaches the intraday VIX signal's 59% precision. Verify: comparison table with both signal types side by side.

## 5. Output Generation

- [x] 5.1 Write merged DataFrame with all derived columns to `fii_dii_vix_correlation.csv` in project root. Verify: file exists, has 50 rows, includes original + derived columns.
- [x] 5.2 Write JSON output with correlation matrices, cross-tabs, rule test results, and metadata to `fii_dii_vix_correlation.json`. Verify: valid JSON that loads without error, contains keys for correlations, cross_tabs, rules, metadata.
- [x] 5.3 Generate `FII_DII_VIX_CORRELATION_SUMMARY.md` with executive summary, correlation findings, rule test results, and actionable trading implications. Verify: markdown file exists with at least sections for Summary, Correlations, Rules, and Implications.
