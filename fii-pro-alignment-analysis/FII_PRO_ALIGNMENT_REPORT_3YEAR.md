# FII-PRO Alignment Reversal Analysis — Last 3 Years

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
| Total Trading Days | 730 | 100.0% |
| **Aligned Days (Bullish + Bearish)** | **342** | **46.8%** |
| Bullish Alignment | 170 | 23.3% |
| Bearish Alignment | 172 | 23.6% |
| Mixed (opposing views) | 82 | 11.2% |
| Neutral/Unclear | 306 | 41.9% |

## Alignment Outcome Breakdown

When FII and PRO align, does the first half move in their direction and then reverse?

### All Aligned Days (342 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 177 | 51.8% | 0.42% | -0.55% | -0.07% |
| Against then Recovered | 165 | 48.2% | 0.42% | -0.5% | -0.03% |

### Bullish Alignment (170 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 97 | 57.1% | 0.16% | -0.8% | -0.55% |
| Against then Recovered | 73 | 42.9% | 0.68% | -0.25% | 0.51% |

### Bearish Alignment (172 days)

| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |
|---------|------:|--:|----------:|---------:|----------------:|
| Worked then Reversed | 80 | 46.5% | 0.74% | -0.26% | 0.51% |
| Against then Recovered | 92 | 53.5% | 0.22% | -0.7% | -0.46% |

## Worked and Remained: Did the Aligned View Win by Close?

A different lens: regardless of intraday path, did the market **close** in the aligned direction?

- **Worked and Remained**: Close was in the aligned direction (bullish alignment + close > open, or bearish alignment + close < open)
- **Reversed by Close**: Close was against the aligned direction

### Overall (342 aligned days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg Range% |
|---------------|------:|--:|----------------:|----------:|---------:|-----------:|
| Worked and Remained | 163 | 47.7% | -0.03% | 0.43% | -0.5% | 0.93% |
| Reversed by Close | 179 | 52.3% | -0.07% | 0.42% | -0.55% | 0.97% |

### Bullish Alignment (170 days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |
|---------------|------:|--:|----------------:|----------:|---------:|
| Worked and Remained | 73 | 42.9% | 0.51% | 0.68% | -0.25% |
| Reversed by Close | 97 | 57.1% | -0.55% | 0.16% | -0.8% |

### Bearish Alignment (172 days)

| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |
|---------------|------:|--:|----------------:|----------:|---------:|
| Worked and Remained | 90 | 52.3% | -0.47% | 0.22% | -0.71% |
| Reversed by Close | 82 | 47.7% | 0.49% | 0.72% | -0.26% |

### Worked and Remained: Expiry vs Non-Expiry

| Context | Aligned | Worked and Remained | % | Reversed by Close | % |
|---------|--------:|--------------------:|--:|------------------:|--:|
| Expiry Days | 68 | 39 | 57.4% | 29 | 42.6% |
| Non-Expiry Days | 274 | 124 | 45.3% | 150 | 54.7% |

### Worked and Remained: VIX Regime

| VIX Regime | Aligned | Worked and Remained | % | Reversed by Close | % |
|------------|--------:|--------------------:|--:|------------------:|--:|
| Low (<15) | 245 | 126 | 51.4% | 119 | 48.6% |
| Normal (15-20) | 81 | 27 | 33.3% | 54 | 66.7% |
| Elevated (20-30) | 16 | 10 | 62.5% | 6 | 37.5% |
| High (>30) | 0 | 0 | - | 0 | - |

### Worked and Remained: Year-over-Year

| Year | Aligned | Worked and Remained | % | Reversed by Close | % |
|------|--------:|--------------------:|--:|------------------:|--:|
| 2023 | 38 | 23 | 60.5% | 15 | 39.5% |
| 2024 | 127 | 52 | 40.9% | 75 | 59.1% |
| 2025 | 102 | 55 | 53.9% | 47 | 46.1% |
| 2026 | 75 | 33 | 44.0% | 42 | 56.0% |

## VIX Half-Range Exhaustion: Did the Move Exhaust Before Reversing?

Compares the first-half move in the aligned direction against **half of the VIX-predicted range**.
If the move exceeded half the predicted range, it suggests momentum exhaustion before reversal.
If it reversed before reaching half, the reversal happened without significant momentum.

- **Exceeded Half then Reversed**: Aligned-direction move > ½ × VIX predicted range
- **Reversed Before Half**: Aligned-direction move ≤ ½ × VIX predicted range

### Overall (342 aligned days with VIX data)

| VIX Exhaustion | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg VIX Predicted% |
|----------------|------:|--:|----------------:|----------:|---------:|-------------------:|
| Exceeded Half then Reversed | 156 | 45.6% | 0.0% | 0.51% | -0.54% | 0.73% |
| Reversed Before Half | 186 | 54.4% | -0.1% | 0.35% | -0.52% | 0.74% |

### Cross-Tab: VIX Exhaustion × Close Outcome

Does exceeding half the VIX range predict whether the aligned view wins by close?

| VIX Exhaustion | Worked and Remained | % | Reversed by Close | % | Total |
|----------------|--------------------:|--:|------------------:|--:|------:|
| Exceeded Half then Reversed | 129 | 82.7% | 27 | 17.3% | 156 |
| Reversed Before Half | 34 | 18.3% | 152 | 81.7% | 186 |

### Bullish Alignment (170 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 65 | 38.2% | 54 | 83.1% | 0.48% |
| Reversed Before Half | 105 | 61.8% | 19 | 18.1% | -0.45% |

### Bearish Alignment (172 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 91 | 52.9% | 75 | 82.4% | -0.34% |
| Reversed Before Half | 81 | 47.1% | 15 | 18.5% | 0.36% |

### VIX Exhaustion by VIX Regime

| VIX Regime | Total | Exceeded Half | % | Reversed Before Half | % |
|------------|------:|--------------:|--:|---------------------:|--:|
| Low (<15) | 245 | 118 | 48.2% | 127 | 51.8% |
| Normal (15-20) | 81 | 30 | 37.0% | 51 | 63.0% |
| Elevated (20-30) | 16 | 8 | 50.0% | 8 | 50.0% |
| High (>30) | 0 | 0 | - | 0 | - |

## Strong Alignment Analysis

Strong alignment = both FII and PRO have Bullish/Strong Bullish or Bearish/Strong Bearish
(excluding Mildly variants).

| Category | Total | Worked then Reversed | % | Against then Recovered | % |
|----------|------:|---------------------:|--:|-----------------------:|--:|
| Strong Bullish | 122 | 68 | 55.7% | 54 | 44.3% |
| Strong Bearish | 116 | 52 | 44.8% | 64 | 55.2% |
| All Strong Aligned | 238 | 120 | 50.4% | 118 | 49.6% |

## Mixed Days: When FII and PRO Oppose Each Other

When FII and PRO have opposing directional views (one bullish, one bearish),
whose view wins by close?

### Overview (82 mixed days)

| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |
|----------|-----:|----------:|----------:|----------------:|-----------:|
| FII Bullish + PRO Bearish | 49 | 26 (53.1%) | 23 (46.9%) | -0.027% | 0.863% |
| FII Bearish + PRO Bullish | 33 | 14 (42.4%) | 19 (57.6%) | 0.235% | 1.11% |
| All Mixed | 82 | 40 (48.8%) | 42 (51.2%) | 0.079% | 0.962% |

### Who Won by Close?

| Sub-Type | Days | FII Correct | FII% | PRO Correct | PRO% |
|----------|-----:|------------:|-----:|------------:|-----:|
| FII Bullish + PRO Bearish | 49 | 23 | 46.9% | 25 | 51.0% |
| FII Bearish + PRO Bullish | 33 | 13 | 39.4% | 19 | 57.6% |

### Mixed Days: Expiry vs Non-Expiry

| Context | Days | Avg Open→Close% | Avg Range% |
|---------|-----:|----------------:|-----------:|
| Expiry | 25 | 0.018% | 0.944% |
| Non-Expiry | 57 | 0.105% | 0.97% |

## Neutral Days: When One or Both Sides Have No View

When one or both participants are Neutral, there is no directional consensus.
Does a solo directional view from one side carry any weight?

### Overview (306 neutral days)

| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |
|----------|-----:|----------:|----------:|----------------:|-----------:|
| Both Neutral | 70 | 34 (48.6%) | 36 (51.4%) | -0.002% | 0.96% |
| FII Neutral + PRO Bullish | 96 | 47 (49.0%) | 49 (51.0%) | -0.007% | 0.83% |
| FII Neutral + PRO Bearish | 94 | 45 (47.9%) | 49 (52.1%) | 0.002% | 0.905% |
| FII Bullish + PRO Neutral | 21 | 13 (61.9%) | 8 (38.1%) | -0.14% | 0.891% |
| FII Bearish + PRO Neutral | 25 | 14 (56.0%) | 11 (44.0%) | -0.18% | 1.092% |
| All Neutral/Unclear | 306 | 153 (50.0%) | 153 (50.0%) | -0.026% | 0.908% |

### Solo View Accuracy: Did the One Directional Side Win?

| Sub-Type | Days | View Correct | % | Avg Open→Close% |
|----------|-----:|-------------:|--:|----------------:|
| FII Neutral + PRO Bullish | 96 | 49 | 51.0% | -0.007% |
| FII Neutral + PRO Bearish | 94 | 44 | 46.8% | 0.002% |
| FII Bullish + PRO Neutral | 21 | 8 | 38.1% | -0.14% |
| FII Bearish + PRO Neutral | 25 | 14 | 56.0% | -0.18% |

### Range Comparison: Aligned vs Mixed vs Neutral

| Category | Days | Avg Range% | Avg High% | Avg Low% |
|----------|-----:|-----------:|----------:|---------:|
| Aligned | 342 | 0.953% | 0.423% | -0.529% |
| Mixed | 82 | 0.962% | 0.501% | -0.46% |
| Neutral/Unclear | 306 | 0.908% | 0.425% | -0.483% |

## Expiry vs Non-Expiry

| Context | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg High% | Avg Low% |
|---------|-------------:|---------------------:|--:|-----------------------:|--:|----------:|---------:|
| Expiry Days | 68 | 29 | 42.6% | 39 | 57.4% | 0.45% | -0.55% |
| Non-Expiry Days | 274 | 148 | 54.0% | 126 | 46.0% | 0.42% | -0.52% |

## VIX Regime Analysis

| VIX Regime | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg Range% |
|------------|-------------:|---------------------:|--:|-----------------------:|--:|-----------:|
| Low (<15) | 245 | 117 | 47.8% | 128 | 52.2% | 0.86% |
| Normal (15-20) | 81 | 54 | 66.7% | 27 | 33.3% | 1.04% |
| Elevated (20-30) | 16 | 6 | 37.5% | 10 | 62.5% | 1.86% |
| High (>30) | 0 | 0 | - | 0 | - | - |

## Year-over-Year Trends

| Year | Trading Days | Aligned Days | Alignment% | Bullish Aligned | Bearish Aligned | Worked then Reversed | Reversal% |
|------|------------:|-------------:|-----------:|----------------:|----------------:|---------------------:|----------:|
| 2023 | 75 | 38 | 50.7% | 21 | 17 | 14 | 36.8% |
| 2024 | 244 | 127 | 52.0% | 64 | 63 | 74 | 58.3% |
| 2025 | 245 | 102 | 41.6% | 49 | 53 | 47 | 46.1% |
| 2026 | 166 | 75 | 45.2% | 36 | 39 | 42 | 56.0% |

