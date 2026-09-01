# FII-PRO Alignment Reversal Analysis — Expiry Days Only

> **Retrospective study**: FII/PRO views are derived from T+1 settlement data,
> so alignment is known only after the trading day. This analysis identifies
> historical patterns, not real-time predictive signals.
>
> **Intraday direction proxy**: `move_direction` captures the dominant intraday
> pattern (open→high→low→close sequence) but does not precisely split the session
> at a fixed time boundary.

## Overall Summary

| Metric | Count | % of Total |
|--------|------:|----------:|
| Total Trading Days | 312 | 100.0% |
| **Aligned Days (Bullish + Bearish)** | **120** | **38.5%** |
| Bullish Alignment | 56 | 17.9% |
| Bearish Alignment | 64 | 20.5% |
| Mixed (opposing views) | 25 | 8.0% |
| Neutral/Unclear | 167 | 53.5% |

## Alignment Outcome Breakdown

When FII and PRO align, does the first half move in their direction and then reverse?

### All Aligned Days (120 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 55 | 45.8% | 0.43% | -0.56% | -0.01% |
| Against then Recovered | 65 | 54.2% | 0.43% | -0.68% | -0.12% |

### Bullish Alignment (56 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 28 | 50.0% | 0.15% | -0.75% | -0.51% |
| Against then Recovered | 28 | 50.0% | 0.78% | -0.29% | 0.57% |

### Bearish Alignment (64 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 27 | 42.2% | 0.72% | -0.36% | 0.51% |
| Against then Recovered | 37 | 57.8% | 0.17% | -0.97% | -0.64% |

## Worked and Remained: Did the Aligned View Win by Close?

A different lens: regardless of intraday path, did the market **close** in the aligned direction?

- **Worked and Remained**: Close was in the aligned direction (bullish alignment + close > open, or bearish alignment + close < open)
- **Reversed by Close**: Close was against the aligned direction

### Overall (120 aligned days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg Range% |
|---------------|------:|--:|----------------:|----------:|---------:|-----------:|
| Worked and Remained | 65 | 54.2% | -0.12% | 0.43% | -0.68% | 1.11% |
| Reversed by Close | 55 | 45.8% | -0.01% | 0.43% | -0.56% | 0.99% |

### Bullish Alignment (56 days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |
|---------------|------:|--:|----------------:|----------:|---------:|
| Worked and Remained | 28 | 50.0% | 0.57% | 0.78% | -0.29% |
| Reversed by Close | 28 | 50.0% | -0.51% | 0.15% | -0.75% |

### Bearish Alignment (64 days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |
|---------------|------:|--:|----------------:|----------:|---------:|
| Worked and Remained | 37 | 57.8% | -0.64% | 0.17% | -0.97% |
| Reversed by Close | 27 | 42.2% | 0.51% | 0.72% | -0.36% |

### Worked and Remained: Expiry vs Non-Expiry

| Context | Aligned | Worked and Remained | % | Reversed by Close | % |
|---------|--------:|--------------------:|--:|------------------:|--:|
| Expiry Days | 120 | 65 | 54.2% | 55 | 45.8% |
| Non-Expiry Days | 0 | 0 | - | 0 | - |

### Worked and Remained: VIX Regime

| VIX Regime | Aligned | Worked and Remained | % | Reversed by Close | % |
|------------|--------:|--------------------:|--:|------------------:|--:|
| Low (<15) | 64 | 32 | 50.0% | 32 | 50.0% |
| Normal (15-20) | 38 | 24 | 63.2% | 14 | 36.8% |
| Elevated (20-30) | 18 | 9 | 50.0% | 9 | 50.0% |
| High (>30) | 0 | 0 | - | 0 | - |

### Worked and Remained: Year-over-Year

| Year | Aligned | Worked and Remained | % | Reversed by Close | % |
|------|--------:|--------------------:|--:|------------------:|--:|
| 2020 | 3 | 0 | 0.0% | 3 | 100.0% |
| 2021 | 13 | 8 | 61.5% | 5 | 38.5% |
| 2022 | 21 | 11 | 52.4% | 10 | 47.6% |
| 2023 | 23 | 12 | 52.2% | 11 | 47.8% |
| 2024 | 22 | 11 | 50.0% | 11 | 50.0% |
| 2025 | 22 | 16 | 72.7% | 6 | 27.3% |
| 2026 | 16 | 7 | 43.8% | 9 | 56.2% |

## VIX Half-Range Exhaustion: Did the Move Exhaust Before Reversing?

Compares the first-half move in the aligned direction against **half of the VIX-predicted range**.
If the move exceeded half the predicted range, it suggests momentum exhaustion before reversal.
If it reversed before reaching half, the reversal happened without significant momentum.

- **Exceeded Half then Reversed**: Aligned-direction move > ½ × VIX predicted range
- **Reversed Before Half**: Aligned-direction move ≤ ½ × VIX predicted range

### Overall (120 aligned days with VIX data)

| VIX Exhaustion | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg VIX Predicted% |
|----------------|------:|--:|----------------:|----------:|---------:|-------------------:|
| Exceeded Half then Reversed | 61 | 50.8% | -0.08% | 0.49% | -0.73% | 1.0% |
| Reversed Before Half | 59 | 49.2% | -0.06% | 0.36% | -0.52% | 0.97% |

