# FII-PRO Alignment Analysis — All Trading Days (Sensex Daily CSV)

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
| Total Trading Days | 1323 | 100.0% |
| **Aligned Days (Bullish + Bearish)** | **583** | **44.1%** |
| Bullish Alignment | 288 | 21.8% |
| Bearish Alignment | 295 | 22.3% |
| Mixed (opposing views) | 92 | 7.0% |
| Neutral/Unclear | 648 | 49.0% |

## Alignment Outcome Breakdown

When FII and PRO align, does the first half move in their direction and then reverse?

### All Aligned Days (583 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 295 | 50.6% | 0.42% | -0.56% | -0.06% |
| Against then Recovered | 288 | 49.4% | 0.41% | -0.58% | -0.08% |

### Bullish Alignment (288 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 156 | 54.2% | 0.18% | -0.79% | -0.55% |
| Against then Recovered | 132 | 45.8% | 0.65% | -0.26% | 0.48% |

### Bearish Alignment (295 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 139 | 47.1% | 0.70% | -0.30% | 0.48% |
| Against then Recovered | 156 | 52.9% | 0.20% | -0.85% | -0.55% |

## Worked and Remained: Did the Aligned View Win by Close?

A different lens: regardless of intraday path, did the market **close** in the aligned direction?

- **Worked and Remained**: Close was in the aligned direction (bullish alignment + close > open, or bearish alignment + close < open)
- **Reversed by Close**: Close was against the aligned direction

### Overall (583 aligned days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg Range% |
|---------------|------:|--:|----------------:|----------:|---------:|-----------:|
| Worked and Remained | 287 | 49.2% | -0.08% | 0.41% | -0.58% | 0.99% |
| Reversed by Close | 296 | 50.8% | -0.06% | 0.42% | -0.56% | 0.98% |

### Bullish Alignment (288 days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |
|---------------|------:|--:|----------------:|----------:|---------:|
| Worked and Remained | 131 | 45.5% | 0.48% | 0.65% | -0.26% |
| Reversed by Close | 157 | 54.5% | -0.54% | 0.18% | -0.78% |

### Bearish Alignment (295 days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |
|---------------|------:|--:|----------------:|----------:|---------:|
| Worked and Remained | 156 | 52.9% | -0.55% | 0.20% | -0.85% |
| Reversed by Close | 139 | 47.1% | 0.48% | 0.70% | -0.30% |

### Worked and Remained: Expiry vs Non-Expiry

| Context | Aligned | Worked and Remained | % | Reversed by Close | % |
|---------|--------:|--------------------:|--:|------------------:|--:|
| Expiry Days | 230 | 121 | 52.6% | 109 | 47.4% |
| Non-Expiry Days | 353 | 166 | 47.0% | 187 | 53.0% |

### Worked and Remained: VIX Regime

| VIX Regime | Aligned | Worked and Remained | % | Reversed by Close | % |
|------------|--------:|--------------------:|--:|------------------:|--:|
| Low (<15) | 128 | 64 | 50.0% | 64 | 50.0% |
| Normal (15-20) | 72 | 38 | 52.8% | 34 | 47.2% |
| Elevated (20-30) | 30 | 19 | 63.3% | 11 | 36.7% |
| High (>30) | 0 | 0 | - | 0 | - |

### Worked and Remained: Year-over-Year

| Year | Aligned | Worked and Remained | % | Reversed by Close | % |
|------|--------:|--------------------:|--:|------------------:|--:|
| 2020 | 14 | 6 | 42.9% | 8 | 57.1% |
| 2021 | 67 | 39 | 58.2% | 28 | 41.8% |
| 2022 | 98 | 51 | 52.0% | 47 | 48.0% |
| 2023 | 129 | 64 | 49.6% | 65 | 50.4% |
| 2024 | 116 | 49 | 42.2% | 67 | 57.8% |
| 2025 | 90 | 47 | 52.2% | 43 | 47.8% |
| 2026 | 69 | 31 | 44.9% | 38 | 55.1% |

## VIX Half-Range Exhaustion: Did the Move Exhaust Before Reversing?

Compares the first-half move in the aligned direction against **half of the VIX-predicted range**.
If the move exceeded half the predicted range, it suggests momentum exhaustion before reversal.
If it reversed before reaching half, the reversal happened without significant momentum.

- **Exceeded Half then Reversed**: Aligned-direction move > ½ × VIX predicted range
- **Reversed Before Half**: Aligned-direction move ≤ ½ × VIX predicted range

### Overall (230 aligned days with VIX data)

| VIX Exhaustion | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg VIX Predicted% |
|----------------|------:|--:|----------------:|----------:|---------:|-------------------:|
| Exceeded Half then Reversed | 101 | 43.9% | -0.05% | 0.51% | -0.64% | 0.97% |
| Reversed Before Half | 129 | 56.1% | -0.15% | 0.34% | -0.57% | 0.97% |

### Cross-Tab: VIX Exhaustion × Close Outcome

Does exceeding half the VIX range predict whether the aligned view wins by close?

| VIX Exhaustion | Worked and Remained | % | Reversed by Close | % | Total |
|----------------|--------------------:|--:|------------------:|--:|------:|
| Exceeded Half then Reversed | 88 | 87.1% | 13 | 12.9% | 101 |
| Reversed Before Half | 33 | 25.6% | 96 | 74.4% | 129 |

### Bullish Alignment (121 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 37 | 30.6% | 33 | 89.2% | 0.67% |
| Reversed Before Half | 84 | 69.4% | 23 | 27.4% | -0.41% |

### Bearish Alignment (109 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 64 | 58.7% | 55 | 85.9% | -0.46% |
| Reversed Before Half | 45 | 41.3% | 10 | 22.2% | 0.32% |

### VIX Exhaustion by VIX Regime

| VIX Regime | Total | Exceeded Half | % | Reversed Before Half | % |
|------------|------:|--------------:|--:|---------------------:|--:|
| Low (<15) | 128 | 56 | 43.8% | 72 | 56.2% |
| Normal (15-20) | 72 | 31 | 43.1% | 41 | 56.9% |
| Elevated (20-30) | 30 | 14 | 46.7% | 16 | 53.3% |
| High (>30) | 0 | 0 | - | 0 | - |

## Strong Alignment Analysis

Strong alignment = both FII and PRO have Bullish/Strong Bullish or Bearish/Strong Bearish
(excluding Mildly variants).

| Category | Total | Worked then Reversed | % | Against then Recovered | % |
|----------|------:|---------------------:|--:|-----------------------:|--:|
| Strong Bullish | 209 | 110 | 52.6% | 99 | 47.4% |
| Strong Bearish | 205 | 92 | 44.9% | 113 | 55.1% |
| All Strong Aligned | 414 | 202 | 48.8% | 212 | 51.2% |

## Mixed Days: When FII and PRO Oppose Each Other

When FII and PRO have opposing directional views (one bullish, one bearish),
whose view wins by close?

### Overview (92 mixed days)

| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |
|----------|-----:|----------:|----------:|----------------:|-----------:|
| FII Bullish + PRO Bearish | 51 | 26 (51.0%) | 25 (49.0%) | -0.03% | 0.86% |
| FII Bearish + PRO Bullish | 41 | 15 (36.6%) | 26 (63.4%) | 0.16% | 1.06% |
| All Mixed | 92 | 41 (44.6%) | 51 (55.4%) | 0.06% | 0.95% |

### Who Won by Close?

| Sub-Type | Days | FII Correct | FII% | PRO Correct | PRO% |
|----------|-----:|------------:|-----:|------------:|-----:|
| FII Bullish + PRO Bearish | 51 | 25 | 49.0% | 26 | 51.0% |
| FII Bearish + PRO Bullish | 41 | 14 | 34.1% | 26 | 63.4% |

### Mixed Days: Expiry vs Non-Expiry

| Context | Days | Avg Open→Close% | Avg Range% |
|---------|-----:|----------------:|-----------:|
| Expiry | 56 | -0.01% | 0.92% |
| Non-Expiry | 36 | 0.17% | 0.98% |

## Neutral Days: When One or Both Sides Have No View

When one or both participants are Neutral, there is no directional consensus.
Does a solo directional view from one side carry any weight?

### Overview (648 neutral days)

| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |
|----------|-----:|----------:|----------:|----------------:|-----------:|
| Both Neutral | 167 | 87 (52.1%) | 80 (47.9%) | -0.05% | 1.07% |
| FII Neutral + PRO Bullish | 188 | 88 (46.8%) | 100 (53.2%) | 0.00% | 1.04% |
| FII Neutral + PRO Bearish | 203 | 101 (49.8%) | 102 (50.2%) | 0.01% | 1.05% |
| FII Bullish + PRO Neutral | 47 | 18 (38.3%) | 29 (61.7%) | 0.09% | 0.87% |
| FII Bearish + PRO Neutral | 43 | 24 (55.8%) | 19 (44.2%) | -0.21% | 1.11% |
| All Neutral/Unclear | 648 | 318 (49.1%) | 330 (50.9%) | -0.02% | 1.04% |

### Solo View Accuracy: Did the One Directional Side Win?

| Sub-Type | Days | View Correct | % | Avg Open→Close% |
|----------|-----:|-------------:|--:|----------------:|
| FII Neutral + PRO Bullish | 188 | 100 | 53.2% | 0.00% |
| FII Neutral + PRO Bearish | 203 | 100 | 49.3% | 0.01% |
| FII Bullish + PRO Neutral | 47 | 29 | 61.7% | 0.09% |
| FII Bearish + PRO Neutral | 43 | 24 | 55.8% | -0.21% |

### Range Comparison: Aligned vs Mixed vs Neutral

| Category | Days | Avg Range% | Avg High% | Avg Low% |
|----------|-----:|-----------:|----------:|---------:|
| Aligned | 583 | 0.98% | 0.41% | -0.57% |
| Mixed | 92 | 0.95% | 0.47% | -0.48% |
| Neutral/Unclear | 648 | 1.04% | 0.47% | -0.58% |

## Expiry vs Non-Expiry

| Context | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg High% | Avg Low% |
|---------|-------------:|---------------------:|--:|-----------------------:|--:|----------:|---------:|
| Expiry Days | 230 | 109 | 47.4% | 121 | 52.6% | 0.41% | -0.60% |
| Non-Expiry Days | 353 | 186 | 52.7% | 167 | 47.3% | 0.41% | -0.55% |

## VIX Regime Analysis

| VIX Regime | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg Range% |
|------------|-------------:|---------------------:|--:|-----------------------:|--:|-----------:|
| Low (<15) | 128 | 64 | 50.0% | 64 | 50.0% | 0.88% |
| Normal (15-20) | 72 | 34 | 47.2% | 38 | 52.8% | 1.12% |
| Elevated (20-30) | 30 | 11 | 36.7% | 19 | 63.3% | 1.36% |
| High (>30) | 0 | 0 | - | 0 | - | - |

## Year-over-Year Trends

| Year | Trading Days | Aligned Days | Alignment% | Bullish Aligned | Bearish Aligned | Worked then Reversed | Reversal% |
|------|------------:|-------------:|-----------:|----------------:|----------------:|---------------------:|----------:|
| 2020 | 94 | 14 | 14.9% | 7 | 7 | 8 | 57.1% |
| 2021 | 219 | 67 | 30.6% | 36 | 31 | 28 | 41.8% |
| 2022 | 222 | 98 | 44.1% | 43 | 55 | 47 | 48.0% |
| 2023 | 213 | 129 | 60.6% | 68 | 61 | 64 | 49.6% |
| 2024 | 212 | 116 | 54.7% | 57 | 59 | 67 | 57.8% |
| 2025 | 221 | 90 | 40.7% | 44 | 46 | 43 | 47.8% |
| 2026 | 142 | 69 | 48.6% | 33 | 36 | 38 | 55.1% |

## Detailed: Bullish Alignment Days

When FII+PRO both lean bullish:

- **Top to Down** (Worked then Reversed): Market rose in first half (aligned), then sold off
- **Down to Up** (Against then Recovered): Market fell in first half (against view), then recovered

| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |
|---------|------:|--:|-------------------:|-------------------:|-----------------:|
| Worked then Reversed (Top→Down) | 156 | 54.2% | 0.18% | -0.79% | -0.55% |
| Against then Recovered (Down→Up) | 132 | 45.8% | 0.65% | -0.26% | 0.48% |

## Detailed: Bearish Alignment Days

When FII+PRO both lean bearish:

- **Down to Up** (Worked then Reversed): Market fell in first half (aligned), then recovered
- **Top to Down** (Against then Recovered): Market rose in first half (against view), then sold off

| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |
|---------|------:|--:|-------------------:|-------------------:|-----------------:|
| Worked then Reversed (Down→Up) | 139 | 47.1% | 0.70% | -0.30% | 0.48% |
| Against then Recovered (Top→Down) | 156 | 52.9% | 0.20% | -0.85% | -0.55% |

## Key Findings

1. **Alignment frequency**: FII and PRO aligned on 583 of 1323 days (44.1%). Bullish alignment (288) vs Bearish alignment (295).

2. **Reversal is the dominant pattern**: On alignment days, "Worked then Reversed" occurred 50.6% of the time (295/583 days). This means when institutions agree, the first half tends to move in their direction but the second half often reverses.

