# SENSEX Expiry Day VIX vs Movement Backtester

Analyzes the relationship between India VIX and actual SENSEX movement on expiry days (weekly + monthly).

## 📊 Available Datasets

- **2-Year Analysis** (2024-2026): 109 expiries - Recent market behavior
- **6-Year Analysis** (2020-2026): 318 expiries - Long-term patterns including COVID period

👉 **[Quick Comparison Guide](./QUICK_COMPARISON.md)** - Which dataset should you use?

## BSE Expiry Day Transitions

**IMPORTANT**: BSE has changed SENSEX expiry days TWICE in recent history:

1. **Before January 1, 2025**: Friday expiries
2. **January 1, 2025 - September 3, 2025**: Tuesday expiries
3. **September 4, 2025 onwards**: Thursday expiries (current)

This script automatically handles all three periods correctly when analyzing historical data.

## What It Does

This script answers the question: **"Does VIX accurately predict how much SENSEX will move on expiry days?"**

It:
1. **Identifies all expiry dates** (weekly + monthly) for the past 2 years
2. **Handles BSE's expiry day transitions** automatically (Friday → Tuesday → Thursday)
3. **Fetches VIX levels** at the start of each expiry day
4. **Calculates predicted movement** based on VIX (using standard volatility formula)
5. **Measures actual SENSEX movement** on those expiry days
6. **Compares predictions vs reality** and generates comprehensive statistics

## Key Insights You'll Get

- ✅ **VIX accuracy for SENSEX** - Does VIX over/underestimate SENSEX expiry day moves?
- 📊 **Correlation** - How well does VIX predict actual SENSEX movement?
- 📆 **Weekly vs Monthly comparison** - Which expiries are more volatile?
- 🔥 **Extreme days** - When VIX was highest, when movement was highest
- 📈 **Detailed data** - Every expiry day with VIX vs actual comparison
- 📉 **Visual charts** - Unicode mini-charts showing intraday OHLC patterns

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
# 2-Year Analysis (Recent behavior - faster)
python .claude/skills/sensex-expiry-vix-backtest/scripts/backtest_vix_sensex_expiries.py --years 2

# 6-Year Analysis (Long-term patterns - comprehensive)
python .claude/skills/sensex-expiry-vix-backtest/scripts/backtest_vix_sensex_expiries.py --years 6

# Or with Homebrew Python
/opt/homebrew/bin/python3 .claude/skills/sensex-expiry-vix-backtest/scripts/backtest_vix_sensex_expiries.py --years 6
```

### 3. View Results

The script outputs:
- **Console report** - Summary and detailed data with visual charts
- **JSON file** - `vix_sensex_expiries_results.json` (structured data)
- **CSV file** - `vix_sensex_expiries_results.csv` (for Excel/spreadsheet analysis)

## Key Results Summary

### 2-Year Results (2024-2026)
- **109 expiry days** analyzed
- **Average ratio: 1.40x** (VIX underestimates by 40%)
- **Correlation: 0.472** (moderate)
- **Weekly: 1.42x** | Monthly: 1.35x
- Recent market behavior, current Thursday expiry schedule

### 6-Year Results (2020-2026) ⭐ Recommended
- **318 expiry days** analyzed (includes COVID period)
- **Average ratio: 1.29x** (VIX underestimates by 29%)
- **Correlation: 0.450** (moderate)
- **Weekly: 1.28x** | Monthly: 1.33x (monthly MORE volatile)
- Statistically robust, captures all market regimes

👉 **See [QUICK_COMPARISON.md](./QUICK_COMPARISON.md) for detailed comparison and trading strategies**

## 📖 Detailed Analysis Reports

- **[2-Year Analysis](./SENSEX_ANALYSIS.md)** - Comprehensive analysis of recent behavior (109 expiries, 2024-2026)
- **[6-Year Analysis](./SENSEX_6YEAR_ANALYSIS.md)** ⭐ - Full historical analysis (318 expiries, includes COVID 2020-2026)
- **[Quick Comparison](./QUICK_COMPARISON.md)** - Side-by-side comparison with trading strategies

## Sample Output

```
================================================================================
SENSEX Expiry Day VIX vs Movement Backtester (Weekly + Monthly)
Period: 2024-06-25 to 2026-07-25
================================================================================

