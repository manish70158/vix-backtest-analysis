# VIX Underestimation × FII/PRO Combination Analysis

> **Dataset**: `vix_fii_t1_intraday_daily_results.csv` — 1,485 trading days (Aug 2020 – Sep 2026)
>
> **Definition**: VIX "Underestimated" = actual intraday range exceeded VIX-predicted move by > 0.5%
> (i.e., the market moved more than VIX implied it would)
>
> **T-1 data caveat**: FII/PRO views are derived from T+1 settlement data — alignment
> is known only after the trading day. This analysis identifies historical patterns,
> not real-time predictive signals.

---

## Overall VIX Accuracy Distribution

| Category | Days | % of Total | Avg Range% | Avg Diff% |
|----------|-----:|-----------:|-----------:|----------:|
| **Underestimated** | **278** | **18.7%** | 1.84% | +0.96% |
| Overestimated | 1,207 | 81.3% | 0.83% | -0.22% |
| **Total** | **1,485** | **100%** | 1.02% | 0.00% |

VIX overestimates intraday range ~81% of the time. The 18.7% of days where it underestimates
are the high-volatility outlier days — and understanding which FII/PRO combinations precede
these events is the focus of this report.

---

## Alignment Category → Underestimation Rate

Which FII/PRO alignment type is most associated with VIX blowouts?

| Alignment Category | Total Days | Underestimated | Rate | Share of All U/E | Avg Range (U/E) | Avg Diff (U/E) |
|--------------------|----------:|--------------:|-----:|-----------------:|----------------:|---------------:|
| **Bearish Alignment** | 324 | 71 | **21.9%** | 25.5% | 1.76% | +0.90% |
| Mixed (Opposing) | 102 | 20 | 19.6% | 7.2% | 1.80% | +0.96% |
| Both Neutral | 179 | 34 | 19.0% | 12.2% | 1.85% | +0.91% |
| FII Neutral + PRO Directional | 446 | 82 | 18.4% | 29.5% | 1.94% | +0.99% |
| **Bullish Alignment** | 328 | 58 | **17.7%** | 20.9% | 1.80% | +0.98% |
| FII Directional + PRO Neutral | 106 | 13 | 12.3% | 4.7% | 1.94% | +1.04% |

**Key insight**: Bearish alignment has the highest underestimation rate (21.9%). When both
FII and PRO lean bearish, the market is more likely to produce a larger-than-expected move.
Conversely, when FII has a solo directional view and PRO is neutral, VIX underestimates least often (12.3%).

---

## FII View × PRO View: Full Cross-Tab (min 20 days)

Ranked by underestimation rate:

| FII View | PRO View | Total | Under. | **Rate** | Avg Range% | Avg VIX Pred% | Avg Diff% |
|----------|----------|------:|-------:|--------:|-----------:|--------------:|----------:|
| Mildly Bullish | Bullish | 26 | 8 | **30.8%** | 1.15% | 0.87% | +0.28% |
| Mildly Bearish | Strong Bearish | 49 | 15 | **30.6%** | 1.23% | 0.84% | +0.39% |
| Neutral | Mildly Bullish | 43 | 12 | **27.9%** | 1.29% | 0.98% | +0.31% |
| Strong Bearish | Strong Bearish | 90 | 22 | **24.4%** | 1.06% | 0.78% | +0.28% |
| Bearish | Bearish | 30 | 7 | **23.3%** | 1.03% | 0.77% | +0.27% |
| Mildly Bearish | Bearish | 26 | 6 | **23.1%** | 1.03% | 0.84% | +0.19% |
| Mildly Bullish | Strong Bullish | 42 | 9 | 21.4% | 1.00% | 0.77% | +0.23% |
| Neutral | Bearish | 88 | 18 | 20.5% | 1.08% | 0.87% | +0.21% |
| Neutral | Mildly Bearish | 60 | 12 | 20.0% | 1.18% | 0.90% | +0.28% |
| Neutral | Strong Bearish | 83 | 16 | 19.3% | 0.99% | 0.79% | +0.20% |
| Neutral | Neutral | 179 | 34 | 19.0% | 1.06% | 0.91% | +0.15% |
| Neutral | Bullish | 85 | 15 | 17.6% | 1.03% | 0.87% | +0.16% |
| Strong Bullish | Strong Bullish | 70 | 12 | 17.1% | 0.99% | 0.75% | +0.24% |
| Bearish | Strong Bearish | 94 | 16 | 17.0% | 1.01% | 0.82% | +0.18% |
| Bullish | Strong Bullish | 133 | 20 | 15.0% | 0.88% | 0.78% | +0.10% |
| Mildly Bullish | Neutral | 29 | 4 | 13.8% | 0.98% | 0.90% | +0.08% |
| Bullish | Bullish | 29 | 4 | 13.8% | 0.94% | 0.83% | +0.11% |
| Bearish | Neutral | 24 | 3 | 12.5% | 1.14% | 0.83% | +0.32% |
| Neutral | Strong Bullish | 87 | 9 | 10.3% | 0.94% | 0.82% | +0.12% |
| Bullish | Neutral | 21 | 0 | **0.0%** | 0.82% | 0.85% | -0.04% |

