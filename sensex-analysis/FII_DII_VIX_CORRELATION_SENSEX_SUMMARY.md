# FII/DII + Sensex VIX Expiry-Day Correlation Analysis (6-Year)

**Generated**: 2026-08-26 21:10
**Period**: 2020-06-26 to 2026-07-23
**Sensex Expiry Days Analyzed**: 305
**Blowout Base Rate**: 22.9% (70/305 days)
**Above-Median Range Rate**: 49.2%
**Nifty Co-Expiry Days**: 45/305 (15%)

---

## Executive Summary

**Best FII pre-market signal (blowout)**: `fii_put_buying_heavy`
- Blowout rate: 30% (lift: 1.3x vs 23% base)
- Triggers on: 60/305 days (20%)

**Best FII pre-market signal (above-median range)**: `fii_fut_selling_heavy`
- Above-median rate: 57% (lift: 1.1x)
- Avg range: 1.15%

**VIX intraday benchmark**: `vix_change > 0.5`
- Blowout rate: 51% (lift: 2.2x)
- Above-median rate: 85% (alt lift: 1.7x)
- Triggers on: 39/305 days

---

## Correlation Findings (6-Year)

### FII T-1 Signals vs Blowout

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_fii_fut_daily | -0.057 | 0.325 | No | 305 |
| fii_net_flow | +0.054 | 0.346 | No | 305 |
| fii_pcr | +0.034 | 0.549 | No | 305 |
| t1_fii_call_daily | +0.033 | 0.565 | No | 305 |
| t1_fii_put_daily | -0.028 | 0.623 | No | 305 |

### FII T-1 Signals vs Actual Range

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_fii_fut_daily | -0.101 | 0.080 | No | 305 |
| t1_fii_call_daily | +0.089 | 0.120 | No | 305 |
| t1_fii_put_daily | +0.059 | 0.307 | No | 305 |
| fii_pcr | +0.047 | 0.414 | No | 305 |
| fii_net_flow | -0.003 | 0.955 | No | 305 |

### FII T-1 Signals vs Above-Median Range

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_fii_fut_daily | -0.092 | 0.110 | No | 305 |
| fii_pcr | +0.081 | 0.159 | No | 305 |
| t1_fii_call_daily | +0.037 | 0.523 | No | 305 |
| t1_fii_put_daily | +0.024 | 0.675 | No | 305 |
| fii_net_flow | -0.022 | 0.705 | No | 305 |

### PRO T-1 Signals vs Blowout

| Signal | Correlation | p-value | Significant? | n |
|--------|------------|---------|-------------|---|
| t1_pro_call_daily | +0.125 | 0.029 | Yes | 305 |
| t1_pro_fut_daily | +0.073 | 0.204 | No | 305 |
| t1_pro_put_daily | -0.034 | 0.552 | No | 305 |

---

## FII Stance vs Blowout (6-Year)

| Stance | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |
|--------|-------|----------|-------------|---------------|-----------|
| FII Very Bearish (sold fut >10K + bought puts >20K) | 26 | 8 | 31% | 58% | 1.14% |
| FII Hedging (bought puts >20K) | 34 | 10 | 29% | 35% | 0.96% |
| FII Bearish (sold fut >10K) | 48 | 13 | 27% | 56% | 1.16% |
| FII Confident (sold puts >20K) | 62 | 15 | 24% | 50% | 1.05% |
| FII Bullish (bought fut + sold puts) | 46 | 11 | 24% | 48% | 1.02% |
| FII Neutral | 50 | 8 | 16% | 54% | 1.08% |
| FII Mildly Bearish | 14 | 2 | 14% | 36% | 0.96% |
| FII Mildly Bullish | 25 | 3 | 12% | 44% | 1.03% |

### FII Direction vs Blowout

| Direction | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |
|-----------|-------|----------|-------------|---------------|-----------|
| Bearish | 106 | 23 | 22% | 47% | 1.04% |
| Bullish | 135 | 34 | 25% | 48% | 1.05% |
| Neutral | 64 | 13 | 20% | 55% | 1.11% |

### Nifty Co-Expiry Effect

| Type | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |
|------|-------|----------|-------------|---------------|-----------|
| sensex_only | 260 | 65 | 25% | 50% | 1.07% |
| nifty_co_expiry | 45 | 5 | 11% | 47% | 1.01% |

---

## Prediction Rule Testing (6-Year)

**Base blowout rate**: 23% (70/305 days)
**Above-median range rate**: 49%

### All Rules Ranked by Blowout Lift

