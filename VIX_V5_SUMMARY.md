# VIX Backtest V5 - 0.5% Threshold (Most Extreme/Conservative)

## What's New in V5

**V5 uses a 0.5% threshold** (highest threshold yet) for the MOST conservative classification of VIX underestimation.

### Threshold Progression

| Version | Threshold | Classification Rule | Use Case |
|---------|-----------|---------------------|----------|
| **V1** | Any positive difference | `actual > predicted` (any amount) | Maximum caution |
| **V2** | 0.2% | `(actual - predicted) > 0.2%` | Realistic trading |
| **V3** | 0.2% | `(actual - predicted) > 0.2%` (+ visual charts) | Visual analysis |
| **V4** | 0.4% | `(actual - predicted) > 0.4%` (+ visual charts) | Significant failures |
| **V5** | **0.5%** | `(actual - predicted) > 0.5%` (+ visual charts) | **EXTREME failures only** |

---

## Impact on Results (6-Year Data: 317 Expiries)

### Classification Comparison

| Version | Threshold | Weekly Under | Monthly Under | Total Under | Change from V1 |
|---------|-----------|--------------|---------------|-------------|----------------|
| **V1** | Any diff | 140/245 (57.1%) | 49/72 (68.1%) | 189/317 (59.6%) | - |
| **V2** | >0.2% | 92/245 (37.6%) | 38/72 (52.8%) | 130/317 (41.0%) | -59 (-31.2%) |
| **V3** | >0.2% | 92/245 (37.6%) | 38/72 (52.8%) | 130/317 (41.0%) | -59 (-31.2%) |
| **V4** | >0.4% | 61/245 (24.9%) | 23/72 (31.9%) | 84/317 (26.5%) | -105 (-55.6%) |
| **V5** | **>0.5%** | **51/245 (20.8%)** | **20/72 (27.8%)** | **71/317 (22.4%)** | **-118 (-62.4%)** |

**V5 identifies 118 fewer underestimations than V1** (62.4% reduction)

This means V5 only flags the **MOST EXTREME** VIX failures, ignoring all but the worst misses.

---

## What 0.5% Means in Trading

### At NIFTY 25,000 Levels

**0.5% = 125 points**

This is a **VERY SIGNIFICANT threshold** for traders:
- Major intraday move
- Multiple option strikes breached
- Well beyond any noise or bid-ask spread
- Indicates VIX completely failed to predict volatility

### Comparison with Other Thresholds

| Threshold | NIFTY 25,000 Equivalent | Trading Impact |
|-----------|------------------------|----------------|
| **0.1%** | 25 points | Noise level |
| **0.2%** (V2/V3) | 50 points | Noticeable |
| **0.3%** | 75 points | Meaningful |
| **0.4%** (V4) | 100 points | Significant |
| **0.5%** (V5) | **125 points** | **EXTREME** |
| **1.0%** | 250 points | Catastrophic |

---

## Key Statistics (V5 Results)

### Overall (All 317 Expiries)

- **Underestimated**: 71 times (22.4%)
- **Overestimated/Accurate**: 246 times (77.6%)

**Interpretation**: VIX significantly underestimates (>0.5%) only on about **1 in 5 expiry days**.

### Weekly Expiries (245 Days)

- **Underestimated**: 51 times (20.8%)
- **Overestimated/Accurate**: 194 times (79.2%)

**Interpretation**: **4 out of 5 weekly expiries** have VIX accuracy within ±0.5%

### Monthly Expiries (72 Days)

- **Underestimated**: 20 times (27.8%)
- **Overestimated/Accurate**: 52 times (72.2%)

**Interpretation**: Monthly expiries still show more underestimation, but only ~28% are extreme (>0.5%)

---

## Progressive Filtering: V1 → V2 → V4 → V5

### How Many Cases Remain at Each Threshold?

**From the 189 underestimations in V1:**
- **130 cases** (68.8%) have diff > 0.2% → V2/V3 threshold ✓
- **84 cases** (44.4%) have diff > 0.4% → V4 threshold ✓
- **71 cases** (37.6%) have diff > 0.5% → V5 threshold ✓

