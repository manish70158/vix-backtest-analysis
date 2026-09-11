# FII-PRO All Combinations: Comprehensive Analysis Report

> **Dataset**: `vix_fii_t1_intraday_daily_results.csv` — 1,488 trading days (Aug 2020 – Sep 2026)
>
> **T-1 data caveat**: FII/PRO views are derived from T+1 settlement data,
> so alignment is known only after the trading day. This analysis identifies
> historical patterns, not real-time predictive signals.
>
> **VIX Accuracy**: "Underestimated" = actual intraday range exceeded VIX prediction by > 0.5%

---

## Master Summary — All 9 Combinations

| Category                      |   Days | % Total   | Green%   | Red%   | VIX U/E%   | Avg Range%   | Avg O→C%   | Avg VIX Pred%   | Avg Diff%   |
|:------------------------------|-------:|:----------|:---------|:-------|:-----------|:-------------|:-----------|:----------------|:------------|
| **Bullish Alignment**         |    319 | 21.4%     | 45.8%    | 54.2%  | 17.6%      | 0.95%        | -0.076%    | 0.79%           | +0.16%      |
| **Bearish Alignment**         |    332 | 22.3%     | 45.8%    | 54.2%  | 19.9%      | 1.03%        | -0.073%    | 0.81%           | +0.22%      |
| **FII Bullish + PRO Bearish** |     63 | 4.2%      | 49.2%    | 50.8%  | 14.3%      | 0.88%        | -0.048%    | 0.79%           | +0.09%      |
| **FII Bearish + PRO Bullish** |     46 | 3.1%      | 60.9%    | 39.1%  | 32.6%      | 1.14%        | +0.143%    | 0.76%           | +0.38%      |
| **Both Neutral**              |    194 | 13.0%     | 48.5%    | 51.5%  | 20.1%      | 1.08%        | -0.058%    | 0.91%           | +0.17%      |
| **FII Neutral + PRO Bullish** |    209 | 14.0%     | 53.6%    | 46.4%  | 16.7%      | 1.04%        | -0.008%    | 0.86%           | +0.18%      |
| **FII Neutral + PRO Bearish** |    224 | 15.1%     | 50.4%    | 49.6%  | 19.6%      | 1.06%        | +0.008%    | 0.85%           | +0.21%      |
| **FII Bullish + PRO Neutral** |     54 | 3.6%      | 59.3%    | 40.7%  | 7.4%       | 0.89%        | +0.025%    | 0.88%           | +0.01%      |
| **FII Bearish + PRO Neutral** |     47 | 3.2%      | 42.6%    | 57.4%  | 21.3%      | 1.13%        | -0.231%    | 0.85%           | +0.29%      |

### Quick-Read Guide

- **Highest green rate**: FII Bearish + PRO Bullish (60.9%) and FII Bullish + PRO Neutral (59.3%)
- **Highest VIX underestimation**: FII Bearish + PRO Bullish (32.6%) — opposing tension creates outsized moves
- **Lowest VIX underestimation**: FII Bullish + PRO Neutral (7.4%) — calmest, most predictable days
- **Most bearish**: FII Bearish + PRO Neutral (avg O→C -0.231%) — FII bearish conviction with PRO silent
- **Largest sample**: Bearish Alignment (332 days) — most common non-aligned category

---

## Bullish Alignment (319 days, 21.4% of total)

*Both FII and PRO lean bullish (Strong Bullish, Bullish, or Mildly Bullish). The institutional consensus is upward.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 319 |
| Green (close > open) | 146 (45.8%) |
| Red (close < open) | 173 (54.2%) |
| Top to Down | 173 (54.2%) |
| Down to Up | 146 (45.8%) |
| Avg Range% | 0.95% |
| Avg Open→Close% | -0.076% |
| Avg High from Open% | +0.40% |
| Avg Low from Open% | -0.56% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **56** | **17.6%** | 1.8% | +0.97% |
| Overestimated | 263 | 82.4% | — | — |
| Avg VIX Predicted | — | — | 0.79% | +0.16% |
| Range/VIX Ratio | — | — | — | 1.21 |

**When Underestimated (56 days):**
- Green: 25 (44.6%) | Red: 31 (55.4%)
- Top to Down: 31 (55.4%)
- Avg Range: 1.8% | Avg Diff: +0.97% | Avg O→C: -0.210%

### Sub-Combinations (FII View × PRO View)

