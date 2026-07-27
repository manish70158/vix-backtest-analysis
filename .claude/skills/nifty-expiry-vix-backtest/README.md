# NIFTY Expiry Day VIX vs Movement Backtester

Analyzes the relationship between India VIX and actual NIFTY movement on monthly expiry days over the last 2 years.

## What It Does

This script answers the question: **"Does VIX accurately predict how much NIFTY will move on expiry days?"**

It:
1. **Identifies all monthly expiry dates** (last Thursday of each month) for the past 2 years
2. **Fetches VIX levels** at the start of each expiry day
3. **Calculates predicted movement** based on VIX (using standard volatility formula)
4. **Measures actual NIFTY movement** on those expiry days
5. **Compares predictions vs reality** and generates statistics

## Key Insights You'll Get

- ✅ **Average VIX accuracy** - Does VIX over/underestimate expiry day moves?
- 📊 **Correlation** - How well does VIX predict actual movement?
- 🔥 **Extreme days** - When VIX was highest, when movement was highest
- 📈 **Detailed data** - Every expiry day with VIX vs actual comparison

## Quick Start

### 1. Install Dependencies

```bash
pip3 install yfinance pandas numpy
```

Or with Homebrew Python:
```bash
/opt/homebrew/bin/pip3 install yfinance pandas numpy
```

### 2. Run the Backtest

```bash
# Default: 2 years of data
python .claude/skills/nifty-expiry-vix-backtest/scripts/backtest_vix_vs_movement.py

# Or with Homebrew Python
/opt/homebrew/bin/python3 .claude/skills/nifty-expiry-vix-backtest/scripts/backtest_vix_vs_movement.py
```

### 3. View Results

The script outputs:
- **Console report** - Summary and detailed data
- **JSON file** - `vix_backtest_results.json` (structured data)
- **CSV file** - `vix_backtest_results.csv` (for Excel/spreadsheet analysis)

## Sample Output

```
================================================================================
BACKTEST RESULTS: VIX vs NIFTY Expiry Day Movement
================================================================================

📊 SUMMARY STATISTICS
--------------------------------------------------------------------------------
Total Expiry Days Analyzed: 24
Average VIX Level: 14.52
Average VIX Predicted Move: 0.76%
Average Actual Range: 1.23%
Average Actual Open-Close: 0.58%

🎯 VIX ACCURACY
--------------------------------------------------------------------------------
Average Actual/Predicted Ratio: 1.62x
Median Ratio: 1.45x
VIX Underestimated Movement: 18 times (75.0%)
VIX Overestimated Movement: 6 times (25.0%)
Correlation (VIX vs Movement): 0.584

🔥 EXTREME DAYS
--------------------------------------------------------------------------------
Highest VIX Day: 2025-03-27
  VIX: 24.5 | Predicted: 1.28% | Actual: 2.45%

Highest Movement Day: 2024-12-26
  VIX: 18.2 | Predicted: 0.95% | Actual: 3.12%

📈 INTERPRETATION
--------------------------------------------------------------------------------
⚠️  VIX consistently UNDERESTIMATES expiry day movement
    → Expiry days are MORE volatile than VIX suggests
~  Moderate correlation (0.584) - VIX has some predictive value
```

## Command Options

### Backtest Different Time Periods

```bash
# 1 year
python backtest_vix_vs_movement.py --years 1

# 3 years
python backtest_vix_vs_movement.py --years 3

# 5 years
python backtest_vix_vs_movement.py --years 5
```

### Custom Output Files

```bash
python backtest_vix_vs_movement.py --json my_results.json --csv my_data.csv
```

### Full Command

```bash
python backtest_vix_vs_movement.py --years 2 --json results_2y.json --csv results_2y.csv
```

## Understanding the Results

### VIX Prediction Formula

VIX represents **annualized** volatility. To convert to expected daily move:

```
Daily Expected Move = VIX / √365 ≈ VIX / 19.1
```

