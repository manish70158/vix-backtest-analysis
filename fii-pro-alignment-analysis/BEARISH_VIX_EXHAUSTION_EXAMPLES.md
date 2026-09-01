# Bearish Alignment + VIX Half-Range Exhaustion: Detailed Examples

> **Context**: When both FII and PRO are bearish (T+1 data), we check whether
> the market's downward move exceeded half the VIX-predicted daily range before
> any reversal. This document walks through real examples from all four outcome
> quadrants.

---

## How It Works

1. **FII and PRO both bearish** (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the bearish move (low from open) exceed that half threshold?

```
VIX Predicted Range = 0.86%
Half Threshold      = 0.43%
Intraday Low%       = -0.60%  ← Exceeded 0.43% downside → "Exceeded Half"

vs.

VIX Predicted Range = 1.30%
Half Threshold      = 0.65%
Intraday Low%       = -0.14%  ← Did NOT reach 0.65% → "Reversed Before Half"
```

---

## Summary Table (293 Bearish Alignment Days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 153 | 52.2% | 129 | **84.3%** | -0.45% |
| Reversed Before Half | 140 | 47.8% | 26 | **18.6%** | +0.36% |

**Key takeaway**: If the bearish move exceeded half the VIX range, the market closed bearish 84.3% of the time. If it didn't reach that level, the market closed bullish 81.4% of the time.

### Bearish vs Bullish Alignment Comparison

| Metric | Bullish (285 days) | Bearish (293 days) |
|--------|-------------------:|-------------------:|
| Exceeded Half: count | 85 (29.8%) | 153 (52.2%) |
| Exceeded Half: WR% | 90.6% | 84.3% |
| Reversed Before Half: count | 200 (70.2%) | 140 (47.8%) |
| Reversed Before Half: loss rate | 73.0% | 81.4% |

**Notable asymmetry**: Bearish alignment exceeds the VIX half-threshold 52% of the time vs only 30% for bullish. Selloffs more readily exhaust the VIX-predicted range than rallies. However, bullish has a higher WR% when the threshold is exceeded (90.6% vs 84.3%).

---

## When Does the Threshold Get Crossed? (5-Minute Candle Analysis)

Using 5-minute candle data from PostgreSQL, we identified the **exact time** each day's bearish low first crossed the VIX half-threshold.

### Bearish Alignment Timing Summary (153 Exceeded Half days)

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **10:25 AM** | 70 min |
| Average | 11:12 AM | 117 min |
| 25th percentile | 9:40 AM | 25 min |
| 75th percentile | 12:35 PM | 200 min |
| Earliest | 9:15 AM | 0 min |
| Latest | 3:25 PM | 370 min |

### Session Distribution

| Session | Count | % | WR% |
|---------|------:|--:|----:|
| Opening (9:15-9:44) | 44 | 28.8% | 81.8% |
| Early Morning (9:45-10:29) | 35 | 22.9% | 80.0% |
| Late Morning (10:30-11:29) | 21 | 13.7% | 61.9% |
| Midday (11:30-12:29) | 11 | 7.2% | 90.9% |
| Early Afternoon (12:30-13:29) | 15 | 9.8% | 93.3% |
| Late Afternoon (13:30-14:29) | 10 | 6.5% | 100.0% |
| Closing (14:30-15:30) | 17 | 11.1% | 100.0% |

**Key insight**: Bearish selloffs are **front-loaded** — 52% cross by 10:30 AM (vs only 34% for bullish). The median is 10:25 AM, over an hour faster than bullish (11:37 AM). However, WR% dips in late morning (62%) — this is the V-shaped recovery danger zone.

### Bearish vs Bullish Timing Comparison

| Metric | Bullish | Bearish |
|--------|:-------:|:-------:|
| Median cross time | 11:37 AM | **10:25 AM** |
| % crossed by 10:30 AM | 34% | **52%** |
| Opening session (9:15-9:44) | 20% | **29%** |
| Lowest WR% session | Early Morning (83%) | Late Morning (**62%**) |

Selloffs are faster because panic selling is immediate; buying conviction builds gradually.

### VIX Regime Timing

| VIX Regime | Avg Cross Time | Median Cross Time |
|------------|:--------------:|:-----------------:|
| Low (<15) | 11:22 AM | 10:40 AM |
| Normal (15-20) | 10:36 AM | 10:02 AM |
| Elevated (20-30) | 11:28 AM | 10:20 AM |

Normal VIX crosses fastest — the threshold is moderate-sized and selloffs are sharp. Elevated VIX has a wider absolute threshold.

---

## Quadrant 1: Exceeded Half + Worked and Remained (129 days, 84.3% of Exceeded Half)

**The high-conviction bearish outcome.** The market moved down past the VIX half-threshold and held those losses by close.

### Recent Examples (2025-2026)

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2025-01-06 | Bearish | Strong Bearish | 0.85% | -2.05% | **-1.73%** | 9:45 | No |
| 2025-01-09 | Bearish | Bearish | 0.91% | -0.73% | **-0.50%** | 10:45 | Yes |
| 2025-03-26 | Bearish | Strong Bearish | 0.86% | -1.05% | **-1.00%** | 11:55 | No |
| 2025-04-30 | Mildly Bearish | Bearish | 1.09% | -0.59% | **-0.39%** | 15:25 | Yes |
| 2025-07-02 | Bearish | Bearish | 0.79% | -0.82% | **-0.57%** | 10:40 | No |
| 2025-07-25 | Mildly Bearish | Strong Bearish | 0.68% | -0.82% | **-0.71%** | 9:15 | No |
| 2025-09-05 | Bearish | Strong Bearish | 0.68% | -0.79% | **-0.30%** | 10:10 | No |
| 2025-09-25 | Mildly Bearish | Bearish | 0.66% | -0.62% | **-0.52%** | 14:10 | No |
| 2025-10-14 | Bearish | Strong Bearish | 0.69% | -0.86% | **-0.61%** | 10:00 | Yes |
| 2025-10-31 | Strong Bearish | Strong Bearish | 0.76% | -0.59% | **-0.51%** | 11:10 | No |
| 2025-11-24 | Strong Bearish | Strong Bearish | 0.86% | -0.81% | **-0.69%** | 15:00 | No |
| 2026-02-24 | Mildly Bearish | Strong Bearish | 0.89% | -1.23% | **-0.71%** | 9:30 | Yes |
| 2026-05-12 | Bearish | Mildly Bearish | 1.17% | -1.58% | **-1.23%** | 11:05 | Yes |
| 2026-06-09 | Mildly Bearish | Bearish | 1.07% | -0.66% | **-0.01%** | 10:45 | Yes |

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
    had already been confirmed. The rest of the day was continuation.

Result: Exceeded Half + Worked and Remained ✓
  Massive selloff. The low of -2.05% dwarfed the VIX prediction of 0.85%.
  Close at -1.73% means the bearish view was decisively confirmed.
```

### Walkthrough: 2025-07-25

```
Setup:
  FII View:  Mildly Bearish  PRO View: Strong Bearish  → Bearish Alignment
  VIX Open:  10.72            Predicted Range: 0.68%
  Half Threshold: 0.68% / 2 = 0.34%

Intraday:
  High from Open:  +0.00%  → Zero upside — opened at the day's high
  Low from Open:   -0.82%  → Exceeded 0.34% threshold (by 2.4x)
  Close from Open: -0.71%  → Closed near lows

Timing:
  Threshold crossed at 9:15 AM (0 min — on the very first candle!)
  → Gap-down opening. The market opened below the threshold immediately.
    No opportunity to react — selling was priced into the open.

Result: Exceeded Half + Worked and Remained ✓
  "Top to Down" pattern. Market opened and sold off all day.
  Low VIX environment but the actual range (0.82%) exceeded the prediction (0.68%).
```

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
| 2023-05-18 | Strong Bearish | Bearish | 0.83% | -1.00% | **-0.84%** | 12:15 | Yes |
| 2024-10-17 | Strong Bearish | Strong Bearish | 0.82% | -1.19% | **-1.11%** | 9:25 | Yes |
| 2024-11-07 | Strong Bearish | Strong Bearish | 0.94% | -1.27% | **-1.20%** | 9:25 | Yes |

### Walkthrough: 2022-02-24 (Russia-Ukraine Invasion Day)

```
Setup:
  FII View:  Mildly Bearish   PRO View: Strong Bearish  → Bearish Alignment
  VIX Open:  24.54             Predicted Range: 1.55%
  Half Threshold: 1.55% / 2 = 0.775%

Intraday:
  High from Open:  +0.93%  → Morning rally attempt (bounce before collapse)
  Low from Open:   -2.08%  → Massive selloff, exceeded threshold by 2.7x
  Close from Open: -2.00%  → Closed near day's lows

Timing:
  Threshold crossed at 1:40 PM (265 min from open)
  → Unusually late cross! The market first rallied +0.93% in the morning.
    The selloff only started after lunch, then collapsed rapidly.
    Despite the late cross, the market closed near lows — once selling
    started, there was no recovery.

Result: Exceeded Half + Worked and Remained ✓
  Elevated VIX day (24.54). Market first rallied +0.93%, then reversed hard.
  Total range of 3.01% was nearly double the VIX prediction.
  This was an expiry day — extreme conviction.
```

---

## Quadrant 2: Exceeded Half + Reversed by Close (24 days, 15.7% of Exceeded Half)

**The bearish failure case.** The market dropped past the VIX half-threshold but then completely reversed and closed bullish. 24 out of 153 times — more frequent than bullish failures (8 out of 85).

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
  FII View:  Strong Bearish   PRO View: Strong Bearish  → Strong Bearish Alignment
  VIX Open:  26.75             Predicted Range: 1.69%
  Half Threshold: 1.69% / 2 = 0.845%

Intraday:
  High from Open:  +2.45%  → Enormous rally
  Low from Open:   -1.52%  → Exceeded 0.845% threshold first ✓
  Close from Open: +2.01%  → Closed massively bullish

Timing:
  Threshold crossed at 9:20 AM (5 min from open!)
  → Gap-down opening crashed through the threshold on the first candle.
    But then the market spent the ENTIRE rest of the day recovering.
    Early cross + violent reversal = the threshold was meaningless here.

Result: Exceeded Half + Reversed by Close ✗
  "Down to Up" pattern. Market crashed first (-1.52%), then reversed hard.
  The close of +2.01% is the largest failure in the dataset.
  Elevated VIX (26.75) — high volatility means wide swings both ways.
  Total range was 3.97% — unprecedented for bearish failures.
```

### Walkthrough: 2020-12-22

```
Setup:
  FII View:  Mildly Bearish   PRO View: Strong Bearish  → Bearish Alignment
  VIX Open:  23.19             Predicted Range: 1.46%
  Half Threshold: 1.46% / 2 = 0.73%

Intraday:
  High from Open:  +0.88%  → Strong bounce after the dip
  Low from Open:   -1.34%  → Exceeded 0.73% threshold (by 1.8x)
  Close from Open: +0.65%  → Closed bullish despite the morning selloff

Timing:
  Threshold crossed at 9:35 AM (20 min from open)
  → Early morning selloff breached the threshold within 20 minutes.
    But the market reversed and spent 5+ hours rallying back.

Result: Exceeded Half + Reversed by Close ✗
  Classic V-shaped recovery. The market dropped -1.34%, then rallied 2.22%
  from the low to close positive. The bearish view was right for the first
  half but completely wrong by close.
```

### Pattern in the Failures

- All 24 had a **"Down to Up"** move direction — the bearish move came first, then reversed
- **Timing is critical**: 17 of 24 (71%) crossed before 10:45 AM — early morning selloff then full-day recovery
- Median cross time for failures: ~9:40 AM (vs ~10:25 AM for all exceeded)
- **Early crosses fail more often for bearish** — if the selloff is concentrated in the opening 30 min, it may be a panic dip rather than sustained selling
- Average close was +0.44% — the bullish reversal was meaningful, not marginal
- Elevated VIX (>20) is overrepresented — 10 of 24 (42%) vs 14% of all exceeded-half days
- 8 of 24 were expiry days (33%) — higher than the ~28% expiry rate in the full dataset
- These are often "panic dip then recovery" days

---

## Quadrant 3: Reversed Before Half + Worked and Remained (26 days, 18.6% of Reversed Before Half)

**The grinding bearish win.** The market never dropped past the VIX half-threshold, yet still managed to close bearish. These are low-conviction, narrow-range down days.

### Timing: When Did the Bearish Move Peak?

Across all 139 "Reversed Before Half" bearish days, the low peaked at a **median of 9:37 AM** (22 min from open). On average only **49% of the half-threshold** was reached. For the 26 that "Worked and Remained," the peaks tend to come **later** and reach **deeper** — grinding selloffs that stay mildly negative without real momentum.

### Recent Examples (2025-2026) with Timing

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Peak Time | % of Threshold |
|------|-----|-----|------:|------:|------:|:----------:|------:|
| 2025-05-28 | Bearish | Mildly Bearish | 1.17% | -0.38% | **-0.30%** | 10:15 | 65.6% |
| 2025-11-28 | Mildly Bearish | Bearish | 0.74% | -0.25% | **-0.13%** | 9:15 | 67.0% |
| 2026-03-12 | Strong Bearish | Strong Bearish | 1.33% | -0.50% | **-0.15%** | 9:15 | 75.3% |
| 2026-04-23 | Strong Bearish | Strong Bearish | 1.15% | -0.28% | **-0.19%** | 9:15 | 48.5% |
| 2026-05-08 | Bearish | Strong Bearish | 1.05% | -0.44% | **-0.22%** | 14:00 | 84.2% |
| 2026-07-15 | Bearish | Bearish | 0.87% | -0.31% | **-0.05%** | 12:55 | 72.0% |
| 2026-07-21 | Bearish | Strong Bearish | 0.82% | -0.33% | **-0.09%** | 13:00 | 81.0% |

### Classic Examples with Timing

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Peak Time | % of Threshold |
|------|-----|-----|------:|------:|------:|:----------:|------:|
| 2021-10-07 | Mildly Bearish | Strong Bearish | 1.09% | -0.25% | **-0.08%** | 9:20 | 45.9% |
| 2021-11-17 | Bearish | Strong Bearish | 0.96% | -0.33% | **-0.29%** | 15:25 | 69.0% |
| 2022-04-06 | Bearish | Strong Bearish | 1.16% | -0.35% | **-0.24%** | 10:40 | 60.5% |
| 2023-08-18 | Bearish | Strong Bearish | 0.77% | -0.25% | **-0.10%** | 10:45 | 64.7% |
| 2023-10-16 | Strong Bearish | Strong Bearish | 0.67% | -0.23% | **-0.03%** | 9:20 | 68.7% |

### Near Misses (Almost Crossed — Still Worked)

| Date | VIX Predicted% | Half Threshold | Peak Move% | % Reached | Peak Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2024-10-16 | 0.82% | 0.41% | 0.400% | 97.6% | 11:45 | **-0.19%** |
| 2023-08-25 | 0.74% | 0.37% | 0.346% | 93.5% | 10:30 | **-0.28%** |
| 2026-05-08 | 1.05% | 0.525% | 0.442% | 84.2% | 14:00 | **-0.22%** |

Near misses that "worked" tend to have deeper selling spread over a longer period — the deepest point comes in late morning or afternoon rather than the opening session.

### Walkthrough: 2026-03-12

```
Setup:
  FII View:  Strong Bearish   PRO View: Strong Bearish  → Strong Bearish Alignment
  VIX Open:  21.06             Predicted Range: 1.33%
  Half Threshold: 1.33% / 2 = 0.665%

Intraday:
  High from Open:  +0.67%  → Nearly hit the upside threshold instead
  Low from Open:   -0.50%  → Did NOT reach -0.665% ✗
  Close from Open: -0.15%  → Barely negative

Timing:
  Bearish peak at 9:15 AM (0 min) — reached 75.3% of threshold
  Reversal at 9:55 AM — price rose above open within 40 min
  But it came back negative by close — weak, choppy day

Result: Reversed Before Half + Worked and Remained
  Despite Strong Bearish Alignment, close of -0.15% lacks conviction.
  Range was only 1.17% vs 1.33% predicted.
```

### Pattern in These Days

- Average close was only **-0.16%** — barely negative
- Low% was well inside the VIX half-threshold (by definition)
- On average, reached **65% of threshold** — closer than the broader group but still short
- These tend to be "Top to Down" days with weak selling
- Elevated VIX environments contribute: the threshold is harder to reach when VIX is high
- Only 26 out of 140 "Reversed Before Half" days (18.6%) — this quadrant is rare

---

## Quadrant 4: Reversed Before Half + Reversed by Close (114 days, 81.4% of Reversed Before Half)

**The dominant bullish outcome.** When the bearish move fails to reach even half the VIX threshold, the market closes bullish 81.4% of the time. This is the largest group within "Reversed Before Half."

### Timing: How Early Is the Failure Apparent?

On these 114 days, the bearish low peaked at a **median of 9:37 AM** — selling exhausted within the first 22 minutes. The reversal (price rises above open) came at a **median of 9:50 AM** — within 35 minutes.

**The First Hour Rule**: If the bearish low peaks by 10:15 AM and hasn't crossed the threshold → **89% chance of bullish close.**

### Recent Examples (2025-2026) with Timing

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Peak Time | % of Threshold | Reversal |
|------|-----|-----|------:|------:|------:|:----------:|------:|:----------:|
| 2025-01-14 | Strong Bearish | Bearish | 1.01% | -0.14% | **+0.18%** | 10:15 | 27.1% | 10:35 |
| 2025-01-31 | Strong Bearish | Strong Bearish | 1.10% | -0.08% | **+1.02%** | 9:15 | 15.1% | 9:20 |
| 2025-04-07 | Bearish | Bearish | 0.87% | -0.07% | **+2.20%** | 9:15 | 15.6% | 9:20 |
| 2025-05-07 | Mildly Bearish | Mildly Bearish | 1.20% | -0.05% | **+0.73%** | 9:15 | 9.2% | 9:20 |
| 2025-05-23 | Bearish | Strong Bearish | 1.09% | -0.10% | **+0.83%** | 9:15 | 18.9% | 9:20 |
| 2025-06-13 | Bearish | Strong Bearish | 0.88% | +0.00% | **+1.07%** | 9:15 | 0.0% | 9:20 |
| 2025-07-23 | Mildly Bearish | Strong Bearish | 0.68% | -0.21% | **+0.28%** | 9:45 | 62.9% | 12:00 |
| 2025-08-04 | Bearish | Strong Bearish | 0.75% | -0.17% | **+0.53%** | 9:45 | 45.6% | 9:50 |
| 2025-08-11 | Bearish | Strong Bearish | 0.76% | -0.10% | **+0.78%** | 9:15 | 26.1% | 9:20 |
| 2025-09-16 | Mildly Bearish | Strong Bearish | 0.66% | -0.01% | **+0.72%** | 9:15 | 3.9% | 9:20 |

Notice: most examples peaked at **9:15 AM** (the opening candle) with reversal at **9:20 AM**. The bearish view was dead within 5 minutes.

### Zero Momentum Days (Low% = 0)

| Date | VIX Predicted% | Close% |
|------|------:|------:|
| 2022-09-05 | 1.23% | **+0.61%** |
| 2022-09-07 | 1.23% | **+0.63%** |
| 2022-11-28 | 0.84% | **+0.67%** |
| 2025-06-13 | 0.88% | **+1.07%** |
| 2026-06-02 | 1.04% | **+1.27%** |

These days gapped up on the open — zero bearish attempt at all. The bearish alignment was completely overridden by bullish price action from the first candle.

### Near Misses That Still Reversed

| Date | VIX Predicted% | Half Threshold | Peak Move% | % Reached | Peak Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2023-08-23 | 0.74% | 0.37% | 0.372% | 100.5% | 9:55 | **+0.01%** |
| 2026-02-02 | 0.95% | 0.475% | 0.472% | 99.4% | 11:25 | **+1.14%** |
| 2024-10-18 | 0.84% | 0.42% | 0.394% | 93.8% | 9:25 | **+0.80%** |

Even days that came within 1% of the threshold still reversed bullish.

### Walkthrough: 2025-04-07

```
Setup:
  FII View:  Bearish         PRO View: Bearish  → Strong Bearish Alignment
  VIX Open:  13.76            Predicted Range: 0.87%
  Half Threshold: 0.87% / 2 = 0.435%

Intraday:
  High from Open:  +2.28%  → Massive rally
  Low from Open:   -0.07%  → Barely any downside — didn't reach 0.435% ✗
  Close from Open: +2.20%  → Closed near the highs, a huge bullish day

Timing:
  Bearish peak at 9:15 AM (0 min) — opening candle was the low
  Reversal at 9:20 AM — within 5 minutes, price was above open
  Only reached 15.6% of the half-threshold
  → Failure was obvious within 5 minutes of the open.

Result: Reversed Before Half + Reversed by Close
  Despite Strong Bearish Alignment, the market surged +2.20%.
  The bearish view never even got started.
```

### Walkthrough: 2025-01-31

```
Setup:
  FII View:  Strong Bearish   PRO View: Strong Bearish  → Strong Bearish Alignment
  VIX Open:  17.39             Predicted Range: 1.10%
  Half Threshold: 1.10% / 2 = 0.55%

Intraday:
  High from Open:  +1.07%  → Strong rally
  Low from Open:   -0.08%  → Almost zero downside — nowhere near 0.55% ✗
  Close from Open: +1.02%  → Closed near highs

Timing:
  Bearish peak at 9:15 AM — reached only 15.1% of threshold
  Reversal at 9:20 AM — price above open within 5 minutes
  → Both FII and PRO were Strong Bearish, yet the market rallied +1.02%.

Result: Reversed Before Half + Reversed by Close
```

### Classic Examples

| Date | FII | PRO | VIX Predicted% | High% | Low% | Close% |
|------|-----|-----|------:|------:|------:|------:|
| 2021-03-01 | Bearish | Strong Bearish | 1.77% | +0.71% | -0.43% | **+0.56%** |
| 2021-05-03 | Mildly Bearish | Bearish | 1.45% | +1.33% | -0.44% | **+1.13%** |
| 2021-09-02 | Mildly Bearish | Strong Bearish | 0.89% | +0.88% | -0.19% | **+0.81%** |
| 2021-12-07 | Bearish | Strong Bearish | 1.26% | +1.22% | -0.32% | **+0.80%** |

### Pattern in These Days

- All have **"Down to Up"** move direction — the market went against the bearish view from the start
- **Bearish peak at median 9:37 AM** — selling exhausted in the first 22 minutes
- **Reversal by 9:50 AM** — price rises above open within 35 minutes
- On average, only **15-27% of the half-threshold** was reached
- High% is often substantial (+0.50% to +2.28%) — real bullish momentum
- Low% is typically < -0.10% — barely any downside at all
- Average close was **+0.36%** — a meaningful bullish day
- **First Hour Rule**: if peak by 10:15 AM and no threshold cross → **89% close bullish**
- This is the **earliest inverse signal**: if the market can't drop past half the VIX range in the bearish direction by the first hour, it's almost certainly closing green

---

## Year-by-Year Distribution

### Exceeded Half then Reversed (153 days total)

| Year | Count | Worked and Remained | WR% |
|------|------:|--------------------:|----:|
| 2020 | 4 | 0 | 0% |
| 2021 | 18 | 16 | 89% |
| 2022 | 31 | 28 | 90% |
| 2023 | 36 | 33 | 92% |
| 2024 | 25 | 19 | 76% |
| 2025 | 25 | 24 | 96% |
| 2026 | 14 | 9 | 64% |

**Note**: 2020 is an outlier with 0% WR (only 4 days, all in the Elevated VIX regime during COVID recovery). 2025 had the highest WR at 96%.

### Reversed Before Half (140 days total)

| Year | Count | Reversed by Close | Rev% |
|------|------:|------------------:|-----:|
| 2020 | 3 | 3 | 100% |
| 2021 | 13 | 11 | 85% |
| 2022 | 23 | 21 | 91% |
| 2023 | 25 | 21 | 84% |
| 2024 | 34 | 27 | 79% |
| 2025 | 21 | 16 | 76% |
| 2026 | 21 | 15 | 71% |

---

## VIX Regime Breakdown (Exceeded Half Only)

| VIX Regime | Count | % of Exceeded Half |
|------------|------:|-------------------:|
| Low (<15) | 93 | 60.8% |
| Normal (15-20) | 38 | 24.8% |
| Elevated (20-30) | 22 | 14.4% |

Same pattern as bullish: most "Exceeded Half" days occur in Low VIX. The half-threshold is smaller in absolute terms and easier to cross.

---

## Expiry Day Performance (Exceeded Half + Bearish Alignment)

42 of 153 "Exceeded Half" days were expiry days. Of these:

| Expiry? | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Expiry | 42 | 34 | **81.0%** |
| Non-Expiry | 111 | 95 | **85.6%** |

Unlike bullish alignment (where expiry boosted WR%), bearish alignment shows slightly lower WR% on expiry days. This may reflect short-covering rallies on expiry that can reverse bearish momentum.

### Expiry Day Examples (Exceeded Half + Bearish)

| Date | FII | PRO | VIX | Low% | Close% | Cross Time | Outcome |
|------|-----|-----|----:|------:|------:|:----------:|---------|
| 2021-03-25 | Mildly Bearish | Strong Bearish | 22.46 | -2.10% | **-1.54%** | 9:20 | Worked |
| 2021-10-28 | Bearish | Strong Bearish | 16.83 | -2.13% | **-1.79%** | 9:35 | Worked |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 24.54 | -2.08% | **-2.00%** | 13:40 | Worked |
| 2022-05-26 | Mildly Bearish | Strong Bearish | 25.28 | -1.25% | **+0.60%** | 10:25 | Failed |
| 2023-01-25 | Mildly Bearish | Strong Bearish | 13.66 | -1.36% | **-1.01%** | 9:45 | Worked |
| 2024-09-12 | Mildly Bearish | Strong Bearish | 13.63 | -0.47% | **+1.02%** | 11:25 | Failed |
| 2024-10-17 | Strong Bearish | Strong Bearish | 13.05 | -1.19% | **-1.11%** | 9:25 | Worked |
| 2025-01-09 | Bearish | Bearish | 14.47 | -0.73% | **-0.50%** | 10:45 | Worked |
| 2025-08-07 | Bearish | Mildly Bearish | 11.96 | -0.49% | **+0.66%** | 13:20 | Failed |
| 2026-02-24 | Mildly Bearish | Strong Bearish | 14.17 | -1.23% | **-0.71%** | 9:30 | Worked |
| 2026-05-12 | Bearish | Mildly Bearish | 18.55 | -1.58% | **-1.23%** | 11:05 | Worked |

---

## Practical Interpretation

```
IF   Bearish Alignment (FII + PRO both bearish, known T+1)
AND  Intraday low exceeds half the VIX-predicted range
THEN 84.3% chance market closes bearish (avg -0.45%)

IF   Bearish Alignment
AND  Intraday low does NOT reach half the VIX-predicted range
THEN 81.4% chance market closes bullish (avg +0.36%)
```

### Timing Rule of Thumb

```
EXCEEDED HALF (153 days):
  Median cross time: 10:25 AM (70 min from open)
  - 29% cross in the opening session (9:15-9:44) → 82% WR
  - 52% cross by 10:30 AM
  - 73% cross by 12:30 PM
  - Afternoon crosses (12:30+) → 93-100% WR (committed selloff)
  - DANGER ZONE: Late morning (10:30-11:30) → only 62% WR
  - FAILURE PATTERN: 71% of failures crossed BEFORE 10:45 AM

REVERSED BEFORE HALF (139 days):
  Median bearish peak: 9:37 AM (22 min from open)
  Median reversal (price above open): 9:50 AM (35 min)
  Average threshold reached: only 49%
  - If peak by 10:15 AM & no threshold cross → 89% close BULLISH
  - Most failures peak at 9:15 AM (opening candle = day's low)
  - Near misses that still worked peaked LATER (10:30-14:00)
  - 50% of deepest points occur in the opening session (9:15-9:44)
```

### Bearish vs Bullish: Key Differences

| Characteristic | Bullish Alignment | Bearish Alignment |
|---------------|:-:|:-:|
| Exceeded Half frequency | 29.8% | **52.2%** |
| Exceeded Half WR% | **90.6%** | 84.3% |
| Failure cases | 8 (9.4%) | 24 (15.7%) |
| Exceeded Half: median cross | 11:37 AM | **10:25 AM** |
| Exceeded Half: % by 10:30 | 34% | **52%** |
| Exceeded Half: lowest WR session | Early AM (83%) | **Late Morning (62%)** |
| Reversed Before Half WR% | 27.0% | 18.6% |
| Rev Before Half: median peak | 9:52 AM | **9:37 AM** |
| Rev Before Half: median reversal | 9:30 AM | 9:50 AM |
| Rev Before Half: % threshold reached | 42% | 49% |
| Rev Before Half: peak by 10:15 → loss | **92%** | 89% |
| Expiry boost | Yes (+5.3%) | No (-4.6%) |

**Bearish alignment is more likely to cross the VIX threshold** (52% vs 30%) because selloffs tend to be sharper and more momentum-driven than rallies. However, the **WR% is lower** (84% vs 91%) because bearish moves are also more prone to V-shaped recoveries — especially when the threshold is crossed in the opening 30 minutes via a gap-down.

**"Reversed Before Half" days are detectable early** — on both bullish and bearish alignment days, the failure is usually apparent within the first 30 minutes. If the aligned move peaks by 10:15 AM without crossing the threshold, there's an ~89-92% chance the market closes against the alignment.

**Caveat**: FII/PRO alignment is only known after T+1 settlement. This analysis identifies historical patterns, not real-time signals. The VIX half-threshold *is* observable intraday, but the alignment condition is not.