Fetching SENSEX data...
✓ Fetched 516 days of SENSEX data
Fetching India VIX data...
✓ Fetched 513 days of VIX data

✓ Identified 109 expiry dates:
  - Weekly expiries: 84
  - Monthly expiries: 25

📆 Weekly  2024-06-28 (Fri): VIX 14.52 → Predicted 0.76% | Actual 1.23% (Overestimated)
📅 Monthly 2024-06-28 (Fri): VIX 14.52 → Predicted 0.76% | Actual 1.23% (Overestimated)
...

================================================================================
BACKTEST RESULTS: VIX vs SENSEX Expiry Day Movement
Weekly + Monthly Expiries Combined
================================================================================

📊 OVERALL STATISTICS (All Expiries)
--------------------------------------------------------------------------------
Total Expiry Days: 109
Average VIX: 14.52
Average VIX Predicted Move: 0.76%
Average Actual Range: 0.99%
Average Ratio: 1.30x
Correlation: 0.652

📆 WEEKLY EXPIRIES
--------------------------------------------------------------------------------
Total: 84 days
Average VIX: 14.48
Average Predicted: 0.76% | Actual: 0.98%
Average Ratio: 1.29x
VIX Underestimated: 12 (14.3%)
Correlation: 0.648

📅 MONTHLY EXPIRIES
--------------------------------------------------------------------------------
Total: 25 days
Average VIX: 14.65
Average Predicted: 0.77% | Actual: 1.02%
Average Ratio: 1.33x
VIX Underestimated: 4 (16.0%)
Correlation: 0.671

⚖️  WEEKLY vs MONTHLY COMPARISON
--------------------------------------------------------------------------------
Weekly Avg Ratio: 1.29x
Monthly Avg Ratio: 1.33x
→ Monthly and weekly expiries have SIMILAR volatility (difference: 0.04x)

================================================================================
```

## Command Options

### Backtest Different Time Periods

```bash
# 1 year
python backtest_vix_sensex_expiries.py --years 1

# 3 years
python backtest_vix_sensex_expiries.py --years 3

# 5 years (covers all expiry day transitions)
python backtest_vix_sensex_expiries.py --years 5
```

### Custom Output Files

```bash
python backtest_vix_sensex_expiries.py --json my_results.json --csv my_data.csv
```

### Full Command

```bash
python backtest_vix_sensex_expiries.py --years 2 --json sensex_results_2y.json --csv sensex_results_2y.csv
```

## Understanding the Results

### VIX Prediction Formula

VIX represents **annualized** volatility. To convert to expected daily move:

```
Daily Expected Move = VIX / √252 ≈ VIX / 19.1
```

Example:
- VIX = 15
- Expected daily move = 15 / 19.1 = **0.79%**

**Note**: This uses India VIX, which applies to both NIFTY and SENSEX.

### Actual Movement Metrics

The script calculates:
- **Daily Range %** = (High - Low) / Open × 100
- **Open-Close Move %** = (Close - Open) / Open × 100
- **Intraday High %** = (High - Open) / Open × 100
- **Intraday Low %** = (Low - Open) / Open × 100

### Accuracy Classification

**V5 Threshold Logic** (0.5% threshold for EXTREME underestimation):

```
Difference = Actual Range % - VIX Predicted Move %

If Difference > 0.5%:
    Classification = "Underestimated"
Else:
    Classification = "Overestimated"
