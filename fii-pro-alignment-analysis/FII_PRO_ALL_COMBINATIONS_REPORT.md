# FII-PRO All Combinations: Comprehensive Analysis Report

> **Dataset**: `vix_fii_t1_intraday_daily_results.csv` — 1,485 trading days (Aug 2020 – Sep 2026)
>
> **T-1 data caveat**: FII/PRO views are derived from T+1 settlement data,
> so alignment is known only after the trading day. This analysis identifies
> historical patterns, not real-time predictive signals.
>
> **VIX Accuracy**: "Underestimated" = actual intraday range exceeded VIX prediction by > 0.5%

---

## Master Summary — All 9 Combinations

| Category | Days | % Total | Green% | Red% | VIX U/E% | Avg Range% | Avg O→C% | Avg VIX Pred% | Avg Diff% |
|----------|-----:|--------:|-------:|-----:|---------:|-----------:|---------:|--------------:|----------:|
| **Bullish Alignment** | 328 | 22.1% | 46.3% | 53.7% | 17.7% | 0.96% | -0.080% | 0.79% | +0.17% |
| **Bearish Alignment** | 324 | 21.8% | 46.3% | 53.7% | 21.9% | 1.05% | -0.087% | 0.81% | +0.24% |
| **FII Bullish + PRO Bearish** | 55 | 3.7% | 45.5% | 54.5% | 12.7% | 0.85% | -0.052% | 0.79% | +0.07% |
| **FII Bearish + PRO Bullish** | 47 | 3.2% | 61.7% | 38.3% | 27.7% | 1.07% | +0.157% | 0.76% | +0.31% |
| **Both Neutral** | 179 | 12.1% | 48.6% | 51.4% | 19.0% | 1.06% | -0.041% | 0.91% | +0.15% |
| **FII Neutral + PRO Bullish** | 215 | 14.5% | 52.1% | 47.9% | 16.7% | 1.05% | +0.003% | 0.87% | +0.17% |
| **FII Neutral + PRO Bearish** | 231 | 15.6% | 49.8% | 50.2% | 19.9% | 1.07% | -0.004% | 0.85% | +0.22% |
| **FII Bullish + PRO Neutral** | 55 | 3.7% | 61.8% | 38.2% | 7.3% | 0.88% | +0.080% | 0.86% | +0.02% |
| **FII Bearish + PRO Neutral** | 51 | 3.4% | 47.1% | 52.9% | 17.6% | 1.1% | -0.222% | 0.82% | +0.28% |

### Quick-Read Guide

- **Highest green rate**: FII Bullish + PRO Neutral (61.8%) and FII Bearish + PRO Bullish (61.7%)
- **Highest VIX underestimation**: FII Bearish + PRO Bullish (27.7%) — opposing tension creates outsized moves
- **Lowest VIX underestimation**: FII Bullish + PRO Neutral (7.3%) — calmest, most predictable days
- **Most bearish**: FII Bearish + PRO Neutral (avg O→C -0.222%) — FII bearish conviction with PRO silent
- **Largest sample**: FII Neutral + PRO Bearish (231 days) — most common non-aligned category

---

## Bullish Alignment (328 days, 22.1% of total)

*Both FII and PRO lean bullish (Strong Bullish, Bullish, or Mildly Bullish). The institutional consensus is upward.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 328 |
| Green (close > open) | 152 (46.3%) |
| Red (close < open) | 176 (53.7%) |
| Top to Down | 176 (53.7%) |
| Down to Up | 152 (46.3%) |
| Avg Range% | 0.96% |
| Avg Open→Close% | -0.080% |
| Avg High from Open% | +0.4% |
| Avg Low from Open% | -0.56% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **58** | **17.7%** | 1.8% | +0.98% |
| Overestimated | 270 | 82.3% | — | — |
| Avg VIX Predicted | — | — | 0.79% | +0.17% |
| Range/VIX Ratio | — | — | — | 1.22 |

**When Underestimated (58 days):**
- Green: 27 (46.6%) | Red: 31 (53.4%)
- Top to Down: 31 (53.4%)
- Avg Range: 1.8% | Avg Diff: +0.98% | Avg O→C: -0.176%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Bullish | Strong Bullish | 133 | 15.0% | 40.6% | 0.88% | -0.145% | +0.10% |
| Strong Bullish | Strong Bullish | 70 | 17.1% | 58.6% | 0.99% | -0.018% | +0.24% |
| Mildly Bullish | Strong Bullish | 42 | 21.4% | 33.3% | 1.0% | -0.209% | +0.23% |
| Bullish | Bullish | 29 | 13.8% | 55.2% | 0.94% | +0.120% | +0.11% |
| Mildly Bullish | Bullish | 26 | 30.8% | 38.5% | 1.15% | -0.240% | +0.28% |
| Bullish | Mildly Bullish | 10 | 30.0% | 40.0% | 0.92% | +0.188% | +0.26% |
| Mildly Bullish | Mildly Bullish | 7 | 14.3% | 85.7% | 0.99% | +0.389% | -0.02% |
| Strong Bullish | Mildly Bullish | 6 | 16.7% | 50.0% | 1.41% | +0.018% | +0.26% |
| Strong Bullish | Bullish | 5 | 0.0% | 80.0% | 0.84% | +0.238% | +0.16% |

