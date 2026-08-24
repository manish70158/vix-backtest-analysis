## Purpose

Correlates FII/DII institutional positioning data with VIX expiry-day backtest results to determine whether institutional flow signals improve prediction of VIX blowout days and expiry-day movement patterns.

## ADDED Requirements

### Requirement: Join FII/DII data with VIX expiry results on matching dates

The system SHALL merge `fii_dii_backtest_daily_results.csv` with `vix_all_expiries_results_v6.csv` on expiry dates that exist in both datasets, producing a single merged DataFrame with all columns from both sources.

#### Scenario: Successful date merge
- **WHEN** the script runs with both input files present
- **THEN** it produces a merged dataset containing only rows where the date appears in both the FII/DII file and the VIX expiry results, with all columns preserved from each source

#### Scenario: Missing input file
- **WHEN** either input CSV file is not found at the expected path
- **THEN** the script exits with a clear error message naming the missing file

### Requirement: Compute correlation between FII positioning and blowout occurrence

The system SHALL calculate statistical correlations between FII numeric signals (fii_fut_idx_net, fii_call_net, fii_put_net) and blowout occurrence (vix_accuracy == "Underestimated"), including Pearson correlation coefficients and point-biserial correlation for categorical outcomes.

#### Scenario: Correlation output for numeric FII signals vs blowout
- **WHEN** the merged dataset is computed
- **THEN** the system outputs correlation coefficients between each FII numeric column and a binary blowout indicator, with p-values indicating statistical significance

### Requirement: Analyze FII/DII direction signals vs expiry-day outcomes

The system SHALL cross-tabulate categorical direction signals (FII_Direction, DII_Direction, Pro_Direction, Client_Direction) against expiry-day outcomes (blowout yes/no, move direction, market direction) and compute hit rates for each combination.

#### Scenario: FII_Direction vs blowout cross-tabulation
- **WHEN** the analysis runs
- **THEN** it produces a contingency table showing blowout rate for each FII_Direction value (Bullish, Bearish, Neutral), with the count and percentage for each cell

#### Scenario: Multi-participant direction consensus
- **WHEN** multiple participant directions agree (e.g., FII + DII both Bullish)
- **THEN** the system reports blowout rate and average range for the consensus condition vs non-consensus

### Requirement: Analyze FII put/call ratio as VIX blowout predictor

The system SHALL compute a derived FII put-call ratio (fii_put_net / abs(fii_call_net)) and correlate it with blowout occurrence, expiry-day range, and move direction.

#### Scenario: High FII put/call ratio days
- **WHEN** the FII put-call ratio exceeds its median value
- **THEN** the system reports the blowout rate, average range, and dominant direction for high-ratio days vs low-ratio days

### Requirement: Generate combined output files

The system SHALL produce:
1. A CSV file with the merged data including all derived correlation features
2. A JSON file with correlation statistics, cross-tabulation results, and summary findings
3. A markdown summary report with key findings and actionable trading implications

#### Scenario: Output file generation
- **WHEN** the analysis completes successfully
- **THEN** three output files are created: `fii_dii_vix_correlation.csv`, `fii_dii_vix_correlation.json`, and `FII_DII_VIX_CORRELATION_SUMMARY.md`

### Requirement: Test FII data as pre-market blowout predictor

The system SHALL evaluate whether FII positioning on the expiry day (or day before) improves blowout prediction beyond the 22% base rate, by computing precision and lift for FII-based rules compared to the baseline.

#### Scenario: FII signal lift calculation
- **WHEN** a FII-based filter is applied (e.g., FII_Direction == "Bearish")
- **THEN** the system reports the blowout rate under that filter, the lift versus base rate (22%), and the number of days triggered
