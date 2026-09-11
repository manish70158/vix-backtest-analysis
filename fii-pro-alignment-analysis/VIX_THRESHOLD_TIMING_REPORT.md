# VIX Half-Threshold Timing Analysis

> **Question**: By what time during the trading day does the market
> exceed half the VIX-predicted range in the aligned direction?
>
> Uses 5-minute candle data from PostgreSQL to find the exact candle
> where the threshold was first crossed.

## Overall Summary

| Metric | Count |
|--------|------:|
| Total alignment days analyzed | 645 |
| Exceeded half-threshold | 306 (47.4%) |
| Never exceeded | 339 (52.6%) |

## All Exceeded Days (306 days)

When did the aligned move first cross half the VIX-predicted range?

### Timing Statistics

| Statistic | Minutes from Open | Clock Time |
|-----------|------------------:|-----------:|
| Average | 107 min | ~11:02 |
| Median | 62 min | ~10:17 |
| 25th percentile | 16 min | ~9:31 |
| 75th percentile | 184 min | ~12:18 |
| Earliest | 0 min | ~9:15 |
| Latest | 370 min | ~15:25 |

### Session Distribution

| Session | Count | % | Cumulative % |
|---------|------:|--:|-----------:|
| Opening (9:15-9:44) | 102 | 33.3% | 33.3% |
| Early Morning (9:45-10:29) | 64 | 20.9% | 54.2% |
| Late Morning (10:30-11:29) | 38 | 12.4% | 66.6% |
| Midday (11:30-12:29) | 30 | 9.8% | 76.4% |
| Early Afternoon (12:30-13:29) | 25 | 8.2% | 84.6% |
| Late Afternoon (13:30-14:29) | 29 | 9.5% | 94.1% |
| Closing (14:30-15:30) | 18 | 5.9% | 100.0% |

### Win Rate by Cross Time

Does earlier crossing predict higher win rate?

| Session | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Opening (9:15-9:44) | 102 | 82 | 80.4% |
| Early Morning (9:45-10:29) | 64 | 49 | 76.6% |
| Late Morning (10:30-11:29) | 38 | 28 | 73.7% |
| Midday (11:30-12:29) | 30 | 28 | 93.3% |
| Early Afternoon (12:30-13:29) | 25 | 21 | 84.0% |
| Late Afternoon (13:30-14:29) | 29 | 27 | 93.1% |
| Closing (14:30-15:30) | 18 | 18 | 100.0% |

### 30-Minute Bucket Distribution

| Time Window | Count | % | WR% |
|-------------|------:|--:|----:|
| 09:15-09:44 | 102 | 33.3% | 80.4% |
| 09:45-10:14 | 46 | 15.0% | 73.9% |
| 10:15-10:44 | 27 | 8.8% | 81.5% |
| 10:45-11:14 | 21 | 6.9% | 81.0% |
| 11:15-11:44 | 15 | 4.9% | 73.3% |
| 11:45-12:14 | 11 | 3.6% | 90.9% |
| 12:15-12:44 | 20 | 6.5% | 95.0% |
| 12:45-13:14 | 14 | 4.6% | 78.6% |
| 13:15-13:44 | 12 | 3.9% | 83.3% |
| 13:45-14:14 | 11 | 3.6% | 90.9% |
| 14:15-14:44 | 13 | 4.2% | 100.0% |
| 14:45-15:14 | 10 | 3.3% | 100.0% |
| 15:15-15:30 | 4 | 1.3% | 100.0% |

### Expiry vs Non-Expiry Timing

| Context | Count | Avg Minutes | Avg Time | Median Minutes | Median Time |
|---------|------:|------------:|---------:|---------------:|------------:|
| Expiry | 71 | 111 | ~11:06 | 55 | ~10:10 |
| Non-Expiry | 235 | 106 | ~11:00 | 65 | ~10:20 |

### VIX Regime Timing

| VIX Regime | Count | Avg Minutes | Avg Time | Median Time |
|------------|------:|------------:|---------:|------------:|
| Low (<15) | 185 | 111 | ~11:06 | ~10:25 |
| Normal (15-20) | 77 | 83 | ~10:38 | ~10:00 |
| Elevated (20-30) | 44 | 133 | ~11:27 | ~10:52 |

### Year-over-Year Timing

