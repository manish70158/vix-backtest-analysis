# VIX Half-Threshold Timing Analysis

> **Question**: By what time during the trading day does the market
> exceed half the VIX-predicted range in the aligned direction?
>
> Uses 5-minute candle data from PostgreSQL to find the exact candle
> where the threshold was first crossed.

## Overall Summary

| Metric | Count |
|--------|------:|
| Total alignment days analyzed | 575 |
| Exceeded half-threshold | 239 (41.6%) |
| Never exceeded | 336 (58.4%) |

## All Exceeded Days (239 days)

When did the aligned move first cross half the VIX-predicted range?

### Timing Statistics

| Statistic | Minutes from Open | Clock Time |
|-----------|------------------:|-----------:|
| Average | 129 min | ~11:24 |
| Median | 90 min | ~10:45 |
| 25th percentile | 25 min | ~9:40 |
| 75th percentile | 225 min | ~13:00 |
| Earliest | 0 min | ~9:15 |
| Latest | 370 min | ~15:25 |

### Session Distribution

| Session | Count | % | Cumulative % |
|---------|------:|--:|-----------:|
| Opening (9:15-9:44) | 61 | 25.5% | 25.5% |
| Early Morning (9:45-10:29) | 47 | 19.7% | 45.2% |
| Late Morning (10:30-11:29) | 34 | 14.2% | 59.4% |
| Midday (11:30-12:29) | 26 | 10.9% | 70.3% |
| Early Afternoon (12:30-13:29) | 25 | 10.5% | 80.8% |
| Late Afternoon (13:30-14:29) | 20 | 8.4% | 89.2% |
| Closing (14:30-15:30) | 26 | 10.9% | 100.1% |

### Win Rate by Cross Time

Does earlier crossing predict higher win rate?

| Session | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Opening (9:15-9:44) | 61 | 52 | 85.2% |
| Early Morning (9:45-10:29) | 47 | 38 | 80.9% |
| Late Morning (10:30-11:29) | 34 | 25 | 73.5% |
| Midday (11:30-12:29) | 26 | 23 | 88.5% |
| Early Afternoon (12:30-13:29) | 25 | 24 | 96.0% |
| Late Afternoon (13:30-14:29) | 20 | 18 | 90.0% |
| Closing (14:30-15:30) | 26 | 26 | 100.0% |

### 30-Minute Bucket Distribution

| Time Window | Count | % | WR% |
|-------------|------:|--:|----:|
| 09:15-09:44 | 61 | 25.5% | 85.2% |
| 09:45-10:14 | 30 | 12.6% | 73.3% |
| 10:15-10:44 | 24 | 10.0% | 87.5% |
| 10:45-11:14 | 21 | 8.8% | 76.2% |
| 11:15-11:44 | 10 | 4.2% | 70.0% |
| 11:45-12:14 | 13 | 5.4% | 84.6% |
| 12:15-12:44 | 15 | 6.3% | 100.0% |
| 12:45-13:14 | 10 | 4.2% | 100.0% |
| 13:15-13:44 | 16 | 6.7% | 81.2% |
| 13:45-14:14 | 7 | 2.9% | 100.0% |
| 14:15-14:44 | 14 | 5.9% | 100.0% |
| 14:45-15:14 | 14 | 5.9% | 100.0% |
| 15:15-15:30 | 4 | 1.7% | 100.0% |

### Expiry vs Non-Expiry Timing

| Context | Count | Avg Minutes | Avg Time | Median Minutes | Median Time |
|---------|------:|------------:|---------:|---------------:|------------:|
| Expiry | 61 | 133 | ~11:28 | 90 | ~10:45 |
| Non-Expiry | 178 | 128 | ~11:23 | 95 | ~10:50 |

### VIX Regime Timing

| VIX Regime | Count | Avg Minutes | Avg Time | Median Time |
|------------|------:|------------:|---------:|------------:|
| Low (<15) | 145 | 140 | ~11:34 | ~11:00 |
| Normal (15-20) | 62 | 95 | ~10:50 | ~10:15 |
| Elevated (20-30) | 32 | 149 | ~11:43 | ~11:07 |

### Year-over-Year Timing