## Detailed: Bullish Alignment Days

When FII+PRO both lean bullish:

- **Top to Down** (Worked then Reversed): Market rose in first half (aligned), then sold off
- **Down to Up** (Against then Recovered): Market fell in first half (against view), then recovered

| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |
|---------|------:|--:|-------------------:|-------------------:|-----------------:|
| Worked then Reversed (Top→Down) | 97 | 57.1% | 0.16% | -0.8% | -0.55% |
| Against then Recovered (Down→Up) | 73 | 42.9% | 0.68% | -0.25% | 0.51% |

## Detailed: Bearish Alignment Days

When FII+PRO both lean bearish:

- **Down to Up** (Worked then Reversed): Market fell in first half (aligned), then recovered
- **Top to Down** (Against then Recovered): Market rose in first half (against view), then sold off

| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |
|---------|------:|--:|-------------------:|-------------------:|-----------------:|
| Worked then Reversed (Down→Up) | 80 | 46.5% | 0.74% | -0.26% | 0.51% |
| Against then Recovered (Top→Down) | 92 | 53.5% | 0.22% | -0.7% | -0.46% |

## Key Findings

1. **Alignment frequency**: FII and PRO aligned on 342 of 730 days (46.8%). Bullish alignment (170) vs Bearish alignment (172).

2. **Reversal is the dominant pattern**: On alignment days, "Worked then Reversed" occurred 51.8% of the time (177/342 days). This means when institutions agree, the first half tends to move in their direction but the second half reverses.

3. **Worked and Remained (close validated view)**: On 47.7% of alignment days (163/342), the market closed in the aligned direction — meaning the institutional consensus was ultimately correct by end of day. The remaining 52.3% closed against the aligned view.

4. **VIX half-range exhaustion**: 45.6% of alignment days exceeded half the VIX-predicted range in the aligned direction (156/342). Among those, 82.7% closed in the aligned direction (Worked and Remained) vs 18.3% for days that reversed before reaching half range. Exceeding half range predicts a better close outcome.

5. **Bullish vs Bearish reversal**: Bullish alignment reversal rate = 57.1%, Bearish alignment reversal rate = 46.5%. Bullish alignment shows a higher tendency to reverse in the second half.

6. **Expiry effect**: Reversal rate on expiry days = 42.6% vs non-expiry = 54.0%. Non-expiry days show higher reversal tendency.

7. **Strong alignment signal**: When both have strong views (excluding Mildly), reversal rate = 50.4% (120/238 days). Stronger conviction shows lower reversal tendency.

8. **Mixed days (opposing views)**: 82 days where FII and PRO disagreed. When FII was bullish and PRO bearish (49 days), it was a coin flip (50/50). When FII was bearish and PRO bullish (33 days), PRO's bullish view won 57.6% of the time — PRO tends to be more reliable when they disagree.

9. **Neutral days (no consensus)**: 306 days (54.6%) where one or both sides had no view — a perfect coin flip overall (50/50 direction split). However, when FII alone has a view and PRO is neutral, FII's solo signal is reliable: bullish correct 38.1% (21 days), bearish correct 56.0% (25 days). PRO's solo view shows no edge. Neutral days also have the widest avg range (0.91%) — institutional indecision means unpredictable volatility.

## Trading Implications

- When FII and PRO align, the first-half move in their direction is not reliable for holding through the full session
- Consider booking profits in the first half if positioned in the direction of institutional alignment
- The second-half reversal pattern suggests mean-reversion trades may be viable after the initial directional move
- Expiry days and high-VIX regimes may amplify or dampen these patterns — check the breakdowns above
- **This is retrospective analysis using T+1 data** — use as a framework for understanding institutional behavior, not as a standalone entry signal

## Last 6 Years: All Examples

*2023-09-11 to 2026-09-09 (730 trading days)*

