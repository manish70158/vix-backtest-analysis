## Purpose

Analyze 5-minute intraday Nifty data on expiry days to identify the precise afternoon timing window when directional moves (top-to-down or down-to-up) begin, cross-referenced with VIX levels and FII/DII positioning.

## ADDED Requirements

### Requirement: Join expiry metadata with 5-minute intraday bars

The system SHALL read all expiry dates from `vix_fii_t1_intraday_expiry_results.csv` and fetch corresponding 5-minute OHLCV candles from PostgreSQL table `market_data.nifty50_5min` for each expiry date's afternoon session (14:00–15:30 IST).

#### Scenario: Successful data join for an expiry date present in both sources
- **WHEN** an expiry date exists in the CSV and has 5-minute bars in PostgreSQL
- **THEN** the system SHALL produce a merged record containing the CSV metadata columns (move_direction, vix_open, vix_close, expiry_type, t1_fii_stance, t1_pro_stance) alongside the afternoon 5-minute OHLCV bars for that date

#### Scenario: Expiry date missing from 5-minute database
- **WHEN** an expiry date from the CSV has no corresponding rows in `nifty50_5min`
- **THEN** the system SHALL skip that date, log a warning, and continue processing remaining dates

### Requirement: Classify afternoon directional move for each expiry day

The system SHALL classify the post-2 PM move for each expiry day as either "Top to Down" (price at 2 PM > close) or "Down to Up" (price at 2 PM < close), using the 14:00 candle open as the reference price and the last available candle close as the session close.

#### Scenario: Price drops from 2 PM to close
- **WHEN** the 14:00 candle open price is higher than the session close price
- **THEN** the afternoon move SHALL be classified as "Top to Down"

#### Scenario: Price rises from 2 PM to close
- **WHEN** the 14:00 candle open price is lower than the session close price
- **THEN** the afternoon move SHALL be classified as "Down to Up"

#### Scenario: Price is flat from 2 PM to close
- **WHEN** the 14:00 candle open price equals the session close price (within 0.01% tolerance)
- **THEN** the afternoon move SHALL be classified as "Flat"

### Requirement: Identify the inflection candle timing

The system SHALL identify the specific 5-minute candle where the directional move begins by finding the afternoon high (for top-to-down) or afternoon low (for down-to-up) — the point from which price moves monotonically toward the close direction.

#### Scenario: Top-to-down move inflection detection
- **WHEN** the afternoon is classified as "Top to Down"
- **THEN** the inflection time SHALL be the timestamp of the 5-minute candle containing the afternoon high (highest high between 14:00 and 15:30)

#### Scenario: Down-to-up move inflection detection
- **WHEN** the afternoon is classified as "Down to Up"
- **THEN** the inflection time SHALL be the timestamp of the 5-minute candle containing the afternoon low (lowest low between 14:00 and 15:30)

### Requirement: Compute timing distribution statistics

The system SHALL aggregate inflection times across all expiry days and produce frequency counts for each 5-minute slot from 14:00 to 15:25, grouped by:
1. Overall (all expiry days)
2. Move direction (Top to Down vs Down to Up)
3. Expiry type (weekly vs monthly)
4. VIX level buckets (low: <15, medium: 15–20, high: >20)
5. FII stance categories

#### Scenario: Distribution table for all expiry days
- **WHEN** the analysis completes for all available expiry days
- **THEN** the output SHALL include a table showing the count and percentage of inflection points occurring at each 5-minute time slot from 14:00 through 15:25

#### Scenario: Breakdown by expiry type
- **WHEN** the analysis completes
- **THEN** the output SHALL include separate distribution tables for weekly and monthly expiry days

### Requirement: Compute move magnitude by time bucket

The system SHALL calculate the average absolute price move (in percentage) from each time bucket (14:00, 14:15, 14:30, 14:45, 15:00) to the session close, across all expiry days.

#### Scenario: Magnitude table generation
- **WHEN** the analysis completes
- **THEN** the output SHALL include a table showing the average, median, min, and max percentage move from each 15-minute time marker to session close, broken down by direction

### Requirement: Generate output in dedicated folder

The system SHALL write all outputs to a folder named `expiry-afternoon-analysis/` in the repository root.

#### Scenario: Output folder structure
- **WHEN** the analysis script runs successfully
- **THEN** the following files SHALL exist in `expiry-afternoon-analysis/`:
  - A Python analysis script
  - A CSV file with per-expiry-day afternoon analysis results
  - A markdown report summarizing all findings

### Requirement: Generate comprehensive markdown report

The system SHALL produce a markdown report containing:
1. Executive summary with the most statistically significant timing window
2. Timing distribution tables (overall and segmented)
3. Move magnitude analysis by time bucket
4. Cross-tabulation with VIX levels and FII stance
5. Key actionable findings for traders

#### Scenario: Report identifies the dominant reversal window
- **WHEN** the analysis finds that a plurality of inflection points cluster in a specific time range
- **THEN** the report SHALL highlight that window as the "primary reversal zone" with its frequency percentage and confidence

#### Scenario: Report includes comparison with CSV move_direction
- **WHEN** the CSV already classifies each day as "Top to Down" or "Down to Up" based on full-day analysis
- **THEN** the report SHALL include a concordance table showing how often the afternoon-only classification matches the full-day CSV classification
