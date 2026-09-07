## Purpose

Analyzes daily Nifty intraday behavior when FII and PRO participants align on the same directional view, measuring whether the market follows through or reverses between the first and second halves of the trading session, whether the close ultimately validates the aligned direction, and whether the aligned-direction move exceeded half the VIX-predicted range before reversing.

## ADDED Requirements

### Requirement: Classify participant alignment

The system SHALL classify each trading day into one of four alignment categories based on `fii_view` and `pro_view`:
- **Bullish Alignment**: Both FII and PRO have a bullish-leaning view (Strong Bullish, Bullish, or Mildly Bullish)
- **Bearish Alignment**: Both FII and PRO have a bearish-leaning view (Strong Bearish, Bearish, or Mildly Bearish)
- **Mixed**: FII and PRO have opposing directional views (one bullish, one bearish)
- **Neutral/Unclear**: One or both views are Neutral or empty

#### Scenario: Bullish alignment detected
- **WHEN** fii_view is "Mildly Bullish" and pro_view is "Bullish"
- **THEN** the day SHALL be classified as "Bullish Alignment"

#### Scenario: Bearish alignment detected
- **WHEN** fii_view is "Bearish" and pro_view is "Strong Bearish"
- **THEN** the day SHALL be classified as "Bearish Alignment"

#### Scenario: Mixed views detected
- **WHEN** fii_view is "Bullish" and pro_view is "Bearish"
- **THEN** the day SHALL be classified as "Mixed"

#### Scenario: Neutral view detected
- **WHEN** fii_view is "Neutral" and pro_view is "Bullish"
- **THEN** the day SHALL be classified as "Neutral/Unclear"

### Requirement: Determine first-half and second-half direction

The system SHALL use the `move_direction` column to determine intraday behavior:
- "Top to Down" = bullish first half (market rose from open), bearish second half (market fell to close)
- "Down to Up" = bearish first half (market fell from open), bullish second half (market rose to close)

The system SHALL use `intraday_high_pct` as the magnitude of the bullish move from open and `intraday_low_pct` as the magnitude of the bearish move from open.

#### Scenario: Top to Down pattern
- **WHEN** move_direction is "Top to Down"
- **THEN** first_half_direction SHALL be "Bullish" and second_half_direction SHALL be "Bearish"

#### Scenario: Down to Up pattern
- **WHEN** move_direction is "Down to Up"
- **THEN** first_half_direction SHALL be "Bearish" and second_half_direction SHALL be "Bullish"

### Requirement: Classify follow-through vs reversal

For each alignment day, the system SHALL determine:
- **Follow-through**: The first half moved in the direction of the aligned view (bullish alignment + bullish first half, or bearish alignment + bearish first half)
- **Reversal**: The second half moved opposite to the aligned view despite initial follow-through
- **Against from start**: The first half moved opposite to the aligned view

#### Scenario: Bullish alignment with follow-through then reversal
- **WHEN** alignment is "Bullish Alignment" and move_direction is "Top to Down"
- **THEN** the day SHALL be classified as "Follow-through then Reversal" (first half bullish matched the alignment, but second half reversed to bearish)

#### Scenario: Bearish alignment with follow-through then reversal
- **WHEN** alignment is "Bearish Alignment" and move_direction is "Down to Up"
- **THEN** the day SHALL be classified as "Follow-through then Reversal" (first half bearish matched the alignment, but second half reversed to bullish)

#### Scenario: Bullish alignment that worked all day
- **WHEN** alignment is "Bullish Alignment" and move_direction is "Down to Up"
- **THEN** the day SHALL be classified as "Against then Recovery" (market dipped first but recovered in the aligned bullish direction)

### Requirement: Classify close outcome (Worked and Remained)

For each alignment day, the system SHALL independently classify whether the market close validated the aligned direction using `actual_open_close_pct`:
- **Worked and Remained**: The close was in the aligned direction (bullish alignment + actual_open_close_pct > 0, or bearish alignment + actual_open_close_pct < 0)
- **Reversed by Close**: The close was against the aligned direction (bullish alignment + actual_open_close_pct ≤ 0, or bearish alignment + actual_open_close_pct ≥ 0)

This classification is independent of the intraday-path classification (Worked then Reversed / Against then Recovered) and answers: "Was the institutional consensus ultimately correct by end of day?"

#### Scenario: Bullish alignment with close above open
- **WHEN** alignment is "Bullish Alignment" and actual_open_close_pct is 0.48
- **THEN** close_outcome SHALL be "Worked and Remained"

