---
name: nifty50-volume-filter
description: Screen Nifty 50 stocks for volume breakouts with lower low patterns. Identifies stocks where current volume exceeds 7-day average AND recent swing low is below previous swing low, signaling potential bearish momentum. Use when user asks about Nifty 50 volume analysis, high volume Nifty stocks, lower low patterns, breakdown screening, or wants to find Nifty stocks with selling pressure. Trigger on phrases like "nifty 50 volume", "nifty lower low", "screen nifty 50", "nifty breakdown stocks", "nifty high volume", "which nifty stocks showing weakness", "nifty stocks with volume surge".
---

# Nifty 50 Volume & Lower Low Filter

A technical screening tool for identifying Nifty 50 stocks showing potential bearish patterns through the combination of volume surges and lower low formations.

## Purpose

This skill helps traders and investors identify Nifty 50 stocks that meet two specific technical criteria:

1. **Volume Surge**: Current trading volume exceeds the 7-day average volume
2. **Lower Low Pattern**: Recent swing low is below the previous swing low (technical downtrend signal)

Stocks meeting both criteria may indicate:
- Increased selling pressure with technical weakness
- Potential short opportunities
- Risk management signals for existing long positions
- Breakdown from support levels with confirmation

## When to Use This Skill

Use this skill when the user wants to:
- Screen Nifty 50 for bearish technical patterns
- Identify stocks with high volume and weakening price action
- Find potential breakdown candidates
- Monitor for risk in blue-chip holdings
- Discover short-term trading opportunities on the bearish side

**Trigger phrases**: "scan nifty 50 for lower lows", "which nifty stocks have high volume", "nifty breakdown screening", "stocks showing weakness in nifty 50", "volume and price weakness analysis"

## Methodology

### Volume Filter (7-Day Average)

The script calculates the 7-day average volume and compares it to the current day's volume:

```
Volume Ratio = Current Volume / 7-Day Average Volume
```

**Filter**: Volume Ratio > 1.0 (current volume exceeds average)

**Interpretation**:
- **1.0 - 1.5x**: Moderate volume increase
- **1.5 - 2.0x**: Strong volume surge
- **> 2.0x**: Very strong volume spike, heightened activity

### Swing Low Detection (5-Bar Window)

A **swing low** is a local price minimum where the low price at a specific bar is lower than the surrounding bars within a defined window.

**Algorithm**:
- For each bar position `i`, check if `Low[i]` is the minimum value in the range `[i-5, i+5]`
- A swing low indicates a price level where selling pressure was exhausted temporarily
- The script identifies all swing lows in the 30-day history

**Lower Low Pattern**:
- Compare the two most recent swing lows
- If `Recent Swing Low < Previous Swing Low`, the stock is making lower lows
- This indicates a bearish trend structure (series of lower lows)

### Combined Filter

Both conditions must be TRUE:
```
✓ Volume Ratio ≥ 1.0 (configurable)
✓ Recent Swing Low < Previous Swing Low
```

Only stocks passing both filters are included in the results.

## Running the Skill

The skill provides a Python script that can be executed directly:

### Basic Usage

```bash
python ~/.claude/skills/nifty50-volume-filter/scripts/nifty50_volume_filter.py
```

This will:
- Scan all 50 Nifty stocks
- Apply both filters
- Display results in terminal
- Export to `nifty50_filtered.csv`

### Command Options

**Custom output file**:
```bash
python nifty50_volume_filter.py --output my_results.csv
```

**Adjust swing low window** (default: 5 bars):
```bash
python nifty50_volume_filter.py --window 7
```

Larger windows (7-10) detect major swing lows, smaller windows (3-5) are more sensitive.

**Minimum volume ratio** (default: 1.0):
```bash
python nifty50_volume_filter.py --min-volume-ratio 1.5
```

Set to 1.5 to only see stocks with 50%+ volume increase.