Example:
- VIX = 15
- Expected daily move = 15 / 19.1 = **0.79%**

### Actual Movement Metrics

The script calculates:
- **Daily Range %** = (High - Low) / Open × 100
- **Open-Close Move %** = |Close - Open| / Open × 100
- **Intraday High %** = (High - Open) / Open × 100
- **Intraday Low %** = (Open - Low) / Open × 100

### Accuracy Ratio

```
Ratio = Actual Movement / VIX Predicted Movement
```

- **Ratio > 1.0** = VIX underestimated (actual move was bigger)
- **Ratio < 1.0** = VIX overestimated (actual move was smaller)
- **Ratio = 1.0** = Perfect prediction

### Correlation

- **0.8 to 1.0** = Strong positive correlation (VIX is excellent predictor)
- **0.5 to 0.8** = Moderate correlation (VIX has decent predictive value)
- **0.3 to 0.5** = Weak correlation (VIX is somewhat useful)
- **Below 0.3** = Very weak (VIX is poor predictor)

## Trading Implications

### If VIX Consistently Underestimates

**Strategy**:
- Buy wider straddles/strangles on expiry day
- Expect larger moves than VIX suggests
- Increase position size cautiously

**Risk**:
- Expiry days have higher realized volatility
- Theta decay accelerates rapidly
- Gamma risk increases

### If VIX Consistently Overestimates

**Strategy**:
- Sell premium (credit spreads, iron condors)
- VIX premiums are inflated vs actual movement
- Reduce directional exposure

**Risk**:
- Occasional large moves (tail risk)
- Early assignment risk
- Gap risk overnight

### If Correlation is Strong

**Strategy**:
- Use VIX as primary input for position sizing
- Trust VIX-based stop losses
- Scale positions based on VIX level

### If Correlation is Weak

**Strategy**:
- Don't rely solely on VIX
- Use price action and technical levels
- Combine VIX with other indicators

## Output Files

### JSON File (`vix_backtest_results.json`)

Structured data with:
- Metadata (backtest date, period)
- Individual expiry data
- Summary statistics

**Use for**: Programming, further analysis, automation

### CSV File (`vix_backtest_results.csv`)

Spreadsheet-compatible with columns:
- Date, VIX Open, VIX Close
- Predicted Move %, Actual Range %
- Ratio, Accuracy (Over/Under)
- NIFTY OHLC data

**Use for**: Excel analysis, charts, manual review

## Expiry Date Calculation

NIFTY monthly expiries are on the **last Thursday of each month**.

The script:
1. Finds last day of each month
2. Works backward to find last Thursday
3. Handles edge cases (holidays, special circumstances)

**Note**: If an expiry falls on a holiday, NSE may adjust the date. This script uses the standard last Thursday rule.

## Data Sources

### NIFTY Data
- **Ticker**: `^NSEI` (Yahoo Finance)
- **Includes**: Open, High, Low, Close, Volume
- **Frequency**: Daily

### India VIX Data
- **Ticker**: `^INDIAVIX` (Yahoo Finance)
- **Includes**: Open, High, Low, Close
- **Frequency**: Daily

**Data Quality**: Yahoo Finance data is generally reliable but may have occasional gaps for Indian market data. The script handles missing data gracefully.

## Limitations

### Data Limitations
- **2-year limit** recommended (Yahoo Finance reliability)
- **Daily data only** (no intraday granularity)
- **Holiday adjustments** not fully automated

### Analysis Limitations
- **VIX formula** assumes normal distribution (reality differs)
- **Expiry vs regular days** - Expiry days have different dynamics
- **No vol surface** - Uses ATM VIX, ignores skew
- **Overnight gaps** not factored in predictions

### Market Limitations
- **Regime changes** - VIX behavior changes over time
- **Black swan events** - Extreme moves break correlations
- **Regulatory changes** - SEBI rule changes affect expiry behavior

## Troubleshooting