3. **Worked and Remained (close validated view)**: On 49.2% of alignment days (287/583), the market closed in the aligned direction — meaning the institutional consensus was ultimately correct by end of day. The remaining 50.8% closed against the aligned view.

4. **VIX half-range exhaustion**: 43.9% of alignment days with VIX data exceeded half the VIX-predicted range (101/230). Among those, 87.1% closed in the aligned direction vs 25.6% for days that reversed before half range.

5. **Bullish vs Bearish reversal**: Bullish alignment reversal rate = 54.2%, Bearish alignment reversal rate = 47.1%.

6. **Expiry effect**: Reversal rate on expiry days = 47.4% vs non-expiry = 52.7%.

7. **Strong alignment signal**: When both have strong views (excluding Mildly), reversal rate = 48.8% (202/414 days). Stronger conviction shows lower reversal tendency.

8. **Mixed days (opposing views)**: 92 days where FII and PRO disagreed. When FII bullish + PRO bearish (51 days): FII correct 49.0%. When FII bearish + PRO bullish (41 days): PRO correct 63.4%.

9. **Neutral days (no consensus)**: 648 days (49.0%) where one or both sides had no view. FII solo bearish correct 55.8% (43 days). FII solo bullish correct 61.7% (47 days). Avg range on neutral days: 1.04%.

## Trading Implications

- When FII and PRO align, the first-half move in their direction is not reliable for holding through the full session
- Consider booking profits in the first half if positioned in the direction of institutional alignment
- The second-half reversal pattern suggests mean-reversion trades may be viable after the initial directional move
- Expiry days and high-VIX regimes may amplify or dampen these patterns — check the breakdowns above
- Non-expiry days now included provide a broader sample for validation
- **This is retrospective analysis using T+1 data** — use as a framework for understanding institutional behavior, not as a standalone entry signal

## Last 6 Years: All Examples

*2020-08-06 to 2026-09-01 (1323 trading days)*