### Cross-Tab: VIX Exhaustion × Close Outcome

Does exceeding half the VIX range predict whether the aligned view wins by close?

| VIX Exhaustion | Worked and Remained | % | Reversed by Close | % | Total |
|----------------|--------------------:|--:|------------------:|--:|------:|
| Exceeded Half then Reversed | 52 | 85.2% | 9 | 14.8% | 61 |
| Reversed Before Half | 13 | 22.0% | 46 | 78.0% | 59 |

### Bullish Alignment (56 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 19 | 33.9% | 18 | 94.7% | 0.74% |
| Reversed Before Half | 37 | 66.1% | 10 | 27.0% | -0.34% |

### Bearish Alignment (64 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 42 | 65.6% | 34 | 81.0% | -0.46% |
| Reversed Before Half | 22 | 34.4% | 3 | 13.6% | 0.42% |

### VIX Exhaustion by VIX Regime

| VIX Regime | Total | Exceeded Half | % | Reversed Before Half | % |
|------------|------:|--------------:|--:|---------------------:|--:|
| Low (<15) | 64 | 29 | 45.3% | 35 | 54.7% |
| Normal (15-20) | 38 | 22 | 57.9% | 16 | 42.1% |
| Elevated (20-30) | 18 | 10 | 55.6% | 8 | 44.4% |
| High (>30) | 0 | 0 | - | 0 | - |

## Strong Alignment Analysis

Strong alignment = both FII and PRO have Bullish/Strong Bullish or Bearish/Strong Bearish
(excluding Mildly variants).

| Category | Total | Worked then Reversed | % | Against then Recovered | % |
|----------|------:|---------------------:|--:|-----------------------:|--:|
| Strong Bullish | 37 | 18 | 48.6% | 19 | 51.4% |
| Strong Bearish | 34 | 11 | 32.4% | 23 | 67.6% |
| All Strong Aligned | 71 | 29 | 40.8% | 42 | 59.2% |

## Mixed Days: When FII and PRO Oppose Each Other

When FII and PRO have opposing directional views (one bullish, one bearish),
whose view wins by close?

### Overview (25 mixed days)

| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |
|----------|-----:|----------:|----------:|----------------:|-----------:|
| FII Bullish + PRO Bearish | 17 | 9 (52.9%) | 8 (47.1%) | 0.049% | 0.878% |
| FII Bearish + PRO Bullish | 8 | 4 (50.0%) | 4 (50.0%) | -0.005% | 0.951% |
| All Mixed | 25 | 13 (52.0%) | 12 (48.0%) | 0.032% | 0.902% |

### Who Won by Close?

| Sub-Type | Days | FII Correct | FII% | PRO Correct | PRO% |
|----------|-----:|------------:|-----:|------------:|-----:|
| FII Bullish + PRO Bearish | 17 | 8 | 47.1% | 9 | 52.9% |
| FII Bearish + PRO Bullish | 8 | 4 | 50.0% | 4 | 50.0% |

### Mixed Days: Expiry vs Non-Expiry

| Context | Days | Avg Open→Close% | Avg Range% |
|---------|-----:|----------------:|-----------:|
| Expiry | 25 | 0.032% | 0.902% |
| Non-Expiry | 0 | - | - |

## Neutral Days: When One or Both Sides Have No View

When one or both participants are Neutral, there is no directional consensus.
Does a solo directional view from one side carry any weight?

### Overview (167 neutral days)

| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |
|----------|-----:|----------:|----------:|----------------:|-----------:|
| Both Neutral | 62 | 39 (62.9%) | 23 (37.1%) | -0.194% | 1.054% |
| FII Neutral + PRO Bullish | 41 | 21 (51.2%) | 20 (48.8%) | -0.091% | 0.99% |
| FII Neutral + PRO Bearish | 44 | 22 (50.0%) | 22 (50.0%) | 0.052% | 0.974% |
| FII Bullish + PRO Neutral | 10 | 6 (60.0%) | 4 (40.0%) | -0.004% | 0.697% |
| FII Bearish + PRO Neutral | 10 | 7 (70.0%) | 3 (30.0%) | -0.323% | 1.24% |
| All Neutral/Unclear | 167 | 95 (56.9%) | 72 (43.1%) | -0.1% | 1.007% |

### Solo View Accuracy: Did the One Directional Side Win?

| Sub-Type | Days | View Correct | % | Avg Open→Close% |
|----------|-----:|-------------:|--:|----------------:|
| FII Neutral + PRO Bullish | 41 | 20 | 48.8% | -0.091% |
| FII Neutral + PRO Bearish | 44 | 22 | 50.0% | 0.052% |
| FII Bullish + PRO Neutral | 10 | 4 | 40.0% | -0.004% |
| FII Bearish + PRO Neutral | 10 | 7 | 70.0% | -0.323% |

### Range Comparison: Aligned vs Mixed vs Neutral

| Category | Days | Avg Range% | Avg High% | Avg Low% |
|----------|-----:|-----------:|----------:|---------:|
| Aligned | 120 | 1.057% | 0.429% | -0.627% |
| Mixed | 25 | 0.902% | 0.457% | -0.444% |
| Neutral/Unclear | 167 | 1.007% | 0.418% | -0.589% |

## Expiry vs Non-Expiry