| Year | Count | Avg Minutes | Avg Time | Median Time |
|------|------:|------------:|---------:|------------:|
| 2020 | 10 | 102 | ~10:57 | ~10:37 |
| 2021 | 41 | 101 | ~10:55 | ~9:40 |
| 2022 | 48 | 100 | ~10:55 | ~10:17 |
| 2023 | 70 | 114 | ~11:08 | ~10:27 |
| 2024 | 52 | 100 | ~10:55 | ~10:10 |
| 2025 | 56 | 117 | ~11:11 | ~10:37 |
| 2026 | 29 | 107 | ~11:02 | ~10:20 |

### Fastest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2020-09-01 | 09:15 | 0 | 0.817% | 1.2% | 0.26% | Failed |
| 2021-03-25 | 09:15 | 0 | 0.654% | 1.18% | -1.54% | Worked |
| 2021-04-06 | 09:15 | 0 | 0.988% | 1.11% | -0.25% | Worked |
| 2021-07-28 | 09:15 | 0 | 0.666% | 0.69% | -0.3% | Worked |
| 2021-10-25 | 09:15 | 0 | 0.808% | 0.92% | -0.51% | Worked |
| 2021-11-29 | 09:15 | 0 | 1.281% | 1.09% | -0.09% | Worked |
| 2021-11-30 | 09:15 | 0 | 0.645% | 1.09% | -0.45% | Failed |
| 2021-12-20 | 09:15 | 0 | 0.613% | 0.86% | -1.26% | Worked |
| 2022-01-19 | 09:15 | 0 | 0.573% | 0.93% | -1.04% | Worked |
| 2022-02-04 | 09:15 | 0 | 0.557% | 1.0% | -0.5% | Worked |

### Slowest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2025-04-30 | 15:25 | 370 | 0.589% | 0.91% | -0.39% | Worked |
| 2026-05-25 | 15:25 | 370 | 0.477% | 0.94% | 0.46% | Worked |
| 2021-09-03 | 15:20 | 365 | 0.446% | 0.75% | 0.34% | Worked |
| 2025-04-16 | 15:20 | 365 | 0.458% | 0.84% | 0.38% | Worked |
| 2021-06-30 | 15:10 | 355 | 0.402% | 0.68% | -0.29% | Worked |
| 2021-04-30 | 15:05 | 350 | 0.761% | 1.22% | -0.88% | Worked |
| 2023-07-14 | 15:05 | 350 | 0.305% | 0.57% | 0.48% | Worked |
| 2025-11-06 | 15:05 | 350 | 0.359% | 0.66% | -0.29% | Worked |
| 2020-11-18 | 15:00 | 345 | 0.577% | 1.04% | 0.59% | Worked |
| 2021-12-22 | 15:00 | 345 | 0.57% | 0.92% | 0.61% | Worked |

## Bullish Alignment — Exceeded Half (116 days)

When did the bullish (high from open) move first cross half the VIX-predicted range?

### Timing Statistics

| Statistic | Minutes from Open | Clock Time |
|-----------|------------------:|-----------:|
| Average | 124 min | ~11:18 |
| Median | 90 min | ~10:45 |
| 25th percentile | 29 min | ~9:43 |
| 75th percentile | 195 min | ~12:30 |
| Earliest | 0 min | ~9:15 |
| Latest | 370 min | ~15:25 |

### Session Distribution

| Session | Count | % | Cumulative % |
|---------|------:|--:|-----------:|
| Opening (9:15-9:44) | 29 | 25.0% | 25.0% |
| Early Morning (9:45-10:29) | 23 | 19.8% | 44.8% |
| Late Morning (10:30-11:29) | 19 | 16.4% | 61.2% |
| Midday (11:30-12:29) | 13 | 11.2% | 72.4% |
| Early Afternoon (12:30-13:29) | 12 | 10.3% | 82.7% |
| Late Afternoon (13:30-14:29) | 10 | 8.6% | 91.3% |
| Closing (14:30-15:30) | 10 | 8.6% | 99.9% |

### Win Rate by Cross Time

Does earlier crossing predict higher win rate?

| Session | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Opening (9:15-9:44) | 29 | 25 | 86.2% |
| Early Morning (9:45-10:29) | 23 | 18 | 78.3% |
| Late Morning (10:30-11:29) | 19 | 17 | 89.5% |
| Midday (11:30-12:29) | 13 | 11 | 84.6% |
| Early Afternoon (12:30-13:29) | 12 | 11 | 91.7% |
| Late Afternoon (13:30-14:29) | 10 | 9 | 90.0% |
| Closing (14:30-15:30) | 10 | 10 | 100.0% |