### Worked then Reversed (first half aligned, second half reversed)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-09-07 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 0.64% | 0.03% | -0.61% | -0.44% |
| 2026-09-02 | Strong Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.54% | 0.24% | -0.3% | 0.24% |
| 2026-08-31 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 0.56% | 0.05% | -0.51% | -0.15% |
| 2026-08-26 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.58% | 0.7% | 0.15% | -0.55% | -0.55% |
| 2026-08-25 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.91% | 0.66% | -0.25% | 0.66% |
| 2026-08-10 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.45% | 0.16% | -0.29% | 0.01% |
| 2026-08-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 1.12% | 0.0% | -1.12% | -0.36% |
| 2026-07-09 | Strong Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.87% | 0.86% | -0.01% | 0.22% |
| 2026-07-07 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.74% | 0.27% | -0.47% | -0.45% |
| 2026-07-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.52% | 0.01% | -0.51% | -0.43% |
| 2026-06-25 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.7% | 0.92% | 0.56% | -0.36% | -0.3% |
| 2026-06-16 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.48% | 0.33% | -0.15% | 0.3% |
| 2026-06-15 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.81% | 0.11% | -0.7% | -0.53% |
| 2026-06-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 1.41% | 1.41% | 0.0% | 1.27% |
| 2026-05-27 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.52% | 0.43% | -0.09% | 0.17% |
| 2026-05-22 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.93% | 0.7% | 0.69% | -0.0% | 0.33% |
| 2026-05-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 0.82% | 0.45% | -0.37% | -0.29% |
| 2026-05-15 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.97% | 0.96% | 0.45% | -0.51% | -0.3% |
| 2026-05-13 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 1.37% | 0.94% | -0.43% | 0.28% |
| 2026-05-07 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 0.81% | 0.34% | -0.47% | -0.25% |
| 2026-05-04 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.97% | 1.19% | 0.94% | -0.24% | 0.25% |
| 2026-04-28 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.96% | 0.93% | 0.55% | -0.39% | -0.14% |
| 2026-04-22 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.92% | 0.67% | 0.18% | -0.48% | -0.42% |
| 2026-04-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 0.98% | 0.37% | -0.62% | -0.25% |
| 2026-04-17 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 1.14% | 0.85% | -0.29% | 0.83% |
| 2026-04-10 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.07% | 0.91% | 0.81% | -0.1% | 0.71% |
| 2026-04-09 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 1.29% | 0.34% | -0.95% | -0.6% |
| 2026-03-27 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.29% | 1.65% | 0.05% | -1.59% | -1.44% |
| 2026-03-20 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.19% | 1.2% | 1.02% | -0.18% | 0.11% |
| 2026-03-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.04% | 1.59% | 0.88% | -0.71% | 0.58% |
| 2026-03-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 1.56% | 1.34% | -0.23% | 0.77% |
| 2026-02-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.12% | 1.01% | -0.11% | 0.63% |
| 2026-02-19 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 1.92% | 0.05% | -1.87% | -1.77% |
| 2026-02-16 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.28% | 1.08% | -0.2% | 1.02% |
| 2026-02-11 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.42% | 0.05% | -0.38% | -0.2% |
| 2026-02-06 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.64% | 0.83% | 0.38% | -0.44% | 0.26% |
| 2026-02-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.69% | 0.01% | -0.68% | -0.44% |
| 2026-02-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.79% | 1.73% | 1.26% | -0.47% | 1.14% |
| 2026-01-21 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.67% | 1.52% | 0.64% | -0.88% | 0.11% |
| 2026-01-13 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 1.14% | 0.01% | -1.14% | -0.71% |
| 2026-01-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.49% | 0.62% | 0.15% | -0.47% | -0.34% |
| 2026-01-01 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.51% | 0.32% | 0.09% | -0.23% | -0.13% |
| 2025-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.51% | 0.44% | 0.11% | -0.33% | -0.15% |
| 2025-12-10 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.57% | 0.82% | 0.32% | -0.5% | -0.47% |
| 2025-12-08 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 1.1% | 0.07% | -1.02% | -0.87% |
| 2025-11-27 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.64% | 0.19% | -0.45% | -0.16% |
| 2025-11-19 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.84% | 0.6% | -0.24% | 0.52% |
| 2025-11-18 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.59% | 0.03% | -0.56% | -0.49% |
| 2025-11-17 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.45% | 0.29% | -0.16% | 0.25% |
| 2025-11-14 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.77% | 0.67% | -0.11% | 0.58% |
| 2025-11-13 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.63% | 0.78% | 0.4% | -0.38% | -0.08% |
| 2025-10-30 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.72% | 0.18% | -0.54% | -0.36% |
| 2025-10-09 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 0.7% | 0.5% | -0.2% | 0.38% |
| 2025-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 0.76% | 0.75% | -0.01% | 0.72% |
| 2025-09-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 1.09% | 0.0% | -1.09% | -0.96% |
| 2025-09-02 | Strong Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.59% | 0.95% | 0.42% | -0.53% | -0.32% |
| 2025-08-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.92% | 0.08% | -0.84% | -0.76% |
| 2025-08-25 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.51% | 0.29% | -0.22% | 0.12% |
| 2025-08-13 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.53% | 0.32% | -0.21% | 0.18% |
| 2025-08-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.64% | 0.96% | 0.57% | -0.4% | -0.32% |
| 2025-08-11 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 1.04% | 0.94% | -0.1% | 0.78% |
| 2025-08-07 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.63% | 1.19% | 0.69% | -0.49% | 0.66% |
| 2025-08-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.58% | 0.05% | -0.53% | -0.29% |
| 2025-08-04 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.74% | 0.57% | -0.17% | 0.53% |
| 2025-07-30 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.52% | 0.05% | -0.48% | -0.18% |
| 2025-07-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.55% | 0.9% | 0.01% | -0.89% | -0.76% |
| 2025-07-23 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 0.59% | 0.37% | -0.21% | 0.28% |
| 2025-07-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.58% | 0.06% | -0.52% | -0.4% |
| 2025-06-13 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.15% | 1.15% | 0.0% | 1.07% |
| 2025-06-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.33% | 0.0% | -0.33% | -0.23% |
| 2025-05-23 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 1.2% | 1.09% | -0.1% | 0.83% |
| 2025-05-14 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 0.94% | 0.62% | -0.32% | 0.29% |
| 2025-05-07 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.99% | 0.95% | 0.89% | -0.05% | 0.73% |
| 2025-05-06 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 0.73% | 0.04% | -0.69% | -0.67% |
| 2025-05-05 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 0.51% | 0.44% | -0.08% | 0.16% |
| 2025-04-29 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.68% | 0.36% | -0.33% | -0.19% |
| 2025-04-15 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.69% | 0.0% | -0.69% | -0.1% |
| 2025-04-07 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 2.35% | 2.28% | -0.07% | 2.2% |
| 2025-04-02 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.83% | 0.68% | -0.15% | 0.6% |
| 2025-02-28 | Strong Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.54% | 0.08% | -1.46% | -1.36% |
| 2025-02-25 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.76% | 0.49% | 0.48% | -0.01% | 0.04% |
| 2025-02-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.53% | 0.02% | -0.51% | -0.48% |
| 2025-02-04 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 1.44% | 1.08% | -0.37% | 0.84% |
| 2025-01-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 1.16% | 1.07% | -0.08% | 1.02% |
| 2025-01-24 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.87% | 1.28% | 0.7% | -0.58% | -0.4% |
| 2025-01-21 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.86% | 1.92% | 0.02% | -1.9% | -1.57% |
| 2025-01-15 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 0.63% | 0.19% | -0.45% | -0.1% |
| 2025-01-14 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.56% | 0.43% | -0.14% | 0.18% |
| 2025-01-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.91% | 0.0% | -0.91% | -0.85% |
| 2024-12-26 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 0.84% | 0.33% | -0.51% | -0.07% |
| 2024-12-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.71% | 0.77% | 0.41% | -0.35% | -0.16% |
| 2024-12-23 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.79% | 0.94% | 0.55% | -0.38% | 0.04% |
| 2024-12-19 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.56% | 0.54% | -0.03% | 0.36% |
| 2024-12-16 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 0.73% | 0.11% | -0.61% | -0.42% |
| 2024-12-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.84% | 0.34% | -0.5% | -0.11% |
| 2024-11-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 1.09% | 1.09% | 0.0% | 0.82% |
| 2024-11-27 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.86% | 0.62% | -0.24% | 0.3% |
| 2024-11-26 | Strong Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.9% | 0.0% | -0.9% | -0.62% |
| 2024-11-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.89% | 0.4% | -0.49% | -0.01% |
| 2024-11-19 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.79% | 1.34% | 1.07% | -0.28% | -0.26% |
| 2024-11-18 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 1.09% | 0.01% | -1.08% | -0.59% |
| 2024-11-04 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 2.06% | 0.0% | -2.05% | -1.34% |
| 2024-10-28 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.77% | 1.47% | 1.0% | -0.48% | 0.48% |
| 2024-10-25 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.5% | 0.09% | -1.41% | -0.84% |
| 2024-10-23 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.93% | 0.93% | -0.0% | 0.24% |
| 2024-10-21 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 1.2% | 0.09% | -1.11% | -0.87% |
| 2024-10-18 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.7% | 1.29% | 0.9% | -0.39% | 0.8% |
| 2024-10-15 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 0.81% | 0.1% | -0.71% | -0.48% |
| 2024-10-11 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.43% | 0.17% | -0.26% | -0.04% |
| 2024-10-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.79% | 1.16% | 0.85% | -0.3% | 0.83% |
| 2024-10-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.67% | 0.65% | 0.46% | -0.19% | 0.09% |
| 2024-09-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 0.62% | 0.51% | -0.11% | 0.44% |
| 2024-09-17 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.65% | 0.35% | 0.1% | -0.25% | -0.04% |
| 2024-09-12 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.71% | 1.96% | 1.49% | -0.47% | 1.02% |
| 2024-09-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.82% | 0.54% | -0.28% | 0.48% |
| 2024-09-02 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 0.39% | 0.0% | -0.39% | -0.24% |
| 2024-08-28 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.66% | 0.39% | -0.26% | 0.06% |
| 2024-08-26 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.68% | 0.55% | -0.13% | 0.42% |
| 2024-08-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.52% | 0.35% | -0.17% | 0.1% |
| 2024-08-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.47% | 0.01% | -0.46% | -0.23% |
| 2024-08-13 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 1.0% | 0.07% | -0.93% | -0.83% |
| 2024-08-07 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.98% | 0.63% | 0.2% | -0.43% | 0.11% |
| 2024-07-29 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.9% | 0.23% | -0.68% | -0.41% |
| 2024-07-23 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 2.07% | 0.06% | -2.01% | -0.38% |
| 2024-07-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.78% | 0.95% | 0.61% | -0.34% | 0.29% |
| 2024-07-19 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.76% | 1.39% | 0.0% | -1.39% | -1.32% |
| 2024-07-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.3% | 0.18% | -0.11% | -0.06% |
| 2024-07-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 0.49% | 0.13% | -0.36% | -0.27% |
| 2024-06-24 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 0.89% | 0.75% | -0.14% | 0.71% |
| 2024-06-21 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.14% | 0.03% | -1.11% | -0.88% |
| 2024-06-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.54% | 0.0% | -0.54% | -0.35% |
| 2024-06-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.77% | 0.63% | 0.42% | -0.21% | -0.15% |
| 2024-06-10 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.88% | 0.79% | 0.4% | -0.39% | -0.36% |
| 2024-06-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 1.4% | 3.97% | 2.45% | -1.52% | 2.01% |
| 2024-06-04 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.1% | 8.19% | 0.0% | -8.19% | -5.1% |
| 2024-05-18 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.04% | 0.22% | 0.03% | -0.19% | -0.03% |
| 2024-05-10 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 0.82% | 0.64% | -0.18% | 0.29% |
| 2024-05-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 1.69% | 0.37% | -1.32% | -1.15% |
| 2024-05-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.83% | 0.62% | -0.21% | 0.34% |
| 2024-04-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.64% | 0.95% | 0.46% | -0.49% | -0.41% |
| 2024-04-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 0.95% | 0.8% | -0.15% | 0.7% |
| 2024-04-26 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 1.04% | 0.0% | -1.04% | -0.75% |
| 2024-04-23 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.44% | 0.0% | -0.43% | -0.38% |
| 2024-04-19 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.68% | 1.84% | 1.45% | -0.38% | 1.32% |
| 2024-04-16 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.65% | 0.61% | 0.4% | -0.21% | 0.24% |
| 2024-04-03 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.78% | 0.6% | -0.18% | 0.27% |
| 2024-03-20 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.74% | 1.01% | 0.4% | -0.61% | 0.05% |
| 2024-03-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.84% | 0.15% | -0.7% | -0.62% |
| 2024-03-14 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.76% | 1.31% | 1.01% | -0.3% | 0.78% |
| 2024-03-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 2.41% | 0.06% | -2.35% | -2.01% |
| 2024-02-29 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.91% | 0.57% | -0.34% | 0.49% |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.81% | 0.73% | 0.22% | -0.51% | 0.09% |
| 2024-02-13 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.84% | 1.03% | 0.47% | -0.56% | 0.29% |
| 2024-02-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 1.18% | 0.14% | -1.04% | -0.86% |
| 2024-02-09 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.83% | 0.8% | 0.36% | -0.45% | 0.27% |
| 2024-02-07 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.88% | 0.04% | -0.84% | -0.43% |
| 2024-02-06 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.98% | 0.58% | -0.4% | 0.52% |
| 2024-02-01 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.8% | 0.24% | -0.56% | -0.41% |
| 2024-01-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.36% | 1.18% | -0.18% | 1.03% |
| 2024-01-30 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 1.43% | 0.17% | -1.26% | -1.13% |
| 2024-01-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.99% | 0.02% | -0.97% | -0.39% |
| 2024-01-18 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Exceeded Half then Reversed | 0.79% | 1.19% | 0.58% | -0.6% | 0.29% |
| 2024-01-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.7% | 0.2% | -0.5% | -0.22% |
| 2023-12-26 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.69% | 0.52% | -0.17% | 0.42% |
| 2023-12-20 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 2.35% | 0.23% | -2.12% | -2.05% |
| 2023-12-01 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.53% | 0.48% | -0.05% | 0.31% |
| 2023-11-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.41% | 0.04% | -0.37% | -0.24% |
| 2023-11-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.58% | 0.19% | 0.0% | -0.19% | -0.13% |
| 2023-10-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 0.56% | 0.25% | -0.3% | -0.21% |
| 2023-10-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.73% | 0.0% | -0.73% | -0.51% |
| 2023-09-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.67% | 0.89% | 0.74% | -0.15% | 0.29% |
| 2023-09-28 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 1.39% | 0.02% | -1.36% | -1.06% |
| 2023-09-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 0.31% | 0.08% | -0.23% | -0.05% |
| 2023-09-18 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 0.38% | 0.2% | -0.19% | -0.16% |
| 2023-09-15 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.46% | 0.33% | -0.13% | 0.06% |
| 2023-09-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.61% | 0.2% | -0.41% | -0.13% |
| 2023-09-12 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.97% | 0.0% | -0.97% | -0.62% |