| Context | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg High% | Avg Low% |
|---------|-------------:|---------------------:|--:|-----------------------:|--:|----------:|---------:|
| Expiry Days | 120 | 55 | 45.8% | 65 | 54.2% | 0.43% | -0.63% |
| Non-Expiry Days | 0 | 0 | - | 0 | - | - | - |

## VIX Regime Analysis

| VIX Regime | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg Range% |
|------------|-------------:|---------------------:|--:|-----------------------:|--:|-----------:|
| Low (<15) | 64 | 32 | 50.0% | 32 | 50.0% | 0.91% |
| Normal (15-20) | 38 | 14 | 36.8% | 24 | 63.2% | 1.15% |
| Elevated (20-30) | 18 | 9 | 50.0% | 9 | 50.0% | 1.39% |
| High (>30) | 0 | 0 | - | 0 | - | - |

## Year-over-Year Trends

| Year | Trading Days | Aligned Days | Alignment% | Bullish Aligned | Bearish Aligned | Worked then Reversed | Reversal% |
|------|------------:|-------------:|-----------:|----------------:|----------------:|---------------------:|----------:|
| 2020 | 21 | 3 | 14.3% | 0 | 3 | 3 | 100.0% |
| 2021 | 52 | 13 | 25.0% | 4 | 9 | 5 | 38.5% |
| 2022 | 51 | 21 | 41.2% | 8 | 13 | 10 | 47.6% |
| 2023 | 51 | 23 | 45.1% | 13 | 10 | 11 | 47.8% |
| 2024 | 51 | 22 | 43.1% | 10 | 12 | 11 | 50.0% |
| 2025 | 52 | 22 | 42.3% | 13 | 9 | 6 | 27.3% |
| 2026 | 34 | 16 | 47.1% | 8 | 8 | 9 | 56.2% |

## Detailed: Bullish Alignment Days

When FII+PRO both lean bullish:

- **Top to Down** (Worked then Reversed): Market rose in first half (aligned), then sold off
- **Down to Up** (Against then Recovered): Market fell in first half (against view), then recovered

| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |
|---------|------:|--:|-------------------:|-------------------:|-----------------:|
| Worked then Reversed (Top→Down) | 28 | 50.0% | 0.15% | -0.75% | -0.51% |
| Against then Recovered (Down→Up) | 28 | 50.0% | 0.78% | -0.29% | 0.57% |

## Detailed: Bearish Alignment Days

When FII+PRO both lean bearish:

- **Down to Up** (Worked then Reversed): Market fell in first half (aligned), then recovered
- **Top to Down** (Against then Recovered): Market rose in first half (against view), then sold off

| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |
|---------|------:|--:|-------------------:|-------------------:|-----------------:|
| Worked then Reversed (Down→Up) | 27 | 42.2% | 0.72% | -0.36% | 0.51% |
| Against then Recovered (Top→Down) | 37 | 57.8% | 0.17% | -0.97% | -0.64% |

## Key Findings

1. **Alignment frequency**: FII and PRO aligned on 120 of 312 days (38.5%). Bullish alignment (56) vs Bearish alignment (64).

2. **Reversal is the dominant pattern**: On alignment days, "Worked then Reversed" occurred 45.8% of the time (55/120 days). This means when institutions agree, the first half tends to move in their direction but the second half reverses.

3. **Worked and Remained (close validated view)**: On 54.2% of alignment days (65/120), the market closed in the aligned direction — meaning the institutional consensus was ultimately correct by end of day. The remaining 45.8% closed against the aligned view.

4. **VIX half-range exhaustion**: 50.8% of alignment days exceeded half the VIX-predicted range in the aligned direction (61/120). Among those, 85.2% closed in the aligned direction (Worked and Remained) vs 22.0% for days that reversed before reaching half range. Exceeding half range predicts a better close outcome.

5. **Bullish vs Bearish reversal**: Bullish alignment reversal rate = 50.0%, Bearish alignment reversal rate = 42.2%. Bullish alignment shows a higher tendency to reverse in the second half.

6. **Expiry effect**: Reversal rate on expiry days = 45.8% vs non-expiry = 0%. Expiry days show higher reversal tendency.

7. **Strong alignment signal**: When both have strong views (excluding Mildly), reversal rate = 40.8% (29/71 days). Stronger conviction shows lower reversal tendency.

8. **Mixed days (opposing views)**: 25 days where FII and PRO disagreed. When FII was bullish and PRO bearish (17 days), it was a coin flip (50/50). When FII was bearish and PRO bullish (8 days), PRO's bullish view won 50.0% of the time — PRO tends to be more reliable when they disagree.

9. **Neutral days (no consensus)**: 167 days (54.6%) where one or both sides had no view — a perfect coin flip overall (50/50 direction split). However, when FII alone has a view and PRO is neutral, FII's solo signal is reliable: bullish correct 40.0% (10 days), bearish correct 70.0% (10 days). PRO's solo view shows no edge. Neutral days also have the widest avg range (1.01%) — institutional indecision means unpredictable volatility.

## Trading Implications

- When FII and PRO align, the first-half move in their direction is not reliable for holding through the full session
- Consider booking profits in the first half if positioned in the direction of institutional alignment
- The second-half reversal pattern suggests mean-reversion trades may be viable after the initial directional move
- Expiry days and high-VIX regimes may amplify or dampen these patterns — check the breakdowns above
- **This is retrospective analysis using T+1 data** — use as a framework for understanding institutional behavior, not as a standalone entry signal

