# FII-PRO Alignment × VIX Half-Range Exhaustion: Complete Guide

> **Retrospective study**: FII/PRO views are derived from T+1 settlement data,
> so alignment is known only after the trading day. This analysis identifies
> historical patterns, not real-time predictive signals.
>
> **Timing data**: Uses 5-minute candle data from PostgreSQL (`nifty50_5min`,
> Aug 2020 – Aug 2026) to determine the exact candle where the VIX half-threshold
> was first crossed.

---

## How It Works

1. **FII and PRO align** — both bullish or both bearish (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the market move in the aligned direction past the half threshold?

```
BULLISH ALIGNMENT:
  VIX Predicted = 0.86%  →  Half Threshold = 0.43%
  Intraday High% = 0.60%  →  Exceeded 0.43% ✓  ("Exceeded Half")
  Intraday High% = 0.15%  →  Did NOT reach     ("Reversed Before Half")

BEARISH ALIGNMENT:
  VIX Predicted = 0.86%  →  Half Threshold = 0.43%
  Intraday Low% = -0.60%  →  Exceeded 0.43% ✓  ("Exceeded Half")
  Intraday Low% = -0.14%  →  Did NOT reach     ("Reversed Before Half")
```

---

## Master Summary (578 Aligned Days with VIX Data)

### Bullish Alignment (285 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 85 | 29.8% | 77 | **90.6%** | +0.59% |
| Reversed Before Half | 200 | 70.2% | 54 | **27.0%** | -0.36% |

### Bearish Alignment (293 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 153 | 52.2% | 129 | **84.3%** | -0.45% |
| Reversed Before Half | 140 | 47.8% | 26 | **18.6%** | +0.36% |

### Bullish vs Bearish Comparison

| Metric | Bullish | Bearish |
|--------|:-------:|:-------:|
| Exceeded Half frequency | 29.8% | **52.2%** |
| Exceeded Half WR% | **90.6%** | 84.3% |
| Failure cases | 8 (9.4%) | 24 (15.7%) |
| Exceeded Half: median cross time | 11:37 AM | **10:25 AM** |
| Exceeded Half: % crossed by 10:30 AM | 34% | **52%** |
| Reversed Before Half WR% | 27.0% | 18.6% |
| Rev Before Half: median peak time | 9:52 AM | **9:37 AM** |
| Rev Before Half: median reversal time | 9:30 AM | 9:50 AM |
| Rev Before Half: % threshold reached | 42% | 49% |
| Rev Before Half: peak by 10:15 → loss rate | **92%** | 89% |
| Expiry boost on WR% | Yes (+5.3%) | No (-4.6%) |

**Notable asymmetry**: Bearish alignment crosses the threshold 52% of the time vs 30% for bullish — selloffs are sharper and more momentum-driven. But bullish has higher WR% (91% vs 84%) because rallies that cross are more durable while bearish crosses are prone to V-shaped recoveries.

---

## Threshold Crossing Timing (5-Minute Candle Analysis)

### Side-by-Side Timing

| Statistic | Bullish (86 days) | Bearish (153 days) |
|-----------|:-----------------:|:------------------:|
| Median | **11:37 AM** (142 min) | **10:25 AM** (70 min) |
| Average | 11:46 AM (152 min) | 11:12 AM (117 min) |
| 25th pctl | 10:03 AM | 9:40 AM |
| 75th pctl | 1:08 PM | 12:35 PM |
| Earliest | 9:15 AM (gap open) | 9:15 AM (gap open) |
| Latest | 3:25 PM | 3:25 PM |

**Bearish crosses 72 minutes faster** — panic selling is immediate; buying conviction builds gradually.

### Session Distribution

| Session | Bullish Count | Bullish % | Bullish WR% | Bearish Count | Bearish % | Bearish WR% |
|---------|------:|--:|----:|------:|--:|----:|
| Opening (9:15-9:44) | 17 | 19.8% | 94.1% | 44 | 28.8% | 81.8% |
| Early Morning (9:45-10:29) | 12 | 14.0% | 83.3% | 35 | 22.9% | 80.0% |
| Late Morning (10:30-11:29) | 13 | 15.1% | 92.3% | 21 | 13.7% | **61.9%** |
| Midday (11:30-12:29) | 15 | 17.4% | 86.7% | 11 | 7.2% | 90.9% |
| Early Afternoon (12:30-13:29) | 10 | 11.6% | 100.0% | 15 | 9.8% | 93.3% |
| Late Afternoon (13:30-14:29) | 10 | 11.6% | 80.0% | 10 | 6.5% | 100.0% |
| Closing (14:30-15:30) | 9 | 10.5% | 100.0% | 17 | 11.1% | 100.0% |

**Key patterns**:
- Bullish is evenly spread across the day; bearish is front-loaded (52% by 10:30)
- Afternoon crosses (12:30+) → near-perfect WR% for both directions
- **Bearish danger zone**: Late morning (10:30-11:30) → only 62% WR (V-shaped recovery window)
- Bullish opening crosses → 94% WR (gap-up days that hold)

### VIX Regime Timing

| VIX Regime | Bullish Median | Bearish Median |
|------------|:--------------:|:--------------:|
| Low (<15) | 11:45 AM | 10:40 AM |
| Normal (15-20) | 11:02 AM | 10:02 AM |
| Elevated (20-30) | 12:35 PM | 10:20 AM |

Higher VIX = wider threshold in absolute terms. Normal VIX crosses fastest for bearish (moderate threshold + sharp selling).

---

## "Reversed Before Half" Timing: When Does the Aligned Move Peak and Fail?

On days where the threshold was **never** crossed, when did the market reach its deepest point in the aligned direction before reversing? This tells you **by what time the aligned view has failed**.

### When Does the Aligned Move Peak? (Deepest Point Timing)

| Statistic | Bullish (199 days) | Bearish (139 days) |
|-----------|:------------------:|:------------------:|
| Median | **9:52 AM** (38 min) | **9:37 AM** (22 min) |
| Average | 11:08 AM (114 min) | 10:40 AM (86 min) |
| 25th pctl | 9:15 AM (opening) | 9:15 AM (opening) |
| 75th pctl | 1:18 PM | 11:17 AM |

**On most "Reversed Before Half" days, the aligned move peaked within the first 30-40 minutes.** The market never builds meaningful momentum in the aligned direction — the failure is apparent very early.

### How Close Did They Get to the Threshold?

| Depth | Bullish (199 days) | Bearish (139 days) |
|-------|:------------------:|:------------------:|
| Average % of threshold reached | 41.9% | 48.9% |
| Median % of threshold reached | 40.9% | 51.6% |
| < 25% of threshold (no momentum) | 75 (37.7%) | 27 (19.4%) |
| 25-50% | 44 (22.1%) | 38 (27.3%) |
| 50-75% | 40 (20.1%) | 50 (36.0%) |
| 75-100% (near miss) | 39 (19.6%) | 23 (16.5%) |

Bullish "Reversed Before Half" days are weaker — 38% don't even reach 25% of the threshold. Bearish days get closer on average (49% vs 42%) but still fall short.

### Deepest Point by Session

| Session | Bullish Count | Bullish % | Bearish Count | Bearish % |
|---------|------:|--:|------:|--:|
| Opening (9:15-9:44) | 89 | 44.7% | 69 | 49.6% |
| Early Morning (9:45-10:29) | 17 | 8.5% | 16 | 11.5% |
| Late Morning (10:30-11:29) | 23 | 11.6% | 15 | 10.8% |
| Midday (11:30-12:29) | 4 | 2.0% | 5 | 3.6% |
| Early Afternoon (12:30-13:29) | 7 | 3.5% | 10 | 7.2% |
| Late Afternoon (13:30-14:29) | 15 | 7.5% | 6 | 4.3% |
| Closing (14:30-15:30) | 31 | 15.6% | 11 | 7.9% |

~50% of deepest points occur in the opening session (9:15-9:44) for both. The aligned move either starts and fails quickly, or never really starts at all.

### When Does the Reversal Become Obvious? (Price Crosses Back Past Open)

| Statistic | Bullish (161 of 199 days) | Bearish (126 of 139 days) |
|-----------|:-------------------------:|:-------------------------:|
| Days with clear reversal | 161 (80.9%) | 126 (90.6%) |
| Median reversal time | **9:30 AM** (15 min) | **9:50 AM** (35 min) |
| Average reversal time | 10:36 AM (81 min) | 10:46 AM (91 min) |
| 25th pctl | 9:20 AM (5 min) | 9:20 AM (5 min) |
| 75th pctl | 11:40 AM | 11:33 AM |
| **Median gap: deepest → reversal** | **10 min** | **15 min** |

For bullish alignment, the reversal (price drops below open) happens at a median of **9:30 AM** — just 15 minutes into the session. For bearish, the reversal (price rises above open) is at **9:50 AM**. The gap between deepest point and reversal is only 10-15 minutes.

### The First Hour Rule: Deepest Point by 10:15 AM = Aligned View Dead

| Deepest Point By | Bullish: Reversed by Close | Bearish: Reversed by Close |
|---|---:|---:|
| Within first hour (by 10:15) | **92.0%** (92 of 100) | **89.3%** (75 of 84) |
| After first hour | 46.5% (40 of 86) | 64.6% (31 of 48) |

**If the aligned move peaks within the first hour and hasn't crossed the half-threshold, there's an ~90% chance the market closes AGAINST the alignment.** This is the clearest timing signal in the dataset.

### Practical Summary

```
"REVERSED BEFORE HALF" TIMING:
  Bearish: Deepest point at median 9:37 AM → reversal by 9:50 AM
  Bullish: Deepest point at median 9:52 AM → reversal by 9:30 AM

  If by 10:15 AM the aligned move hasn't reached half the VIX range:
    → 90% chance the aligned view is WRONG by close
    → The failure is apparent within the first hour
    → On average, only 42-49% of the threshold is ever reached
```

---

# Part 1: Bullish Alignment (285 Days)

## Exceeded Half + Worked and Remained (77 days, 90.6%)

**The high-conviction bullish outcome.** The market moved up past the VIX half-threshold and held those gains by close.

### Recent Examples (2025-2026)

| Date | FII | PRO | VIX Predicted% | High% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2025-01-02 | Bullish | Mildly Bullish | 0.91% | +1.87% | **+1.62%** | 10:35 | Yes |
| 2025-01-29 | Strong Bullish | Strong Bullish | 1.15% | +0.68% | **+0.65%** | 12:15 | No |
| 2025-03-24 | Bullish | Mildly Bullish | 0.79% | +0.82% | **+0.68%** | 10:55 | No |
| 2025-05-15 | Mildly Bullish | Strong Bullish | 1.09% | +1.71% | **+1.38%** | 13:05 | Yes |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | 0.82% | +1.17% | **+1.03%** | 9:30 | Yes |
| 2025-10-16 | Bullish | Strong Bullish | 0.66% | +0.91% | **+0.67%** | 12:15 | No |
| 2025-11-26 | Mildly Bullish | Strong Bullish | 0.77% | +1.44% | **+1.40%** | 9:15 | No |
| 2025-12-22 | Strong Bullish | Strong Bullish | 0.60% | +0.48% | **+0.41%** | 9:30 | No |
| 2026-02-17 | Bullish | Strong Bullish | 0.84% | +0.49% | **+0.30%** | 11:35 | Yes |
| 2026-04-13 | Bullish | Bullish | 1.19% | +1.35% | **+0.97%** | 10:25 | Yes |

### Classic Examples (2021-2024)

| Date | FII | PRO | VIX Predicted% | High% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2021-08-03 | Bullish | Bullish | 0.81% | +1.22% | **+1.08%** | 12:20 | No |
| 2021-12-02 | Bullish | Strong Bullish | 1.23% | +1.36% | **+1.27%** | 10:15 | Yes |
| 2022-02-28 | Strong Bullish | Mildly Bullish | 1.68% | +2.02% | **+1.87%** | 11:20 | No |
| 2022-07-28 | Strong Bullish | Strong Bullish | 1.14% | +1.01% | **+0.88%** | 11:05 | Yes |
| 2023-07-20 | Bullish | Strong Bullish | 0.73% | +0.81% | **+0.70%** | 13:15 | Yes |
| 2024-04-25 | Bullish | Mildly Bullish | 0.65% | +1.38% | **+1.09%** | 9:35 | Yes |
| 2024-05-23 | Bullish | Strong Bullish | 1.35% | +1.68% | **+1.49%** | 11:55 | Yes |

### Walkthrough: 2025-01-02

```
Setup:
  FII View:  Bullish      PRO View: Mildly Bullish  → Bullish Alignment
  VIX Open:  14.51        Predicted Range: 0.91%
  Half Threshold: 0.91% / 2 = 0.455%

Intraday:
  High from Open:  +1.87%  → Exceeded 0.455% ✓ (by 4x!)
  Low from Open:   -0.13%  → Minimal downside dip
  Close from Open: +1.62%  → Strong bullish close

Timing:
  Threshold crossed at 10:35 AM (80 min from open)
  → Market dipped early, then rallied past threshold by late morning

Result: Exceeded Half + Worked and Remained ✓
  Expiry day — extra conviction. Rallied well past threshold and held.
```

### Walkthrough: 2025-05-15

```
Setup:
  FII View:  Mildly Bullish   PRO View: Strong Bullish  → Bullish Alignment
  VIX Open:  17.23             Predicted Range: 1.09%
  Half Threshold: 1.09% / 2 = 0.545%

Intraday:
  High from Open:  +1.71%  → Exceeded 0.545% ✓
  Low from Open:   -0.81%  → Significant dip first (Down to Up pattern)
  Close from Open: +1.38%  → Strong recovery and close near highs

Timing:
  Threshold crossed at 1:05 PM (230 min from open)
  → Morning selloff (-0.81%), then slow recovery, threshold crossed
    only in early afternoon. Late cross but still held by close.

Result: Exceeded Half + Worked and Remained ✓
```

---

## Exceeded Half + Reversed by Close — Bullish Failures (8 days, 9.4%)

**The rare failure.** Market exceeded the VIX half-threshold upward but reversed and closed bearish. Only 8 out of 85.

### All 8 Instances

| Date | FII | PRO | VIX Predicted% | High% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|------:|:----------:|:---:|
| 2021-11-30 | Bullish | Bullish | 1.31% | +1.60% | -0.69% | **-0.45%** | 9:20 | No |
| 2022-05-23 | Strong Bullish | Strong Bullish | 1.46% | +0.76% | -0.64% | **-0.61%** | 13:30 | No |
| 2024-04-30 | Strong Bullish | Strong Bullish | 0.77% | +0.46% | -0.49% | **-0.41%** | 10:50 | No |
| 2025-01-24 | Strong Bullish | Strong Bullish | 1.05% | +0.70% | -0.58% | **-0.40%** | 11:40 | No |
| 2025-08-12 | Bullish | Strong Bullish | 0.77% | +0.57% | -0.40% | **-0.32%** | 9:45 | No |
| 2025-09-02 | Strong Bullish | Bullish | 0.71% | +0.42% | -0.53% | **-0.32%** | 10:00 | Yes |
| 2025-11-13 | Bullish | Bullish | 0.76% | +0.40% | -0.38% | **-0.08%** | 13:40 | No |
| 2026-06-25 | Bullish | Strong Bullish | 0.84% | +0.56% | -0.36% | **-0.30%** | 11:55 | No |

### Walkthrough: 2021-11-30

```
Setup:
  VIX Open: 20.83  →  Half Threshold: 0.655%

Timing:
  Threshold crossed at 9:20 AM (5 min from open!)
  → Gap-up opening exceeded the threshold immediately.
    The rally was front-loaded and unsustainable — classic morning trap.

Result: Market rallied 1.6% then gave it all back. Close: -0.45%.
```

### Failure Patterns
- All 8 had "Top to Down" direction — bullish move came first, then reversed
- 5 of 8 crossed before 12:00 PM — early spikes that faded
- 7 of 8 were non-expiry days
- Average close: only -0.36%

---

## Reversed Before Half + Worked and Remained — Bullish (54 days, 27.0%)

**The grinding win.** Never exceeded the threshold, but closed bullish anyway. Low-conviction, narrow-range days.

### Timing: When Did the Bullish Move Peak?

The bullish high peaked at a **median of 9:52 AM** (38 min from open) — and never reached the threshold. On 38% of these days the high didn't even reach 25% of the half-threshold.

### Examples

| Date | FII | PRO | VIX Predicted% | High% | Close% | Peak Time | % of Threshold |
|------|-----|-----|------:|------:|------:|:----------:|------:|
| 2020-09-11 | Mildly Bullish | Strong Bullish | 1.34% | +0.39% | **+0.06%** | 9:25 | 58.5% |
| 2021-03-02 | Mildly Bullish | Mildly Bullish | 1.61% | +0.63% | **+0.51%** | 15:25 | 78.3% |

### Near Misses (Almost Crossed)

| Date | VIX Predicted% | Half Threshold | Peak Move% | % Reached | Peak Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2025-12-12 | 0.66% | 0.33% | 0.333% | 100.9% | 15:10 | **+0.28%** |
| 2024-05-14 | 1.30% | 0.65% | 0.649% | 99.8% | 14:05 | **+0.44%** |
| 2021-10-12 | 1.01% | 0.505% | 0.501% | 99.2% | 15:15 | **+0.50%** |
| 2021-09-03 | 0.90% | 0.45% | 0.446% | 99.1% | 15:20 | **+0.34%** |

Near misses that "Worked and Remained" tend to peak **late afternoon** (14:00-15:30) — the rally builds all day and just barely falls short of the threshold but still closes positive.

**Pattern**: Average close only +0.16%. High% well below threshold. Barely positive — these are low-quality wins.

---

## Reversed Before Half + Reversed by Close — Bullish (146 days, 73.0%)

**The dominant bearish outcome.** When the bullish move can't reach half the VIX range, 73% close bearish.

### Timing: How Early Is the Failure Apparent?

On these 146 days, the bullish high peaked at a **median of 9:15 AM** — the opening candle was often the day's best bullish attempt. The reversal (price drops below open) came at a **median of 9:20-9:30 AM**.

**If the bullish high peaks by 10:15 AM and hasn't crossed the threshold → 92% chance of bearish close.**

### Examples

| Date | FII | PRO | VIX Predicted% | High% | Close% | Peak Time | % of Threshold |
|------|-----|-----|------:|------:|------:|:----------:|------:|
| 2025-01-03 | Bullish | Strong Bullish | 0.87% | +0.00% | **-0.85%** | 9:15 | 0.0% |
| 2025-01-21 | Mildly Bullish | Strong Bullish | 1.03% | +0.02% | **-1.57%** | 9:15 | 3.9% |
| 2025-05-06 | Mildly Bullish | Bullish | 1.16% | +0.04% | **-0.67%** | 9:15 | 6.2% |
| 2025-09-04 | Bullish | Strong Bullish | 0.69% | +0.00% | **-0.96%** | 9:15 | 0.0% |

### Zero Momentum Days (High% = 0)

| Date | VIX Predicted% | Close% |
|------|------:|------:|
| 2022-03-10 | 1.73% | **-1.14%** |
| 2022-10-25 | 1.10% | **-0.93%** |
| 2022-12-09 | 0.84% | **-0.91%** |
| 2024-06-04 | 1.32% | **-5.10%** |

These days gapped down on the open — zero bullish attempt at all. The 2024-06-04 example (-5.10%) is the worst bullish alignment day in the dataset.

### Walkthrough: 2025-01-21

```
Setup:
  VIX Predicted: 1.03%  →  Half Threshold: 0.515%

Intraday:
  High from Open: +0.02%  → Barely moved up. Nowhere near 0.515%.
  Close: -1.57%           → Massive selloff despite bullish alignment.

Timing:
  Bullish peak at 9:15 AM (0 min) — opening candle was the high.
  Reversal at 9:20 AM — within 5 minutes, price was below open.
  Only reached 3.9% of the half-threshold.

  → Failure was obvious within 5 minutes of the open.
```

**Pattern**: Most have "Top to Down" direction. High% typically < 0.10%. Peak at 9:15 AM (opening candle). Average close: -0.36%.

---

# Part 2: Bearish Alignment (293 Days)

## Exceeded Half + Worked and Remained (129 days, 84.3%)

**The high-conviction bearish outcome.** The market dropped past the VIX half-threshold and held those losses by close.

### Recent Examples (2025-2026)

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2025-01-06 | Bearish | Strong Bearish | 0.85% | -2.05% | **-1.73%** | 9:45 | No |
| 2025-01-09 | Bearish | Bearish | 0.91% | -0.73% | **-0.50%** | 10:45 | Yes |
| 2025-03-26 | Bearish | Strong Bearish | 0.86% | -1.05% | **-1.00%** | 11:55 | No |
| 2025-07-02 | Bearish | Bearish | 0.79% | -0.82% | **-0.57%** | 10:40 | No |
| 2025-07-25 | Mildly Bearish | Strong Bearish | 0.68% | -0.82% | **-0.71%** | 9:15 | No |
| 2025-09-05 | Bearish | Strong Bearish | 0.68% | -0.79% | **-0.30%** | 10:10 | No |
| 2025-10-14 | Bearish | Strong Bearish | 0.69% | -0.86% | **-0.61%** | 10:00 | Yes |
| 2025-10-31 | Strong Bearish | Strong Bearish | 0.76% | -0.59% | **-0.51%** | 11:10 | No |
| 2025-11-24 | Strong Bearish | Strong Bearish | 0.86% | -0.81% | **-0.69%** | 15:00 | No |
| 2026-02-24 | Mildly Bearish | Strong Bearish | 0.89% | -1.23% | **-0.71%** | 9:30 | Yes |
| 2026-05-12 | Bearish | Mildly Bearish | 1.17% | -1.58% | **-1.23%** | 11:05 | Yes |

### Classic Examples (2021-2024)

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2021-01-18 | Bearish | Bearish | 1.51% | -1.58% | **-1.54%** | 9:30 | No |
| 2021-03-25 | Mildly Bearish | Strong Bearish | 1.41% | -2.10% | **-1.54%** | 9:20 | Yes |
| 2021-10-28 | Bearish | Strong Bearish | 1.06% | -2.13% | **-1.79%** | 9:35 | Yes |
| 2021-12-06 | Strong Bearish | Strong Bearish | 1.16% | -1.83% | **-1.74%** | 9:35 | No |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 1.55% | -2.08% | **-2.00%** | 13:40 | Yes |
| 2022-12-15 | Bearish | Strong Bearish | 0.81% | -1.21% | **-1.15%** | 12:30 | Yes |
| 2023-01-25 | Mildly Bearish | Strong Bearish | 0.86% | -1.36% | **-1.01%** | 9:45 | Yes |
| 2024-10-17 | Strong Bearish | Strong Bearish | 0.82% | -1.19% | **-1.11%** | 9:25 | Yes |
| 2024-11-07 | Strong Bearish | Strong Bearish | 0.94% | -1.27% | **-1.20%** | 9:25 | Yes |

### Walkthrough: 2025-01-06

```
Setup:
  FII View:  Bearish         PRO View: Strong Bearish  → Strong Bearish Alignment
  VIX Open:  13.54           Predicted Range: 0.85%
  Half Threshold: 0.85% / 2 = 0.425%

Intraday:
  High from Open:  +0.18%  → Minor upside attempt
  Low from Open:   -2.05%  → Crashed well past 0.425% threshold (by 5x!)
  Close from Open: -1.73%  → Closed deep in the red, near lows

Timing:
  Threshold crossed at 9:45 AM (30 min from open)
  → Selling started immediately. Within 30 minutes, the bearish view
    was confirmed. The rest of the day was continuation.

Result: Exceeded Half + Worked and Remained ✓
```

### Walkthrough: 2022-02-24 (Russia-Ukraine Invasion Day)

```
Setup:
  VIX Open: 24.54  →  Half Threshold: 0.775%

Timing:
  Threshold crossed at 1:40 PM (265 min from open)
  → Unusually late! Market first rallied +0.93% in the morning.
    Selloff only started after lunch, then collapsed rapidly.
    Despite late cross, closed at -2.00% — no recovery once selling began.

Result: Exceeded Half + Worked and Remained ✓
  Total range: 3.01% — nearly double the VIX prediction.
```

---

## Exceeded Half + Reversed by Close — Bearish Failures (24 days, 15.7%)

**The V-shaped recovery.** Market dropped past the threshold but completely reversed and closed bullish. 24 out of 153 — more frequent than bullish failures (8 of 85).

### All 24 Instances

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2020-09-01 | Strong Bearish | Strong Bearish | 1.44% | -0.85% | **+0.26%** | 9:15 | No |
| 2020-11-20 | Mildly Bearish | Strong Bearish | 1.23% | -0.65% | **+0.25%** | 11:20 | No |
| 2020-11-26 | Bearish | Strong Bearish | 1.46% | -0.90% | **+0.84%** | 10:00 | Yes |
| 2020-12-22 | Mildly Bearish | Strong Bearish | 1.46% | -1.34% | **+0.65%** | 9:35 | No |
| 2021-04-01 | Strong Bearish | Bearish | 1.30% | -0.71% | **+0.46%** | 10:55 | Yes |
| 2021-09-21 | Bearish | Strong Bearish | 1.10% | -0.71% | **+0.65%** | 11:10 | No |
| 2022-04-28 | Mildly Bearish | Strong Bearish | 1.30% | -0.69% | **+0.24%** | 10:45 | Yes |
| 2022-05-26 | Mildly Bearish | Strong Bearish | 1.59% | -1.25% | **+0.60%** | 10:25 | Yes |
| 2022-08-03 | Bearish | Bearish | 1.17% | -0.71% | **+0.25%** | 9:45 | No |
| 2023-04-24 | Bearish | Bearish | 0.73% | -0.54% | **+0.23%** | 9:35 | No |
| 2023-06-20 | Bearish | Strong Bearish | 0.71% | -0.49% | **+0.43%** | 9:45 | No |
| 2023-07-19 | Bearish | Strong Bearish | 0.74% | -0.38% | **+0.22%** | 9:25 | No |
| 2023-07-31 | Strong Bearish | Bearish | 0.64% | -0.35% | **+0.39%** | 9:20 | No |
| 2024-01-18 | Bearish | Strong Bearish | 0.95% | -0.60% | **+0.29%** | 10:10 | Yes |
| 2024-02-13 | Strong Bearish | Strong Bearish | 1.01% | -0.56% | **+0.29%** | 9:30 | No |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | 0.97% | -0.51% | **+0.09%** | 9:40 | Yes |
| 2024-03-20 | Bearish | Strong Bearish | 0.89% | -0.61% | **+0.05%** | 9:30 | No |
| 2024-06-05 | Strong Bearish | Strong Bearish | 1.69% | -1.52% | **+2.01%** | 9:20 | No |
| 2024-09-12 | Mildly Bearish | Strong Bearish | 0.86% | -0.47% | **+1.02%** | 11:25 | Yes |
| 2024-10-28 | Strong Bearish | Strong Bearish | 0.92% | -0.48% | **+0.48%** | 9:30 | No |
| 2025-08-07 | Bearish | Mildly Bearish | 0.75% | -0.49% | **+0.66%** | 13:20 | Yes |
| 2026-01-21 | Mildly Bearish | Bearish | 0.80% | -0.88% | **+0.11%** | 10:40 | No |
| 2026-02-06 | Bearish | Strong Bearish | 0.77% | -0.44% | **+0.26%** | 9:40 | No |
| 2026-03-09 | Strong Bearish | Strong Bearish | 1.25% | -0.71% | **+0.58%** | 9:25 | No |

### Walkthrough: 2024-06-05

```
Setup:
  VIX Open: 26.75  →  Half Threshold: 0.845%

Timing:
  Threshold crossed at 9:20 AM (5 min from open!)
  → Gap-down opening crashed through threshold on the first candle.
    Then spent the ENTIRE rest of the day recovering.
    Close: +2.01% — largest failure in the dataset.
```

### Failure Patterns
- All 24 had "Down to Up" direction — bearish dip came first, then reversed
- **17 of 24 (71%) crossed before 10:45 AM** — early morning panic dips
- Median cross time for failures: ~9:40 AM (vs ~10:25 AM overall)
- Elevated VIX overrepresented: 10 of 24 (42%)
- 8 of 24 were expiry days (33%)
- Average close: +0.44%

---

## Reversed Before Half + Worked and Remained — Bearish (26 days, 18.6%)

**The grinding bearish win.** Never exceeded the threshold, but closed bearish anyway. Rare and low-conviction.

### Timing: When Did the Bearish Move Peak?

The bearish low peaked at a **median of 9:37 AM** (22 min) — but these 26 days are different because the price **never crossed back above open** (or did so only late). On average they reached 65% of the threshold — closer than the broader group but still short.

### Examples

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Peak Time | % of Threshold |
|------|-----|-----|------:|------:|------:|:----------:|------:|
| 2025-05-28 | Bearish | Mildly Bearish | 1.17% | -0.38% | **-0.30%** | 10:15 | 65.6% |
| 2025-11-28 | Mildly Bearish | Bearish | 0.74% | -0.25% | **-0.13%** | 9:15 | 67.0% |
| 2026-03-12 | Strong Bearish | Strong Bearish | 1.33% | -0.50% | **-0.15%** | 9:15 | 75.3% |
| 2023-10-16 | Strong Bearish | Strong Bearish | 0.67% | -0.23% | **-0.03%** | 9:20 | 68.7% |

### Near Misses (Almost Crossed — Bearish)

| Date | VIX Predicted% | Half Threshold | Peak Move% | % Reached | Peak Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2024-10-16 | 0.82% | 0.41% | 0.400% | 97.6% | 11:45 | **-0.19%** |
| 2023-08-25 | 0.74% | 0.37% | 0.346% | 93.5% | 10:30 | **-0.28%** |

These near misses that still "worked" had the deepest point in the **late morning** — deeper selling over a longer period, even if it didn't quite cross.

**Pattern**: Average close only -0.16%. Low% well inside threshold. Only 26 of 140 "Reversed Before Half" days — this quadrant is rare.

---

## Reversed Before Half + Reversed by Close — Bearish (114 days, 81.4%)

**The dominant bullish outcome.** When the bearish move can't reach half the VIX range, 81.4% close bullish.

### Timing: How Early Is the Failure Apparent?

On these 114 days, the bearish low peaked at a **median of 9:37 AM** — selling exhausted within the first 22 minutes. The reversal (price rises above open) came at a **median of 9:50 AM**.

**If the bearish low peaks by 10:15 AM and hasn't crossed the threshold → 89% chance of bullish close.**

### Examples

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Peak Time | % of Threshold |
|------|-----|-----|------:|------:|------:|:----------:|------:|
| 2025-01-31 | Strong Bearish | Strong Bearish | 1.10% | -0.08% | **+1.02%** | 9:15 | 15.1% |
| 2025-04-07 | Bearish | Bearish | 0.87% | -0.07% | **+2.20%** | 9:15 | 15.6% |
| 2025-06-13 | Bearish | Strong Bearish | 0.88% | +0.00% | **+1.07%** | 9:15 | 0.0% |
| 2025-09-16 | Mildly Bearish | Strong Bearish | 0.66% | -0.01% | **+0.72%** | 9:15 | 3.9% |

### Zero Momentum Days (Low% = 0)

| Date | VIX Predicted% | Close% |
|------|------:|------:|
| 2022-09-05 | 1.23% | **+0.61%** |
| 2022-09-07 | 1.23% | **+0.63%** |
| 2022-11-28 | 0.84% | **+0.67%** |
| 2025-06-13 | 0.88% | **+1.07%** |
| 2026-06-02 | 1.04% | **+1.27%** |

These days gapped up on the open — zero bearish attempt at all. The bearish alignment signal was completely overridden by bullish price action from the first candle.

### Near Misses That Still Reversed

| Date | VIX Predicted% | Half Threshold | Peak Move% | % Reached | Peak Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2023-08-23 | 0.74% | 0.37% | 0.372% | 100.5% | 9:55 | **+0.01%** |
| 2026-02-02 | 0.95% | 0.475% | 0.472% | 99.4% | 11:25 | **+1.14%** |
| 2024-10-18 | 0.84% | 0.42% | 0.394% | 93.8% | 9:25 | **+0.80%** |

Even days that came within 1% of the threshold still reversed bullish — the threshold is not a hard floor, and the 5-min candle data may slightly differ from daily OHLC used in the original classification.

### Walkthrough: 2025-04-07

```
Setup:
  VIX Predicted: 0.87%  →  Half Threshold: 0.435%

Intraday:
  Low from Open: -0.07%  → Barely any downside. Didn't reach 0.435%.
  Close: +2.20%          → Massive rally despite Strong Bearish Alignment.

Timing:
  Bearish peak at 9:15 AM (0 min) — opening candle was the low.
  Reversal at 9:20 AM — within 5 minutes, price was above open.
  Only reached 15.6% of the half-threshold.

  → Failure was obvious within 5 minutes of the open.
```

**Pattern**: All "Down to Up" direction. Low% typically < -0.10%. Peak at 9:15 AM (opening candle). Average close: +0.36%.

---

# Part 3: Year-by-Year and Regime Breakdowns

## Exceeded Half: Year-by-Year WR%

| Year | Bullish Count | Bullish WR% | Bearish Count | Bearish WR% |
|------|------:|----:|------:|----:|
| 2020 | 5 | 100% | 4 | 0% |
| 2021 | 12 | 92% | 18 | 89% |
| 2022 | 9 | 89% | 31 | 90% |
| 2023 | 16 | 100% | 36 | 92% |
| 2024 | 15 | 93% | 25 | 76% |
| 2025 | 20 | 90% | 25 | 96% |
| 2026 | 8 | 63% | 14 | 64% |

2020 bearish is an outlier (4 days, COVID recovery). 2026 shows lower WR% for both — partial year.

## Reversed Before Half: Year-by-Year Loss Rate

| Year | Bullish Count | Bearish Close% | Bearish Count | Bullish Close% |
|------|------:|----:|------:|----:|
| 2020 | 2 | 50% | 3 | 100% |
| 2021 | 24 | 67% | 13 | 85% |
| 2022 | 34 | 74% | 23 | 91% |
| 2023 | 51 | 75% | 25 | 84% |
| 2024 | 41 | 78% | 34 | 79% |
| 2025 | 24 | 63% | 21 | 76% |
| 2026 | 24 | 79% | 21 | 71% |

## VIX Regime: Exceeded Half Distribution

| VIX Regime | Bullish Count | Bullish % | Bearish Count | Bearish % |
|------------|------:|----:|------:|----:|
| Low (<15) | 51 | 60.0% | 93 | 60.8% |
| Normal (15-20) | 24 | 28.2% | 38 | 24.8% |
| Elevated (20-30) | 10 | 11.8% | 22 | 14.4% |

Most "Exceeded Half" days occur in Low VIX — the threshold is smaller and easier to cross.

## Expiry Day Performance

| Alignment | Expiry WR% | Non-Expiry WR% | Expiry Effect |
|-----------|:----------:|:--------------:|:--------------|
| Bullish | **94.7%** | 89.4% | +5.3% (helps) |
| Bearish | **81.0%** | 85.6% | -4.6% (hurts) |

Expiry helps bullish (momentum continues) but hurts bearish (short-covering rallies).

### Expiry Examples (Exceeded Half)

**Bullish Expiry** (19 days, 18 worked):

| Date | VIX | High% | Close% | Cross Time |
|------|----:|------:|------:|:----------:|
| 2021-12-02 | 19.45 | +1.36% | **+1.27%** | 10:15 |
| 2024-04-25 | 10.28 | +1.38% | **+1.09%** | 9:35 |
| 2025-01-02 | 14.51 | +1.87% | **+1.62%** | 10:35 |
| 2025-05-15 | 17.23 | +1.71% | **+1.38%** | 13:05 |
| 2026-04-13 | 18.85 | +1.35% | **+0.97%** | 10:25 |

**Bearish Expiry** (42 days, 34 worked):

| Date | VIX | Low% | Close% | Cross Time |
|------|----:|------:|------:|:----------:|
| 2021-03-25 | 22.46 | -2.10% | **-1.54%** | 9:20 |
| 2022-02-24 | 24.54 | -2.08% | **-2.00%** | 13:40 |
| 2023-01-25 | 13.66 | -1.36% | **-1.01%** | 9:45 |
| 2024-10-17 | 13.05 | -1.19% | **-1.11%** | 9:25 |
| 2026-05-12 | 18.55 | -1.58% | **-1.23%** | 11:05 |

---

# Quick Reference: Decision Rules

```
┌──────────────────────────────────────────────────────────────────────┐
│               FII + PRO ALIGNED + VIX HALF-THRESHOLD                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  BULLISH ALIGNMENT                                                   │
│  ├─ Exceeded Half → 90.6% close bullish (avg +0.59%)                │
│  │   Median cross: 11:37 AM                                         │
│  │   Afternoon cross (12:30+) → ~95-100% WR                         │
│  │   Failures: 8 of 85 — all "Top to Down" morning traps            │
│  │                                                                   │
│  └─ Reversed Before Half → 73% close BEARISH (avg -0.36%)           │
│      Bullish peak: median 9:52 AM (only 42% of threshold reached)   │
│      Reversal apparent: median 9:30 AM (price drops below open)     │
│      If peak by 10:15 & no threshold cross → 92% close bearish      │
│      Zero-momentum days (High=0%): gap-down, never tried to rally   │
│                                                                      │
│  BEARISH ALIGNMENT                                                   │
│  ├─ Exceeded Half → 84.3% close bearish (avg -0.45%)                │
│  │   Median cross: 10:25 AM (72 min faster than bullish)             │
│  │   Afternoon cross (12:30+) → ~95-100% WR                         │
│  │   DANGER: Late morning (10:30-11:30) → only 62% WR               │
│  │   Failures: 24 of 153 — mostly early AM panic dips                │
│  │                                                                   │
│  └─ Reversed Before Half → 81.4% close BULLISH (avg +0.36%)         │
│      Bearish peak: median 9:37 AM (only 49% of threshold reached)   │
│      Reversal apparent: median 9:50 AM (price rises above open)     │
│      If peak by 10:15 & no threshold cross → 89% close bullish      │
│      Zero-momentum days (Low=0%): gap-up, never tried to sell off   │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  EXCEEDED HALF TIMING                                                │
│  • Bearish crosses threshold 52% vs 30% for bullish                  │
│  • Bullish has higher WR% (91% vs 84%) when it does cross            │
│  • Selloffs are front-loaded (panic); rallies build gradually        │
│  • Expiry helps bullish (+5.3%) but hurts bearish (-4.6%)            │
│  • Afternoon crosses → near-perfect WR% for both directions         │
├──────────────────────────────────────────────────────────────────────┤
│  REVERSED BEFORE HALF TIMING (the "when is it dead?" signal)         │
│  • Both directions: ~50% peak in the opening session (9:15-9:44)     │
│  • Reversal (price crosses open) within 10-15 min of peak            │
│  • If aligned move peaks by 10:15 & misses threshold → ~90% WRONG   │
│  • On average, only 42-49% of the half-threshold is ever reached     │
│  • Bullish failures often show High% = 0 (gap-down, no rally)       │
│  • Bearish failures often show Low% = 0 (gap-up, no selloff)        │
├──────────────────────────────────────────────────────────────────────┤
│  CAVEAT: FII/PRO alignment is known only after T+1 settlement.      │
│  The VIX half-threshold IS observable intraday, but the              │
│  alignment condition is not.                                         │
└──────────────────────────────────────────────────────────────────────┘
```