### VIX Half-Range Exhaustion

| Exhaustion | Days | % | Worked & Remained | WR% | VIX U/E% | Avg Range% | Avg O→C% |
|------------|-----:|--:|------------------:|----:|---------:|-----------:|---------:|
| Exceeded Half | 123 | 37.5% | 105 | **85.4%** | 22.0% | 1.01% | +0.503% |
| Reversed Before Half | 205 | 62.5% | 46 | **22.4%** | 15.1% | 0.93% | -0.429% |

**Close Outcome**: Worked and Remained: 151 (46.0%) | Reversed by Close: 177 (54.0%)

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 198 | 15.7% | 44.9% | 0.8% |
| Normal (15-20) | 87 | 18.4% | 43.7% | 1.07% |
| Elevated (20-30) | 43 | 25.6% | 58.1% | 1.46% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 66 | 19.7% | 47.0% |
| Non-Expiry | 262 | 17.2% | 46.2% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 59 | 16.9% | 42.4% |
| Tuesday | 82 | 13.4% | 41.5% |
| Wednesday | 59 | 11.9% | 52.5% |
| Thursday | 66 | 21.2% | 45.5% |
| Friday | 60 | 26.7% | 53.3% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 9 | 11.1% | 77.8% |
| 2021 | 40 | 20.0% | 55.0% |
| 2022 | 49 | 16.3% | 46.9% |
| 2023 | 78 | 12.8% | 44.9% |
| 2024 | 67 | 29.9% | 43.3% |
| 2025 | 48 | 18.8% | 45.8% |
| 2026 | 37 | 5.4% | 37.8% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2024-06-04 | Strong Bullish | Strong Bullish | 1.1% | 8.19% | +7.09% | Top to Down | Red | -5.10% |
| 2022-02-28 | Strong Bullish | Mildly Bullish | 1.4% | 2.78% | +1.38% | Down to Up | Green | +1.87% |
| 2021-01-29 | Mildly Bullish | Strong Bullish | 1.27% | 2.64% | +1.37% | Top to Down | Red | -2.05% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | 0.9% | 2.52% | +1.62% | Down to Up | Green | +1.38% |
| 2021-03-12 | Mildly Bullish | Bullish | 1.09% | 2.47% | +1.38% | Top to Down | Red | -1.94% |

---

## Bearish Alignment (324 days, 21.8% of total)

*Both FII and PRO lean bearish (Strong Bearish, Bearish, or Mildly Bearish). The institutional consensus is downward.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 324 |
| Green (close > open) | 150 (46.3%) |
| Red (close < open) | 174 (53.7%) |
| Top to Down | 174 (53.7%) |
| Down to Up | 150 (46.3%) |
| Avg Range% | 1.05% |
| Avg Open→Close% | -0.087% |
| Avg High from Open% | +0.44% |
| Avg Low from Open% | -0.61% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **71** | **21.9%** | 1.76% | +0.9% |
| Overestimated | 253 | 78.1% | — | — |
| Avg VIX Predicted | — | — | 0.81% | +0.24% |
| Range/VIX Ratio | — | — | — | 1.31 |

**When Underestimated (71 days):**
- Green: 26 (36.6%) | Red: 45 (63.4%)
- Top to Down: 45 (63.4%)
- Avg Range: 1.76% | Avg Diff: +0.9% | Avg O→C: -0.368%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Bearish | Strong Bearish | 94 | 17.0% | 46.8% | 1.01% | -0.054% | +0.18% |
| Strong Bearish | Strong Bearish | 90 | 24.4% | 42.2% | 1.06% | -0.085% | +0.28% |
| Mildly Bearish | Strong Bearish | 49 | 30.6% | 51.0% | 1.23% | -0.148% | +0.39% |
| Bearish | Bearish | 30 | 23.3% | 43.3% | 1.03% | -0.170% | +0.27% |
| Mildly Bearish | Bearish | 26 | 23.1% | 46.2% | 1.03% | -0.026% | +0.19% |
| Mildly Bearish | Mildly Bearish | 11 | 9.1% | 81.8% | 0.78% | +0.140% | +0.00% |
| Strong Bearish | Bearish | 11 | 9.1% | 36.4% | 1.07% | -0.200% | +0.21% |
| Bearish | Mildly Bearish | 8 | 37.5% | 37.5% | 0.95% | -0.094% | +0.18% |
| Strong Bearish | Mildly Bearish | 5 | 0.0% | 40.0% | 0.83% | -0.190% | +0.08% |

### VIX Half-Range Exhaustion