### Worked then Reversed (first half aligned, second half reversed)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-31 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.56% | 0.05% | -0.51% | -0.15% |
| 2026-08-26 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.70% | 0.15% | -0.55% | -0.55% |
| 2026-08-25 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.91% | 0.66% | -0.25% | 0.66% |
| 2026-08-10 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.45% | 0.16% | -0.29% | 0.01% |
| 2026-08-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 1.12% | 0.00% | -1.12% | -0.36% |
| 2026-07-09 | Strong Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.92% | 0.87% | 0.86% | -0.01% | 0.22% |
| 2026-07-07 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.74% | 0.27% | -0.47% | -0.45% |
| 2026-07-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.52% | 0.01% | -0.51% | -0.43% |
| 2026-06-25 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.84% | 0.92% | 0.56% | -0.36% | -0.30% |
| 2026-06-16 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 0.48% | 0.33% | -0.15% | 0.30% |
| 2026-06-15 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.81% | 0.11% | -0.70% | -0.53% |
| 2026-06-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.04% | 1.41% | 1.41% | 0.00% | 1.27% |
| 2026-05-27 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.52% | 0.43% | -0.09% | 0.17% |
| 2026-05-22 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.70% | 0.69% | -0.00% | 0.33% |
| 2026-05-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.24% | 0.82% | 0.45% | -0.37% | -0.29% |
| 2026-05-15 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.96% | 0.45% | -0.51% | -0.30% |
| 2026-05-13 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.37% | 0.94% | -0.43% | 0.28% |
| 2026-05-07 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.81% | 0.34% | -0.47% | -0.25% |
| 2026-04-28 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.93% | 0.55% | -0.39% | -0.14% |
| 2026-04-22 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.67% | 0.18% | -0.48% | -0.42% |
| 2026-04-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.98% | 0.37% | -0.62% | -0.25% |
| 2026-04-17 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.14% | 0.85% | -0.29% | 0.83% |
| 2026-04-10 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.91% | 0.81% | -0.10% | 0.71% |
| 2026-04-09 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.24% | 1.29% | 0.34% | -0.95% | -0.60% |
| 2026-03-20 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.20% | 1.02% | -0.18% | 0.11% |
| 2026-03-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.59% | 0.88% | -0.71% | 0.58% |
| 2026-03-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.86% | 1.56% | 1.34% | -0.23% | 0.77% |
| 2026-02-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.12% | 1.01% | -0.11% | 0.63% |
| 2026-02-19 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 1.92% | 0.05% | -1.87% | -1.77% |
| 2026-02-16 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.28% | 1.08% | -0.20% | 1.02% |
| 2026-02-11 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.42% | 0.05% | -0.38% | -0.20% |
| 2026-02-06 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.83% | 0.38% | -0.44% | 0.26% |
| 2026-02-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.69% | 0.01% | -0.68% | -0.44% |
| 2026-02-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.73% | 1.26% | -0.47% | 1.14% |
| 2026-01-21 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.52% | 0.64% | -0.88% | 0.11% |
| 2026-01-13 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 1.14% | 0.01% | -1.14% | -0.71% |
| 2026-01-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.62% | 0.15% | -0.47% | -0.34% |
| 2026-01-01 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.32% | 0.09% | -0.23% | -0.13% |
| 2025-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.44% | 0.11% | -0.33% | -0.15% |
| 2025-12-10 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.82% | 0.32% | -0.50% | -0.47% |
| 2025-12-08 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.10% | 0.07% | -1.02% | -0.87% |
| 2025-11-27 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.64% | 0.19% | -0.45% | -0.16% |
| 2025-11-19 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.84% | 0.60% | -0.24% | 0.52% |
| 2025-11-18 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.59% | 0.03% | -0.56% | -0.49% |
| 2025-11-17 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.45% | 0.29% | -0.16% | 0.25% |
| 2025-11-14 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.77% | 0.67% | -0.11% | 0.58% |
| 2025-11-13 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.76% | 0.78% | 0.40% | -0.38% | -0.08% |
| 2025-10-30 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.72% | 0.18% | -0.54% | -0.36% |
| 2025-10-09 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.65% | 0.70% | 0.50% | -0.20% | 0.38% |
| 2025-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.76% | 0.75% | -0.01% | 0.72% |
| 2025-09-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 1.09% | 0.00% | -1.09% | -0.96% |
| 2025-09-02 | Strong Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.71% | 0.95% | 0.42% | -0.53% | -0.32% |
| 2025-08-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.92% | 0.08% | -0.84% | -0.76% |
| 2025-08-25 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.51% | 0.29% | -0.22% | 0.12% |
| 2025-08-13 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.53% | 0.32% | -0.21% | 0.18% |
| 2025-08-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.77% | 0.96% | 0.57% | -0.40% | -0.32% |
| 2025-08-11 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.04% | 0.94% | -0.10% | 0.78% |
| 2025-08-07 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.75% | 1.19% | 0.69% | -0.49% | 0.66% |
| 2025-08-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.58% | 0.05% | -0.53% | -0.29% |
| 2025-08-04 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.74% | 0.57% | -0.17% | 0.53% |
| 2025-07-30 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.52% | 0.05% | -0.48% | -0.18% |
| 2025-07-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.90% | 0.01% | -0.89% | -0.76% |
| 2025-07-23 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.59% | 0.37% | -0.21% | 0.28% |
| 2025-07-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.58% | 0.06% | -0.52% | -0.40% |
| 2025-06-13 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.15% | 1.15% | 0.00% | 1.07% |
| 2025-06-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.33% | 0.00% | -0.33% | -0.23% |
| 2025-05-23 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.20% | 1.09% | -0.10% | 0.83% |
| 2025-05-14 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.94% | 0.62% | -0.32% | 0.29% |
| 2025-05-07 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.95% | 0.89% | -0.05% | 0.73% |
| 2025-05-06 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.73% | 0.04% | -0.69% | -0.67% |
| 2025-04-29 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.07% | 0.68% | 0.36% | -0.33% | -0.19% |
| 2025-04-07 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 2.35% | 2.28% | -0.07% | 2.20% |
| 2025-02-25 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.49% | 0.48% | -0.01% | 0.04% |
| 2025-02-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.53% | 0.02% | -0.51% | -0.48% |
| 2025-02-04 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 1.44% | 1.08% | -0.37% | 0.84% |
| 2025-01-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.16% | 1.07% | -0.08% | 1.02% |
| 2025-01-24 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.28% | 0.70% | -0.58% | -0.40% |
| 2025-01-21 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 1.92% | 0.02% | -1.90% | -1.57% |
| 2025-01-15 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.63% | 0.19% | -0.45% | -0.10% |
| 2025-01-14 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 0.56% | 0.43% | -0.14% | 0.18% |
| 2025-01-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.91% | 0.00% | -0.91% | -0.85% |
| 2024-12-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.77% | 0.41% | -0.35% | -0.16% |
| 2024-12-23 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.94% | 0.55% | -0.38% | 0.04% |
| 2024-12-19 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.56% | 0.54% | -0.03% | 0.36% |
| 2024-12-16 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.73% | 0.11% | -0.61% | -0.42% |
| 2024-12-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.84% | 0.34% | -0.50% | -0.11% |
| 2024-11-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 1.09% | 1.09% | 0.00% | 0.82% |
| 2024-11-27 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.86% | 0.62% | -0.24% | 0.30% |
| 2024-11-26 | Strong Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.90% | 0.00% | -0.90% | -0.62% |
| 2024-11-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.89% | 0.40% | -0.49% | -0.01% |
| 2024-11-04 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 2.06% | 0.00% | -2.05% | -1.34% |
| 2024-10-28 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.47% | 1.00% | -0.48% | 0.48% |
| 2024-10-25 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.88% | 1.50% | 0.09% | -1.41% | -0.84% |
| 2024-10-23 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.93% | 0.93% | -0.00% | 0.24% |
| 2024-10-21 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.20% | 0.09% | -1.11% | -0.87% |
| 2024-10-18 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.29% | 0.90% | -0.39% | 0.80% |
| 2024-10-15 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.81% | 0.10% | -0.71% | -0.48% |
| 2024-10-11 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.43% | 0.17% | -0.26% | -0.04% |
| 2024-10-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.16% | 0.85% | -0.30% | 0.83% |
| 2024-10-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.65% | 0.46% | -0.19% | 0.09% |
| 2024-09-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.62% | 0.51% | -0.11% | 0.44% |
| 2024-09-17 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.35% | 0.10% | -0.25% | -0.04% |
| 2024-09-12 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.86% | 1.96% | 1.49% | -0.47% | 1.02% |
| 2024-09-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.82% | 0.54% | -0.28% | 0.48% |
| 2024-09-02 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.39% | 0.00% | -0.39% | -0.24% |
| 2024-08-28 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.66% | 0.39% | -0.26% | 0.06% |
| 2024-08-26 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.68% | 0.55% | -0.13% | 0.42% |
| 2024-08-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.52% | 0.35% | -0.17% | 0.10% |
| 2024-08-13 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.00% | 0.07% | -0.93% | -0.83% |
| 2024-08-07 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.63% | 0.20% | -0.43% | 0.11% |
| 2024-07-29 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.90% | 0.23% | -0.68% | -0.41% |
| 2024-07-23 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 2.07% | 0.06% | -2.01% | -0.38% |
| 2024-07-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.95% | 0.61% | -0.34% | 0.29% |
| 2024-07-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.30% | 0.18% | -0.11% | -0.06% |
| 2024-07-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.49% | 0.13% | -0.36% | -0.27% |
| 2024-06-24 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.89% | 0.75% | -0.14% | 0.71% |
| 2024-06-21 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.14% | 0.03% | -1.11% | -0.88% |
| 2024-06-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.54% | 0.00% | -0.54% | -0.35% |
| 2024-06-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.63% | 0.42% | -0.21% | -0.15% |
| 2024-06-10 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.79% | 0.40% | -0.39% | -0.36% |
| 2024-06-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 3.97% | 2.45% | -1.52% | 2.01% |
| 2024-06-04 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 8.19% | 0.00% | -8.19% | -5.10% |
| 2024-05-18 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.22% | 0.03% | -0.19% | -0.03% |
| 2024-05-10 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.15% | 0.82% | 0.64% | -0.18% | 0.29% |
| 2024-05-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.08% | 1.69% | 0.37% | -1.32% | -1.15% |
| 2024-05-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.83% | 0.62% | -0.21% | 0.34% |
| 2024-04-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.95% | 0.46% | -0.49% | -0.41% |
| 2024-04-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.95% | 0.80% | -0.15% | 0.70% |
| 2024-04-26 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 1.04% | 0.00% | -1.04% | -0.75% |
| 2024-04-23 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.44% | 0.00% | -0.43% | -0.38% |
| 2024-04-16 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.61% | 0.40% | -0.21% | 0.24% |
| 2024-04-03 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.78% | 0.60% | -0.18% | 0.27% |
| 2024-03-20 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.01% | 0.40% | -0.61% | 0.05% |
| 2024-03-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.84% | 0.15% | -0.70% | -0.62% |
| 2024-03-14 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 1.31% | 1.01% | -0.30% | 0.78% |
| 2024-03-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 2.41% | 0.06% | -2.35% | -2.01% |
| 2024-02-29 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 0.91% | 0.57% | -0.34% | 0.49% |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.97% | 0.73% | 0.22% | -0.51% | 0.09% |
| 2024-02-13 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.03% | 0.47% | -0.56% | 0.29% |
| 2024-02-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.18% | 0.14% | -1.04% | -0.86% |
| 2024-02-09 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.0% | 0.80% | 0.36% | -0.45% | 0.27% |
| 2024-02-07 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.88% | 0.04% | -0.84% | -0.43% |
| 2024-02-06 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.98% | 0.58% | -0.40% | 0.52% |
| 2024-02-01 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 0.80% | 0.24% | -0.56% | -0.41% |
| 2024-01-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.36% | 1.18% | -0.18% | 1.03% |
| 2024-01-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.99% | 0.02% | -0.97% | -0.39% |
| 2024-01-18 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.95% | 1.19% | 0.58% | -0.60% | 0.29% |
| 2024-01-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.70% | 0.20% | -0.50% | -0.22% |
| 2023-12-20 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 2.35% | 0.23% | -2.12% | -2.05% |
| 2023-12-01 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.53% | 0.48% | -0.05% | 0.31% |
| 2023-11-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.41% | 0.04% | -0.37% | -0.24% |
| 2023-11-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.19% | 0.00% | -0.19% | -0.13% |
| 2023-10-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.56% | 0.25% | -0.30% | -0.21% |
| 2023-09-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 0.89% | 0.74% | -0.15% | 0.29% |
| 2023-09-28 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.39% | 0.02% | -1.36% | -1.06% |
| 2023-09-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.31% | 0.08% | -0.23% | -0.05% |
| 2023-09-18 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.38% | 0.20% | -0.19% | -0.16% |
| 2023-09-15 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.46% | 0.33% | -0.13% | 0.06% |
| 2023-09-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.61% | 0.20% | -0.41% | -0.13% |
| 2023-09-12 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.97% | 0.00% | -0.97% | -0.62% |
| 2023-08-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.35% | 0.02% | -0.33% | -0.11% |
| 2023-08-28 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.60% | 0.35% | -0.25% | 0.02% |
| 2023-08-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 1.10% | 0.25% | -0.85% | -0.79% |
| 2023-08-23 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.54% | 0.17% | -0.37% | 0.01% |
| 2023-08-22 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.32% | 0.14% | -0.18% | -0.14% |
| 2023-08-01 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.46% | 0.06% | -0.40% | -0.24% |
| 2023-07-31 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.89% | 0.54% | -0.35% | 0.39% |
| 2023-07-27 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 1.33% | 0.08% | -1.25% | -0.76% |
| 2023-07-19 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.63% | 0.25% | -0.38% | 0.22% |
| 2023-07-18 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.65% | 0.16% | -0.49% | -0.18% |
| 2023-07-12 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.75% | 0.05% | -0.70% | -0.58% |
| 2023-06-26 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.40% | 0.21% | -0.19% | 0.07% |
| 2023-06-22 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.67% | 0.17% | -0.49% | -0.39% |
| 2023-06-20 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.94% | 0.46% | -0.49% | 0.43% |
| 2023-06-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.85% | 0.03% | -0.82% | -0.63% |
| 2023-06-16 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 0.81% | 0.75% | -0.06% | 0.54% |
| 2023-06-12 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.35% | 0.16% | -0.18% | 0.11% |
| 2023-06-08 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.86% | 0.28% | -0.58% | -0.42% |
| 2023-06-05 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.30% | 0.15% | -0.15% | -0.07% |
| 2023-05-31 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.64% | 0.04% | -0.59% | -0.39% |
| 2023-05-30 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.45% | 0.30% | -0.16% | 0.18% |
| 2023-05-29 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.31% | 0.11% | -0.20% | -0.10% |
| 2023-05-25 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.73% | 0.37% | -0.36% | 0.37% |
| 2023-05-16 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.91% | 0.00% | -0.91% | -0.84% |
| 2023-05-11 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.47% | 0.00% | -0.47% | -0.29% |
| 2023-05-09 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.62% | 0.22% | -0.40% | -0.25% |
| 2023-05-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.02% | 0.92% | -0.10% | 0.82% |
| 2023-04-26 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.65% | 0.33% | -0.31% | 0.29% |
| 2023-04-24 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.80% | 0.26% | -0.54% | 0.23% |
| 2023-04-21 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.61% | 0.13% | -0.49% | -0.12% |
| 2023-03-28 | Strong Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.86% | 0.17% | -0.69% | -0.44% |
| 2023-03-22 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.57% | 0.17% | -0.40% | -0.20% |
| 2023-03-21 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.65% | 0.39% | -0.26% | 0.27% |
| 2023-03-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.38% | 0.00% | -1.38% | -0.37% |
| 2023-03-03 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 1.23% | 1.11% | -0.12% | 0.81% |
| 2023-03-02 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.79% | 0.13% | -0.66% | -0.59% |
| 2023-03-01 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.66% | 0.62% | -0.04% | 0.56% |
| 2023-02-28 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.06% | 0.33% | -0.73% | -0.38% |
| 2023-02-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 1.01% | 0.05% | -0.96% | -0.72% |
| 2023-02-22 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.36% | 0.09% | -1.27% | -1.14% |
| 2023-02-14 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.86% | 0.64% | -0.22% | 0.46% |
| 2023-02-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.67% | 0.00% | -0.67% | -0.32% |
| 2023-02-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.06% | 1.17% | 0.78% | -0.39% | 0.54% |
| 2023-01-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.67% | 0.09% | -0.58% | -0.46% |
| 2023-01-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.50% | 0.19% | -0.31% | -0.17% |
| 2023-01-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.02% | 0.82% | -0.19% | 0.75% |
| 2023-01-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.08% | 0.09% | -0.99% | -0.78% |
| 2023-01-10 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.47% | 0.01% | -1.46% | -1.08% |
| 2023-01-09 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.14% | 1.05% | -0.09% | 0.76% |
| 2023-01-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.94% | 1.39% | 0.21% | -1.18% | -0.79% |
| 2023-01-04 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.20% | 0.06% | -1.14% | -1.06% |
| 2023-01-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.70% | 0.46% | -0.24% | 0.42% |
| 2022-12-26 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.73% | 1.42% | -0.31% | 1.01% |
| 2022-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 1.48% | 0.38% | -1.10% | -0.85% |
| 2022-12-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.34% | 0.13% | -0.20% | -0.15% |
| 2022-12-12 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.95% | 0.65% | -0.30% | 0.50% |
| 2022-12-09 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.35% | 0.00% | -1.35% | -0.91% |
| 2022-12-08 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.47% | 0.29% | -0.18% | 0.23% |
| 2022-12-01 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 0.57% | 0.08% | -0.50% | -0.38% |
| 2022-11-28 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.00% | 1.00% | 0.00% | 0.67% |
| 2022-11-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.48% | 0.03% | -0.45% | -0.16% |
| 2022-11-22 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.65% | 0.43% | -0.22% | 0.40% |
| 2022-11-15 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.79% | 0.35% | -0.44% | 0.32% |
| 2022-11-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.47% | 0.12% | -0.35% | -0.31% |
| 2022-11-03 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.79% | 0.76% | -0.02% | 0.44% |
| 2022-10-25 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.95% | 0.00% | -0.95% | -0.93% |
| 2022-10-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.27% | 0.90% | 0.14% | -0.76% | -0.41% |
| 2022-10-12 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.06% | 0.68% | -0.38% | 0.61% |
| 2022-10-04 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.92% | 0.80% | -0.12% | 0.76% |
| 2022-10-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.51% | 0.06% | -1.44% | -1.32% |
| 2022-09-22 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 1.08% | 0.64% | -0.44% | 0.15% |
| 2022-09-21 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.99% | 0.41% | -0.58% | -0.28% |
| 2022-09-12 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.50% | 0.50% | 0.00% | 0.23% |
| 2022-09-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.15% | 0.78% | 0.01% | -0.77% | -0.52% |
| 2022-09-08 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 0.64% | 0.33% | -0.31% | 0.29% |
| 2022-09-07 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.75% | 0.75% | 0.00% | 0.63% |
| 2022-09-06 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.99% | 0.39% | -0.61% | -0.25% |
| 2022-09-05 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.78% | 0.78% | 0.00% | 0.61% |
| 2022-08-03 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.04% | 0.33% | -0.71% | 0.25% |
| 2022-08-02 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.00% | 0.46% | -0.54% | -0.09% |
| 2022-07-27 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.29% | 1.08% | -0.22% | 1.02% |
| 2022-07-25 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.84% | 0.25% | -0.59% | -0.32% |
| 2022-06-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.10% | 0.08% | -1.02% | -0.93% |
| 2022-06-10 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.21% | 0.93% | 0.25% | -0.68% | -0.57% |
| 2022-06-06 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.00% | 0.48% | -0.51% | 0.20% |
| 2022-05-26 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.59% | 1.86% | 0.61% | -1.25% | 0.60% |
| 2022-05-23 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.39% | 0.76% | -0.64% | -0.61% |
| 2022-05-18 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.15% | 0.50% | -0.65% | -0.38% |
| 2022-05-09 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.61% | 1.08% | -0.52% | 0.50% |
| 2022-04-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 1.87% | 0.28% | -1.59% | -1.26% |
| 2022-04-28 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.3% | 1.46% | 0.77% | -0.69% | 0.24% |
| 2022-04-05 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.95% | 0.08% | -0.87% | -0.83% |
| 2022-03-16 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.87% | 0.66% | -0.21% | 0.53% |
| 2022-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.73% | 1.84% | 0.00% | -1.84% | -1.14% |
| 2022-03-08 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 2.26% | 1.78% | -0.48% | 1.69% |
| 2022-02-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.33% | 0.47% | -0.86% | -0.66% |
| 2022-02-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.17% | 1.47% | 0.04% | -1.43% | -1.39% |
| 2022-01-31 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.84% | 0.63% | -0.21% | 0.22% |
| 2022-01-07 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.13% | 1.12% | 0.60% | -0.52% | 0.12% |
| 2021-12-30 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.02% | 0.67% | 0.36% | -0.31% | 0.16% |
| 2021-12-17 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.0% | 1.89% | 0.10% | -1.79% | -1.63% |
| 2021-12-14 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.87% | 0.54% | -0.33% | 0.21% |
| 2021-12-07 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.54% | 1.22% | -0.32% | 0.80% |
| 2021-11-30 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 2.29% | 1.60% | -0.69% | -0.45% |
| 2021-11-26 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 2.06% | 0.04% | -2.03% | -1.92% |
| 2021-11-24 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.39% | 0.29% | -1.11% | -1.10% |
| 2021-11-15 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.76% | 0.38% | -0.38% | -0.27% |
| 2021-11-10 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.81% | 0.49% | -0.32% | 0.20% |
| 2021-11-02 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.90% | 0.22% | -0.68% | -0.45% |
| 2021-10-01 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.59% | 0.14% | -0.45% | -0.03% |
| 2021-09-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.71% | 0.28% | -0.43% | -0.31% |
| 2021-09-21 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.44% | 0.73% | -0.71% | 0.65% |
| 2021-09-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 1.06% | 0.88% | -0.19% | 0.81% |
| 2021-08-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.56% | 0.35% | -0.22% | -0.11% |
| 2021-07-30 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.74% | 0.39% | -0.35% | -0.17% |
| 2021-07-26 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.59% | 0.28% | -0.31% | -0.18% |
| 2021-07-19 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.82% | 0.52% | -0.30% | 0.02% |
| 2021-07-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.62% | 0.27% | -0.35% | 0.06% |
| 2021-06-17 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.94% | 0.97% | 0.77% | -0.19% | 0.21% |
| 2021-06-07 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.59% | 0.30% | -0.29% | 0.14% |
| 2021-05-24 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 0.72% | 0.29% | -0.43% | -0.18% |
| 2021-05-03 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.77% | 1.33% | -0.44% | 1.13% |
| 2021-04-01 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.3% | 1.28% | 0.57% | -0.71% | 0.46% |
| 2021-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.42% | 0.76% | 0.10% | -0.66% | -0.22% |
| 2021-03-01 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.14% | 0.71% | -0.43% | 0.56% |
| 2021-02-16 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | nan | - | 1.22% | 0.39% | -0.83% | -0.35% |
| 2021-01-29 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.53% | 2.64% | 0.14% | -2.50% | -2.05% |
| 2020-12-22 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 2.22% | 0.88% | -1.34% | 0.65% |
| 2020-11-27 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.26% | 0.88% | 0.14% | -0.74% | -0.53% |
| 2020-11-26 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.46% | 1.75% | 0.86% | -0.90% | 0.84% |
| 2020-11-20 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.23% | 1.25% | 0.61% | -0.65% | 0.25% |
| 2020-10-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.47% | 1.18% | 0.95% | -0.23% | 0.32% |
| 2020-09-15 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 0.81% | 0.42% | -0.39% | 0.39% |
| 2020-09-10 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.4% | 1.17% | 0.88% | -0.30% | 0.80% |
| 2020-09-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | nan | - | 1.62% | 0.77% | -0.85% | 0.26% |

