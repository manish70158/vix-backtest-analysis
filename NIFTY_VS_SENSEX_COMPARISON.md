# NIFTY vs SENSEX: VIX Expiry Day Analysis Comparison

## Quick Comparison Table

| Metric | NIFTY 50 | SENSEX 30 | Better For Trading |
|--------|----------|-----------|-------------------|
| **Total Expiries** | 317 | 318 | - |
| **Period** | Jun 2020 - Jul 2026 | Jun 2020 - Jul 2026 | - |
| **Average VIX** | 16.22 | 15.93 | Similar |
| **Avg Predicted** | 0.85% | 0.83% | Similar |
| **Avg Actual** | 1.04% | 1.07% | NIFTY (lower) |
| **Avg Ratio** | 1.24x | 1.29x | **NIFTY (lower)** ✅ |
| **VIX Correlation** | 0.411 | 0.450 | **SENSEX (higher)** ✅ |
| **Underestimated (>0.5%)** | 71 (22.4%) | 76 (23.9%) | **NIFTY (less)** ✅ |
| **Green Zone (0-0.5%)** | 120 (37.9%) | 128 (40.3%) | **SENSEX (more)** ✅ |

---

## Weekly Expiries

| Metric | NIFTY | SENSEX | Winner |
|--------|-------|--------|--------|
| **Count** | 245 | 245 | - |
| **Avg Ratio** | 1.22x | 1.28x | NIFTY (lower) |
| **Underestimated** | 51 (20.8%) | 55 (22.4%) | NIFTY (less) |
| **Correlation** | 0.394 | 0.405 | SENSEX (higher) |

---

## Monthly Expiries

| Metric | NIFTY | SENSEX | Winner |
|--------|-------|--------|--------|
| **Count** | 72 | 73 | - |
| **Avg Ratio** | 1.32x | 1.33x | Nearly identical |
| **Underestimated** | 20 (27.8%) | 21 (28.8%) | Nearly identical |
| **Correlation** | 0.461 | 0.563 | **SENSEX (much higher)** |

---

## Weekly vs Monthly Volatility

### NIFTY
```
Weekly: 1.22x
Monthly: 1.32x
Difference: 0.10x (8% higher monthly)
```
**Classification**: MORE volatile on monthly expiries

### SENSEX
```
Weekly: 1.28x
Monthly: 1.33x
Difference: 0.05x (4% higher monthly)
```
**Classification**: SIMILAR volatility (negligible difference)

---

## Expiry Day Schedules

### NIFTY (NSE)
- **Before Sep 1, 2025**: Thursday (weekday=3)
- **From Sep 1, 2025 onwards**: Tuesday (weekday=1)

### SENSEX (BSE)
- **Before Jan 1, 2025**: Friday (weekday=4)
- **Jan 1 - Sep 3, 2025**: Tuesday (weekday=1)
- **From Sep 4, 2025 onwards**: Thursday (weekday=3)

---

## Trading Recommendations

### Choose NIFTY If You Want:

1. ✅ **Lower volatility** (1.24x vs 1.29x)
   - Better for conservative option sellers
   - Tighter stop losses work better

2. ✅ **Higher liquidity**
   - NSE derivatives > BSE derivatives
   - Better fills, tighter spreads

3. ✅ **Less underestimation risk** (22.4% vs 23.9%)
   - VIX more reliable for NIFTY
   - Fewer extreme events

4. ✅ **More diversification** (50 stocks vs 30)
   - Single stock impact lower
   - Smoother price action

### Choose SENSEX If You Want:

1. ✅ **Better VIX correlation** (0.450 vs 0.411)
   - VIX predictions more accurate
   - Technical analysis more reliable

2. ✅ **More "acceptable miss" days** (40.3% vs 37.9%)
   - Green zone is larger
   - VIX guidance useful more often

3. ✅ **Consistent weekly-monthly behavior** (0.05x diff vs 0.10x)
   - No need to adjust strategy for monthlies
   - Same risk management year-round

4. ✅ **Stronger monthly correlation** (0.563 vs 0.461)
   - Monthly options trading more predictable
   - Better for long-term positions

---

## Position Sizing Recommendations

### For NIFTY (at 25,000)

**Conservative Buffer**: 0.5%
```
VIX 15 → 0.79% + 0.5% = 1.29%
Range: 25,000 ± 323 points
Sell strikes: 24,675 PUT / 25,325 CALL
```

**Moderate Buffer**: 0.3%
```
VIX 15 → 0.79% + 0.3% = 1.09%
Range: 25,000 ± 273 points
Sell strikes: 24,725 PUT / 25,275 CALL
```

### For SENSEX (at 50,000)

**Conservative Buffer**: 0.5%
```
VIX 15 → 0.79% + 0.5% = 1.29%
Range: 50,000 ± 645 points
Sell strikes: 49,350 PUT / 50,650 CALL
```

**Moderate Buffer**: 0.3%
```
VIX 15 → 0.79% + 0.3% = 1.09%
Range: 50,000 ± 545 points
Sell strikes: 49,450 PUT / 50,550 CALL
```

---

## Risk Assessment

### NIFTY
**Strengths**:
- Lower average volatility ✅
- Higher liquidity ✅
- More stable (50 stocks) ✅
- Industry standard ✅

**Weaknesses**:
- Lower VIX correlation ❌
- Monthly expiries 8% more volatile ❌
- Smaller "acceptable miss" zone ❌

