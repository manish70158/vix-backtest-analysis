## 1. Setup & Folder Structure

- [x] 1.1 Create `expiry-afternoon-analysis/` folder in the repository root. Verify with `ls expiry-afternoon-analysis/` returning an empty directory.

## 2. Data Loading & Joining

- [x] 2.1 Write the data loading section of `expiry-afternoon-analysis/analyze_afternoon_reversals.py`: read `vix_fii_t1_intraday_expiry_results.csv` into a pandas DataFrame, parse the `date` column, and extract the key columns (`date`, `move_direction`, `expiry_type`, `vix_open`, `vix_close`, `t1_fii_stance`, `t1_pro_stance`, `nifty_open`, `nifty_high`, `nifty_low`, `nifty_close`). Verify by running the script and printing the DataFrame shape (expect 322 rows).

- [x] 2.2 Add the PostgreSQL query function: for each expiry date, query `market_data.nifty50_5min` for rows where `datetime::date = <expiry_date>` and `datetime::time >= '14:00'` and `datetime::time <= '15:25'`. Use `psycopg2` with connection params `host=localhost, dbname=market_data`. Verify by running for a single date (e.g., 2026-07-16) and confirming 18 candles are returned.

- [x] 2.3 Implement the join loop: iterate over all CSV expiry dates, fetch 5-min bars for each, skip dates with no data (log warning with date), and build a combined DataFrame with columns `[date, move_direction, expiry_type, vix_open, vix_close, t1_fii_stance, t1_pro_stance, afternoon_candles]`. Verify by checking that the number of successfully joined dates is ~317 (322 minus ~5 early dates).

## 3. Afternoon Move Classification

- [x] 3.1 For each expiry day with 5-min data, compute the afternoon move direction: compare the 14:00 candle open price vs the last candle close price. Classify as "Top to Down" (open > close), "Down to Up" (open < close), or "Flat" (within 0.01% tolerance). Add column `afternoon_direction` to the results DataFrame. Verify by spot-checking 5 known dates against the CSV `move_direction` column.

- [x] 3.2 Add a concordance column comparing `afternoon_direction` (post-2 PM only) with the CSV's `move_direction` (full-day). Compute match percentage. Verify the concordance rate is logged to console (expect >70% match since most daily moves persist into afternoon).

## 4. Inflection Point Detection

- [x] 4.1 Implement inflection detection: for "Top to Down" afternoons, find the 5-min candle with the highest `high` between 14:00–15:25; for "Down to Up" afternoons, find the candle with the lowest `low`. Record the inflection timestamp. For "Flat" days, record None. Add columns `inflection_time` (time only, e.g., "14:30") and `inflection_price`. Verify by printing the first 10 results and manually checking 2 dates against raw DB data.

- [x] 4.2 Compute the move magnitude: percentage change from inflection price to session close. Add column `move_from_inflection_pct`. Verify values are non-negative (absolute) and in a reasonable range (0–5%).

## 5. Statistical Analysis

- [x] 5.1 Build the overall timing distribution: count how many inflection points fall at each 5-minute slot (14:00, 14:05, ..., 15:25). Compute both count and percentage. Store as a DataFrame. Verify the counts sum to the total number of non-flat days.

- [x] 5.2 Build segmented distributions: create separate timing distribution tables for (a) Top to Down vs Down to Up, (b) weekly vs monthly expiry, (c) VIX buckets (low <15, medium 15–20, high >20 using `vix_open`), (d) FII stance categories. Verify each segment's counts sum to its group total.

- [x] 5.3 Compute move magnitude by 15-minute time buckets: for each marker (14:00, 14:15, 14:30, 14:45, 15:00), calculate the average, median, min, and max absolute percentage move from that time's candle open to session close, broken down by direction. Verify the table has 5 rows × 2 directions × 4 statistics.

- [x] 5.4 Build the VIX-level × FII-stance cross-tabulation of inflection times: for each combination, show the modal (most common) inflection time and average move magnitude. Verify the table covers all non-empty VIX × FII combinations.

## 6. CSV Output

- [x] 6.1 Write the per-expiry-day results to `expiry-afternoon-analysis/afternoon_reversal_results.csv` with columns: `date, day_of_week, expiry_type, csv_move_direction, afternoon_direction, concordance, vix_open, vix_close, vix_bucket, t1_fii_stance, t1_pro_stance, price_at_2pm, session_close, inflection_time, inflection_price, move_from_inflection_pct, move_from_2pm_pct`. Verify the CSV has the expected row count and all columns are present by reading back with pandas.

## 7. Markdown Report Generation

- [x] 7.1 Generate `expiry-afternoon-analysis/EXPIRY_AFTERNOON_REVERSAL_REPORT.md` with the following sections: (1) Executive Summary identifying the primary reversal time zone with its frequency, (2) Overall Timing Distribution table (5-min granularity), (3) Direction-segmented distribution tables, (4) Expiry-type breakdown tables, (5) VIX-level breakdown tables, (6) FII stance breakdown tables, (7) Move magnitude by time bucket table, (8) VIX × FII cross-tabulation, (9) Concordance analysis (afternoon vs full-day direction match rate), (10) Key Findings and Trading Implications. Verify the file exists and contains all 10 section headers.

## 8. End-to-End Verification

- [x] 8.1 Run the complete script end-to-end with `python3 expiry-afternoon-analysis/analyze_afternoon_reversals.py` and verify: (a) no errors or unhandled exceptions, (b) `expiry-afternoon-analysis/afternoon_reversal_results.csv` exists with ~317 rows, (c) `expiry-afternoon-analysis/EXPIRY_AFTERNOON_REVERSAL_REPORT.md` exists with all 10 sections, (d) console output shows the number of dates processed, dates skipped, and the top 3 most common inflection times.