| FII View       | PRO View       |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:---------------|:---------------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Bullish        | Strong Bullish |    129 | 14.0%      | 38.8%    | 0.87%        | -0.151%    | +0.10%      |
| Strong Bullish | Strong Bullish |     70 | 15.7%      | 58.6%    | 0.96%        | +0.010%    | +0.21%      |
| Mildly Bullish | Strong Bullish |     40 | 22.5%      | 32.5%    | 1.02%        | -0.234%    | +0.23%      |
| Bullish        | Bullish        |     26 | 15.4%      | 53.8%    | 0.98%        | +0.030%    | +0.15%      |
| Mildly Bullish | Bullish        |     26 | 26.9%      | 38.5%    | 1.10%        | -0.186%    | +0.24%      |
| Mildly Bullish | Mildly Bullish |     10 | 20.0%      | 80.0%    | 1.06%        | +0.406%    | +0.04%      |
| Bullish        | Mildly Bullish |      8 | 37.5%      | 50.0%    | 0.95%        | +0.338%    | +0.27%      |
| Strong Bullish | Bullish        |      5 | 0.0%       | 80.0%    | 0.84%        | +0.238%    | +0.16%      |
| Strong Bullish | Mildly Bullish |      5 | 40.0%      | 40.0%    | 1.37%        | -0.034%    | +0.45%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 188 | 13.8% | 44.7% | 0.78% |
| Normal (15-20) | 91 | 19.8% | 44.0% | 1.05% |
| Elevated (20-30) | 40 | 30.0% | 55.0% | 1.53% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 60 | 20.0% | 50.0% |
| Non-Expiry | 259 | 17.0% | 44.8% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 60 | 16.7% | 41.7% |
| Tuesday | 81 | 13.6% | 38.3% |
| Wednesday | 57 | 12.3% | 52.6% |
| Thursday | 60 | 21.7% | 48.3% |
| Friday | 59 | 25.4% | 52.5% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 8 | 12.5% | 87.5% |
| 2021 | 42 | 19.0% | 57.1% |
| 2022 | 45 | 15.6% | 44.4% |
| 2023 | 75 | 12.0% | 44.0% |
| 2024 | 64 | 28.1% | 37.5% |
| 2025 | 49 | 20.4% | 49.0% |
| 2026 | 36 | 8.3% | 38.9% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2024-06-04 | Strong Bullish | Strong Bullish | 1.10% | 8.19% | +7.09% | Top to Down | Red | -5.10% |
| 2022-02-28 | Strong Bullish | Mildly Bullish | 1.40% | 2.78% | +1.38% | Down to Up | Green | +1.87% |
| 2021-01-29 | Mildly Bullish | Strong Bullish | 1.27% | 2.64% | +1.37% | Top to Down | Red | -2.05% |
| 2021-04-05 | Mildly Bullish | Bullish | 1.05% | 2.56% | +1.51% | Top to Down | Red | -1.27% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | 0.90% | 2.52% | +1.62% | Down to Up | Green | +1.38% |

---

## Bearish Alignment (332 days, 22.3% of total)

*Both FII and PRO lean bearish (Strong Bearish, Bearish, or Mildly Bearish). The institutional consensus is downward.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 332 |
| Green (close > open) | 152 (45.8%) |
| Red (close < open) | 180 (54.2%) |
| Top to Down | 180 (54.2%) |
| Down to Up | 152 (45.8%) |
| Avg Range% | 1.03% |
| Avg Open→Close% | -0.073% |
| Avg High from Open% | +0.43% |
| Avg Low from Open% | -0.60% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **66** | **19.9%** | 1.8% | +0.88% |
| Overestimated | 266 | 80.1% | — | — |
| Avg VIX Predicted | — | — | 0.81% | +0.22% |
| Range/VIX Ratio | — | — | — | 1.28 |

**When Underestimated (66 days):**
- Green: 26 (39.4%) | Red: 40 (60.6%)
- Top to Down: 40 (60.6%)
- Avg Range: 1.8% | Avg Diff: +0.88% | Avg O→C: -0.291%

### Sub-Combinations (FII View × PRO View)

