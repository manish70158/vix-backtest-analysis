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
| Median | **9:37** | 22 min |
| Average | 10:40 | 86 min |
| 25th percentile | 9:15 | 0 min |
| 75th percentile | 11:17 | 122 min |
| Earliest | 9:15 | 0 min |
| Latest | 18:50 | 575 min |

### How Close Did They Get to the Threshold?

| Statistic | % of Half-Threshold Reached |
|-----------|---------------------------:|
| Average | 48.9% |
| Median | 51.6% |
| < 25% of threshold | 27 days (19.4%) |
| 25-50% of threshold | 38 days (27.3%) |
| 50-75% of threshold | 50 days (36.0%) |
| 75-100% of threshold | 23 days (16.5%) |

### Deepest Point Session Distribution

| Session | Count | % | Avg % of Threshold Reached |
|---------|------:|--:|---------------------------:|
| Opening (9:15-9:44) | 69 | 49.6% | 44.6% |
| Early Morning (9:45-10:29) | 16 | 11.5% | 57.5% |
| Late Morning (10:30-11:29) | 15 | 10.8% | 67.3% |
| Midday (11:30-12:29) | 5 | 3.6% | 73.1% |
| Early Afternoon (12:30-13:29) | 10 | 7.2% | 62.9% |
| Late Afternoon (13:30-14:29) | 6 | 4.3% | 62.2% |
| Closing (14:30-15:30) | 11 | 7.9% | 38.8% |

### When Did the Reversal Become Apparent?

The reversal point is when the close of a 5-min candle crosses back past the open price
(bullish: drops below open; bearish: rises above open) after the deepest point.

- **126** days (90.6%): price crossed back past open (clear reversal)
- **13** days (9.4%): price never crossed back past open (aligned direction held weakly)

#### Reversal Timing (price crosses back past open)

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **9:50** | 35 min |
| Average | 10:46 | 91 min |
| 25th percentile | 9:20 | 5 min |
| 75th percentile | 11:33 | 139 min |

#### Time from Deepest Point to Reversal

| Statistic | Minutes |
|-----------|--------:|
| Average gap | 31 min |
| Median gap | 15 min |

### Close Outcome by Deepest Point Timing

If the deepest aligned-direction move happens early and is shallow,
what's the probability the market reverses by close?

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Before 11:15 AM | 99 | 85 | 85.9% | 14 | 14.1% |
| After 11:15 AM | 33 | 21 | 63.6% | 12 | 36.4% |

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Within first hour (by 10:15) | 84 | 75 | 89.3% | 9 | 10.7% |
| After first hour | 48 | 31 | 64.6% | 17 | 35.4% |

### Examples: Shallowest Moves (Least Momentum)

Days where the aligned move barely got started:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2022-09-05 | 1.23% | 0.615% | 0.0% | 0.0% | nan | 0.61% |
| 2022-09-07 | 1.23% | 0.615% | 0.0% | 0.0% | nan | 0.63% |
| 2022-09-12 | 1.12% | 0.56% | 0.0% | 0.0% | nan | 0.23% |
| 2022-11-28 | 0.84% | 0.42% | 0.0% | 0.0% | nan | 0.67% |
| 2024-10-23 | 0.91% | 0.455% | 0.0% | 0.0% | 09:15 | 0.24% |
| 2024-11-29 | 0.96% | 0.48% | 0.0% | 0.0% | nan | 0.82% |
| 2025-06-13 | 0.88% | 0.44% | 0.0% | 0.0% | nan | 1.07% |
| 2026-06-02 | 1.04% | 0.52% | 0.0% | 0.0% | nan | 1.27% |
| 2026-05-22 | 1.12% | 0.56% | 0.001% | 0.2% | 09:15 | 0.33% |
| 2025-02-25 | 0.91% | 0.455% | 0.011% | 2.4% | 15:25 | 0.04% |

### Examples: Closest to Threshold (Near Misses)

Days that almost crossed the threshold but fell just short:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2023-08-23 | 0.74% | 0.37% | 0.372% | 100.5% | 09:55 | 0.01% |
| 2026-02-02 | 0.95% | 0.475% | 0.472% | 99.4% | 11:25 | 1.14% |
| 2024-10-16 | 0.82% | 0.41% | 0.4% | 97.6% | 11:45 | -0.19% |
| 2024-10-18 | 0.84% | 0.42% | 0.394% | 93.8% | 09:25 | 0.8% |
| 2023-08-25 | 0.74% | 0.37% | 0.346% | 93.5% | 10:30 | -0.28% |
| 2022-11-15 | 0.94% | 0.47% | 0.438% | 93.2% | 11:10 | 0.32% |
| 2022-01-07 | 1.13% | 0.565% | 0.52% | 92.0% | 12:45 | 0.12% |
| 2024-02-26 | 0.94% | 0.47% | 0.424% | 90.2% | 12:15 | -0.23% |
| 2024-02-09 | 1.0% | 0.5% | 0.447% | 89.4% | 11:05 | 0.27% |
| 2023-05-25 | 0.83% | 0.415% | 0.362% | 87.2% | 13:40 | 0.37% |

---

## Bullish Alignment — Reversed Before Half (199 days)

The bullish high from open never crossed the VIX half-threshold.

### When Did the Aligned Move Reach Its Deepest Point?

