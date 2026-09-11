# Bearish Alignment + VIX Half-Range Exhaustion: Detailed Examples

> **Context**: When both FII and PRO are bearish (T+1 data), we check whether
> the market's downward move exceeded half the VIX-predicted daily range before
> any reversal. This document walks through real examples from all four outcome
> quadrants.

---

## How It Works

1. **FII and PRO both bearish** (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the bearish move (low from open) exceed that half threshold?

```
VIX Predicted Range = 0.86%
Half Threshold      = 0.43%
Intraday Low%       = -0.60%  ← Exceeded 0.43% downside → "Exceeded Half"

vs.

VIX Predicted Range = 1.30%
Half Threshold      = 0.65%
Intraday Low%       = -0.14%  ← Did NOT reach 0.65% → "Reversed Before Half"
```

---

## Summary Table (332 Bearish Alignment Days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 191 | 57.5% | 153 | **80.1%** | -0.40% |
| Reversed Before Half | 141 | 42.5% | 25 | **17.7%** | +0.37% |

**Key takeaway**: If the bearish move exceeded half the VIX range, the market closed bearish 80.1% of the time. If it didn't reach that level, the market closed bullish 82.3% of the time.

### Bearish vs Bullish Alignment Comparison

| Metric | Bullish (285 days) | Bearish (293 days) |
|--------|-------------------:|-------------------:|
| Exceeded Half: count | 116 (36.4%) | 191 (57.5%) |
| Exceeded Half: WR% | 87.1% | 80.1% |
| Reversed Before Half: count | 203 (63.6%) | 141 (42.5%) |
| Reversed Before Half: loss rate | 78.3% | 82.3% |

**Notable asymmetry**: Bearish alignment exceeds the VIX half-threshold 57.5% of the time vs only 36.4% for bullish. Selloffs more readily exhaust the VIX-predicted range than rallies. However, bullish has a higher WR% when the threshold is exceeded (87.1% vs 80.1%).

---

## Quadrant 1: Exceeded Half + Worked and Remained (153 days, 80.1% of Exceeded Half)

**The high-conviction bearish outcome.** The market moved down past the VIX half-threshold and held those losses by close.

### Recent Examples (2025-2026)

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2026-08-27 | Mildly Bearish | Strong Bearish | 0.58% | -0.77% | **-0.77%** | N/A | No |
| 2026-08-19 | Strong Bearish | Strong Bearish | 0.60% | -0.52% | **-0.31%** | N/A | No |
| 2026-08-12 | Bearish | Strong Bearish | 0.62% | -0.84% | **-0.15%** | N/A | No |
| 2026-08-05 | Bearish | Bearish | 0.64% | -0.69% | **-0.18%** | N/A | No |
| 2026-07-22 | Strong Bearish | Strong Bearish | 0.66% | -0.78% | **-0.66%** | N/A | No |
| 2026-06-09 | Mildly Bearish | Bearish | 0.89% | -0.66% | **-0.01%** | N/A | Yes |
| 2026-05-12 | Bearish | Mildly Bearish | 0.97% | -1.58% | **-1.23%** | N/A | Yes |
| 2026-05-08 | Bearish | Strong Bearish | 0.87% | -0.44% | **-0.22%** | N/A | No |
| 2026-04-24 | Bearish | Strong Bearish | 0.97% | -1.19% | **-0.82%** | N/A | No |
| 2026-03-30 | Mildly Bearish | Bearish | 1.40% | -1.18% | **-0.76%** | N/A | Yes |
| 2026-02-24 | Mildly Bearish | Strong Bearish | 0.74% | -1.23% | **-0.71%** | N/A | Yes |
| 2026-02-13 | Mildly Bearish | Strong Bearish | 0.61% | -0.50% | **-0.43%** | N/A | No |
| 2026-02-01 | Mildly Bearish | Strong Bearish | 0.71% | -3.01% | **-2.23%** | N/A | No |
| 2026-01-09 | Strong Bearish | Strong Bearish | 0.55% | -0.84% | **-0.53%** | N/A | No |

---

## Quadrant 2: Exceeded Half + Reversed by Close (38 days, 19.9% of Exceeded Half)

**The bearish failure case.** The market dropped past the VIX half-threshold but then completely reversed and closed bullish. 38 out of 191 times — more frequent than bullish failures (15 out of 116).

### All 38 Instances

| Date | FII | PRO | VIX Predicted% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2020-09-01 | Strong Bearish | Strong Bearish | 1.20% | -0.85% | **+0.26%** | N/A | No |
| 2020-11-20 | Mildly Bearish | Strong Bearish | 1.02% | -0.65% | **+0.25%** | N/A | No |
| 2020-11-26 | Bearish | Strong Bearish | 1.21% | -0.90% | **+0.84%** | N/A | Yes |
| 2020-12-22 | Mildly Bearish | Strong Bearish | 1.21% | -1.34% | **+0.65%** | N/A | No |
| 2021-01-28 | Bearish | Bearish | 1.28% | -0.69% | **+0.07%** | N/A | Yes |
| 2021-04-01 | Strong Bearish | Bearish | 1.08% | -0.71% | **+0.46%** | N/A | Yes |
| 2021-09-21 | Bearish | Strong Bearish | 0.92% | -0.71% | **+0.65%** | N/A | No |
| 2022-01-07 | Bearish | Strong Bearish | 0.94% | -0.52% | **+0.12%** | N/A | No |
| 2022-03-22 | Bearish | Strong Bearish | 1.29% | -0.67% | **+1.22%** | N/A | No |
| 2022-04-28 | Mildly Bearish | Strong Bearish | 1.08% | -0.69% | **+0.24%** | N/A | Yes |
| 2022-05-26 | Mildly Bearish | Strong Bearish | 1.32% | -1.25% | **+0.60%** | N/A | Yes |
| 2022-08-03 | Bearish | Bearish | 0.97% | -0.71% | **+0.25%** | N/A | No |
| 2022-11-15 | Bearish | Strong Bearish | 0.78% | -0.44% | **+0.32%** | N/A | No |
| 2023-01-30 | Bearish | Strong Bearish | 0.91% | -0.77% | **+0.71%** | N/A | No |
| 2023-03-08 | Mildly Bearish | Strong Bearish | 0.64% | -0.35% | **+0.49%** | N/A | No |
| 2023-04-24 | Bearish | Bearish | 0.61% | -0.54% | **+0.23%** | N/A | No |
| 2023-04-26 | Mildly Bearish | Strong Bearish | 0.60% | -0.31% | **+0.29%** | N/A | No |
| 2023-05-25 | Bearish | Strong Bearish | 0.69% | -0.36% | **+0.37%** | N/A | Yes |
| 2023-06-20 | Bearish | Strong Bearish | 0.59% | -0.49% | **+0.43%** | N/A | No |
| 2023-07-19 | Bearish | Strong Bearish | 0.61% | -0.38% | **+0.22%** | N/A | No |
| 2023-07-31 | Strong Bearish | Bearish | 0.53% | -0.35% | **+0.39%** | N/A | No |
| 2023-08-23 | Strong Bearish | Strong Bearish | 0.62% | -0.37% | **+0.01%** | N/A | No |
| 2023-10-04 | Strong Bearish | Strong Bearish | 0.62% | -0.58% | **-0.00%** | N/A | No |
| 2024-01-18 | Bearish | Strong Bearish | 0.79% | -0.60% | **+0.29%** | N/A | Yes |
| 2024-02-09 | Bearish | Strong Bearish | 0.83% | -0.45% | **+0.27%** | N/A | No |
| 2024-02-13 | Strong Bearish | Strong Bearish | 0.84% | -0.56% | **+0.29%** | N/A | No |
| 2024-02-15 | Mildly Bearish | Mildly Bearish | 0.81% | -0.51% | **+0.09%** | N/A | Yes |
| 2024-03-20 | Bearish | Strong Bearish | 0.74% | -0.61% | **+0.05%** | N/A | No |
| 2024-04-19 | Mildly Bearish | Strong Bearish | 0.68% | -0.38% | **+1.32%** | N/A | No |
| 2024-06-05 | Strong Bearish | Strong Bearish | 1.40% | -1.52% | **+2.01%** | N/A | No |
| 2024-09-12 | Mildly Bearish | Strong Bearish | 0.71% | -0.47% | **+1.02%** | N/A | Yes |
| 2024-10-18 | Bearish | Bearish | 0.70% | -0.39% | **+0.80%** | N/A | No |
| 2024-10-28 | Strong Bearish | Strong Bearish | 0.77% | -0.48% | **+0.48%** | N/A | No |
| 2025-08-07 | Bearish | Mildly Bearish | 0.63% | -0.49% | **+0.66%** | N/A | Yes |
| 2026-01-21 | Mildly Bearish | Bearish | 0.67% | -0.88% | **+0.11%** | N/A | No |
| 2026-02-02 | Mildly Bearish | Strong Bearish | 0.79% | -0.47% | **+1.14%** | N/A | No |
| 2026-02-06 | Bearish | Strong Bearish | 0.64% | -0.44% | **+0.26%** | N/A | No |
| 2026-03-09 | Strong Bearish | Strong Bearish | 1.04% | -0.71% | **+0.58%** | N/A | No |

---

*Report generated from corrected alignment data on 2026-09-11 at 22:41:53*