### 30-Minute Bucket Distribution

| Time Window | Count | % | WR% |
|-------------|------:|--:|----:|
| 09:15-09:44 | 29 | 25.0% | 86.2% |
| 09:45-10:14 | 14 | 12.1% | 78.6% |
| 10:15-10:44 | 14 | 12.1% | 78.6% |
| 10:45-11:14 | 11 | 9.5% | 100.0% |
| 11:15-11:44 | 7 | 6.0% | 85.7% |
| 11:45-12:14 | 5 | 4.3% | 80.0% |
| 12:15-12:44 | 9 | 7.8% | 88.9% |
| 12:45-13:14 | 5 | 4.3% | 80.0% |
| 13:15-13:44 | 5 | 4.3% | 100.0% |
| 13:45-14:14 | 5 | 4.3% | 80.0% |
| 14:15-14:44 | 4 | 3.4% | 100.0% |
| 14:45-15:14 | 5 | 4.3% | 100.0% |
| 15:15-15:30 | 3 | 2.6% | 100.0% |

### Expiry vs Non-Expiry Timing

| Context | Count | Avg Minutes | Avg Time | Median Minutes | Median Time |
|---------|------:|------------:|---------:|---------------:|------------:|
| Expiry | 22 | 107 | ~11:02 | 68 | ~10:22 |
| Non-Expiry | 94 | 127 | ~11:22 | 95 | ~10:50 |

### VIX Regime Timing

| VIX Regime | Count | Avg Minutes | Avg Time | Median Time |
|------------|------:|------------:|---------:|------------:|
| Low (<15) | 69 | 129 | ~11:24 | ~10:55 |
| Normal (15-20) | 32 | 101 | ~10:55 | ~10:12 |
| Elevated (20-30) | 15 | 147 | ~11:41 | ~11:50 |

### Year-over-Year Timing

| Year | Count | Avg Minutes | Avg Time | Median Time |
|------|------:|------------:|---------:|------------:|
| 2020 | 6 | 144 | ~11:39 | ~10:57 |
| 2021 | 18 | 131 | ~11:26 | ~10:47 |
| 2022 | 11 | 104 | ~10:58 | ~10:25 |
| 2023 | 23 | 151 | ~11:46 | ~11:30 |
| 2024 | 20 | 134 | ~11:29 | ~11:00 |
| 2025 | 26 | 93 | ~10:47 | ~10:10 |
| 2026 | 12 | 116 | ~11:10 | ~10:22 |

### Fastest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2021-11-30 | 09:15 | 0 | 0.645% | 1.09% | -0.45% | Failed |
| 2022-04-04 | 09:15 | 0 | 0.573% | 0.96% | 1.27% | Worked |
| 2022-09-14 | 09:15 | 0 | 0.65% | 0.91% | 1.29% | Worked |
| 2025-10-03 | 09:15 | 0 | 0.388% | 0.54% | 0.55% | Worked |
| 2025-11-26 | 09:15 | 0 | 0.49% | 0.64% | 1.4% | Worked |
| 2021-10-12 | 09:20 | 5 | 0.446% | 0.84% | 0.5% | Worked |
| 2023-03-06 | 09:20 | 5 | 0.424% | 0.64% | 0.22% | Worked |
| 2024-06-07 | 09:20 | 5 | 0.487% | 0.88% | 1.96% | Worked |
| 2024-11-19 | 09:20 | 5 | 0.467% | 0.79% | -0.26% | Failed |
| 2025-01-24 | 09:20 | 5 | 0.466% | 0.87% | -0.4% | Failed |

### Slowest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2026-05-25 | 15:25 | 370 | 0.477% | 0.94% | 0.46% | Worked |
| 2021-09-03 | 15:20 | 365 | 0.446% | 0.75% | 0.34% | Worked |
| 2025-04-16 | 15:20 | 365 | 0.458% | 0.84% | 0.38% | Worked |
| 2023-07-14 | 15:05 | 350 | 0.305% | 0.57% | 0.48% | Worked |
| 2020-11-18 | 15:00 | 345 | 0.577% | 1.04% | 0.59% | Worked |
| 2021-12-22 | 15:00 | 345 | 0.57% | 0.92% | 0.61% | Worked |
| 2023-06-27 | 15:00 | 345 | 0.363% | 0.6% | 0.37% | Worked |
| 2024-08-21 | 15:00 | 345 | 0.376% | 0.72% | 0.41% | Worked |
| 2023-02-15 | 14:35 | 320 | 0.36% | 0.7% | 0.71% | Worked |
| 2026-04-06 | 14:35 | 320 | 0.704% | 1.34% | 0.79% | Worked |