This is the candle where the running high (bullish) or running low (bearish)
hit its maximum — the closest it ever got to the threshold before fading.

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **9:52** | 38 min |
| Average | 11:08 | 114 min |
| 25th percentile | 9:15 | 0 min |
| 75th percentile | 13:18 | 244 min |
| Earliest | 9:15 | 0 min |
| Latest | 15:25 | 370 min |

### How Close Did They Get to the Threshold?

| Statistic | % of Half-Threshold Reached |
|-----------|---------------------------:|
| Average | 41.9% |
| Median | 40.9% |
| < 25% of threshold | 75 days (37.7%) |
| 25-50% of threshold | 44 days (22.1%) |
| 50-75% of threshold | 40 days (20.1%) |
| 75-100% of threshold | 39 days (19.6%) |

### Deepest Point Session Distribution

| Session | Count | % | Avg % of Threshold Reached |
|---------|------:|--:|---------------------------:|
| Opening (9:15-9:44) | 89 | 44.7% | 25.9% |
| Early Morning (9:45-10:29) | 17 | 8.5% | 59.0% |
| Late Morning (10:30-11:29) | 23 | 11.6% | 62.7% |
| Midday (11:30-12:29) | 4 | 2.0% | 60.0% |
| Early Afternoon (12:30-13:29) | 7 | 3.5% | 63.9% |
| Late Afternoon (13:30-14:29) | 15 | 7.5% | 64.9% |
| Closing (14:30-15:30) | 31 | 15.6% | 62.4% |

### When Did the Reversal Become Apparent?

The reversal point is when the close of a 5-min candle crosses back past the open price
(bullish: drops below open; bearish: rises above open) after the deepest point.

- **161** days (80.9%): price crossed back past open (clear reversal)
- **38** days (19.1%): price never crossed back past open (aligned direction held weakly)

#### Reversal Timing (price crosses back past open)

| Statistic | Clock Time | Minutes from 9:15 |
|-----------|:----------:|-------------------:|
| Median | **9:30** | 15 min |
| Average | 10:36 | 81 min |
| 25th percentile | 9:20 | 5 min |
| 75th percentile | 11:40 | 145 min |

#### Time from Deepest Point to Reversal

| Statistic | Minutes |
|-----------|--------:|
| Average gap | 30 min |
| Median gap | 10 min |

### Close Outcome by Deepest Point Timing

If the deepest aligned-direction move happens early and is shallow,
what's the probability the market reverses by close?

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Before 11:15 AM | 125 | 111 | 88.8% | 14 | 11.2% |
| After 11:15 AM | 61 | 21 | 34.4% | 40 | 65.6% |

| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |
|---------------|------:|------------------:|-----:|--------------------:|----:|
| Within first hour (by 10:15) | 100 | 92 | 92.0% | 8 | 8.0% |
| After first hour | 86 | 40 | 46.5% | 46 | 53.5% |

### Examples: Shallowest Moves (Least Momentum)

Days where the aligned move barely got started:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2022-03-10 | 1.73% | 0.865% | 0.0% | 0.0% | nan | -1.14% |
| 2022-10-25 | 1.1% | 0.55% | 0.0% | 0.0% | nan | -0.93% |
| 2022-12-09 | 0.84% | 0.42% | 0.0% | 0.0% | nan | -0.91% |
| 2023-02-06 | 0.91% | 0.455% | 0.0% | 0.0% | nan | -0.32% |
| 2023-03-20 | 0.93% | 0.465% | 0.0% | 0.0% | nan | -0.37% |
| 2023-05-11 | 0.82% | 0.41% | 0.0% | 0.0% | nan | -0.29% |
| 2023-05-16 | 0.83% | 0.415% | 0.0% | 0.0% | nan | -0.84% |
| 2024-04-26 | 0.68% | 0.34% | 0.0% | 0.0% | nan | -0.75% |
| 2024-06-04 | 1.32% | 0.66% | 0.0% | 0.0% | nan | -5.1% |
| 2024-06-13 | 0.91% | 0.455% | 0.0% | 0.0% | 09:15 | -0.35% |

### Examples: Closest to Threshold (Near Misses)

Days that almost crossed the threshold but fell just short:

| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |
|------|------:|------:|------:|------:|:----------:|------:|
| 2025-12-12 | 0.66% | 0.33% | 0.333% | 100.9% | 15:10 | 0.28% |
| 2024-05-14 | 1.3% | 0.65% | 0.649% | 99.8% | 14:05 | 0.44% |
| 2021-10-12 | 1.01% | 0.505% | 0.501% | 99.2% | 15:15 | 0.5% |
| 2021-09-03 | 0.9% | 0.45% | 0.446% | 99.1% | 15:20 | 0.34% |
| 2024-12-24 | 0.85% | 0.425% | 0.415% | 97.6% | 10:35 | -0.16% |
| 2023-04-12 | 0.75% | 0.375% | 0.365% | 97.3% | 15:20 | 0.33% |
| 2026-08-07 | 0.77% | 0.385% | 0.373% | 96.9% | 09:55 | 0.13% |
| 2021-07-30 | 0.82% | 0.41% | 0.391% | 95.4% | 14:20 | -0.17% |
| 2026-04-28 | 1.16% | 0.58% | 0.548% | 94.5% | 10:25 | -0.14% |
| 2025-12-10 | 0.69% | 0.345% | 0.323% | 93.6% | 10:25 | -0.47% |

---
