## Why

The Nifty FII/DII-VIX correlation analysis revealed that institutional positioning has limited pre-market predictive power for Nifty blowouts. Sensex has a different expiry schedule (Friday → Tuesday → Thursday transitions) and slightly higher volatility (1.29x vs 1.24x), with a VIX underestimation rate of 23.9% over 318 expiries. The same FII/DII institutional flow data should be tested against Sensex expiry-day results to determine whether the correlation patterns differ — given that Sensex's VIX correlation is stronger (0.450 vs 0.411 for Nifty) and expiry dynamics may differ from Nifty due to lower derivatives liquidity.

## What Changes

- Build a correlation analysis script that joins the FII/DII daily positioning data with Sensex VIX expiry-day results (`vix_sensex_6y_results.csv`)
- Compute correlation metrics between FII/DII direction signals and: blowout occurrence, Sensex expiry-day range, move direction, and VIX accuracy
- Analyze whether FII positioning (futures net, call net, put net) on or before Sensex expiry day predicts whether VIX will underestimate
- Generate a combined results file with merged FII/DII + Sensex VIX features per expiry day
- Produce a summary report with correlation findings and comparison against Nifty correlation results
- Fetch daily participant-wise data with **separate FII and PRO** columns from NSE archives
- All Sensex-related outputs consolidated in `sensex-analysis/` directory

## Capabilities

### New Capabilities
- `fii-dii-vix-correlation-sensex`: Correlation analysis between FII/DII institutional flow data and Sensex VIX expiry-day backtest results — joining on Sensex expiry dates, computing statistical correlations, and comparing findings with the Nifty correlation analysis
- `participant-wise-daily-fetch`: Daily FII/PRO/DII/Client participant-wise OI data fetcher with separate columns for each participant category

### Modified Capabilities

## Impact

- All Sensex analysis consolidated in `sensex-analysis/` directory at project root
- Python scripts: `build_sensex_fii_6year.py`, `correlate_fii_dii_vix_sensex.py`, `fetch_bse_participant_data.py`
- Output CSV/JSON with merged correlation data (305 valid Sensex expiry days, 6-year period)
- Summary markdown with correlation findings and Nifty comparison
- Daily participant-wise data with separate FII, PRO, DII, Client positions and directions
- Data dependencies: `vix_sensex_6y_results.csv` (in same directory), NSE archives for participant OI
- Note: BSE India API (api.bseindia.com) is blocked by Akamai WAF; NSE archives used as equivalent source