### SENSEX
**Strengths**:
- Better VIX correlation ✅
- Consistent weekly-monthly ✅
- Larger "acceptable miss" zone ✅
- Strong monthly correlation ✅

**Weaknesses**:
- Higher average volatility ❌
- Lower liquidity ❌
- Concentrated (30 stocks) ❌
- Less traded derivatives ❌

---

## Which Index is "Better"?

### For Different Trader Types

**Retail Options Sellers** (Premium collection):
- **Winner**: NIFTY
- **Reason**: Lower volatility, higher liquidity, tighter stop losses

**Institutional Traders** (Large positions):
- **Winner**: NIFTY
- **Reason**: Liquidity is paramount, slippage kills profitability

**Technical Analysts** (VIX-based strategies):
- **Winner**: SENSEX
- **Reason**: Better correlation with VIX (0.450 vs 0.411)

**Monthly Options Traders** (Longer duration):
- **Winner**: SENSEX
- **Reason**: Much better monthly correlation (0.563 vs 0.461)

**Risk Managers** (Minimize surprises):
- **Winner**: NIFTY
- **Reason**: Lower underestimation rate (22.4% vs 23.9%)

**Quantitative Traders** (Model-based):
- **Winner**: SENSEX
- **Reason**: Better predictability, stronger correlations

---

## Combined Strategy

### Trade Both for Diversification

**Correlation between NIFTY and SENSEX**: ~0.95
- While highly correlated, not identical
- Different expiry days = different gamma exposure
- Different constituent stocks = different sector exposures

**Sample Portfolio**:
```
40% NIFTY options (focus on weekly)
30% SENSEX options (focus on monthly)
30% Cash / hedges
```

**Benefits**:
- Spread expiry risk across different days
- Capitalize on different volatility profiles
- Diversify counterparty/exchange risk

---

## Statistical Summary

### Underestimation by Severity

#### NIFTY (317 expiries)
| Severity | Diff Range | Count | % |
|----------|-----------|-------|---|
| Overestimated | < 0.0% | 125 | 39.4% |
| Minor | 0.0-0.2% | 59 | 18.6% |
| Acceptable | 0.2-0.5% | 61 | 19.2% |
| **Significant** | **> 0.5%** | **69** | **21.8%** |
| Near-perfect | < 0.01% | 3 | 0.9% |

#### SENSEX (318 expiries)
| Severity | Diff Range | Count | % |
|----------|-----------|-------|---|
| Overestimated | < 0.0% | 112 | 35.2% |
| Minor | 0.0-0.2% | 61 | 19.2% |
| Acceptable | 0.2-0.5% | 67 | 21.1% |
| **Significant** | **> 0.5%** | **75** | **23.6%** |
| Near-perfect | < 0.01% | 3 | 0.9% |

**Key Difference**: SENSEX has **larger "acceptable" zone** (21.1% vs 19.2%)

---

## Trading Calendar Considerations

### 2025-2026 Expiry Schedule

**NIFTY** (NSE):
- Weekly: Every Tuesday
- Monthly: Last Tuesday of month

**SENSEX** (BSE):
- Weekly (before Sep 2025): Every Tuesday
- Weekly (from Sep 2025): Every Thursday
- Monthly: Last Thursday of month

**Overlap Period** (Jan - Sep 2025):
- Both indices expire on Tuesday
- High gamma concentration on single day
- Consider staggering positions

**Post-Sep 2025**:
- NIFTY Tuesday / SENSEX Thursday
- Better risk distribution
- Two gamma expiry days per week

---

## Real-World Example

### Scenario: VIX at 15 on Expiry Day

#### NIFTY at 25,000
```
Predicted move: 15 / 19.1 = 0.79%
Historical ratio: 1.24x
Expected actual: 0.79% × 1.24 = 0.98%
Range: ±245 points

Conservative strikes:
- PUT: 24,750 (1% OTM)
- CALL: 25,250 (1% OTM)

Risk: 22.4% chance of >0.5% miss
      = 1.29% actual = ±323 points
```

#### SENSEX at 50,000
```
Predicted move: 15 / 19.1 = 0.79%
Historical ratio: 1.29x
Expected actual: 0.79% × 1.29 = 1.02%
Range: ±510 points

Conservative strikes:
- PUT: 49,500 (1% OTM)
- CALL: 50,500 (1% OTM)

Risk: 23.9% chance of >0.5% miss
      = 1.29% actual = ±645 points
```

**Verdict**: NIFTY requires ~80 points less buffer per side

---

## Final Recommendation

### Best Overall: **NIFTY**

**Primary reasons**:
1. **Liquidity is king** - Better fills, tighter spreads
2. **Lower volatility** - 4% less volatile (1.24x vs 1.29x)
3. **Industry standard** - More research, more traders, better tools
4. **Proven track record** - NSE derivatives are world-class

**When to use SENSEX**:
- Monthly options (better correlation: 0.563)
- VIX-based systematic strategies (better overall correlation: 0.450)
- When seeking Tuesday expiries after Sep 2025 (diversification)
- Research/academic purposes (cleaner 30-stock basket)

### Hybrid Approach (Recommended)

**70% NIFTY / 30% SENSEX**
- Core positions on NIFTY (liquidity + stability)
- Satellite positions on SENSEX (correlation benefits)
- Diversify expiry days for smoother gamma decay

---

**Generated**: July 25, 2026
**Data Period**: June 2020 - July 2026 (6 years)
**Methodology**: 0.5% threshold, identical for both indices
**Recommendation**: Trade primarily NIFTY, use SENSEX for diversification
