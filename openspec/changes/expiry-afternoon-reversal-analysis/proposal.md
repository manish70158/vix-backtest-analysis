## Why

The existing VIX-FII expiry analysis (`vix_fii_t1_intraday_expiry_results.csv`) classifies each of the 322 Nifty expiry days (Jul 2020–Aug 2026) as "Top to Down" or "Down to Up" but does not reveal **when** the directional move begins in the afternoon session. Traders need to know the precise timing window (2:00 PM, 2:15 PM, 2:30 PM, 2:45 PM, 3:00 PM) when reversals or continuation moves typically kick in on expiry days, so they can position before the move rather than chase it.

## What Changes

- Build a Python analysis script that joins expiry-day metadata from the CSV with 5-minute OHLCV bars from PostgreSQL (`market_data.nifty50_5min`) to compute afternoon price trajectories on each expiry day.
- For every expiry day, classify the afternoon (post-2 PM) move as top-to-down or down-to-up by comparing the 2 PM price level against the close, and identify the 5-minute candle where the directional move inflects.
- Compute statistics: distribution of reversal start times, magnitude of moves by time bucket, correlation with VIX level, FII stance, and expiry type (weekly vs monthly).
- Generate a comprehensive markdown report with tables and summary statistics, output into a new `expiry-afternoon-analysis/` folder (following the pattern of the existing `sensex-analysis/` folder).
- Generate supporting CSV data files for further consumption.

## Capabilities

### New Capabilities
- `expiry-afternoon-reversal`: Analyze 5-minute intraday data on Nifty expiry days to identify the timing, direction, and magnitude of afternoon (post-2 PM) price moves, cross-referenced with VIX and FII/DII positioning data.

### Modified Capabilities
<!-- No existing capabilities are being modified. -->

## Impact

- **New folder**: `expiry-afternoon-analysis/` containing the analysis script, output CSV, and final markdown report.
- **Database dependency**: Reads from `market_data.nifty50_5min` (PostgreSQL, localhost). Read-only queries.
- **File dependency**: Reads `vix_fii_t1_intraday_expiry_results.csv` from repo root.
- **Python dependencies**: `pandas`, `psycopg2` (or `sqlalchemy`), standard library. No new external dependencies beyond what the project already uses.