### Notable Patterns

- **Highest rate**: `Mildly Bullish × Bullish` (30.8%) and `Mildly Bearish × Strong Bearish` (30.6%)
  — partial conviction from one side + full conviction from the other
- **Zero underestimation**: `Bullish FII + Neutral PRO` (0/21 days) — when FII is bullish
  alone and PRO has no view, the market stays within VIX bounds
- **Large sample bearish**: `Strong Bearish × Strong Bearish` (22/90 = 24.4%) — the most
  reliable large-sample signal for VIX underestimation

---

## Deep Dive: Bearish Alignment (Highest Underestimation Rate)

When both FII and PRO lean bearish (324 days total):

| Metric | Value |
|--------|------:|
| Total bearish alignment days | 324 |
| Underestimated | 71 (21.9%) |
| Avg range on underestimated days | 1.76% |
| Avg VIX miss (diff%) | +0.90% |
| Avg VIX predicted | 0.86% |
| Top to Down on U/E days | 45 (63.4%) |
| Down to Up on U/E days | 26 (36.6%) |
| Red (down close) on U/E days | 45 (63.4%) |

### Bearish Sub-Combinations (Underestimated Only)

| FII View | PRO View | Under. / Total | Rate |
|----------|----------|:--------------:|-----:|
| Mildly Bearish | Strong Bearish | 15 / 49 | **30.6%** |
| Strong Bearish | Strong Bearish | 22 / 90 | **24.4%** |
| Bearish | Bearish | 7 / 30 | **23.3%** |
| Mildly Bearish | Bearish | 6 / 26 | **23.1%** |
| Bearish | Strong Bearish | 16 / 94 | 17.0% |
| Bearish | Mildly Bearish | 3 / 8 | 37.5% |
| Mildly Bearish | Mildly Bearish | 1 / 11 | 9.1% |
| Strong Bearish | Bearish | 1 / 11 | 9.1% |

**Takeaway**: When both sides are bearish but PRO shows stronger conviction than FII
(e.g., `Mildly Bearish FII × Strong Bearish PRO`), VIX underestimation rate is highest.
When the conviction is lopsided with PRO being more aggressive, expect bigger-than-predicted moves.

---

## Deep Dive: Bullish Alignment

When both FII and PRO lean bullish (328 days total):

| Metric | Value |
|--------|------:|
| Total bullish alignment days | 328 |
| Underestimated | 58 (17.7%) |
| Avg range on underestimated days | 1.80% |
| Avg VIX miss (diff%) | +0.98% |
| Red (down close) on U/E days | 31 (53.4%) |
| Green (up close) on U/E days | 27 (46.6%) |

When VIX underestimates on bullish alignment days, the market still closes RED 53.4% of the time
— meaning the excess volatility tends to work against the bullish institutional view.

