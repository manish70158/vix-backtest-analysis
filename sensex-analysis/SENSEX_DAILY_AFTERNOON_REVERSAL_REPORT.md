# Sensex Daily Afternoon Reversal Analysis — ALL Trading Days

**Analyzed 1470 trading days** (Nifty 5-min proxy for intraday timing)
**Date range**: 2020-08-06 to 2026-08-21

> Uses Nifty 5-min data as timing proxy. Sensex expiry dates tagged from CSV.

**Day type breakdown:**
- No Expiry: 870
- Nifty-Only Expiry: 308
- Sensex Expiry: 291
- Dual Expiry (Sensex+Nifty): 1

## 1. Executive Summary

Across **all 1470 trading days**:
- Top to Down afternoons: 682 (46.4%)
- Down to Up afternoons: 727 (49.5%)
- Flat afternoons: 61 (4.1%)

**Primary reversal zone:** `14:00` — 703 of 1409 days (49.9%)

**Top 3 inflection times:**

| Time | Count | % |
|------|------:|----:|
| 14:00 | 418 | 29.7% |
| 14:05 | 169 | 12.0% |
| 14:15 | 129 | 9.2% |

## 2. Four-Way Day Type Comparison

| Metric | Sensex Expiry (all) |   - Sensex-Only |   - Dual (Sensex+Nifty) | Nifty-Only Expiry | No Expiry | All Days |
|--------| ---: | ---: | ---: | ---: | ---: | ---: |
| Total | 292 | 291 | 1 | 308 | 870 | 1470 |
| TTD % | 50.3% | 50.2% | 100.0% | 47.1% | 44.8% | 46.4% |
| DTU % | 45.5% | 45.7% | 0.0% | 49.0% | 50.9% | 49.5% |
| Concordance | 67.9% | 67.7% | 100.0% | 68.9% | 67.7% | 68.0% |
| Avg move % | 0.232% | 0.232% | 0.058% | 0.249% | 0.257% | 0.251% |
| Median move % | 0.168% | 0.168% | 0.058% | 0.184% | 0.19% | 0.183% |

### Top 3 Inflection Times by Day Type

- **Sensex Expiry (all)**: 14:00 (79), 14:05 (31), 14:20 (23)
- **- Sensex-Only**: 14:00 (79), 14:05 (31), 14:20 (23)
- **- Dual (Sensex+Nifty)**: 14:45 (1)
- **Nifty-Only Expiry**: 14:00 (88), 14:15 (31), 14:05 (27)
- **No Expiry**: 14:00 (251), 14:05 (111), 14:10 (82)

## 3. Overall Timing Distribution (5-min granularity)

### All Trading Days

| Time | Count | % |
|------|------:|----:|
| 14:00 | 418 | 29.7% |
| 14:05 | 169 | 12.0% |
| 14:10 | 116 | 8.2% |
| 14:15 | 129 | 9.2% |
| 14:20 | 78 | 5.5% |
| 14:25 | 68 | 4.8% |
| 14:30 | 74 | 5.3% |
| 14:35 | 63 | 4.5% |
| 14:40 | 47 | 3.3% |
| 14:45 | 52 | 3.7% |
| 14:50 | 47 | 3.3% |
| 14:55 | 35 | 2.5% |
| 15:00 | 52 | 3.7% |
| 15:05 | 22 | 1.6% |
| 15:10 | 17 | 1.2% |
| 15:15 | 7 | 0.5% |
| 15:20 | 7 | 0.5% |
| 15:25 | 8 | 0.6% |

## 4. Timing Distribution by Afternoon Direction

### Top to Down

| Time | Count | % |
|------|------:|----:|
| 14:00 | 203 | 29.8% |
| 14:05 | 81 | 11.9% |
| 14:10 | 60 | 8.8% |
| 14:15 | 73 | 10.7% |
| 14:20 | 33 | 4.8% |
| 14:25 | 32 | 4.7% |
| 14:30 | 40 | 5.9% |
| 14:35 | 27 | 4.0% |
| 14:40 | 18 | 2.6% |
| 14:45 | 21 | 3.1% |
| 14:50 | 23 | 3.4% |
| 14:55 | 14 | 2.1% |
| 15:00 | 30 | 4.4% |
| 15:05 | 11 | 1.6% |
| 15:10 | 7 | 1.0% |
| 15:15 | 2 | 0.3% |
| 15:20 | 4 | 0.6% |
| 15:25 | 3 | 0.4% |

### Down to Up

