# VIX Backtest V4 - 0.4% Threshold (Most Conservative)

## What's New in V4

**V4 uses a 0.4% threshold** (double the V2/V3 threshold) for the most conservative classification of VIX underestimation.

### Threshold Comparison

| Version | Threshold | Classification Rule |
|---------|-----------|---------------------|
| **V1** | Any positive difference | `actual > predicted` (any amount) |
| **V2** | 0.2% | `(actual - predicted) > 0.2%` |
| **V3** | 0.2% | `(actual - predicted) > 0.2%` (+ visual charts) |
| **V4** | **0.4%** | `(actual - predicted) > 0.4%` (+ visual charts) |

---

## Impact on Results (6-Year Data: 317 Expiries)

### Classification Changes

| Version | Threshold | Weekly Under | Monthly Under | Total Under | Change from V1 |
|---------|-----------|--------------|---------------|-------------|----------------|
| **V1** | Any diff | 140/245 (57.1%) | 49/72 (68.1%) | 189/317 (59.6%) | - |
| **V2** | >0.2% | 92/245 (37.6%) | 38/72 (52.8%) | 130/317 (41.0%) | -59 (-31.2%) |
| **V3** | >0.2% | 92/245 (37.6%) | 38/72 (52.8%) | 130/317 (41.0%) | -59 (-31.2%) |
| **V4** | **>0.4%** | **61/245 (24.9%)** | **23/72 (31.9%)** | **84/317 (26.5%)** | **-105 (-55.6%)** |

**V4 identifies 105 fewer underestimations than V1** (55.6% reduction)

This means V4 only flags the MOST SIGNIFICANT VIX failures, ignoring minor misses.

---

## What 0.4% Means in Trading

### At NIFTY 25,000 Levels

**0.4% = 100 points**

This is a **meaningful threshold** for traders:
- Enough to matter for intraday positions
- Significant for option strike selection
- Beyond normal bid-ask spread and noise

### Comparison with Other Thresholds

| Threshold | NIFTY 25,000 Equivalent | Trading Impact |
|-----------|------------------------|----------------|
| **0.1%** | 25 points | Noise level |
| **0.2%** (V2/V3) | 50 points | Noticeable |
| **0.4%** (V4) | **100 points** | **Significant** |
| **0.5%** | 125 points | Major move |
| **1.0%** | 250 points | Rare event |

---

## Key Statistics (V4 Results)

### Overall (All 317 Expiries)

- **Underestimated**: 84 times (26.5%)
- **Overestimated**: 233 times (73.5%)

**Interpretation**: VIX significantly underestimates (>0.4%) only on about 1 in 4 expiry days.

### Weekly Expiries (245 Days)

- **Underestimated**: 61 times (24.9%)
- **Overestimated**: 184 times (75.1%)

**Interpretation**: 3 out of 4 weekly expiries have VIX accuracy within ±0.4%

### Monthly Expiries (72 Days)

- **Underestimated**: 23 times (31.9%)
- **Overestimated**: 49 times (68.1%)

**Interpretation**: Monthly expiries still show more underestimation, but only ~32% are significant (>0.4%)

---

## When Each Version is Most Useful

### Use V1 (Any Difference) If:
✅ You need **maximum conservative** approach
✅ ANY VIX error is unacceptable
✅ Building ultra-wide safety margins
✅ You're selling naked options with unlimited risk

**Example**: Market maker hedging large positions

### Use V2/V3 (0.2% Threshold) If:
✅ You want **realistic** trading signals
✅ Accept ±0.2% (50 points) as "good enough"
✅ Focus on actionable underestimations
✅ Practical backtesting of strategies

**Example**: Retail options trader with defined risk strategies

### Use V4 (0.4% Threshold) If:
✅ You want **only significant** VIX failures
✅ Filtering out all but major misses
✅ Identify extreme risk days
✅ Conservative strategy development

**Example**: Risk manager identifying high-risk expiry days

---

## Example Classifications

### Case 1: Small Difference (0.12%)
```
Date: 2020-07-16
VIX Predicted: 1.38% | Actual: 1.50% | Diff: +0.12%

V1: "Underestimated" (any positive)
V2/V3: "Overestimated" (0.12% < 0.2%)
V4: "Overestimated" (0.12% < 0.4%)
```
**All thresholds agree**: This is essentially accurate

### Case 2: Medium Difference (0.25%)
```
Date: Example
VIX Predicted: 0.75% | Actual: 1.00% | Diff: +0.25%

V1: "Underestimated" (any positive)
V2/V3: "Underestimated" (0.25% > 0.2%)
V4: "Overestimated" (0.25% < 0.4%)
```
**V4 differs**: Considers this "close enough"

### Case 3: Large Difference (0.65%)
```
Date: 2020-07-30
VIX Predicted: 1.26% | Actual: 1.91% | Diff: +0.65%

V1: "Underestimated" (any positive)
V2/V3: "Underestimated" (0.65% > 0.2%)
V4: "Underestimated" (0.65% > 0.4%)
```
**All agree**: This is a significant miss

---

## V4 Identifies Only Extreme Cases

### Distribution Analysis