## Bearish Alignment — Exceeded Half (190 days)

When did the bearish (low from open) move first cross half the VIX-predicted range?

### Timing Statistics

| Statistic | Minutes from Open | Clock Time |
|-----------|------------------:|-----------:|
| Average | 97 min | ~10:52 |
| Median | 45 min | ~10:00 |
| 25th percentile | 15 min | ~9:30 |
| 75th percentile | 178 min | ~12:12 |
| Earliest | 0 min | ~9:15 |
| Latest | 370 min | ~15:25 |

### Session Distribution

| Session | Count | % | Cumulative % |
|---------|------:|--:|-----------:|
| Opening (9:15-9:44) | 73 | 38.4% | 38.4% |
| Early Morning (9:45-10:29) | 41 | 21.6% | 60.0% |
| Late Morning (10:30-11:29) | 19 | 10.0% | 70.0% |
| Midday (11:30-12:29) | 17 | 8.9% | 78.9% |
| Early Afternoon (12:30-13:29) | 13 | 6.8% | 85.7% |
| Late Afternoon (13:30-14:29) | 19 | 10.0% | 95.7% |
| Closing (14:30-15:30) | 8 | 4.2% | 99.9% |

### Win Rate by Cross Time

Does earlier crossing predict higher win rate?

| Session | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Opening (9:15-9:44) | 73 | 57 | 78.1% |
| Early Morning (9:45-10:29) | 41 | 31 | 75.6% |
| Late Morning (10:30-11:29) | 19 | 11 | 57.9% |
| Midday (11:30-12:29) | 17 | 17 | 100.0% |
| Early Afternoon (12:30-13:29) | 13 | 10 | 76.9% |
| Late Afternoon (13:30-14:29) | 19 | 18 | 94.7% |
| Closing (14:30-15:30) | 8 | 8 | 100.0% |

### 30-Minute Bucket Distribution

| Time Window | Count | % | WR% |
|-------------|------:|--:|----:|
| 09:15-09:44 | 73 | 38.4% | 78.1% |
| 09:45-10:14 | 32 | 16.8% | 71.9% |
| 10:15-10:44 | 13 | 6.8% | 84.6% |
| 10:45-11:14 | 10 | 5.3% | 60.0% |
| 11:15-11:44 | 8 | 4.2% | 62.5% |
| 11:45-12:14 | 6 | 3.2% | 100.0% |
| 12:15-12:44 | 11 | 5.8% | 100.0% |
| 12:45-13:14 | 9 | 4.7% | 77.8% |
| 13:15-13:44 | 7 | 3.7% | 71.4% |
| 13:45-14:14 | 6 | 3.2% | 100.0% |
| 14:15-14:44 | 9 | 4.7% | 100.0% |
| 14:45-15:14 | 5 | 2.6% | 100.0% |
| 15:15-15:30 | 1 | 0.5% | 100.0% |

### Expiry vs Non-Expiry Timing

| Context | Count | Avg Minutes | Avg Time | Median Minutes | Median Time |
|---------|------:|------------:|---------:|---------------:|------------:|
| Expiry | 49 | 113 | ~11:08 | 55 | ~10:10 |
| Non-Expiry | 141 | 92 | ~10:46 | 40 | ~9:55 |

### VIX Regime Timing

| VIX Regime | Count | Avg Minutes | Avg Time | Median Time |
|------------|------:|------------:|---------:|------------:|
| Low (<15) | 116 | 100 | ~10:55 | ~10:10 |
| Normal (15-20) | 45 | 71 | ~10:25 | ~9:50 |
| Elevated (20-30) | 29 | 126 | ~11:20 | ~10:25 |

### Year-over-Year Timing

| Year | Count | Avg Minutes | Avg Time | Median Time |
|------|------:|------------:|---------:|------------:|
| 2020 | 4 | 39 | ~9:53 | ~9:35 |
| 2021 | 23 | 77 | ~10:31 | ~9:35 |
| 2022 | 37 | 99 | ~10:54 | ~10:00 |
| 2023 | 47 | 95 | ~10:50 | ~9:55 |
| 2024 | 32 | 80 | ~10:34 | ~9:42 |
| 2025 | 30 | 138 | ~11:32 | ~10:47 |
| 2026 | 17 | 101 | ~10:56 | ~10:20 |