### Against then Recovered (first half against view, second half recovered)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-27 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.85% | 0.08% | -0.77% | -0.77% |
| 2026-08-19 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.6% | 0.61% | 0.09% | -0.52% | -0.31% |
| 2026-08-12 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.62% | 0.85% | 0.0% | -0.84% | -0.15% |
| 2026-08-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.44% | 0.37% | -0.07% | 0.13% |
| 2026-08-05 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.73% | 0.03% | -0.69% | -0.18% |
| 2026-07-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.63% | 0.64% | 0.39% | -0.26% | 0.19% |
| 2026-07-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.73% | 0.5% | 0.35% | -0.15% | 0.31% |
| 2026-07-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.85% | 0.07% | -0.78% | -0.66% |
| 2026-07-21 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.68% | 0.52% | 0.19% | -0.33% | -0.09% |
| 2026-07-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.69% | 0.54% | 0.31% | -0.22% | 0.2% |
| 2026-07-15 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.72% | 0.87% | 0.56% | -0.31% | -0.05% |
| 2026-07-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 1.08% | 0.92% | -0.16% | 0.71% |
| 2026-07-10 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.45% | 0.43% | -0.02% | 0.36% |
| 2026-06-22 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.68% | 0.39% | 0.25% | -0.14% | -0.08% |
| 2026-06-09 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 0.75% | 0.09% | -0.66% | -0.01% |
| 2026-05-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 0.55% | 0.48% | -0.07% | 0.46% |
| 2026-05-12 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.97% | 1.72% | 0.15% | -1.58% | -1.23% |
| 2026-05-08 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.87% | 0.52% | 0.08% | -0.44% | -0.22% |
| 2026-04-24 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.97% | 1.63% | 0.44% | -1.19% | -0.82% |
| 2026-04-23 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.96% | 0.72% | 0.45% | -0.28% | -0.19% |
| 2026-04-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.99% | 1.49% | 1.35% | -0.14% | 0.97% |
| 2026-04-06 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.34% | 2.0% | 0.96% | -1.04% | 0.79% |
| 2026-03-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.4% | 1.91% | 0.73% | -1.18% | -0.76% |
| 2026-03-18 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.04% | 1.03% | 0.97% | -0.06% | 0.56% |
| 2026-03-12 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 1.1% | 1.17% | 0.67% | -0.5% | -0.15% |
| 2026-03-10 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.22% | 0.92% | 0.09% | -0.83% | 0.02% |
| 2026-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 1.23% | 0.0% | -1.23% | -0.71% |
| 2026-02-23 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.75% | 0.63% | 0.36% | -0.27% | 0.1% |
| 2026-02-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.76% | 0.49% | -0.26% | 0.3% |
| 2026-02-13 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.61% | 0.73% | 0.23% | -0.5% | -0.43% |
| 2026-02-04 | Strong Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.99% | 0.56% | -0.43% | 0.24% |
| 2026-02-01 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 3.43% | 0.42% | -3.01% | -2.23% |
| 2026-01-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 1.23% | 0.39% | -0.84% | -0.53% |
| 2025-12-31 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.51% | 0.84% | 0.84% | -0.01% | 0.66% |
| 2025-12-29 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.48% | 0.72% | 0.17% | -0.55% | -0.44% |
| 2025-12-26 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.48% | 0.52% | 0.09% | -0.43% | -0.28% |
| 2025-12-22 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.5% | 0.51% | 0.48% | -0.03% | 0.41% |
| 2025-12-17 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.53% | 0.61% | 0.1% | -0.51% | -0.31% |
| 2025-12-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 0.46% | 0.33% | -0.13% | 0.28% |
| 2025-12-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.76% | 0.22% | -0.54% | -0.1% |
| 2025-12-01 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.61% | 0.77% | 0.0% | -0.77% | -0.57% |
| 2025-11-28 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.62% | 0.41% | 0.17% | -0.25% | -0.13% |
| 2025-11-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 1.44% | 1.44% | 0.0% | 1.4% |
| 2025-11-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.67% | 0.13% | -0.54% | -0.53% |
| 2025-11-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 0.88% | 0.08% | -0.81% | -0.69% |
| 2025-11-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.63% | 0.7% | 0.44% | -0.26% | 0.25% |
| 2025-11-06 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.73% | 0.34% | -0.4% | -0.29% |
| 2025-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.63% | 0.94% | 0.35% | -0.59% | -0.51% |
| 2025-10-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 0.98% | 0.91% | -0.07% | 0.67% |
| 2025-10-14 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.99% | 0.13% | -0.86% | -0.61% |
| 2025-10-10 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.53% | 0.69% | 0.65% | -0.04% | 0.44% |
| 2025-10-03 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 0.64% | 0.59% | -0.05% | 0.55% |
| 2025-09-26 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.96% | 0.2% | -0.76% | -0.59% |
| 2025-09-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 0.86% | 0.23% | -0.62% | -0.52% |
| 2025-09-23 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 0.7% | 0.21% | -0.49% | -0.09% |
| 2025-09-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 0.28% | 0.28% | -0.0% | 0.21% |
| 2025-09-05 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 0.85% | 0.05% | -0.79% | -0.3% |
| 2025-08-28 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.9% | 0.03% | -0.87% | -0.66% |
| 2025-08-18 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 0.68% | 0.34% | -0.34% | -0.22% |
| 2025-08-14 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.64% | 0.31% | 0.27% | -0.04% | 0.04% |
| 2025-08-06 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.61% | 0.54% | 0.12% | -0.41% | -0.29% |
| 2025-07-28 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.59% | 0.98% | 0.43% | -0.55% | -0.44% |
| 2025-07-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.82% | 0.0% | -0.82% | -0.71% |
| 2025-07-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.62% | 0.59% | 0.01% | -0.59% | -0.25% |
| 2025-07-03 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 0.8% | 0.32% | -0.47% | -0.42% |
| 2025-07-02 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.9% | 0.08% | -0.82% | -0.57% |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 1.21% | 1.17% | -0.04% | 1.03% |
| 2025-06-24 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 1.26% | 0.55% | -0.72% | -0.43% |
| 2025-06-05 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.16% | 0.85% | -0.32% | 0.28% |
| 2025-05-28 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.97% | 0.51% | 0.13% | -0.38% | -0.3% |
| 2025-05-26 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.9% | 0.72% | 0.64% | -0.08% | 0.31% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.9% | 2.52% | 1.71% | -0.81% | 1.38% |
| 2025-04-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.81% | 0.22% | -0.59% | -0.39% |
| 2025-04-16 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.77% | 0.46% | -0.3% | 0.38% |
| 2025-04-03 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.69% | 0.67% | -0.02% | 0.39% |
| 2025-03-26 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 1.2% | 0.15% | -1.05% | -1.0% |
| 2025-03-24 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 1.17% | 0.82% | -0.35% | 0.68% |
| 2025-03-19 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.69% | 0.58% | 0.29% | -0.29% | 0.16% |
| 2025-03-18 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 1.14% | 0.86% | -0.28% | 0.82% |
| 2025-03-06 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.72% | 1.38% | 0.36% | -1.03% | 0.24% |
| 2025-02-07 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 1.06% | 0.19% | -0.87% | -0.37% |
| 2025-01-30 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.79% | 0.66% | -0.13% | 0.55% |
| 2025-01-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.95% | 0.9% | 0.68% | -0.22% | 0.65% |
| 2025-01-23 | Strong Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 0.78% | 0.62% | -0.16% | 0.38% |
| 2025-01-13 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 1.27% | 0.63% | -0.64% | -0.46% |
| 2025-01-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.79% | 0.06% | -0.73% | -0.5% |
| 2025-01-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 2.24% | 0.18% | -2.05% | -1.73% |
| 2025-01-02 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 2.0% | 1.87% | -0.13% | 1.62% |
| 2024-12-18 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 1.01% | 0.4% | -0.61% | -0.34% |
| 2024-12-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.3% | 0.16% | -1.14% | -1.08% |
| 2024-12-10 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 0.68% | 0.1% | -0.58% | -0.13% |
| 2024-12-02 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 1.21% | 0.67% | -0.55% | 0.56% |
| 2024-11-13 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 1.53% | 0.21% | -1.31% | -0.92% |
| 2024-11-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.87% | 0.28% | -0.58% | -0.4% |
| 2024-11-07 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 1.32% | 0.06% | -1.27% | -1.2% |
| 2024-11-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 1.37% | 0.94% | -0.43% | 0.76% |
| 2024-11-01 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.81% | 0.36% | 0.27% | -0.09% | -0.01% |
| 2024-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 0.82% | 0.09% | -0.73% | -0.46% |
| 2024-10-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 1.41% | 0.64% | -0.77% | 0.51% |
| 2024-10-24 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.77% | 0.57% | 0.28% | -0.29% | 0.01% |
| 2024-10-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 1.76% | 0.34% | -1.42% | -1.28% |
| 2024-10-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 1.2% | 0.01% | -1.19% | -1.11% |
| 2024-10-16 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.74% | 0.34% | -0.4% | -0.19% |
| 2024-10-04 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 2.06% | 1.2% | -0.85% | -0.53% |
| 2024-09-23 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.67% | 0.42% | 0.32% | -0.1% | 0.22% |
| 2024-09-16 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.66% | 0.43% | 0.15% | -0.28% | -0.12% |
| 2024-09-10 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.93% | 0.52% | -0.41% | 0.21% |
| 2024-09-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.74% | 0.34% | 0.03% | -0.31% | -0.18% |
| 2024-08-21 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.54% | 0.44% | -0.11% | 0.41% |
| 2024-08-14 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.85% | 0.4% | 0.05% | -0.35% | -0.16% |
| 2024-08-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.8% | 1.07% | 0.63% | -0.44% | 0.12% |
| 2024-08-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.87% | 0.45% | 0.13% | -0.31% | -0.09% |
| 2024-08-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 1.75% | 0.8% | -0.95% | -0.65% |
| 2024-08-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 1.88% | 0.19% | -1.68% | -1.03% |
| 2024-07-26 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 1.84% | 1.79% | -0.05% | 1.75% |
| 2024-07-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.81% | 0.24% | -0.56% | -0.01% |
| 2024-07-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.07% | 0.84% | -0.23% | 0.51% |
| 2024-07-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.86% | 0.03% | -0.83% | -0.24% |
| 2024-06-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 0.81% | 0.75% | -0.06% | 0.61% |
| 2024-06-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 2.33% | 2.18% | -0.14% | 1.96% |
| 2024-06-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.99% | 1.17% | 0.49% | -0.68% | 0.22% |
| 2024-05-30 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.27% | 1.28% | 0.39% | -0.89% | -0.27% |
| 2024-05-24 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 1.12% | 0.52% | 0.42% | -0.1% | 0.09% |
| 2024-05-23 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.12% | 1.84% | 1.68% | -0.16% | 1.49% |
| 2024-05-21 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 0.83% | 0.83% | 0.0% | 0.46% |
| 2024-05-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.08% | 0.85% | 0.65% | -0.2% | 0.44% |
| 2024-05-06 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.77% | 0.79% | 0.12% | -0.67% | -0.46% |
| 2024-04-25 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 1.44% | 1.38% | -0.05% | 1.09% |
| 2024-04-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.53% | 0.41% | 0.24% | -0.17% | -0.04% |
| 2024-04-15 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.6% | 0.75% | 0.4% | -0.36% | -0.28% |
| 2024-04-05 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.59% | 0.49% | 0.23% | -0.26% | 0.16% |
| 2024-03-12 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Reversed by Close | Reversed Before Half | 0.73% | 0.88% | 0.53% | -0.35% | -0.0% |
| 2024-03-01 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.39% | 1.38% | -0.0% | 1.26% |
| 2024-02-26 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.57% | 0.15% | -0.42% | -0.23% |
| 2024-02-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 1.58% | 1.36% | -0.22% | 1.25% |
| 2024-01-15 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.69% | 0.69% | 0.28% | -0.41% | 0.26% |
| 2024-01-09 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.95% | 0.33% | -0.63% | -0.47% |
| 2024-01-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 1.25% | 0.08% | -1.17% | -1.09% |
| 2024-01-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.7% | 0.55% | 0.2% | -0.35% | 0.02% |
| 2024-01-04 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.74% | 0.56% | 0.37% | -0.19% | 0.3% |
| 2024-01-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.82% | 0.07% | -0.74% | -0.63% |
| 2023-12-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.77% | 0.84% | 0.83% | -0.01% | 0.7% |
| 2023-12-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.74% | 0.44% | -0.3% | 0.17% |
| 2023-12-19 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.78% | 0.13% | -0.65% | -0.15% |
| 2023-12-12 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.81% | 0.09% | -0.72% | -0.56% |
| 2023-12-08 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.69% | 0.34% | -0.34% | 0.18% |
| 2023-12-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.52% | 0.05% | -0.47% | -0.07% |
| 2023-12-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.68% | 0.73% | 0.27% | -0.47% | 0.23% |
| 2023-11-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.67% | 0.71% | 0.25% | -0.46% | 0.09% |
| 2023-11-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.74% | 0.64% | -0.1% | 0.6% |
| 2023-11-22 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.64% | 0.62% | 0.21% | -0.41% | 0.13% |
| 2023-11-20 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.62% | 0.44% | 0.13% | -0.31% | -0.19% |
| 2023-11-09 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.44% | 0.03% | -0.41% | -0.27% |
| 2023-11-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Reversed Before Half | 0.58% | 0.49% | 0.1% | -0.39% | 0.07% |
| 2023-11-01 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.62% | 0.64% | 0.17% | -0.47% | -0.39% |
| 2023-10-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 1.15% | 0.55% | -0.6% | 0.5% |
| 2023-10-23 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 1.53% | 0.18% | -1.35% | -1.25% |
| 2023-10-16 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Reversed Before Half | 0.56% | 0.45% | 0.22% | -0.23% | -0.03% |
| 2023-10-11 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.59% | 0.42% | 0.37% | -0.05% | 0.21% |
| 2023-10-04 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Reversed by Close | Exceeded Half then Reversed | 0.62% | 0.64% | 0.06% | -0.58% | -0.0% |
| 2023-09-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.67% | 0.28% | -0.39% | -0.02% |
| 2023-09-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 0.71% | 0.27% | -0.44% | -0.31% |
| 2023-09-21 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.69% | 0.04% | -0.65% | -0.46% |
| 2023-09-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 0.86% | 0.35% | -0.51% | -0.36% |
| 2023-09-11 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.68% | 0.59% | -0.08% | 0.55% |