**What this shows**:
- V5 catches the **top 37.6%** worst VIX predictions
- Ignores medium errors (0.2-0.4%) AND large errors (0.4-0.5%)
- Most useful for identifying days when VIX **catastrophically failed**

### Distribution Breakdown

| Difference Range | Count | % of V1 | Flagged By |
|-----------------|-------|---------|------------|
| 0.0% - 0.2% | 59 | 31.2% | V1 only |
| 0.2% - 0.4% | 46 | 24.3% | V1, V2, V3 |
| 0.4% - 0.5% | 13 | 6.9% | V1, V2, V3, V4 |
| **>0.5%** | **71** | **37.6%** | **V1, V2, V3, V4, V5** |

---

## Version Comparison Summary

### Full Comparison Table

| Metric | V1 | V2/V3 | V4 | V5 |
|--------|----|----|----|----|
| **Threshold** | Any | 0.2% | 0.4% | **0.5%** |
| **NIFTY Equivalent** | 0 pts | 50 pts | 100 pts | **125 pts** |
| **Total Under** | 189 (59.6%) | 130 (41.0%) | 84 (26.5%) | **71 (22.4%)** |
| **Weekly Under** | 140 (57.1%) | 92 (37.6%) | 61 (24.9%) | **51 (20.8%)** |
| **Monthly Under** | 49 (68.1%) | 38 (52.8%) | 23 (31.9%) | **20 (27.8%)** |
| **Philosophy** | Max caution | Realistic | Significant only | **Extreme only** |
| **Use Case** | Risk-averse traders | Daily trading | Risk management | **Crisis identification** |

---

## When to Use Each Version

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

### Use V5 (0.5% Threshold) If:
✅ You want **only catastrophic** VIX failures
✅ Crisis/black swan event identification
✅ Extreme outlier analysis
✅ Building worst-case scenario models

**Example**: Portfolio insurance specialist or tail risk hedger

---

## Practical Use Cases for V5

### Use Case 1: Black Swan Event Identification

**Scenario**: You want to identify only the most extreme volatility events

**Solution**: Use V5
- Only 71 out of 317 days flagged (22.4%)
- These are days where VIX missed by 125+ points
- Build crisis response protocols around these specific patterns

### Use Case 2: Tail Risk Hedging Strategy

**Scenario**: Designing insurance for catastrophic events

**Solution**: Filter V5 = "Underestimated"
- Get 71 worst-case days in 6 years
- Study patterns: What triggers extreme underestimation?
- Design hedges that activate only on these extreme scenarios

### Use Case 3: "Normal Day" Strategy Development

**Scenario**: Develop strategies that work in non-crisis conditions

**Solution**: Filter V5 = "Overestimated"
- Get 246 days (77.6%) where VIX was accurate within 0.5%
- These are all non-crisis days
- Strategies optimized for these days won't be skewed by outliers

---

## Example Classifications

### Case 1: Small Difference (0.12%)
```
Date: 2020-07-16
VIX Predicted: 1.38% | Actual: 1.50% | Diff: +0.12%

V1: "Underestimated" (any positive)
V2/V3: "Overestimated" (0.12% < 0.2%)
V4: "Overestimated" (0.12% < 0.4%)
V5: "Overestimated" (0.12% < 0.5%)
```
**All advanced versions agree**: Essentially accurate

### Case 2: Medium Difference (0.25%)
```
Date: Example
VIX Predicted: 0.75% | Actual: 1.00% | Diff: +0.25%

V1: "Underestimated" (any positive)
V2/V3: "Underestimated" (0.25% > 0.2%)
V4: "Overestimated" (0.25% < 0.4%)
V5: "Overestimated" (0.25% < 0.5%)
```
**V4 and V5 agree**: Not significant enough

### Case 3: Large Difference (0.48%)
```
Date: Example
VIX Predicted: 0.80% | Actual: 1.28% | Diff: +0.48%

V1: "Underestimated" (any positive)
V2/V3: "Underestimated" (0.48% > 0.2%)
V4: "Underestimated" (0.48% > 0.4%)
V5: "Overestimated" (0.48% < 0.5%)
```
**V5 alone disagrees**: Just barely misses V5 threshold