### Against then Recovered (first half against view, second half recovered)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-27 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.85% | 0.08% | -0.77% | -0.77% |
| 2026-08-19 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.61% | 0.09% | -0.52% | -0.31% |
| 2026-08-12 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.85% | 0.00% | -0.84% | -0.15% |
| 2026-08-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.44% | 0.37% | -0.07% | 0.13% |
| 2026-08-05 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.73% | 0.03% | -0.69% | -0.18% |
| 2026-07-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.64% | 0.39% | -0.26% | 0.19% |
| 2026-07-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.50% | 0.35% | -0.15% | 0.31% |
| 2026-07-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.85% | 0.07% | -0.78% | -0.66% |
| 2026-07-21 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.82% | 0.52% | 0.19% | -0.33% | -0.09% |
| 2026-07-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.54% | 0.31% | -0.22% | 0.20% |
| 2026-07-15 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.87% | 0.56% | -0.31% | -0.05% |
| 2026-07-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.08% | 0.92% | -0.16% | 0.71% |
| 2026-07-10 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.45% | 0.43% | -0.02% | 0.36% |
| 2026-06-22 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.39% | 0.25% | -0.14% | -0.08% |
| 2026-06-09 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 0.75% | 0.09% | -0.66% | -0.01% |
| 2026-05-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.55% | 0.48% | -0.07% | 0.46% |
| 2026-05-12 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.72% | 0.15% | -1.58% | -1.23% |
| 2026-05-08 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.52% | 0.08% | -0.44% | -0.22% |
| 2026-04-24 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.63% | 0.44% | -1.19% | -0.82% |
| 2026-04-23 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.15% | 0.72% | 0.45% | -0.28% | -0.19% |
| 2026-04-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.19% | 1.49% | 1.35% | -0.14% | 0.97% |
| 2026-03-18 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.03% | 0.97% | -0.06% | 0.56% |
| 2026-03-12 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.33% | 1.17% | 0.67% | -0.50% | -0.15% |
| 2026-03-10 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.47% | 0.92% | 0.09% | -0.83% | 0.02% |
| 2026-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 1.23% | 0.00% | -1.23% | -0.71% |
| 2026-02-23 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.63% | 0.36% | -0.27% | 0.10% |
| 2026-02-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.76% | 0.49% | -0.26% | 0.30% |
| 2026-02-13 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.73% | 0.23% | -0.50% | -0.43% |
| 2026-02-04 | Strong Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.99% | 0.56% | -0.43% | 0.24% |
| 2026-02-01 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 3.43% | 0.42% | -3.01% | -2.23% |
| 2026-01-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.23% | 0.39% | -0.84% | -0.53% |
| 2025-12-31 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.84% | 0.84% | -0.01% | 0.66% |
| 2025-12-22 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.51% | 0.48% | -0.03% | 0.41% |
| 2025-12-17 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.61% | 0.10% | -0.51% | -0.31% |
| 2025-12-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.46% | 0.33% | -0.13% | 0.28% |
| 2025-12-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.76% | 0.22% | -0.54% | -0.10% |
| 2025-12-01 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.77% | 0.00% | -0.77% | -0.57% |
| 2025-11-28 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.41% | 0.17% | -0.25% | -0.13% |
| 2025-11-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.44% | 1.44% | 0.00% | 1.40% |
| 2025-11-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 0.67% | 0.13% | -0.54% | -0.53% |
| 2025-11-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.88% | 0.08% | -0.81% | -0.69% |
| 2025-11-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.70% | 0.44% | -0.26% | 0.25% |
| 2025-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.94% | 0.35% | -0.59% | -0.51% |
| 2025-10-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.98% | 0.91% | -0.07% | 0.67% |
| 2025-10-14 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.99% | 0.13% | -0.86% | -0.61% |
| 2025-10-10 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.69% | 0.65% | -0.04% | 0.44% |
| 2025-09-26 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.96% | 0.20% | -0.76% | -0.59% |
| 2025-09-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.86% | 0.23% | -0.62% | -0.52% |
| 2025-09-23 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.70% | 0.21% | -0.49% | -0.09% |
| 2025-09-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.28% | 0.28% | -0.00% | 0.21% |
| 2025-09-05 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.85% | 0.05% | -0.79% | -0.30% |
| 2025-08-14 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.76% | 0.31% | 0.27% | -0.04% | 0.04% |
| 2025-08-06 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.54% | 0.12% | -0.41% | -0.29% |
| 2025-07-28 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.98% | 0.43% | -0.55% | -0.44% |
| 2025-07-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.82% | 0.00% | -0.82% | -0.71% |
| 2025-07-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.59% | 0.01% | -0.59% | -0.25% |
| 2025-07-03 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.80% | 0.32% | -0.47% | -0.42% |
| 2025-07-02 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.90% | 0.08% | -0.82% | -0.57% |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.21% | 1.17% | -0.04% | 1.03% |
| 2025-06-24 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 1.26% | 0.55% | -0.72% | -0.43% |
| 2025-06-05 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.99% | 1.16% | 0.85% | -0.32% | 0.28% |
| 2025-05-28 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.51% | 0.13% | -0.38% | -0.30% |
| 2025-05-26 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.72% | 0.64% | -0.08% | 0.31% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 2.52% | 1.71% | -0.81% | 1.38% |
| 2025-04-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 0.81% | 0.22% | -0.59% | -0.39% |
| 2025-04-03 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.69% | 0.67% | -0.02% | 0.39% |
| 2025-03-26 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.20% | 0.15% | -1.05% | -1.00% |
| 2025-03-24 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.17% | 0.82% | -0.35% | 0.68% |
| 2025-03-19 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.58% | 0.29% | -0.29% | 0.16% |
| 2025-03-06 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.86% | 1.38% | 0.36% | -1.03% | 0.24% |
| 2025-02-07 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.06% | 0.19% | -0.87% | -0.37% |
| 2025-01-30 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 0.79% | 0.66% | -0.13% | 0.55% |
| 2025-01-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.90% | 0.68% | -0.22% | 0.65% |
| 2025-01-23 | Strong Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 0.78% | 0.62% | -0.16% | 0.38% |
| 2025-01-13 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.27% | 0.63% | -0.64% | -0.46% |
| 2025-01-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.79% | 0.06% | -0.73% | -0.50% |
| 2025-01-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 2.24% | 0.18% | -2.05% | -1.73% |
| 2025-01-02 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 2.00% | 1.87% | -0.13% | 1.62% |
| 2024-12-18 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.01% | 0.40% | -0.61% | -0.34% |
| 2024-12-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.30% | 0.16% | -1.14% | -1.08% |
| 2024-12-10 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.68% | 0.10% | -0.58% | -0.13% |
| 2024-12-02 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.21% | 0.67% | -0.55% | 0.56% |
| 2024-11-13 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.53% | 0.21% | -1.31% | -0.92% |
| 2024-11-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 0.87% | 0.28% | -0.58% | -0.40% |
| 2024-11-07 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 1.32% | 0.06% | -1.27% | -1.20% |
| 2024-11-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.37% | 0.94% | -0.43% | 0.76% |
| 2024-11-01 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.98% | 0.36% | 0.27% | -0.09% | -0.01% |
| 2024-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.82% | 0.09% | -0.73% | -0.46% |
| 2024-10-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.41% | 0.64% | -0.77% | 0.51% |
| 2024-10-24 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.92% | 0.57% | 0.28% | -0.29% | 0.01% |
| 2024-10-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.76% | 0.34% | -1.42% | -1.28% |
| 2024-10-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.20% | 0.01% | -1.19% | -1.11% |
| 2024-10-16 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.74% | 0.34% | -0.40% | -0.19% |
| 2024-09-23 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.42% | 0.32% | -0.10% | 0.22% |
| 2024-09-16 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.43% | 0.15% | -0.28% | -0.12% |
| 2024-09-10 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.93% | 0.52% | -0.41% | 0.21% |
| 2024-09-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.34% | 0.03% | -0.31% | -0.18% |
| 2024-08-21 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.54% | 0.44% | -0.11% | 0.41% |
| 2024-08-14 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.02% | 0.40% | 0.05% | -0.35% | -0.16% |
| 2024-08-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.07% | 0.63% | -0.44% | 0.12% |
| 2024-08-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.05% | 0.45% | 0.13% | -0.31% | -0.09% |
| 2024-08-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.75% | 0.80% | -0.95% | -0.65% |
| 2024-08-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.88% | 0.19% | -1.68% | -1.03% |
| 2024-07-26 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.79% | 1.84% | 1.79% | -0.05% | 1.75% |
| 2024-07-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.81% | 0.24% | -0.56% | -0.01% |
| 2024-07-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 1.07% | 0.84% | -0.23% | 0.51% |
| 2024-07-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.86% | 0.03% | -0.83% | -0.24% |
| 2024-06-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.81% | 0.75% | -0.06% | 0.61% |
| 2024-06-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 2.33% | 2.18% | -0.14% | 1.96% |
| 2024-06-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.19% | 1.17% | 0.49% | -0.68% | 0.22% |
| 2024-05-30 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 1.28% | 0.39% | -0.89% | -0.27% |
| 2024-05-24 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.35% | 0.52% | 0.42% | -0.10% | 0.09% |
| 2024-05-23 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.35% | 1.84% | 1.68% | -0.16% | 1.49% |
| 2024-05-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.85% | 0.65% | -0.20% | 0.44% |
| 2024-05-06 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.79% | 0.12% | -0.67% | -0.46% |
| 2024-04-25 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 1.44% | 1.38% | -0.05% | 1.09% |
| 2024-04-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.41% | 0.24% | -0.17% | -0.04% |
| 2024-04-05 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.71% | 0.49% | 0.23% | -0.26% | 0.16% |
| 2024-03-01 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 1.39% | 1.38% | -0.00% | 1.26% |
| 2024-02-26 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.57% | 0.15% | -0.42% | -0.23% |
| 2024-02-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.58% | 1.36% | -0.22% | 1.25% |
| 2024-01-15 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.69% | 0.28% | -0.41% | 0.26% |
| 2024-01-09 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.95% | 0.33% | -0.63% | -0.47% |
| 2024-01-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.25% | 0.08% | -1.17% | -1.09% |
| 2024-01-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.84% | 0.55% | 0.20% | -0.35% | 0.02% |
| 2024-01-04 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.89% | 0.56% | 0.37% | -0.19% | 0.30% |
| 2024-01-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.82% | 0.07% | -0.74% | -0.63% |
| 2023-12-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.87% | 0.74% | 0.44% | -0.30% | 0.17% |
| 2023-12-19 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.78% | 0.13% | -0.65% | -0.15% |
| 2023-12-12 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.81% | 0.09% | -0.72% | -0.56% |
| 2023-12-08 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.8% | 0.69% | 0.34% | -0.34% | 0.18% |
| 2023-12-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.52% | 0.05% | -0.47% | -0.07% |
| 2023-12-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.73% | 0.27% | -0.47% | 0.23% |
| 2023-11-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.8% | 0.71% | 0.25% | -0.46% | 0.09% |
| 2023-11-22 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.62% | 0.21% | -0.41% | 0.13% |
| 2023-11-20 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.44% | 0.13% | -0.31% | -0.19% |
| 2023-11-09 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.44% | 0.03% | -0.41% | -0.27% |
| 2023-11-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.49% | 0.10% | -0.39% | 0.07% |
| 2023-11-01 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.64% | 0.17% | -0.47% | -0.39% |
| 2023-10-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.15% | 0.55% | -0.60% | 0.50% |
| 2023-10-23 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.53% | 0.18% | -1.35% | -1.25% |
| 2023-10-16 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.45% | 0.22% | -0.23% | -0.03% |
| 2023-10-11 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.42% | 0.37% | -0.05% | 0.21% |
| 2023-09-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.67% | 0.28% | -0.39% | -0.02% |
| 2023-09-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.71% | 0.27% | -0.44% | -0.31% |
| 2023-09-11 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.68% | 0.59% | -0.08% | 0.55% |
| 2023-09-08 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.70% | 0.47% | -0.23% | 0.23% |
| 2023-09-04 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.58% | 0.10% | -0.47% | 0.05% |
| 2023-08-25 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.74% | 0.56% | 0.22% | -0.35% | -0.28% |
| 2023-08-18 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.77% | 0.62% | 0.37% | -0.25% | -0.10% |
| 2023-08-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.72% | 0.00% | -0.72% | -0.66% |
| 2023-08-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 1.23% | 0.38% | -0.85% | -0.36% |
| 2023-07-25 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.57% | 0.00% | -0.57% | -0.26% |
| 2023-07-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.63% | 0.17% | -0.46% | -0.42% |
| 2023-07-20 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.18% | 0.81% | -0.37% | 0.70% |
| 2023-07-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.83% | 0.52% | -0.31% | 0.48% |
| 2023-07-13 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.93% | 0.37% | -0.56% | -0.27% |
| 2023-06-28 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.79% | 0.54% | -0.25% | 0.44% |
| 2023-06-27 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.61% | 0.43% | -0.18% | 0.37% |
| 2023-06-23 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.55% | 0.05% | -0.50% | -0.39% |
| 2023-06-21 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.43% | 0.14% | -0.29% | 0.07% |
| 2023-06-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.42% | 0.13% | -0.29% | 0.03% |
| 2023-06-13 | Strong Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.51% | 0.51% | 0.00% | 0.47% |
| 2023-06-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 0.65% | 0.11% | -0.54% | -0.47% |
| 2023-06-06 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.48% | 0.11% | -0.37% | 0.09% |
| 2023-06-02 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.51% | 0.12% | -0.39% | -0.13% |
| 2023-06-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.62% | 0.00% | -0.61% | -0.50% |
| 2023-05-26 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.79% | 0.95% | 0.76% | -0.19% | 0.67% |
| 2023-05-19 | Strong Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.81% | 0.86% | 0.17% | -0.69% | 0.11% |
| 2023-05-18 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 1.04% | 0.05% | -1.00% | -0.84% |
| 2023-05-17 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.05% | 0.04% | -1.01% | -0.56% |
| 2023-05-15 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.91% | 0.65% | -0.26% | 0.25% |
| 2023-05-10 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.62% | 0.07% | -0.55% | -0.01% |
| 2023-04-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.75% | 0.66% | -0.08% | 0.62% |
| 2023-04-25 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Reversed by Close | nan | - | 0.51% | 0.26% | -0.25% | 0.00% |
| 2023-04-19 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.48% | 0.07% | -0.42% | -0.24% |
| 2023-04-12 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.60% | 0.36% | -0.24% | 0.33% |
| 2023-03-27 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.01% | 0.63% | -0.38% | -0.12% |
| 2023-03-13 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 2.38% | 0.62% | -1.76% | -1.36% |
| 2023-03-10 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.8% | 0.68% | 0.00% | -0.68% | -0.14% |
| 2023-03-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.67% | 0.67% | 0.00% | 0.22% |
| 2023-02-23 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.93% | 0.25% | -0.67% | -0.29% |
| 2023-02-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.03% | 0.21% | -0.82% | -0.66% |
| 2023-02-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 0.82% | 0.33% | -0.49% | -0.18% |
| 2023-02-15 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.01% | 0.77% | -0.24% | 0.71% |
| 2023-02-13 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.89% | 0.12% | -0.78% | -0.53% |
| 2023-02-07 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.89% | 0.12% | -0.77% | -0.39% |
| 2023-01-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 1.36% | 0.00% | -1.36% | -1.01% |
| 2023-01-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 0.70% | 0.16% | -0.54% | -0.49% |
| 2023-01-18 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.83% | 0.60% | -0.23% | 0.50% |
| 2023-01-11 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.84% | 0.29% | -0.55% | -0.20% |
| 2023-01-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.96% | 1.25% | 0.09% | -1.16% | -0.56% |
| 2022-12-27 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.00% | 0.33% | -0.68% | 0.26% |
| 2022-12-22 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 1.36% | 0.15% | -1.20% | -0.95% |
| 2022-12-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.10% | 0.35% | -0.75% | 0.25% |
| 2022-12-16 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.86% | 1.01% | 0.66% | -0.35% | -0.27% |
| 2022-12-15 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 1.41% | 0.20% | -1.21% | -1.15% |
| 2022-12-13 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.68% | 0.50% | -0.18% | 0.39% |
| 2022-12-07 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.75% | 0.16% | -0.59% | -0.47% |
| 2022-12-06 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.40% | 0.29% | -0.12% | 0.25% |
| 2022-12-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.70% | 0.02% | -0.68% | -0.14% |
| 2022-12-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.74% | 0.14% | -0.60% | -0.25% |
| 2022-11-18 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 1.00% | 0.06% | -0.94% | -0.43% |
| 2022-11-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.53% | 0.24% | -0.29% | 0.02% |
| 2022-11-01 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.63% | 0.25% | -0.38% | 0.07% |
| 2022-10-21 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 0.84% | 0.27% | -0.58% | -0.22% |
| 2022-10-18 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.51% | 0.51% | 0.00% | 0.30% |
| 2022-10-14 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.28% | 1.02% | 0.15% | -0.88% | -0.70% |
| 2022-10-11 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.77% | 0.00% | -1.77% | -1.69% |
| 2022-09-26 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.26% | 0.23% | -1.03% | -0.75% |
| 2022-09-20 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.88% | 0.83% | -0.05% | 0.12% |
| 2022-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.16% | 1.78% | 0.11% | -1.68% | -1.39% |
| 2022-09-15 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.29% | 0.27% | -1.02% | -0.96% |
| 2022-09-14 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.80% | 1.80% | 0.00% | 1.29% |
| 2022-09-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.40% | 0.24% | -0.16% | 0.12% |
| 2022-08-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.24% | 0.03% | -1.21% | -1.07% |
| 2022-08-19 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 1.55% | 0.13% | -1.42% | -1.33% |
| 2022-07-28 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.14% | 1.16% | 1.01% | -0.16% | 0.88% |
| 2022-07-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.06% | 1.06% | 0.00% | 0.88% |
| 2022-07-15 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.16% | 0.87% | 0.35% | -0.52% | 0.26% |
| 2022-07-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.32% | 0.32% | -1.00% | -0.44% |
| 2022-07-13 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.17% | 0.07% | -1.10% | -0.95% |
| 2022-07-07 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.28% | 0.64% | 0.23% | -0.41% | 0.14% |
| 2022-07-01 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.38% | 1.78% | 0.56% | -1.22% | 0.38% |
| 2022-06-15 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.66% | 0.34% | -0.32% | -0.29% |
| 2022-06-13 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.24% | 0.02% | -1.22% | -0.48% |
| 2022-06-08 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.33% | 0.23% | -1.10% | -0.85% |
| 2022-06-01 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.26% | 0.33% | -0.94% | -0.32% |
| 2022-05-19 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.4% | 1.30% | 0.41% | -0.89% | -0.56% |
| 2022-05-06 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.28% | 0.86% | 0.42% | -0.45% | 0.14% |
| 2022-04-25 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.97% | 0.26% | -0.71% | -0.15% |
| 2022-04-12 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.86% | 0.06% | -0.81% | -0.37% |
| 2022-04-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.67% | 0.32% | -0.35% | -0.24% |
| 2022-04-04 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.63% | 1.56% | -0.07% | 1.27% |
| 2022-03-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 0.98% | 0.82% | -0.16% | 0.56% |
| 2022-02-28 | Strong Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 2.78% | 2.02% | -0.76% | 1.87% |
| 2022-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.55% | 3.01% | 0.93% | -2.08% | -2.00% |
| 2022-02-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.60% | 0.04% | -1.56% | -1.50% |
| 2022-02-10 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.17% | 1.21% | 0.49% | -0.72% | 0.19% |
| 2022-02-08 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.51% | 0.14% | -1.37% | -0.23% |
| 2022-02-04 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.21% | 0.87% | 0.15% | -0.72% | -0.50% |
| 2022-01-20 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.12% | 1.59% | 0.07% | -1.52% | -0.77% |
| 2022-01-19 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.35% | 0.00% | -1.35% | -1.04% |
| 2021-12-31 | Strong Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.04% | 0.90% | 0.90% | 0.00% | 0.69% |
| 2021-12-28 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.51% | 0.42% | -0.10% | 0.32% |
| 2021-12-22 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.89% | 0.62% | -0.27% | 0.61% |
| 2021-12-20 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 2.49% | 0.03% | -2.46% | -1.26% |
| 2021-12-08 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.99% | 0.98% | -0.02% | 0.88% |
| 2021-12-06 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.84% | 0.01% | -1.83% | -1.74% |
| 2021-12-02 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.23% | 1.51% | 1.36% | -0.14% | 1.27% |
| 2021-11-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 2.21% | 0.61% | -1.59% | -0.09% |
| 2021-11-17 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.79% | 0.46% | -0.33% | -0.29% |
| 2021-11-11 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.03% | 0.93% | 0.00% | -0.93% | -0.46% |
| 2021-11-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.28% | 0.22% | -1.06% | -0.64% |
| 2021-10-28 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 2.13% | 0.00% | -2.13% | -1.79% |
| 2021-10-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.46% | 0.04% | -1.42% | -0.51% |
| 2021-10-21 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.82% | 0.00% | -1.82% | -0.89% |
| 2021-10-12 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.78% | 0.50% | -0.28% | 0.50% |
| 2021-10-08 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.02% | 0.56% | 0.31% | -0.26% | 0.12% |
| 2021-10-07 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.09% | 0.51% | 0.26% | -0.25% | -0.08% |
| 2021-09-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.75% | 0.60% | -0.16% | 0.50% |
| 2021-09-03 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.9% | 0.74% | 0.45% | -0.29% | 0.34% |
| 2021-08-16 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.65% | 0.42% | -0.22% | 0.17% |
| 2021-08-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.97% | 0.96% | -0.00% | 0.82% |
| 2021-08-04 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.63% | 0.59% | -0.04% | 0.36% |
| 2021-08-03 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.45% | 1.22% | -0.22% | 1.08% |
| 2021-07-28 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.57% | 0.00% | -1.57% | -0.30% |
| 2021-07-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.93% | 0.14% | -0.80% | -0.51% |
| 2021-07-14 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.71% | 0.43% | -0.28% | 0.23% |
| 2021-06-30 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 0.82% | 0.39% | -0.42% | -0.29% |
| 2021-06-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.95% | 0.62% | 0.19% | -0.42% | 0.05% |
| 2021-05-18 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.62% | 0.46% | -0.15% | 0.28% |
| 2021-04-30 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.47% | 1.72% | 0.73% | -0.98% | -0.88% |
| 2021-03-26 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.43% | 1.08% | 0.46% | -0.63% | 0.09% |
| 2021-03-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.41% | 2.10% | 0.00% | -2.10% | -1.54% |
| 2021-03-05 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 1.52% | 0.75% | -0.77% | -0.10% |
| 2021-03-02 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.33% | 0.63% | -0.70% | 0.51% |
| 2021-02-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.52% | 0.68% | 0.62% | -0.06% | 0.16% |
| 2021-01-25 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.87% | 0.08% | -1.78% | -1.59% |
| 2021-01-20 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.02% | 0.88% | -0.14% | 0.58% |
| 2021-01-18 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | nan | - | 1.59% | 0.01% | -1.58% | -1.54% |
| 2021-01-11 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.78% | 0.15% | -0.62% | 0.06% |
| 2020-12-04 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.2% | 0.94% | 0.76% | -0.19% | 0.71% |
| 2020-11-03 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 0.90% | 0.86% | -0.04% | 0.62% |
| 2020-09-28 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.24% | 0.88% | -0.36% | 0.88% |
| 2020-09-25 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.48% | 1.98% | 1.48% | -0.50% | 1.15% |
| 2020-09-11 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.34% | 0.63% | 0.39% | -0.24% | 0.06% |
| 2020-08-18 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | nan | - | 1.29% | 1.26% | -0.04% | 1.17% |

