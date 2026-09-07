# Validation Report: fii_pro_alignment_results_v2.csv

> **Generated**: 2026-09-01
> **Data**: 1,484 trading days | Aug 2020 - Sep 2026
> **V2 Change**: Neutral band narrowed from ±30k to ±25k composite. Mildly band widened from 30k-50k to 25k-50k.

---

## Part 1: Data Integrity

| Check | Result | Details |
|-------|--------|---------|
| Null values in critical columns | **PASS** | 0 nulls across all 9 critical columns |
| OHLC integrity | **PASS** | 0 violations |
| Result (Green/Red/Flat) vs computed | **PASS** | 8 correctly labeled "Flat" rows |
| change_pct accuracy | **PASS** | 0 rows >0.05% deviation |
| up_from_open accuracy | **PASS** | 0 rows >0.1 pt deviation |
| down_from_open accuracy | **PASS** | 0 rows >0.1 pt deviation |
| Alignment logic (bucket → alignment) | **PASS** | 0 mismatches |
| close_outcome consistency | **PASS** | 321 Worked = 321 wins, 316 Reversed = 316 losses |

---

## Part 2: V2 Threshold Application

| Check | Result | Details |
|-------|--------|---------|
| fii_view vs composite (V2 thresholds) | **PASS** | 0 mismatches across 1,484 rows |
| pro_view vs composite (V2 thresholds) | **PASS** | 0 mismatches |
| FII composite 25k-30k → Mildly Bullish | **PASS** | All 43 rows correct |
| FII composite -30k to -25k → Mildly Bearish | **PASS** | All 37 rows correct |
| PRO composite 25k-30k → Mildly Bullish | **PASS** | All 15 rows correct |
| PRO composite -30k to -25k → Mildly Bearish | **PASS** | All 15 rows correct |
| No reverse shifts (non-Neutral → Neutral) | **PASS** | 0 FII, 0 PRO |

**80 FII rows** and **30 PRO rows** correctly shifted from Neutral to Mildly categories.

---

## Part 3: Alignment Signal Win Rate

| Metric | V2 Result |
|--------|-----------|
| Overall alignment win rate | **321/637 = 50.4%** |
| Bullish Alignment | 148/316 = 46.8% |
| Bearish Alignment | 173/321 = 53.9% |

### By Year

| Year | Signals | Wins | Win Rate |
|------|---------|------|----------|
| 2020 | 18 | 10 | 55.6% |
| 2021 | 86 | 54 | 62.8% |
| 2022 | 107 | 56 | 52.3% |
| 2023 | 134 | 66 | 49.3% |
| 2024 | 118 | 50 | 42.4% |
| 2025 | 100 | 52 | 52.0% |
| 2026 | 74 | 33 | 44.6% |

---

## Part 4: Strong Alignment

| Filter | Signals | Wins | Win Rate |
|--------|---------|------|----------|
| Any strong alignment | 414 | 211 | 51.0% |
| Strong Bullish Alignment | 209 | 98 | 46.9% |
| Strong Bearish Alignment | 205 | 113 | 55.1% |
| Both "Strong" views AND aligned | 142 | 83 | 58.5% |

Strong alignment counts are unchanged from V1 (thresholds for Strong/Bullish/Bearish are the same).

---

## Part 5: Day-of-Week

| Day | Signals | Wins | Win Rate |
|-----|---------|------|----------|
| Monday | 135 | 65 | 48.1% |
| Tuesday | 136 | 59 | 43.4% |
| Wednesday | 123 | 66 | 53.7% |
| Thursday | 124 | 64 | 51.6% |
| Friday | 116 | 66 | 56.9% |

All days cluster around 43-57%. No single day has a meaningful edge.

---

## Part 6: VIX Regime

| Regime | Signals | Wins | Win Rate |
|--------|---------|------|----------|
| Low (<15) | 357 | 178 | 49.9% |
| Normal (15-20) | 198 | 93 | 47.0% |
| Elevated (20-30) | 81 | 49 | **60.5%** |
| High (>30) | 1 | 1 | 100.0% |

Elevated VIX (20-30) shows the best win rate at 60.5% — a moderate improvement over V1's 53.1%. Still a small sample relative to Low VIX.

---

## Part 7: Expiry vs Non-Expiry

| Context | Signals | Wins | Win Rate |
|---------|---------|------|----------|
| Expiry | 133 | 72 | 54.1% |
| Non-Expiry | 504 | 249 | 49.4% |

---

## Part 8: VIX Exhaustion

| Pattern | Signals | Wins | Win Rate |
|---------|---------|------|----------|
| Exceeded Half then Reversed | 259 | 223 | **86.1%** |
| Reversed Before Half | 378 | 98 | **25.9%** |

Identical to V1 pattern — VIX exhaustion remains the strongest retrospective indicator regardless of threshold changes.

---

## Part 9: Profitability