### Exceeded Half VIX Range + Worked and Remained (129 days — strongest signal, ~85% win rate)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-27 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.85% | 0.08% | -0.77% | -0.77% |
| 2026-08-19 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.6% | 0.61% | 0.09% | -0.52% | -0.31% |
| 2026-08-12 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.62% | 0.85% | 0.0% | -0.84% | -0.15% |
| 2026-08-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.44% | 0.37% | -0.07% | 0.13% |
| 2026-08-05 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.73% | 0.03% | -0.69% | -0.18% |
| 2026-07-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.63% | 0.64% | 0.39% | -0.26% | 0.19% |
| 2026-07-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.85% | 0.07% | -0.78% | -0.66% |
| 2026-07-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 1.08% | 0.92% | -0.16% | 0.71% |
| 2026-07-10 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.45% | 0.43% | -0.02% | 0.36% |
| 2026-06-09 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.89% | 0.75% | 0.09% | -0.66% | -0.01% |
| 2026-05-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.94% | 0.55% | 0.48% | -0.07% | 0.46% |
| 2026-05-12 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.97% | 1.72% | 0.15% | -1.58% | -1.23% |
| 2026-05-08 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.87% | 0.52% | 0.08% | -0.44% | -0.22% |
| 2026-04-24 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.97% | 1.63% | 0.44% | -1.19% | -0.82% |
| 2026-04-13 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.99% | 1.49% | 1.35% | -0.14% | 0.97% |
| 2026-04-06 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.34% | 2.0% | 0.96% | -1.04% | 0.79% |
| 2026-03-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.4% | 1.91% | 0.73% | -1.18% | -0.76% |
| 2026-03-18 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.04% | 1.03% | 0.97% | -0.06% | 0.56% |
| 2026-02-24 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 1.23% | 0.0% | -1.23% | -0.71% |
| 2026-02-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.76% | 0.49% | -0.26% | 0.3% |
| 2026-02-13 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.61% | 0.73% | 0.23% | -0.5% | -0.43% |
| 2026-02-04 | Strong Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.99% | 0.56% | -0.43% | 0.24% |
| 2026-02-01 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 3.43% | 0.42% | -3.01% | -2.23% |
| 2026-01-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 1.23% | 0.39% | -0.84% | -0.53% |
| 2025-12-31 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.51% | 0.84% | 0.84% | -0.01% | 0.66% |
| 2025-12-29 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.48% | 0.72% | 0.17% | -0.55% | -0.44% |
| 2025-12-26 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.48% | 0.52% | 0.09% | -0.43% | -0.28% |
| 2025-12-22 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.5% | 0.51% | 0.48% | -0.03% | 0.41% |
| 2025-12-17 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.53% | 0.61% | 0.1% | -0.51% | -0.31% |
| 2025-12-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 0.46% | 0.33% | -0.13% | 0.28% |
| 2025-12-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.76% | 0.22% | -0.54% | -0.1% |
| 2025-12-01 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.61% | 0.77% | 0.0% | -0.77% | -0.57% |
| 2025-11-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 1.44% | 1.44% | 0.0% | 1.4% |
| 2025-11-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 0.67% | 0.13% | -0.54% | -0.53% |
| 2025-11-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 0.88% | 0.08% | -0.81% | -0.69% |
| 2025-11-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.63% | 0.7% | 0.44% | -0.26% | 0.25% |
| 2025-11-06 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.73% | 0.34% | -0.4% | -0.29% |
| 2025-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.63% | 0.94% | 0.35% | -0.59% | -0.51% |
| 2025-10-16 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 0.98% | 0.91% | -0.07% | 0.67% |
| 2025-10-14 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.99% | 0.13% | -0.86% | -0.61% |
| 2025-10-10 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.53% | 0.69% | 0.65% | -0.04% | 0.44% |
| 2025-10-03 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 0.64% | 0.59% | -0.05% | 0.55% |
| 2025-09-26 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.96% | 0.2% | -0.76% | -0.59% |
| 2025-09-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 0.86% | 0.23% | -0.62% | -0.52% |
| 2025-09-23 | Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.55% | 0.7% | 0.21% | -0.49% | -0.09% |
| 2025-09-17 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 0.28% | 0.28% | -0.0% | 0.21% |
| 2025-09-05 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 0.85% | 0.05% | -0.79% | -0.3% |
| 2025-08-28 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.9% | 0.03% | -0.87% | -0.66% |
| 2025-08-18 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 0.68% | 0.34% | -0.34% | -0.22% |
| 2025-08-06 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.61% | 0.54% | 0.12% | -0.41% | -0.29% |
| 2025-07-28 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.59% | 0.98% | 0.43% | -0.55% | -0.44% |
| 2025-07-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.82% | 0.0% | -0.82% | -0.71% |
| 2025-07-14 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.62% | 0.59% | 0.01% | -0.59% | -0.25% |
| 2025-07-03 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.65% | 0.8% | 0.32% | -0.47% | -0.42% |
| 2025-07-02 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.9% | 0.08% | -0.82% | -0.57% |
| 2025-06-26 | Mildly Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 1.21% | 1.17% | -0.04% | 1.03% |
| 2025-06-24 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 1.26% | 0.55% | -0.72% | -0.43% |
| 2025-06-05 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.16% | 0.85% | -0.32% | 0.28% |
| 2025-05-26 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.9% | 0.72% | 0.64% | -0.08% | 0.31% |
| 2025-05-15 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.9% | 2.52% | 1.71% | -0.81% | 1.38% |
| 2025-04-30 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.91% | 0.81% | 0.22% | -0.59% | -0.39% |
| 2025-04-16 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 0.77% | 0.46% | -0.3% | 0.38% |
| 2025-04-03 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.69% | 0.67% | -0.02% | 0.39% |
| 2025-03-26 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 1.2% | 0.15% | -1.05% | -1.0% |
| 2025-03-24 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 1.17% | 0.82% | -0.35% | 0.68% |
| 2025-03-18 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 1.14% | 0.86% | -0.28% | 0.82% |
| 2025-02-07 | Strong Bearish | Mildly Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 1.06% | 0.19% | -0.87% | -0.37% |
| 2025-01-30 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.98% | 0.79% | 0.66% | -0.13% | 0.55% |
| 2025-01-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.95% | 0.9% | 0.68% | -0.22% | 0.65% |
| 2025-01-23 | Strong Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 0.78% | 0.62% | -0.16% | 0.38% |
| 2025-01-13 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 1.27% | 0.63% | -0.64% | -0.46% |
| 2025-01-09 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.79% | 0.06% | -0.73% | -0.5% |
| 2025-01-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.71% | 2.24% | 0.18% | -2.05% | -1.73% |
| 2025-01-02 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 2.0% | 1.87% | -0.13% | 1.62% |
| 2024-12-18 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 1.01% | 0.4% | -0.61% | -0.34% |
| 2024-12-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.3% | 0.16% | -1.14% | -1.08% |
| 2024-12-10 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 0.68% | 0.1% | -0.58% | -0.13% |
| 2024-12-02 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 1.21% | 0.67% | -0.55% | 0.56% |
| 2024-11-13 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 1.53% | 0.21% | -1.31% | -0.92% |
| 2024-11-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.87% | 0.28% | -0.58% | -0.4% |
| 2024-11-07 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 1.32% | 0.06% | -1.27% | -1.2% |
| 2024-11-06 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.84% | 1.37% | 0.94% | -0.43% | 0.76% |
| 2024-10-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.81% | 0.82% | 0.09% | -0.73% | -0.46% |
| 2024-10-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 1.41% | 0.64% | -0.77% | 0.51% |
| 2024-10-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 1.76% | 0.34% | -1.42% | -1.28% |
| 2024-10-17 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 1.2% | 0.01% | -1.19% | -1.11% |
| 2024-10-16 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.68% | 0.74% | 0.34% | -0.4% | -0.19% |
| 2024-10-04 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.69% | 2.06% | 1.2% | -0.85% | -0.53% |
| 2024-09-10 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 0.93% | 0.52% | -0.41% | 0.21% |
| 2024-08-21 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.54% | 0.44% | -0.11% | 0.41% |
| 2024-08-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.8% | 1.07% | 0.63% | -0.44% | 0.12% |
| 2024-08-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 1.75% | 0.8% | -0.95% | -0.65% |
| 2024-08-05 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.75% | 1.88% | 0.19% | -1.68% | -1.03% |
| 2024-07-26 | Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 1.84% | 1.79% | -0.05% | 1.75% |
| 2024-07-24 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.81% | 0.24% | -0.56% | -0.01% |
| 2024-07-12 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 1.07% | 0.84% | -0.23% | 0.51% |
| 2024-07-11 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.86% | 0.03% | -0.83% | -0.24% |
| 2024-06-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.74% | 0.81% | 0.75% | -0.06% | 0.61% |
| 2024-06-07 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.88% | 2.33% | 2.18% | -0.14% | 1.96% |
| 2024-05-30 | Strong Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.27% | 1.28% | 0.39% | -0.89% | -0.27% |
| 2024-05-23 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.12% | 1.84% | 1.68% | -0.16% | 1.49% |
| 2024-05-21 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.07% | 0.83% | 0.83% | 0.0% | 0.46% |
| 2024-05-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 1.08% | 0.85% | 0.65% | -0.2% | 0.44% |
| 2024-05-06 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.77% | 0.79% | 0.12% | -0.67% | -0.46% |
| 2024-04-25 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.54% | 1.44% | 1.38% | -0.05% | 1.09% |
| 2024-04-15 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.6% | 0.75% | 0.4% | -0.36% | -0.28% |
| 2024-03-01 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.82% | 1.39% | 1.38% | -0.0% | 1.26% |
| 2024-02-26 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.78% | 0.57% | 0.15% | -0.42% | -0.23% |
| 2024-02-14 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.83% | 1.58% | 1.36% | -0.22% | 1.25% |
| 2024-01-09 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.95% | 0.33% | -0.63% | -0.47% |
| 2024-01-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 1.25% | 0.08% | -1.17% | -1.09% |
| 2024-01-03 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.76% | 0.82% | 0.07% | -0.74% | -0.63% |
| 2023-12-27 | Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.77% | 0.84% | 0.83% | -0.01% | 0.7% |
| 2023-12-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.72% | 0.74% | 0.44% | -0.3% | 0.17% |
| 2023-12-19 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.73% | 0.78% | 0.13% | -0.65% | -0.15% |
| 2023-12-12 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.67% | 0.81% | 0.09% | -0.72% | -0.56% |
| 2023-12-08 | Bullish | Mildly Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.66% | 0.69% | 0.34% | -0.34% | 0.18% |
| 2023-12-06 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.7% | 0.52% | 0.05% | -0.47% | -0.07% |
| 2023-11-29 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.64% | 0.74% | 0.64% | -0.1% | 0.6% |
| 2023-11-09 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.44% | 0.03% | -0.41% | -0.27% |
| 2023-11-01 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.62% | 0.64% | 0.17% | -0.47% | -0.39% |
| 2023-10-30 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 1.15% | 0.55% | -0.6% | 0.5% |
| 2023-10-23 | Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 1.53% | 0.18% | -1.35% | -1.25% |
| 2023-10-11 | Strong Bullish | Strong Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.59% | 0.42% | 0.37% | -0.05% | 0.21% |
| 2023-09-25 | Mildly Bearish | Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.67% | 0.28% | -0.39% | -0.02% |
| 2023-09-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 0.71% | 0.27% | -0.44% | -0.31% |
| 2023-09-21 | Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.58% | 0.69% | 0.04% | -0.65% | -0.46% |
| 2023-09-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.57% | 0.86% | 0.35% | -0.51% | -0.36% |
| 2023-09-11 | Mildly Bullish | Bullish | Bullish Alignment | Down to Up | Against then Recovered | Worked and Remained | Exceeded Half then Reversed | 0.56% | 0.68% | 0.59% | -0.08% | 0.55% |