### Exceeded Half VIX Range + Worked and Remained (88 days — strongest signal)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-27 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.85% | 0.08% | -0.77% | -0.77% |
| 2026-07-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.64% | 0.39% | -0.26% | 0.19% |
| 2026-06-09 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 0.75% | 0.09% | -0.66% | -0.01% |
| 2026-05-12 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.72% | 0.15% | -1.58% | -1.23% |
| 2026-04-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.19% | 1.49% | 1.35% | -0.14% | 0.97% |
| 2026-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 1.23% | 0.00% | -1.23% | -0.71% |
| 2026-02-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.76% | 0.49% | -0.26% | 0.30% |
| 2025-12-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.76% | 0.22% | -0.54% | -0.10% |
| 2025-11-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 0.67% | 0.13% | -0.54% | -0.53% |
| 2025-11-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.70% | 0.44% | -0.26% | 0.25% |
| 2025-10-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.98% | 0.91% | -0.07% | 0.67% |
| 2025-10-14 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.99% | 0.13% | -0.86% | -0.61% |
| 2025-09-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.86% | 0.23% | -0.62% | -0.52% |
| 2025-09-23 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.70% | 0.21% | -0.49% | -0.09% |
| 2025-07-03 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.80% | 0.32% | -0.47% | -0.42% |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.21% | 1.17% | -0.04% | 1.03% |
| 2025-06-24 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 1.26% | 0.55% | -0.72% | -0.43% |
| 2025-06-05 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.99% | 1.16% | 0.85% | -0.32% | 0.28% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 2.52% | 1.71% | -0.81% | 1.38% |
| 2025-04-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 0.81% | 0.22% | -0.59% | -0.39% |
| 2025-04-03 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.69% | 0.67% | -0.02% | 0.39% |
| 2025-01-30 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 0.79% | 0.66% | -0.13% | 0.55% |
| 2025-01-23 | Strong Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 0.78% | 0.62% | -0.16% | 0.38% |
| 2025-01-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.79% | 0.06% | -0.73% | -0.50% |
| 2025-01-02 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 2.00% | 1.87% | -0.13% | 1.62% |
| 2024-11-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 0.87% | 0.28% | -0.58% | -0.40% |
| 2024-11-07 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 1.32% | 0.06% | -1.27% | -1.20% |
| 2024-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.82% | 0.09% | -0.73% | -0.46% |
| 2024-10-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.20% | 0.01% | -1.19% | -1.11% |
| 2024-07-26 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.79% | 1.84% | 1.79% | -0.05% | 1.75% |
| 2024-07-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 1.07% | 0.84% | -0.23% | 0.51% |
| 2024-07-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.86% | 0.03% | -0.83% | -0.24% |
| 2024-06-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 2.33% | 2.18% | -0.14% | 1.96% |
| 2024-05-30 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 1.28% | 0.39% | -0.89% | -0.27% |
| 2024-05-23 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.35% | 1.84% | 1.68% | -0.16% | 1.49% |
| 2024-04-25 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 1.44% | 1.38% | -0.05% | 1.09% |
| 2024-03-01 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 1.39% | 1.38% | -0.00% | 1.26% |
| 2023-12-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.87% | 0.74% | 0.44% | -0.30% | 0.17% |
| 2023-11-09 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.44% | 0.03% | -0.41% | -0.27% |
| 2023-09-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.71% | 0.27% | -0.44% | -0.31% |
| 2023-09-08 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.70% | 0.47% | -0.23% | 0.23% |
| 2023-08-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.72% | 0.00% | -0.72% | -0.66% |
| 2023-08-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 1.23% | 0.38% | -0.85% | -0.36% |
| 2023-07-20 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.18% | 0.81% | -0.37% | 0.70% |
| 2023-07-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.83% | 0.52% | -0.31% | 0.48% |
| 2023-07-13 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.93% | 0.37% | -0.56% | -0.27% |
| 2023-06-28 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.79% | 0.54% | -0.25% | 0.44% |
| 2023-06-23 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.55% | 0.05% | -0.50% | -0.39% |
| 2023-06-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 0.65% | 0.11% | -0.54% | -0.47% |
| 2023-06-02 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.51% | 0.12% | -0.39% | -0.13% |
| 2023-06-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.62% | 0.00% | -0.61% | -0.50% |
| 2023-05-26 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.79% | 0.95% | 0.76% | -0.19% | 0.67% |
| 2023-05-18 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 1.04% | 0.05% | -1.00% | -0.84% |
| 2023-04-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.75% | 0.66% | -0.08% | 0.62% |
| 2023-03-10 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.8% | 0.68% | 0.00% | -0.68% | -0.14% |
| 2023-02-23 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.93% | 0.25% | -0.67% | -0.29% |
| 2023-02-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 0.82% | 0.33% | -0.49% | -0.18% |
| 2023-01-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 1.36% | 0.00% | -1.36% | -1.01% |
| 2023-01-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 0.70% | 0.16% | -0.54% | -0.49% |
| 2023-01-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.96% | 1.25% | 0.09% | -1.16% | -0.56% |
| 2022-12-22 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 1.36% | 0.15% | -1.20% | -0.95% |
| 2022-12-15 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 1.41% | 0.20% | -1.21% | -1.15% |
| 2022-12-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.74% | 0.14% | -0.60% | -0.25% |
| 2022-11-18 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 1.00% | 0.06% | -0.94% | -0.43% |
| 2022-10-21 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 0.84% | 0.27% | -0.58% | -0.22% |
| 2022-10-14 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.28% | 1.02% | 0.15% | -0.88% | -0.70% |
| 2022-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.16% | 1.78% | 0.11% | -1.68% | -1.39% |
| 2022-09-15 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.29% | 0.27% | -1.02% | -0.96% |
| 2022-08-19 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.09% | 1.55% | 0.13% | -1.42% | -1.33% |
| 2022-07-28 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.14% | 1.16% | 1.01% | -0.16% | 0.88% |
| 2022-07-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.17% | 1.32% | 0.32% | -1.00% | -0.44% |
| 2022-05-19 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.4% | 1.30% | 0.41% | -0.89% | -0.56% |
| 2022-03-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 0.98% | 0.82% | -0.16% | 0.56% |
| 2022-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.55% | 3.01% | 0.93% | -2.08% | -2.00% |
| 2022-02-04 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.21% | 0.87% | 0.15% | -0.72% | -0.50% |
| 2022-01-20 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.12% | 1.59% | 0.07% | -1.52% | -0.77% |
| 2021-12-31 | Strong Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.04% | 0.90% | 0.90% | 0.00% | 0.69% |
| 2021-12-02 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.23% | 1.51% | 1.36% | -0.14% | 1.27% |
| 2021-11-11 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.03% | 0.93% | 0.00% | -0.93% | -0.46% |
| 2021-10-28 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.06% | 2.13% | 0.00% | -2.13% | -1.79% |
| 2021-10-21 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.15% | 1.82% | 0.00% | -1.82% | -0.89% |
| 2021-09-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.86% | 0.75% | 0.60% | -0.16% | 0.50% |
| 2021-08-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.97% | 0.96% | -0.00% | 0.82% |
| 2021-04-30 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.47% | 1.72% | 0.73% | -0.98% | -0.88% |
| 2021-03-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.41% | 2.10% | 0.00% | -2.10% | -1.54% |
| 2021-03-05 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.52% | 1.52% | 0.75% | -0.77% | -0.10% |
| 2020-12-04 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.2% | 0.94% | 0.76% | -0.19% | 0.71% |
| 2020-09-25 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.48% | 1.98% | 1.48% | -0.50% | 1.15% |