---

## Strong Views (Excluding "Mildly") vs Underestimation

| Combination | Total | Under. | Rate | Avg Range% |
|-------------|------:|-------:|-----:|-----------:|
| Both Strong Bearish | 225 | 46 | **20.4%** | 1.03% |
| Strong FII Bear + Strong PRO Bull | 23 | 5 | **21.7%** | 1.00% |
| Both Strong Bullish | 237 | 36 | 15.2% | 0.92% |
| Strong FII Bull + Strong PRO Bear | 27 | 2 | 7.4% | 0.82% |

Strong bearish conviction (both or opposing) produces VIX underestimation 20-22% of the time.
Strong bullish conviction from FII with PRO opposing produces the lowest rate (7.4%) — these
days tend to be range-bound.

---

## Combined Composite Score (FII + PRO) vs Underestimation

| Composite Bucket | Total | Under. | Rate | Avg Range% |
|------------------|------:|-------:|-----:|-----------:|
| < -200K (extreme bearish) | 224 | 46 | **20.5%** | 1.02% |
| -200K to -100K | 200 | 45 | **22.5%** | 1.06% |
| -100K to -50K | 154 | 27 | 17.5% | 1.08% |
| -50K to 0 | 165 | 36 | **21.8%** | 1.11% |
| 0 to 50K | 163 | 27 | 16.6% | 0.99% |
| 50K to 100K | 134 | 26 | 19.4% | 1.08% |
| 100K to 200K | 203 | 34 | 16.7% | 0.99% |
| > 200K (extreme bullish) | 242 | 37 | **15.3%** | 0.93% |

**Key finding**: The negative composite range (-200K to -100K) has the highest underestimation
rate at 22.5%. The -50K to 0 range (mildly bearish) also shows elevated risk at 21.8%.
Extreme bullish composites (>200K) have the lowest underestimation rate (15.3%).

**The pattern is clear**: bearish institutional positioning is a stronger predictor of
VIX underestimation than bullish positioning.

---

## VIX Regime Analysis

| VIX Regime | Total | Under. | Rate | Avg Range% | Avg Diff% |
|------------|------:|-------:|-----:|-----------:|----------:|
| **Elevated (20-30)** | 286 | 74 | **25.9%** | 1.41% | +0.24% |
| Normal (15-20) | 435 | 86 | 19.8% | 1.09% | +0.18% |
| Low (<15) | 763 | 118 | 15.5% | 0.84% | +0.18% |
| High (>30) | 1 | 0 | 0.0% | 1.57% | -0.10% |

Elevated VIX (20-30) has the highest underestimation rate. When VIX is already signaling
heightened volatility, it still underestimates 1 in 4 trading days.

---

## Direction & Close Outcome on Underestimated Days

| Move Direction | Count | % | Avg Range% | Avg Diff% |
|----------------|------:|--:|-----------:|----------:|
| **Top to Down** | 164 | **59.0%** | 1.90% | +1.03% |
| Down to Up | 114 | 41.0% | 1.76% | +0.85% |

When VIX underestimates, the dominant pattern is **Top to Down** (59%) — meaning the market
opens, moves up initially, then sells off hard enough to produce a range that exceeds VIX predictions.

### Nifty Day Color on Underestimated Days by Alignment

| Alignment | Green (Up) | Red (Down) |
|-----------|----------:|----------:|
| Bearish Alignment | 26 (36.6%) | **45 (63.4%)** |
| Both Neutral | 14 (41.2%) | **20 (58.8%)** |
| FII Neutral + PRO Directional | 37 (45.1%) | **45 (54.9%)** |
| Bullish Alignment | 27 (46.6%) | **31 (53.4%)** |

Underestimated days are disproportionately **red days** across all alignment categories,
most pronounced under bearish alignment (63.4% red).

---

## Underestimation Direction When FII & PRO Are Aligned

When both institutional players agree on direction, which way does the VIX blowout actually go?

