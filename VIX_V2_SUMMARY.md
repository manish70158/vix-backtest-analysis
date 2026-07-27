# VIX Backtest V2 - Modified Threshold Logic

## What Changed in V2

**V2 introduces a 0.2% threshold for classifying VIX underestimation:**

### V1 (Original Logic)
```
IF actual_range_pct > vix_predicted_move_pct:
    → "Underestimated"
ELSE:
    → "Overestimated"
```

### V2 (Modified with 0.2% Threshold)
```
diff = actual_range_pct - vix_predicted_move_pct

IF diff > 0.2:
    → "Underestimated"
ELSE:
    → "Overestimated" (includes accurate predictions within 0.2%)
```

---

## Impact on Results (6-Year Data: 317 Expiries)

### Classification Changes

| Category | V1 Original | V2 (0.2% threshold) | Change |
|----------|-------------|---------------------|--------|
| **Underestimated** | 189 (59.6%) | 130 (41.0%) | **-59 (-18.6%)** |
| **Overestimated** | 128 (40.4%) | 187 (59.0%) | **+59 (+18.6%)** |

**59 out of 317 expiries (18.6%) changed classification from "Underestimated" to "Overestimated"**

These were cases where:
- V1: Flagged as underestimated (any positive difference)
- V2: Treated as accurate/overestimated (difference ≤ 0.2%)

### Weekly vs Monthly Breakdown

**Weekly Expiries (245 days):**
- V1: 140 underestimated (57.1%)
- V2: 92 underestimated (37.6%)
- **Change**: 48 fewer (19.5% reduction)

**Monthly Expiries (72 days):**
- V1: 49 underestimated (68.1%)
- V2: 38 underestimated (52.8%)
- **Change**: 11 fewer (15.3% reduction)

---

## New CSV Columns in V2

V2 adds one new column to help analyze the threshold logic:

| Column | Description | Example |
|--------|-------------|---------|
| `diff_pct` | Actual - Predicted (percentage points) | 0.65, -0.40, 0.12 |

**All other columns remain the same.**

---

## Example Cases

### Case 1: Small Underestimation (Now Treated as Accurate)
```
Date: 2020-07-16
VIX Predicted: 1.38%
Actual Range: 1.50%
Difference: +0.12%

V1: "Underestimated" (actual > predicted)
V2: "Overestimated" (diff 0.12% < threshold 0.2%)
```
**Interpretation**: VIX was close enough. 0.12% difference is acceptable.

### Case 2: Significant Underestimation (Still Flagged)
```
Date: 2020-07-30
VIX Predicted: 1.26%
Actual Range: 1.91%
Difference: +0.65%

V1: "Underestimated"
V2: "Underestimated" (diff 0.65% > threshold 0.2%)
```
**Interpretation**: VIX significantly missed. This is a real underestimation.

### Case 3: Tiny Underestimation (Now Treated as Accurate)
```
Date: 2020-09-10
VIX Predicted: 1.16%
Actual Range: 1.20%
Difference: +0.04%

V1: "Underestimated" (actual > predicted)
V2: "Overestimated" (diff 0.04% < threshold 0.2%)
```
**Interpretation**: VIX was essentially accurate. 0.04% is noise.

---

## Why 0.2% Threshold?

### Practical Trading Perspective

**At current NIFTY levels (~25,000):**
- 0.2% = **50 points**
- This is a meaningful move for intraday traders
- Differences below this are typically within bid-ask spreads and noise

**Benefits of 0.2% threshold:**
1. **Reduces noise**: Ignores insignificant variations
2. **More realistic**: Focuses on meaningful VIX failures
3. **Better for backtesting**: Identifies genuinely problematic predictions
4. **Trading actionable**: Small differences don't require position adjustments

---

## When to Use V1 vs V2

### Use V1 (Original) If:
✅ You need maximum conservative approach
✅ Any VIX error is unacceptable for your strategy
✅ Building ultra-wide safety margins
✅ Risk management requires worst-case assumptions

**Example use case**: Selling naked options where even small underestimations cause losses

### Use V2 (0.2% Threshold) If:
✅ You want realistic trading signals
✅ Accept ±0.2% as "good enough" prediction
✅ Focus on significant VIX failures only
✅ Practical backtesting of strategies

**Example use case**: Adjusting strike prices where <0.2% doesn't matter

---

## Files Generated

### V1 (Original Logic)
- `vix_all_expiries_results.json` - All 317 expiries, original logic
- `vix_all_expiries_results.csv` - Original classification
- No `diff_pct` column

### V2 (Modified 0.2% Threshold)
- `vix_all_expiries_results_v2.json` - All 317 expiries, modified logic
- `vix_all_expiries_results_v2.csv` - **New classification with `diff_pct` column**
- More conservative underestimation counts

### Comparison
- `vix_v1_v2_comparison.md` - Detailed comparison document
- `VIX_V2_SUMMARY.md` - This summary (you are here)

---

## Key Statistics Summary

| Metric | V1 | V2 | Interpretation |
|--------|----|----|----------------|
| **Total Expiries** | 317 | 317 | Same dataset |
| **Underestimated (All)** | 189 (59.6%) | 130 (41.0%) | V2 is more selective |
| **Underestimated (Weekly)** | 140 (57.1%) | 92 (37.6%) | 19.5% fewer |
| **Underestimated (Monthly)** | 49 (68.1%) | 38 (52.8%) | 15.3% fewer |
| **Average Ratio** | 1.24x | 1.24x | Unchanged |
| **Correlation** | 0.411 | 0.411 | Unchanged |

**Bottom line**: V2 doesn't change the mathematical relationships, just the classification thresholds for what counts as "significant" underestimation.

---

## Recommendation

**For most traders**: Use V2

**Reason**: The 0.2% threshold provides a more realistic assessment of VIX accuracy. In practice, differences below 0.2% are:
- Within normal market noise
- Don't require strategy adjustments
- Too small to reliably trade on

**Exception**: Use V1 if your trading strategy is extremely sensitive to VIX accuracy and you need absolute worst-case scenarios.

---

## Quick Start: Using V2

1. **Run the V2 script**:
   ```bash
   python3 backtest_vix_all_expiries_v2.py --years 6
   ```

2. **Check the CSV**:
   - Open `vix_all_expiries_results_v2.csv`
   - Look at `diff_pct` column to see actual differences
   - Filter for `vix_accuracy == "Underestimated"` to find significant cases

3. **Interpret results**:
   - Underestimated (V2) = VIX was off by >0.2%
   - Overestimated (V2) = VIX was accurate within ±0.2% OR overestimated

---

**Generated**: July 25, 2026
**Data**: 317 expiry days (June 2020 - July 2026)
**Threshold**: 0.2% difference
**Recommendation**: Use V2 for practical trading analysis
