## Context

The source CSV (`vix_fii_t1_intraday_daily_results.csv`) has 1,482 rows spanning Aug 2020–Aug 2026. Each row contains:
- Participant positioning: `fii_view` and `pro_view` (8 levels from "Strong Bearish" to "Strong Bullish", plus empty)
- Intraday pattern: `move_direction` is strictly binary — "Down to Up" or "Top to Down"
- Magnitudes: `intraday_high_pct` (max upside from open) and `intraday_low_pct` (max downside from open, negative)
- VIX prediction: `vix_predicted_move_pct` (VIX-implied expected daily range as a percentage, available for 1,463 of 1,482 rows)
- Context: `is_nifty_expiry`, `expiry_type`, `vix_open`, OHLC data

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Single self-contained Python script that reads the CSV, classifies alignment, and produces both a detailed CSV and a markdown report
- Clear view bucketing: map the 8 `fii_view`/`pro_view` values into Bullish / Bearish / Neutral
- Measure first-half vs second-half behavior relative to the aligned direction
- Separately classify whether the close validated the aligned view ("Worked and Remained" vs "Reversed by Close")
- Measure whether the aligned-direction move exceeded half the VIX-predicted range before reversing (momentum exhaustion signal)
- Slice results by expiry/non-expiry, VIX regime, and year

**Non-Goals:**
- Real-time or streaming analysis
- Statistical significance testing (report raw counts and percentages)
- Visualization or chart generation (markdown tables only)
- Modifying the source CSV

## Decisions

### 1. View bucketing logic

**Decision**: Map views into three directional buckets:
- **Bullish bucket**: "Strong Bullish", "Bullish", "Mildly Bullish"
- **Bearish bucket**: "Strong Bearish", "Bearish", "Mildly Bearish"
- **Neutral bucket**: "Neutral", empty/blank

**Rationale**: "Mildly Bullish/Bearish" still represents a directional lean from institutional participants. Including them captures the full range of directional alignment. Alternative was to require "Bullish" or stronger, but that would discard ~40% of directional signals.

### 2. Alignment + reversal classification

**Decision**: For alignment days, classify into four outcomes:

| Alignment | move_direction | Classification |
|-----------|---------------|----------------|
| Bullish | Top to Down | **Worked then Reversed** — first half bullish (matched view), second half reversed bearish |
| Bullish | Down to Up | **Against then Recovered** — first half bearish (against view), second half recovered bullish |
| Bearish | Down to Up | **Worked then Reversed** — first half bearish (matched view), second half reversed bullish |
| Bearish | Top to Down | **Against then Recovered** — first half bullish (against view), second half recovered bearish |

**Rationale**: The user's core question is "when aligned, did first half work and second half reverse?" This 2x2 matrix captures exactly that. "Worked then Reversed" is the key pattern of interest.

### 3. Close outcome classification (Worked and Remained)

**Decision**: Add an independent `close_outcome` classification based on `actual_open_close_pct`:
- **Worked and Remained**: close was in the aligned direction (bullish alignment + close > open, bearish alignment + close < open)
- **Reversed by Close**: close was against the aligned direction

This is a separate dimension from the intraday-path classification. Data shows `move_direction` perfectly determines close direction ("Top to Down" → close < open, "Down to Up" → close > open), so "Worked and Remained" for bullish alignment maps to "Down to Up" days and for bearish alignment maps to "Top to Down" days.

**Rationale**: The intraday-path classification tracks the journey (first half vs second half). The close-outcome classification tracks the destination (did the aligned view win by end of day?). Both perspectives are useful: the path tells you about intraday risk, the close tells you about the view's correctness.

### 4. VIX half-range exhaustion classification

**Decision**: For each alignment day, compare the aligned-direction move against half the VIX-predicted range:
- **Threshold** = `vix_predicted_move_pct / 2`
- **Aligned-direction move**: For bullish alignment, use `intraday_high_pct`. For bearish alignment, use `abs(intraday_low_pct)`.
- If aligned move > threshold → "Exceeded Half then Reversed"
- If aligned move ≤ threshold → "Reversed Before Half"
- Days with missing `vix_predicted_move_pct` get an empty value (4 alignment days affected).

**Rationale**: VIX-predicted range represents the market's expected daily movement. If the aligned-direction move exceeds half this range, it suggests meaningful momentum exhaustion occurred before any reversal. Data shows this is the strongest predictor in the analysis: 86.6% of "Exceeded Half" days close in the aligned direction vs only 23.5% for "Reversed Before Half". This distinguishes genuine institutional follow-through from weak/false alignment signals.

**Alternative considered**: Using the full VIX range as threshold. Rejected because only a small fraction of days use the full range, and the half-range threshold already produces a stark separation in close-outcome rates.

### 5. Single script approach (unchanged)

**Decision**: One `analyze_fii_pro_alignment.py` file using pandas, producing both outputs.

**Alternative considered**: Separate scripts for analysis and reporting. Rejected because the analysis is straightforward enough that separation adds complexity without benefit.

### 6. VIX regime bands

**Decision**: Use bands < 15, 15–20, 20–30, > 30.

**Rationale**: These are standard India VIX interpretation bands used in the existing project analysis files.

## Risks / Trade-offs

- **[Risk] `move_direction` is a simplified proxy for first-half/second-half** → The column captures the dominant pattern but doesn't precisely define "first half = 9:15–12:15" and "second half = 12:15–3:30". It's the best available signal in this dataset. Mitigation: report this as a data limitation in the output report.
- **[Risk] T+1 lag in participant data** → FII/PRO views are derived from T+1 settlement data, so alignment is known only after the trading day. Mitigation: clearly state in the report that this is a retrospective study, not a predictive signal (though patterns can inform next-day positioning).
- **[Trade-off] Including "Mildly" views in directional buckets increases alignment day count but dilutes signal strength** → Mitigated by also reporting breakdowns for "Strong" alignment (both sides Bullish/Strong Bullish or Bearish/Strong Bearish).