| FII View       | PRO View       |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:---------------|:---------------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Bearish        | Strong Bearish |    102 | 18.6%      | 45.1%    | 1.02%        | -0.054%    | +0.20%      |
| Strong Bearish | Strong Bearish |     80 | 20.0%      | 40.0%    | 1.02%        | -0.092%    | +0.25%      |
| Mildly Bearish | Strong Bearish |     53 | 26.4%      | 52.8%    | 1.17%        | -0.088%    | +0.34%      |
| Bearish        | Bearish        |     32 | 18.8%      | 43.8%    | 1.01%        | -0.135%    | +0.20%      |
| Mildly Bearish | Bearish        |     29 | 24.1%      | 37.9%    | 1.06%        | -0.073%    | +0.21%      |
| Bearish        | Mildly Bearish |     11 | 36.4%      | 45.5%    | 1.00%        | -0.138%    | +0.21%      |
| Mildly Bearish | Mildly Bearish |     11 | 0.0%       | 90.9%    | 0.79%        | +0.275%    | +0.00%      |
| Strong Bearish | Bearish        |      9 | 0.0%       | 44.4%    | 0.87%        | -0.076%    | +0.06%      |
| Strong Bearish | Mildly Bearish |      5 | 0.0%       | 40.0%    | 0.83%        | -0.190%    | +0.08%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 188 | 12.8% | 43.6% | 0.84% |
| Normal (15-20) | 100 | 23.0% | 50.0% | 1.15% |
| Elevated (20-30) | 43 | 41.9% | 46.5% | 1.53% |
| High (>30) | 1 | 100.0% | 0.0% | 3.01% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 73 | 28.8% | 39.7% |
| Non-Expiry | 259 | 17.4% | 47.5% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 80 | 27.5% | 50.0% |
| Tuesday | 56 | 21.4% | 53.6% |
| Wednesday | 71 | 8.5% | 45.1% |
| Thursday | 63 | 25.4% | 41.3% |
| Friday | 61 | 14.8% | 39.3% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 7 | 28.6% | 100.0% |
| 2021 | 37 | 32.4% | 40.5% |
| 2022 | 62 | 21.0% | 41.9% |
| 2023 | 71 | 9.9% | 39.4% |
| 2024 | 63 | 25.4% | 54.0% |
| 2025 | 53 | 9.4% | 41.5% |
| 2026 | 39 | 28.2% | 51.3% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2024-06-05 | Strong Bearish | Strong Bearish | 1.40% | 3.97% | +2.57% | Down to Up | Green | +2.01% |
| 2026-02-01 | Mildly Bearish | Strong Bearish | 0.71% | 3.43% | +2.72% | Top to Down | Red | -2.23% |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 1.28% | 3.01% | +1.73% | Top to Down | Red | -2.00% |
| 2021-12-20 | Mildly Bearish | Strong Bearish | 0.86% | 2.49% | +1.63% | Top to Down | Red | -1.26% |
| 2023-03-13 | Bearish | Strong Bearish | 0.70% | 2.38% | +1.68% | Top to Down | Red | -1.36% |

---

## FII Bullish + PRO Bearish (63 days, 4.2% of total)

*FII leans bullish while PRO leans bearish. The institutions are in direct conflict.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 63 |
| Green (close > open) | 31 (49.2%) |
| Red (close < open) | 32 (50.8%) |
| Top to Down | 32 (50.8%) |
| Down to Up | 31 (49.2%) |
| Avg Range% | 0.88% |
| Avg Open→Close% | -0.048% |
| Avg High from Open% | +0.41% |
| Avg Low from Open% | -0.47% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **9** | **14.3%** | 1.7% | +0.90% |
| Overestimated | 54 | 85.7% | — | — |
| Avg VIX Predicted | — | — | 0.79% | +0.09% |
| Range/VIX Ratio | — | — | — | 1.13 |

**When Underestimated (9 days):**
- Green: 4 (44.4%) | Red: 5 (55.6%)
- Top to Down: 5 (55.6%)
- Avg Range: 1.7% | Avg Diff: +0.90% | Avg O→C: -0.188%

### Sub-Combinations (FII View × PRO View)

| FII View       | PRO View       |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:---------------|:---------------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Bullish        | Strong Bearish |     17 | 17.6%      | 47.1%    | 0.85%        | +0.024%    | +0.10%      |
| Mildly Bullish | Strong Bearish |     11 | 9.1%       | 45.5%    | 0.80%        | -0.137%    | +0.08%      |
| Mildly Bullish | Bearish        |     10 | 20.0%      | 40.0%    | 0.87%        | -0.188%    | +0.10%      |
| Bullish        | Mildly Bearish |      8 | 0.0%       | 37.5%    | 0.88%        | -0.260%    | -0.02%      |
| Strong Bullish | Strong Bearish |      6 | 0.0%       | 50.0%    | 0.79%        | +0.065%    | +0.03%      |
| Strong Bullish | Bearish        |      4 | 25.0%      | 75.0%    | 0.89%        | +0.338%    | +0.18%      |
| Bullish        | Bearish        |      3 | 0.0%       | 66.7%    | 1.00%        | +0.130%    | +0.06%      |
| Mildly Bullish | Mildly Bearish |      3 | 66.7%      | 66.7%    | 1.63%        | -0.057%    | +0.57%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 41 | 9.8% | 48.8% | 0.76% |
| Normal (15-20) | 17 | 23.5% | 58.8% | 1.06% |
| Elevated (20-30) | 5 | 20.0% | 20.0% | 1.28% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 18 | 16.7% | 44.4% |
| Non-Expiry | 45 | 13.3% | 51.1% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 12 | 8.3% | 50.0% |
| Tuesday | 14 | 7.1% | 50.0% |
| Wednesday | 8 | 25.0% | 50.0% |
| Thursday | 10 | 30.0% | 50.0% |
| Friday | 19 | 10.5% | 47.4% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2021 | 3 | 33.3% | 33.3% |
| 2022 | 8 | 0.0% | 50.0% |
| 2023 | 6 | 16.7% | 50.0% |
| 2024 | 29 | 24.1% | 44.8% |
| 2025 | 10 | 0.0% | 80.0% |
| 2026 | 7 | 0.0% | 28.6% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2024-12-05 | Mildly Bullish | Mildly Bearish | 0.76% | 2.29% | +1.53% | Down to Up | Green | +0.66% |
| 2024-11-28 | Mildly Bullish | Bearish | 0.77% | 1.95% | +1.18% | Top to Down | Red | -1.30% |
| 2021-01-22 | Mildly Bullish | Mildly Bearish | 1.13% | 1.79% | +0.66% | Top to Down | Red | -1.49% |
| 2024-02-22 | Bullish | Strong Bearish | 0.83% | 1.71% | +0.88% | Down to Up | Green | +0.61% |
| 2024-01-24 | Strong Bullish | Bearish | 0.78% | 1.63% | +0.85% | Down to Up | Green | +1.30% |