```

At SENSEX 50,000 levels:
- 0.5% = ~250 points
- This identifies only EXTREME VIX failures

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

### Visual Mini-Charts

The script generates Unicode charts for each expiry day showing intraday OHLC patterns:

```
▁↓▁↑█↓▅ 📉  = Bearish day (opened high, sold off)
▁↑▆↑█→█ 📈  = Bullish day (strong buying)
▄→▂↑▆↓▃ ━  = Choppy, neutral day
```

Format: `O→L→H→C [direction emoji]`

## BSE Expiry Day Transition Handling

The script's `get_all_expiries()` method uses **date-aware logic**:

```python
# Before January 1, 2025
if current_date < datetime(2025, 1, 1).date():
    target_weekday = 4  # Friday

# January 1, 2025 - September 3, 2025
elif current_date < datetime(2025, 9, 4).date():
    target_weekday = 1  # Tuesday

# September 4, 2025 onwards
else:
    target_weekday = 3  # Thursday
```

This ensures:
- ✅ Historical backtests correctly identify expiry dates across all periods
- ✅ No manual date adjustments needed
- ✅ Seamless analysis across the transition points

## Trading Implications

### If VIX Consistently Underestimates (Ratio > 1.2x)

**Strategy**:
- Buy wider straddles/strangles on expiry day
- Expect larger SENSEX moves than VIX suggests
- Increase breakeven calculations by ratio amount

**Risk**:
- Expiry days have higher realized volatility
- Theta decay accelerates rapidly on BSE options
- Gamma risk increases

### If VIX Consistently Overestimates (Ratio < 0.8x)

**Strategy**:
- Sell premium (credit spreads, iron condors)
- VIX premiums are inflated vs actual SENSEX movement
- Reduce directional exposure

**Risk**:
- Occasional large moves (tail risk)
- Early assignment risk on BSE options
- Gap risk overnight

### Weekly vs Monthly Insights

If the backtest shows:
- **Similar ratios** (difference < 0.1x): Treat weekly and monthly expiries the same
- **Monthly higher**: Monthly expiries are more volatile, size positions accordingly
- **Weekly higher**: Weekly expiries have elevated risk, be cautious

## Expiry Date Calculation

### BSE Expiry Day Rules

The script identifies:
1. **Weekly expiries**: Every target weekday (Friday/Tuesday/Thursday based on date)
2. **Monthly expiries**: Last target weekday of each month

### Holiday Handling

If an expiry falls on a holiday, the script:
1. Checks T-1 (previous trading day)
2. If not found, checks T-2
3. If not found, checks T-3
4. Skips expiry if no data found within 3 days

**Example**:
```
ℹ️  Monthly expiry 2025-01-31 was holiday, using 2025-01-30 (T-1)
```

## Data Sources

### SENSEX Data
- **Ticker**: `^BSESN` (Yahoo Finance)
- **Includes**: Open, High, Low, Close, Volume
- **Frequency**: Daily
- **Exchange**: BSE (Bombay Stock Exchange)

### India VIX Data
- **Ticker**: `^INDIAVIX` (Yahoo Finance)
- **Includes**: Open, High, Low, Close
- **Frequency**: Daily
- **Note**: India VIX is calculated by NSE but applies to overall Indian equity volatility

**Data Quality**: Yahoo Finance data is generally reliable but may have occasional gaps for Indian market data. The script handles missing data gracefully.

## Output Files

### JSON File (`vix_sensex_expiries_results.json`)

Structured data with:
- Individual expiry data for each date
- Summary statistics (overall, weekly, monthly)
- Metadata (backtest date, period)

**Use for**: Programming, further analysis, automation, building trading systems

### CSV File (`vix_sensex_expiries_results.csv`)

Spreadsheet-compatible with columns:
- `date`, `day_of_week`, `expiry_type`
- `chart` (visual Unicode mini-chart)
- `sensex_open`, `sensex_high`, `sensex_low`, `sensex_close`
- `vix_open`, `vix_close`
- `vix_predicted_move_pct`, `actual_range_pct`, `actual_open_close_pct`
- `intraday_high_pct`, `intraday_low_pct`
- `range_vs_vix_ratio`, `diff_pct`, `vix_accuracy`

**Use for**: Excel analysis, charts, manual review, pivot tables

## Comparison with NIFTY VIX Backtest

Both scripts use the same VIX data but different underlyings:

| Feature | NIFTY Backtest | SENSEX Backtest |
|---------|---------------|-----------------|
| Underlying Index | NIFTY 50 (NSE) | SENSEX (BSE) |
| Ticker | ^NSEI | ^BSESN |
| Current Expiry Day | Tuesday | Thursday |
| Transition Date 1 | Sept 1, 2025 (Thu→Tue) | Jan 1, 2025 (Fri→Tue) |
| Transition Date 2 | - | Sept 4, 2025 (Tue→Thu) |
| VIX Source | India VIX | India VIX (same) |
| VIX Conversion | VIX / 19.1 | VIX / 19.1 (same) |

**Key Insight**: SENSEX has TWO expiry day transitions vs NIFTY's one, making the backtest more complex but more comprehensive.

## Limitations

### Data Limitations
- **2-year limit** recommended (Yahoo Finance reliability)
- **Daily data only** (no intraday granularity)
- **Holiday adjustments** may not capture all NSE/BSE special trading days

### Analysis Limitations
- **VIX formula** assumes normal distribution (reality differs)
- **Expiry vs regular days** - Expiry days have different dynamics
- **No vol surface** - Uses ATM VIX, ignores skew
- **Overnight gaps** not factored in predictions
- **Cross-market correlation** - India VIX is NSE-calculated but applied to BSE

### Market Limitations
- **Regime changes** - VIX behavior changes over time
- **Black swan events** - Extreme moves break correlations
- **Regulatory changes** - SEBI rule changes affect expiry behavior
- **Liquidity differences** - SENSEX options may have different liquidity vs NIFTY

## Troubleshooting

### "No SENSEX data found for ticker ^BSESN"

**Cause**: Yahoo Finance API issue or ticker change

**Fix**:
- Check internet connection
- Verify ticker on Yahoo Finance website
- Try `^BSESN` directly on finance.yahoo.com
- Alternative: Try `SENSEX` or `BSE-SENSEX`

### "No VIX data found"

**Cause**: India VIX ticker not available

**Fix**:
- Verify ticker symbol: `^INDIAVIX`
- Check if NSE VIX is available on Yahoo Finance
- Alternative: Download VIX data from NSE website manually

### Holiday Data Missing

**Output**: `ℹ️  Weekly expiry 2025-01-26 was holiday, using 2025-01-23 (T-3)`

**This is normal** - The script automatically handles Indian market holidays by looking back up to 3 days.

### Correlation shows NaN

**Cause**: Insufficient data points

**Fix**:
- Ensure at least 20-25 expiry dates in range
- Increase `--years` parameter
- Check data availability on Yahoo Finance

## Advanced Usage

### Analyze Specific Period (Cross-Transition Analysis)

To analyze a period covering both BSE transitions:

```bash
# Covers Friday → Tuesday → Thursday transitions
python backtest_vix_sensex_expiries.py --years 3
```

The script automatically handles the transition logic internally.

### Compare with NIFTY

Run both backtests and compare:

```bash
# SENSEX backtest
python .claude/skills/sensex-expiry-vix-backtest/scripts/backtest_vix_sensex_expiries.py --csv sensex.csv