| Year | Count | Avg Minutes | Avg Time | Median Time |
|------|------:|------------:|---------:|------------:|
| 2020 | 9 | 137 | ~11:32 | ~11:20 |
| 2021 | 30 | 120 | ~11:15 | ~10:15 |
| 2022 | 40 | 124 | ~11:19 | ~10:45 |
| 2023 | 53 | 150 | ~11:45 | ~11:50 |
| 2024 | 40 | 119 | ~11:13 | ~10:32 |
| 2025 | 46 | 140 | ~11:34 | ~10:52 |
| 2026 | 21 | 95 | ~10:50 | ~10:25 |

### Fastest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2020-09-01 | 09:15 | 0 | 0.817% | 1.44% | 0.26% | Failed |
| 2021-07-28 | 09:15 | 0 | 0.666% | 0.83% | -0.3% | Worked |
| 2021-10-25 | 09:15 | 0 | 0.808% | 1.11% | -0.51% | Worked |
| 2021-11-29 | 09:15 | 0 | 1.281% | 1.31% | -0.09% | Worked |
| 2021-12-20 | 09:15 | 0 | 0.613% | 1.03% | -1.26% | Worked |
| 2022-01-19 | 09:15 | 0 | 0.573% | 1.12% | -1.04% | Worked |
| 2022-02-14 | 09:15 | 0 | 0.771% | 1.18% | -1.5% | Worked |
| 2022-09-14 | 09:15 | 0 | 0.65% | 1.1% | 1.29% | Worked |
| 2024-11-08 | 09:15 | 0 | 0.54% | 0.94% | -0.4% | Worked |
| 2025-07-25 | 09:15 | 0 | 0.346% | 0.68% | -0.71% | Worked |

### Slowest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2024-08-21 | 15:25 | 370 | 0.435% | 0.87% | 0.41% | Worked |
| 2025-04-30 | 15:25 | 370 | 0.589% | 1.09% | -0.39% | Worked |
| 2026-07-30 | 15:25 | 370 | 0.385% | 0.76% | 0.19% | Worked |
| 2021-06-30 | 15:15 | 360 | 0.412% | 0.82% | -0.29% | Worked |
| 2020-12-04 | 15:10 | 355 | 0.629% | 1.2% | 0.71% | Worked |
| 2022-12-07 | 15:10 | 355 | 0.475% | 0.88% | -0.47% | Worked |
| 2023-07-14 | 15:10 | 355 | 0.384% | 0.69% | 0.48% | Worked |
| 2025-12-12 | 15:10 | 355 | 0.333% | 0.66% | 0.28% | Worked |
| 2021-04-30 | 15:05 | 350 | 0.761% | 1.47% | -0.88% | Worked |
| 2026-02-13 | 15:05 | 350 | 0.388% | 0.74% | -0.43% | Worked |

## Bullish Alignment — Exceeded Half (86 days)

When did the bullish (high from open) move first cross half the VIX-predicted range?

### Timing Statistics

| Statistic | Minutes from Open | Clock Time |
|-----------|------------------:|-----------:|
| Average | 152 min | ~11:46 |
| Median | 142 min | ~11:37 |
| 25th percentile | 49 min | ~10:03 |
| 75th percentile | 234 min | ~13:08 |
| Earliest | 0 min | ~9:15 |
| Latest | 370 min | ~15:25 |

### Session Distribution

| Session | Count | % | Cumulative % |
|---------|------:|--:|-----------:|
| Opening (9:15-9:44) | 17 | 19.8% | 19.8% |
| Early Morning (9:45-10:29) | 12 | 14.0% | 33.8% |
| Late Morning (10:30-11:29) | 13 | 15.1% | 48.9% |
| Midday (11:30-12:29) | 15 | 17.4% | 66.3% |
| Early Afternoon (12:30-13:29) | 10 | 11.6% | 77.9% |
| Late Afternoon (13:30-14:29) | 10 | 11.6% | 89.5% |
| Closing (14:30-15:30) | 9 | 10.5% | 100.0% |

### Win Rate by Cross Time

Does earlier crossing predict higher win rate?

| Session | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Opening (9:15-9:44) | 17 | 16 | 94.1% |
| Early Morning (9:45-10:29) | 12 | 10 | 83.3% |
| Late Morning (10:30-11:29) | 13 | 12 | 92.3% |
| Midday (11:30-12:29) | 15 | 13 | 86.7% |
| Early Afternoon (12:30-13:29) | 10 | 10 | 100.0% |
| Late Afternoon (13:30-14:29) | 10 | 8 | 80.0% |
| Closing (14:30-15:30) | 9 | 9 | 100.0% |

### 30-Minute Bucket Distribution