### Bearish Alignment (both bearish) — 71 underestimation days / 324 total

| Metric | Count | % |
|--------|------:|--:|
| **Top to Down** (opens up, sells off) | **45** | **63.4%** |
| Down to Up (opens down, recovers) | 26 | 36.6% |
| **Red close (down)** | **45** | **63.4%** |
| Green close (up) | 26 | 36.6% |

When both FII and PRO lean bearish and VIX underestimates, the excess move is **predominantly
downward** — the market sells off harder than VIX predicted, closing red nearly 2 out of 3 times.

### Bullish Alignment (both bullish) — 58 underestimation days / 328 total

| Metric | Count | % |
|--------|------:|--:|
| **Red close (down)** | **31** | **53.4%** |
| Green close (up) | 27 | 46.6% |

**Counterintuitive finding**: Even when both FII and PRO are bullish, underestimation days still
close **red more often than green** (53.4% vs 46.6%). The excess volatility tends to work
*against* the bullish institutional view rather than amplify it.

### Conclusion: VIX Underestimation Has a Bearish Bias Regardless of Alignment

| Alignment | Red Close on U/E Days | Green Close on U/E Days |
|-----------|----------------------:|------------------------:|
| Bearish Alignment | **63.4%** | 36.6% |
| Both Neutral | **58.8%** | 41.2% |
| FII Neutral + PRO Directional | **54.9%** | 45.1% |
| Bullish Alignment | **53.4%** | 46.6% |

**Regardless of whether institutions are aligned bullish or bearish, VIX underestimation
skews bearish.** When both are bearish-aligned, the downside bias is strong (63.4% red).
When both are bullish-aligned, the market still closes red 53.4% of the time on blowout days.
The excess move that VIX failed to predict is more frequently a sell-off than a rally across
all alignment types — suggesting that when volatility surprises to the upside, it is
predominantly fear-driven (selling) rather than greed-driven (buying).

---

## FII Stance (Granular) → Top Underestimation Combinations (min 10 days)

| FII Stance | PRO Stance | Total | Under. | Rate |
|------------|-----------|------:|-------:|-----:|
| FII Very Bearish (sold fut + bought puts) | PRO Mildly Bullish | 10 | 6 | **60.0%** |
| FII Hedging (bought puts >20K) | PRO Very Bearish (sold fut + bought puts) | 15 | 7 | **46.7%** |
| FII Very Bearish (sold fut + bought puts) | PRO Hedging (bought puts >20K) | 92 | 29 | **31.5%** |
| FII Bearish (sold fut >10K) | PRO Confident (sold puts >20K) | 28 | 8 | **28.6%** |
| FII Neutral | PRO Mildly Bearish | 57 | 16 | **28.1%** |
| FII Very Bearish (sold fut + bought puts) | PRO Bullish (bought fut + sold puts) | 11 | 3 | 27.3% |
| FII Confident (sold puts >20K) | PRO Bearish (sold fut >10K) | 15 | 4 | 26.7% |
| FII Bullish (bought fut + sold puts) | PRO Very Bearish (sold fut + bought puts) | 20 | 5 | 25.0% |
| FII Very Bearish (sold fut + bought puts) | PRO Confident (sold puts >20K) | 21 | 5 | 23.8% |
| FII Mildly Bearish | PRO Confident (sold puts >20K) | 21 | 5 | 23.8% |
| FII Hedging (bought puts >20K) | PRO Mildly Bearish | 31 | 7 | 22.6% |

### Most Dangerous Combination

**FII Very Bearish × PRO Mildly Bullish** (60% underestimation rate, 6/10 days):
When FII is aggressively selling futures AND buying puts, but PRO remains mildly bullish — this
extreme divergence produces an outsized move 60% of the time. The opposing strong conviction
creates maximum uncertainty, and the market overshoots VIX predictions.

**FII Hedging × PRO Very Bearish** (46.7%, 7/15 days):
When FII is buying protective puts while PRO is aggressively bearish — both sides loading puts
from different angles — this produces the second-highest underestimation rate.

