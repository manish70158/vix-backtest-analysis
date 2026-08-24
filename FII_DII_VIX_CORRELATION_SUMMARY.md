# FII/DII + VIX Expiry-Day Correlation Analysis

**Generated**: 2026-08-24 18:30
**Overlap Period**: 2025-08-14 to 2026-07-21
**Expiry Days Analyzed**: 50
**Blowout Base Rate**: 22.0% (11/50 days)

---

## Executive Summary

**Best FII pre-market signal**: `FII_Direction_Bearish`
- Blowout rate: 67% (lift: 3.0x vs 22% base)
- Triggers on: 3/50 days (6%)

**VIX intraday benchmark** (for comparison): `vix_change > 0.5`
- Blowout rate: 100% (lift: 4.5x)
- Triggers on: 6/50 days

---

## Correlation Findings

### Same-Day FII Signals vs Blowout

| Signal | Correlation | p-value | Significant? |
|--------|------------|---------|-------------|
| fii_fut_idx_net | -0.305 | 0.031 | Yes |
| fii_call_net | -0.326 | 0.021 | Yes |
| fii_put_net | +0.242 | 0.090 | No |
| fii_pcr | -0.172 | 0.234 | No |
| fii_net_sentiment | -0.306 | 0.031 | Yes |
| fii_put_change | +0.269 | 0.062 | No |

### Same-Day FII Signals vs Actual Range

| Signal | Correlation | p-value | Significant? |
|--------|------------|---------|-------------|
| fii_fut_idx_net | -0.320 | 0.023 | Yes |
| fii_call_net | -0.440 | 0.001 | Yes |
| fii_put_net | +0.236 | 0.099 | No |
| fii_pcr | -0.108 | 0.454 | No |
| fii_net_sentiment | -0.353 | 0.012 | Yes |
| fii_put_change | +0.108 | 0.459 | No |

### T-1 Pre-Market FII Signals (Observable Before Open)

| Signal | vs Blowout | p-value | vs Range | p-value |
|--------|-----------|---------|---------|---------|
| t1_fii_call_net | -0.328 | 0.020 | -0.474 | 0.001 |
| t1_fii_fut_idx_net | -0.318 | 0.024 | -0.372 | 0.008 |
| t1_fii_pcr | -0.098 | 0.501 | -0.252 | 0.078 |
| t1_fii_put_net | +0.270 | 0.058 | +0.350 | 0.013 |

---

## Direction Signal Cross-Tabulation

### FII_Direction vs Blowout

| Direction | Count | Blowouts | Blowout Rate | Avg Range |
|-----------|-------|----------|-------------|-----------|
| Neutral | 27 | 7 | 26% | 0.97% |
| Bullish | 20 | 2 | 10% | 0.85% |
| Bearish | 3 | 2 | 67% | 1.32% |

### DII_Direction vs Blowout

| Direction | Count | Blowouts | Blowout Rate | Avg Range |
|-----------|-------|----------|-------------|-----------|
| Neutral | 24 | 3 | 12% | 0.81% |
| Bullish | 26 | 8 | 31% | 1.07% |

### Pro_Direction vs Blowout

| Direction | Count | Blowouts | Blowout Rate | Avg Range |
|-----------|-------|----------|-------------|-----------|
| Bearish | 5 | 2 | 40% | 1.04% |
| Neutral | 26 | 4 | 15% | 0.93% |
| Bullish | 19 | 5 | 26% | 0.94% |

### Client_Direction vs Blowout

| Direction | Count | Blowouts | Blowout Rate | Avg Range |
|-----------|-------|----------|-------------|-----------|
| Neutral | 27 | 6 | 22% | 0.97% |
| Bearish | 23 | 5 | 22% | 0.92% |

### t1_FII_Direction vs Blowout

| Direction | Count | Blowouts | Blowout Rate | Avg Range |
|-----------|-------|----------|-------------|-----------|
| Neutral | 29 | 7 | 24% | 0.99% |
| Bullish | 16 | 2 | 12% | 0.70% |
| Bearish | 5 | 2 | 40% | 1.46% |

### Consensus Count (participants matching market direction)

| Consensus | Count | Blowouts | Blowout Rate | Avg Range |
|-----------|-------|----------|-------------|-----------|
| 0/4 | 14 | 2 | 14% | 0.79% |
| 1/4 | 26 | 5 | 19% | 0.97% |
| 2/4 | 7 | 3 | 43% | 0.92% |
| 3/4 | 3 | 1 | 33% | 1.49% |

---

## Prediction Rule Testing

**Base blowout rate**: 22% (11/50 days)

### All Rules Ranked by Lift

| Rule | Triggers | Blowout Rate | Lift | Type |
|------|----------|-------------|------|------|
| vix_change_gt_0.5 | 6 | 100% | 4.5x | Intraday |
| FII_Direction_Bearish | 3 | 67% | 3.0x | Pre-market |
| t1_FII_Direction_Bearish | 5 | 40% | 1.8x | Pre-market |
| fii_pcr_below_25pct | 13 | 38% | 1.8x | Pre-market |
| consensus_ge3 | 3 | 33% | 1.5x | Pre-market |
| fii_put_change_positive | 31 | 26% | 1.2x | Pre-market |
| t1_FII_Direction_Bullish | 16 | 12% | 0.6x | Pre-market |
| fii_pcr_above_median | 25 | 12% | 0.6x | Pre-market |
| vix_change_lt_0 | 34 | 12% | 0.5x | Intraday |
| FII_Direction_Bullish | 20 | 10% | 0.5x | Pre-market |
| fii_pcr_above_75pct | 13 | 0% | 0.0x | Pre-market |

---

## Trading Implications

### Key Findings

1. **FII signals show meaningful lift**: Best pre-market FII signal achieves 1.8x lift over base rate
2. Consider integrating FII direction into the pre-market tier system
3. **VIX intraday signal remains dominant**: 100% blowout rate (4.5x lift) far exceeds any FII signal

### Recommendation

FII positioning data adds marginal pre-market value. Use as a secondary sizing signal alongside the primary VIX intraday confirmation.

---

**Sample size warning**: Analysis based on 50 expiry days. Subgroup findings with n<10 are unreliable.
