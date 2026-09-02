## 1. Data Loading and Merge

- [x] 1.1 Create script `correlate_fii_dii_vix_sensex.py` in `.claude/skills/sensex-expiry-vix-backtest/scripts/` that loads both CSVs (`fii_dii_backtest_daily_results.csv` and `vix_sensex_6y_results.csv`) with proper error handling if files are missing. Verify: script runs without error and prints row counts for both DataFrames.
- [x] 1.2 Implement inner join on date column between FII/DII data and Sensex VIX expiry results. Handle column name differences (FII uses `Date`, Sensex uses `date`). Verify: merged DataFrame has exactly 46 rows (the known overlap) with all columns from both sources preserved.
- [x] 1.3 Add T-1 lookback — for each Sensex expiry date, also attach the previous trading day's FII/DII data as `t1_fii_fut_idx_net`, `t1_fii_call_net`, `t1_fii_put_net`, `t1_FII_Direction`. Verify: T-1 columns populated for at least 45/46 rows (first row may be NaN).
- [x] 1.4 Add `is_nifty_expiry_day` flag — for each Sensex expiry date, check if it's also a Nifty expiry (Thursday) to control for dual-expiry effects. Verify: column populated for all 46 rows.

## 2. Derived Features

- [x] 2.1 Compute `fii_pcr` (fii_put_net / abs(fii_call_net)), `fii_net_sentiment` (fii_fut_idx_net + fii_call_net - fii_put_net), and `fii_put_change` (day-over-day change in fii_put_net). Verify: all three columns present with no unexpected NaN beyond first row.
- [x] 2.2 Derive Sensex market direction from `actual_open_close_pct` (positive = Bullish, negative = Bearish, near-zero = Neutral). Compute `is_blowout` binary column from vix_accuracy == "Underestimated". Verify: is_blowout has exactly 4 True values; sensex_direction populated for all 46 rows.
- [x] 2.3 Compute `fii_direction_matches_sensex` boolean (FII direction matches Sensex direction) and `consensus_count` (number of FII/DII/Pro/Client matching Sensex direction). Verify: consensus_count ranges 0-4.

## 3. Correlation Analysis

- [x] 3.1 Compute Pearson and point-biserial correlations between each FII numeric signal (fii_fut_idx_net, fii_call_net, fii_put_net, fii_pcr, fii_net_sentiment, fii_put_change) and is_blowout, actual_range_pct, diff_pct. Include p-values. Verify: correlation matrix printed with all values between -1 and 1, p-values between 0 and 1.
- [x] 3.2 Compute same correlations using T-1 FII data (pre-market observable signals). Verify: separate correlation table for T-1 signals printed.
- [x] 3.3 Build cross-tabulation of FII_Direction x is_blowout, DII_Direction x is_blowout, and consensus conditions x is_blowout. Report count, percentage, and blowout rate per cell. Verify: all contingency tables have row/column totals summing to 46. Flag cells with n < 5.
- [x] 3.4 Compute correlations for the alternative target: `above_median_range` (actual_range_pct above 46-day median) to provide more statistical power than the 4-blowout binary. Verify: above_median_range has ~23 True values; correlation table produced.

## 4. Predictive Rule Testing

- [x] 4.1 Test FII-based blowout prediction rules: (a) FII_Direction == "Bearish", (b) fii_pcr above median, (c) fii_put_change > 0 (puts increasing), (d) T-1 FII_Direction == "Bearish". For each, report: triggers, blowout rate, lift vs 8.7% overlap base rate (and vs 23.9% full base rate), sample size. Verify: lift values computed correctly.
- [x] 4.2 Test combination rules: (a) FII Bearish + VIX < 14, (b) fii_pcr above 75th percentile, (c) consensus_count >= 3 matching one direction, (d) FII Bearish + is_nifty_expiry_day. Report same metrics. Verify: combination rules produce non-empty subsets.
- [x] 4.3 Compare Sensex FII signal results with Nifty correlation findings. Report whether correlations are stronger, weaker, or similar. Verify: side-by-side comparison table produced.
- [x] 4.4 Test FII rules against the alternative target (above_median_range) for higher statistical power. Report precision, recall, and lift for each rule. Verify: all rules tested against both blowout and above_median_range targets.

## 5. Output Generation

- [x] 5.1 Write merged DataFrame with all derived columns to `fii_dii_vix_correlation_sensex.csv` in `sensex-analysis/`. Verify: file exists, has 305 rows (6-year data), includes original + derived columns.
- [x] 5.2 Write JSON output with correlation matrices, cross-tabs, rule test results, comparison with Nifty, and metadata to `fii_dii_vix_correlation_sensex.json`. Verify: valid JSON that loads without error, contains keys for correlations, cross_tabs, rules, nifty_comparison, metadata.
- [x] 5.3 Generate `FII_DII_VIX_CORRELATION_SENSEX_SUMMARY.md` with executive summary, correlation findings, rule test results, Nifty vs Sensex comparison, and actionable trading implications. Include clear caveats about the 4-blowout sample size. Verify: markdown file exists with sections for Summary, Correlations, Rules, Nifty Comparison, Limitations, and Implications.

## 6. Participant-wise Daily Data (FII/PRO separate)

- [x] 6.1 Create `fetch_bse_participant_data.py` that fetches daily participant-wise OI from NSE archives with separate FII, PRO, DII, Client columns. Source: `archives.nseindia.com/content/nsccl/fao_participant_oi_DDMMYYYY.csv`. Verify: script runs and produces `sensex_participant_wise_daily.csv` with separate participant columns.
- [x] 6.2 Compute daily changes (day-over-day position change) and direction signals (Bullish/Bearish/Neutral) independently for FII and PRO. Verify: `fii_direction`, `fii_stance`, `pro_direction`, `pro_stance` columns present.
- [x] 6.3 Include both absolute positions (net long-short) and derived signals (stance, direction) for all 4 participants. Verify: columns for `{fii,pro,dii,client}_{fut_idx_net,call_net,put_net,fut_daily,direction,stance}`.

## 7. Directory Consolidation

- [x] 7.1 Move all Sensex-related files (CSV, JSON, XLSX, MD, PY) from project root and `sensex-fii-dii-correlation/` into `sensex-analysis/` at project root. Verify: `sensex-analysis/` contains all Sensex artifacts, old `sensex-fii-dii-correlation/` removed.
- [x] 7.2 Update script path references to use relative paths from new directory. Verify: all scripts run from `sensex-analysis/` without path errors.
- [x] 7.3 Update OpenSpec proposal, design, and tasks to reflect new directory structure and participant data capabilities. Verify: all spec files reference `sensex-analysis/` correctly.
