# Reversed Before Half: Timing Analysis

> On days when the aligned move NEVER reached half the VIX-predicted range,
> when did the market reach its deepest point before reversing?
> And when did the reversal become apparent (price crossing back past open)?

## Bearish Alignment — Reversed Before Half (139 days)

The bearish low from open never crossed the VIX half-threshold.

### When Did the Aligned Move Reach Its Deepest Point?

This is the candle where the running high (bullish) or running low (bearish)
hit its maximum — the closest it ever got to the threshold before fading.

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **9:30** | 15 min |
| Average | 10:39 | 84 min |
| 25th percentile | 9:15 | 0 min |
| 75th percentile | 11:11 | 116 min |
| Earliest | 9:15 | 0 min |
| Latest | 18:50 | 575 min |

### How Close Did They Get to the Threshold?

| Statistic | % of Half-Threshold Reached |
|-----------|---------------------------:|
| Average | 54.2% |
| Median | 58.2% |
| < 25% of threshold | 29 days (20.9%) |
| 25-50% of threshold | 28 days (20.1%) |
| 50-75% of threshold | 42 days (30.2%) |
| 75-100% of threshold | 40 days (28.8%) |

### Deepest Point Session Distribution

| Session | Count | % | Avg % of Threshold Reached |
|---------|------:|--:|---------------------------:|
| Opening (9:15-9:44) | 74 | 53.2% | 51.2% |
| Early Morning (9:45-10:29) | 14 | 10.1% | 63.2% |
| Late Morning (10:30-11:29) | 12 | 8.6% | 71.6% |
| Midday (11:30-12:29) | 4 | 2.9% | 73.4% |
| Early Afternoon (12:30-13:29) | 9 | 6.5% | 72.0% |
| Late Afternoon (13:30-14:29) | 8 | 5.8% | 68.3% |
| Closing (14:30-15:30) | 11 | 7.9% | 46.7% |

### When Did the Reversal Become Apparent?

The reversal point is when the close of a 5-min candle crosses back past the open price
(bullish: drops below open; bearish: rises above open) after the deepest point.

- **125** days (89.9%): price crossed back past open (clear reversal)
- **14** days (10.1%): price never crossed back past open (aligned direction held weakly)

#### Reversal Timing (price crosses back past open)

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **9:45** | 30 min |
| Average | 10:36 | 81 min |
| 25th percentile | 9:20 | 5 min |
| 75th percentile | 11:10 | 115 min |

#### Time from Deepest Point to Reversal

| Statistic | Minutes |
|-----------|--------:|
| Average gap | 25 min |
| Median gap | 10 min |

### Close Outcome by Deepest Point Timing

If the deepest aligned-direction move happens early and is shallow,
what's the probability the market reverses by close?

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Before 11:15 AM | 100 | 87 | 87.0% | 13 | 13.0% |
| After 11:15 AM | 32 | 20 | 62.5% | 12 | 37.5% |

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Within first hour (by 10:15) | 87 | 78 | 89.7% | 9 | 10.3% |
| After first hour | 45 | 29 | 64.4% | 16 | 35.6% |

### Examples: Shallowest Moves (Least Momentum)

Days where the aligned move barely got started:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2022-09-05 | 1.02% | 0.51% | 0.0% | 0.0% | nan | 0.61% |
| 2022-09-07 | 1.02% | 0.51% | 0.0% | 0.0% | nan | 0.63% |
| 2022-09-12 | 0.93% | 0.465% | 0.0% | 0.0% | nan | 0.23% |
| 2022-11-28 | 0.7% | 0.35% | 0.0% | 0.0% | nan | 0.67% |
| 2024-10-23 | 0.75% | 0.375% | 0.0% | 0.0% | 09:15 | 0.24% |
| 2024-11-29 | 0.8% | 0.4% | 0.0% | 0.0% | nan | 0.82% |
| 2025-06-13 | 0.73% | 0.365% | 0.0% | 0.0% | nan | 1.07% |
| 2026-06-02 | 0.87% | 0.435% | 0.0% | 0.0% | nan | 1.27% |
| 2026-05-22 | 0.93% | 0.465% | 0.001% | 0.2% | 09:15 | 0.33% |
| 2025-02-25 | 0.76% | 0.38% | 0.011% | 2.9% | 15:25 | 0.04% |

### Examples: Closest to Threshold (Near Misses)

Days that almost crossed the threshold but fell just short:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2022-11-10 | 0.83% | 0.415% | 0.414% | 99.8% | 14:20 | -0.04% |
| 2023-11-20 | 0.62% | 0.31% | 0.307% | 99.0% | 12:00 | -0.19% |
| 2025-02-04 | 0.75% | 0.375% | 0.369% | 98.4% | 10:35 | 0.84% |
| 2021-07-09 | 0.71% | 0.355% | 0.349% | 98.3% | 09:20 | 0.06% |
| 2024-02-06 | 0.82% | 0.41% | 0.402% | 98.0% | 09:20 | 0.52% |
| 2022-06-06 | 1.05% | 0.525% | 0.514% | 97.9% | 09:30 | 0.2% |
| 2026-07-21 | 0.68% | 0.34% | 0.332% | 97.6% | 13:00 | -0.09% |
| 2021-07-19 | 0.61% | 0.305% | 0.297% | 97.4% | 14:45 | 0.02% |
| 2024-12-23 | 0.79% | 0.395% | 0.383% | 97.0% | 13:35 | 0.04% |
| 2024-03-12 | 0.73% | 0.365% | 0.351% | 96.2% | 10:45 | -0.0% |