| Time Window | Count | % | WR% |
|-------------|------:|--:|----:|
| 09:15-09:44 | 17 | 19.8% | 94.1% |
| 09:45-10:14 | 5 | 5.8% | 60.0% |
| 10:15-10:44 | 9 | 10.5% | 100.0% |
| 10:45-11:14 | 7 | 8.1% | 85.7% |
| 11:15-11:44 | 6 | 7.0% | 83.3% |
| 11:45-12:14 | 8 | 9.3% | 87.5% |
| 12:15-12:44 | 6 | 7.0% | 100.0% |
| 12:45-13:14 | 7 | 8.1% | 100.0% |
| 13:15-13:44 | 5 | 5.8% | 60.0% |
| 13:45-14:14 | 3 | 3.5% | 100.0% |
| 14:15-14:44 | 4 | 4.7% | 100.0% |
| 14:45-15:14 | 7 | 8.1% | 100.0% |
| 15:15-15:30 | 2 | 2.3% | 100.0% |

### Expiry vs Non-Expiry Timing

| Context | Count | Avg Minutes | Avg Time | Median Minutes | Median Time |
|---------|------:|------------:|---------:|---------------:|------------:|
| Expiry | 19 | 137 | ~11:31 | 140 | ~11:35 |
| Non-Expiry | 67 | 156 | ~11:50 | 145 | ~11:40 |

### VIX Regime Timing

| VIX Regime | Count | Avg Minutes | Avg Time | Median Time |
|------------|------:|------------:|---------:|------------:|
| Low (<15) | 52 | 161 | ~11:56 | ~11:45 |
| Normal (15-20) | 24 | 118 | ~11:12 | ~11:02 |
| Elevated (20-30) | 10 | 182 | ~12:17 | ~12:35 |

### Year-over-Year Timing

| Year | Count | Avg Minutes | Avg Time | Median Time |
|------|------:|------------:|---------:|------------:|
| 2020 | 5 | 209 | ~12:44 | ~12:50 |
| 2021 | 12 | 161 | ~11:55 | ~11:20 |
| 2022 | 9 | 136 | ~11:30 | ~11:20 |
| 2023 | 16 | 187 | ~12:22 | ~12:00 |
| 2024 | 15 | 158 | ~11:53 | ~11:55 |
| 2025 | 21 | 119 | ~11:13 | ~10:55 |
| 2026 | 8 | 121 | ~11:16 | ~10:42 |

### Fastest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2022-09-14 | 09:15 | 0 | 0.65% | 1.1% | 1.29% | Worked |
| 2025-11-26 | 09:15 | 0 | 0.49% | 0.77% | 1.4% | Worked |
| 2021-11-30 | 09:20 | 5 | 0.842% | 1.31% | -0.45% | Failed |
| 2023-03-06 | 09:20 | 5 | 0.424% | 0.77% | 0.22% | Worked |
| 2025-04-03 | 09:20 | 5 | 0.451% | 0.86% | 0.39% | Worked |
| 2022-04-04 | 09:25 | 10 | 0.674% | 1.16% | 1.27% | Worked |
| 2024-06-07 | 09:25 | 10 | 0.532% | 1.06% | 1.96% | Worked |
| 2026-02-04 | 09:25 | 10 | 0.441% | 0.81% | 0.24% | Worked |
| 2021-12-31 | 09:30 | 15 | 0.545% | 1.04% | 0.69% | Worked |
| 2025-05-26 | 09:30 | 15 | 0.548% | 1.09% | 0.31% | Worked |

### Slowest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2024-08-21 | 15:25 | 370 | 0.435% | 0.87% | 0.41% | Worked |
| 2026-07-30 | 15:25 | 370 | 0.385% | 0.76% | 0.19% | Worked |
| 2020-12-04 | 15:10 | 355 | 0.629% | 1.2% | 0.71% | Worked |
| 2023-07-14 | 15:10 | 355 | 0.384% | 0.69% | 0.48% | Worked |
| 2025-12-12 | 15:10 | 355 | 0.333% | 0.66% | 0.28% | Worked |
| 2021-12-22 | 15:00 | 345 | 0.57% | 1.1% | 0.61% | Worked |
| 2023-06-27 | 15:00 | 345 | 0.363% | 0.72% | 0.37% | Worked |
| 2021-08-16 | 14:50 | 335 | 0.422% | 0.82% | 0.17% | Worked |
| 2023-02-15 | 14:50 | 335 | 0.436% | 0.85% | 0.71% | Worked |
| 2021-01-20 | 14:15 | 300 | 0.726% | 1.44% | 0.58% | Worked |