**Verbose mode** (show progress for each stock):
```bash
python nifty50_volume_filter.py --verbose
```

**Combined example**:
```bash
python nifty50_volume_filter.py --output results.csv --window 7 --min-volume-ratio 1.5 --verbose
```

## Output Format

### Console Output

The script displays:
1. **Progress**: Live scan progress through 50 stocks
2. **Summary**: Count of stocks meeting criteria
3. **Results Table**: Filtered stocks with key metrics
4. **Interpretation Guide**: What the signals mean

### Results Table Columns

| Column | Description |
|--------|-------------|
| **Symbol** | NSE stock symbol |
| **Company** | Full company name |
| **Current Vol** | Today's trading volume (formatted: M/K) |
| **7D Avg Vol** | 7-day average volume |
| **Ratio** | Volume ratio (Current / 7D Average) |
| **Recent Low** | Most recent swing low price (₹) |
| **Previous Low** | Previous swing low price (₹) |
| **Diff** | Percentage difference between swing lows |
| **Current Price** | Latest closing price (₹) |

### CSV Export

The CSV file contains the same data plus additional columns:
- `sector`: Industry sector
- `low_diff`: Absolute rupee difference between swing lows
- `low_diff_pct`: Percentage breakdown from previous low

## Interpreting Results

### Strong Bearish Signals

Look for stocks with:
- **Volume Ratio > 2.0**: Very strong surge in activity
- **Diff % > 2%**: Significant breakdown from previous support
- **Current Price near Recent Low**: Still in breakdown zone

These combinations suggest strong bearish momentum with confirmation.

### Caution Flags

- **Very small Diff % (<0.5%)**: Marginal lower low, may not be significant
- **Recent Low from many days ago**: Pattern may be stale
- **Very high volume ratio (>5x)**: May indicate news/event, not sustainable trend

### Context is Critical

Always consider:
1. **Overall market direction**: Is Nifty index itself declining?
2. **Sector performance**: Is the entire sector weak, or just this stock?
3. **News events**: Check for company-specific news driving the pattern
4. **Support levels**: Is the stock near a major support level that might hold?

A bearish signal in a strong uptrending market may have less significance than the same signal during a market downturn.

## Best Practices

### Timing
- **Run after market close** (post 3:30 PM IST) for complete data
- Daily scans capture fresh patterns
- Yahoo Finance data may have 15-minute delay during trading hours

### Combining with Other Analysis
This skill identifies technical patterns. Strengthen your analysis by:
- Checking fundamentals (P/E, debt levels, earnings trends)
- Reading recent news and company announcements
- Examining longer-term charts for context
- Analyzing sector trends and relative performance
- Checking institutional holding changes

### Risk Management
- These are bearish signals, not guarantees of further decline
- Always use stop losses when trading based on technical patterns
- Consider position sizing based on volatility and risk tolerance
- Stocks can reverse quickly, especially blue chips with strong fundamentals

## Typical Workflow

When the user asks to screen Nifty 50 for volume and lower lows:

1. **Run the script** with appropriate parameters
2. **Review results table** - identify the most interesting candidates
3. **For top 3-5 stocks**, offer to:
   - Pull up detailed technical analysis (RSI, MACD, moving averages)
   - Check recent news and announcements
   - Analyze fundamental metrics
   - Provide historical chart context
4. **Export CSV** for the user to track or analyze further
5. **Set up tracking** if user wants to monitor these stocks going forward

### Example Interaction

**User**: "Show me nifty 50 stocks with high volume and making lower lows"

**Your Response**:
```
Let me scan the Nifty 50 for stocks showing volume surges with lower low patterns.

[Run the script]

Found 8 stocks matching criteria:
- TATASTEEL: 1.88x volume, Recent Low ₹125.30 vs Previous ₹127.50
- SBIN: 1.68x volume, Recent Low ₹592.15 vs Previous ₹598.40
...

Would you like me to:
1. Analyze the top 3 stocks in detail (technical + fundamental)?
2. Check recent news for these stocks?
3. Export the full list to CSV for your review?
```