### Reversed Before Half VIX Range + Reversed by Close (152 days — weak alignment, ~76% lose)

| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|
| 2026-09-07 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 0.64% | 0.03% | -0.61% | -0.44% |
| 2026-09-02 | Strong Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.54% | 0.24% | -0.3% | 0.24% |
| 2026-08-31 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 0.56% | 0.05% | -0.51% | -0.15% |
| 2026-08-26 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.58% | 0.7% | 0.15% | -0.55% | -0.55% |
| 2026-08-25 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.91% | 0.66% | -0.25% | 0.66% |
| 2026-08-10 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.45% | 0.16% | -0.29% | 0.01% |
| 2026-08-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 1.12% | 0.0% | -1.12% | -0.36% |
| 2026-07-09 | Strong Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.87% | 0.86% | -0.01% | 0.22% |
| 2026-07-07 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.74% | 0.27% | -0.47% | -0.45% |
| 2026-07-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.52% | 0.01% | -0.51% | -0.43% |
| 2026-06-16 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.48% | 0.33% | -0.15% | 0.3% |
| 2026-06-15 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.81% | 0.11% | -0.7% | -0.53% |
| 2026-06-02 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 1.41% | 1.41% | 0.0% | 1.27% |
| 2026-05-27 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.52% | 0.43% | -0.09% | 0.17% |
| 2026-05-22 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.93% | 0.7% | 0.69% | -0.0% | 0.33% |
| 2026-05-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 0.82% | 0.45% | -0.37% | -0.29% |
| 2026-05-15 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.97% | 0.96% | 0.45% | -0.51% | -0.3% |
| 2026-05-13 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.01% | 1.37% | 0.94% | -0.43% | 0.28% |
| 2026-05-07 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.87% | 0.81% | 0.34% | -0.47% | -0.25% |
| 2026-05-04 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.97% | 1.19% | 0.94% | -0.24% | 0.25% |
| 2026-04-22 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.92% | 0.67% | 0.18% | -0.48% | -0.42% |
| 2026-04-20 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 0.98% | 0.37% | -0.62% | -0.25% |
| 2026-04-17 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 1.14% | 0.85% | -0.29% | 0.83% |
| 2026-04-10 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.07% | 0.91% | 0.81% | -0.1% | 0.71% |
| 2026-04-09 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.03% | 1.29% | 0.34% | -0.95% | -0.6% |
| 2026-03-27 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.29% | 1.65% | 0.05% | -1.59% | -1.44% |
| 2026-03-20 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.19% | 1.2% | 1.02% | -0.18% | 0.11% |
| 2026-03-02 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 1.56% | 1.34% | -0.23% | 0.77% |
| 2026-02-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.12% | 1.01% | -0.11% | 0.63% |
| 2026-02-19 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 1.92% | 0.05% | -1.87% | -1.77% |
| 2026-02-16 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.28% | 1.08% | -0.2% | 1.02% |
| 2026-02-11 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.42% | 0.05% | -0.38% | -0.2% |
| 2026-02-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.69% | 0.01% | -0.68% | -0.44% |
| 2026-01-13 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 1.14% | 0.01% | -1.14% | -0.71% |
| 2026-01-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.49% | 0.62% | 0.15% | -0.47% | -0.34% |
| 2026-01-01 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.51% | 0.32% | 0.09% | -0.23% | -0.13% |
| 2025-12-23 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.51% | 0.44% | 0.11% | -0.33% | -0.15% |
| 2025-12-08 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 1.1% | 0.07% | -1.02% | -0.87% |
| 2025-11-27 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.64% | 0.19% | -0.45% | -0.16% |
| 2025-11-19 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.84% | 0.6% | -0.24% | 0.52% |
| 2025-11-18 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.59% | 0.03% | -0.56% | -0.49% |
| 2025-11-17 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.45% | 0.29% | -0.16% | 0.25% |
| 2025-11-14 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.77% | 0.67% | -0.11% | 0.58% |
| 2025-10-30 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.72% | 0.18% | -0.54% | -0.36% |
| 2025-10-09 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 0.7% | 0.5% | -0.2% | 0.38% |
| 2025-09-16 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 0.76% | 0.75% | -0.01% | 0.72% |
| 2025-09-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 1.09% | 0.0% | -1.09% | -0.96% |
| 2025-08-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.92% | 0.08% | -0.84% | -0.76% |
| 2025-08-25 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.51% | 0.29% | -0.22% | 0.12% |
| 2025-08-13 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.53% | 0.32% | -0.21% | 0.18% |
| 2025-08-11 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 1.04% | 0.94% | -0.1% | 0.78% |
| 2025-08-05 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.58% | 0.05% | -0.53% | -0.29% |
| 2025-08-04 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.63% | 0.74% | 0.57% | -0.17% | 0.53% |
| 2025-07-30 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.52% | 0.05% | -0.48% | -0.18% |
| 2025-07-24 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.55% | 0.9% | 0.01% | -0.89% | -0.76% |
| 2025-07-23 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 0.59% | 0.37% | -0.21% | 0.28% |
| 2025-07-22 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.58% | 0.06% | -0.52% | -0.4% |
| 2025-06-13 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.15% | 1.15% | 0.0% | 1.07% |
| 2025-06-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 0.33% | 0.0% | -0.33% | -0.23% |
| 2025-05-23 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.9% | 1.2% | 1.09% | -0.1% | 0.83% |
| 2025-05-14 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 0.94% | 0.62% | -0.32% | 0.29% |
| 2025-05-07 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.99% | 0.95% | 0.89% | -0.05% | 0.73% |
| 2025-05-06 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 0.73% | 0.04% | -0.69% | -0.67% |
| 2025-05-05 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.96% | 0.51% | 0.44% | -0.08% | 0.16% |
| 2025-04-29 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.68% | 0.36% | -0.33% | -0.19% |
| 2025-04-15 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.05% | 0.69% | 0.0% | -0.69% | -0.1% |
| 2025-04-07 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 2.35% | 2.28% | -0.07% | 2.2% |
| 2025-04-02 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.83% | 0.68% | -0.15% | 0.6% |
| 2025-02-28 | Strong Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.54% | 0.08% | -1.46% | -1.36% |
| 2025-02-25 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.76% | 0.49% | 0.48% | -0.01% | 0.04% |
| 2025-02-05 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.53% | 0.02% | -0.51% | -0.48% |
| 2025-02-04 | Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 1.44% | 1.08% | -0.37% | 0.84% |
| 2025-01-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.91% | 1.16% | 1.07% | -0.08% | 1.02% |
| 2025-01-21 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.86% | 1.92% | 0.02% | -1.9% | -1.57% |
| 2025-01-15 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 0.63% | 0.19% | -0.45% | -0.1% |
| 2025-01-14 | Strong Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.56% | 0.43% | -0.14% | 0.18% |
| 2025-01-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.91% | 0.0% | -0.91% | -0.85% |
| 2024-12-26 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 0.84% | 0.33% | -0.51% | -0.07% |
| 2024-12-23 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.79% | 0.94% | 0.55% | -0.38% | 0.04% |
| 2024-12-19 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.56% | 0.54% | -0.03% | 0.36% |
| 2024-12-16 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 0.73% | 0.11% | -0.61% | -0.42% |
| 2024-12-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.84% | 0.34% | -0.5% | -0.11% |
| 2024-11-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 1.09% | 1.09% | 0.0% | 0.82% |
| 2024-11-27 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.86% | 0.62% | -0.24% | 0.3% |
| 2024-11-26 | Strong Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.9% | 0.0% | -0.9% | -0.62% |
| 2024-11-25 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.89% | 0.4% | -0.49% | -0.01% |
| 2024-11-18 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.77% | 1.09% | 0.01% | -1.08% | -0.59% |
| 2024-11-04 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 2.06% | 0.0% | -2.05% | -1.34% |
| 2024-10-25 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 1.5% | 0.09% | -1.41% | -0.84% |
| 2024-10-23 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.93% | 0.93% | -0.0% | 0.24% |
| 2024-10-21 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 1.2% | 0.09% | -1.11% | -0.87% |
| 2024-10-15 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.68% | 0.81% | 0.1% | -0.71% | -0.48% |
| 2024-10-11 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.43% | 0.17% | -0.26% | -0.04% |
| 2024-10-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.79% | 1.16% | 0.85% | -0.3% | 0.83% |
| 2024-10-01 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.67% | 0.65% | 0.46% | -0.19% | 0.09% |
| 2024-09-25 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 0.62% | 0.51% | -0.11% | 0.44% |
| 2024-09-17 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.65% | 0.35% | 0.1% | -0.25% | -0.04% |
| 2024-09-09 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.8% | 0.82% | 0.54% | -0.28% | 0.48% |
| 2024-09-02 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 0.39% | 0.0% | -0.39% | -0.24% |
| 2024-08-28 | Mildly Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.66% | 0.39% | -0.26% | 0.06% |
| 2024-08-26 | Mildly Bearish | Mildly Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 0.68% | 0.55% | -0.13% | 0.42% |
| 2024-08-20 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.52% | 0.35% | -0.17% | 0.1% |
| 2024-08-19 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.47% | 0.01% | -0.46% | -0.23% |
| 2024-08-13 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 1.0% | 0.07% | -0.93% | -0.83% |
| 2024-08-07 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.98% | 0.63% | 0.2% | -0.43% | 0.11% |
| 2024-07-29 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.64% | 0.9% | 0.23% | -0.68% | -0.41% |
| 2024-07-23 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 2.07% | 0.06% | -2.01% | -0.38% |
| 2024-07-22 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.78% | 0.95% | 0.61% | -0.34% | 0.29% |
| 2024-07-19 | Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.76% | 1.39% | 0.0% | -1.39% | -1.32% |
| 2024-07-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.74% | 0.3% | 0.18% | -0.11% | -0.06% |
| 2024-07-04 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 0.49% | 0.13% | -0.36% | -0.27% |
| 2024-06-24 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.69% | 0.89% | 0.75% | -0.14% | 0.71% |
| 2024-06-21 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.7% | 1.14% | 0.03% | -1.11% | -0.88% |
| 2024-06-13 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.54% | 0.0% | -0.54% | -0.35% |
| 2024-06-10 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.88% | 0.79% | 0.4% | -0.39% | -0.36% |
| 2024-06-04 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.1% | 8.19% | 0.0% | -8.19% | -5.1% |
| 2024-05-18 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 1.04% | 0.22% | 0.03% | -0.19% | -0.03% |
| 2024-05-10 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.95% | 0.82% | 0.64% | -0.18% | 0.29% |
| 2024-05-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 1.69% | 0.37% | -1.32% | -1.15% |
| 2024-05-08 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.89% | 0.83% | 0.62% | -0.21% | 0.34% |
| 2024-04-29 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 0.95% | 0.8% | -0.15% | 0.7% |
| 2024-04-26 | Strong Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.56% | 1.04% | 0.0% | -1.04% | -0.75% |
| 2024-04-23 | Mildly Bullish | Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.44% | 0.0% | -0.43% | -0.38% |
| 2024-04-16 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.65% | 0.61% | 0.4% | -0.21% | 0.24% |
| 2024-04-03 | Bearish | Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 0.78% | 0.6% | -0.18% | 0.27% |
| 2024-03-19 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 0.84% | 0.15% | -0.7% | -0.62% |
| 2024-03-14 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.76% | 1.31% | 1.01% | -0.3% | 0.78% |
| 2024-03-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.71% | 2.41% | 0.06% | -2.35% | -2.01% |
| 2024-03-12 | Mildly Bearish | Strong Bearish | Bearish Alignment | Top to Down | Against then Recovered | Reversed by Close | Reversed Before Half | 0.73% | 0.88% | 0.53% | -0.35% | -0.0% |
| 2024-02-29 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.85% | 0.91% | 0.57% | -0.34% | 0.49% |
| 2024-02-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.81% | 1.18% | 0.14% | -1.04% | -0.86% |
| 2024-02-07 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.83% | 0.88% | 0.04% | -0.84% | -0.43% |
| 2024-02-06 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 0.98% | 0.58% | -0.4% | 0.52% |
| 2024-02-01 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 0.8% | 0.24% | -0.56% | -0.41% |
| 2024-01-31 | Strong Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.84% | 1.36% | 1.18% | -0.18% | 1.03% |
| 2024-01-30 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.82% | 1.43% | 0.17% | -1.26% | -1.13% |
| 2024-01-25 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.75% | 0.99% | 0.02% | -0.97% | -0.39% |
| 2024-01-16 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.7% | 0.2% | -0.5% | -0.22% |
| 2023-12-26 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.72% | 0.69% | 0.52% | -0.17% | 0.42% |
| 2023-12-20 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.73% | 2.35% | 0.23% | -2.12% | -2.05% |
| 2023-12-01 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.66% | 0.53% | 0.48% | -0.05% | 0.31% |
| 2023-11-13 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.41% | 0.04% | -0.37% | -0.24% |
| 2023-11-12 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.58% | 0.19% | 0.0% | -0.19% | -0.13% |
| 2023-10-09 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.54% | 0.56% | 0.25% | -0.3% | -0.21% |
| 2023-10-03 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.6% | 0.73% | 0.0% | -0.73% | -0.51% |
| 2023-09-29 | Mildly Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.67% | 0.89% | 0.74% | -0.15% | 0.29% |
| 2023-09-28 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.61% | 1.39% | 0.02% | -1.36% | -1.06% |
| 2023-09-26 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 0.31% | 0.08% | -0.23% | -0.05% |
| 2023-09-18 | Bullish | Mildly Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.57% | 0.38% | 0.2% | -0.19% | -0.16% |
| 2023-09-15 | Bearish | Strong Bearish | Bearish Alignment | Down to Up | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.46% | 0.33% | -0.13% | 0.06% |
| 2023-09-14 | Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.62% | 0.61% | 0.2% | -0.41% | -0.13% |
| 2023-09-12 | Mildly Bullish | Strong Bullish | Bullish Alignment | Top to Down | Worked then Reversed | Reversed by Close | Reversed Before Half | 0.59% | 0.97% | 0.0% | -0.97% | -0.62% |

