# FII/DII + Sensex VIX Expiry-Day Correlation Analysis (6-Year)

**Generated**: 2026-09-11 22:29
**Period**: 2020-06-26 to 2026-09-10
**Sensex Expiry Days Analyzed**: 312
**Blowout Base Rate**: 22.8% (71/312 days)
**Above-Median Range Rate**: 49.7%
**Nifty Co-Expiry Days**: 52/312 (17%)

---

## Executive Summary

**Best FII pre-market signal (blowout)**: `fii_put_buying_heavy`
- Blowout rate: 30% (lift: 1.3x vs 23% base)
- Triggers on: 60/312 days (19%)

**Best FII pre-market signal (above-median range)**: `fii_fut_selling_heavy`
- Above-median rate: 57% (lift: 1.1x)
- Avg range: 1.13%

**VIX intraday benchmark**: `vix_change > 0.5`
- Blowout rate: 51% (lift: 2.2x)
- Above-median rate: 85% (alt lift: 1.7x)
- Triggers on: 39/312 days

---

## Correlation Findings (6-Year)

### FII T-1 Signals vs Blowout

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_fii_fut_daily | -0.056 | 0.328 | No | 312 |
| fii_net_flow | +0.055 | 0.335 | No | 312 |
| fii_pcr | +0.032 | 0.569 | No | 312 |
| t1_fii_call_daily | +0.031 | 0.582 | No | 312 |
| t1_fii_put_daily | -0.031 | 0.590 | No | 312 |

### FII T-1 Signals vs Actual Range

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_fii_fut_daily | -0.095 | 0.095 | No | 312 |
| t1_fii_call_daily | +0.090 | 0.111 | No | 312 |
| t1_fii_put_daily | +0.054 | 0.345 | No | 312 |
| fii_pcr | +0.042 | 0.464 | No | 312 |
| fii_net_flow | +0.007 | 0.900 | No | 312 |

### FII T-1 Signals vs Above-Median Range

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_fii_fut_daily | -0.089 | 0.118 | No | 312 |
| fii_pcr | +0.076 | 0.183 | No | 312 |
| t1_fii_call_daily | +0.041 | 0.466 | No | 312 |
| t1_fii_put_daily | +0.020 | 0.720 | No | 312 |
| fii_net_flow | -0.010 | 0.863 | No | 312 |

### PRO T-1 Signals vs Blowout

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_pro_call_daily | +0.122 | 0.031 | Yes | 312 |
| t1_pro_fut_daily | +0.069 | 0.222 | No | 312 |
| t1_pro_put_daily | -0.034 | 0.548 | No | 312 |

---

## FII Stance vs Blowout (6-Year)

| Stance | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |
|--------|-------|----------|-------------|---------------|-----------|
| FII Very Bearish (sold fut >10K + bought puts >20K) | 25 | 8 | 32% | 60% | 1.16% |
| FII Hedging (bought puts >20K) | 34 | 10 | 29% | 35% | 0.96% |
| FII Bearish (sold fut >10K) | 50 | 13 | 26% | 56% | 1.12% |
| FII Confident (sold puts >20K) | 64 | 16 | 25% | 52% | 1.04% |
| FII Bullish (bought fut + sold puts) | 47 | 11 | 23% | 49% | 1.01% |
| FII Neutral | 50 | 8 | 16% | 54% | 1.08% |
| FII Mildly Bearish | 16 | 2 | 12% | 31% | 0.92% |
| FII Mildly Bullish | 25 | 3 | 12% | 48% | 1.03% |
| FII Very Bearish (sold fut + bought puts) ⚠️ | 1 | 0 | 0% | 0% | 0.75% |

### FII Direction vs Blowout

| Direction | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |
|-----------|-------|----------|-------------|---------------|-----------|
| Bearish | 112 | 24 | 21% | 46% | 1.01% |
| Bullish | 136 | 34 | 25% | 50% | 1.05% |
| Neutral | 64 | 13 | 20% | 55% | 1.11% |

### Nifty Co-Expiry Effect