| Exhaustion | Days | % | Worked & Remained | WR% | VIX U/E% | Avg Range% | Avg O→C% |
|------------|-----:|--:|------------------:|----:|---------:|-----------:|---------:|
| Exceeded Half | 188 | 58.0% | 150 | **79.8%** | 31.9% | 1.18% | -0.417% |
| Reversed Before Half | 136 | 42.0% | 23 | **16.9%** | 8.1% | 0.86% | +0.371% |

**Close Outcome**: Worked and Remained: 173 (53.4%) | Reversed by Close: 151 (46.6%)

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 184 | 19.6% | 39.7% | 0.92% |
| Normal (15-20) | 98 | 23.5% | 55.1% | 1.09% |
| Elevated (20-30) | 42 | 28.6% | 54.8% | 1.53% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 71 | 29.6% | 40.8% |
| Non-Expiry | 253 | 19.8% | 47.8% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 75 | 29.3% | 52.0% |
| Tuesday | 53 | 20.8% | 52.8% |
| Wednesday | 69 | 11.6% | 43.5% |
| Thursday | 62 | 27.4% | 43.5% |
| Friday | 64 | 18.8% | 40.6% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 7 | 28.6% | 100.0% |
| 2021 | 37 | 35.1% | 40.5% |
| 2022 | 57 | 19.3% | 43.9% |
| 2023 | 67 | 11.9% | 37.3% |
| 2024 | 65 | 29.2% | 53.8% |
| 2025 | 50 | 12.0% | 44.0% |
| 2026 | 41 | 29.3% | 51.2% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2024-06-05 | Strong Bearish | Strong Bearish | 1.4% | 3.97% | +2.57% | Down to Up | Green | +2.01% |
| 2026-02-01 | Mildly Bearish | Strong Bearish | 0.71% | 3.43% | +2.72% | Top to Down | Red | -2.23% |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 1.28% | 3.01% | +1.73% | Top to Down | Red | -2.00% |
| 2021-04-05 | Strong Bearish | Bearish | 1.05% | 2.56% | +1.51% | Top to Down | Red | -1.27% |
| 2021-12-20 | Mildly Bearish | Strong Bearish | 0.86% | 2.49% | +1.63% | Top to Down | Red | -1.26% |

---

## FII Bullish + PRO Bearish (55 days, 3.7% of total)

*FII leans bullish while PRO leans bearish. The institutions are in direct conflict.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 55 |
| Green (close > open) | 25 (45.5%) |
| Red (close < open) | 30 (54.5%) |
| Top to Down | 30 (54.5%) |
| Down to Up | 25 (45.5%) |
| Avg Range% | 0.85% |
| Avg Open→Close% | -0.052% |
| Avg High from Open% | +0.39% |
| Avg Low from Open% | -0.46% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **7** | **12.7%** | 1.73% | +0.91% |
| Overestimated | 48 | 87.3% | — | — |
| Avg VIX Predicted | — | — | 0.79% | +0.07% |
| Range/VIX Ratio | — | — | — | 1.09 |

**When Underestimated (7 days):**
- Green: 3 (42.9%) | Red: 4 (57.1%)
- Top to Down: 4 (57.1%)
- Avg Range: 1.73% | Avg Diff: +0.91% | Avg O→C: -0.309%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Bullish | Strong Bearish | 15 | 13.3% | 46.7% | 0.83% | +0.076% | +0.07% |
| Mildly Bullish | Bearish | 9 | 22.2% | 44.4% | 0.88% | -0.209% | +0.13% |
| Mildly Bullish | Strong Bearish | 9 | 11.1% | 44.4% | 0.81% | -0.096% | +0.10% |
| Bullish | Mildly Bearish | 6 | 0.0% | 33.3% | 0.69% | -0.142% | -0.15% |
| Bullish | Bearish | 5 | 0.0% | 40.0% | 0.88% | -0.022% | +0.05% |
| Strong Bullish | Strong Bearish | 5 | 0.0% | 40.0% | 0.76% | -0.034% | -0.04% |
| Mildly Bullish | Mildly Bearish | 3 | 66.7% | 66.7% | 1.63% | -0.057% | +0.57% |
| Strong Bullish | Bearish | 2 | 0.0% | 50.0% | 0.73% | -0.005% | +0.04% |
| Strong Bullish | Mildly Bearish | 1 | 0.0% | 100.0% | 0.45% | +0.060% | -0.35% |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 35 | 11.4% | 40.0% | 0.8% |
| Normal (15-20) | 14 | 14.3% | 57.1% | 0.86% |
| Elevated (20-30) | 6 | 16.7% | 50.0% | 1.1% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 17 | 17.6% | 47.1% |
| Non-Expiry | 38 | 10.5% | 44.7% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 9 | 11.1% | 55.6% |
| Tuesday | 13 | 7.7% | 46.2% |
| Wednesday | 7 | 0.0% | 42.9% |
| Thursday | 10 | 30.0% | 50.0% |
| Friday | 16 | 12.5% | 37.5% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2021 | 3 | 33.3% | 33.3% |
| 2022 | 7 | 0.0% | 57.1% |
| 2023 | 3 | 0.0% | 33.3% |
| 2024 | 29 | 20.7% | 34.5% |
| 2025 | 8 | 0.0% | 87.5% |
| 2026 | 5 | 0.0% | 40.0% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2024-12-05 | Mildly Bullish | Mildly Bearish | 0.76% | 2.29% | +1.53% | Down to Up | Green | +0.66% |
| 2024-11-28 | Mildly Bullish | Bearish | 0.77% | 1.95% | +1.18% | Top to Down | Red | -1.30% |
| 2021-01-22 | Mildly Bullish | Mildly Bearish | 1.13% | 1.79% | +0.66% | Top to Down | Red | -1.49% |
| 2024-02-22 | Bullish | Strong Bearish | 0.83% | 1.71% | +0.88% | Down to Up | Green | +0.61% |
| 2024-11-05 | Bullish | Strong Bearish | 0.87% | 1.62% | +0.75% | Down to Up | Green | +1.18% |