| Time | Count | % |
|------|------:|----:|
| 14:00 | 215 | 29.6% |
| 14:05 | 88 | 12.1% |
| 14:10 | 56 | 7.7% |
| 14:15 | 56 | 7.7% |
| 14:20 | 45 | 6.2% |
| 14:25 | 36 | 5.0% |
| 14:30 | 34 | 4.7% |
| 14:35 | 36 | 5.0% |
| 14:40 | 29 | 4.0% |
| 14:45 | 31 | 4.3% |
| 14:50 | 24 | 3.3% |
| 14:55 | 21 | 2.9% |
| 15:00 | 22 | 3.0% |
| 15:05 | 11 | 1.5% |
| 15:10 | 10 | 1.4% |
| 15:15 | 5 | 0.7% |
| 15:20 | 3 | 0.4% |
| 15:25 | 5 | 0.7% |

## 5. Timing Distribution by Day Type

### Sensex Expiry

| Time | Count | % |
|------|------:|----:|
| 14:00 | 79 | 28.3% |
| 14:05 | 31 | 11.1% |
| 14:10 | 16 | 5.7% |
| 14:15 | 22 | 7.9% |
| 14:20 | 23 | 8.2% |
| 14:25 | 16 | 5.7% |
| 14:30 | 17 | 6.1% |
| 14:35 | 11 | 3.9% |
| 14:40 | 12 | 4.3% |
| 14:45 | 8 | 2.9% |
| 14:50 | 9 | 3.2% |
| 14:55 | 7 | 2.5% |
| 15:00 | 10 | 3.6% |
| 15:05 | 6 | 2.2% |
| 15:10 | 7 | 2.5% |
| 15:15 | 2 | 0.7% |
| 15:20 | 2 | 0.7% |
| 15:25 | 1 | 0.4% |

### Nifty-Only Expiry

| Time | Count | % |
|------|------:|----:|
| 14:00 | 88 | 29.7% |
| 14:05 | 27 | 9.1% |
| 14:10 | 18 | 6.1% |
| 14:15 | 31 | 10.5% |
| 14:20 | 13 | 4.4% |
| 14:25 | 15 | 5.1% |
| 14:30 | 18 | 6.1% |
| 14:35 | 19 | 6.4% |
| 14:40 | 10 | 3.4% |
| 14:45 | 13 | 4.4% |
| 14:50 | 9 | 3.0% |
| 14:55 | 5 | 1.7% |
| 15:00 | 12 | 4.1% |
| 15:05 | 9 | 3.0% |
| 15:10 | 2 | 0.7% |
| 15:15 | 2 | 0.7% |
| 15:20 | 2 | 0.7% |
| 15:25 | 3 | 1.0% |

### No Expiry

| Time | Count | % |
|------|------:|----:|
| 14:00 | 251 | 30.1% |
| 14:05 | 111 | 13.3% |
| 14:10 | 82 | 9.8% |
| 14:15 | 76 | 9.1% |
| 14:20 | 42 | 5.0% |
| 14:25 | 37 | 4.4% |
| 14:30 | 39 | 4.7% |
| 14:35 | 33 | 4.0% |
| 14:40 | 25 | 3.0% |
| 14:45 | 30 | 3.6% |
| 14:50 | 29 | 3.5% |
| 14:55 | 23 | 2.8% |
| 15:00 | 30 | 3.6% |
| 15:05 | 7 | 0.8% |
| 15:10 | 8 | 1.0% |
| 15:15 | 3 | 0.4% |
| 15:20 | 3 | 0.4% |
| 15:25 | 4 | 0.5% |

## 6. Timing Distribution by Day of Week

### Day: Monday

| Time | Count | % |
|------|------:|----:|
| 14:00 | 79 | 28.4% |
| 14:05 | 43 | 15.5% |
| 14:10 | 26 | 9.4% |
| 14:15 | 24 | 8.6% |
| 14:20 | 14 | 5.0% |
| 14:25 | 12 | 4.3% |
| 14:30 | 12 | 4.3% |
| 14:35 | 12 | 4.3% |
| 14:40 | 6 | 2.2% |
| 14:45 | 11 | 4.0% |
| 14:50 | 10 | 3.6% |
| 14:55 | 11 | 4.0% |
| 15:00 | 11 | 4.0% |
| 15:05 | 3 | 1.1% |
| 15:10 | 4 | 1.4% |
| 15:15 | 0 | 0.0% |
| 15:20 | 0 | 0.0% |
| 15:25 | 0 | 0.0% |

### Day: Tuesday

| Time | Count | % |
|------|------:|----:|
| 14:00 | 86 | 30.5% |
| 14:05 | 38 | 13.5% |
| 14:10 | 20 | 7.1% |
| 14:15 | 28 | 9.9% |
| 14:20 | 16 | 5.7% |
| 14:25 | 13 | 4.6% |
| 14:30 | 16 | 5.7% |
| 14:35 | 11 | 3.9% |
| 14:40 | 10 | 3.5% |
| 14:45 | 11 | 3.9% |
| 14:50 | 7 | 2.5% |
| 14:55 | 5 | 1.8% |
| 15:00 | 8 | 2.8% |
| 15:05 | 3 | 1.1% |
| 15:10 | 1 | 0.4% |
| 15:15 | 3 | 1.1% |
| 15:20 | 5 | 1.8% |
| 15:25 | 1 | 0.4% |