### "Could not fetch NIFTY data"

**Cause**: Yahoo Finance API issue or network problem

**Fix**:
- Check internet connection
- Try again later (Yahoo Finance can be temporarily down)
- Reduce backtest period (`--years 1`)

### "Could not fetch VIX data"

**Cause**: India VIX ticker not available

**Fix**:
- Verify ticker symbol: `^INDIAVIX`
- Check if NSE VIX is available on Yahoo Finance
- Alternative: Download VIX data from NSE website manually

### Empty results / No expiry dates

**Cause**: Date range too narrow or data missing

**Fix**:
- Increase years: `--years 3`
- Check start/end dates in output
- Manually verify expiry dates on NSE website

### Correlation shows NaN

**Cause**: Insufficient data points or all-zero values

**Fix**:
- Ensure at least 10-12 expiry dates in range
- Check if VIX data is populated
- Verify NIFTY data has price movements

## Advanced Usage

### Analyze Specific Period

Modify the script to analyze custom date ranges:
```python
backtester = NiftyExpiryBacktester(years=2)
backtester.start_date = datetime(2024, 1, 1)
backtester.end_date = datetime(2024, 12, 31)
results = backtester.run_backtest()
```

### Weekly Expiries

To analyze **weekly** expiries instead of monthly:
1. Modify `get_expiry_dates()` to identify weekly Thursdays
2. Adjust sample size (52 weeks vs 12 months per year)

### Custom VIX Formula

To test alternative VIX conversion formulas:
```python
# In analyze_expiry_day(), modify:
vix_predicted_move_pct = vix_open / 19.1  # Standard
# To:
vix_predicted_move_pct = vix_open / 16    # More aggressive
```

## Integration with Trading

### Pre-Expiry Planning

Run the backtest to understand typical expiry behavior:
1. Check average ratio (1.6x means expect 60% more movement than VIX)
2. Size positions accordingly
3. Set wider stops on expiry days

### Risk Management

Use historical data to:
- Calculate maximum expiry day move (99th percentile)
- Set appropriate margin requirements
- Plan exit strategies

### Backtesting Strategies

Use the CSV output to:
- Backtest expiry-specific strategies
- Calculate optimal entry/exit times
- Test different strike selections

## Example Analysis Workflow

```bash
# 1. Run backtest
python backtest_vix_vs_movement.py --years 3 --csv results.csv

# 2. Open CSV in Excel/Numbers
open results.csv

# 3. Create charts:
#    - VIX vs Actual Movement (scatter plot)
#    - Ratio distribution (histogram)
#    - Time series (VIX accuracy over time)

# 4. Calculate your insights:
#    - What VIX level triggers biggest underestimation?
#    - Are certain months more volatile?
#    - Has VIX accuracy improved over time?

# 5. Apply to next expiry:
#    - Check current VIX
#    - Apply average ratio from backtest
#    - Plan trades accordingly
```

## Next Steps

### After Running the Backtest

1. **Review the correlation** - Is VIX useful for expiry trading?
2. **Note the ratio** - Adjust expectations (e.g., 1.5x VIX)
3. **Identify extremes** - When was VIX most wrong?
4. **Export & analyze** - Use CSV for deeper dives

### Extend the Analysis

- Compare monthly vs weekly expiries
- Analyze by month (Jan effect, Dec volatility, etc.)
- Correlate with market trend (bull vs bear)
- Add technical indicators (RSI, moving averages)
- Include option chain data (PCR, max pain)

## Support

For issues or questions:
- Check the console output for error messages
- Verify data sources are accessible (Yahoo Finance)
- Try reducing backtest period if data issues occur

## License

Created with Claude Code - Free to use and modify

---

**Quick Command**:
```bash
python .claude/skills/nifty-expiry-vix-backtest/scripts/backtest_vix_vs_movement.py
```

That's it! The backtest will run and show you if VIX is a good predictor of expiry day movement.
