## Purpose

Correlates FII/DII institutional positioning data (Nifty-based proxy) with Sensex VIX expiry-day backtest results to determine whether institutional flow signals improve prediction of Sensex VIX blowout days and expiry-day movement patterns. Compares findings with the existing Nifty correlation analysis to assess whether the relationship is market-wide or index-specific.

## ADDED Requirements

### Requirement: Join FII/DII data with Sensex VIX expiry results on matching dates

The system SHALL merge `fii_dii_backtest_daily_results.csv` with `vix_sensex_6y_results.csv` on expiry dates that exist in both datasets, producing a single merged DataFrame with all columns from both sources.

#### Scenario: Successful date merge
- **WHEN** the script runs with both input files present
- **THEN** it produces a merged dataset containing only rows where the date appears in both the FII/DII file and the Sensex VIX expiry results, with all columns preserved from each source (expected: 46 rows)

#### Scenario: Missing input file
- **WHEN** either input CSV file is not found at the expected path
- **THEN** the script exits with a clear error message naming the missing file

#### Scenario: Date column normalization
- **WHEN** merging the two datasets with different date column names (`Date` in FII/DII, `date` in Sensex)
- **THEN** the system normalizes both to a consistent format before joining

### Requirement: Compute correlation between FII positioning and Sensex blowout occurrence

The system SHALL calculate statistical correlations between FII numeric signals (fii_fut_idx_net, fii_call_net, fii_put_net) and blowout occurrence (vix_accuracy == "Underestimated"), including Pearson correlation coefficients and point-biserial correlation for categorical outcomes.

#### Scenario: Correlation output for numeric FII signals vs blowout
- **WHEN** the merged dataset is computed
- **THEN** the system outputs correlation coefficients between each FII numeric column and a binary blowout indicator, with p-values indicating statistical significance

#### Scenario: Low blowout count handling
- **WHEN** the blowout sample is very small (n < 10)
- **THEN** the system flags all blowout-specific correlations with a warning about insufficient sample size and also computes correlations against alternative continuous targets (actual_range_pct, diff_pct)

### Requirement: Analyze FII/DII direction signals vs Sensex expiry-day outcomes

The system SHALL cross-tabulate categorical direction signals (FII_Direction, DII_Direction, Pro_Direction, Client_Direction) against Sensex expiry-day outcomes (blowout yes/no, move direction, range magnitude) and compute hit rates for each combination.

#### Scenario: FII_Direction vs blowout cross-tabulation
- **WHEN** the analysis runs
- **THEN** it produces a contingency table showing blowout rate for each FII_Direction value (Bullish, Bearish, Neutral), with the count and percentage for each cell, flagging cells with n < 5

#### Scenario: Multi-participant direction consensus
- **WHEN** multiple participant directions agree (e.g., FII + DII both Bullish)
- **THEN** the system reports blowout rate and average range for the consensus condition vs non-consensus

#### Scenario: Direction accuracy against Sensex
- **WHEN** computing direction match signals
- **THEN** the system uses Sensex's own open-to-close direction (from actual_open_close_pct) rather than the Nifty-based Market_Direction from the FII/DII dataset

### Requirement: Analyze FII put/call ratio as Sensex VIX blowout predictor

The system SHALL compute a derived FII put-call ratio (fii_put_net / abs(fii_call_net)) and correlate it with blowout occurrence, Sensex expiry-day range, and move direction.

#### Scenario: High FII put/call ratio days
- **WHEN** the FII put-call ratio exceeds its median value
- **THEN** the system reports the blowout rate, average range, and dominant direction for high-ratio days vs low-ratio days

### Requirement: Flag Nifty co-expiry days

The system SHALL identify which Sensex expiry days are also Nifty expiry days (Thursday) and analyze whether FII signal quality differs on dual-expiry vs Sensex-only expiry days.

#### Scenario: Dual-expiry flag computation
- **WHEN** the merged dataset is produced
- **THEN** each row has an `is_nifty_expiry_day` boolean flag based on whether the date is a Thursday (Nifty weekly expiry day)

#### Scenario: Conditional analysis by co-expiry status
- **WHEN** correlations and rules are tested
- **THEN** results are reported both overall and split by is_nifty_expiry_day, to assess if FII signals are stronger when Nifty also expires

### Requirement: Generate combined output files with Nifty comparison

The system SHALL produce:
1. A CSV file with the merged data including all derived correlation features
2. A JSON file with correlation statistics, cross-tabulation results, rule findings, and Nifty comparison data
3. A markdown summary report with key findings, Nifty vs Sensex comparison, and actionable trading implications

#### Scenario: Output file generation
- **WHEN** the analysis completes successfully
- **THEN** three output files are created: `fii_dii_vix_correlation_sensex.csv`, `fii_dii_vix_correlation_sensex.json`, and `FII_DII_VIX_CORRELATION_SENSEX_SUMMARY.md`

#### Scenario: Nifty comparison section
- **WHEN** the summary report is generated
- **THEN** it includes a dedicated comparison section showing Sensex vs Nifty correlation coefficients, blowout rates, and rule lift values side-by-side

### Requirement: Test FII data as pre-market Sensex blowout predictor

The system SHALL evaluate whether FII positioning on the Sensex expiry day (or day before) improves blowout prediction beyond the base rate, by computing precision and lift for FII-based rules compared to the baseline.

#### Scenario: FII signal lift calculation
- **WHEN** a FII-based filter is applied (e.g., FII_Direction == "Bearish")
- **THEN** the system reports the blowout rate under that filter, the lift versus base rate (8.7% overlap period / 23.9% full period), and the number of days triggered

#### Scenario: Alternative target for higher power
- **WHEN** the blowout sample is too small for meaningful analysis
- **THEN** the system also tests all rules against `above_median_range` (actual_range_pct above the 46-day median) as an alternative binary target, providing higher statistical power

### Requirement: Provide separate FII and PRO participant-wise data

The system SHALL fetch daily participant-wise OI data from NSE archives with separate columns for FII, PRO, DII, and Client — not aggregated as "FPI".

#### Scenario: Separate participant categories
- **WHEN** the participant data fetcher runs
- **THEN** it produces a CSV with independent columns for each of the 4 participants (FII, PRO, DII, Client), each with: futures index net, stock futures net, call net, put net, daily change, direction, and stance

#### Scenario: Daily direction signals per participant
- **WHEN** daily changes are computed from absolute positions
- **THEN** each participant has independent `{prefix}_direction` (Bullish/Bearish/Neutral) and `{prefix}_stance` (detailed classification) columns

#### Scenario: Data source (NSE archives)
- **WHEN** BSE India API is inaccessible (protected by Akamai WAF)
- **THEN** the system uses NSE participant-wise OI archives (`archives.nseindia.com/content/nsccl/fao_participant_oi_DDMMYYYY.csv`) which provide equivalent institutional positioning data across all F&O segments

### Requirement: Consolidate all Sensex analysis in dedicated directory

The system SHALL store all Sensex-related artifacts (scripts, data files, summaries) in `sensex-analysis/` at the project root.

#### Scenario: Directory structure
- **WHEN** the analysis outputs are generated
- **THEN** all files are placed in `sensex-analysis/` including: VIX backtest results, FII correlation data, participant-wise daily data, Python scripts, and markdown summaries
