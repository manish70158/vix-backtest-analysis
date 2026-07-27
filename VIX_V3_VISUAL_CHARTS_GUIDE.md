# VIX Backtest V3 - Visual Chart Guide

## What's New in V3

**V3 adds a visual mini-chart column** that lets you see intraday price movement at a glance without opening separate charts!

### New Column: `chart`

Each row now includes a visual representation using Unicode block characters and emojis showing:
- Opening price level
- Intraday low
- Intraday high
- Closing price level
- Overall direction (bullish/bearish)

---

## How to Read the Charts

### Unicode Block Characters

The chart uses 8 levels of Unicode blocks to show relative price levels:

```
▁ = Lowest (1/8)
▂ = Very Low (2/8)
▃ = Low (3/8)
▄ = Medium-Low (4/8)
▅ = Medium-High (5/8)
▆ = High (6/8)
▇ = Very High (7/8)
█ = Highest (8/8)
```

### Direction Indicators

```
↑ = Upward movement
↓ = Downward movement
→ = Sideways/Flat
```

### Final Direction Emojis

```
📈 = Bullish day (Close > Open)
📉 = Bearish day (Close < Open)
━ = Flat day (Close = Open)
```

---

## Chart Format

**Format**: `Open → Movement → Low → Movement → High → Movement → Close Direction`

**Example 1: Bullish Rally**
```
▁↑▁↑█↓▅ 📈
```
**Reading**:
- `▁` = Opened at low level
- `↑` = Moved up from open
- `▁` = Went down to make the low
- `↑` = Rallied up
- `█` = Hit the high (highest point of day)
- `↓` = Pulled back from high
- `▅` = Closed at medium-high level
- `📈` = Net bullish (closed higher than opened)

**Example 2: Bearish Drop**
```
█↓▁↑█↓▁ 📉
```
**Reading**:
- `█` = Opened at high level
- `↓` = Immediately dropped
- `▁` = Made the low (lowest point of day)
- `↑` = Bounced back up
- `█` = Reached back to high
- `↓` = Sold off again
- `▁` = Closed at low level
- `📉` = Net bearish (closed lower than opened)

**Example 3: Range-Bound Day**
```
▄↓▁↑█↓▄ 📈
```
**Reading**:
- `▄` = Opened at medium-low
- `↓` = Dipped down
- `▁` = Hit the low
- `↑` = Rallied strongly
- `█` = Made the high
- `↓` = Came back down
- `▄` = Closed near opening level
- `📈` = Slightly bullish close

---

## Real Examples from the Data

### Example 1: Strong Bullish Day
```
Date: 2020-07-09
Chart: ▃↓▁↑█↓▆ 📈
OHLC: 10755.55 / 10836.85 / 10733.0 / 10813.45
```
**What happened**: Opened medium-low, dipped to the low, rallied strongly to the high, pulled back slightly, closed high. Strong bullish candle.

### Example 2: Volatile Bearish Day
```
Date: 2020-07-30
Chart: ▇↓▁↑█↓▂ 📉
OHLC: 11254.3 / 11299.95 / 11084.95 / 11102.15
```
**What happened**: Opened high, crashed to the low, rallied back to high, collapsed again to close very low. Highly volatile bearish day (underestimated by VIX).

### Example 3: Massive Crash Day
```
Date: 2020-09-24
Chart: █↓▁↑█↓▁ 📉
OHLC: 11011.0 / 11015.3 / 10790.2 / 10805.55
```
**What happened**: Gap down open (already at high), immediate sell-off to low, brief bounce back, then closed near lows. Classic capitulation pattern.

### Example 4: Sideways Grind
```
Date: 2020-10-08
Chart: ▄↓▁↑█↓▄ 📉
OHLC: 11835.4 / 11905.7 / 11791.15 / 11834.6
```
**What happened**: Opened middle, tested low, rallied to high, sold off back to opening level. Range-bound with slight bearish bias.

---

## Quick Visual Patterns to Recognize

### Bullish Patterns

**Strong Bull Trend**
```
▁↑▁↑█→▇ 📈
```
Opens low, stays high, closes near highs = Strength

**Gap Up Hold**
```
▆→▃↑█→▇ 📈
```
Opens high, holds gains all day = Strong buyers

### Bearish Patterns

**Strong Bear Trend**
```
█↓▁→▂→▁ 📉
```
Opens high, collapses to lows, stays low = Weakness

**Failed Rally**
```
▃↑▅↑█↓▁ 📉
```
Tried to rally but sellers dominated = Distribution

### Volatile Patterns

**High Volatility Day**
```
▄↓▁↑█↓▁ 📉
```
Big swings from low to high and back = VIX underestimated

**Whipsaw**
```
▅↑█↓▁↑▄ 📈
```
Multiple reversals, choppy action = Indecision

---

## Using Charts for Quick Analysis

### 1. Scan for Volatility
Look for charts with multiple `↑↓` changes = High volatility days
```
▄↓▁↑█↓▁↑▃ 📈  = Very volatile
▅→▅→▆→▅ 📈   = Low volatility
```

### 2. Identify Trend Days
Charts showing consistent direction = Strong trend
```
▁↑▃↑▆↑█ 📈  = Strong uptrend
█↓▆↓▃↓▁ 📉  = Strong downtrend
```

### 3. Spot Reversals
Look for large gaps between open and close blocks
```
█↓▁ 📉 = Major reversal (opened high, closed low)
▁↑█ 📈 = Major reversal (opened low, closed high)
```