| Rule | Triggers | Blowout Rate | Lift | Above-Med Rate | Alt Lift | Avg Range | Type |
|------|----------|-------------|------|---------------|----------|-----------|------|
| vix_change_gt_1.0 | 15 | 67% | 2.9x | 93% | 1.9x | 1.82% | Intraday |
| vix_change_gt_0.5 | 39 | 51% | 2.2x | 85% | 1.7x | 1.56% | Intraday |
| fii_put_buying_heavy | 60 | 30% | 1.3x | 45% | 0.9x | 1.04% | Pre-market |
| FII_Hedging_stance | 34 | 29% | 1.3x | 35% | 0.7x | 0.96% | Pre-market |
| fii_fut_selling_heavy | 74 | 28% | 1.2x | 57% | 1.1x | 1.15% | Pre-market |
| fii_pcr_above_75pct | 76 | 28% | 1.2x | 50% | 1.0x | 1.06% | Pre-market |
| FII_Bearish_stance | 88 | 26% | 1.1x | 53% | 1.1x | 1.12% | Pre-market |
| FII_Direction_Bullish | 135 | 25% | 1.1x | 48% | 1.0x | 1.05% | Pre-market |
| sensex_only_expiry | 260 | 25% | 1.1x | 50% | 1.0x | 1.07% | Pre-market |
| fii_pcr_above_median | 152 | 24% | 1.1x | 49% | 1.0x | 1.07% | Pre-market |
| FII_Confident_stance | 62 | 24% | 1.1x | 50% | 1.0x | 1.05% | Pre-market |
| fii_net_flow_negative | 137 | 23% | 1.0x | 50% | 1.0x | 1.06% | Pre-market |
| fii_net_flow_very_negative | 76 | 22% | 1.0x | 47% | 1.0x | 1.03% | Pre-market |
| FII_Direction_Bearish | 106 | 22% | 0.9x | 47% | 1.0x | 1.04% | Pre-market |
| FII_Direction_Neutral | 64 | 20% | 0.9x | 55% | 1.1x | 1.11% | Pre-market |
| FII_Bullish_stance | 71 | 20% | 0.9x | 46% | 0.9x | 1.02% | Pre-market |
| fii_pcr_below_25pct | 76 | 18% | 0.8x | 46% | 0.9x | 1.03% | Pre-market |
| FII_Bearish_AND_VIX_lt16 | 64 | 17% | 0.8x | 34% | 0.7x | 0.91% | Pre-market |
| vix_change_lt_0 | 202 | 17% | 0.8x | 41% | 0.8x | 0.96% | Intraday |
| FII_Bearish_AND_VIX_lt14 | 45 | 11% | 0.5x | 24% | 0.5x | 0.83% | Pre-market |
| is_nifty_expiry_day | 45 | 11% | 0.5x | 47% | 0.9x | 1.01% | Pre-market |
| FII_Bearish_AND_nifty_expiry | 18 | 6% | 0.2x | 44% | 0.9x | 0.97% | Pre-market |

---

## Sensex vs Nifty Comparison

| Metric | Sensex (6yr) | Nifty (1yr overlap) |
|--------|-------------|-------------------|
| Days analyzed | 305 | 50 |
| Blowout count | 70 | 11 |
| Blowout rate | 22.9% | 22.0% |

---

## Trading Implications

1. **FII signals show limited blowout prediction**: Best pre-market signal achieves only 1.3x lift over 23% base rate
3. **FII signals do not reliably predict range magnitude**: Best alt lift is only 1.1x
4. **VIX intraday remains dominant**: 51% blowout rate (2.2x lift)

### Recommendation

FII positioning data does NOT reliably predict Sensex VIX blowouts. Continue using VIX intraday behavior as the primary signal.

---

---

## Data Sources & Directory Structure

All Sensex analysis files are consolidated in `sensex-analysis/`:

| Source | File | Description |
|--------|------|-------------|
| NSE Archives | `sensex_participant_wise_daily.csv` | Daily FII/PRO/DII/Client positions (separate) |
| NSE Archives | `sensex_fii_t1_6year_expiry.csv` | T-1 FII/PRO data for 318 expiry days |
| NSDL FPI | `bse_fpi_participant_daily.csv` | FPI equity + derivatives (aggregated) |
| Derived | `fii_dii_vix_correlation_sensex.csv` | 305 expiry days with all features |

**Note**: BSE India API (api.bseindia.com) is protected by Akamai WAF. NSE participant-wise OI archives used as equivalent source (covers same institutional positioning).

*Analysis based on 305 Sensex expiry days with valid FII T-1 data.*