# NIFTY backtest
python .claude/skills/nifty-expiry-vix-backtest/scripts/backtest_vix_all_expiries_v5.py --csv nifty.csv

# Compare in Excel/Python
# Key metrics to compare:
# - Average ratio (SENSEX vs NIFTY)
# - Correlation differences
# - Weekly vs monthly patterns
```

### Custom Threshold

To modify the underestimation threshold (currently 0.5%):

1. Open `backtest_vix_sensex_expiries.py`
2. Find line: `vix_accuracy = 'Underestimated' if diff > 0.5 else 'Overestimated'`
3. Change `0.5` to your desired threshold (e.g., `0.3` for less conservative, `0.7` for more conservative)

## Integration with Trading

### Pre-Expiry Planning

1. Run the backtest to understand typical SENSEX expiry behavior
2. Check average ratio (e.g., 1.3x means expect 30% more movement than VIX)
3. Size SENSEX options positions accordingly
4. Set wider stops on BSE expiry days

### Position Sizing

```python
current_vix = 15
predicted_move_pct = current_vix / 19.1  # 0.79%
backtest_ratio = 1.30  # From backtest results
expected_move_pct = predicted_move_pct * backtest_ratio  # 1.03%

sensex_level = 50000
expected_move_points = sensex_level * expected_move_pct / 100  # 515 points