### Case 4: Extreme Difference (0.65%)
```
Date: 2020-07-30
VIX Predicted: 1.26% | Actual: 1.91% | Diff: +0.65%

V1: "Underestimated" (any positive)
V2/V3: "Underestimated" (0.65% > 0.2%)
V4: "Underestimated" (0.65% > 0.4%)
V5: "Underestimated" (0.65% > 0.5%)
```
**ALL versions agree**: This is a catastrophic miss

---

## Statistical Insights

### Underestimation by Severity

Based on V1's 189 underestimations:

| Severity Level | Diff Range | Count | % | Versions That Catch |
|---------------|------------|-------|---|-------------------|
| **Noise** | 0-0.2% | 59 | 31.2% | V1 only |
| **Minor** | 0.2-0.4% | 46 | 24.3% | V1, V2, V3 |
| **Moderate** | 0.4-0.5% | 13 | 6.9% | V1, V2, V3, V4 |
| **Severe** | 0.5-1.0% | 55 | 29.1% | All versions |
| **Extreme** | >1.0% | 16 | 8.5% | All versions |

**Key Observation**: V5 catches all severe + extreme cases (71 total = 37.6% of V1)

---

## Files Generated

### V5 Files (0.5% Threshold)
- ✅ **vix_all_expiries_results_v5.csv** - Complete dataset with 0.5% threshold
- ✅ **vix_all_expiries_results_v5.json** - JSON with 0.5% classification
- ✅ **backtest_vix_all_expiries_v5.py** - Script with 0.5% threshold

### All Versions Available
- `vix_all_expiries_results.csv` (V1 - any difference)
- `vix_all_expiries_results_v2.csv` (V2 - 0.2% threshold)
- `vix_all_expiries_results_v3.csv` (V3 - 0.2% + charts)
- `vix_all_expiries_results_v4.csv` (V4 - 0.4% + charts)
- `vix_all_expiries_results_v5.csv` (V5 - 0.5% + charts)

---

## Command to Run V5

```bash
# Run for last 6 years (recommended)
python3 backtest_vix_all_expiries_v5.py --years 6

# Run for last 2 years
python3 backtest_vix_all_expiries_v5.py --years 2

# Custom output filenames
python3 backtest_vix_all_expiries_v5.py --years 6 --csv my_v5_results.csv
```

---

## Quick Decision Matrix

**Choose your version based on your risk profile:**

| Your Question | Use This Version |
|--------------|------------------|
| "Give me the most conservative assessment" | V1 (any diff) |
| "What's realistic for trading?" | V2/V3 (0.2%) |
| "Which days had MAJOR VIX failures?" | V4 (0.4%) |
| "Which days had CATASTROPHIC VIX failures?" | **V5 (0.5%)** |
| "I need visual charts too" | V3, V4, or V5 |
| "Show me only crisis-level volatility events" | **V5 (0.5%)** |

---

## Key Insight: V5 Findings

**22.4% underestimation rate** (V5) means:

✅ **Nearly 4 out of 5 expiry days**: VIX is accurate within ±0.5%
❌ **1 out of 5 expiry days**: VIX catastrophically underestimates (>0.5%)

**For tail risk management**:
- These 1-in-5 days are your extreme scenarios
- Normal risk models work on the other 4-in-5 days
- Use V5 to build crisis protocols and tail hedges

---

## Comparison: All Versions at a Glance

| Feature | V1 | V2 | V3 | V4 | V5 |
|---------|----|----|----|----|-----|
| **Threshold** | Any | 0.2% | 0.2% | 0.4% | **0.5%** |
| **Visual Charts** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **diff_pct Column** | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Underest. Count** | 189 (59.6%) | 130 (41.0%) | 130 (41.0%) | 84 (26.5%) | **71 (22.4%)** |
| **Best Use Case** | Max conservative | Realistic trading | Visual analysis | Extreme risk ID | **Crisis/tail risk** |
| **Noise Level** | Very high | Low | Low | Very low | **Minimal** |

---

**Generated**: July 25, 2026
**Data**: 317 expiry days with 0.5% threshold
**Recommendation**: Use V5 for **tail risk analysis** and identifying only catastrophic VIX failures