---

## FII Bearish + PRO Bullish (47 days, 3.2% of total)

*FII leans bearish while PRO leans bullish. The institutions oppose each other — historically PRO wins more often.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 47 |
| Green (close > open) | 29 (61.7%) |
| Red (close < open) | 18 (38.3%) |
| Top to Down | 18 (38.3%) |
| Down to Up | 29 (61.7%) |
| Avg Range% | 1.07% |
| Avg Open→Close% | +0.157% |
| Avg High from Open% | +0.56% |
| Avg Low from Open% | -0.51% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **13** | **27.7%** | 1.83% | +0.98% |
| Overestimated | 34 | 72.3% | — | — |
| Avg VIX Predicted | — | — | 0.76% | +0.31% |
| Range/VIX Ratio | — | — | — | 1.37 |

**When Underestimated (13 days):**
- Green: 6 (46.2%) | Red: 7 (53.8%)
- Top to Down: 7 (53.8%)
- Avg Range: 1.83% | Avg Diff: +0.98% | Avg O→C: 0.186%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Bearish | Strong Bullish | 11 | 9.1% | 63.6% | 0.78% | +0.134% | +0.07% |
| Mildly Bearish | Strong Bullish | 11 | 36.4% | 63.6% | 1.31% | +0.144% | +0.49% |
| Mildly Bearish | Bullish | 7 | 42.9% | 42.9% | 0.92% | -0.194% | +0.17% |
| Bearish | Bullish | 6 | 33.3% | 83.3% | 1.23% | +0.243% | +0.48% |
| Strong Bearish | Strong Bullish | 4 | 25.0% | 25.0% | 0.92% | -0.155% | +0.19% |
| Bearish | Mildly Bullish | 3 | 0.0% | 33.3% | 0.76% | +0.093% | +0.08% |
| Mildly Bearish | Mildly Bullish | 3 | 33.3% | 100.0% | 1.36% | +1.000% | +0.59% |
| Strong Bearish | Bullish | 2 | 50.0% | 100.0% | 1.74% | +0.775% | +0.76% |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 27 | 14.8% | 59.3% | 0.86% |
| Normal (15-20) | 17 | 41.2% | 58.8% | 1.25% |
| Elevated (20-30) | 3 | 66.7% | 100.0% | 1.97% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 9 | 22.2% | 44.4% |
| Non-Expiry | 38 | 28.9% | 65.8% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 7 | 28.6% | 85.7% |
| Tuesday | 2 | 50.0% | 50.0% |
| Wednesday | 9 | 33.3% | 55.6% |
| Thursday | 15 | 13.3% | 40.0% |
| Friday | 14 | 35.7% | 78.6% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2021 | 2 | 50.0% | 50.0% |
| 2022 | 3 | 0.0% | 100.0% |
| 2023 | 10 | 20.0% | 80.0% |
| 2024 | 20 | 35.0% | 50.0% |
| 2025 | 3 | 33.3% | 100.0% |
| 2026 | 9 | 22.2% | 44.4% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2024-11-22 | Mildly Bearish | Strong Bullish | 0.84% | 2.55% | +1.71% | Down to Up | Green | +1.97% |
| 2024-12-13 | Bearish | Bullish | 0.69% | 2.5% | +1.81% | Down to Up | Green | +1.15% |
| 2026-03-16 | Strong Bearish | Bullish | 1.19% | 2.37% | +1.18% | Down to Up | Green | +1.04% |
| 2025-05-12 | Mildly Bearish | Mildly Bullish | 1.13% | 2.32% | +1.19% | Down to Up | Green | +2.05% |
| 2024-12-20 | Mildly Bearish | Strong Bullish | 0.76% | 2.21% | +1.45% | Top to Down | Red | -1.37% |

---