### Reversed Before Half VIX Range + Reversed by Close (96 days — weak alignment)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-25 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.91% | 0.66% | -0.25% | 0.66% |
| 2026-08-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 1.12% | 0.00% | -1.12% | -0.36% |
| 2026-07-09 | Strong Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.92% | 0.87% | 0.86% | -0.01% | 0.22% |
| 2026-07-07 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.74% | 0.27% | -0.47% | -0.45% |
| 2026-06-16 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 0.48% | 0.33% | -0.15% | 0.30% |
| 2026-06-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.04% | 1.41% | 1.41% | 0.00% | 1.27% |
| 2026-05-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.24% | 0.82% | 0.45% | -0.37% | -0.29% |
| 2026-05-07 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.81% | 0.34% | -0.47% | -0.25% |
| 2026-04-28 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.93% | 0.55% | -0.39% | -0.14% |
| 2026-04-09 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.24% | 1.29% | 0.34% | -0.95% | -0.60% |
| 2026-03-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.86% | 1.56% | 1.34% | -0.23% | 0.77% |
| 2026-02-19 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 1.92% | 0.05% | -1.87% | -1.77% |
| 2026-02-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.69% | 0.01% | -0.68% | -0.44% |
| 2026-01-13 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 1.14% | 0.01% | -1.14% | -0.71% |
| 2026-01-01 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.32% | 0.09% | -0.23% | -0.13% |
| 2025-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.44% | 0.11% | -0.33% | -0.15% |
| 2025-11-27 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.64% | 0.19% | -0.45% | -0.16% |
| 2025-11-18 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.59% | 0.03% | -0.56% | -0.49% |
| 2025-10-30 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.72% | 0.18% | -0.54% | -0.36% |
| 2025-10-09 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.65% | 0.70% | 0.50% | -0.20% | 0.38% |
| 2025-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.76% | 0.75% | -0.01% | 0.72% |
| 2025-09-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 1.09% | 0.00% | -1.09% | -0.96% |
| 2025-08-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.92% | 0.08% | -0.84% | -0.76% |
| 2025-08-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.58% | 0.05% | -0.53% | -0.29% |
| 2025-07-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.90% | 0.01% | -0.89% | -0.76% |
| 2025-07-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.58% | 0.06% | -0.52% | -0.40% |
| 2025-05-06 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.73% | 0.04% | -0.69% | -0.67% |
| 2025-04-29 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.07% | 0.68% | 0.36% | -0.33% | -0.19% |
| 2025-02-25 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.49% | 0.48% | -0.01% | 0.04% |
| 2025-02-04 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 1.44% | 1.08% | -0.37% | 0.84% |
| 2025-01-21 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 1.92% | 0.02% | -1.90% | -1.57% |
| 2025-01-14 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 0.56% | 0.43% | -0.14% | 0.18% |
| 2024-12-19 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.56% | 0.54% | -0.03% | 0.36% |
| 2024-11-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 1.09% | 1.09% | 0.00% | 0.82% |
| 2024-10-25 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.88% | 1.50% | 0.09% | -1.41% | -0.84% |
| 2024-10-18 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.29% | 0.90% | -0.39% | 0.80% |
| 2024-10-11 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.43% | 0.17% | -0.26% | -0.04% |
| 2024-07-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.49% | 0.13% | -0.36% | -0.27% |
| 2024-06-21 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.14% | 0.03% | -1.11% | -0.88% |
| 2024-06-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.54% | 0.00% | -0.54% | -0.35% |
| 2024-05-10 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.15% | 0.82% | 0.64% | -0.18% | 0.29% |
| 2024-05-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.08% | 1.69% | 0.37% | -1.32% | -1.15% |
| 2024-04-26 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 1.04% | 0.00% | -1.04% | -0.75% |
| 2024-03-14 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 1.31% | 1.01% | -0.30% | 0.78% |
| 2024-02-29 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 0.91% | 0.57% | -0.34% | 0.49% |
| 2024-02-09 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.0% | 0.80% | 0.36% | -0.45% | 0.27% |
| 2024-02-01 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 0.80% | 0.24% | -0.56% | -0.41% |
| 2024-01-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.99% | 0.02% | -0.97% | -0.39% |
| 2023-12-01 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.53% | 0.48% | -0.05% | 0.31% |
| 2023-09-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 0.89% | 0.74% | -0.15% | 0.29% |
| 2023-09-28 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.39% | 0.02% | -1.36% | -1.06% |
| 2023-09-15 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.46% | 0.33% | -0.13% | 0.06% |
| 2023-09-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.61% | 0.20% | -0.41% | -0.13% |
| 2023-08-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 1.10% | 0.25% | -0.85% | -0.79% |
| 2023-07-27 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 1.33% | 0.08% | -1.25% | -0.76% |
| 2023-06-22 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.67% | 0.17% | -0.49% | -0.39% |
| 2023-06-16 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 0.81% | 0.75% | -0.06% | 0.54% |
| 2023-06-08 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.86% | 0.28% | -0.58% | -0.42% |
| 2023-05-25 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.73% | 0.37% | -0.36% | 0.37% |
| 2023-05-11 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.47% | 0.00% | -0.47% | -0.29% |
| 2023-04-21 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.61% | 0.13% | -0.49% | -0.12% |
| 2023-03-03 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 1.23% | 1.11% | -0.12% | 0.81% |
| 2023-03-02 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.79% | 0.13% | -0.66% | -0.59% |
| 2023-02-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 1.01% | 0.05% | -0.96% | -0.72% |
| 2023-02-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.06% | 1.17% | 0.78% | -0.39% | 0.54% |
| 2023-01-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 0.50% | 0.19% | -0.31% | -0.17% |
| 2023-01-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.94% | 1.39% | 0.21% | -1.18% | -0.79% |
| 2022-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 1.48% | 0.38% | -1.10% | -0.85% |
| 2022-12-09 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.35% | 0.00% | -1.35% | -0.91% |
| 2022-12-08 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.47% | 0.29% | -0.18% | 0.23% |
| 2022-12-01 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 0.57% | 0.08% | -0.50% | -0.38% |
| 2022-11-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.48% | 0.03% | -0.45% | -0.16% |
| 2022-11-03 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.79% | 0.76% | -0.02% | 0.44% |
| 2022-10-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.27% | 0.90% | 0.14% | -0.76% | -0.41% |
| 2022-09-22 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 1.08% | 0.64% | -0.44% | 0.15% |
| 2022-09-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.15% | 0.78% | 0.01% | -0.77% | -0.52% |
| 2022-09-08 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 0.64% | 0.33% | -0.31% | 0.29% |
| 2022-06-10 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.21% | 0.93% | 0.25% | -0.68% | -0.57% |
| 2022-04-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.22% | 1.87% | 0.28% | -1.59% | -1.26% |
| 2022-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.73% | 1.84% | 0.00% | -1.84% | -1.14% |
| 2022-02-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.17% | 1.47% | 0.04% | -1.43% | -1.39% |
| 2022-01-07 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.13% | 1.12% | 0.60% | -0.52% | 0.12% |
| 2021-12-30 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.02% | 0.67% | 0.36% | -0.31% | 0.16% |
| 2021-12-17 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.0% | 1.89% | 0.10% | -1.79% | -1.63% |
| 2021-11-26 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 2.06% | 0.04% | -2.03% | -1.92% |
| 2021-10-01 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.16% | 0.59% | 0.14% | -0.45% | -0.03% |
| 2021-09-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.71% | 0.28% | -0.43% | -0.31% |
| 2021-09-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 1.06% | 0.88% | -0.19% | 0.81% |
| 2021-07-30 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.74% | 0.39% | -0.35% | -0.17% |
| 2021-07-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.62% | 0.27% | -0.35% | 0.06% |
| 2021-06-17 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.94% | 0.97% | 0.77% | -0.19% | 0.21% |
| 2021-03-10 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.42% | 0.76% | 0.10% | -0.66% | -0.22% |
| 2021-01-29 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.53% | 2.64% | 0.14% | -2.50% | -2.05% |
| 2020-11-27 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.26% | 0.88% | 0.14% | -0.74% | -0.53% |
| 2020-10-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.47% | 1.18% | 0.95% | -0.23% | 0.32% |
| 2020-09-10 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.4% | 1.17% | 0.88% | -0.30% | 0.80% |