## Limitations & Considerations

### Data Source
- Uses Yahoo Finance with `.NS` suffix for NSE stocks
- End-of-day data (not real-time intraday)
- Possible 15-minute delay during market hours
- Data quality depends on Yahoo Finance availability

### Nifty 50 Constituents
- The constituent list is static (as of July 2026)
- Nifty 50 composition changes quarterly
- User may want to check NSE website for current constituents
- The JSON file can be manually updated if needed

### Technical Limitations
- **Swing low detection** is sensitive to window parameter
  - Smaller windows (3-5): More swing lows detected, potentially noisy
  - Larger windows (7-10): Fewer, more significant swing lows
- **Volume comparison** uses simple 7-day average
  - Doesn't account for earnings days or major events
  - May give false positives on low-volume stocks
- **No consideration of** gaps, splits, bonuses, or corporate actions

### False Signals
- High volume can occur for positive reasons (accumulation, breakout)
- Lower lows in a consolidation may not indicate trend
- End-of-day data misses intraday reversals
- News-driven spikes may not reflect sustainable trends

## Troubleshooting

### "Insufficient data" errors
- Stock may be newly listed or have gaps in history
- Try reducing the `--window` parameter
- Some stocks may not have full 30-day history on Yahoo Finance

### No results / Empty output
- Try lowering `--min-volume-ratio` (e.g., to 0.8)
- Adjust `--window` parameter (try 3 or 7)
- Market may be in strong uptrend (few lower lows)
- Run after market close for complete data

### Slow execution
- Normal execution: 20-30 seconds for 50 stocks
- If significantly slower, check internet connection
- Yahoo Finance may be experiencing delays

### Dependencies
The script requires:
- Python 3.7+
- `yfinance` package
- `pandas` package

Install if missing:
```bash
pip install yfinance pandas
```

## Technical Details

### Data Fetching
- **Source**: Yahoo Finance (`yfinance` library)
- **Format**: `{symbol}.NS` (e.g., `RELIANCE.NS`)
- **Period**: 30 days (1 month) of OHLCV data
- **Parallel Processing**: 10 concurrent threads via ThreadPoolExecutor
- **Error Handling**: Individual stock failures don't stop the scan

### Performance
- **Typical execution**: 20-30 seconds for 50 stocks
- **Network dependent**: Varies with Yahoo Finance API response time
- **Memory usage**: ~50MB for data and processing
- **CSV output**: Typically <5KB for filtered results

### File Locations
- Script: `~/.claude/skills/nifty50-volume-filter/scripts/nifty50_volume_filter.py`
- Data: `~/.claude/skills/nifty50-volume-filter/data/nifty50_constituents.json`
- Default output: `./nifty50_filtered.csv` (current directory)

## Extensions & Customizations

### For Advanced Users

The script can be customized for different needs:

**Different stock universe**: Edit `nifty50_constituents.json` to scan different stocks (e.g., Nifty Next 50, sector-specific stocks)

**Alternative volume periods**: Modify the script to use 10-day or 20-day volume averages

**Additional filters**: Add RSI, MACD, or moving average filters in the `analyze_stock` method

**Swing high patterns**: Adapt the swing low logic to detect swing highs for bullish patterns

**Intraday scanning**: Use intraday data intervals for real-time monitoring (requires different yfinance parameters)

## Summary

This skill provides a focused technical screening tool for Nifty 50 stocks combining volume analysis with price structure patterns. It's most useful for:
- Identifying potential risk in blue-chip holdings
- Finding short-term bearish trading opportunities
- Monitoring market sentiment through blue-chip behavior
- Risk management and portfolio protection

Remember: Technical patterns are just one piece of the puzzle. Always combine with fundamental analysis, news awareness, and proper risk management for trading decisions.