**From the 189 underestimations in V1:**
- **84 cases** (44%) have diff > 0.4% → Flagged by V4 ✓
- **46 cases** (24%) have diff 0.2-0.4% → Ignored by V4 (but flagged by V2/V3)
- **59 cases** (32%) have diff < 0.2% → Ignored by V2/V3/V4

**What this means**:
- V4 catches the top ~44% worst VIX predictions
- Ignores medium-sized errors (0.2-0.4%)
- Most useful for identifying days when VIX **completely failed**

---

## Practical Use Cases

### Use Case 1: Risk Management Dashboard
**Scenario**: You want to flag only HIGH RISK expiry days

**Solution**: Use V4
- Only 84 out of 317 days flagged (26.5%)
- These are days where VIX missed by 100+ points
- Focus risk controls on these specific days

### Use Case 2: Strategy Backtesting
**Scenario**: Testing if your strategy works on "normal" expiry days

**Solution**: Filter V4 = "Overestimated"
- Get 233 days where VIX was accurate within 0.4%
- These are "typical" expiry days
- Backtest strategy without extreme outliers

### Use Case 3: Volatility Research
**Scenario**: Studying what causes major VIX failures

**Solution**: Filter V4 = "Underestimated"
- Get only 84 worst cases
- Analyze patterns: charts, VIX levels, market conditions
- Understand extreme underestimation causes

---

## Comparison: V2 vs V4

| Aspect | V2/V3 (0.2%) | V4 (0.4%) |
|--------|-------------|-----------|
| **Philosophy** | Catch all meaningful errors | Catch only extreme errors |
| **Sensitivity** | Moderate | Low |
| **Underest. Count** | 130 (41.0%) | 84 (26.5%) |
| **Best For** | Daily trading decisions | Risk management |
| **Noise Level** | Some medium errors included | Only significant errors |
| **Use Case** | "When should I widen strikes?" | "When is expiry day high risk?" |

---

## CSV Structure (V4)

Same columns as V3, with modified `vix_accuracy` classification:

```csv
date, day_of_week, expiry_type, chart, nifty_open, nifty_high, nifty_low,
nifty_close, vix_open, vix_close, vix_predicted_move_pct, actual_range_pct,
actual_open_close_pct, intraday_high_pct, intraday_low_pct, range_vs_vix_ratio,
diff_pct, vix_accuracy
```

**Key columns**:
- `diff_pct`: Actual - Predicted (in percentage points)
- `vix_accuracy`: "Underestimated" only if `diff_pct > 0.4`
- `chart`: Visual mini-chart (from V3)

---

## Files Generated

### V4 Files (0.4% Threshold)
- ✅ **vix_all_expiries_results_v4.csv** - Complete dataset with 0.4% threshold
- ✅ **vix_all_expiries_results_v4.json** - JSON with 0.4% classification
- ✅ **backtest_vix_all_expiries_v4.py** - Script with 0.4% threshold

### All Versions Available
- `vix_all_expiries_results.csv` (V1 - any difference)
- `vix_all_expiries_results_v2.csv` (V2 - 0.2% threshold)
- `vix_all_expiries_results_v3.csv` (V3 - 0.2% + charts)
- `vix_all_expiries_results_v4.csv` (V4 - 0.4% + charts)

---

## Quick Decision Matrix

**Choose your version based on your need:**

| Your Question | Use This Version |
|--------------|------------------|
| "Give me the most conservative assessment" | V1 (any diff) |
| "What's a realistic view for trading?" | V2/V3 (0.2%) |
| "Which days had MAJOR VIX failures?" | **V4 (0.4%)** |
| "I need visual charts too" | V3 or V4 |

---

## Command to Run V4

```bash
# Run for last 6 years (recommended)
python3 backtest_vix_all_expiries_v4.py --years 6

# Run for last 2 years
python3 backtest_vix_all_expiries_v4.py --years 2

# Custom output filenames
python3 backtest_vix_all_expiries_v4.py --years 6 --csv my_v4_results.csv
```

---

## Summary Table: All Versions

| Feature | V1 | V2 | V3 | V4 |
|---------|----|----|----|----|
| **Threshold** | Any | 0.2% | 0.2% | 0.4% |
| **Visual Charts** | ❌ | ❌ | ✅ | ✅ |
| **diff_pct Column** | ❌ | ✅ | ✅ | ✅ |
| **Underest. Count** | 189 (59.6%) | 130 (41.0%) | 130 (41.0%) | 84 (26.5%) |
| **Best Use Case** | Max conservative | Realistic trading | Visual analysis | Extreme risk ID |
| **Noise Level** | High (catches everything) | Low | Low | Very low |

---

## Key Insight: V4 Findings

**26.5% underestimation rate** (V4) means:

✅ **3 out of 4 expiry days**: VIX is accurate within ±0.4%
❌ **1 out of 4 expiry days**: VIX significantly underestimates (>0.4%)

**For risk management**:
- Focus extra caution on the 1-in-4 high-risk days
- Normal risk controls sufficient for other 3-in-4 days
- Use V4 to identify which is which

---

**Generated**: July 25, 2026
**Data**: 317 expiry days with 0.4% threshold
**Recommendation**: Use V4 for **conservative risk management** and identifying only extreme VIX failures
