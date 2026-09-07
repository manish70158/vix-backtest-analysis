## Context

The repository contains a 322-row CSV (`vix_fii_t1_intraday_expiry_results.csv`) with daily expiry metadata (Jul 2020–Aug 2026) and a PostgreSQL table (`market_data.nifty50_5min`) with ~110K 5-minute OHLCV candles (Aug 2020–Aug 2026). See proposal.md for full motivation.

Key data characteristics discovered during exploration:
- CSV columns include: `date`, `move_direction` (Down to Up / Top to Down), `expiry_type` (weekly/monthly), `vix_open`, `vix_close`, `t1_fii_stance`, `t1_pro_stance`, `nifty_open/high/low/close`
- PostgreSQL table schema: `datetime` (timestamptz), `open`, `high`, `low`, `close`, `volume` (bigint, often 0)
- 5-min data starts 2020-08-06; CSV starts 2020-07-02 — ~5 early CSV dates will have no 5-min match
- Afternoon session has 18 candles per day (14:00 to 15:25, inclusive)
- Existing `sensex-analysis/` folder establishes the pattern: Python scripts + CSV output + markdown reports

## Goals / Non-Goals

**Goals:**
- Single-script analysis that reads both sources, computes all metrics, and generates CSV + markdown report
- Identify the statistically dominant time window for afternoon reversals on expiry days
- Segment findings by direction, expiry type, VIX level, and FII stance
- Self-contained output in `expiry-afternoon-analysis/` folder

**Non-Goals:**
- Real-time or live monitoring (this is a historical backtest)
- Sensex/BSE analysis (Nifty-only; sensex analysis lives in `sensex-analysis/`)
- Predicting future moves (this is descriptive statistics, not a predictive model)
- Modifying the existing CSV or database

## Decisions

### 1. Inflection point detection: Afternoon High/Low approach

**Choice:** For "Top to Down" days, the inflection is the candle with the afternoon high. For "Down to Up" days, it is the candle with the afternoon low. This is the point where price reverses toward the closing direction.

**Alternatives considered:**
- *Percentage threshold crossing*: Mark inflection when price moves >0.1% from the 2 PM level. Rejected — threshold is arbitrary and VIX-dependent.
- *Rolling momentum change*: Detect when 3-candle rolling return flips sign. Rejected — adds complexity without clear accuracy improvement for a descriptive study.

**Rationale:** The high/low approach is deterministic, reproducible, and directly answers "when did the move start" — the candle that marks the extremum before price moves toward close.

### 2. Time bucket granularity: 5-minute slots with 15-minute summary

**Choice:** Track inflection times at 5-minute granularity (matching the raw data), but also produce summary tables at 15-minute buckets (14:00, 14:15, 14:30, 14:45, 15:00, 15:15) for readability.

**Alternatives considered:**
- *15-minute only*: Loses precision; a reversal at 14:10 vs 14:00 matters to traders.
- *1-minute data*: Not available in PostgreSQL.

### 3. Database connection: psycopg2 with direct SQL

**Choice:** Use `psycopg2` for PostgreSQL queries, returning results as pandas DataFrames.

**Alternatives considered:**
- *SQLAlchemy ORM*: Over-engineering for read-only SELECT queries against a single table.
- *pandas read_sql with connection string*: Slightly simpler but less control over connection params.

**Rationale:** Consistent with how the existing scripts in the project access data. Minimal dependency footprint.

### 4. VIX level bucketing: Three tiers

**Choice:** Low (<15), Medium (15–20), High (>20) based on `vix_open` from the CSV.

**Rationale:** These thresholds align with the historical VIX distribution for Nifty. The CSV data shows VIX ranging from ~10 to ~35, with ~15 and ~20 as natural break points visible in the data.

### 5. Output folder naming: `expiry-afternoon-analysis/`

**Choice:** New folder `expiry-afternoon-analysis/` in repo root, following the pattern of `sensex-analysis/`.

**Rationale:** Keeps analysis outputs organized by topic. The user requested output "in a separate folder like sensex-analysis."

## Risks / Trade-offs

- **[Missing 5-min data for early dates]** → The CSV has 5 expiry dates before the 5-min DB starts (2020-08-06). These will be skipped with a logged warning. Impact: <2% of data loss.
- **[Volume field is 0]** → The `nifty50_5min` table has volume=0 for all observed rows. Volume-based analysis is not possible. → Mitigation: Focus purely on price action (OHLC) for inflection detection.
- **[Inflection at session boundaries]** → If the afternoon high/low occurs at exactly 14:00 or 15:25, the "inflection" is at the boundary — this is a valid data point (move started immediately or very late) and will be reported as-is.
- **[Multiple candles at same high/low]** → If two candles share the exact same high (or low), the first occurrence is taken as the inflection point.