## Both Neutral (179 days, 12.1% of total)

*Neither FII nor PRO has a directional view. No institutional signal — a coin flip.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 179 |
| Green (close > open) | 87 (48.6%) |
| Red (close < open) | 92 (51.4%) |
| Top to Down | 92 (51.4%) |
| Down to Up | 87 (48.6%) |
| Avg Range% | 1.06% |
| Avg Open→Close% | -0.041% |
| Avg High from Open% | +0.46% |
| Avg Low from Open% | -0.6% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **34** | **19.0%** | 1.85% | +0.91% |
| Overestimated | 145 | 81.0% | — | — |
| Avg VIX Predicted | — | — | 0.91% | +0.15% |
| Range/VIX Ratio | — | — | — | 1.18 |

**When Underestimated (34 days):**
- Green: 14 (41.2%) | Red: 20 (58.8%)
- Top to Down: 20 (58.8%)
- Avg Range: 1.85% | Avg Diff: +0.91% | Avg O→C: -0.432%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Neutral | Neutral | 179 | 19.0% | 48.6% | 1.06% | -0.041% | +0.15% |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 64 | 18.8% | 51.6% | 0.84% |
| Normal (15-20) | 54 | 14.8% | 42.6% | 1.05% |
| Elevated (20-30) | 61 | 23.0% | 50.8% | 1.3% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 35 | 17.1% | 37.1% |
| Non-Expiry | 144 | 19.4% | 51.4% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 39 | 25.6% | 56.4% |
| Tuesday | 37 | 13.5% | 51.4% |
| Wednesday | 39 | 12.8% | 53.8% |
| Thursday | 38 | 15.8% | 36.8% |
| Friday | 24 | 33.3% | 45.8% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 47 | 14.9% | 36.2% |
| 2021 | 42 | 26.2% | 57.1% |
| 2022 | 27 | 14.8% | 44.4% |
| 2023 | 5 | 0.0% | 60.0% |
| 2024 | 10 | 30.0% | 80.0% |
| 2025 | 33 | 12.1% | 48.5% |
| 2026 | 15 | 33.3% | 46.7% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2022-01-24 | Neutral | Neutral | 0.99% | 3.41% | +2.42% | Top to Down | Red | -2.63% |
| 2020-10-15 | Neutral | Neutral | 1.06% | 3.0% | +1.94% | Top to Down | Red | -2.92% |
| 2020-09-21 | Neutral | Neutral | 1.05% | 2.74% | +1.69% | Top to Down | Red | -2.45% |
| 2021-04-12 | Neutral | Neutral | 1.04% | 2.7% | +1.66% | Top to Down | Red | -2.01% |
| 2020-08-14 | Neutral | Neutral | 1.08% | 2.24% | +1.16% | Top to Down | Red | -1.50% |

---

## FII Neutral + PRO Bullish (215 days, 14.5% of total)

*FII has no view while PRO leans bullish. Only PRO provides a directional signal.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 215 |
| Green (close > open) | 112 (52.1%) |
| Red (close < open) | 103 (47.9%) |
| Top to Down | 103 (47.9%) |
| Down to Up | 112 (52.1%) |
| Avg Range% | 1.05% |
| Avg Open→Close% | +0.003% |
| Avg High from Open% | +0.48% |
| Avg Low from Open% | -0.57% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **36** | **16.7%** | 2.02% | +1.0% |
| Overestimated | 179 | 83.3% | — | — |
| Avg VIX Predicted | — | — | 0.87% | +0.17% |
| Range/VIX Ratio | — | — | — | 1.18 |

**When Underestimated (36 days):**
- Green: 16 (44.4%) | Red: 20 (55.6%)
- Top to Down: 20 (55.6%)
- Avg Range: 2.02% | Avg Diff: +1.0% | Avg O→C: -0.146%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Neutral | Strong Bullish | 87 | 10.3% | 51.7% | 0.94% | +0.014% | +0.12% |
| Neutral | Bullish | 85 | 17.6% | 51.8% | 1.03% | +0.035% | +0.16% |
| Neutral | Mildly Bullish | 43 | 27.9% | 53.5% | 1.29% | -0.081% | +0.31% |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 90 | 6.7% | 52.2% | 0.71% |
| Normal (15-20) | 67 | 19.4% | 46.3% | 1.1% |
| Elevated (20-30) | 57 | 29.8% | 57.9% | 1.5% |
| High (>30) | 1 | 0.0% | 100.0% | 1.57% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 45 | 17.8% | 48.9% |
| Non-Expiry | 170 | 16.5% | 52.9% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 38 | 18.4% | 65.8% |
| Tuesday | 40 | 17.5% | 45.0% |
| Wednesday | 48 | 16.7% | 45.8% |
| Thursday | 44 | 13.6% | 54.5% |
| Friday | 44 | 18.2% | 52.3% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 18 | 22.2% | 61.1% |
| 2021 | 44 | 22.7% | 47.7% |
| 2022 | 36 | 22.2% | 63.9% |
| 2023 | 35 | 8.6% | 54.3% |
| 2024 | 21 | 9.5% | 47.6% |
| 2025 | 38 | 5.3% | 39.5% |
| 2026 | 23 | 30.4% | 56.5% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2020-08-31 | Neutral | Mildly Bullish | 0.96% | 3.97% | +3.01% | Top to Down | Red | -3.71% |
| 2023-02-01 | Neutral | Bullish | 0.88% | 3.47% | +2.59% | Top to Down | Red | -1.16% |
| 2022-06-16 | Neutral | Mildly Bullish | 1.16% | 3.33% | +2.17% | Top to Down | Red | -3.06% |
| 2021-03-19 | Neutral | Strong Bullish | 1.05% | 3.02% | +1.97% | Down to Up | Green | +1.81% |
| 2026-04-02 | Neutral | Mildly Bullish | 1.31% | 2.68% | +1.37% | Down to Up | Green | +1.42% |