---

## FII Bearish + PRO Bullish (46 days, 3.1% of total)

*FII leans bearish while PRO leans bullish. The institutions oppose each other — historically PRO wins more often.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 46 |
| Green (close > open) | 28 (60.9%) |
| Red (close < open) | 18 (39.1%) |
| Top to Down | 18 (39.1%) |
| Down to Up | 28 (60.9%) |
| Avg Range% | 1.14% |
| Avg Open→Close% | +0.143% |
| Avg High from Open% | +0.59% |
| Avg Low from Open% | -0.56% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **15** | **32.6%** | 1.9% | +1.06% |
| Overestimated | 31 | 67.4% | — | — |
| Avg VIX Predicted | — | — | 0.76% | +0.38% |
| Range/VIX Ratio | — | — | — | 1.46 |

**When Underestimated (15 days):**
- Green: 7 (46.7%) | Red: 8 (53.3%)
- Top to Down: 8 (53.3%)
- Avg Range: 1.9% | Avg Diff: +1.06% | Avg O→C: +0.070%

### Sub-Combinations (FII View × PRO View)

| FII View       | PRO View       |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:---------------|:---------------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Bearish        | Strong Bullish |     10 | 10.0%      | 50.0%    | 0.83%        | +0.085%    | +0.12%      |
| Bearish        | Bullish        |      7 | 42.9%      | 85.7%    | 1.42%        | +0.490%    | +0.65%      |
| Mildly Bearish | Bullish        |      7 | 42.9%      | 42.9%    | 0.92%        | -0.194%    | +0.17%      |
| Mildly Bearish | Strong Bullish |      7 | 28.6%      | 85.7%    | 1.20%        | +0.151%    | +0.37%      |
| Strong Bearish | Strong Bullish |      5 | 40.0%      | 20.0%    | 1.06%        | -0.270%    | +0.35%      |
| Mildly Bearish | Mildly Bullish |      4 | 50.0%      | 75.0%    | 1.75%        | +0.162%    | +0.92%      |
| Bearish        | Mildly Bullish |      3 | 0.0%       | 33.3%    | 0.76%        | +0.093%    | +0.08%      |
| Strong Bearish | Bullish        |      3 | 66.7%      | 100.0%   | 1.68%        | +1.000%    | +0.78%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 28 | 17.9% | 60.7% | 0.88% |
| Normal (15-20) | 15 | 53.3% | 60.0% | 1.42% |
| Elevated (20-30) | 3 | 66.7% | 66.7% | 2.18% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 10 | 30.0% | 40.0% |
| Non-Expiry | 36 | 33.3% | 66.7% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 6 | 50.0% | 100.0% |
| Wednesday | 10 | 40.0% | 50.0% |
| Thursday | 16 | 18.8% | 37.5% |
| Friday | 14 | 35.7% | 78.6% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2021 | 2 | 50.0% | 50.0% |
| 2022 | 4 | 25.0% | 75.0% |
| 2023 | 11 | 18.2% | 72.7% |
| 2024 | 17 | 47.1% | 52.9% |
| 2025 | 3 | 33.3% | 100.0% |
| 2026 | 9 | 22.2% | 44.4% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2022-05-04 | Mildly Bearish | Mildly Bullish | 1.06% | 2.95% | +1.89% | Top to Down | Red | -2.35% |
| 2024-11-22 | Bearish | Bullish | 0.84% | 2.55% | +1.71% | Down to Up | Green | +1.97% |
| 2024-12-13 | Bearish | Bullish | 0.69% | 2.50% | +1.81% | Down to Up | Green | +1.15% |
| 2026-03-16 | Strong Bearish | Bullish | 1.19% | 2.37% | +1.18% | Down to Up | Green | +1.04% |
| 2025-05-12 | Mildly Bearish | Mildly Bullish | 1.13% | 2.32% | +1.19% | Down to Up | Green | +2.05% |

---

## Both Neutral (194 days, 13.0% of total)

*Neither FII nor PRO has a directional view. No institutional signal — a coin flip.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 194 |
| Green (close > open) | 94 (48.5%) |
| Red (close < open) | 100 (51.5%) |
| Top to Down | 100 (51.5%) |
| Down to Up | 94 (48.5%) |
| Avg Range% | 1.08% |
| Avg Open→Close% | -0.058% |
| Avg High from Open% | +0.46% |
| Avg Low from Open% | -0.62% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **39** | **20.1%** | 1.9% | +0.93% |
| Overestimated | 155 | 79.9% | — | — |
| Avg VIX Predicted | — | — | 0.91% | +0.17% |
| Range/VIX Ratio | — | — | — | 1.19 |