### Mixed Days (FII vs PRO opposing) — 92 days

| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|
| 2026-09-01 | Mildly Bullish | Strong Bearish | Top to Down | 0.7% | 0.79% | 0.27% | -0.52% | -0.09% |
| 2026-08-20 | Bearish | Bullish | Down to Up | 0.71% | 0.33% | 0.16% | -0.17% | 0.03% |
| 2026-08-18 | Mildly Bullish | Bearish | Top to Down | 0.71% | 0.47% | 0.19% | -0.28% | -0.28% |
| 2026-08-14 | Mildly Bearish | Bullish | Down to Up | - | 0.44% | 0.18% | -0.27% | 0.02% |
| 2026-08-13 | Bearish | Mildly Bullish | Top to Down | 0.74% | 0.49% | 0.00% | -0.49% | -0.15% |
| 2026-08-06 | Mildly Bearish | Bullish | Top to Down | 0.76% | 0.30% | 0.15% | -0.15% | -0.02% |
| 2026-07-28 | Bullish | Mildly Bearish | Down to Up | 0.8% | 0.36% | 0.29% | -0.07% | 0.07% |
| 2026-07-16 | Bearish | Mildly Bullish | Top to Down | 0.84% | 0.57% | 0.18% | -0.38% | -0.25% |
| 2026-06-04 | Mildly Bearish | Strong Bullish | Down to Up | 1.03% | 0.94% | 0.79% | -0.15% | 0.67% |
| 2026-06-03 | Mildly Bearish | Bullish | Top to Down | - | 1.32% | 0.19% | -1.13% | -0.08% |
| 2026-04-08 | Mildly Bullish | Mildly Bearish | Down to Up | - | 0.82% | 0.71% | -0.11% | 0.66% |
| 2026-03-16 | Strong Bearish | Bullish | Down to Up | - | 2.37% | 1.67% | -0.70% | 1.04% |
| 2026-02-10 | Bullish | Strong Bearish | Top to Down | 0.77% | 0.46% | 0.26% | -0.20% | -0.02% |
| 2026-01-22 | Bearish | Strong Bullish | Top to Down | 0.87% | 1.05% | 0.36% | -0.69% | -0.09% |
| 2025-12-05 | Mildly Bearish | Mildly Bullish | Down to Up | - | 0.84% | 0.78% | -0.06% | 0.68% |
| 2025-09-09 | Mildly Bullish | Bearish | Down to Up | 0.68% | 0.31% | 0.11% | -0.20% | 0.06% |
| 2025-07-04 | Bullish | Strong Bearish | Down to Up | - | 0.55% | 0.16% | -0.38% | 0.15% |
| 2025-06-27 | Bullish | Strong Bearish | Down to Up | - | 0.51% | 0.30% | -0.21% | 0.22% |
| 2025-05-12 | Mildly Bearish | Mildly Bullish | Down to Up | - | 2.32% | 2.15% | -0.17% | 2.05% |
| 2025-04-24 | Bullish | Mildly Bearish | Top to Down | 1.01% | 0.54% | 0.29% | -0.25% | -0.14% |
| 2025-03-20 | Mildly Bullish | Bearish | Down to Up | 0.84% | 1.05% | 0.78% | -0.27% | 0.56% |
| 2025-03-07 | Mildly Bullish | Bearish | Down to Up | - | 0.75% | 0.56% | -0.20% | 0.13% |
| 2025-01-28 | Strong Bullish | Strong Bearish | Down to Up | 1.14% | 1.22% | 0.77% | -0.45% | 0.07% |
| 2025-01-07 | Bullish | Strong Bearish | Down to Up | 0.99% | 0.66% | 0.49% | -0.18% | 0.06% |
| 2025-01-01 | Strong Bearish | Bullish | Down to Up | - | 1.10% | 0.78% | -0.32% | 0.51% |
| 2024-12-20 | Mildly Bearish | Strong Bullish | Top to Down | 0.91% | 2.21% | 0.44% | -1.77% | -1.37% |
| 2024-12-13 | Bearish | Bullish | Down to Up | 0.83% | 2.50% | 1.20% | -1.30% | 1.15% |
| 2024-12-05 | Mildly Bullish | Mildly Bearish | Down to Up | 0.91% | 2.29% | 1.30% | -0.99% | 0.66% |
| 2024-11-28 | Mildly Bullish | Bearish | Top to Down | 0.92% | 1.95% | 0.29% | -1.65% | -1.30% |
| 2024-11-14 | Mildly Bearish | Strong Bullish | Down to Up | 0.97% | 0.81% | 0.57% | -0.25% | 0.07% |
| 2024-11-05 | Bullish | Strong Bearish | Down to Up | - | 1.62% | 1.31% | -0.31% | 1.18% |
| 2024-10-09 | Bearish | Strong Bullish | Top to Down | - | 1.14% | 0.67% | -0.47% | -0.18% |
| 2024-09-30 | Mildly Bullish | Strong Bearish | Top to Down | - | 1.31% | 0.28% | -1.03% | -0.92% |
| 2024-09-27 | Bullish | Strong Bearish | Top to Down | 0.76% | 0.48% | 0.11% | -0.37% | -0.28% |
| 2024-09-06 | Mildly Bullish | Bearish | Top to Down | 0.9% | 1.46% | 0.30% | -1.17% | -0.90% |
| 2024-08-29 | Mildly Bullish | Strong Bearish | Down to Up | 0.88% | 0.78% | 0.63% | -0.15% | 0.49% |
| 2024-08-23 | Mildly Bullish | Bearish | Top to Down | 0.82% | 0.35% | 0.05% | -0.30% | -0.05% |
| 2024-08-08 | Strong Bearish | Strong Bullish | Top to Down | 1.02% | 1.08% | 0.38% | -0.70% | -0.62% |
| 2024-08-02 | Strong Bullish | Strong Bearish | Top to Down | 0.81% | 0.67% | 0.25% | -0.41% | -0.36% |
| 2024-08-01 | Strong Bearish | Strong Bullish | Top to Down | 0.83% | 0.49% | 0.19% | -0.30% | -0.10% |
| 2024-07-25 | Bearish | Bullish | Down to Up | 0.74% | 0.89% | 0.81% | -0.08% | 0.76% |
| 2024-07-10 | Strong Bearish | Strong Bullish | Top to Down | - | 1.31% | 0.00% | -1.30% | -0.60% |
| 2024-07-09 | Strong Bullish | Strong Bearish | Down to Up | - | 0.46% | 0.38% | -0.08% | 0.27% |
| 2024-07-01 | Mildly Bullish | Strong Bearish | Down to Up | - | 0.71% | 0.71% | -0.00% | 0.54% |
| 2024-06-28 | Strong Bullish | Bearish | Top to Down | 0.89% | 0.78% | 0.37% | -0.42% | -0.32% |
| 2024-06-27 | Bullish | Strong Bearish | Down to Up | 0.89% | 1.18% | 0.86% | -0.32% | 0.65% |
| 2024-06-20 | Bullish | Strong Bearish | Top to Down | 0.86% | 0.77% | 0.16% | -0.61% | -0.03% |
| 2024-06-14 | Bullish | Bearish | Top to Down | 0.85% | 0.67% | 0.11% | -0.56% | -0.05% |
| 2024-06-11 | Strong Bullish | Strong Bearish | Top to Down | - | 0.79% | 0.45% | -0.33% | -0.09% |
| 2024-05-29 | Mildly Bullish | Strong Bearish | Top to Down | - | 0.62% | 0.28% | -0.34% | -0.25% |
| 2024-05-27 | Bullish | Strong Bearish | Top to Down | - | 1.04% | 0.31% | -0.73% | -0.47% |
| 2024-04-10 | Mildly Bullish | Strong Bearish | Down to Up | 0.72% | 0.45% | 0.24% | -0.20% | 0.07% |
| 2024-04-09 | Bullish | Strong Bearish | Top to Down | - | 0.69% | 0.01% | -0.67% | -0.54% |
| 2024-03-28 | Bearish | Strong Bullish | Down to Up | 0.8% | 1.59% | 1.59% | 0.00% | 0.81% |
| 2024-03-18 | Mildly Bullish | Strong Bearish | Down to Up | - | 0.94% | 0.61% | -0.33% | 0.28% |
| 2024-03-06 | Bearish | Mildly Bullish | Down to Up | - | 1.22% | 0.76% | -0.46% | 0.68% |
| 2024-03-05 | Strong Bullish | Strong Bearish | Top to Down | - | 0.66% | 0.20% | -0.46% | -0.06% |
| 2024-02-22 | Bullish | Strong Bearish | Down to Up | 1.0% | 1.71% | 0.77% | -0.93% | 0.61% |
| 2024-02-19 | Bearish | Bullish | Down to Up | - | 0.75% | 0.38% | -0.37% | 0.06% |
| 2024-02-16 | Strong Bullish | Mildly Bearish | Down to Up | 0.96% | 0.45% | 0.22% | -0.23% | 0.06% |
| 2024-02-08 | Mildly Bearish | Bullish | Top to Down | 0.98% | 1.57% | 0.01% | -1.56% | -1.14% |
| 2024-02-05 | Bullish | Strong Bearish | Top to Down | - | 1.08% | 0.20% | -0.89% | -0.73% |
| 2024-01-19 | Bearish | Strong Bullish | Down to Up | 0.89% | 0.44% | 0.26% | -0.19% | 0.11% |
| 2024-01-11 | Bearish | Strong Bullish | Top to Down | 0.82% | 0.61% | 0.18% | -0.43% | -0.09% |
| 2023-12-29 | Bullish | Strong Bearish | Top to Down | 0.95% | 0.43% | 0.15% | -0.28% | -0.04% |
| 2023-12-28 | Bearish | Strong Bullish | Down to Up | 0.98% | 0.57% | 0.40% | -0.17% | 0.27% |
| 2023-12-11 | Mildly Bearish | Bullish | Down to Up | - | 0.49% | 0.29% | -0.20% | 0.13% |
| 2023-12-07 | Bullish | Strong Bearish | Top to Down | 0.87% | 0.43% | 0.04% | -0.39% | -0.08% |
| 2023-10-27 | Strong Bearish | Strong Bullish | Down to Up | 0.74% | 0.79% | 0.78% | -0.01% | 0.70% |
| 2023-10-20 | Bearish | Strong Bullish | Top to Down | 0.69% | 0.38% | 0.26% | -0.12% | -0.00% |
| 2023-08-21 | Strong Bullish | Bearish | Down to Up | - | 0.67% | 0.55% | -0.12% | 0.31% |
| 2023-08-09 | Mildly Bearish | Mildly Bullish | Down to Up | - | 0.91% | 0.34% | -0.56% | 0.27% |
| 2023-08-04 | Mildly Bearish | Strong Bullish | Down to Up | 0.7% | 0.53% | 0.39% | -0.14% | 0.24% |
| 2023-06-07 | Bearish | Strong Bullish | Down to Up | - | 0.55% | 0.39% | -0.16% | 0.35% |
| 2023-03-17 | Mildly Bearish | Strong Bullish | Down to Up | 1.02% | 1.09% | 0.19% | -0.90% | 0.07% |
| 2023-03-15 | Bearish | Bullish | Top to Down | - | 1.57% | 0.26% | -1.32% | -1.12% |
| 2023-02-03 | Mildly Bearish | Strong Bullish | Down to Up | 0.99% | 1.61% | 0.84% | -0.78% | 0.62% |
| 2022-12-30 | Bullish | Mildly Bearish | Top to Down | 0.93% | 1.01% | 0.03% | -0.98% | -0.78% |
| 2022-11-17 | Bullish | Mildly Bearish | Top to Down | 0.95% | 0.57% | 0.32% | -0.25% | -0.13% |
| 2022-11-02 | Mildly Bullish | Bearish | Top to Down | - | 0.70% | 0.00% | -0.70% | -0.58% |
| 2022-07-29 | Bullish | Strong Bearish | Down to Up | 1.07% | 0.90% | 0.54% | -0.36% | 0.46% |
| 2022-07-22 | Bullish | Bearish | Down to Up | 1.06% | 0.85% | 0.55% | -0.30% | 0.32% |
| 2022-07-11 | Bullish | Mildly Bearish | Down to Up | - | 0.82% | 0.70% | -0.13% | 0.39% |
| 2022-07-04 | Mildly Bearish | Strong Bullish | Down to Up | - | 1.21% | 0.90% | -0.31% | 0.76% |
| 2022-05-16 | Bullish | Bearish | Down to Up | - | 1.49% | 0.83% | -0.65% | 0.12% |
| 2022-04-08 | Bearish | Bullish | Down to Up | 1.2% | 1.36% | 0.82% | -0.54% | 0.58% |
| 2022-01-21 | Bearish | Strong Bullish | Down to Up | 1.12% | 1.25% | 0.53% | -0.72% | 0.21% |
| 2021-12-01 | Mildly Bullish | Bearish | Down to Up | - | 0.86% | 0.63% | -0.23% | 0.48% |
| 2021-10-22 | Mildly Bearish | Bullish | Top to Down | 1.14% | 1.53% | 0.45% | -1.07% | -0.65% |
| 2021-10-13 | Mildly Bearish | Bullish | Down to Up | - | 0.79% | 0.55% | -0.24% | 0.38% |
| 2021-05-19 | Bullish | Mildly Bearish | Top to Down | 1.21% | 0.82% | 0.49% | -0.33% | -0.26% |
| 2021-01-22 | Mildly Bullish | Mildly Bearish | Top to Down | 1.36% | 1.79% | 0.25% | -1.54% | -1.49% |