## Last 6 Years: All Examples

*2020-09-03 to 2026-09-01 (308 trading days)*

### Worked then Reversed (first half aligned, second half reversed)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-25 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.91% | 0.66% | -0.25% | 0.66% |
| 2026-08-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 1.12% | 0.0% | -1.12% | -0.36% |
| 2026-07-07 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.74% | 0.27% | -0.47% | -0.45% |
| 2026-06-16 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 0.48% | 0.33% | -0.15% | 0.3% |
| 2026-06-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.04% | 1.41% | 1.41% | 0.0% | 1.27% |
| 2026-05-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.24% | 0.82% | 0.45% | -0.37% | -0.29% |
| 2026-04-28 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.93% | 0.55% | -0.39% | -0.14% |
| 2026-03-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.86% | 1.56% | 1.34% | -0.23% | 0.77% |
| 2026-01-13 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 1.14% | 0.01% | -1.14% | -0.71% |
| 2025-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.44% | 0.11% | -0.33% | -0.15% |
| 2025-11-18 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.59% | 0.03% | -0.56% | -0.49% |
| 2025-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.76% | 0.75% | -0.01% | 0.72% |
| 2025-09-02 | Strong Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.71% | 0.95% | 0.42% | -0.53% | -0.32% |
| 2025-08-07 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.75% | 1.19% | 0.69% | -0.49% | 0.66% |
| 2025-07-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.9% | 0.01% | -0.89% | -0.76% |
| 2024-12-19 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.56% | 0.54% | -0.03% | 0.36% |
| 2024-09-12 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.86% | 1.96% | 1.49% | -0.47% | 1.02% |
| 2024-07-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.49% | 0.13% | -0.36% | -0.27% |
| 2024-06-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.54% | 0.0% | -0.54% | -0.35% |
| 2024-05-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.08% | 1.69% | 0.37% | -1.32% | -1.15% |
| 2024-03-14 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 1.31% | 1.01% | -0.3% | 0.78% |
| 2024-02-29 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 0.91% | 0.57% | -0.34% | 0.49% |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.97% | 0.73% | 0.22% | -0.51% | 0.09% |
| 2024-02-01 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 0.8% | 0.24% | -0.56% | -0.41% |
| 2024-01-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.99% | 0.02% | -0.97% | -0.39% |
| 2024-01-18 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.95% | 1.19% | 0.58% | -0.6% | 0.29% |
| 2023-09-28 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.39% | 0.02% | -1.36% | -1.06% |
| 2023-09-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.61% | 0.2% | -0.41% | -0.13% |
| 2023-08-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 1.1% | 0.25% | -0.85% | -0.79% |
| 2023-07-27 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 1.33% | 0.08% | -1.25% | -0.76% |
| 2023-06-22 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.67% | 0.17% | -0.49% | -0.39% |
| 2023-06-08 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.86% | 0.28% | -0.58% | -0.42% |
| 2023-05-25 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.73% | 0.37% | -0.36% | 0.37% |
| 2023-05-11 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.47% | 0.0% | -0.47% | -0.29% |
| 2023-03-02 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.79% | 0.13% | -0.66% | -0.59% |
| 2023-02-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.06% | 1.17% | 0.78% | -0.39% | 0.54% |
| 2023-01-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.5% | 0.19% | -0.31% | -0.17% |
| 2022-12-08 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.47% | 0.29% | -0.18% | 0.23% |
| 2022-12-01 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 0.57% | 0.08% | -0.5% | -0.38% |
| 2022-11-03 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.79% | 0.76% | -0.02% | 0.44% |
| 2022-10-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.27% | 0.9% | 0.14% | -0.76% | -0.41% |
| 2022-09-22 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 1.08% | 0.64% | -0.44% | 0.15% |
| 2022-09-08 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 0.64% | 0.33% | -0.31% | 0.29% |
| 2022-05-26 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.59% | 1.86% | 0.61% | -1.25% | 0.6% |
| 2022-04-28 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.3% | 1.46% | 0.77% | -0.69% | 0.24% |
| 2022-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.73% | 1.84% | 0.0% | -1.84% | -1.14% |
| 2022-02-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.17% | 1.47% | 0.04% | -1.43% | -1.39% |
| 2021-12-30 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.02% | 0.67% | 0.36% | -0.31% | 0.16% |
| 2021-09-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 1.06% | 0.88% | -0.19% | 0.81% |
| 2021-06-17 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.94% | 0.97% | 0.77% | -0.19% | 0.21% |
| 2021-04-01 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.3% | 1.28% | 0.57% | -0.71% | 0.46% |
| 2021-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.42% | 0.76% | 0.1% | -0.66% | -0.22% |
| 2020-11-26 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.46% | 1.75% | 0.86% | -0.9% | 0.84% |
| 2020-10-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.47% | 1.18% | 0.95% | -0.23% | 0.32% |
| 2020-09-10 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.4% | 1.17% | 0.88% | -0.3% | 0.8% |