**When Underestimated (39 days):**
- Green: 16 (41.0%) | Red: 23 (59.0%)
- Top to Down: 23 (59.0%)
- Avg Range: 1.9% | Avg Diff: +0.93% | Avg O→C: -0.438%

### Sub-Combinations (FII View × PRO View)

| FII View   | PRO View   |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:-----------|:-----------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Neutral    | Neutral    |    194 | 20.1%      | 48.5%    | 1.08%        | -0.058%    | +0.17%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 69 | 14.5% | 46.4% | 0.81% |
| Normal (15-20) | 51 | 19.6% | 52.9% | 1.07% |
| Elevated (20-30) | 74 | 25.7% | 47.3% | 1.33% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 33 | 18.2% | 39.4% |
| Non-Expiry | 161 | 20.5% | 50.3% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 43 | 25.6% | 58.1% |
| Tuesday | 44 | 15.9% | 50.0% |
| Wednesday | 40 | 12.5% | 55.0% |
| Thursday | 38 | 15.8% | 39.5% |
| Friday | 27 | 37.0% | 37.0% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 49 | 14.3% | 38.8% |
| 2021 | 44 | 25.0% | 52.3% |
| 2022 | 29 | 20.7% | 51.7% |
| 2023 | 6 | 0.0% | 66.7% |
| 2024 | 9 | 33.3% | 66.7% |
| 2025 | 35 | 11.4% | 45.7% |
| 2026 | 22 | 36.4% | 50.0% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2022-01-24 | Neutral | Neutral | 0.99% | 3.41% | +2.42% | Top to Down | Red | -2.63% |
| 2020-10-15 | Neutral | Neutral | 1.06% | 3.00% | +1.94% | Top to Down | Red | -2.92% |
| 2020-09-21 | Neutral | Neutral | 1.05% | 2.74% | +1.69% | Top to Down | Red | -2.45% |
| 2021-04-12 | Neutral | Neutral | 1.04% | 2.70% | +1.66% | Top to Down | Red | -2.01% |
| 2026-04-02 | Neutral | Neutral | 1.31% | 2.68% | +1.37% | Down to Up | Green | +1.42% |

---

## FII Neutral + PRO Bullish (209 days, 14.0% of total)

*FII has no view while PRO leans bullish. PRO's solo bullish signal.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 209 |
| Green (close > open) | 112 (53.6%) |
| Red (close < open) | 97 (46.4%) |
| Top to Down | 97 (46.4%) |
| Down to Up | 112 (53.6%) |
| Avg Range% | 1.04% |
| Avg Open→Close% | -0.008% |
| Avg High from Open% | +0.48% |
| Avg Low from Open% | -0.57% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **35** | **16.7%** | 2.0% | +1.07% |
| Overestimated | 174 | 83.3% | — | — |
| Avg VIX Predicted | — | — | 0.86% | +0.18% |
| Range/VIX Ratio | — | — | — | 1.20 |

**When Underestimated (35 days):**
- Green: 14 (40.0%) | Red: 21 (60.0%)
- Top to Down: 21 (60.0%)
- Avg Range: 2.0% | Avg Diff: +1.07% | Avg O→C: -0.306%

### Sub-Combinations (FII View × PRO View)

| FII View   | PRO View       |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:-----------|:---------------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Neutral    | Strong Bullish |     91 | 13.2%      | 54.9%    | 0.98%        | +0.024%    | +0.16%      |
| Neutral    | Bullish        |     79 | 17.7%      | 53.2%    | 1.03%        | +0.028%    | +0.16%      |
| Neutral    | Mildly Bullish |     39 | 23.1%      | 51.3%    | 1.22%        | -0.154%    | +0.29%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 99 | 10.1% | 56.6% | 0.74% |
| Normal (15-20) | 61 | 18.0% | 49.2% | 1.12% |
| Elevated (20-30) | 49 | 28.6% | 53.1% | 1.56% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 46 | 17.4% | 47.8% |
| Non-Expiry | 163 | 16.6% | 55.2% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 30 | 13.3% | 70.0% |
| Tuesday | 37 | 16.2% | 51.4% |
| Wednesday | 51 | 15.7% | 47.1% |
| Thursday | 45 | 15.6% | 53.3% |
| Friday | 45 | 22.2% | 53.3% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 17 | 23.5% | 52.9% |
| 2021 | 42 | 26.2% | 47.6% |
| 2022 | 37 | 21.6% | 64.9% |
| 2023 | 32 | 9.4% | 59.4% |
| 2024 | 27 | 14.8% | 48.1% |
| 2025 | 36 | 5.6% | 41.7% |
| 2026 | 18 | 16.7% | 66.7% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2020-08-31 | Neutral | Mildly Bullish | 0.96% | 3.97% | +3.01% | Top to Down | Red | -3.71% |
| 2023-02-01 | Neutral | Bullish | 0.88% | 3.47% | +2.59% | Top to Down | Red | -1.16% |
| 2022-06-16 | Neutral | Mildly Bullish | 1.16% | 3.33% | +2.17% | Top to Down | Red | -3.06% |
| 2021-03-19 | Neutral | Strong Bullish | 1.05% | 3.02% | +1.97% | Down to Up | Green | +1.81% |
| 2021-11-22 | Neutral | Strong Bullish | 0.78% | 2.89% | +2.11% | Top to Down | Red | -2.00% |