## Bearish Alignment — Exceeded Half (153 days)

When did the bearish (low from open) move first cross half the VIX-predicted range?

### Timing Statistics

| Statistic | Minutes from Open | Clock Time |
|-----------|------------------:|-----------:|
| Average | 117 min | ~11:12 |
| Median | 70 min | ~10:25 |
| 25th percentile | 25 min | ~9:40 |
| 75th percentile | 200 min | ~12:35 |
| Earliest | 0 min | ~9:15 |
| Latest | 370 min | ~15:25 |

### Session Distribution

| Session | Count | % | Cumulative % |
|---------|------:|--:|-----------:|
| Opening (9:15-9:44) | 44 | 28.8% | 28.8% |
| Early Morning (9:45-10:29) | 35 | 22.9% | 51.7% |
| Late Morning (10:30-11:29) | 21 | 13.7% | 65.4% |
| Midday (11:30-12:29) | 11 | 7.2% | 72.6% |
| Early Afternoon (12:30-13:29) | 15 | 9.8% | 82.4% |
| Late Afternoon (13:30-14:29) | 10 | 6.5% | 88.9% |
| Closing (14:30-15:30) | 17 | 11.1% | 100.0% |

### Win Rate by Cross Time

Does earlier crossing predict higher win rate?

| Session | Count | Worked and Remained | WR% |
|---------|------:|--------------------:|----:|
| Opening (9:15-9:44) | 44 | 36 | 81.8% |
| Early Morning (9:45-10:29) | 35 | 28 | 80.0% |
| Late Morning (10:30-11:29) | 21 | 13 | 61.9% |
| Midday (11:30-12:29) | 11 | 10 | 90.9% |
| Early Afternoon (12:30-13:29) | 15 | 14 | 93.3% |
| Late Afternoon (13:30-14:29) | 10 | 10 | 100.0% |
| Closing (14:30-15:30) | 17 | 17 | 100.0% |

### 30-Minute Bucket Distribution

| Time Window | Count | % | WR% |
|-------------|------:|--:|----:|
| 09:15-09:44 | 44 | 28.8% | 81.8% |
| 09:45-10:14 | 25 | 16.3% | 76.0% |
| 10:15-10:44 | 15 | 9.8% | 80.0% |
| 10:45-11:14 | 14 | 9.2% | 71.4% |
| 11:15-11:44 | 4 | 2.6% | 50.0% |
| 11:45-12:14 | 5 | 3.3% | 80.0% |
| 12:15-12:44 | 9 | 5.9% | 100.0% |
| 12:45-13:14 | 3 | 2.0% | 100.0% |
| 13:15-13:44 | 11 | 7.2% | 90.9% |
| 13:45-14:14 | 4 | 2.6% | 100.0% |
| 14:15-14:44 | 10 | 6.5% | 100.0% |
| 14:45-15:14 | 7 | 4.6% | 100.0% |
| 15:15-15:30 | 2 | 1.3% | 100.0% |

### Expiry vs Non-Expiry Timing

| Context | Count | Avg Minutes | Avg Time | Median Minutes | Median Time |
|---------|------:|------------:|---------:|---------------:|------------:|
| Expiry | 42 | 131 | ~11:26 | 90 | ~10:45 |
| Non-Expiry | 111 | 112 | ~11:06 | 65 | ~10:20 |

### VIX Regime Timing

| VIX Regime | Count | Avg Minutes | Avg Time | Median Time |
|------------|------:|------------:|---------:|------------:|
| Low (<15) | 93 | 128 | ~11:22 | ~10:40 |
| Normal (15-20) | 38 | 81 | ~10:36 | ~10:02 |
| Elevated (20-30) | 22 | 134 | ~11:28 | ~10:20 |

### Year-over-Year Timing

| Year | Count | Avg Minutes | Avg Time | Median Time |
|------|------:|------------:|---------:|------------:|
| 2020 | 4 | 48 | ~10:02 | ~9:47 |
| 2021 | 18 | 93 | ~10:48 | ~9:37 |
| 2022 | 31 | 121 | ~11:16 | ~10:25 |
| 2023 | 37 | 134 | ~11:29 | ~11:10 |
| 2024 | 25 | 95 | ~10:50 | ~9:55 |
| 2025 | 25 | 157 | ~11:52 | ~10:50 |
| 2026 | 13 | 79 | ~10:33 | ~10:10 |