#### Scenario: Bullish alignment with close below open
- **WHEN** alignment is "Bullish Alignment" and actual_open_close_pct is -0.55
- **THEN** close_outcome SHALL be "Reversed by Close"

#### Scenario: Bearish alignment with close below open
- **WHEN** alignment is "Bearish Alignment" and actual_open_close_pct is -0.85
- **THEN** close_outcome SHALL be "Worked and Remained"

#### Scenario: Bearish alignment with close above open
- **WHEN** alignment is "Bearish Alignment" and actual_open_close_pct is 0.48
- **THEN** close_outcome SHALL be "Reversed by Close"

### Requirement: Classify VIX half-range exhaustion

For each alignment day with valid `vix_predicted_move_pct`, the system SHALL compare the first-half move in the aligned direction against half the VIX-predicted range:
- **Half-range threshold** = `vix_predicted_move_pct / 2`
- **Aligned-direction move**: For bullish alignment, use `intraday_high_pct` (upside from open). For bearish alignment, use `abs(intraday_low_pct)` (downside from open).
- **Exceeded Half then Reversed**: The aligned-direction move exceeded the half-range threshold
- **Reversed Before Half**: The aligned-direction move was at or below the half-range threshold

Days with missing or zero `vix_predicted_move_pct` SHALL have an empty `vix_exhaustion` value.

#### Scenario: Bullish alignment exceeds half VIX range
- **WHEN** alignment is "Bullish Alignment" and vix_predicted_move_pct is 1.0 and intraday_high_pct is 0.65
- **THEN** vix_exhaustion SHALL be "Exceeded Half then Reversed" (0.65 > 0.5 threshold)

#### Scenario: Bullish alignment does not reach half VIX range
- **WHEN** alignment is "Bullish Alignment" and vix_predicted_move_pct is 1.0 and intraday_high_pct is 0.30
- **THEN** vix_exhaustion SHALL be "Reversed Before Half" (0.30 ≤ 0.5 threshold)

#### Scenario: Bearish alignment exceeds half VIX range
- **WHEN** alignment is "Bearish Alignment" and vix_predicted_move_pct is 1.2 and intraday_low_pct is -0.80
- **THEN** vix_exhaustion SHALL be "Exceeded Half then Reversed" (0.80 > 0.6 threshold)

#### Scenario: Bearish alignment does not reach half VIX range
- **WHEN** alignment is "Bearish Alignment" and vix_predicted_move_pct is 1.2 and intraday_low_pct is -0.40
- **THEN** vix_exhaustion SHALL be "Reversed Before Half" (0.40 ≤ 0.6 threshold)

#### Scenario: Missing VIX predicted move
- **WHEN** alignment is "Bullish Alignment" and vix_predicted_move_pct is NaN
- **THEN** vix_exhaustion SHALL be empty

### Requirement: Generate statistical summary report

The system SHALL produce a markdown report containing:
- Total alignment days vs total trading days
- Breakdown by alignment type (bullish vs bearish)
- For each alignment type: follow-through rate in first half, reversal rate in second half, average first-half magnitude, average second-half magnitude
- Worked and Remained analysis: overall close-outcome rates, breakdown by bullish/bearish alignment, by expiry/non-expiry, by VIX regime, and by year
- VIX half-range exhaustion analysis: overall exhaustion rates, cross-tab of exhaustion × close outcome, breakdown by bullish/bearish alignment, and by VIX regime
- Expiry day vs non-expiry day comparison
- VIX regime breakdown (VIX < 15, 15-20, 20-30, >30)
- Year-over-year trends
- Key findings and trading implications (including Worked and Remained insight and VIX exhaustion insight)

#### Scenario: Report generation
- **WHEN** the analysis script is executed
- **THEN** the system SHALL generate a markdown report file with all summary statistics and a CSV file with per-day classification details

### Requirement: Output files in dedicated folder

The system SHALL write all outputs to a new `fii-pro-alignment-analysis/` folder in the project root containing:
- The Python analysis script
- A per-day results CSV with alignment classification, direction flags, close_outcome, vix_exhaustion, vix_predicted_move_pct, and magnitudes
- A markdown report with summary tables and findings

#### Scenario: Output folder structure
- **WHEN** the analysis completes successfully
- **THEN** the folder `fii-pro-alignment-analysis/` SHALL contain at minimum one `.py` script, one `.csv` results file, and one `.md` report file