| Type | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |
|------|-------|----------|-------------|---------------|-----------|
| sensex_only | 260 | 65 | 25% | 51% | 1.07% |
| nifty_co_expiry | 52 | 6 | 12% | 42% | 0.95% |

---

## Prediction Rule Testing (6-Year)

**Base blowout rate**: 23% (71/312 days)
**Above-median range rate**: 50%

### All Rules Ranked by Blowout Lift

| Rule | Triggers | Blowout Rate | Lift | Above-Med Rate | Alt Lift | Avg Range | Type |
|------|----------|-------------|------|---------------|----------|-----------|------|
| vix_change_gt_1.0 | 15 | 67% | 2.9x | 93% | 1.9x | 1.82% | Intraday |
| vix_change_gt_0.5 | 39 | 51% | 2.2x | 85% | 1.7x | 1.56% | Intraday |
| fii_put_buying_heavy | 60 | 30% | 1.3x | 45% | 0.9x | 1.04% | Pre-market |
| FII_Hedging_stance | 34 | 29% | 1.3x | 35% | 0.7x | 0.96% | Pre-market |
| fii_fut_selling_heavy | 76 | 28% | 1.2x | 57% | 1.1x | 1.13% | Pre-market |
| fii_pcr_above_75pct | 78 | 27% | 1.2x | 51% | 1.0x | 1.06% | Pre-market |
| FII_Direction_Bullish | 136 | 25% | 1.1x | 50% | 1.0x | 1.05% | Pre-market |
| FII_Bearish_stance | 92 | 25% | 1.1x | 52% | 1.1x | 1.09% | Pre-market |
| FII_Confident_stance | 64 | 25% | 1.1x | 52% | 1.0x | 1.04% | Pre-market |
| sensex_only_expiry | 260 | 25% | 1.1x | 51% | 1.0x | 1.07% | Pre-market |
| fii_pcr_above_median | 156 | 24% | 1.0x | 49% | 1.0x | 1.06% | Pre-market |
| fii_net_flow_negative | 143 | 22% | 1.0x | 49% | 1.0x | 1.04% | Pre-market |
| FII_Direction_Bearish | 112 | 21% | 0.9x | 46% | 0.9x | 1.01% | Pre-market |
| fii_net_flow_very_negative | 78 | 21% | 0.9x | 45% | 0.9x | 1.00% | Pre-market |
| FII_Direction_Neutral | 64 | 20% | 0.9x | 55% | 1.1x | 1.11% | Pre-market |
| FII_Bullish_stance | 72 | 19% | 0.8x | 49% | 1.0x | 1.02% | Pre-market |
| fii_pcr_below_25pct | 78 | 18% | 0.8x | 47% | 0.9x | 1.02% | Pre-market |
| vix_change_lt_0 | 207 | 17% | 0.8x | 42% | 0.8x | 0.95% | Intraday |
| FII_Bearish_AND_VIX_lt16 | 70 | 17% | 0.8x | 33% | 0.7x | 0.88% | Pre-market |
| FII_Bearish_AND_VIX_lt14 | 51 | 12% | 0.5x | 24% | 0.5x | 0.80% | Pre-market |
| is_nifty_expiry_day | 52 | 12% | 0.5x | 42% | 0.8x | 0.95% | Pre-market |
| FII_Bearish_AND_nifty_expiry | 24 | 8% | 0.4x | 38% | 0.8x | 0.87% | Pre-market |

---

## Sensex vs Nifty Comparison

| Metric | Sensex (6yr) | Nifty (1yr overlap) |
|--------|-------------|-------------------|
| Days analyzed | 312 | 50 |
| Blowout count | 71 | 11 |
| Blowout rate | 22.8% | 22.0% |

---

## Trading Implications

1. **FII signals show limited blowout prediction**: Best pre-market signal achieves only 1.3x lift over 23% base rate
3. **FII signals do not reliably predict range magnitude**: Best alt lift is only 1.1x
4. **VIX intraday remains dominant**: 51% blowout rate (2.2x lift)

### Recommendation

FII positioning data does NOT reliably predict Sensex VIX blowouts. Continue using VIX intraday behavior as the primary signal.

---

*Analysis based on 312 Sensex expiry days with valid FII T-1 data.*
