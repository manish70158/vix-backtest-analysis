## 1. Setup

- [x] 1.1 Create `fii-pro-alignment-analysis/` folder in the project root. Verify folder exists with `ls -d fii-pro-alignment-analysis/`.

## 2. Core Analysis Script

- [x] 2.1 Create `fii-pro-alignment-analysis/analyze_fii_pro_alignment.py` with CSV reading and view bucketing logic. The script SHALL map `fii_view`/`pro_view` into Bullish/Bearish/Neutral buckets per design decision #1 and classify each day's alignment as Bullish Alignment, Bearish Alignment, Mixed, or Neutral/Unclear. Verify by running the script and confirming alignment column is populated for all rows.

- [x] 2.2 Add first-half/second-half direction classification using `move_direction` column. For alignment days, classify outcome as "Worked then Reversed" or "Against then Recovered" per design decision #2. Also compute magnitudes using `intraday_high_pct` and `intraday_low_pct`. Verify by spot-checking 5 rows from the output CSV against manual classification.

- [x] 2.3 Add "Strong Alignment" sub-classification for days where both FII and PRO have strong views (Strong Bullish/Bullish or Strong Bearish/Bearish, excluding "Mildly" variants). Verify by confirming strong alignment count is a subset of total alignment count.

- [x] 2.4 Add close outcome classification ("Worked and Remained" / "Reversed by Close") based on `actual_open_close_pct` per design decision #3. For bullish alignment, close > open = Worked and Remained. For bearish alignment, close < open = Worked and Remained. Verify by running script and confirming `close_outcome` column is populated for all alignment days.

- [x] 2.5 Add VIX half-range exhaustion classification per design decision #4. Compare aligned-direction move (`intraday_high_pct` for bullish, `abs(intraday_low_pct)` for bearish) against `vix_predicted_move_pct / 2`. Classify as "Exceeded Half then Reversed" or "Reversed Before Half". Days with missing VIX data get empty value. Verify by running script and confirming `vix_exhaustion` column is populated for alignment days with VIX data (578 of 582).

## 3. Statistical Analysis and Report Generation

- [x] 3.1 Add summary statistics computation: total alignment days vs total trading days, breakdown by alignment type (bullish vs bearish), follow-through rate, reversal rate, and average magnitudes for each alignment type. Verify by running the script and confirming the markdown report contains an "Overall Summary" section with counts and percentages.

- [x] 3.1a Add "Worked and Remained" report section with close-outcome rates overall, by bullish/bearish alignment, by expiry/non-expiry, by VIX regime, and by year. Verify by confirming the report contains a "Worked and Remained: Did the Aligned View Win by Close?" section with all sub-tables.

- [x] 3.1b Add "VIX Half-Range Exhaustion" report section with: overall exhaustion rates, cross-tab of exhaustion × close outcome, breakdown by bullish/bearish alignment (count, %, Worked and Remained rate, avg open→close%), and exhaustion rates by VIX regime. Verify by confirming the report contains a "VIX Half-Range Exhaustion: Did the Move Exhaust Before Reversing?" section with all sub-tables.

- [x] 3.2 Add expiry vs non-expiry day comparison using the `is_nifty_expiry` column. Verify by confirming the report contains an "Expiry vs Non-Expiry" section with separate statistics for each group.

- [x] 3.3 Add VIX regime breakdown using `vix_open` with bands <15, 15–20, 20–30, >30. Verify by confirming the report contains a "VIX Regime Analysis" section with statistics per band.

- [x] 3.4 Add year-over-year trend analysis. Verify by confirming the report contains a "Year-over-Year Trends" table showing alignment and reversal rates per year.

- [x] 3.5 Add key findings and trading implications section that summarizes the most actionable patterns discovered. Verify by confirming the report ends with a "Key Findings" section.

## 4. Output Generation

- [x] 4.1 Generate per-day results CSV (`fii-pro-alignment-analysis/fii_pro_alignment_results.csv`) with columns: date, fii_view, pro_view, fii_bucket, pro_bucket, alignment, strong_alignment, move_direction, outcome_classification, close_outcome, vix_exhaustion, vix_predicted_move_pct, intraday_high_pct, intraday_low_pct, actual_open_close_pct, actual_range_pct, is_nifty_expiry, vix_open, vix_regime, year. Verify by opening the CSV and confirming all columns are present and populated.

- [x] 4.2 Generate markdown report (`fii-pro-alignment-analysis/FII_PRO_ALIGNMENT_REPORT.md`) with all sections from tasks 3.1–3.5 including 3.1a and 3.1b. Verify by running `python3 fii-pro-alignment-analysis/analyze_fii_pro_alignment.py` and confirming the report file is created with all expected sections.