# Choose strikes:
bull_call_spread = sensex_level to sensex_level + 500  # Within expected range
```

### Risk Management

Use historical data to:
- Calculate maximum expiry day move (99th percentile)
- Set appropriate margin requirements for BSE options
- Plan exit strategies before theta decay accelerates
- Understand Friday vs Tuesday vs Thursday behavior patterns

## Example Analysis Workflow

```bash
# 1. Run backtest (covers both BSE transitions)
python backtest_vix_sensex_expiries.py --years 2 --csv sensex_results.csv

# 2. Open CSV in Excel/Numbers
open sensex_results.csv

# 3. Create charts:
#    - VIX vs Actual Movement (scatter plot)
#    - Ratio distribution (histogram)
#    - Time series (VIX accuracy over time)
#    - Expiry day comparison (Friday vs Tuesday vs Thursday)

# 4. Calculate insights:
#    - What VIX level triggers biggest underestimation?
#    - Are certain months more volatile for SENSEX?
#    - Did VIX accuracy change after expiry day transitions?
#    - Is Thursday expiry more/less volatile than Friday was?

# 5. Apply to next expiry:
#    - Check current VIX
#    - Apply average ratio from backtest
#    - Adjust for expiry type (weekly vs monthly)
#    - Plan SENSEX trades accordingly
```

## Key Questions This Backtest Answers

1. ✅ **Does VIX accurately predict SENSEX moves?** (Check correlation)
2. ✅ **Is SENSEX more/less volatile than VIX suggests?** (Check ratio)
3. ✅ **Do weekly and monthly SENSEX expiries behave differently?** (Compare stats)
4. ✅ **Did expiry day transitions affect volatility patterns?** (Analyze by date range)
5. ✅ **Should I trust VIX for SENSEX options trading?** (Review overall accuracy)

## Next Steps

### After Running the Backtest

1. **Review the correlation** - Is VIX useful for SENSEX expiry trading?
2. **Note the ratio** - Adjust expectations (e.g., 1.3x means 30% more volatile)
3. **Compare weekly vs monthly** - Do they differ significantly?
4. **Identify extremes** - When was VIX most wrong for SENSEX?
5. **Export & analyze** - Use CSV for deeper dives in Excel

### Extend the Analysis

- Compare SENSEX vs NIFTY expiry behavior
- Analyze by month (Jan effect, Diwali volatility, etc.)
- Correlate with market trend (bull vs bear markets)
- Add technical indicators (RSI, moving averages)
- Include BSE option chain data (PCR, max pain)
- Study pre/post BSE expiry day transition patterns

## Support

For issues or questions:
- Check console output for error messages
- Verify data sources are accessible (Yahoo Finance)
- Try reducing backtest period if data issues occur
- Compare results with NIFTY backtest for validation

## License

Created with Claude Code - Free to use and modify

---

## Quick Command Reference

```bash
# Basic run (2 years, weekly + monthly)
python .claude/skills/sensex-expiry-vix-backtest/scripts/backtest_vix_sensex_expiries.py

# 3 years (covers both BSE transitions)
python backtest_vix_sensex_expiries.py --years 3

# Custom output files
python backtest_vix_sensex_expiries.py --json my_results.json --csv my_data.csv

# Full command
python backtest_vix_sensex_expiries.py --years 2 --json sensex_2y.json --csv sensex_2y.csv
```

That's it! The backtest will run and show you if VIX is a good predictor of SENSEX expiry day movement across all three BSE expiry day schedules (Friday → Tuesday → Thursday).