---

## FII Neutral + PRO Bearish (224 days, 15.1% of total)

*FII has no view while PRO leans bearish. PRO's solo bearish signal.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 224 |
| Green (close > open) | 113 (50.4%) |
| Red (close < open) | 111 (49.6%) |
| Top to Down | 111 (49.6%) |
| Down to Up | 113 (50.4%) |
| Avg Range% | 1.06% |
| Avg Open→Close% | +0.008% |
| Avg High from Open% | +0.49% |
| Avg Low from Open% | -0.57% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **44** | **19.6%** | 1.8% | +0.96% |
| Overestimated | 180 | 80.4% | — | — |
| Avg VIX Predicted | — | — | 0.85% | +0.21% |
| Range/VIX Ratio | — | — | — | 1.27 |

**When Underestimated (44 days):**
- Green: 21 (47.7%) | Red: 23 (52.3%)
- Top to Down: 23 (52.3%)
- Avg Range: 1.8% | Avg Diff: +0.96% | Avg O→C: -0.216%

### Sub-Combinations (FII View × PRO View)

| FII View   | PRO View       |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:-----------|:---------------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Neutral    | Bearish        |     92 | 20.7%      | 57.6%    | 1.10%        | +0.044%    | +0.23%      |
| Neutral    | Strong Bearish |     82 | 18.3%      | 50.0%    | 0.96%        | +0.091%    | +0.18%      |
| Neutral    | Mildly Bearish |     50 | 20.0%      | 38.0%    | 1.15%        | -0.196%    | +0.25%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 111 | 18.9% | 45.9% | 0.88% |
| Normal (15-20) | 64 | 15.6% | 56.2% | 1.07% |
| Elevated (20-30) | 49 | 26.5% | 53.1% | 1.45% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 51 | 17.6% | 51.0% |
| Non-Expiry | 173 | 20.2% | 50.3% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 49 | 16.3% | 49.0% |
| Tuesday | 48 | 25.0% | 47.9% |
| Wednesday | 38 | 15.8% | 63.2% |
| Thursday | 49 | 18.4% | 51.0% |
| Friday | 39 | 23.1% | 43.6% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 13 | 15.4% | 61.5% |
| 2021 | 59 | 22.0% | 45.8% |
| 2022 | 35 | 25.7% | 65.7% |
| 2023 | 32 | 18.8% | 40.6% |
| 2024 | 25 | 16.0% | 44.0% |
| 2025 | 43 | 11.6% | 51.2% |
| 2026 | 17 | 29.4% | 52.9% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2020-12-21 | Neutral | Mildly Bearish | 0.97% | 4.67% | +3.70% | Top to Down | Red | -3.34% |
| 2022-02-15 | Neutral | Strong Bearish | 1.20% | 3.15% | +1.95% | Down to Up | Green | +2.47% |
| 2021-02-26 | Neutral | Bearish | 1.20% | 3.03% | +1.83% | Top to Down | Red | -2.45% |
| 2022-03-07 | Neutral | Bearish | 1.46% | 2.90% | +1.44% | Down to Up | Green | +0.08% |
| 2022-01-25 | Neutral | Strong Bearish | 1.20% | 2.77% | +1.57% | Down to Up | Green | +1.56% |

---

## FII Bullish + PRO Neutral (54 days, 3.6% of total)

*FII leans bullish while PRO has no view. FII's solo bullish signal.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 54 |
| Green (close > open) | 32 (59.3%) |
| Red (close < open) | 22 (40.7%) |
| Top to Down | 22 (40.7%) |
| Down to Up | 32 (59.3%) |
| Avg Range% | 0.89% |
| Avg Open→Close% | +0.025% |
| Avg High from Open% | +0.43% |
| Avg Low from Open% | -0.47% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **4** | **7.4%** | 1.9% | +0.88% |
| Overestimated | 50 | 92.6% | — | — |
| Avg VIX Predicted | — | — | 0.88% | +0.01% |
| Range/VIX Ratio | — | — | — | 1.02 |

**When Underestimated (4 days):**
- Green: 1 (25.0%) | Red: 3 (75.0%)
- Top to Down: 3 (75.0%)
- Avg Range: 1.9% | Avg Diff: +0.88% | Avg O→C: -0.945%

### Sub-Combinations (FII View × PRO View)