### Fastest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2020-09-01 | 09:15 | 0 | 0.817% | 1.2% | 0.26% | Failed |
| 2021-03-25 | 09:15 | 0 | 0.654% | 1.18% | -1.54% | Worked |
| 2021-04-06 | 09:15 | 0 | 0.988% | 1.11% | -0.25% | Worked |
| 2021-07-28 | 09:15 | 0 | 0.666% | 0.69% | -0.3% | Worked |
| 2021-10-25 | 09:15 | 0 | 0.808% | 0.92% | -0.51% | Worked |
| 2021-11-29 | 09:15 | 0 | 1.281% | 1.09% | -0.09% | Worked |
| 2021-12-20 | 09:15 | 0 | 0.613% | 0.86% | -1.26% | Worked |
| 2022-01-19 | 09:15 | 0 | 0.573% | 0.93% | -1.04% | Worked |
| 2022-02-04 | 09:15 | 0 | 0.557% | 1.0% | -0.5% | Worked |
| 2022-02-14 | 09:15 | 0 | 0.771% | 0.98% | -1.5% | Worked |

### Slowest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2025-04-30 | 15:25 | 370 | 0.589% | 0.91% | -0.39% | Worked |
| 2021-06-30 | 15:10 | 355 | 0.402% | 0.68% | -0.29% | Worked |
| 2021-04-30 | 15:05 | 350 | 0.761% | 1.22% | -0.88% | Worked |
| 2025-11-06 | 15:05 | 350 | 0.359% | 0.66% | -0.29% | Worked |
| 2026-02-13 | 15:00 | 345 | 0.323% | 0.61% | -0.43% | Worked |
| 2025-11-25 | 14:55 | 340 | 0.388% | 0.69% | -0.53% | Worked |
| 2024-05-30 | 14:35 | 320 | 0.664% | 1.27% | -0.27% | Worked |
| 2025-07-03 | 14:30 | 315 | 0.381% | 0.65% | -0.42% | Worked |
| 2022-10-21 | 14:25 | 310 | 0.534% | 0.9% | -0.22% | Worked |
| 2024-01-09 | 14:25 | 310 | 0.452% | 0.7% | -0.47% | Worked |

## Early vs Late Cross: Does Timing Predict Close Outcome?

Split at the median cross time for each alignment type.

### Bullish Alignment (Median: 90 min = ~10:45)

| Timing | Count | Worked and Remained | WR% | Avg Close% |
|--------|------:|--------------------:|----:|-----------:|
| Early (≤ median) | 60 | 50 | 83.3% | 0.56% |
| Late (> median) | 56 | 51 | 91.1% | 0.467% |

### Bearish Alignment (Median: 45 min = ~10:00)

| Timing | Count | Worked and Remained | WR% | Avg Close% |
|--------|------:|--------------------:|----:|-----------:|
| Early (≤ median) | 97 | 74 | 76.3% | -0.417% |
| Late (> median) | 93 | 78 | 83.9% | -0.371% |

## First Hour Rule: Cross Before 10:15 AM

If the threshold is crossed within the first hour (by 10:15 AM), is the signal stronger?

### Bullish Alignment

| Timing | Count | % | Worked and Remained | WR% | Avg Close% |
|--------|------:|--:|--------------------:|----:|-----------:|
| Within first hour (≤10:15) | 45 | 38.8% | 38 | 84.4% | 0.59% |
| After first hour (>10:15) | 71 | 61.2% | 63 | 88.7% | 0.467% |

### Bearish Alignment

| Timing | Count | % | Worked and Remained | WR% | Avg Close% |
|--------|------:|--:|--------------------:|----:|-----------:|
| Within first hour (≤10:15) | 108 | 56.8% | 83 | 76.9% | -0.405% |
| After first hour (>10:15) | 82 | 43.2% | 69 | 84.1% | -0.381% |

## Practical Interpretation

**Bullish Alignment**: Median threshold cross at **10:45** (90 minutes from open)

**Bearish Alignment**: Median threshold cross at **10:00** (45 minutes from open)

```
Caveat: FII/PRO alignment is only known after T+1 settlement.
The timing analysis answers: IF you knew the alignment,
by what time would the VIX threshold typically be crossed?
This is useful for post-hoc pattern recognition, not real-time trading.
```