### Against then Recovered (first half against view, second half recovered)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-07-21 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.82% | 0.52% | 0.19% | -0.33% | -0.09% |
| 2026-06-09 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 0.75% | 0.09% | -0.66% | -0.01% |
| 2026-05-12 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.72% | 0.15% | -1.58% | -1.23% |
| 2026-04-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.19% | 1.49% | 1.35% | -0.14% | 0.97% |
| 2026-03-10 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.47% | 0.92% | 0.09% | -0.83% | 0.02% |
| 2026-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 1.23% | 0.0% | -1.23% | -0.71% |
| 2026-02-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.76% | 0.49% | -0.26% | 0.3% |
| 2025-12-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.76% | 0.22% | -0.54% | -0.1% |
| 2025-11-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 0.67% | 0.13% | -0.54% | -0.53% |
| 2025-10-14 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.99% | 0.13% | -0.86% | -0.61% |
| 2025-09-23 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.7% | 0.21% | -0.49% | -0.09% |
| 2025-08-14 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.76% | 0.31% | 0.27% | -0.04% | 0.04% |
| 2025-07-03 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.8% | 0.32% | -0.47% | -0.42% |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.21% | 1.17% | -0.04% | 1.03% |
| 2025-06-05 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.99% | 1.16% | 0.85% | -0.32% | 0.28% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 2.52% | 1.71% | -0.81% | 1.38% |
| 2025-04-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 0.81% | 0.22% | -0.59% | -0.39% |
| 2025-04-03 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.69% | 0.67% | -0.02% | 0.39% |
| 2025-03-06 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.86% | 1.38% | 0.36% | -1.03% | 0.24% |
| 2025-01-30 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 0.79% | 0.66% | -0.13% | 0.55% |
| 2025-01-23 | Strong Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 0.78% | 0.62% | -0.16% | 0.38% |
| 2025-01-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.79% | 0.06% | -0.73% | -0.5% |
| 2025-01-02 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 2.0% | 1.87% | -0.13% | 1.62% |
| 2024-11-07 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 1.32% | 0.06% | -1.27% | -1.2% |
| 2024-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.82% | 0.09% | -0.73% | -0.46% |
| 2024-10-24 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.92% | 0.57% | 0.28% | -0.29% | 0.01% |
| 2024-10-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.2% | 0.01% | -1.19% | -1.11% |
| 2024-08-14 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.02% | 0.4% | 0.05% | -0.35% | -0.16% |
| 2024-07-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.86% | 0.03% | -0.83% | -0.24% |
| 2024-06-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.19% | 1.17% | 0.49% | -0.68% | 0.22% |
| 2024-05-30 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 1.28% | 0.39% | -0.89% | -0.27% |
| 2024-05-23 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.35% | 1.84% | 1.68% | -0.16% | 1.49% |
| 2024-04-25 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 1.44% | 1.38% | -0.05% | 1.09% |
| 2024-01-04 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.89% | 0.56% | 0.37% | -0.19% | 0.3% |
| 2023-11-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.8% | 0.71% | 0.25% | -0.46% | 0.09% |
| 2023-11-09 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.44% | 0.03% | -0.41% | -0.27% |
| 2023-08-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 1.23% | 0.38% | -0.85% | -0.36% |
| 2023-07-20 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.18% | 0.81% | -0.37% | 0.7% |
| 2023-07-13 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.93% | 0.37% | -0.56% | -0.27% |
| 2023-06-28 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.79% | 0.54% | -0.25% | 0.44% |
| 2023-06-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.62% | 0.0% | -0.61% | -0.5% |
| 2023-05-18 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 1.04% | 0.05% | -1.0% | -0.84% |
| 2023-04-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.75% | 0.66% | -0.08% | 0.62% |
| 2023-02-23 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.93% | 0.25% | -0.67% | -0.29% |
| 2023-01-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 1.36% | 0.0% | -1.36% | -1.01% |
| 2023-01-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.96% | 1.25% | 0.09% | -1.16% | -0.56% |
| 2022-12-22 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 1.36% | 0.15% | -1.2% | -0.95% |
| 2022-12-15 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 1.41% | 0.2% | -1.21% | -1.15% |
| 2022-09-15 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.29% | 0.27% | -1.02% | -0.96% |
| 2022-07-28 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.14% | 1.16% | 1.01% | -0.16% | 0.88% |
| 2022-07-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.32% | 0.32% | -1.0% | -0.44% |
| 2022-07-07 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.28% | 0.64% | 0.23% | -0.41% | 0.14% |
| 2022-05-19 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.4% | 1.3% | 0.41% | -0.89% | -0.56% |
| 2022-03-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 0.98% | 0.82% | -0.16% | 0.56% |
| 2022-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.55% | 3.01% | 0.93% | -2.08% | -2.0% |
| 2022-02-10 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.17% | 1.21% | 0.49% | -0.72% | 0.19% |
| 2022-01-20 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.12% | 1.59% | 0.07% | -1.52% | -0.77% |
| 2021-12-02 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.23% | 1.51% | 1.36% | -0.14% | 1.27% |
| 2021-11-11 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.03% | 0.93% | 0.0% | -0.93% | -0.46% |
| 2021-10-28 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 2.13% | 0.0% | -2.13% | -1.79% |
| 2021-10-21 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.82% | 0.0% | -1.82% | -0.89% |
| 2021-10-07 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.09% | 0.51% | 0.26% | -0.25% | -0.08% |
| 2021-09-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.75% | 0.6% | -0.16% | 0.5% |
| 2021-03-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.41% | 2.1% | 0.0% | -2.1% | -1.54% |
| 2021-02-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.52% | 0.68% | 0.62% | -0.06% | 0.16% |