### FII Solo View (PRO Neutral) — 90 days

| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-21 | Strong Bullish | Neutral | Top to Down | - | 0.32% | 0.00% | -0.32% | -0.13% |
| 2026-07-24 | Bearish | Neutral | Down to Up | - | 0.92% | 0.66% | -0.25% | 0.51% |
| 2026-07-23 | Strong Bearish | Neutral | Top to Down | 0.84% | 0.77% | 0.36% | -0.41% | -0.14% |
| 2026-07-17 | Mildly Bullish | Neutral | Down to Up | - | 1.11% | 0.99% | -0.12% | 0.91% |
| 2026-07-14 | Bullish | Neutral | Top to Down | 0.84% | 0.55% | 0.37% | -0.18% | -0.14% |
| 2026-07-06 | Mildly Bearish | Neutral | Down to Up | - | 0.71% | 0.62% | -0.08% | 0.48% |
| 2026-07-01 | Bullish | Neutral | Down to Up | - | 0.65% | 0.64% | -0.01% | 0.38% |
| 2026-06-10 | Bullish | Neutral | Top to Down | - | 1.04% | 0.82% | -0.21% | -0.08% |
| 2026-05-26 | Strong Bullish | Neutral | Top to Down | 1.05% | 0.85% | 0.36% | -0.49% | -0.29% |
| 2026-03-23 | Bearish | Neutral | Top to Down | - | 1.67% | 0.12% | -1.55% | -1.45% |
| 2026-03-17 | Bullish | Neutral | Down to Up | 1.36% | 1.32% | 0.70% | -0.62% | 0.28% |
| 2026-03-06 | Bearish | Neutral | Top to Down | - | 1.16% | 0.18% | -0.98% | -0.76% |
| 2026-02-25 | Bearish | Neutral | Top to Down | - | 0.88% | 0.55% | -0.33% | -0.13% |
| 2026-02-03 | Bearish | Neutral | Top to Down | 0.87% | 2.66% | 0.13% | -2.53% | -2.26% |
| 2026-01-29 | Mildly Bearish | Neutral | Down to Up | 0.85% | 1.18% | 0.45% | -0.73% | 0.30% |
| 2026-01-14 | Mildly Bearish | Neutral | Down to Up | - | 0.73% | 0.56% | -0.17% | 0.08% |
| 2025-12-15 | Bullish | Neutral | Down to Up | - | 0.55% | 0.45% | -0.10% | 0.32% |
| 2025-11-12 | Mildly Bullish | Neutral | Down to Up | - | 0.59% | 0.39% | -0.21% | 0.15% |
| 2025-10-17 | Bullish | Neutral | Down to Up | - | 1.07% | 0.92% | -0.15% | 0.62% |
| 2025-10-07 | Mildly Bullish | Neutral | Down to Up | 0.64% | 0.58% | 0.54% | -0.04% | 0.11% |
| 2025-09-30 | Mildly Bullish | Neutral | Top to Down | 0.72% | 0.58% | 0.16% | -0.42% | -0.24% |
| 2025-09-03 | Bearish | Neutral | Down to Up | - | 0.83% | 0.49% | -0.34% | 0.39% |
| 2025-07-29 | Bearish | Neutral | Down to Up | 0.76% | 1.01% | 0.97% | -0.04% | 0.90% |
| 2025-07-21 | Bearish | Neutral | Down to Up | - | 0.92% | 0.45% | -0.47% | 0.38% |
| 2025-05-13 | Mildly Bullish | Neutral | Top to Down | 1.16% | 1.71% | 0.44% | -1.27% | -1.09% |
| 2025-04-04 | Mildly Bullish | Neutral | Top to Down | - | 1.54% | 0.10% | -1.44% | -1.20% |
| 2025-03-28 | Mildly Bullish | Neutral | Top to Down | - | 0.84% | 0.21% | -0.64% | -0.45% |
| 2025-02-17 | Mildly Bearish | Neutral | Down to Up | - | 1.09% | 0.72% | -0.37% | 0.67% |
| 2025-01-27 | Strong Bearish | Neutral | Top to Down | - | 0.96% | 0.29% | -0.67% | -0.54% |
| 2025-01-10 | Mildly Bearish | Neutral | Top to Down | - | 1.07% | 0.19% | -0.88% | -0.49% |
| 2024-12-12 | Bullish | Neutral | Top to Down | 0.84% | 0.60% | 0.29% | -0.31% | -0.26% |
| 2024-10-10 | Bearish | Neutral | Top to Down | 0.89% | 0.62% | 0.27% | -0.35% | -0.24% |
| 2024-10-07 | Strong Bearish | Neutral | Top to Down | - | 1.79% | 0.23% | -1.55% | -1.06% |
| 2024-08-30 | Strong Bullish | Neutral | Top to Down | 0.87% | 0.27% | 0.07% | -0.20% | -0.01% |
| 2024-07-08 | Strong Bearish | Neutral | Down to Up | - | 0.43% | 0.06% | -0.37% | 0.01% |
| 2024-05-31 | Strong Bearish | Neutral | Top to Down | 1.52% | 0.84% | 0.38% | -0.46% | -0.08% |
| 2024-05-07 | Mildly Bullish | Neutral | Top to Down | - | 1.19% | 0.04% | -1.15% | -0.82% |
| 2024-04-04 | Mildly Bearish | Neutral | Top to Down | 0.72% | 1.40% | 0.12% | -1.28% | -0.23% |
| 2024-01-10 | Strong Bullish | Neutral | Down to Up | - | 0.90% | 0.52% | -0.37% | 0.45% |
| 2023-11-24 | Bearish | Neutral | Top to Down | 0.71% | 0.32% | 0.12% | -0.21% | -0.11% |
| 2023-09-27 | Mildly Bearish | Neutral | Down to Up | - | 0.90% | 0.48% | -0.42% | 0.46% |
| 2023-09-07 | Strong Bearish | Neutral | Down to Up | 0.67% | 0.95% | 0.71% | -0.25% | 0.64% |
| 2023-09-05 | Bullish | Neutral | Down to Up | - | 0.31% | 0.11% | -0.20% | 0.07% |
| 2023-08-08 | Strong Bullish | Neutral | Top to Down | - | 0.51% | 0.04% | -0.48% | -0.29% |
| 2023-07-26 | Mildly Bearish | Neutral | Down to Up | - | 0.55% | 0.47% | -0.08% | 0.20% |
| 2023-07-11 | Strong Bearish | Neutral | Down to Up | - | 0.56% | 0.45% | -0.11% | 0.11% |
| 2023-04-20 | Mildly Bullish | Neutral | Top to Down | 0.77% | 0.56% | 0.26% | -0.31% | -0.08% |
| 2023-02-08 | Bullish | Neutral | Down to Up | - | 0.86% | 0.84% | -0.03% | 0.63% |
| 2023-01-13 | Bullish | Neutral | Down to Up | 0.96% | 1.26% | 0.74% | -0.52% | 0.46% |
| 2022-12-21 | Strong Bearish | Neutral | Top to Down | - | 1.67% | 0.20% | -1.47% | -1.23% |
| 2022-11-29 | Mildly Bullish | Neutral | Down to Up | - | 0.68% | 0.68% | 0.00% | 0.28% |
| 2022-11-11 | Mildly Bullish | Neutral | Down to Up | 0.98% | 0.55% | 0.48% | -0.07% | 0.45% |
| 2022-10-20 | Bearish | Neutral | Down to Up | 1.1% | 0.93% | 0.92% | -0.01% | 0.82% |
| 2022-10-19 | Bullish | Neutral | Top to Down | - | 0.76% | 0.22% | -0.54% | -0.28% |
| 2022-10-17 | Bullish | Neutral | Down to Up | - | 1.34% | 1.07% | -0.27% | 1.03% |
| 2022-09-23 | Mildly Bearish | Neutral | Top to Down | 1.19% | 1.97% | 0.26% | -1.71% | -1.49% |
| 2022-08-26 | Bullish | Neutral | Top to Down | 1.23% | 0.94% | 0.37% | -0.56% | -0.21% |
| 2022-08-12 | Bullish | Neutral | Down to Up | 1.16% | 0.71% | 0.37% | -0.35% | 0.22% |
| 2022-06-20 | Mildly Bullish | Neutral | Down to Up | - | 1.24% | 0.31% | -0.93% | 0.22% |
| 2022-06-02 | Bearish | Neutral | Down to Up | 1.31% | 1.22% | 1.00% | -0.22% | 0.94% |
| 2022-05-25 | Mildly Bullish | Neutral | Top to Down | - | 1.33% | 0.16% | -1.17% | -0.98% |
| 2022-05-13 | Bearish | Neutral | Top to Down | 1.53% | 2.14% | 0.66% | -1.48% | -1.31% |
| 2022-04-13 | Bearish | Neutral | Top to Down | 1.14% | 1.17% | 0.36% | -0.81% | -0.75% |
| 2022-03-31 | Mildly Bullish | Neutral | Top to Down | 1.3% | 0.70% | 0.23% | -0.48% | -0.29% |
| 2022-03-29 | Bullish | Neutral | Down to Up | - | 0.61% | 0.26% | -0.35% | 0.22% |
| 2022-02-23 | Mildly Bearish | Neutral | Top to Down | - | 1.12% | 0.15% | -0.97% | -0.81% |
| 2022-02-21 | Mildly Bullish | Neutral | Down to Up | - | 1.63% | 0.92% | -0.71% | 0.08% |
| 2022-02-11 | Bullish | Neutral | Top to Down | 1.12% | 0.85% | 0.00% | -0.85% | -0.60% |
| 2022-02-02 | Mildly Bullish | Neutral | Down to Up | - | 0.67% | 0.49% | -0.17% | 0.48% |
| 2022-02-01 | Mildly Bullish | Neutral | Down to Up | - | 2.15% | 0.53% | -1.62% | 0.43% |
| 2021-12-15 | Bearish | Neutral | Top to Down | - | 0.91% | 0.15% | -0.75% | -0.67% |
| 2021-10-14 | Mildly Bullish | Neutral | Down to Up | 1.01% | 0.55% | 0.42% | -0.13% | 0.36% |
| 2021-09-30 | Bearish | Neutral | Top to Down | 1.19% | 0.88% | 0.13% | -0.75% | -0.62% |
| 2021-09-28 | Mildly Bearish | Neutral | Top to Down | - | 1.84% | 0.00% | -1.84% | -0.97% |
| 2021-08-27 | Bullish | Neutral | Down to Up | 0.85% | 0.92% | 0.47% | -0.45% | 0.29% |
| 2021-08-18 | Bearish | Neutral | Top to Down | 0.84% | 0.98% | 0.06% | -0.93% | -0.85% |
| 2021-08-02 | Mildly Bearish | Neutral | Down to Up | - | 0.34% | 0.11% | -0.23% | 0.08% |
| 2021-05-28 | Bullish | Neutral | Down to Up | 1.25% | 0.48% | 0.31% | -0.17% | 0.22% |
| 2021-05-21 | Bearish | Neutral | Down to Up | 1.24% | 1.35% | 1.34% | -0.01% | 1.31% |
| 2021-01-21 | Mildly Bearish | Neutral | Top to Down | 1.36% | 1.59% | 0.15% | -1.44% | -0.68% |
| 2021-01-12 | Mildly Bearish | Neutral | Down to Up | - | 1.06% | 0.80% | -0.26% | 0.70% |
| 2021-01-04 | Mildly Bearish | Neutral | Down to Up | - | 1.36% | 0.31% | -1.05% | 0.28% |
| 2021-01-01 | Mildly Bullish | Neutral | Down to Up | 1.33% | 0.39% | 0.38% | -0.01% | 0.13% |
| 2020-11-09 | Mildly Bullish | Neutral | Down to Up | - | 0.85% | 0.59% | -0.25% | 0.55% |
| 2020-11-06 | Bullish | Neutral | Down to Up | 1.32% | 1.19% | 1.01% | -0.18% | 0.86% |
| 2020-10-26 | Mildly Bearish | Neutral | Top to Down | - | 1.89% | 0.00% | -1.89% | -1.34% |
| 2020-10-01 | Mildly Bullish | Neutral | Down to Up | 1.23% | 0.68% | 0.56% | -0.12% | 0.51% |
| 2020-09-02 | Mildly Bullish | Neutral | Down to Up | - | 1.08% | 0.66% | -0.42% | 0.56% |
| 2020-08-24 | Mildly Bullish | Neutral | Down to Up | - | 0.74% | 0.74% | 0.00% | 0.53% |
| 2020-08-21 | Mildly Bearish | Neutral | Top to Down | 1.3% | 0.49% | 0.07% | -0.41% | -0.27% |


---
*Generated from 1323 trading days (2020-08-06 to 2026-09-01)*
