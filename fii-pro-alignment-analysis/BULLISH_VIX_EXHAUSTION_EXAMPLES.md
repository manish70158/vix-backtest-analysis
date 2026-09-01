# Bullish Alignment + VIX Half-Range Exhaustion: Detailed Examples

> **Context**: When both FII and PRO are bullish (T+1 data), we check whether
> the market's upward move exceeded half the VIX-predicted daily range before
> any reversal. This document walks through real examples from all four outcome
> quadrants.

---

## How It Works

1. **FII and PRO both bullish** (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the bullish move (high from open) exceed that half threshold?

```
VIX Predicted Range = 0.86%
Half Threshold      = 0.43%
Intraday High%      = 0.60%  ← Exceeded 0.43% → "Exceeded Half"

vs.

VIX Predicted Range = 1.30%
Half Threshold      = 0.65%
Intraday High%      = 0.15%  ← Did NOT reach 0.65% → "Reversed Before Half"
```

---

## Summary Table (285 Bullish Alignment Days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 85 | 29.8% | 77 | **90.6%** | +0.59% |
| Reversed Before Half | 200 | 70.2% | 54 | **27.0%** | -0.36% |

**Key takeaway**: If the bullish move exceeded half the VIX range, the market closed bullish 90.6% of the time. If it didn't reach that level, the market closed bearish 73% of the time.

---

## When Does the Threshold Get Crossed? (5-Minute Candle Analysis)

Using 5-minute candle data from PostgreSQL, we identified the **exact time** each day's bullish high first crossed the VIX half-threshold.

### Bullish Alignment Timing Summary (86 Exceeded Half days)

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **11:37 AM** | 142 min |
| Average | 11:46 AM | 152 min |
| 25th percentile | 10:03 AM | 49 min |
| 75th percentile | 1:08 PM | 234 min |
| Earliest | 9:15 AM | 0 min |
| Latest | 3:25 PM | 370 min |

### Session Distribution

| Session | Count | % | WR% |
|---------|------:|--:|----:|
| Opening (9:15-9:44) | 17 | 19.8% | 94.1% |
| Early Morning (9:45-10:29) | 12 | 14.0% | 83.3% |
| Late Morning (10:30-11:29) | 13 | 15.1% | 92.3% |
| Midday (11:30-12:29) | 15 | 17.4% | 86.7% |
| Early Afternoon (12:30-13:29) | 10 | 11.6% | 100.0% |
| Late Afternoon (13:30-14:29) | 10 | 11.6% | 80.0% |
| Closing (14:30-15:30) | 9 | 10.5% | 100.0% |

**Key insight**: Bullish rallies build gradually — only 34% cross before 10:30 AM. The distribution is spread across the full session. Afternoon crosses (12:30+) have near-perfect WR% because by then the market has committed.

### VIX Regime Timing

| VIX Regime | Avg Cross Time | Median Cross Time |
|------------|:--------------:|:-----------------:|
| Low (<15) | 11:56 AM | 11:45 AM |
| Normal (15-20) | 11:12 AM | 11:02 AM |
| Elevated (20-30) | 12:17 PM | 12:35 PM |

Higher VIX = wider threshold = takes longer to cross on average.

---

## Quadrant 1: Exceeded Half + Worked and Remained (77 days, 90.6% of Exceeded Half)

**This is the high-conviction bullish outcome.** The market moved up past the VIX half-threshold and held those gains by close.

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
  The market rallied well past the VIX threshold and held.
  This was an expiry day — extra conviction.
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
  Despite a -0.81% dip, the market recovered and closed +1.38%.
  The high of +1.71% far exceeded the VIX half-threshold.
```

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

---

## Quadrant 2: Exceeded Half + Reversed by Close (8 days, 9.4% of Exceeded Half)

**The rare failure case.** The market exceeded the VIX half-threshold to the upside but then completely reversed and closed bearish. Only 8 out of 85 times.

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
  FII View:  Bullish     PRO View: Bullish  → Strong Bullish Alignment
  VIX Open:  20.83       Predicted Range: 1.31%
  Half Threshold: 1.31% / 2 = 0.655%

Intraday:
  High from Open:  +1.60%  → Exceeded 0.655% ✓ (moved up strongly first)
  Low from Open:   -0.69%  → Then collapsed into negative territory
  Close from Open: -0.45%  → Closed bearish despite strong first-half rally

Timing:
  Threshold crossed at 9:20 AM (5 min from open!)
  → Gap-up opening exceeded the threshold immediately on the first candle.
    The rally was front-loaded and unsustainable — classic morning trap.

Result: Exceeded Half + Reversed by Close ✗
  Classic "Top to Down" pattern. Market rallied 1.6% then gave it all back.
  Wide range of 2.29% shows extreme intraday volatility.
```

### Pattern in the Failures

- All 8 had a "Top to Down" move direction — the bullish move came **first** and then reversed
- **Timing pattern**: 5 of 8 crossed before 12:00 PM — the early bullish spike faded
- Cross times: 9:20, 9:45, 10:00, 10:50, 11:40, 11:55, 13:30, 13:40
- Most had relatively moderate VIX (Low or Normal regime)
- 7 of 8 were non-expiry days
- The average close was only -0.36% — the reversals weren't devastating

---

## Quadrant 3: Reversed Before Half + Worked and Remained (54 days, 27.0% of Reversed Before Half)

**The grinding win.** The market never exceeded the VIX half-threshold to the upside, yet still managed to close bullish. These are low-conviction, narrow-range bullish days.

### Timing: When Did the Bullish Move Peak?

Across all 199 "Reversed Before Half" bullish days, the high peaked at a **median of 9:52 AM** (38 min from open). On average only **42% of the half-threshold** was reached. For the 54 that "Worked and Remained," the peaks tend to come **later** (afternoon) — slow grinding rallies that never built enough momentum to cross.

### Examples with Timing

| Date | FII | PRO | VIX Predicted% | High% | Close% | Peak Time | % of Threshold |
|------|-----|-----|------:|------:|------:|:----------:|------:|
| 2020-09-11 | Mildly Bullish | Strong Bullish | 1.34% | +0.39% | **+0.06%** | 9:25 | 58.5% |
| 2021-01-11 | Mildly Bullish | Mildly Bullish | 1.30% | +0.15% | **+0.06%** | 15:20 | 23.8% |
| 2021-03-02 | Mildly Bullish | Mildly Bullish | 1.61% | +0.63% | **+0.51%** | 15:25 | 78.3% |
| 2021-05-18 | Bullish | Strong Bullish | 1.24% | +0.46% | **+0.28%** | 13:40 | 74.8% |

### Near Misses (Almost Crossed the Threshold)

| Date | VIX Predicted% | Half Threshold | Peak Move% | % Reached | Peak Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2025-12-12 | 0.66% | 0.33% | 0.333% | 100.9% | 15:10 | **+0.28%** |
| 2024-05-14 | 1.30% | 0.65% | 0.649% | 99.8% | 14:05 | **+0.44%** |
| 2021-10-12 | 1.01% | 0.505% | 0.501% | 99.2% | 15:15 | **+0.50%** |
| 2021-09-03 | 0.90% | 0.45% | 0.446% | 99.1% | 15:20 | **+0.34%** |

Near misses that "Worked and Remained" tend to peak **late afternoon** (14:00-15:30) — the rally builds all day, just barely falls short of the threshold, but still closes positive.

### Walkthrough: 2020-09-11

```
Setup:
  FII View:  Mildly Bullish   PRO View: Strong Bullish  → Bullish Alignment
  VIX Open:  21.26             Predicted Range: 1.34%
  Half Threshold: 1.34% / 2 = 0.67%

Intraday:
  High from Open:  +0.39%  → Did NOT reach 0.67% ✗
  Low from Open:   -0.24%  → Modest dip
  Close from Open: +0.06%  → Barely positive close

Timing:
  Bullish peak at 9:25 AM (10 min) — reached 58.5% of threshold
  Reversal at 9:45 AM — price dropped below open within 30 min
  But then recovered to close barely positive (+0.06%)

Result: Reversed Before Half + Worked and Remained
  The bullish view "won" by close, but just barely (+0.06%).
  This is a low-quality win.
```

### Pattern in These Days

- Average close was only +0.16% — barely positive
- High% was well below the VIX half-threshold (that's the definition)
- On average, only 42% of the threshold was reached
- Near misses that worked tend to peak in the **afternoon** (slow grind higher)
- High VIX environments (Elevated regime) are overrepresented — the threshold is harder to reach

---

## Quadrant 4: Reversed Before Half + Reversed by Close (146 days, 73.0% of Reversed Before Half)

**The dominant bearish outcome.** When the bullish move fails to reach even half the VIX threshold, the market closes bearish 73% of the time. This is the largest group.

### Timing: How Early Is the Failure Apparent?

On these 146 days, the bullish high peaked at a **median of 9:15 AM** — the opening candle was often the day's best bullish attempt. The reversal (price drops below open) came at a **median of 9:20-9:30 AM** — within 5-15 minutes.

**The First Hour Rule**: If the bullish high peaks by 10:15 AM and hasn't crossed the threshold → **92% chance of bearish close.**

### Recent Examples (2025-2026)

| Date | FII | PRO | VIX Predicted% | High% | Close% | Peak Time | % of Threshold | Reversal |
|------|-----|-----|------:|------:|------:|:----------:|------:|:----------:|
| 2025-01-03 | Bullish | Strong Bullish | 0.87% | +0.00% | **-0.85%** | 9:15 | 0.0% | 9:20 |
| 2025-01-21 | Mildly Bullish | Strong Bullish | 1.03% | +0.02% | **-1.57%** | 9:15 | 3.9% | 9:20 |
| 2025-02-05 | Strong Bullish | Strong Bullish | 0.88% | +0.02% | **-0.48%** | 9:15 | 5.2% | 9:20 |
| 2025-05-06 | Mildly Bullish | Bullish | 1.16% | +0.04% | **-0.67%** | 9:15 | 6.2% | 9:20 |
| 2025-06-09 | Bullish | Strong Bullish | 0.92% | +0.00% | **-0.23%** | 9:15 | 0.0% | 9:20 |
| 2025-07-22 | Mildly Bullish | Strong Bullish | 0.71% | +0.06% | **-0.40%** | 9:15 | 17.2% | 9:20 |
| 2025-07-24 | Bullish | Strong Bullish | 0.66% | +0.01% | **-0.76%** | 9:15 | 3.6% | 9:20 |
| 2025-08-05 | Bullish | Strong Bullish | 0.75% | +0.05% | **-0.29%** | 9:15 | 13.9% | 9:20 |
| 2025-08-26 | Mildly Bullish | Strong Bullish | 0.74% | +0.08% | **-0.76%** | 9:15 | 21.9% | 9:20 |
| 2025-09-04 | Bullish | Strong Bullish | 0.69% | +0.00% | **-0.96%** | 9:15 | 0.0% | 9:20 |
| 2025-11-18 | Mildly Bullish | Bullish | 0.74% | +0.03% | **-0.49%** | 9:15 | 8.4% | 9:20 |

Notice: nearly every example peaked at **9:15 AM** (the opening candle) with the reversal at **9:20 AM**. The bullish view was dead within 5 minutes.

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
  FII View:  Mildly Bullish   PRO View: Strong Bullish  → Bullish Alignment
  VIX Open:  16.42             Predicted Range: 1.03%
  Half Threshold: 1.03% / 2 = 0.515%

Intraday:
  High from Open:  +0.02%  → Barely moved up at all! Nowhere near 0.515%
  Low from Open:   -1.90%  → Massive selloff
  Close from Open: -1.57%  → Closed deep in the red

Timing:
  Bullish peak at 9:15 AM (0 min) — opening candle was the high
  Reversal at 9:20 AM — within 5 minutes, price was below open
  Only reached 3.9% of the half-threshold
  → Failure was obvious within 5 minutes of the open.

Result: Reversed Before Half + Reversed by Close
  FII and PRO were both bullish, but the market opened and immediately sold off.
  The high of +0.02% means there was essentially zero upside momentum all day.
```

### Walkthrough: 2025-09-04

```
Setup:
  FII View:  Bullish          PRO View: Strong Bullish  → Strong Bullish Alignment
  VIX Open:  10.93             Predicted Range: 0.69%
  Half Threshold: 0.69% / 2 = 0.345%

Intraday:
  High from Open:  +0.00%  → Zero upside! Opened at the high
  Low from Open:   -1.09%  → Sold off hard (1.09% > VIX predicted 0.69%)
  Close from Open: -0.96%  → Closed near the lows

Timing:
  Bullish peak at 9:15 AM — zero upside, 0% of threshold reached
  Reversal at 9:20 AM — gap-down open, never looked back
  → The actual range (1.09%) exceeded VIX prediction (0.69%)

Result: Reversed Before Half + Reversed by Close
  Even with Strong Bullish Alignment and low VIX, the market went straight down.
```

### Pattern in These Days

- Most have "Top to Down" move direction — market opened, tried to go up, failed immediately
- **Bullish peak at median 9:15 AM** — the opening candle is the high of the day
- **Reversal by 9:20 AM** — price drops below open within 5 minutes
- High% is typically < 0.10% — almost no upside momentum at all
- On average, only **6-20% of the half-threshold** was reached
- Average close was -0.36% — not catastrophic but consistently bearish
- **First Hour Rule**: if peak by 10:15 AM and no threshold cross → **92% close bearish**
- This is the **earliest warning signal**: if the market can't rally past half the VIX range in the bullish direction by the first hour, it's almost certainly closing red

---

## Year-by-Year Distribution

### Exceeded Half then Reversed (85 days total)

| Year | Count | Worked and Remained | WR% |
|------|------:|--------------------:|----:|
| 2020 | 5 | 5 | 100% |
| 2021 | 12 | 11 | 92% |
| 2022 | 9 | 8 | 89% |
| 2023 | 16 | 16 | 100% |
| 2024 | 15 | 14 | 93% |
| 2025 | 20 | 18 | 90% |
| 2026 | 8 | 5 | 63% |

### Reversed Before Half (200 days total)

| Year | Count | Reversed by Close | Rev% |
|------|------:|------------------:|-----:|
| 2020 | 2 | 1 | 50% |
| 2021 | 24 | 16 | 67% |
| 2022 | 34 | 25 | 74% |
| 2023 | 51 | 38 | 75% |
| 2024 | 41 | 32 | 78% |
| 2025 | 24 | 15 | 63% |
| 2026 | 24 | 19 | 79% |

---

## VIX Regime Breakdown (Exceeded Half Only)

| VIX Regime | Count | % of Exceeded Half |
|------------|------:|-------------------:|
| Low (<15) | 51 | 60.0% |
| Normal (15-20) | 24 | 28.2% |
| Elevated (20-30) | 10 | 11.8% |

Most "Exceeded Half" days occur in Low VIX environments. This makes sense: when VIX is low, the half-threshold is smaller and easier to exceed.

---

## Expiry Day Performance (Exceeded Half + Bullish Alignment)

19 of 85 "Exceeded Half" days were expiry days. Of these:

| Expiry? | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Expiry | 19 | 18 | **94.7%** |
| Non-Expiry | 66 | 59 | **89.4%** |

Expiry days show slightly higher conviction when the VIX half-threshold is exceeded.

### All Expiry Day Examples (Exceeded Half + Bullish)

| Date | FII | PRO | VIX | High% | Close% | Cross Time |
|------|-----|-----|----:|------:|------:|:----------:|
| 2021-09-16 | Bullish | Strong Bullish | 13.73 | +0.60% | **+0.50%** | 14:15 |
| 2021-12-02 | Bullish | Strong Bullish | 19.45 | +1.36% | **+1.27%** | 10:15 |
| 2022-03-17 | Bullish | Strong Bullish | 24.12 | +0.82% | **+0.56%** | 14:05 |
| 2022-07-28 | Strong Bullish | Strong Bullish | 18.13 | +1.01% | **+0.88%** | 11:05 |
| 2023-04-27 | Bullish | Strong Bullish | 11.65 | +0.66% | **+0.62%** | 13:30 |
| 2023-06-28 | Bullish | Strong Bullish | 10.78 | +0.54% | **+0.44%** | 12:00 |
| 2023-07-20 | Bullish | Strong Bullish | 11.60 | +0.81% | **+0.70%** | 13:15 |
| 2024-04-25 | Bullish | Mildly Bullish | 10.28 | +1.38% | **+1.09%** | 9:35 |
| 2024-05-23 | Bullish | Strong Bullish | 21.47 | +1.68% | **+1.49%** | 11:55 |
| 2025-01-02 | Bullish | Mildly Bullish | 14.51 | +1.87% | **+1.62%** | 10:35 |
| 2025-01-23 | Strong Bullish | Mildly Bullish | 16.77 | +0.62% | **+0.38%** | 12:15 |
| 2025-01-30 | Mildly Bullish | Bullish | 18.64 | +0.66% | **+0.55%** | 10:20 |
| 2025-04-03 | Bullish | Strong Bullish | 13.72 | +0.67% | **+0.39%** | 9:20 |
| 2025-05-15 | Mildly Bullish | Strong Bullish | 17.23 | +1.71% | **+1.38%** | 13:05 |
| 2025-06-05 | Mildly Bullish | Bullish | 15.75 | +0.85% | **+0.28%** | 12:05 |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | 12.96 | +1.17% | **+1.03%** | 9:30 |
| 2025-09-02 | Strong Bullish | Bullish | 11.29 | +0.42% | **-0.32%** | 10:00 |
| 2026-02-17 | Bullish | Strong Bullish | 13.33 | +0.49% | **+0.30%** | 11:35 |
| 2026-04-13 | Bullish | Bullish | 18.85 | +1.35% | **+0.97%** | 10:25 |

Only 2025-09-02 reversed by close — the sole expiry failure (crossed at 10:00 AM, early cross that didn't hold).

---

## Practical Interpretation

```
IF   Bullish Alignment (FII + PRO both bullish, known T+1)
AND  Intraday high exceeds half the VIX-predicted range
THEN 90.6% chance market closes bullish (avg +0.59%)

IF   Bullish Alignment
AND  Intraday high does NOT reach half the VIX-predicted range
THEN 73.0% chance market closes bearish (avg -0.36%)
```

### Timing Rule of Thumb

```
EXCEEDED HALF (86 days):
  Median cross time: 11:37 AM (142 min from open)
  - 20% cross in the opening session (9:15-9:44) → 94% WR
  - 34% cross by 10:30 AM
  - 66% cross by 12:30 PM
  - Afternoon crosses (12:30+) → 90-100% WR (market committed)

REVERSED BEFORE HALF (199 days):
  Median bullish peak: 9:52 AM (38 min from open)
  Median reversal (price below open): 9:30 AM (15 min)
  Average threshold reached: only 42%
  - If peak by 10:15 AM & no threshold cross → 92% close BEARISH
  - Most failures peak at 9:15 AM (opening candle = day's high)
  - Near misses that still worked peaked in AFTERNOON (14:00-15:30)
```

**The VIX half-range threshold acts as a momentum confirmation filter:**
- Exceeding it confirms the aligned bullish view has market support
- Failing to reach it signals the bullish alignment is not translating into price action
- **Early morning crosses (before 10:00)** tend to be gap-up days — if they hold, they hold strongly (94% WR)
- **Afternoon crosses** are the safest — by then the market has shown sustained buying
- **"Reversed Before Half" days are detectable early** — the failure is usually apparent within the first 15-30 minutes

**Caveat**: FII/PRO alignment is only known after T+1 settlement. This analysis identifies historical patterns, not real-time signals. The VIX half-threshold *is* observable intraday, but the alignment condition is not.
