# FII-PRO Alignment × VIX Half-Range Exhaustion: Complete Guide

> **Retrospective study**: FII/PRO views are derived from T+1 settlement data,
> so alignment is known only after the trading day. This analysis identifies
> historical patterns, not real-time predictive signals.
>
> **Timing data**: Uses 5-minute candle data from PostgreSQL (`nifty50_5min`,
> Aug 2020 – Aug 2026) to determine the exact candle where the VIX half-threshold
> was first crossed.

---

## How It Works

1. **FII and PRO align** — both bullish or both bearish (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the market move in the aligned direction past the half threshold?

```
BULLISH ALIGNMENT:
  VIX Predicted = 0.86%  →  Half Threshold = 0.43%
  Intraday High% = 0.60%  →  Exceeded 0.43% ✓  ("Exceeded Half")
  Intraday High% = 0.15%  →  Did NOT reach     ("Reversed Before Half")

BEARISH ALIGNMENT:
  VIX Predicted = 0.86%  →  Half Threshold = 0.43%
  Intraday Low% = -0.60%  →  Exceeded 0.43% ✓  ("Exceeded Half")
  Intraday Low% = -0.14%  →  Did NOT reach     ("Reversed Before Half")
```

---

## Master Summary (652 Aligned Days with VIX Data)

### Bullish Alignment (319 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 116 | 36.4% | 101 | **87.1%** | +0.51% |
| Reversed Before Half | 203 | 63.6% | 44 | **21.7%** | -0.41% |

### Bearish Alignment (333 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 191 | 57.4% | 153 | **80.1%** | -0.40% |
| Reversed Before Half | 142 | 42.6% | 26 | **18.3%** | +0.36% |

---

## Sub-Category Breakdown: Which FII-PRO Combinations Reach the Half Threshold?

> This section analyzes which specific FII-PRO stance combinations are most prone
> to crossing the VIX half-threshold, and which tend to fail before reaching it.

### Bullish Alignment: Exceeded Half % by Combination

| FII View | PRO View | N | ExcH | ExcH% | ExcH WR% | RevBH | RevBH WR% |
|----------|----------|--:|-----:|------:|----------:|------:|----------:|
| Strong Bullish | Strong Bullish | 70 | 31 | 44.3% | 90.3% | 39 | 33.3% |
| Strong Bullish | Bullish | 5 | 4 | 80.0% | 75.0% | 1 | 100.0% |
| Strong Bullish | Mildly Bullish | 5 | 2 | 40.0% | 100.0% | 3 | 0.0% |
| Bullish | Strong Bullish | 129 | 39 | 30.2% | 79.5% | 90 | 20.0% |
| Bullish | Bullish | 26 | 11 | 42.3% | 81.8% | 15 | 33.3% |
| Bullish | Mildly Bullish | 8 | 4 | 50.0% | 100.0% | 4 | 0.0% |
| Mildly Bullish | Strong Bullish | 40 | 11 | 27.5% | 90.9% | 29 | 10.3% |
| Mildly Bullish | Bullish | 26 | 9 | 34.6% | 100.0% | 17 | 5.9% |
| Mildly Bullish | Mildly Bullish | 10 | 5 | 50.0% | 100.0% | 5 | 60.0% |

### Bearish Alignment: Exceeded Half % by Combination

| FII View | PRO View | N | ExcH | ExcH% | ExcH WR% | RevBH | RevBH WR% |
|----------|----------|--:|-----:|------:|----------:|------:|----------:|
| Strong Bearish | Strong Bearish | 80 | 48 | 60.0% | 85.4% | 32 | 18.8% |
| Strong Bearish | Bearish | 9 | 6 | 66.7% | 66.7% | 3 | 33.3% |
| Strong Bearish | Mildly Bearish | 5 | 2 | 40.0% | 100.0% | 3 | 33.3% |
| Bearish | Strong Bearish | 103 | 61 | 59.2% | 78.7% | 42 | 21.4% |
| Bearish | Bearish | 32 | 18 | 56.2% | 77.8% | 14 | 28.6% |
| Bearish | Mildly Bearish | 11 | 5 | 45.5% | 80.0% | 6 | 33.3% |
| Mildly Bearish | Strong Bearish | 53 | 32 | 60.4% | 71.9% | 21 | 4.8% |
| Mildly Bearish | Bearish | 29 | 17 | 58.6% | 94.1% | 12 | 16.7% |
| Mildly Bearish | Mildly Bearish | 11 | 2 | 18.2% | 50.0% | 9 | 0.0% |

---

*Report generated from corrected alignment data on 2026-09-12 at 14:43:12*