---

## Temporal Patterns

### Day of Week

| Day | Total | Under. | Rate |
|-----|------:|-------:|-----:|
| Friday | 291 | 63 | **21.6%** |
| Monday | 297 | 62 | **20.9%** |
| Thursday | 296 | 58 | 19.6% |
| Tuesday | 299 | 54 | 18.1% |
| Wednesday | 295 | 40 | **13.6%** |

Fridays and Mondays have the highest underestimation rates. Wednesdays are the calmest.
Weekend positioning effects (Monday) and pre-weekend gamma risk (Friday) likely drive this.

### Year-over-Year

| Year | Total | Under. | Rate | Avg Range% | Avg Diff% |
|------|------:|-------:|-----:|-----------:|----------:|
| 2024 | 244 | 62 | **25.4%** | 1.01% | +0.24% |
| 2021 | 245 | 59 | **24.1%** | 1.15% | +0.21% |
| 2026 | 163 | 34 | 20.9% | 1.02% | +0.22% |
| 2022 | 243 | 48 | 19.8% | 1.20% | +0.19% |
| 2020 | 102 | 17 | 16.7% | 1.21% | +0.12% |
| 2025 | 245 | 30 | 12.2% | 0.88% | +0.17% |
| 2023 | 243 | 28 | 11.5% | 0.80% | +0.15% |

2024 had the highest underestimation rate (25.4%) — a year with multiple surprise events.
2023 and 2025 were the most well-behaved (VIX was accurate ~88% of the time).

### Expiry vs Non-Expiry

| Context | Total | Under. | Rate | Avg Range% |
|---------|------:|-------:|-----:|-----------:|
| Expiry | 312 | 64 | **20.5%** | 1.02% |
| Non-Expiry | 1,173 | 214 | 18.2% | 1.02% |

Expiry days show slightly higher underestimation (20.5% vs 18.2%), consistent with
gamma-driven moves exceeding VIX-implied ranges.

---

## Top 20 Largest VIX Misses (Extreme Underestimation Days)

| Date | FII View | PRO View | VIX Pred% | Actual Range% | Miss | Direction | Close |
|------|----------|----------|----------:|--------------:|-----:|-----------|-------|
| 2024-06-04 | Strong Bullish | Strong Bullish | 1.10% | 8.19% | **+7.09%** | Top to Down | Red |
| 2020-12-21 | Neutral | Mildly Bearish | 0.97% | 4.67% | +3.70% | Top to Down | Red |
| 2020-08-31 | Neutral | Mildly Bullish | 0.96% | 3.97% | +3.01% | Top to Down | Red |
| 2026-02-01 | Mildly Bearish | Strong Bearish | 0.71% | 3.43% | +2.72% | Top to Down | Red |
| 2023-02-01 | Neutral | Bullish | 0.88% | 3.47% | +2.59% | Top to Down | Red |
| 2024-06-05 | Strong Bearish | Strong Bearish | 1.40% | 3.97% | +2.57% | Down to Up | Green |
| 2022-01-24 | Neutral | Neutral | 0.99% | 3.41% | +2.42% | Top to Down | Red |
| 2022-06-16 | Neutral | Mildly Bullish | 1.16% | 3.33% | +2.17% | Top to Down | Red |
| 2021-11-22 | Neutral | Mildly Bearish | 0.78% | 2.89% | +2.11% | Top to Down | Red |
| 2021-03-19 | Neutral | Strong Bullish | 1.05% | 3.02% | +1.97% | Down to Up | Green |
| 2022-02-15 | Neutral | Strong Bearish | 1.20% | 3.15% | +1.95% | Down to Up | Green |
| 2020-10-15 | Neutral | Neutral | 1.06% | 3.00% | +1.94% | Top to Down | Red |
| 2026-02-03 | Bearish | Neutral | 0.73% | 2.66% | +1.93% | Top to Down | Red |
| 2022-05-04 | Neutral | Strong Bearish | 1.06% | 2.95% | +1.89% | Top to Down | Red |
| 2024-01-23 | Neutral | Bearish | 0.72% | 2.57% | +1.85% | Top to Down | Red |
| 2021-02-26 | Neutral | Bearish | 1.20% | 3.03% | +1.83% | Top to Down | Red |
| 2024-12-13 | Bearish | Bullish | 0.69% | 2.50% | +1.81% | Down to Up | Green |
| 2022-02-24 | Mildly Bearish | Strong Bearish | 1.28% | 3.01% | +1.73% | Top to Down | Red |
| 2024-11-22 | Mildly Bearish | Strong Bullish | 0.84% | 2.55% | +1.71% | Down to Up | Green |
| 2024-03-13 | Bullish | Strong Bullish | 0.71% | 2.41% | +1.70% | Top to Down | Red |