### Day: Wednesday

| Time | Count | % |
|------|------:|----:|
| 14:00 | 80 | 28.2% |
| 14:05 | 32 | 11.3% |
| 14:10 | 32 | 11.3% |
| 14:15 | 29 | 10.2% |
| 14:20 | 12 | 4.2% |
| 14:25 | 12 | 4.2% |
| 14:30 | 15 | 5.3% |
| 14:35 | 13 | 4.6% |
| 14:40 | 9 | 3.2% |
| 14:45 | 7 | 2.5% |
| 14:50 | 13 | 4.6% |
| 14:55 | 6 | 2.1% |
| 15:00 | 16 | 5.6% |
| 15:05 | 5 | 1.8% |
| 15:10 | 2 | 0.7% |
| 15:15 | 0 | 0.0% |
| 15:20 | 0 | 0.0% |
| 15:25 | 1 | 0.4% |

### Day: Thursday

| Time | Count | % |
|------|------:|----:|
| 14:00 | 88 | 31.3% |
| 14:05 | 26 | 9.3% |
| 14:10 | 16 | 5.7% |
| 14:15 | 25 | 8.9% |
| 14:20 | 17 | 6.0% |
| 14:25 | 13 | 4.6% |
| 14:30 | 18 | 6.4% |
| 14:35 | 16 | 5.7% |
| 14:40 | 13 | 4.6% |
| 14:45 | 11 | 3.9% |
| 14:50 | 11 | 3.9% |
| 14:55 | 5 | 1.8% |
| 15:00 | 10 | 3.6% |
| 15:05 | 5 | 1.8% |
| 15:10 | 2 | 0.7% |
| 15:15 | 1 | 0.4% |
| 15:20 | 1 | 0.4% |
| 15:25 | 3 | 1.1% |

### Day: Friday

| Time | Count | % |
|------|------:|----:|
| 14:00 | 84 | 29.8% |
| 14:05 | 30 | 10.6% |
| 14:10 | 22 | 7.8% |
| 14:15 | 23 | 8.2% |
| 14:20 | 19 | 6.7% |
| 14:25 | 18 | 6.4% |
| 14:30 | 13 | 4.6% |
| 14:35 | 10 | 3.5% |
| 14:40 | 9 | 3.2% |
| 14:45 | 12 | 4.3% |
| 14:50 | 6 | 2.1% |
| 14:55 | 8 | 2.8% |
| 15:00 | 7 | 2.5% |
| 15:05 | 6 | 2.1% |
| 15:10 | 8 | 2.8% |
| 15:15 | 3 | 1.1% |
| 15:20 | 1 | 0.4% |
| 15:25 | 3 | 1.1% |

## 7. Move Magnitude from 2 PM to Close by Day Type

| Direction | Day Type | Avg % | Median % | Min % | Max % | Count |
|-----------|----------|------:|---------:|------:|------:|------:|
| Down to Up | Nifty-Only Expiry | 0.258 | 0.189 | 0.011 | 1.216 | 151 |
| Down to Up | No Expiry | 0.245 | 0.198 | 0.011 | 1.298 | 443 |
| Down to Up | Sensex Expiry | 0.217 | 0.168 | 0.012 | 0.76 | 133 |
| Top to Down | Dual Expiry (Sensex+Nifty) | 0.058 | 0.058 | 0.058 | 0.058 | 1 |
| Top to Down | Nifty-Only Expiry | 0.24 | 0.168 | 0.012 | 1.605 | 145 |
| Top to Down | No Expiry | 0.271 | 0.182 | 0.011 | 2.145 | 390 |
| Top to Down | Sensex Expiry | 0.246 | 0.168 | 0.011 | 1.595 | 146 |

## 8. Continuation vs Reversal Breakdown

**Continuation** = afternoon moves in SAME direction as daily open→close
**Reversal** = afternoon moves OPPOSITE to daily open→close

### All Days

- Continuation: 958 (68.0%) | Reversal: 451 (32.0%)

#### Continuation Days

| Daily Direction | Afternoon Direction | Count | Avg Move % |
|-----------------|---------------------|------:|-----------:|
| Top to Down | Top to Down | 470 | 0.309% |
| Down to Up | Down to Up | 488 | 0.268% |

#### Reversal Days

