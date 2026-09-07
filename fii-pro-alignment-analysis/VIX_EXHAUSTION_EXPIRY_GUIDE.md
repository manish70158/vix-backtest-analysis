# FII-PRO Alignment × VIX Half-Range Exhaustion: Expiry Day Guide

> **Scope**: This guide focuses exclusively on **Nifty expiry days** (weekly/monthly).
> For the full dataset including non-expiry days, see `VIX_EXHAUSTION_COMPLETE_GUIDE.md`.
>
> **Retrospective study**: FII/PRO views are derived from T+1 settlement data,
> so alignment is known only after the trading day. This analysis identifies
> historical patterns, not real-time predictive signals.
>
> **Data**: 119 aligned expiry days from Aug 2020 – Aug 2026 (56 Bullish, 63 Bearish).
> Timing from 5-minute candle data (PostgreSQL `nifty50_5min`).

---

## How It Works (Recap)

1. **FII and PRO align** — both bullish or both bearish (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the market move in the aligned direction past the half threshold?

---

## Master Summary: Expiry Days (119 Aligned Days)

### Bullish Alignment on Expiry (56 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 19 | 33.9% | 18 | **94.7%** | +0.80% |
| Reversed Before Half | 37 | 66.1% | 10 | **27.0%** | -0.34% |

### Bearish Alignment on Expiry (63 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 42 | 66.7% | 34 | **81.0%** | -0.69% |
| Reversed Before Half | 21 | 33.3% | 3 | **14.3%** | +0.41% |

### Expiry vs Non-Expiry Comparison

| Metric | Expiry | Non-Expiry | Delta |
|--------|:------:|:---------:|:-----:|
| **Bullish ExcH Rate** | 33.9% | 29.4% | **+4.5pp** |
| **Bullish ExcH WR%** | **94.7%** | 89.6% | **+5.2pp** |
| **Bearish ExcH Rate** | **66.7%** | 48.7% | **+18.0pp** |
| **Bearish ExcH WR%** | 81.0% | 84.7% | **-3.7pp** |

**Key asymmetries on expiry**:

- **Bearish alignment crosses the threshold much more often on expiry** (+18pp). Expiry-day selling (delta hedging, put unwinding, stop-loss cascades) dramatically amplifies downward moves.
- **Bullish alignment is more durable on expiry** — 94.7% WR vs 89.6%, only 1 failure in 19 exceeded-half days.
- **Bearish WR% is slightly worse on expiry** (-3.7pp) — expiry also triggers short-covering V-recoveries that undermine bearish holds.

---

## Combination Breakdown: Which FII-PRO Combos Work Best on Expiry?

### Bullish Alignment: Exceeded Half on Expiry (19 days)

| Combo (FII + PRO) | N | Won | WR% | Avg Close% |
|--------------------|--:|----:|----:|----------:|
| Bullish + Strong Bullish | 9 | 9 | **100%** | +0.70% |
| Bullish + Mildly Bullish | 2 | 2 | 100% | +1.36% |
| Mildly Bullish + Bullish | 2 | 2 | 100% | +0.42% |
| Mildly Bullish + Mildly Bullish | 1 | 1 | 100% | +1.03% |
| Mildly Bullish + Strong Bullish | 1 | 1 | 100% | +1.38% |
| Strong Bullish + Mildly Bullish | 1 | 1 | 100% | +0.38% |
| Strong Bullish + Strong Bullish | 1 | 1 | 100% | +0.88% |
| Bullish + Bullish | 1 | 1 | 100% | +0.97% |
| Strong Bullish + Bullish | 1 | 0 | **0%** | -0.32% |

**On expiry, bullish exceeded-half is near-automatic** — 18 of 19 worked across every combination. The single failure was "Strong Bullish + Bullish" on 2025-09-02 (close -0.32%). When the bullish half-threshold is crossed on an expiry day, conviction is extremely high.

**Note**: "Bullish + Strong Bullish" dominates with 9 of 19 cases (47%) — this is the most common bullish expiry combination. Despite being the weakest threshold crosser overall (19.1% ExcH rate), when it does cross on expiry, it's 9-for-9.

### Bullish Alignment: Expected Value on Expiry

| Combo (FII + PRO) | Total | ExcH% | WR% | **EV** |
|--------------------|------:|------:|----:|------:|
| Bullish + Mildly Bullish | 2 | 100% | 100% | 100%* |
| Bullish + Strong Bullish | 27 | 33.3% | **100%** | **33.3%** |
| Bullish + Bullish | 4 | 25.0% | 100% | 25.0% |
| Mildly Bullish + Bullish | 8 | 25.0% | 100% | 25.0% |
| Strong Bullish + Strong Bullish | 5 | 20.0% | 100% | 20.0% |
| Mildly Bullish + Strong Bullish | 7 | 14.3% | 100% | 14.3% |

*\* Small sample*

"Bullish + Strong Bullish" has the highest reliable EV at 33.3% — it crosses the threshold on 1 in 3 expiry days, and when it does, it has a perfect record.

### Bearish Alignment: Exceeded Half on Expiry (42 days)

| Combo (FII + PRO) | N | Won | WR% | Avg Close% |
|--------------------|--:|----:|----:|----------:|
| **Strong Bearish + Strong Bearish** | **7** | **7** | **100%** | **-0.60%** |
| **Mildly Bearish + Bearish** | **4** | **4** | **100%** | **-0.44%** |
| Strong Bearish + Mildly Bearish | 1 | 1 | 100% | -0.96% |
| Bearish + Strong Bearish | 11 | 9 | **81.8%** | -0.46% |
| Strong Bearish + Bearish | 4 | 3 | 75.0% | -0.27% |
| Bearish + Mildly Bearish | 3 | 2 | 66.7% | -0.22% |
| Mildly Bearish + Strong Bearish | 9 | 6 | **66.7%** | -0.52% |
| Bearish + Bearish | 2 | 2 | 100% | -0.47% |
| Mildly Bearish + Mildly Bearish | 1 | 0 | 0% | +0.09% |

**On expiry, bearish combination choice matters more**:

1. **"Strong Bearish + Strong Bearish" is 7-for-7 (100%)** — the gold standard. Maximum conviction + expiry selling = durable downside.

2. **"Mildly Bearish + Bearish" is 4-for-4 (100%)** — balanced moderate conviction holds well on expiry.

3. **"Mildly Bearish + Strong Bearish" drops to 66.7%** — 3 of 9 failed. On expiry, when FII is only mildly bearish but PRO is strong, the PRO-heavy selling gets absorbed by expiry-related flows.

4. **"Mildly Bearish + Mildly Bearish" is the only 0% WR** — weak conviction bearish fails on expiry just as it does on non-expiry days.

### Bearish Alignment: Expected Value on Expiry

| Combo (FII + PRO) | Total | ExcH% | WR% | **EV** |
|--------------------|------:|------:|----:|------:|
| **Strong Bearish + Strong Bearish** | **9** | **77.8%** | **100%** | **77.8%** |
| Strong Bearish + Bearish | 4 | 100% | 75.0% | 75.0% |
| Mildly Bearish + Bearish | 6 | 66.7% | 100% | **66.7%** |
| Bearish + Strong Bearish | 18 | 61.1% | 81.8% | 50.0% |
| Bearish + Bearish | 2 | 100% | 100% | 100%* |
| Bearish + Mildly Bearish | 3 | 100% | 66.7% | 66.7%* |
| Mildly Bearish + Strong Bearish | 18 | 50.0% | 66.7% | 33.3% |
| Mildly Bearish + Mildly Bearish | 2 | 50.0% | 0% | 0% |

*\* Small sample*

**"Strong Bearish + Strong Bearish" on expiry is the highest-conviction setup in the entire dataset** — 77.8% EV (crosses 78% of the time AND holds 100% when it does). Compare this to its non-expiry EV of ~52%.

---

## Conviction Score Analysis on Expiry

Assigning: Strong=3, Regular=2, Mildly=1. Combined score = FII + PRO (range: 2-6).

### Bullish Alignment on Expiry

| Score | Total | Exceeded | ExcH% | WR% | EV |
|:-----:|------:|---------:|------:|----:|---:|
| 6 (max) | 5 | 1 | 20.0% | 100% | 20.0% |
| 5 | 28 | 10 | **35.7%** | 90.0% | 32.1% |
| 4 | 12 | 3 | 25.0% | 100% | 25.0% |
| 3 | 10 | 4 | **40.0%** | 100% | **40.0%** |
| 2 (min) | 1 | 1 | 100%* | 100%* | 100%* |

**On bullish expiry, moderate conviction (Score 3-4) outperforms maximum conviction (Score 6)**. Score 3 has the highest EV at 40% — when both participants are only moderately bullish on expiry, the threshold is easier to cross (wider VIX = lower threshold relative to available move) and holds well.

### Bearish Alignment on Expiry

| Score | Total | Exceeded | ExcH% | WR% | EV |
|:-----:|------:|---------:|------:|----:|---:|
| 6 (max) | 9 | 7 | **77.8%** | **100%** | **77.8%** |
| 5 | 22 | 15 | **68.2%** | 80.0% | 54.5% |
| 4 | 21 | 12 | 57.1% | 75.0% | 42.9% |
| 3 | 9 | 7 | **77.8%** | 85.7% | **66.7%** |
| 2 (min) | 2 | 1 | 50.0% | 0% | 0% |

**Bearish expiry is nearly monotonic with conviction**: Score 6 leads at 77.8% EV, followed by Score 3 (66.7%), Score 5 (54.5%), Score 4 (42.9%). The Score 3 anomaly is driven by "Mildly Bearish + Bearish" which is 4-for-4 when exceeded on expiry.

---

## Threshold Crossing Timing on Expiry

### Bullish Exceeded Half: Timing (19 days)

| Statistic | Value |
|-----------|:-----:|
| Median | **11:35 AM** (140 min) |
| Mean | 11:32 AM (137 min) |
| 25th pctl | 10:13 AM (62 min) |
| 75th pctl | 12:40 PM (205 min) |

### Bearish Exceeded Half: Timing (42 days)

| Statistic | Value |
|-----------|:-----:|
| Median | **10:45 AM** (90 min) |
| Mean | 11:26 AM (131 min) |
| 25th pctl | 9:46 AM (31 min) |
| 75th pctl | 13:11 PM (236 min) |

**Bearish crosses 50 minutes faster on expiry** (median 90 min vs 140 min) — but this is actually *slower* than the non-expiry bearish median of ~70 min. Expiry mechanics (delta hedging, institutional positioning) create more complex price action before the definitive move.

### Session Distribution on Expiry

#### Bullish Exceeded Half: By Session

| Session | N | % | WR% | Avg Close% |
|---------|--:|--:|----:|----------:|
| Opening (9:15-9:44) | 3 | 15.8% | **100%** | +0.84% |
| Early Morning (9:45-10:29) | 4 | 21.1% | 75.0% | +0.62% |
| Late Morning (10:30-11:29) | 2 | 10.5% | **100%** | +1.25% |
| Midday (11:30-12:29) | 5 | 26.3% | **100%** | +0.58% |
| Early Afternoon (12:30-13:29) | 2 | 10.5% | **100%** | +1.04% |
| Late Afternoon (13:30-14:29) | 3 | 15.8% | **100%** | +0.56% |

**Bullish expiry is remarkably uniform**: Every session except Early AM has 100% WR. The single Early AM failure was "Strong Bullish + Bullish" on 2025-09-02. Bullish crosses on expiry hold regardless of when they occur.

#### Bearish Exceeded Half: By Session

| Session | N | % | WR% | Avg Close% |
|---------|--:|--:|----:|----------:|
| Opening (9:15-9:44) | 9 | 21.4% | **100%** | -0.95% |
| Early Morning (9:45-10:29) | 11 | 26.2% | **63.6%** | -0.19% |
| **Late Morning (10:30-11:29)** | **7** | **16.7%** | **57.1%** | **-0.11%** |
| Midday (11:30-12:29) | 2 | 4.8% | **100%** | -0.65% |
| Early Afternoon (12:30-13:29) | 4 | 9.5% | 75.0% | -0.32% |
| Late Afternoon (13:30-14:29) | 1 | 2.4% | **100%** | -2.00% |
| Closing (14:30-15:30) | 8 | 19.0% | **100%** | -0.40% |

**Bearish expiry has TWO danger zones**:

1. **Early Morning (9:45-10:29)** — 63.6% WR (4 of 11 failed). This is *worse* on expiry than non-expiry (non-expiry Early AM = ~85% WR). Expiry-morning panic dips get bought aggressively.

2. **Late Morning (10:30-11:29)** — 57.1% WR (3 of 7 failed). Consistent with the full-dataset danger zone. Expiry amplifies this weakness further.

**Opening crosses are perfect (9/9 = 100%)** — when bearish alignment breaks through at the open on expiry, it never recovers. Closing crosses are also perfect (8/8 = 100%).

---

## Bearish Late Morning on Expiry: Deep Dive (7 days)

The 7 bearish late-morning crosses on expiry had a 57.1% WR — the worst session-expiry combination in the dataset.

### All 7 Cases

| Date | FII View | PRO View | VIX | Cross | Low% | Close% | Held? |
|------|----------|----------|----:|:-----:|-----:|-------:|:-----:|
| 2021-04-01 | Strong Bearish | Bearish | 20.6 | 10:55 | -0.71% | +0.46% | ✗ |
| 2022-01-20 | Mildly Bearish | Strong Bearish | 17.8 | 10:45 | -1.52% | -0.77% | ✓ |
| 2022-04-28 | Mildly Bearish | Strong Bearish | 20.6 | 10:45 | -0.69% | +0.24% | ✗ |
| 2024-09-12 | Mildly Bearish | Strong Bearish | 13.6 | 11:25 | -0.47% | +1.02% | ✗ |
| 2025-01-09 | Bearish | Bearish | 14.5 | 10:45 | -0.73% | -0.50% | ✓ |
| 2026-05-12 | Bearish | Mildly Bearish | 18.6 | 11:05 | -1.58% | -1.23% | ✓ |
| 2026-06-09 | Mildly Bearish | Bearish | 17.0 | 10:45 | -0.66% | -0.01% | ✓ |

### Failure Pattern

All 3 failures share characteristics:
- **"Mildly Bearish + Strong Bearish"** appears in 2 of 3 failures — the PRO-heavy combo that exhausts selling momentum
- **Shallow crosses**: Failures averaged only -0.62% intraday low vs winners at -1.12%
- All 3 failures reversed to close bullish (V-recovery)

The 4 winners either had balanced conviction ("Bearish + Bearish"), FII-led conviction, or very deep moves (low% > -1.5%).

---

## Bearish Early Morning on Expiry: Emerging Danger (11 days)

Early Morning (9:45-10:29) is surprisingly weak on expiry at 63.6% WR — normally this session runs ~80% on non-expiry days.

### All 11 Cases

| Date | FII View | PRO View | VIX | Cross | Low% | Close% | Held? |
|------|----------|----------|----:|:-----:|-----:|-------:|:-----:|
| 2020-11-26 | Bearish | Strong Bearish | 23.1 | 10:00 | -0.90% | +0.84% | ✗ |
| 2021-11-11 | Mildly Bearish | Bearish | 16.3 | 10:15 | -0.93% | -0.46% | ✓ |
| 2022-05-26 | Mildly Bearish | Strong Bearish | 25.3 | 10:25 | -1.25% | +0.60% | ✗ |
| 2023-01-05 | Strong Bearish | Strong Bearish | 15.2 | 10:05 | -1.16% | -0.56% | ✓ |
| 2024-01-18 | Bearish | Strong Bearish | 15.1 | 09:50 | -0.60% | +0.29% | ✗ |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | 15.4 | 09:55 | -0.51% | +0.09% | ✗ |
| 2024-07-11 | Bearish | Strong Bearish | 14.4 | 10:10 | -0.83% | -0.24% | ✓ |
| 2024-10-17 | Strong Bearish | Strong Bearish | 13.1 | 09:25 | -1.19% | -1.11% | ✓ |
| 2025-09-23 | Bearish | Mildly Bearish | 10.6 | 09:45 | -0.49% | -0.09% | ✓ |
| 2025-10-14 | Bearish | Strong Bearish | 11.0 | 10:00 | -0.86% | -0.61% | ✓ |
| 2026-02-24 | Mildly Bearish | Strong Bearish | 14.2 | 09:30 | -1.23% | -0.71% | ✓ |

### Failure Pattern

| Metric | Winners (7) | Failures (4) |
|--------|:---:|:---:|
| Avg VIX | 13.5 | 19.7 |
| Avg intraday low% | -0.96% | -0.82% |
| Elevated VIX (20+) present | 0 | 2 |

Same pattern as the overall late-morning danger: **elevated VIX on expiry is a trap**. Both elevated-VIX cases reversed. Lower VIX combined with meaningful depth held.

---

## Bearish Exceeded Half: All 8 Failures on Expiry

Every failure reversed from "Down to Up" — a V-shaped recovery.

| Date | FII View | PRO View | VIX | Cross | Low% | Close% |
|------|----------|----------|----:|:-----:|-----:|-------:|
| 2020-11-26 | Bearish | Strong Bearish | 23.1 | 10:00 | -0.90% | **+0.84%** |
| 2021-04-01 | Strong Bearish | Bearish | 20.6 | 10:55 | -0.71% | **+0.46%** |
| 2022-04-28 | Mildly Bearish | Strong Bearish | 20.6 | 10:45 | -0.69% | **+0.24%** |
| 2022-05-26 | Mildly Bearish | Strong Bearish | 25.3 | 10:25 | -1.25% | **+0.60%** |
| 2024-01-18 | Bearish | Strong Bearish | 15.1 | 09:50 | -0.60% | **+0.29%** |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | 15.4 | 09:55 | -0.51% | **+0.09%** |
| 2024-09-12 | Mildly Bearish | Strong Bearish | 13.6 | 11:25 | -0.47% | **+1.02%** |
| 2025-08-07 | Bearish | Mildly Bearish | 12.0 | 13:20 | -0.49% | **+0.66%** |

### Failure Fingerprints

- **6 of 8 crossed before 11:00 AM** — front-loaded panic that gets bought
- **5 of 8 had PRO "Strong Bearish" or "Mildly Bearish"** but not matching FII conviction — asymmetric combos
- **4 of 8 had VIX ≥ 20** — elevated VIX is overrepresented in failures (50% of failures vs 19% of all bearish expiry crosses)
- **Average close: +0.40%** — the reversal is meaningful, not marginal
- **"Mildly Bearish + Strong Bearish" accounts for 3 of 8 failures** — the single most dangerous combo on expiry
- **Zero failures had "Strong Bearish + Strong Bearish"** — maximum conviction never fails on expiry

### What the Failures Tell You

```
BEARISH EXPIRY FAILURE PROFILE:
  → PRO-heavy selling (FII weaker than PRO) + expiry = selling exhaustion + short-covering
  → Elevated VIX (20+) on expiry = wider threshold barely crossed + V-recovery
  → Crosses before 11:00 AM on expiry = morning panic absorbed by institutional buying
  → Shallow crosses (low% barely past threshold) = insufficient momentum
```

---

## Bullish Exceeded Half: The Sole Failure on Expiry

Only 1 of 19 bullish exceeded-half expiry days failed:

```
Date: 2025-09-02
  FII: Strong Bullish    PRO: Bullish    → Bullish Alignment
  VIX: 11.3              Predicted Range: 0.71%
  Half Threshold: 0.355%

  Cross time: 10:00 AM (45 min)
  Intraday High: +0.42%  (barely exceeded 0.355%)
  Close: -0.32%

  → Shallow cross, early morning, VIX at 11 = low conviction.
    The rally barely crossed the threshold and faded by close.
```

This makes bullish exceeded-half on expiry nearly automatic — 94.7% WR. The one failure was a marginal cross with a "Top to Down" reversal.

---

## Reversed Before Half on Expiry

### Bullish Reversed Before Half (37 days, 27.0% worked)

When the bullish move doesn't reach the half threshold on expiry, 73% close bearish (same as non-expiry).

| Combo (FII + PRO) | N | Worked | WR% | Avg Close% |
|--------------------|--:|-------:|----:|----------:|
| Bullish + Strong Bullish | 18 | 4 | 22.2% | -0.38% |
| Mildly Bullish + Bullish | 6 | 1 | 16.7% | -0.45% |
| Mildly Bullish + Strong Bullish | 6 | 1 | 16.7% | -0.42% |
| Strong Bullish + Strong Bullish | 4 | 2 | 50.0% | -0.06% |
| Bullish + Bullish | 3 | 2 | 66.7% | -0.13% |

"Bullish + Strong Bullish" dominates this quadrant (18 of 37) with only 22.2% working — when the most common bullish combo fails to cross on expiry, the day is likely bearish.

### Bearish Reversed Before Half (21 days, 14.3% worked)

When the bearish move doesn't reach the half threshold on expiry, **85.7% close bullish** — even higher than the non-expiry rate of 81.4%.

| Combo (FII + PRO) | N | Worked | WR% | Avg Close% |
|--------------------|--:|-------:|----:|----------:|
| Mildly Bearish + Strong Bearish | 9 | 1 | 11.1% | +0.46% |
| Bearish + Strong Bearish | 7 | 1 | 14.3% | +0.36% |
| Mildly Bearish + Bearish | 2 | 0 | 0% | +0.55% |
| Strong Bearish + Strong Bearish | 2 | 1 | 50.0% | +0.31% |

**On expiry, if the bearish move fails to cross the half threshold, go long with confidence.** The short-covering dynamics on expiry make this reversal even more powerful than non-expiry days.

---

## VIX Regime Analysis on Expiry

### Bullish Exceeded Half: By VIX Regime

| VIX Regime | N | Won | WR% | Avg Close% |
|------------|--:|----:|----:|----------:|
| Low (<15) | 10 | 9 | 90.0% | +0.64% |
| Normal (15-20) | 7 | 7 | **100%** | +0.82% |
| Elevated (20-30) | 2 | 2 | **100%** | +1.03% |

Bullish crosses on expiry work across all VIX regimes. Higher VIX = larger average close.

### Bearish Exceeded Half: By VIX Regime

| VIX Regime | N | Won | WR% | Avg Close% |
|------------|--:|----:|----:|----------:|
| Low (<15) | 19 | 17 | **89.5%** | -0.43% |
| Normal (15-20) | 15 | 13 | **86.7%** | -0.59% |
| **Elevated (20-30)** | **8** | **4** | **50.0%** | **-0.28%** |

**Elevated VIX (20+) on bearish expiry is a coin flip** — 50% WR (4 of 8). This is the single worst filter in the dataset. High VIX means the threshold is wider in absolute terms, the cross is marginal, and expiry short-covering + bargain hunting creates powerful V-recoveries.

**Low and Normal VIX both work well** at 87-90% WR.

---

## Year-by-Year Performance on Expiry

### Bullish Exceeded Half

| Year | N | WR% | Avg Close% |
|------|--:|----:|----------:|
| 2021 | 2 | 100% | +0.89% |
| 2022 | 2 | 100% | +0.72% |
| 2023 | 3 | 100% | +0.59% |
| 2024 | 2 | 100% | +1.29% |
| 2025 | 8 | 87.5% | +0.66% |
| 2026 | 2 | 100% | +0.64% |

100% WR every year except 2025 (1 failure in 8). Remarkably consistent.

### Bearish Exceeded Half

| Year | N | WR% | Avg Close% |
|------|--:|----:|----------:|
| 2020 | 1 | 0%* | +0.84% |
| 2021 | 5 | 80% | -0.84% |
| 2022 | 9 | 77.8% | -0.67% |
| 2023 | 8 | **100%** | -0.51% |
| 2024 | 8 | 62.5% | -0.24% |
| 2025 | 8 | 87.5% | -0.25% |
| 2026 | 3 | **100%** | -0.65% |

2024 was the weakest bearish expiry year at 62.5% — 3 of 8 failed. 2023 and 2026 were perfect.

---

## All Bullish Exceeded Half on Expiry (19 Days Reference)

| Date | FII View | PRO View | VIX | Cross | High% | Close% | Held? |
|------|----------|----------|----:|:-----:|------:|-------:|:-----:|
| 2021-09-16 | Bullish | Strong Bullish | 13.7 | 14:15 | +0.60% | +0.50% | ✓ |
| 2021-12-02 | Bullish | Strong Bullish | 19.4 | 10:15 | +1.36% | +1.27% | ✓ |
| 2022-03-17 | Bullish | Strong Bullish | 24.1 | 14:05 | +0.82% | +0.56% | ✓ |
| 2022-07-28 | Strong Bullish | Strong Bullish | 18.1 | 11:05 | +1.01% | +0.88% | ✓ |
| 2023-04-27 | Bullish | Strong Bullish | 11.7 | 13:30 | +0.66% | +0.62% | ✓ |
| 2023-06-28 | Bullish | Strong Bullish | 10.8 | 12:00 | +0.54% | +0.44% | ✓ |
| 2023-07-20 | Bullish | Strong Bullish | 11.6 | 13:15 | +0.81% | +0.70% | ✓ |
| 2024-04-25 | Bullish | Mildly Bullish | 10.3 | 09:35 | +1.38% | +1.09% | ✓ |
| 2024-05-23 | Bullish | Strong Bullish | 21.5 | 11:55 | +1.68% | +1.49% | ✓ |
| 2025-01-02 | Bullish | Mildly Bullish | 14.5 | 10:35 | +1.87% | +1.62% | ✓ |
| 2025-01-23 | Strong Bullish | Mildly Bullish | 16.8 | 12:15 | +0.62% | +0.38% | ✓ |
| 2025-01-30 | Mildly Bullish | Bullish | 18.6 | 10:20 | +0.66% | +0.55% | ✓ |
| 2025-04-03 | Bullish | Strong Bullish | 13.7 | 09:20 | +0.67% | +0.39% | ✓ |
| 2025-05-15 | Mildly Bullish | Strong Bullish | 17.2 | 13:05 | +1.71% | +1.38% | ✓ |
| 2025-06-05 | Mildly Bullish | Bullish | 15.8 | 12:05 | +0.85% | +0.28% | ✓ |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | 13.0 | 09:30 | +1.17% | +1.03% | ✓ |
| 2025-09-02 | Strong Bullish | Bullish | 11.3 | 10:00 | +0.42% | -0.32% | ✗ |
| 2026-02-17 | Bullish | Strong Bullish | 13.3 | 11:35 | +0.49% | +0.30% | ✓ |
| 2026-04-13 | Bullish | Bullish | 18.9 | 10:25 | +1.35% | +0.97% | ✓ |

---

## All Bearish Exceeded Half on Expiry (42 Days Reference)

| Date | FII View | PRO View | VIX | Cross | Low% | Close% | Held? |
|------|----------|----------|----:|:-----:|-----:|-------:|:-----:|
| 2020-11-26 | Bearish | Strong Bearish | 23.1 | 10:00 | -0.90% | +0.84% | ✗ |
| 2021-03-25 | Mildly Bearish | Strong Bearish | 22.5 | 09:20 | -2.10% | -1.54% | ✓ |
| 2021-04-01 | Strong Bearish | Bearish | 20.6 | 10:55 | -0.71% | +0.46% | ✗ |
| 2021-10-21 | Mildly Bearish | Bearish | 18.3 | 09:30 | -1.82% | -0.89% | ✓ |
| 2021-10-28 | Bearish | Strong Bearish | 16.8 | 09:35 | -2.13% | -1.79% | ✓ |
| 2021-11-11 | Mildly Bearish | Bearish | 16.3 | 10:15 | -0.93% | -0.46% | ✓ |
| 2022-01-20 | Mildly Bearish | Strong Bearish | 17.8 | 10:45 | -1.52% | -0.77% | ✓ |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 24.5 | 13:40 | -2.08% | -2.00% | ✓ |
| 2022-04-28 | Mildly Bearish | Strong Bearish | 20.6 | 10:45 | -0.69% | +0.24% | ✗ |
| 2022-05-19 | Bearish | Strong Bearish | 22.3 | 14:30 | -0.89% | -0.56% | ✓ |
| 2022-05-26 | Mildly Bearish | Strong Bearish | 25.3 | 10:25 | -1.25% | +0.60% | ✗ |
| 2022-07-14 | Bearish | Bearish | 18.5 | 13:20 | -1.00% | -0.44% | ✓ |
| 2022-09-15 | Strong Bearish | Mildly Bearish | 18.3 | 10:10 | -1.02% | -0.96% | ✓ |
| 2022-12-15 | Bearish | Strong Bearish | 12.9 | 12:30 | -1.21% | -1.15% | ✓ |
| 2022-12-22 | Bearish | Strong Bearish | 15.6 | 09:25 | -1.20% | -0.95% | ✓ |
| 2023-01-05 | Strong Bearish | Strong Bearish | 15.2 | 10:05 | -1.16% | -0.56% | ✓ |
| 2023-01-25 | Mildly Bearish | Strong Bearish | 13.7 | 09:45 | -1.36% | -1.01% | ✓ |
| 2023-02-23 | Strong Bearish | Strong Bearish | 15.6 | 09:30 | -0.67% | -0.29% | ✓ |
| 2023-05-18 | Strong Bearish | Bearish | 13.1 | 12:15 | -1.00% | -0.84% | ✓ |
| 2023-06-01 | Strong Bearish | Strong Bearish | 12.0 | 14:45 | -0.61% | -0.50% | ✓ |
| 2023-07-13 | Bearish | Strong Bearish | 10.9 | 14:40 | -0.56% | -0.27% | ✓ |
| 2023-08-03 | Bearish | Strong Bearish | 11.3 | 12:45 | -0.85% | -0.36% | ✓ |
| 2023-11-09 | Bearish | Strong Bearish | 11.0 | 14:40 | -0.41% | -0.27% | ✓ |
| 2024-01-18 | Bearish | Strong Bearish | 15.1 | 09:50 | -0.60% | +0.29% | ✗ |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | 15.4 | 09:55 | -0.51% | +0.09% | ✗ |
| 2024-05-30 | Strong Bearish | Bearish | 24.2 | 14:55 | -0.89% | -0.27% | ✓ |
| 2024-07-11 | Bearish | Strong Bearish | 14.4 | 10:10 | -0.83% | -0.24% | ✓ |
| 2024-09-12 | Mildly Bearish | Strong Bearish | 13.6 | 11:25 | -0.47% | +1.02% | ✗ |
| 2024-10-17 | Strong Bearish | Strong Bearish | 13.1 | 09:25 | -1.19% | -1.11% | ✓ |
| 2024-10-31 | Strong Bearish | Strong Bearish | 15.5 | 12:15 | -0.73% | -0.46% | ✓ |
| 2024-11-07 | Strong Bearish | Strong Bearish | 14.9 | 09:25 | -1.27% | -1.20% | ✓ |
| 2025-01-09 | Bearish | Bearish | 14.5 | 10:45 | -0.73% | -0.50% | ✓ |
| 2025-04-30 | Mildly Bearish | Bearish | 17.4 | 15:25 | -0.59% | -0.39% | ✓ |
| 2025-07-03 | Strong Bearish | Bearish | 12.4 | 14:35 | -0.47% | -0.42% | ✓ |
| 2025-08-07 | Bearish | Mildly Bearish | 12.0 | 13:20 | -0.49% | +0.66% | ✗ |
| 2025-09-23 | Bearish | Mildly Bearish | 10.6 | 09:45 | -0.49% | -0.09% | ✓ |
| 2025-10-14 | Bearish | Strong Bearish | 11.0 | 10:00 | -0.86% | -0.61% | ✓ |
| 2025-11-25 | Mildly Bearish | Strong Bearish | 13.2 | 15:00 | -0.54% | -0.53% | ✓ |
| 2025-12-09 | Strong Bearish | Strong Bearish | 11.1 | 09:30 | -0.54% | -0.10% | ✓ |
| 2026-02-24 | Mildly Bearish | Strong Bearish | 14.2 | 09:30 | -1.23% | -0.71% | ✓ |
| 2026-05-12 | Bearish | Mildly Bearish | 18.6 | 11:05 | -1.58% | -1.23% | ✓ |
| 2026-06-09 | Mildly Bearish | Bearish | 17.0 | 10:45 | -0.66% | -0.01% | ✓ |

---

# Quick Reference: Expiry Day Decision Rules

```
┌──────────────────────────────────────────────────────────────────────┐
│            FII + PRO ALIGNED + VIX HALF-THRESHOLD: EXPIRY DAYS       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  BULLISH ALIGNMENT ON EXPIRY (56 days)                               │
│  ├─ Exceeded Half → 94.7% close bullish (18/19)                     │
│  │   Near-automatic. Only 1 failure in entire dataset.               │
│  │   Every combo works. Every session works (except 1 Early AM).     │
│  │   Avg close: +0.80%                                               │
│  │                                                                   │
│  └─ Reversed Before Half → 73% close BEARISH (same as non-expiry)   │
│      Most common failure combo: Bullish + Strong Bullish (22% WR)    │
│                                                                      │
│  BEARISH ALIGNMENT ON EXPIRY (63 days)                               │
│  ├─ Exceeded Half → 81.0% close bearish (34/42)                     │
│  │   ExcH rate jumps to 66.7% on expiry (+18pp vs non-expiry)       │
│  │   Avg close: -0.69%                                               │
│  │                                                                   │
│  │   BEST COMBOS (expiry):                                           │
│  │     Strong Bear + Strong Bear   7/7 = 100% WR, 77.8% EV         │
│  │     Mildly Bear + Bearish       4/4 = 100% WR, 66.7% EV         │
│  │                                                                   │
│  │   DANGER COMBOS (expiry):                                         │
│  │     Mildly Bear + Strong Bear   6/9 =  67% WR (3 failures)       │
│  │     Mildly Bear + Mildly Bear   0/1 =   0% WR                    │
│  │                                                                   │
│  │   DANGER SESSIONS (expiry):                                       │
│  │     Early AM (9:45-10:29)       7/11 = 64% WR                    │
│  │     Late AM  (10:30-11:29)      4/7  = 57% WR                    │
│  │                                                                   │
│  │   SAFE SESSIONS (expiry):                                         │
│  │     Opening  (9:15-9:44)        9/9  = 100% WR                   │
│  │     Closing  (14:30-15:30)      8/8  = 100% WR                   │
│  │     Midday   (11:30-12:29)      2/2  = 100% WR                   │
│  │                                                                   │
│  │   VIX REGIME (expiry):                                            │
│  │     Low (<15)       89.5% WR  ← safest                           │
│  │     Normal (15-20)  86.7% WR  ← reliable                         │
│  │     Elevated (20+)  50.0% WR  ← AVOID (coin flip)                │
│  │                                                                   │
│  └─ Reversed Before Half → 85.7% close BULLISH                      │
│      Short-covering on expiry makes reversal even stronger           │
│      "Mildly Bear + Strong Bear" fails 89% when threshold missed    │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  EXPIRY-SPECIFIC EDGE vs NON-EXPIRY                                  │
│  • Bearish exceeds threshold +18pp more often (66.7% vs 48.7%)      │
│  • Bullish WR% higher on expiry (+5.2pp: 94.7% vs 89.6%)           │
│  • Bearish WR% slightly lower on expiry (-3.7pp: 81.0% vs 84.7%)   │
│  • "Rev Before Half + Bearish expiry" reverses bullish 85.7%        │
│  • Elevated VIX bearish drops to 50% WR on expiry (AVOID)           │
│                                                                      │
│  HIGHEST EV SETUPS ON EXPIRY:                                        │
│  1. Bear: Strong Bear + Strong Bear  EV=77.8% (best in dataset)     │
│  2. Bear: Mildly Bear + Bearish      EV=66.7%                       │
│  3. Bear: Bearish + Strong Bear      EV=50.0%                       │
│  4. Bull: Bullish + Strong Bullish   EV=33.3% (100% WR when exc)   │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  CAVEAT: FII/PRO alignment is known only after T+1 settlement.      │
│  The VIX half-threshold IS observable intraday, but the              │
│  alignment condition is not.                                         │
└──────────────────────────────────────────────────────────────────────┘
```