### 4. Check Day Type
- `📈` with large blocks = Strong bullish
- `📉` with large blocks = Strong bearish
- Small blocks + neutral emoji = Range-bound

---

## CSV Column Order in V3

```csv
date, day_of_week, expiry_type, chart, nifty_open, nifty_high, nifty_low,
nifty_close, vix_open, vix_close, vix_predicted_move_pct, actual_range_pct,
actual_open_close_pct, intraday_high_pct, intraday_low_pct, range_vs_vix_ratio,
diff_pct, vix_accuracy
```

**New column**: `chart` (position 4, right after expiry_type)

---

## Practical Use Cases

### Use Case 1: Quick Risk Assessment
**Before opening the full chart**, scan the `chart` column:
- Lots of `↑↓` = High volatility = Widen strikes
- Mostly `→` = Low volatility = Normal strikes

### Use Case 2: Pattern Recognition
Filter by chart patterns:
- All charts showing `█↓▁` pattern = Market crashes
- All charts showing `▁↑█` pattern = Strong rallies

### Use Case 3: VIX Validation
Look at `chart` + `vix_accuracy`:
- Complex chart (`↑↓↑↓`) + Underestimated = VIX missed the volatility
- Simple chart (`→→→`) + Overestimated = VIX was too high

### Use Case 4: Expiry Day Characteristics
Compare weekly vs monthly `chart` patterns:
- Count how many have `↓▁` (crashes) on monthly vs weekly
- Identify if certain patterns appear more on specific expiry types

---

## Tips for Excel/Google Sheets Users

### Viewing in Spreadsheet Software

**Good**: The charts display perfectly in:
- Google Sheets (recommended)
- LibreOffice Calc
- Excel for Mac (recent versions)
- Excel Online

**Potential Issues**:
- Old Excel versions may show boxes instead of Unicode blocks
- Font matters: Use "Segoe UI", "Arial Unicode MS", or "Noto Sans"

### Conditional Formatting Ideas

You can add rules based on patterns:
1. Highlight rows where `chart` contains "📉" = Bearish days
2. Highlight rows where `chart` contains "█↓▁" = Crash patterns
3. Highlight rows where `vix_accuracy` = "Underestimated" AND chart is complex

### Filtering

Filter the CSV by:
- `chart` contains "📈" = Only bullish days
- `chart` contains "█↓▁↑█↓▁" = High volatility days
- `expiry_type` = "monthly" AND `chart` contains "📉" = Bearish monthly expiries

---

## Comparison: V1 vs V2 vs V3

| Feature | V1 | V2 | V3 |
|---------|----|----|-----|
| **Underestimation Logic** | Any difference | >0.2% threshold | >0.2% threshold |
| **Diff Column** | ❌ No | ✅ Yes | ✅ Yes |
| **Visual Charts** | ❌ No | ❌ No | ✅ **Yes** |
| **Day of Week** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Best For** | Conservative | Realistic | Visual Analysis |

---

## Example: Reading a Full Row

```csv
2020-07-30,Thursday,monthly,▇↓▁↑█↓▂ 📉,11254.3,11299.95,11084.95,11102.15,24.11,24.73,1.26,1.91,1.35,0.41,1.5,1.51,0.65,Underestimated
```

**Interpretation**:
- **Date**: 2020-07-30 (Thursday)
- **Type**: Monthly expiry
- **Chart**: `▇↓▁↑█↓▂ 📉`
  - Opened very high (▇)
  - Dropped immediately (↓)
  - Hit the low (▁)
  - Bounced to high (↑█)
  - Crashed again (↓)
  - Closed very low (▂)
  - Net bearish (📉)
- **OHLC**: 11254.3 / 11299.95 / 11084.95 / 11102.15
- **VIX**: Predicted 1.26%, Actual 1.91%
- **Result**: Underestimated (diff +0.65%)

**What this tells us**: This was a highly volatile bearish day on a monthly expiry where VIX significantly underestimated the actual movement. The chart shows the whipsaw nature of the day.

---

## Files Generated

### V3 Files (With Visual Charts)
- ✅ **vix_all_expiries_results_v3.csv** - Complete dataset with `chart` column
- ✅ **vix_all_expiries_results_v3.json** - JSON with chart data
- ✅ **backtest_vix_all_expiries_v3.py** - Script with chart generation

### Previous Versions (For Comparison)
- `vix_all_expiries_results.csv` (V1 - original)
- `vix_all_expiries_results_v2.csv` (V2 - with 0.2% threshold)

---

## Command to Run V3

```bash
# Run for last 6 years (recommended)
python3 backtest_vix_all_expiries_v3.py --years 6

# Run for last 2 years
python3 backtest_vix_all_expiries_v3.py --years 2

# Custom output filenames
python3 backtest_vix_all_expiries_v3.py --years 6 --csv my_results.csv --json my_results.json
```

---

## Summary

**V3 is the most comprehensive version:**
- ✅ Includes all V2 improvements (0.2% threshold, diff_pct)
- ✅ Adds visual mini-charts for at-a-glance analysis
- ✅ Preserves all numerical data
- ✅ Easy to scan and identify patterns
- ✅ Perfect for quick risk assessment

**Best use**: Open the CSV in Google Sheets and you can immediately see which days had volatile moves, which were trend days, and which were range-bound - all without opening TradingView!

---

**Generated**: July 25, 2026
**Data**: 317 expiry days with visual charts
**Recommendation**: Use V3 for comprehensive visual analysis