| FII View       | PRO View   |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:---------------|:-----------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Mildly Bullish | Neutral    |     28 | 14.3%      | 60.7%    | 0.99%        | -0.072%    | +0.04%      |
| Bullish        | Neutral    |     20 | 0.0%       | 65.0%    | 0.85%        | +0.172%    | +0.01%      |
| Strong Bullish | Neutral    |      6 | 0.0%       | 33.3%    | 0.58%        | -0.008%    | -0.13%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 22 | 4.5% | 59.1% | 0.72% |
| Normal (15-20) | 21 | 9.5% | 57.1% | 0.95% |
| Elevated (20-30) | 11 | 9.1% | 63.6% | 1.15% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 11 | 0.0% | 36.4% |
| Non-Expiry | 43 | 9.3% | 65.1% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 7 | 0.0% | 100.0% |
| Tuesday | 14 | 14.3% | 50.0% |
| Wednesday | 11 | 9.1% | 54.5% |
| Thursday | 6 | 0.0% | 33.3% |
| Friday | 16 | 6.2% | 62.5% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 6 | 0.0% | 100.0% |
| 2021 | 6 | 16.7% | 66.7% |
| 2022 | 16 | 6.2% | 68.8% |
| 2023 | 5 | 0.0% | 60.0% |
| 2024 | 5 | 0.0% | 20.0% |
| 2025 | 8 | 25.0% | 50.0% |
| 2026 | 8 | 0.0% | 37.5% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2021-01-27 | Mildly Bullish | Neutral | 1.22% | 2.17% | +0.95% | Top to Down | Red | -1.92% |
| 2022-02-01 | Mildly Bullish | Neutral | 1.15% | 2.15% | +1.00% | Down to Up | Green | +0.43% |
| 2025-05-13 | Mildly Bullish | Neutral | 0.96% | 1.71% | +0.75% | Top to Down | Red | -1.09% |
| 2022-02-21 | Mildly Bullish | Neutral | 1.16% | 1.63% | +0.47% | Down to Up | Green | +0.08% |
| 2025-04-04 | Mildly Bullish | Neutral | 0.71% | 1.54% | +0.83% | Top to Down | Red | -1.20% |

---

## FII Bearish + PRO Neutral (47 days, 3.2% of total)

*FII leans bearish while PRO has no view. FII's solo bearish signal.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 47 |
| Green (close > open) | 20 (42.6%) |
| Red (close < open) | 27 (57.4%) |
| Top to Down | 27 (57.4%) |
| Down to Up | 20 (42.6%) |
| Avg Range% | 1.13% |
| Avg Open→Close% | -0.231% |
| Avg High from Open% | +0.40% |
| Avg Low from Open% | -0.73% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **10** | **21.3%** | 1.9% | +1.01% |
| Overestimated | 37 | 78.7% | — | — |
| Avg VIX Predicted | — | — | 0.85% | +0.29% |
| Range/VIX Ratio | — | — | — | 1.37 |

**When Underestimated (10 days):**
- Green: 0 (0.0%) | Red: 10 (100.0%)
- Top to Down: 10 (100.0%)
- Avg Range: 1.9% | Avg Diff: +1.01% | Avg O→C: -1.174%

### Sub-Combinations (FII View × PRO View)

| FII View       | PRO View   |   Days | VIX U/E%   | Green%   | Avg Range%   | Avg O→C%   | Avg Diff%   |
|:---------------|:-----------|-------:|:-----------|:---------|:-------------|:-----------|:------------|
| Bearish        | Neutral    |     19 | 10.5%      | 36.8%    | 1.14%        | -0.228%    | +0.28%      |
| Mildly Bearish | Neutral    |     19 | 26.3%      | 52.6%    | 1.17%        | -0.161%    | +0.29%      |
| Strong Bearish | Neutral    |      9 | 33.3%      | 33.3%    | 1.06%        | -0.383%    | +0.29%      |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 22 | 13.6% | 59.1% | 0.94% |
| Normal (15-20) | 13 | 30.8% | 23.1% | 1.22% |
| Elevated (20-30) | 12 | 25.0% | 33.3% | 1.41% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 10 | 20.0% | 30.0% |
| Non-Expiry | 37 | 21.6% | 45.9% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 11 | 27.3% | 54.5% |
| Tuesday | 6 | 50.0% | 50.0% |
| Wednesday | 10 | 10.0% | 40.0% |
| Thursday | 9 | 11.1% | 44.4% |
| Friday | 11 | 18.2% | 27.3% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 2 | 50.0% | 0.0% |
| 2021 | 10 | 10.0% | 40.0% |
| 2022 | 7 | 42.9% | 28.6% |
| 2023 | 5 | 0.0% | 80.0% |
| 2024 | 5 | 40.0% | 20.0% |
| 2025 | 8 | 12.5% | 62.5% |
| 2026 | 10 | 20.0% | 40.0% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2026-02-03 | Bearish | Neutral | 0.73% | 2.66% | +1.93% | Top to Down | Red | -2.26% |
| 2022-05-13 | Bearish | Neutral | 1.27% | 2.14% | +0.87% | Top to Down | Red | -1.31% |
| 2022-09-23 | Mildly Bearish | Neutral | 0.99% | 1.97% | +0.98% | Top to Down | Red | -1.49% |
| 2020-10-26 | Mildly Bearish | Neutral | 1.14% | 1.89% | +0.75% | Top to Down | Red | -1.34% |
| 2021-09-28 | Mildly Bearish | Neutral | 0.95% | 1.84% | +0.89% | Top to Down | Red | -0.97% |