---

## FII Neutral + PRO Bearish (231 days, 15.6% of total)

*FII has no view while PRO leans bearish. Only PRO provides a directional signal.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 231 |
| Green (close > open) | 115 (49.8%) |
| Red (close < open) | 116 (50.2%) |
| Top to Down | 116 (50.2%) |
| Down to Up | 115 (49.8%) |
| Avg Range% | 1.07% |
| Avg Open→Close% | -0.004% |
| Avg High from Open% | +0.49% |
| Avg Low from Open% | -0.58% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **46** | **19.9%** | 1.88% | +0.98% |
| Overestimated | 185 | 80.1% | — | — |
| Avg VIX Predicted | — | — | 0.85% | +0.22% |
| Range/VIX Ratio | — | — | — | 1.27 |

**When Underestimated (46 days):**
- Green: 21 (45.7%) | Red: 25 (54.3%)
- Top to Down: 25 (54.3%)
- Avg Range: 1.88% | Avg Diff: +0.98% | Avg O→C: -0.299%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Neutral | Bearish | 88 | 20.5% | 59.1% | 1.08% | +0.045% | +0.21% |
| Neutral | Strong Bearish | 83 | 19.3% | 45.8% | 0.99% | +0.030% | +0.20% |
| Neutral | Mildly Bearish | 60 | 20.0% | 41.7% | 1.18% | -0.125% | +0.28% |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 114 | 16.7% | 44.7% | 0.87% |
| Normal (15-20) | 63 | 20.6% | 58.7% | 1.16% |
| Elevated (20-30) | 54 | 25.9% | 50.0% | 1.4% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 49 | 18.4% | 51.0% |
| Non-Expiry | 182 | 20.3% | 49.5% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 49 | 16.3% | 49.0% |
| Tuesday | 49 | 24.5% | 49.0% |
| Wednesday | 42 | 19.0% | 61.9% |
| Thursday | 47 | 19.1% | 51.1% |
| Friday | 43 | 20.9% | 39.5% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 12 | 16.7% | 58.3% |
| 2021 | 60 | 23.3% | 43.3% |
| 2022 | 39 | 30.8% | 61.5% |
| 2023 | 33 | 15.2% | 45.5% |
| 2024 | 23 | 13.0% | 34.8% |
| 2025 | 49 | 10.2% | 51.0% |
| 2026 | 15 | 33.3% | 66.7% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2020-12-21 | Neutral | Mildly Bearish | 0.97% | 4.67% | +3.70% | Top to Down | Red | -3.34% |
| 2022-02-15 | Neutral | Strong Bearish | 1.2% | 3.15% | +1.95% | Down to Up | Green | +2.47% |
| 2021-02-26 | Neutral | Bearish | 1.2% | 3.03% | +1.83% | Top to Down | Red | -2.45% |
| 2022-05-04 | Neutral | Strong Bearish | 1.06% | 2.95% | +1.89% | Top to Down | Red | -2.35% |
| 2022-03-07 | Neutral | Bearish | 1.46% | 2.9% | +1.44% | Down to Up | Green | +0.08% |

---

## FII Bullish + PRO Neutral (55 days, 3.7% of total)

*FII leans bullish while PRO has no view. FII's solo signal — historically the most reliable bullish setup.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 55 |
| Green (close > open) | 34 (61.8%) |
| Red (close < open) | 21 (38.2%) |
| Top to Down | 21 (38.2%) |
| Down to Up | 34 (61.8%) |
| Avg Range% | 0.88% |
| Avg Open→Close% | +0.080% |
| Avg High from Open% | +0.46% |
| Avg Low from Open% | -0.42% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **4** | **7.3%** | 1.81% | +0.94% |
| Overestimated | 51 | 92.7% | — | — |
| Avg VIX Predicted | — | — | 0.86% | +0.02% |
| Range/VIX Ratio | — | — | — | 1.04 |