### Exceeded Half VIX Range + Worked and Remained (52 days — strongest signal, ~85% win rate)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-06-09 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 0.75% | 0.09% | -0.66% | -0.01% |
| 2026-05-12 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.72% | 0.15% | -1.58% | -1.23% |
| 2026-04-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.19% | 1.49% | 1.35% | -0.14% | 0.97% |
| 2026-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 1.23% | 0.0% | -1.23% | -0.71% |
| 2026-02-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.76% | 0.49% | -0.26% | 0.3% |
| 2025-12-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.76% | 0.22% | -0.54% | -0.1% |
| 2025-11-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 0.67% | 0.13% | -0.54% | -0.53% |
| 2025-10-14 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.99% | 0.13% | -0.86% | -0.61% |
| 2025-09-23 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.7% | 0.21% | -0.49% | -0.09% |
| 2025-07-03 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.8% | 0.32% | -0.47% | -0.42% |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.21% | 1.17% | -0.04% | 1.03% |
| 2025-06-05 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.99% | 1.16% | 0.85% | -0.32% | 0.28% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 2.52% | 1.71% | -0.81% | 1.38% |
| 2025-04-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 0.81% | 0.22% | -0.59% | -0.39% |
| 2025-04-03 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.69% | 0.67% | -0.02% | 0.39% |
| 2025-01-30 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 0.79% | 0.66% | -0.13% | 0.55% |
| 2025-01-23 | Strong Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 0.78% | 0.62% | -0.16% | 0.38% |
| 2025-01-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.79% | 0.06% | -0.73% | -0.5% |
| 2025-01-02 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 2.0% | 1.87% | -0.13% | 1.62% |
| 2024-11-07 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 1.32% | 0.06% | -1.27% | -1.2% |
| 2024-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.82% | 0.09% | -0.73% | -0.46% |
| 2024-10-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.2% | 0.01% | -1.19% | -1.11% |
| 2024-07-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.86% | 0.03% | -0.83% | -0.24% |
| 2024-05-30 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 1.28% | 0.39% | -0.89% | -0.27% |
| 2024-05-23 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.35% | 1.84% | 1.68% | -0.16% | 1.49% |
| 2024-04-25 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 1.44% | 1.38% | -0.05% | 1.09% |
| 2023-11-09 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.44% | 0.03% | -0.41% | -0.27% |
| 2023-08-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 1.23% | 0.38% | -0.85% | -0.36% |
| 2023-07-20 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.18% | 0.81% | -0.37% | 0.7% |
| 2023-07-13 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.93% | 0.37% | -0.56% | -0.27% |
| 2023-06-28 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.79% | 0.54% | -0.25% | 0.44% |
| 2023-06-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.62% | 0.0% | -0.61% | -0.5% |
| 2023-05-18 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 1.04% | 0.05% | -1.0% | -0.84% |
| 2023-04-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.75% | 0.66% | -0.08% | 0.62% |
| 2023-02-23 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.93% | 0.25% | -0.67% | -0.29% |
| 2023-01-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 1.36% | 0.0% | -1.36% | -1.01% |
| 2023-01-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.96% | 1.25% | 0.09% | -1.16% | -0.56% |
| 2022-12-22 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 1.36% | 0.15% | -1.2% | -0.95% |
| 2022-12-15 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 1.41% | 0.2% | -1.21% | -1.15% |
| 2022-09-15 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.29% | 0.27% | -1.02% | -0.96% |
| 2022-07-28 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.14% | 1.16% | 1.01% | -0.16% | 0.88% |
| 2022-07-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.32% | 0.32% | -1.0% | -0.44% |
| 2022-05-19 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.4% | 1.3% | 0.41% | -0.89% | -0.56% |
| 2022-03-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 0.98% | 0.82% | -0.16% | 0.56% |
| 2022-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.55% | 3.01% | 0.93% | -2.08% | -2.0% |
| 2022-01-20 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.12% | 1.59% | 0.07% | -1.52% | -0.77% |
| 2021-12-02 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.23% | 1.51% | 1.36% | -0.14% | 1.27% |
| 2021-11-11 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.03% | 0.93% | 0.0% | -0.93% | -0.46% |
| 2021-10-28 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 2.13% | 0.0% | -2.13% | -1.79% |
| 2021-10-21 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.82% | 0.0% | -1.82% | -0.89% |
| 2021-09-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.75% | 0.6% | -0.16% | 0.5% |
| 2021-03-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.41% | 2.1% | 0.0% | -2.1% | -1.54% |