### Fastest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2020-09-01 | 09:15 | 0 | 0.817% | 1.44% | 0.26% | Failed |
| 2021-07-28 | 09:15 | 0 | 0.666% | 0.83% | -0.3% | Worked |
| 2021-10-25 | 09:15 | 0 | 0.808% | 1.11% | -0.51% | Worked |
| 2021-11-29 | 09:15 | 0 | 1.281% | 1.31% | -0.09% | Worked |
| 2021-12-20 | 09:15 | 0 | 0.613% | 1.03% | -1.26% | Worked |
| 2022-01-19 | 09:15 | 0 | 0.573% | 1.12% | -1.04% | Worked |
| 2022-02-14 | 09:15 | 0 | 0.771% | 1.18% | -1.5% | Worked |
| 2024-11-08 | 09:15 | 0 | 0.54% | 0.94% | -0.4% | Worked |
| 2025-07-25 | 09:15 | 0 | 0.346% | 0.68% | -0.71% | Worked |
| 2021-03-25 | 09:20 | 5 | 0.872% | 1.41% | -1.54% | Worked |

### Slowest Threshold Crosses (Top 10)

| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |
|------|-----------|--------:|---------------:|---------------:|-------:|---------|
| 2025-04-30 | 15:25 | 370 | 0.589% | 1.09% | -0.39% | Worked |
| 2021-06-30 | 15:15 | 360 | 0.412% | 0.82% | -0.29% | Worked |
| 2022-12-07 | 15:10 | 355 | 0.475% | 0.88% | -0.47% | Worked |
| 2021-04-30 | 15:05 | 350 | 0.761% | 1.47% | -0.88% | Worked |
| 2026-02-13 | 15:05 | 350 | 0.388% | 0.74% | -0.43% | Worked |
| 2025-11-24 | 15:00 | 345 | 0.557% | 0.86% | -0.69% | Worked |
| 2025-11-25 | 15:00 | 345 | 0.499% | 0.83% | -0.53% | Worked |
| 2024-05-30 | 14:55 | 340 | 0.886% | 1.52% | -0.27% | Worked |
| 2023-06-01 | 14:45 | 330 | 0.399% | 0.75% | -0.5% | Worked |
| 2023-07-13 | 14:40 | 325 | 0.427% | 0.69% | -0.27% | Worked |

## Early vs Late Cross: Does Timing Predict Close Outcome?

Split at the median cross time for each alignment type.

### Bullish Alignment (Median: 142 min = ~11:37)

| Timing | Count | Worked and Remained | WR% | Avg Close% |
|--------|------:|--------------------:|----:|-----------:|
| Early (≤ median) | 43 | 39 | 90.7% | 0.675% |
| Late (> median) | 43 | 39 | 90.7% | 0.497% |

### Bearish Alignment (Median: 70 min = ~10:25)

| Timing | Count | Worked and Remained | WR% | Avg Close% |
|--------|------:|--------------------:|----:|-----------:|
| Early (≤ median) | 79 | 64 | 81.0% | -0.482% |
| Late (> median) | 74 | 64 | 86.5% | -0.399% |

## First Hour Rule: Cross Before 10:15 AM

If the threshold is crossed within the first hour (by 10:15 AM), is the signal stronger?

### Bullish Alignment

| Timing | Count | % | Worked and Remained | WR% | Avg Close% |
|--------|------:|--:|--------------------:|----:|-----------:|
| Within first hour (≤10:15) | 24 | 27.9% | 21 | 87.5% | 0.722% |
| After first hour (>10:15) | 62 | 72.1% | 57 | 91.9% | 0.533% |

### Bearish Alignment

| Timing | Count | % | Worked and Remained | WR% | Avg Close% |
|--------|------:|--:|--------------------:|----:|-----------:|
| Within first hour (≤10:15) | 74 | 48.4% | 60 | 81.1% | -0.48% |
| After first hour (>10:15) | 79 | 51.6% | 68 | 86.1% | -0.406% |

## Practical Interpretation

**Bullish Alignment**: Median threshold cross at **11:37** (142 minutes from open)

**Bearish Alignment**: Median threshold cross at **10:25** (70 minutes from open)

```
Caveat: FII/PRO alignment is only known after T+1 settlement.
The timing analysis answers: IF you knew the alignment,
by what time would the VIX threshold typically be crossed?
This is useful for post-hoc pattern recognition, not real-time trading.
```