**Observation**: The largest VIX miss ever (Jun 4, 2024: +7.09%) occurred when both FII
and PRO were **Strong Bullish** — election result day. Of the top 20, **15 were red days**
and **15 were Top to Down** moves. Many of the extreme misses happen when FII is Neutral —
suggesting that exogenous shocks (not institutional positioning) drive the largest blowouts.

---

## Key Findings

1. **Bearish alignment = highest underestimation risk** (21.9%): When both FII and PRO
   lean bearish, VIX underestimates 1 in 5 days. The market produces outsized moves,
   predominantly downward (63.4% red, 63.4% Top to Down).

2. **Partial conviction is most dangerous**: Combinations where one side is "Mildly" and the
   other is "Strong" (e.g., Mildly Bearish × Strong Bearish at 30.6%) show higher
   underestimation rates than fully aligned strong views. The gap in conviction intensity
   appears to produce unstable price action.

3. **Extreme stance divergence**: When FII is Very Bearish but PRO is Mildly Bullish (60%
   underestimation), or FII is Hedging while PRO is Very Bearish (46.7%) — these tension
   points produce the most frequent VIX blowouts. The conflicting protective positioning
   from multiple angles amplifies actual volatility.

4. **Negative composite scores predict blowouts**: The -200K to -100K combined composite
   range has the highest underestimation rate (22.5%). Bearish institutional flow is a
   stronger predictor of excess volatility than bullish flow.

5. **Bullish alignment is calmer**: At 17.7% underestimation, bullish alignment days are
   3 percentage points less likely to produce VIX blowouts. When both sides are buying,
   the market moves within bounds more often.

6. **FII Bullish + PRO Neutral = safest**: Zero underestimation in 21 days. When FII is
   bullish and PRO has no view, the market stays range-bound without exception.

7. **Elevated VIX (20-30) amplifies**: Even when VIX is already signaling high volatility,
   it underestimates 25.9% of the time. The "volatility of volatility" is highest in the
   20-30 VIX band.

8. **Temporal clusters**: Fridays (21.6%) and Mondays (20.9%) are most prone to underestimation.
   Wednesdays (13.6%) are safest. 2024 and 2021 were the most unpredictable years.

9. **Extreme outliers don't follow alignment patterns**: The largest VIX misses (>+2%)
   often occur when FII is Neutral — suggesting these are exogenous shock events
   (geopolitical, macro, election results) rather than positioning-driven moves.

## Trading Implications

- When both FII and PRO are bearish (especially with mixed conviction intensity), **size
  options wider** — the VIX-implied range is likely too narrow ~22% of the time
- When FII is Bullish + PRO is Neutral, **iron condors and range-bound strategies are safer**
  — VIX never underestimated in this combination
- On Fridays with bearish alignment and elevated VIX (20-30), the probability of an
  outsized move is highest — consider buying premium or widening stop-losses
- **This is retrospective analysis using T+1 data** — use as a volatility framework,
  not as an intraday entry signal

---

*Generated: 2026-09-05 | Data: Aug 2020 – Sep 2026 | Source: vix_fii_t1_intraday_daily_results.csv*