---

## Bullish Alignment — Reversed Before Half (200 days)

The bullish high from open never crossed the VIX half-threshold.

### When Did the Aligned Move Reach Its Deepest Point?

This is the candle where the running high (bullish) or running low (bearish)
hit its maximum — the closest it ever got to the threshold before fading.

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **9:30** | 15 min |
| Average | 10:55 | 100 min |
| 25th percentile | 9:15 | 0 min |
| 75th percentile | 12:30 | 195 min |
| Earliest | 9:15 | 0 min |
| Latest | 15:25 | 370 min |

### How Close Did They Get to the Threshold?

| Statistic | % of Half-Threshold Reached |
|-----------|---------------------------:|
| Average | 42.8% |
| Median | 39.5% |
| < 25% of threshold | 75 days (37.5%) |
| 25-50% of threshold | 42 days (21.0%) |
| 50-75% of threshold | 35 days (17.5%) |
| 75-100% of threshold | 46 days (23.0%) |

### Deepest Point Session Distribution

| Session | Count | % | Avg % of Threshold Reached |
|---------|------:|--:|---------------------------:|
| Opening (9:15-9:44) | 100 | 50.0% | 30.1% |
| Early Morning (9:45-10:29) | 14 | 7.0% | 61.8% |
| Late Morning (10:30-11:29) | 18 | 9.0% | 66.6% |
| Midday (11:30-12:29) | 4 | 2.0% | 72.0% |
| Early Afternoon (12:30-13:29) | 6 | 3.0% | 72.7% |
| Late Afternoon (13:30-14:29) | 13 | 6.5% | 71.0% |
| Closing (14:30-15:30) | 27 | 13.5% | 68.3% |

### When Did the Reversal Become Apparent?

The reversal point is when the close of a 5-min candle crosses back past the open price
(bullish: drops below open; bearish: rises above open) after the deepest point.

- **170** days (85.0%): price crossed back past open (clear reversal)
- **30** days (15.0%): price never crossed back past open (aligned direction held weakly)

#### Reversal Timing (price crosses back past open)

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **9:25** | 10 min |
| Average | 10:27 | 73 min |
| 25th percentile | 9:20 | 5 min |
| 75th percentile | 11:15 | 120 min |

#### Time from Deepest Point to Reversal

| Statistic | Minutes |
|-----------|--------:|
| Average gap | 25 min |
| Median gap | 5 min |

### Close Outcome by Deepest Point Timing

If the deepest aligned-direction move happens early and is shallow,
what's the probability the market reverses by close?

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Before 11:15 AM | 129 | 118 | 91.5% | 11 | 8.5% |
| After 11:15 AM | 53 | 20 | 37.7% | 33 | 62.3% |

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Within first hour (by 10:15) | 110 | 103 | 93.6% | 7 | 6.4% |
| After first hour | 72 | 35 | 48.6% | 37 | 51.4% |

### Examples: Shallowest Moves (Least Momentum)

Days where the aligned move barely got started:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2021-03-31 | 1.07% | 0.535% | 0.0% | 0.0% | nan | -0.8% |
| 2022-03-10 | 1.44% | 0.72% | 0.0% | 0.0% | nan | -1.14% |
| 2022-08-10 | 1.01% | 0.505% | 0.0% | 0.0% | nan | -0.24% |
| 2022-10-25 | 0.91% | 0.455% | 0.0% | 0.0% | nan | -0.93% |
| 2022-12-09 | 0.7% | 0.35% | 0.0% | 0.0% | nan | -0.91% |
| 2023-02-06 | 0.75% | 0.375% | 0.0% | 0.0% | nan | -0.32% |
| 2023-03-20 | 0.77% | 0.385% | 0.0% | 0.0% | nan | -0.37% |
| 2023-04-03 | 0.68% | 0.34% | 0.0% | 0.0% | nan | -0.16% |
| 2023-05-11 | 0.68% | 0.34% | 0.0% | 0.0% | nan | -0.29% |
| 2023-05-16 | 0.69% | 0.345% | 0.0% | 0.0% | nan | -0.84% |

### Examples: Closest to Threshold (Near Misses)

Days that almost crossed the threshold but fell just short:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2022-08-02 | 0.92% | 0.46% | 0.46% | 100.0% | 14:45 | -0.09% |
| 2024-01-04 | 0.74% | 0.37% | 0.37% | 100.0% | 15:25 | 0.3% |
| 2022-12-20 | 0.71% | 0.355% | 0.351% | 98.9% | 15:10 | 0.25% |
| 2025-03-06 | 0.72% | 0.36% | 0.356% | 98.9% | 15:00 | 0.24% |
| 2024-06-06 | 0.99% | 0.495% | 0.489% | 98.8% | 11:10 | 0.22% |
| 2022-07-01 | 1.14% | 0.57% | 0.56% | 98.2% | 15:25 | 0.38% |
| 2021-02-25 | 1.27% | 0.635% | 0.623% | 98.1% | 14:25 | 0.16% |
| 2026-02-23 | 0.75% | 0.375% | 0.362% | 96.5% | 09:30 | 0.1% |
| 2024-09-23 | 0.67% | 0.335% | 0.323% | 96.4% | 15:05 | 0.22% |
| 2024-11-25 | 0.84% | 0.42% | 0.404% | 96.2% | 11:20 | -0.01% |

---