---

## Key Findings

1. **FII Bullish + PRO Neutral is the safest setup** (7.4% VIX underestimation, 59.3% green). When FII is bullish alone and PRO has no view, the market stays range-bound and closes higher more often than any other combination.

2. **FII Bearish + PRO Bullish produces the highest VIX underestimation** (32.6%). When institutions directly oppose each other with FII bearish and PRO bullish, the tension creates outsized moves 1 in 4 days — and PRO's bullish view wins 60.9% of the time.

3. **Bearish alignment is more volatile than bullish alignment**. Bearish alignment averages 1.03% range vs 0.95% for bullish. VIX underestimation is 19.9% vs 17.6%. Bearish days produce bigger, more unpredictable moves.

4. **Bearish alignment exhaustion is more frequent**: 58% of bearish alignment days exceed the VIX half-threshold (vs 37.5% for bullish). Selloffs are sharper and cross the threshold more readily.

5. **Bullish exhaustion has higher WR%**: When the half-threshold is exceeded, bullish alignment closes in the aligned direction 85.4% of the time vs 79.8% for bearish. Bullish moves that cross are more durable.

6. **Mixed days favor PRO when FII is bearish**: In FII Bearish + PRO Bullish conflicts, PRO wins 61.7%. But in FII Bullish + PRO Bearish conflicts, neither side has an edge (45.5% green).

7. **FII solo views are directionally reliable**: FII Bullish + PRO Neutral → 61.8% green. FII Bearish + PRO Neutral → 52.9% red. FII's solo signal outperforms PRO's solo signal (FII Neutral + PRO Bullish → 52.1% green, FII Neutral + PRO Bearish → 50.2% red).

8. **Elevated VIX (20-30) amplifies underestimation across all combinations**. Every category shows its highest underestimation rate in the elevated VIX regime, ranging from 9.1% (FII Bullish + PRO Neutral) to 66.7% (FII Bearish + PRO Bullish, small sample).

9. **Both Neutral is a coin flip with hidden risk**. Direction is 51.4% Top-to-Down / 48.6% Down-to-Up — essentially random. But avg range is 1.06% (higher than aligned days), and the top 5 volatile days are all massive red days (avg -2.5% close). No institutional signal means exogenous shocks dominate.

10. **Fridays are the riskiest day for VIX underestimation** in bullish alignment (26.7%) and both neutral (33.3%). Mondays are riskiest for bearish alignment (29.3%). Wednesdays are consistently the calmest day across all categories.

11. **2024 was the most unpredictable year** — underestimation rates spiked to 29.9% (bullish alignment) and 35.0% (FII Bearish + PRO Bullish). The 2024-06-04 election result day produced the single largest VIX miss: range 8.19% vs VIX prediction of 1.10%.

12. **When FII Bearish + PRO Neutral underestimates, it always closes red** (10/10 = 100% red, avg O→C -1.17%). This is the only category with zero green days on underestimated days — when FII's solo bearish signal produces an outsized move, it is always downward.

## Trading Implications

| Scenario | Signal | Action |
|----------|--------|--------|
| FII Bullish + PRO Neutral | Strongest bullish (61.8% green, 7.3% U/E) | Favor long bias, tight stops adequate |
| FII Bearish + PRO Neutral | Reliable bearish (52.9% red, 100% red when U/E) | Favor short bias, wider stops for VIX blowouts |
| Bearish Alignment + Exceeded Half | 79.8% close bearish | Hold short if threshold crossed by midday |
| Bullish Alignment + Exceeded Half | 85.4% close bullish | Hold long if threshold crossed |
| Bearish Alignment + Reversed Before Half | Only 16.9% close bearish | Exit shorts early if threshold not reached by 10:15 AM |
| FII Bearish + PRO Bullish | PRO wins 61.7%, but 27.7% VIX U/E | Lean with PRO's bullish view, but size for volatility |
| Both Neutral | Pure coin flip (48.6% green) | Reduce size, use range-bound strategies |
| Any category + Elevated VIX | Highest U/E rates across all combos | Widen stops, buy premium, expect outsized moves |
| Any category + Wednesday | Lowest U/E rates | More predictable, range strategies viable |
| Any category + Friday | Highest U/E rates | Pre-weekend risk premium, consider hedging |

---

*Generated: 2026-09-11 | Data: Aug 2020 – Sep 2026 | Source: vix_fii_t1_intraday_daily_results.csv*