### Mixed Days (FII vs PRO opposing) — 82 days

| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|
| 2026-09-01 | Mildly Bullish | Strong Bearish | Top to Down | 0.59% | 0.79% | 0.27% | -0.52% | -0.09% |
| 2026-08-20 | Bearish | Bullish | Down to Up | 0.59% | 0.33% | 0.16% | -0.17% | 0.03% |
| 2026-08-18 | Mildly Bullish | Bearish | Top to Down | 0.59% | 0.47% | 0.19% | -0.28% | -0.28% |
| 2026-08-14 | Mildly Bearish | Bullish | Down to Up | 0.6% | 0.44% | 0.18% | -0.27% | 0.02% |
| 2026-08-13 | Bearish | Mildly Bullish | Top to Down | 0.61% | 0.49% | 0.0% | -0.49% | -0.15% |
| 2026-08-06 | Mildly Bearish | Bullish | Top to Down | 0.63% | 0.3% | 0.15% | -0.15% | -0.02% |
| 2026-07-28 | Bullish | Mildly Bearish | Down to Up | 0.66% | 0.36% | 0.29% | -0.07% | 0.07% |
| 2026-07-16 | Bearish | Mildly Bullish | Top to Down | 0.69% | 0.57% | 0.18% | -0.38% | -0.25% |
| 2026-06-29 | Mildly Bullish | Strong Bearish | Top to Down | 0.68% | 0.81% | 0.24% | -0.57% | -0.35% |
| 2026-06-04 | Mildly Bearish | Strong Bullish | Down to Up | 0.85% | 0.94% | 0.79% | -0.15% | 0.67% |
| 2026-06-03 | Mildly Bearish | Bullish | Top to Down | 0.8% | 1.32% | 0.19% | -1.13% | -0.08% |
| 2026-05-05 | Mildly Bullish | Bearish | Top to Down | 0.96% | 0.83% | 0.12% | -0.71% | -0.0% |
| 2026-04-08 | Mildly Bullish | Mildly Bearish | Down to Up | 1.29% | 0.82% | 0.71% | -0.11% | 0.66% |
| 2026-03-16 | Strong Bearish | Bullish | Down to Up | 1.19% | 2.37% | 1.67% | -0.7% | 1.04% |
| 2026-02-10 | Bullish | Strong Bearish | Top to Down | 0.64% | 0.46% | 0.26% | -0.2% | -0.02% |
| 2026-01-22 | Bearish | Strong Bullish | Top to Down | 0.72% | 1.05% | 0.36% | -0.69% | -0.09% |
| 2025-12-05 | Mildly Bearish | Mildly Bullish | Down to Up | 0.57% | 0.84% | 0.78% | -0.06% | 0.68% |
| 2025-10-24 | Mildly Bullish | Strong Bearish | Top to Down | 0.61% | 0.87% | 0.03% | -0.84% | -0.53% |
| 2025-09-09 | Mildly Bullish | Bearish | Down to Up | 0.57% | 0.31% | 0.11% | -0.2% | 0.06% |
| 2025-07-04 | Bullish | Strong Bearish | Down to Up | 0.65% | 0.55% | 0.16% | -0.38% | 0.15% |
| 2025-06-27 | Bullish | Strong Bearish | Down to Up | 0.66% | 0.51% | 0.3% | -0.21% | 0.22% |
| 2025-05-12 | Mildly Bearish | Mildly Bullish | Down to Up | 1.13% | 2.32% | 2.15% | -0.17% | 2.05% |
| 2025-05-02 | Bullish | Mildly Bearish | Down to Up | 0.95% | 1.44% | 1.14% | -0.3% | 0.01% |
| 2025-04-24 | Bullish | Mildly Bearish | Top to Down | 0.84% | 0.54% | 0.29% | -0.25% | -0.14% |
| 2025-03-20 | Mildly Bullish | Bearish | Down to Up | 0.7% | 1.05% | 0.78% | -0.27% | 0.56% |
| 2025-03-07 | Mildly Bullish | Bearish | Down to Up | 0.72% | 0.75% | 0.56% | -0.2% | 0.13% |
| 2025-01-28 | Strong Bullish | Strong Bearish | Down to Up | 0.95% | 1.22% | 0.77% | -0.45% | 0.07% |
| 2025-01-07 | Bullish | Strong Bearish | Down to Up | 0.82% | 0.66% | 0.49% | -0.18% | 0.06% |
| 2025-01-01 | Strong Bearish | Bullish | Down to Up | 0.76% | 1.1% | 0.78% | -0.32% | 0.51% |
| 2024-12-27 | Mildly Bullish | Strong Bearish | Down to Up | 0.74% | 0.58% | 0.58% | -0.0% | 0.13% |
| 2024-12-20 | Mildly Bearish | Strong Bullish | Top to Down | 0.76% | 2.21% | 0.44% | -1.77% | -1.37% |
| 2024-12-13 | Bearish | Bullish | Down to Up | 0.69% | 2.5% | 1.2% | -1.3% | 1.15% |
| 2024-12-05 | Mildly Bullish | Mildly Bearish | Down to Up | 0.76% | 2.29% | 1.3% | -0.99% | 0.66% |
| 2024-11-28 | Mildly Bullish | Bearish | Top to Down | 0.77% | 1.95% | 0.29% | -1.65% | -1.3% |
| 2024-11-22 | Bearish | Bullish | Down to Up | 0.84% | 2.55% | 2.32% | -0.23% | 1.97% |
| 2024-11-14 | Mildly Bearish | Strong Bullish | Down to Up | 0.81% | 0.81% | 0.57% | -0.25% | 0.07% |
| 2024-11-05 | Bullish | Strong Bearish | Down to Up | 0.87% | 1.62% | 1.31% | -0.31% | 1.18% |
| 2024-10-09 | Bearish | Strong Bullish | Top to Down | 0.76% | 1.14% | 0.67% | -0.47% | -0.18% |
| 2024-10-03 | Strong Bearish | Strong Bullish | Top to Down | 0.63% | 1.61% | 0.73% | -0.87% | -0.73% |
| 2024-09-30 | Mildly Bullish | Strong Bearish | Top to Down | 0.63% | 1.31% | 0.28% | -1.03% | -0.92% |
| 2024-09-27 | Bullish | Strong Bearish | Top to Down | 0.63% | 0.48% | 0.11% | -0.37% | -0.28% |
| 2024-09-06 | Mildly Bullish | Bearish | Top to Down | 0.74% | 1.46% | 0.3% | -1.17% | -0.9% |
| 2024-08-29 | Mildly Bullish | Strong Bearish | Down to Up | 0.73% | 0.78% | 0.63% | -0.15% | 0.49% |
| 2024-08-23 | Mildly Bullish | Bearish | Top to Down | 0.68% | 0.35% | 0.05% | -0.3% | -0.05% |
| 2024-08-08 | Strong Bearish | Strong Bullish | Top to Down | 0.85% | 1.08% | 0.38% | -0.7% | -0.62% |
| 2024-08-02 | Strong Bullish | Strong Bearish | Top to Down | 0.68% | 0.67% | 0.25% | -0.41% | -0.36% |
| 2024-08-01 | Strong Bearish | Strong Bullish | Top to Down | 0.69% | 0.49% | 0.19% | -0.3% | -0.1% |
| 2024-07-25 | Bearish | Bullish | Down to Up | 0.62% | 0.89% | 0.81% | -0.08% | 0.76% |
| 2024-07-10 | Strong Bearish | Strong Bullish | Top to Down | 0.75% | 1.31% | 0.0% | -1.3% | -0.6% |
| 2024-07-09 | Strong Bullish | Strong Bearish | Down to Up | 0.71% | 0.46% | 0.38% | -0.08% | 0.27% |
| 2024-07-01 | Mildly Bullish | Strong Bearish | Down to Up | 0.72% | 0.71% | 0.71% | -0.0% | 0.54% |
| 2024-06-28 | Strong Bullish | Bearish | Top to Down | 0.74% | 0.78% | 0.37% | -0.42% | -0.32% |
| 2024-06-27 | Bullish | Strong Bearish | Down to Up | 0.74% | 1.18% | 0.86% | -0.32% | 0.65% |
| 2024-06-20 | Bullish | Strong Bearish | Top to Down | 0.72% | 0.77% | 0.16% | -0.61% | -0.03% |
| 2024-06-14 | Bullish | Bearish | Top to Down | 0.71% | 0.67% | 0.11% | -0.56% | -0.05% |
| 2024-06-11 | Strong Bullish | Strong Bearish | Top to Down | 0.86% | 0.79% | 0.45% | -0.33% | -0.09% |
| 2024-05-29 | Mildly Bullish | Strong Bearish | Top to Down | 1.27% | 0.62% | 0.28% | -0.34% | -0.25% |
| 2024-05-27 | Bullish | Strong Bearish | Top to Down | 1.14% | 1.04% | 0.31% | -0.73% | -0.47% |
| 2024-04-10 | Mildly Bullish | Strong Bearish | Down to Up | 0.59% | 0.45% | 0.24% | -0.2% | 0.07% |
| 2024-04-09 | Bullish | Strong Bearish | Top to Down | 0.61% | 0.69% | 0.01% | -0.67% | -0.54% |
| 2024-04-01 | Strong Bullish | Bearish | Down to Up | 0.67% | 0.46% | 0.33% | -0.12% | 0.06% |
| 2024-03-28 | Bearish | Strong Bullish | Down to Up | 0.66% | 1.59% | 1.59% | 0.0% | 0.81% |
| 2024-03-18 | Mildly Bullish | Strong Bearish | Down to Up | 0.72% | 0.94% | 0.61% | -0.33% | 0.28% |
| 2024-03-11 | Mildly Bullish | Strong Bearish | Top to Down | 0.71% | 0.97% | 0.04% | -0.93% | -0.88% |
| 2024-03-06 | Bearish | Mildly Bullish | Down to Up | 0.75% | 1.22% | 0.76% | -0.46% | 0.68% |
| 2024-03-05 | Strong Bullish | Strong Bearish | Top to Down | 0.78% | 0.66% | 0.2% | -0.46% | -0.06% |
| 2024-02-22 | Bullish | Strong Bearish | Down to Up | 0.83% | 1.71% | 0.77% | -0.93% | 0.61% |
| 2024-02-19 | Bearish | Bullish | Down to Up | 0.8% | 0.75% | 0.38% | -0.37% | 0.06% |
| 2024-02-16 | Strong Bullish | Mildly Bearish | Down to Up | 0.8% | 0.45% | 0.22% | -0.23% | 0.06% |
| 2024-02-08 | Mildly Bearish | Bullish | Top to Down | 0.81% | 1.57% | 0.01% | -1.56% | -1.14% |
| 2024-02-05 | Bullish | Strong Bearish | Top to Down | 0.77% | 1.08% | 0.2% | -0.89% | -0.73% |
| 2024-01-29 | Strong Bearish | Bullish | Down to Up | 0.73% | 1.56% | 1.54% | -0.02% | 1.45% |
| 2024-01-24 | Strong Bullish | Bearish | Down to Up | 0.78% | 1.63% | 1.4% | -0.23% | 1.3% |
| 2024-01-19 | Bearish | Strong Bullish | Down to Up | 0.74% | 0.44% | 0.26% | -0.19% | 0.11% |
| 2024-01-11 | Bearish | Strong Bullish | Top to Down | 0.68% | 0.61% | 0.18% | -0.43% | -0.09% |
| 2023-12-29 | Bullish | Strong Bearish | Top to Down | 0.79% | 0.43% | 0.15% | -0.28% | -0.04% |
| 2023-12-28 | Bearish | Strong Bullish | Down to Up | 0.81% | 0.57% | 0.4% | -0.17% | 0.27% |
| 2023-12-11 | Mildly Bearish | Bullish | Down to Up | 0.65% | 0.49% | 0.29% | -0.2% | 0.13% |
| 2023-12-07 | Bullish | Strong Bearish | Top to Down | 0.72% | 0.43% | 0.04% | -0.39% | -0.08% |
| 2023-10-27 | Strong Bearish | Strong Bullish | Down to Up | 0.61% | 0.79% | 0.78% | -0.01% | 0.7% |
| 2023-10-25 | Bullish | Strong Bearish | Top to Down | 0.57% | 1.42% | 0.32% | -1.1% | -0.83% |
| 2023-10-20 | Bearish | Strong Bullish | Top to Down | 0.57% | 0.38% | 0.26% | -0.12% | -0.0% |