**When Underestimated (4 days):**
- Green: 1 (25.0%) | Red: 3 (75.0%)
- Top to Down: 3 (75.0%)
- Avg Range: 1.81% | Avg Diff: +0.94% | Avg O→C: -0.638%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Mildly Bullish | Neutral | 29 | 13.8% | 62.1% | 0.98% | +0.004% | +0.08% |
| Bullish | Neutral | 21 | 0.0% | 71.4% | 0.82% | +0.217% | -0.04% |
| Strong Bullish | Neutral | 5 | 0.0% | 20.0% | 0.57% | -0.054% | -0.11% |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 22 | 9.1% | 54.5% | 0.76% |
| Normal (15-20) | 22 | 4.5% | 59.1% | 0.88% |
| Elevated (20-30) | 11 | 9.1% | 81.8% | 1.14% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 10 | 0.0% | 40.0% |
| Non-Expiry | 45 | 8.9% | 66.7% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 8 | 0.0% | 87.5% |
| Tuesday | 16 | 18.8% | 50.0% |
| Wednesday | 11 | 0.0% | 72.7% |
| Thursday | 5 | 0.0% | 40.0% |
| Friday | 15 | 6.7% | 60.0% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 7 | 0.0% | 100.0% |
| 2021 | 6 | 0.0% | 66.7% |
| 2022 | 16 | 6.2% | 68.8% |
| 2023 | 5 | 0.0% | 60.0% |
| 2024 | 4 | 0.0% | 25.0% |
| 2025 | 10 | 30.0% | 50.0% |
| 2026 | 7 | 0.0% | 42.9% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2022-02-01 | Mildly Bullish | Neutral | 1.15% | 2.15% | +1.00% | Down to Up | Green | +0.43% |
| 2025-04-01 | Mildly Bullish | Neutral | 0.67% | 1.84% | +1.17% | Top to Down | Red | -0.69% |
| 2025-05-13 | Mildly Bullish | Neutral | 0.96% | 1.71% | +0.75% | Top to Down | Red | -1.09% |
| 2022-02-21 | Mildly Bullish | Neutral | 1.16% | 1.63% | +0.47% | Down to Up | Green | +0.08% |
| 2025-04-04 | Mildly Bullish | Neutral | 0.71% | 1.54% | +0.83% | Top to Down | Red | -1.20% |

---

## FII Bearish + PRO Neutral (51 days, 3.4% of total)

*FII leans bearish while PRO has no view. FII's solo bearish signal — historically directionally reliable.*

### Core Statistics

| Metric | Value |
|--------|------:|
| Trading Days | 51 |
| Green (close > open) | 24 (47.1%) |
| Red (close < open) | 27 (52.9%) |
| Top to Down | 27 (52.9%) |
| Down to Up | 24 (47.1%) |
| Avg Range% | 1.1% |
| Avg Open→Close% | -0.222% |
| Avg High from Open% | +0.38% |
| Avg Low from Open% | -0.72% |

### VIX Accuracy

| VIX Accuracy | Days | % | Avg Range% | Avg Diff% |
|-------------|-----:|--:|-----------:|----------:|
| **Underestimated** | **9** | **17.6%** | 1.99% | +1.09% |
| Overestimated | 42 | 82.4% | — | — |
| Avg VIX Predicted | — | — | 0.82% | +0.28% |
| Range/VIX Ratio | — | — | — | 1.35 |

**When Underestimated (9 days):**
- Green: 0 (0.0%) | Red: 9 (100.0%)
- Top to Down: 9 (100.0%)
- Avg Range: 1.99% | Avg Diff: +1.09% | Avg O→C: -1.35%

### Sub-Combinations (FII View × PRO View)

| FII View | PRO View | Days | VIX U/E% | Green% | Avg Range% | Avg O→C% | Avg Diff% |
|----------|----------|-----:|---------:|-------:|-----------:|---------:|----------:|
| Bearish | Neutral | 24 | 12.5% | 45.8% | 1.14% | -0.236% | +0.32% |
| Mildly Bearish | Neutral | 19 | 21.1% | 52.6% | 1.09% | -0.178% | +0.25% |
| Strong Bearish | Neutral | 8 | 25.0% | 37.5% | 1.0% | -0.286% | +0.23% |

### VIX Regime Breakdown

| VIX Regime | Days | VIX U/E% | Green% | Avg Range% |
|------------|-----:|---------:|-------:|-----------:|
| Low (<15) | 29 | 13.8% | 58.6% | 0.93% |
| Normal (15-20) | 13 | 23.1% | 38.5% | 1.32% |
| Elevated (20-30) | 9 | 22.2% | 22.2% | 1.34% |

### Expiry vs Non-Expiry

| Context | Days | VIX U/E% | Green% |
|---------|-----:|---------:|-------:|
| Expiry | 10 | 20.0% | 30.0% |
| Non-Expiry | 41 | 17.1% | 51.2% |

### Day of Week

