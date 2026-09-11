# Bullish Alignment + VIX Half-Range Exhaustion: Detailed Examples

> **Context**: When both FII and PRO are bullish (T+1 data), we check whether
> the market's upward move exceeded half the VIX-predicted daily range before
> any reversal. This document walks through real examples from all four outcome
> quadrants.

---

## How It Works

1. **FII and PRO both bullish** (known after T+1 settlement)
2. **VIX predicts a daily range** — e.g., VIX at 15 implies ~0.94% expected move
3. **Half threshold** = VIX predicted range / 2
4. **Check**: Did the bullish move (high from open) exceed that half threshold?

```
VIX Predicted Range = 0.86%
Half Threshold      = 0.43%
Intraday High%      = 0.60%  ← Exceeded 0.43% → "Exceeded Half"

vs.

VIX Predicted Range = 1.30%
Half Threshold      = 0.65%
Intraday High%      = 0.15%  ← Did NOT reach 0.65% → "Reversed Before Half"
```

---

## Summary Table (319 Bullish Alignment Days)

| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |
|----------------|------:|--:|--------------------:|----:|----------------:|
| Exceeded Half then Reversed | 116 | 36.4% | 101 | **87.1%** | +0.51% |
| Reversed Before Half | 203 | 63.6% | 44 | **21.7%** | -0.41% |

**Key takeaway**: If the bullish move exceeded half the VIX range, the market closed bullish 87.1% of the time. If it didn't reach that level, the market closed bearish 78.3% of the time.

---

## Quadrant 1: Exceeded Half + Worked and Remained (101 days, 87.1% of Exceeded Half)

**This is the high-conviction bullish outcome.** The market moved up past the VIX half-threshold and held those gains by close.

### Recent Examples (2025-2026)

| Date | FII | PRO | VIX Predicted% | High% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|:----------:|:---:|
| 2026-08-07 | Strong Bullish | Strong Bullish | 0.64% | +0.37% | **+0.13%** | N/A | No |
| 2026-07-30 | Strong Bullish | Strong Bullish | 0.63% | +0.39% | **+0.19%** | N/A | No |
| 2026-07-13 | Bullish | Bullish | 0.64% | +0.92% | **+0.71%** | N/A | No |
| 2026-07-10 | Bullish | Bullish | 0.70% | +0.43% | **+0.36%** | N/A | No |
| 2026-05-25 | Strong Bullish | Strong Bullish | 0.94% | +0.48% | **+0.46%** | N/A | No |
| 2026-04-13 | Bullish | Bullish | 0.99% | +1.35% | **+0.97%** | N/A | Yes |
| 2026-04-06 | Mildly Bullish | Strong Bullish | 1.34% | +0.96% | **+0.79%** | N/A | No |
| 2026-03-18 | Strong Bullish | Strong Bullish | 1.04% | +0.97% | **+0.56%** | N/A | No |
| 2026-02-17 | Bullish | Strong Bullish | 0.70% | +0.49% | **+0.30%** | N/A | Yes |
| 2026-02-04 | Strong Bullish | Bullish | 0.68% | +0.56% | **+0.24%** | N/A | No |

---

## Quadrant 2: Exceeded Half + Reversed by Close (15 days, 12.9% of Exceeded Half)

**The rare failure case.** The market exceeded the VIX half-threshold to the upside but then completely reversed and closed bearish. Only 15 out of 116 times.

### All 15 Instances

| Date | FII | PRO | VIX Predicted% | High% | Low% | Close% | Cross Time | Expiry? |
|------|-----|-----|------:|------:|------:|------:|:----------:|:---:|
| 2021-07-30 | Bullish | Strong Bullish | 0.68% | +0.39% | -0.35% | **-0.17%** | N/A | No |
| 2021-08-25 | Mildly Bullish | Strong Bullish | 0.69% | +0.35% | -0.22% | **-0.11%** | N/A | No |
| 2021-11-30 | Bullish | Bullish | 1.09% | +1.60% | -0.69% | **-0.45%** | N/A | No |
| 2022-05-23 | Strong Bullish | Strong Bullish | 1.21% | +0.76% | -0.64% | **-0.61%** | N/A | No |
| 2024-04-30 | Strong Bullish | Strong Bullish | 0.64% | +0.46% | -0.49% | **-0.41%** | N/A | No |
| 2024-06-12 | Bullish | Strong Bullish | 0.77% | +0.42% | -0.21% | **-0.15%** | N/A | No |
| 2024-11-19 | Bullish | Strong Bullish | 0.79% | +1.07% | -0.28% | **-0.26%** | N/A | No |
| 2024-12-24 | Bullish | Strong Bullish | 0.71% | +0.41% | -0.35% | **-0.16%** | N/A | No |
| 2025-01-24 | Strong Bullish | Strong Bullish | 0.87% | +0.70% | -0.58% | **-0.40%** | N/A | No |
| 2025-08-12 | Bullish | Strong Bullish | 0.64% | +0.57% | -0.40% | **-0.32%** | N/A | No |
| 2025-09-02 | Strong Bullish | Bullish | 0.59% | +0.42% | -0.53% | **-0.32%** | N/A | Yes |
| 2025-11-13 | Bullish | Bullish | 0.63% | +0.40% | -0.38% | **-0.08%** | N/A | No |
| 2025-12-10 | Bullish | Strong Bullish | 0.57% | +0.32% | -0.50% | **-0.47%** | N/A | No |
| 2026-04-28 | Bullish | Strong Bullish | 0.96% | +0.55% | -0.39% | **-0.14%** | N/A | Yes |
| 2026-06-25 | Bullish | Strong Bullish | 0.70% | +0.56% | -0.36% | **-0.30%** | N/A | No |

---

*Report generated from corrected alignment data on 2026-09-11 at 22:41:53*