### Reversed Before Half VIX Range + Reversed by Close (46 days — weak alignment, ~76% lose)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-25 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.91% | 0.66% | -0.25% | 0.66% |
| 2026-08-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 1.12% | 0.0% | -1.12% | -0.36% |
| 2026-07-07 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.74% | 0.27% | -0.47% | -0.45% |
| 2026-06-16 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 0.48% | 0.33% | -0.15% | 0.3% |
| 2026-06-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.04% | 1.41% | 1.41% | 0.0% | 1.27% |
| 2026-05-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.24% | 0.82% | 0.45% | -0.37% | -0.29% |
| 2026-04-28 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.93% | 0.55% | -0.39% | -0.14% |
| 2026-03-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.86% | 1.56% | 1.34% | -0.23% | 0.77% |
| 2026-01-13 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 1.14% | 0.01% | -1.14% | -0.71% |
| 2025-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.44% | 0.11% | -0.33% | -0.15% |
| 2025-11-18 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.59% | 0.03% | -0.56% | -0.49% |
| 2025-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.76% | 0.75% | -0.01% | 0.72% |
| 2025-07-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.9% | 0.01% | -0.89% | -0.76% |
| 2024-12-19 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.56% | 0.54% | -0.03% | 0.36% |
| 2024-07-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.49% | 0.13% | -0.36% | -0.27% |
| 2024-06-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.54% | 0.0% | -0.54% | -0.35% |
| 2024-05-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.08% | 1.69% | 0.37% | -1.32% | -1.15% |
| 2024-03-14 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 1.31% | 1.01% | -0.3% | 0.78% |
| 2024-02-29 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 0.91% | 0.57% | -0.34% | 0.49% |
| 2024-02-01 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 0.8% | 0.24% | -0.56% | -0.41% |
| 2024-01-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.99% | 0.02% | -0.97% | -0.39% |
| 2023-09-28 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.39% | 0.02% | -1.36% | -1.06% |
| 2023-09-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.61% | 0.2% | -0.41% | -0.13% |
| 2023-08-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 1.1% | 0.25% | -0.85% | -0.79% |
| 2023-07-27 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 1.33% | 0.08% | -1.25% | -0.76% |
| 2023-06-22 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.67% | 0.17% | -0.49% | -0.39% |
| 2023-06-08 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.86% | 0.28% | -0.58% | -0.42% |
| 2023-05-25 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.73% | 0.37% | -0.36% | 0.37% |
| 2023-05-11 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.47% | 0.0% | -0.47% | -0.29% |
| 2023-03-02 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.79% | 0.13% | -0.66% | -0.59% |
| 2023-02-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.06% | 1.17% | 0.78% | -0.39% | 0.54% |
| 2023-01-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.5% | 0.19% | -0.31% | -0.17% |
| 2022-12-08 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.47% | 0.29% | -0.18% | 0.23% |
| 2022-12-01 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 0.57% | 0.08% | -0.5% | -0.38% |
| 2022-11-03 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.79% | 0.76% | -0.02% | 0.44% |
| 2022-10-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.27% | 0.9% | 0.14% | -0.76% | -0.41% |
| 2022-09-22 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 1.08% | 0.64% | -0.44% | 0.15% |
| 2022-09-08 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 0.64% | 0.33% | -0.31% | 0.29% |
| 2022-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.73% | 1.84% | 0.0% | -1.84% | -1.14% |
| 2022-02-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.17% | 1.47% | 0.04% | -1.43% | -1.39% |
| 2021-12-30 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.02% | 0.67% | 0.36% | -0.31% | 0.16% |
| 2021-09-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 1.06% | 0.88% | -0.19% | 0.81% |
| 2021-06-17 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.94% | 0.97% | 0.77% | -0.19% | 0.21% |
| 2021-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.42% | 0.76% | 0.1% | -0.66% | -0.22% |
| 2020-10-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.47% | 1.18% | 0.95% | -0.23% | 0.32% |
| 2020-09-10 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.4% | 1.17% | 0.88% | -0.3% | 0.8% |

### Mixed Days (FII vs PRO opposing) — 25 days

| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|
| 2026-09-01 | Mildly Bullish | Strong Bearish | Top to Down | 0.7% | 0.79% | 0.27% | -0.52% | -0.09% |
| 2026-08-18 | Mildly Bullish | Bearish | Top to Down | 0.71% | 0.47% | 0.19% | -0.28% | -0.28% |
| 2026-07-28 | Bullish | Mildly Bearish | Down to Up | 0.8% | 0.36% | 0.29% | -0.07% | 0.07% |
| 2026-02-10 | Bullish | Strong Bearish | Top to Down | 0.77% | 0.46% | 0.26% | -0.2% | -0.02% |
| 2025-09-09 | Mildly Bullish | Bearish | Down to Up | 0.68% | 0.31% | 0.11% | -0.2% | 0.06% |
| 2025-04-24 | Bullish | Mildly Bearish | Top to Down | 1.01% | 0.54% | 0.29% | -0.25% | -0.14% |
| 2025-03-20 | Mildly Bullish | Bearish | Down to Up | 0.84% | 1.05% | 0.78% | -0.27% | 0.56% |
| 2024-12-05 | Mildly Bullish | Mildly Bearish | Down to Up | 0.91% | 2.29% | 1.3% | -0.99% | 0.66% |
| 2024-11-28 | Mildly Bullish | Bearish | Top to Down | 0.92% | 1.95% | 0.29% | -1.65% | -1.3% |
| 2024-11-14 | Mildly Bearish | Strong Bullish | Down to Up | 0.97% | 0.81% | 0.57% | -0.25% | 0.07% |
| 2024-08-29 | Mildly Bullish | Strong Bearish | Down to Up | 0.88% | 0.78% | 0.63% | -0.15% | 0.49% |
| 2024-08-08 | Strong Bearish | Strong Bullish | Top to Down | 1.02% | 1.08% | 0.38% | -0.7% | -0.62% |
| 2024-08-01 | Strong Bearish | Strong Bullish | Top to Down | 0.83% | 0.49% | 0.19% | -0.3% | -0.1% |
| 2024-07-25 | Bearish | Bullish | Down to Up | 0.74% | 0.89% | 0.81% | -0.08% | 0.76% |
| 2024-06-27 | Bullish | Strong Bearish | Down to Up | 0.89% | 1.18% | 0.86% | -0.32% | 0.65% |
| 2024-06-20 | Bullish | Strong Bearish | Top to Down | 0.86% | 0.77% | 0.16% | -0.61% | -0.03% |
| 2024-04-10 | Mildly Bullish | Strong Bearish | Down to Up | 0.72% | 0.45% | 0.24% | -0.2% | 0.07% |
| 2024-03-28 | Bearish | Strong Bullish | Down to Up | 0.8% | 1.59% | 1.59% | 0.0% | 0.81% |
| 2024-02-22 | Bullish | Strong Bearish | Down to Up | 1.0% | 1.71% | 0.77% | -0.93% | 0.61% |
| 2024-02-08 | Mildly Bearish | Bullish | Top to Down | 0.98% | 1.57% | 0.01% | -1.56% | -1.14% |
| 2024-01-11 | Bearish | Strong Bullish | Top to Down | 0.82% | 0.61% | 0.18% | -0.43% | -0.09% |
| 2023-12-28 | Bearish | Strong Bullish | Down to Up | 0.98% | 0.57% | 0.4% | -0.17% | 0.27% |
| 2023-12-07 | Bullish | Strong Bearish | Top to Down | 0.87% | 0.43% | 0.04% | -0.39% | -0.08% |
| 2022-11-17 | Bullish | Mildly Bearish | Top to Down | 0.95% | 0.57% | 0.32% | -0.25% | -0.13% |
| 2021-05-19 | Bullish | Mildly Bearish | Top to Down | 1.21% | 0.82% | 0.49% | -0.33% | -0.26% |

### FII Solo View (PRO Neutral) — 20 days

| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|
| 2026-07-14 | Bullish | Neutral | Top to Down | 0.84% | 0.55% | 0.37% | -0.18% | -0.14% |
| 2026-05-26 | Strong Bullish | Neutral | Top to Down | 1.05% | 0.85% | 0.36% | -0.49% | -0.29% |
| 2026-03-17 | Bullish | Neutral | Down to Up | 1.36% | 1.32% | 0.7% | -0.62% | 0.28% |
| 2026-02-03 | Bearish | Neutral | Top to Down | 0.87% | 2.66% | 0.13% | -2.53% | -2.26% |
| 2025-10-07 | Mildly Bullish | Neutral | Down to Up | 0.64% | 0.58% | 0.54% | -0.04% | 0.11% |
| 2025-09-30 | Mildly Bullish | Neutral | Top to Down | 0.72% | 0.58% | 0.16% | -0.42% | -0.24% |
| 2024-12-12 | Bullish | Neutral | Top to Down | 0.84% | 0.6% | 0.29% | -0.31% | -0.26% |
| 2024-10-10 | Bearish | Neutral | Top to Down | 0.89% | 0.62% | 0.27% | -0.35% | -0.24% |
| 2024-04-04 | Mildly Bearish | Neutral | Top to Down | 0.72% | 1.4% | 0.12% | -1.28% | -0.23% |
| 2023-09-07 | Strong Bearish | Neutral | Down to Up | 0.67% | 0.95% | 0.71% | -0.25% | 0.64% |
| 2023-04-20 | Mildly Bullish | Neutral | Top to Down | 0.77% | 0.56% | 0.26% | -0.31% | -0.08% |
| 2022-10-20 | Bearish | Neutral | Down to Up | 1.1% | 0.93% | 0.92% | -0.01% | 0.82% |
| 2022-06-02 | Bearish | Neutral | Down to Up | 1.31% | 1.22% | 1.0% | -0.22% | 0.94% |
| 2022-04-13 | Bearish | Neutral | Top to Down | 1.14% | 1.17% | 0.36% | -0.81% | -0.75% |
| 2022-03-31 | Mildly Bullish | Neutral | Top to Down | 1.3% | 0.7% | 0.23% | -0.48% | -0.29% |
| 2021-10-14 | Mildly Bullish | Neutral | Down to Up | 1.01% | 0.55% | 0.42% | -0.13% | 0.36% |
| 2021-09-30 | Bearish | Neutral | Top to Down | 1.19% | 0.88% | 0.13% | -0.75% | -0.62% |
| 2021-08-18 | Bearish | Neutral | Top to Down | 0.84% | 0.98% | 0.06% | -0.93% | -0.85% |
| 2021-01-21 | Mildly Bearish | Neutral | Top to Down | 1.36% | 1.59% | 0.15% | -1.44% | -0.68% |
| 2020-10-01 | Mildly Bullish | Neutral | Down to Up | 1.23% | 0.68% | 0.56% | -0.12% | 0.51% |


---
*Generated from 312 trading days (2020-08-06 to 2026-09-01)*