### FII Solo View (PRO Neutral) — 46 days

| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |
|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|
| 2026-08-21 | Strong Bullish | Neutral | Top to Down | 0.56% | 0.32% | 0.0% | -0.32% | -0.13% |
| 2026-07-24 | Bearish | Neutral | Down to Up | 0.71% | 0.92% | 0.66% | -0.25% | 0.51% |
| 2026-07-23 | Strong Bearish | Neutral | Top to Down | 0.7% | 0.77% | 0.36% | -0.41% | -0.14% |
| 2026-07-17 | Mildly Bullish | Neutral | Down to Up | 0.67% | 1.11% | 0.99% | -0.12% | 0.91% |
| 2026-07-14 | Bullish | Neutral | Top to Down | 0.7% | 0.55% | 0.37% | -0.18% | -0.14% |
| 2026-07-06 | Mildly Bearish | Neutral | Down to Up | 0.62% | 0.71% | 0.62% | -0.08% | 0.48% |
| 2026-07-01 | Bullish | Neutral | Down to Up | 0.71% | 0.65% | 0.64% | -0.01% | 0.38% |
| 2026-06-10 | Bullish | Neutral | Top to Down | 0.82% | 1.04% | 0.82% | -0.21% | -0.08% |
| 2026-06-01 | Strong Bearish | Neutral | Top to Down | 0.85% | 1.59% | 0.33% | -1.25% | -1.16% |
| 2026-05-26 | Strong Bullish | Neutral | Top to Down | 0.87% | 0.85% | 0.36% | -0.49% | -0.29% |
| 2026-04-01 | Mildly Bullish | Neutral | Top to Down | 1.46% | 1.41% | 0.18% | -1.22% | -0.86% |
| 2026-03-23 | Bearish | Neutral | Top to Down | 1.19% | 1.67% | 0.12% | -1.55% | -1.45% |
| 2026-03-17 | Bullish | Neutral | Down to Up | 1.13% | 1.32% | 0.7% | -0.62% | 0.28% |
| 2026-03-06 | Bearish | Neutral | Top to Down | 0.94% | 1.16% | 0.18% | -0.98% | -0.76% |
| 2026-02-25 | Bearish | Neutral | Top to Down | 0.74% | 0.88% | 0.55% | -0.33% | -0.13% |
| 2026-02-03 | Bearish | Neutral | Top to Down | 0.73% | 2.66% | 0.13% | -2.53% | -2.26% |
| 2026-01-29 | Mildly Bearish | Neutral | Down to Up | 0.71% | 1.18% | 0.45% | -0.73% | 0.3% |
| 2026-01-14 | Mildly Bearish | Neutral | Down to Up | 0.59% | 0.73% | 0.56% | -0.17% | 0.08% |
| 2025-12-15 | Bullish | Neutral | Down to Up | 0.53% | 0.55% | 0.45% | -0.1% | 0.32% |
| 2025-11-12 | Mildly Bullish | Neutral | Down to Up | 0.65% | 0.59% | 0.39% | -0.21% | 0.15% |
| 2025-10-17 | Bullish | Neutral | Down to Up | 0.57% | 1.07% | 0.92% | -0.15% | 0.62% |
| 2025-10-07 | Mildly Bullish | Neutral | Down to Up | 0.53% | 0.58% | 0.54% | -0.04% | 0.11% |
| 2025-09-30 | Mildly Bullish | Neutral | Top to Down | 0.6% | 0.58% | 0.16% | -0.42% | -0.24% |
| 2025-09-03 | Bearish | Neutral | Down to Up | 0.6% | 0.83% | 0.49% | -0.34% | 0.39% |
| 2025-07-29 | Bearish | Neutral | Down to Up | 0.63% | 1.01% | 0.97% | -0.04% | 0.9% |
| 2025-07-21 | Bearish | Neutral | Down to Up | 0.6% | 0.92% | 0.45% | -0.47% | 0.38% |
| 2025-05-13 | Mildly Bullish | Neutral | Top to Down | 0.96% | 1.71% | 0.44% | -1.27% | -1.09% |
| 2025-04-11 | Mildly Bearish | Neutral | Down to Up | 1.12% | 1.01% | 1.01% | 0.0% | 0.66% |
| 2025-04-04 | Mildly Bullish | Neutral | Top to Down | 0.71% | 1.54% | 0.1% | -1.44% | -1.2% |
| 2025-04-01 | Mildly Bearish | Neutral | Top to Down | 0.67% | 1.84% | 0.96% | -0.88% | -0.69% |
| 2025-03-28 | Mildly Bullish | Neutral | Top to Down | 0.7% | 0.84% | 0.21% | -0.64% | -0.45% |
| 2025-02-17 | Mildly Bearish | Neutral | Down to Up | 0.79% | 1.09% | 0.72% | -0.37% | 0.67% |
| 2025-01-27 | Strong Bearish | Neutral | Top to Down | 0.88% | 0.96% | 0.29% | -0.67% | -0.54% |
| 2025-01-10 | Mildly Bearish | Neutral | Top to Down | 0.77% | 1.07% | 0.19% | -0.88% | -0.49% |
| 2024-12-12 | Bullish | Neutral | Top to Down | 0.69% | 0.6% | 0.29% | -0.31% | -0.26% |
| 2024-11-21 | Bullish | Neutral | Top to Down | 0.82% | 1.04% | 0.08% | -0.96% | -0.6% |
| 2024-10-10 | Bearish | Neutral | Top to Down | 0.74% | 0.62% | 0.27% | -0.35% | -0.24% |
| 2024-10-07 | Strong Bearish | Neutral | Top to Down | 0.74% | 1.79% | 0.23% | -1.55% | -1.06% |
| 2024-08-30 | Strong Bullish | Neutral | Top to Down | 0.72% | 0.27% | 0.07% | -0.2% | -0.01% |
| 2024-07-08 | Strong Bearish | Neutral | Down to Up | 0.66% | 0.43% | 0.06% | -0.37% | 0.01% |
| 2024-05-31 | Strong Bearish | Neutral | Top to Down | 1.27% | 0.84% | 0.38% | -0.46% | -0.08% |
| 2024-05-07 | Mildly Bullish | Neutral | Top to Down | 0.87% | 1.19% | 0.04% | -1.15% | -0.82% |
| 2024-04-04 | Mildly Bearish | Neutral | Top to Down | 0.6% | 1.4% | 0.12% | -1.28% | -0.23% |
| 2024-01-10 | Strong Bullish | Neutral | Down to Up | 0.69% | 0.9% | 0.52% | -0.37% | 0.45% |
| 2023-11-24 | Bearish | Neutral | Top to Down | 0.59% | 0.32% | 0.12% | -0.21% | -0.11% |
| 2023-09-27 | Mildly Bearish | Neutral | Down to Up | 0.59% | 0.9% | 0.48% | -0.42% | 0.46% |


---
*Generated from 730 trading days (2023-09-11 to 2026-09-09)*