| Metric | V2 Value |
|--------|----------|
| Total trades | 637 |
| Avg PnL per trade | +0.0024% |
| Cumulative PnL | **+1.54%** |
| Max win | +2.45% |
| Max loss | -5.10% |
| Annualized Sharpe | **0.06** |

### By Year

| Year | Trades | Avg PnL | Cum PnL |
|------|--------|---------|---------|
| 2020 | 18 | +0.083% | +1.50% |
| 2021 | 86 | +0.191% | +16.39% |
| 2022 | 107 | +0.034% | +3.63% |
| 2023 | 134 | -0.049% | -6.56% |
| 2024 | 118 | -0.086% | -10.13% |
| 2025 | 100 | +0.006% | +0.56% |
| 2026 | 74 | -0.052% | -3.85% |

2021 was the standout year (+16.39%). 2024 was the worst (-10.13%).

---

## Part 10: Move Direction & Streaks

| Direction | Signals | Wins | Win Rate |
|-----------|---------|------|----------|
| Down to Up | 297 | 148 | 49.8% |
| Top to Down | 340 | 173 | 50.9% |

| Streak Metric | Value |
|---------------|-------|
| Longest winning streak | 8 |
| Longest losing streak | 10 |
| Avg winning streak | 2.0 |
| Avg losing streak | 2.0 |

---

## Part 11: Mixed Signals (FII vs PRO Disagree)

| Metric | V2 |
|--------|-----|
| Mixed signal days | 114 |
| FII correct | 50/114 = 43.9% |
| PRO correct | 63/114 = 55.3% |

PRO remains slightly more reliable when they disagree, consistent with V1.

---

## Part 12: Intraday Movement — Wins vs Losses

| Metric | Wins (321) | Losses (316) |
|--------|-----------|-------------|
| Avg intraday high % | 0.403% | 0.420% |
| Avg intraday low % | -0.582% | -0.569% |
| Avg range % | 0.985% | 0.989% |
| Avg open→close % | -0.082% | -0.070% |

Virtually identical — the signal does not predict different intraday profiles.

---

## Part 13: V1 vs V2 Complete Comparison

| Metric | V1 (±30k) | V2 (±25k) | Delta |
|--------|-----------|-----------|-------|
| FII Neutral days | 719 | 639 | -80 |
| FII Mildly Bullish | 109 | 152 | +43 |
| FII Mildly Bearish | 112 | 149 | +37 |
| PRO Neutral days | 418 | 388 | -30 |
| PRO Mildly Bullish | 62 | 77 | +15 |
| PRO Mildly Bearish | 78 | 93 | +15 |
| Bullish Alignment | 288 | 316 | +28 |
| Bearish Alignment | 295 | 321 | +26 |
| Mixed signals | 92 | 114 | +22 |
| Neutral/Unclear | 809 | 733 | -76 |
| **Alignment win rate** | **287/583 (49.2%)** | **321/637 (50.4%)** | **+1.2pp** |
| **Cumulative PnL** | **-3.10%** | **+1.54%** | **+4.64pp** |
| **Sharpe Ratio** | **-0.12** | **0.06** | **+0.18** |
| VIX Exceeded Half win rate | 86.1% | 86.1% | 0.0pp |
| VIX Reversed Before Half win rate | 23.8% | 25.9% | +2.1pp |

---

## Conclusion

### What Improved in V2

1. **More signal days**: 637 vs 583 (+54 days, +9.3%) — narrower Neutral band captures more borderline positioning
2. **Cumulative PnL turned positive**: -3.10% → +1.54% — the 54 new signals were slightly profitable on average
3. **Sharpe turned positive**: -0.12 → 0.06 — marginal improvement but still near zero
4. **Elevated VIX win rate**: 53.1% → 60.5% — the best regime improvement

### What Stayed the Same

1. **Overall win rate still ~50%**: 49.2% → 50.4% — statistically indistinguishable from random
2. **VIX exhaustion unchanged**: 86.1% for Exceeded Half — this is driven by intraday mechanics, not thresholds
3. **Strong alignment unchanged**: 51.0% — only affects Mildly boundary, Strong thresholds didn't change
4. **Streak patterns identical**: Longest win/loss streaks (8/10) consistent with random 50/50 process
5. **Intraday profiles identical**: Wins and losses look the same on average
6. **No year breaks 63%**: Best is still 2021 at 62.8%

### Bottom Line

The V2 threshold change (±25k vs ±30k) is a marginal improvement. It converts 80 FII and 30 PRO Neutral days into Mildly categories, producing 54 additional alignment signals that happen to be slightly net positive. However, the core finding is unchanged: **FII+PRO alignment signals hover around 50% accuracy regardless of threshold choice**, and the signal provides no reliable directional edge for trading.

The only consistently strong pattern remains the **VIX half-range exhaustion** (86.1% when exceeded), which is a retrospective observation independent of threshold tuning.