| Daily Direction | Afternoon Direction | Reversal Type | Count | Avg Move % |
|-----------------|---------------------|---------------|------:|-----------:|
| Down to Up (bullish) | Top to Down | Rally faded after 2 PM | 207 | 0.145% |
| Top to Down (bearish) | Down to Up | Sell-off recovered after 2 PM | 230 | 0.19% |

**Of 451 reversal days:**
- 207 (45.9%): Morning rally faded → **afternoon sold off**
- 230 (51.0%): Morning sell-off reversed → **afternoon recovered**

### Sensex Expiry Days

- Continuation: 190 (67.9%) | Reversal: 90 (32.1%)

#### Continuation Days

| Daily Direction | Afternoon Direction | Count | Avg Move % |
|-----------------|---------------------|------:|-----------:|
| Top to Down | Top to Down | 104 | 0.29% |
| Down to Up | Down to Up | 86 | 0.24% |

#### Reversal Days

| Daily Direction | Afternoon Direction | Reversal Type | Count | Avg Move % |
|-----------------|---------------------|---------------|------:|-----------:|
| Down to Up (bullish) | Top to Down | Rally faded after 2 PM | 43 | 0.136% |
| Top to Down (bearish) | Down to Up | Sell-off recovered after 2 PM | 47 | 0.173% |

**Of 90 reversal days:**
- 43 (47.8%): Morning rally faded → **afternoon sold off**
- 47 (52.2%): Morning sell-off reversed → **afternoon recovered**

### Nifty-Only Expiry Days

- Continuation: 204 (68.9%) | Reversal: 92 (31.1%)

#### Continuation Days

| Daily Direction | Afternoon Direction | Count | Avg Move % |
|-----------------|---------------------|------:|-----------:|
| Top to Down | Top to Down | 108 | 0.267% |
| Down to Up | Down to Up | 96 | 0.3% |

#### Reversal Days

| Daily Direction | Afternoon Direction | Reversal Type | Count | Avg Move % |
|-----------------|---------------------|---------------|------:|-----------:|
| Down to Up (bullish) | Top to Down | Rally faded after 2 PM | 37 | 0.16% |
| Top to Down (bearish) | Down to Up | Sell-off recovered after 2 PM | 51 | 0.189% |

**Of 92 reversal days:**
- 37 (40.2%): Morning rally faded → **afternoon sold off**
- 51 (55.4%): Morning sell-off reversed → **afternoon recovered**

### No Expiry Days

- Continuation: 564 (67.7%) | Reversal: 269 (32.3%)

#### Continuation Days

| Daily Direction | Afternoon Direction | Count | Avg Move % |
|-----------------|---------------------|------:|-----------:|
| Top to Down | Top to Down | 258 | 0.334% |
| Down to Up | Down to Up | 306 | 0.266% |

#### Reversal Days

| Daily Direction | Afternoon Direction | Reversal Type | Count | Avg Move % |
|-----------------|---------------------|---------------|------:|-----------:|
| Down to Up (bullish) | Top to Down | Rally faded after 2 PM | 127 | 0.143% |
| Top to Down (bearish) | Down to Up | Sell-off recovered after 2 PM | 132 | 0.196% |

**Of 269 reversal days:**
- 127 (47.2%): Morning rally faded → **afternoon sold off**
- 132 (49.1%): Morning sell-off reversed → **afternoon recovered**

## 9. Day of Week Summary

| Day | Total | TTD | DTU | Flat | TTD % | DTU % | Avg Move % | Concordance % |
|-----|------:|----:|----:|-----:|------:|------:|-----------:|--------------:|
| Monday | 294 | 131 | 147 | 16 | 44.6% | 50.0% | 0.25% | 69.4% |
| Tuesday | 297 | 132 | 150 | 15 | 44.4% | 50.5% | 0.268% | 70.6% |
| Wednesday | 292 | 136 | 148 | 8 | 46.6% | 50.7% | 0.255% | 65.8% |
| Thursday | 294 | 139 | 142 | 13 | 47.3% | 48.3% | 0.247% | 68.0% |
| Friday | 290 | 142 | 140 | 8 | 49.0% | 48.3% | 0.229% | 66.0% |

## 10. Key Findings and Trading Implications

1. **The 14:00 inflection zone dominates across ALL trading days** (49.9%). This is a general market microstructure pattern, not Sensex-expiry-specific.

2. **Concordance**: Sensex expiry 67.9% vs No-expiry 67.7%. Virtually identical — Sensex expiry doesn't change afternoon behaviour.

3. **Non-expiry days produce larger afternoon moves** (0.257% vs 0.232%).

4. **Reversal pattern**: On Sensex expiry days, 52.2% of reversals are morning sell-offs recovering after 2 PM. On no-expiry days: 49.1%. Similar reversal mix.