| Day | Days | VIX U/E% | Green% |
|-----|-----:|---------:|-------:|
| Monday | 13 | 15.4% | 53.8% |
| Tuesday | 7 | 42.9% | 57.1% |
| Wednesday | 11 | 9.1% | 45.5% |
| Thursday | 9 | 11.1% | 44.4% |
| Friday | 11 | 18.2% | 36.4% |

### Year-over-Year

| Year | Days | VIX U/E% | Green% |
|------|-----:|---------:|-------:|
| 2020 | 2 | 50.0% | 0.0% |
| 2021 | 11 | 9.1% | 45.5% |
| 2022 | 9 | 44.4% | 33.3% |
| 2023 | 7 | 0.0% | 85.7% |
| 2024 | 5 | 40.0% | 20.0% |
| 2025 | 6 | 0.0% | 66.7% |
| 2026 | 11 | 9.1% | 45.5% |

### Top 5 Most Volatile Days

| Date | FII View | PRO View | VIX Pred% | Range% | Diff% | Direction | Day | O→C% |
|------|----------|----------|----------:|-------:|------:|-----------|-----|-----:|
| 2026-02-03 | Bearish | Neutral | 0.73% | 2.66% | +1.93% | Top to Down | Red | -2.26% |
| 2022-04-19 | Bearish | Neutral | 1.01% | 2.59% | +1.58% | Top to Down | Red | -2.26% |
| 2022-05-13 | Bearish | Neutral | 1.27% | 2.14% | +0.87% | Top to Down | Red | -1.31% |
| 2022-09-23 | Mildly Bearish | Neutral | 0.99% | 1.97% | +0.98% | Top to Down | Red | -1.49% |
| 2020-10-26 | Mildly Bearish | Neutral | 1.14% | 1.89% | +0.75% | Top to Down | Red | -1.34% |

---

## Key Findings

1. **FII Bullish + PRO Neutral is the safest setup** (7.3% VIX underestimation, 61.8% green). When FII is bullish alone and PRO has no view, the market stays range-bound and closes higher more often than any other combination.

2. **FII Bearish + PRO Bullish produces the highest VIX underestimation** (27.7%). When institutions directly oppose each other with FII bearish and PRO bullish, the tension creates outsized moves 1 in 4 days — and PRO's bullish view wins 61.7% of the time.

3. **Bearish alignment is more volatile than bullish alignment**. Bearish alignment averages 1.05% range vs 0.96% for bullish. VIX underestimation is 21.9% vs 17.7%. Bearish days produce bigger, more unpredictable moves.

4. **Bearish alignment exhaustion is more frequent**: 58% of bearish alignment days exceed the VIX half-threshold (vs 37.5% for bullish). Selloffs are sharper and cross the threshold more readily.

5. **Bullish exhaustion has higher WR%**: When the half-threshold is exceeded, bullish alignment closes in the aligned direction 85.4% of the time vs 79.8% for bearish. Bullish moves that cross are more durable.

6. **Mixed days favor PRO when FII is bearish**: In FII Bearish + PRO Bullish conflicts, PRO wins 61.7%. But in FII Bullish + PRO Bearish conflicts, neither side has an edge (45.5% green).

7. **FII solo views are directionally reliable**: FII Bullish + PRO Neutral → 61.8% green. FII Bearish + PRO Neutral → 52.9% red. FII's solo signal outperforms PRO's solo signal (FII Neutral + PRO Bullish → 52.1% green, FII Neutral + PRO Bearish → 50.2% red).

8. **Elevated VIX (20-30) amplifies underestimation across all combinations**. Every category shows its highest underestimation rate in the elevated VIX regime, ranging from 9.1% (FII Bullish + PRO Neutral) to 66.7% (FII Bearish + PRO Bullish, small sample).

9. **Both Neutral is a coin flip with hidden risk**. Direction is 51.4% Top-to-Down / 48.6% Down-to-Up — essentially random. But avg range is 1.06% (higher than aligned days), and the top 5 volatile days are all massive red days (avg -2.5% close). No institutional signal means exogenous shocks dominate.

10. **Fridays are the riskiest day for VIX underestimation** in bullish alignment (26.7%) and both neutral (33.3%). Mondays are riskiest for bearish alignment (29.3%). Wednesdays are consistently the calmest day across all categories.

11. **2024 was the most unpredictable year** — underestimation rates spiked to 29.9% (bullish alignment) and 35.0% (FII Bearish + PRO Bullish). The 2024-06-04 election result day produced the single largest VIX miss: range 8.19% vs VIX prediction of 1.10%.

12. **When FII Bearish + PRO Neutral underestimates, it always closes red** (9/9 = 100% red, avg O→C -1.35%). This is the only category with zero green days on underestimated days — when FII's solo bearish signal produces an outsized move, it is always downward.

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

*Generated: 2026-09-05 | Data: Aug 2020 – Sep 2026 | Source: vix_fii_t1_intraday_daily_results.csv*