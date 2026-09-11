# FII-PRO Alignment × VIX Half-Range Exhaustion: Expiry Day Guide

> **Scope**: This guide focuses exclusively on **Nifty expiry days** (weekly/monthly).
> For the full dataset including non-expiry days, see `VIX_EXHAUSTION_COMPLETE_GUIDE.md`.
>
> **Retrospective study**: FII/PRO views are derived from T+1 settlement data,
> so alignment is known only after the trading day. This analysis identifies
> historical patterns, not real-time predictive signals.
>
> **Data**: 133 aligned expiry days from Aug 2020 – Aug 2026 (60 Bullish, 73 Bearish).
> Timing from 5-minute candle data (PostgreSQL `nifty50_5min`).

---

## How It Works (Recap)

1. **FII and PRO align** — both bullish or both bearish (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the market move in the aligned direction past the half threshold?

---

## Master Summary: Expiry Days (133 Aligned Days)

### Bullish Alignment on Expiry (60 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 22 | 36.7% | 20 | **90.9%** | +0.66% |
| Reversed Before Half | 38 | 63.3% | 10 | **26.3%** | -0.33% |

### Bearish Alignment on Expiry (73 days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Close% |
|----------------|------:|--:|--------------------:|----:|----------:|
| Exceeded Half | 49 | 67.1% | 39 | **79.6%** | -0.47% |
| Reversed Before Half | 24 | 32.9% | 5 | **20.8%** | +0.38% |

### Expiry vs Non-Expiry Comparison

| Metric | Expiry | Non-Expiry | Delta |
|--------|:------:|:---------:|:-----:|
| **Bullish ExcH Rate** | 36.7% | 36.3% | **+0.4pp** |
| **Bullish ExcH WR%** | **90.9%** | 86.2% | **+4.7pp** |
| **Bearish ExcH Rate** | **67.1%** | 54.8% | **+12.3pp** |
| **Bearish ExcH WR%** | 79.6% | 80.3% | **-0.7pp** |

---

## Combination Breakdown: Which FII-PRO Combos Work Best on Expiry?

### Bullish Alignment: Exceeded Half on Expiry (22 days)

| Combo (FII + PRO) | N | Won | WR% | Avg Close% |
|--------------------|--:|----:|----:|----------:|
| Strong Bullish + Strong Bullish | 2 | 2 | 100.0% | +0.64% |
| Strong Bullish + Bullish | 1 | 0 | 0.0% | -0.32% |
| Strong Bullish + Mildly Bullish | 1 | 1 | 100.0% | +0.38% |
| Bullish + Strong Bullish | 11 | 10 | 90.9% | +0.57% |
| Bullish + Bullish | 1 | 1 | 100.0% | +0.97% |
| Bullish + Mildly Bullish | 2 | 2 | 100.0% | +1.35% |
| Mildly Bullish + Strong Bullish | 1 | 1 | 100.0% | +1.38% |
| Mildly Bullish + Bullish | 2 | 2 | 100.0% | +0.42% |
| Mildly Bullish + Mildly Bullish | 1 | 1 | 100.0% | +1.03% |

### Bearish Alignment: Exceeded Half on Expiry (49 days)

| Combo (FII + PRO) | N | Won | WR% | Avg Close% |
|--------------------|--:|----:|----:|----------:|
| Strong Bearish + Strong Bearish | 7 | 7 | 100.0% | -0.60% |
| Strong Bearish + Bearish | 4 | 3 | 75.0% | -0.27% |
| Strong Bearish + Mildly Bearish | 1 | 1 | 100.0% | -0.96% |
| Bearish + Strong Bearish | 15 | 12 | 80.0% | -0.50% |
| Bearish + Bearish | 3 | 2 | 66.7% | -0.29% |
| Bearish + Mildly Bearish | 3 | 2 | 66.7% | -0.22% |
| Mildly Bearish + Strong Bearish | 10 | 7 | 70.0% | -0.54% |
| Mildly Bearish + Bearish | 5 | 5 | 100.0% | -0.50% |
| Mildly Bearish + Mildly Bearish | 1 | 0 | 0.0% | +0.09% |

---

*Report generated from corrected alignment data on 2026-09-11 at 22:41:53*