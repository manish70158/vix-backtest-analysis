# Excel Files with Conditional Formatting

## What's Been Created

All VIX backtest CSV files have been converted to Excel format with **green background highlighting** applied:

```
✅ vix_all_expiries_results_v2_formatted.xlsx
✅ vix_all_expiries_results_v3_formatted.xlsx
✅ vix_all_expiries_results_v4_formatted.xlsx
✅ vix_all_expiries_results_v5_formatted.xlsx
```

## What Does Green Highlighting Mean?

**Green rows = VIX was "almost right" but slightly underestimated**

Specifically, rows are highlighted in green when:
- **Difference (actual_range_pct - vix_predicted_move_pct) is between 0.0% and 0.5%**
- VIX predicted the move within acceptable range
- Actual movement exceeded VIX prediction by a small margin

### Why This Range Matters

| Difference | What It Means | Highlighted? |
|------------|---------------|--------------|
| **Negative** | VIX overestimated (movement < prediction) | ❌ No |
| **0.0 - 0.2%** | Very close, minor underestimation | ✅ **Yes (Green)** |
| **0.2 - 0.5%** | Noticeable but acceptable underestimation | ✅ **Yes (Green)** |
| **> 0.5%** | Significant underestimation | ❌ No |

### At NIFTY 25,000 Levels

Green highlighted rows represent:
- **0 - 125 points** difference between predicted and actual
- VIX was reasonably accurate
- Within "acceptable miss" range for most traders

## What 120 Highlighted Rows Tells Us

Out of 317 total expiry days:
- **120 rows highlighted** (37.9%) = VIX was close (0.0-0.5% miss)
- **125 rows** (39.4%) = VIX overestimated (negative difference)
- **69 rows** (21.8%) = VIX significantly underestimated (>0.5% miss)
- **3 rows** (0.9%) = Perfect or extremely close (<0.01% diff)

**Key Insight**: Green rows (37.9%) represent the "sweet spot" where VIX provides useful guidance but traders should widen margins slightly.

## Distribution Breakdown

### All 317 Expiry Days

```
📊 Difference Distribution:
   VIX Overestimated (< 0.0%):        125 rows (39.4%)

   GREEN HIGHLIGHTED ZONE:            120 rows (37.9%)
   ├─ 0.0 - 0.2% (minor):              59 rows (18.6%)
   └─ 0.2 - 0.5% (noticeable):         61 rows (19.2%)

   Significant Miss (> 0.5%):          69 rows (21.8%)
   └─ These exceed green threshold
```

## How to Use These Files

### 1. Quick Visual Analysis

Open any `*_formatted.xlsx` file:
- **White rows** = VIX overestimated OR significantly underestimated
- **Green rows** = VIX was close, slight underestimation

### 2. Trading Strategy Development

**For Premium Sellers**:
- Focus on green rows + white overestimated rows
- These are days where VIX provided good coverage
- Safe to sell at VIX-implied strikes

**For Premium Buyers**:
- Focus on white rows with large positive diff (>0.5%)
- These are days where VIX badly underestimated
- Opportunity for cheap protection

### 3. Risk Management

**Green rows = Normal risk**
- Standard position sizing
- VIX-based stop losses work well
- Typical margin requirements sufficient

**White rows (>0.5% diff) = High risk**
- Increase position margins
- Widen stop losses
- Consider reducing size on expiry day

## Comparison Across Versions

All versions (V2, V3, V4, V5) have **identical green highlighting**:
- Same 120 rows highlighted
- Same 0.0-0.5% threshold
- Only the `vix_accuracy` classification differs

### What Changes Between Versions

| Version | Threshold | Classification Impact | Green Rows |
|---------|-----------|----------------------|------------|
| V2 | 0.2% | 61 green rows = "Underestimated" | 120 (same) |
| V3 | 0.2% | 61 green rows = "Underestimated" | 120 (same) |
| V4 | 0.4% | All 120 green rows = "Overestimated" | 120 (same) |
| V5 | 0.5% | All 120 green rows = "Overestimated" | 120 (same) |

**Why this matters**:
- Green highlighting is **absolute** (0.0-0.5% range)
- Version classification is **relative** to threshold
- V4/V5 classify green rows as "Overestimated" because diff < threshold

## Examples

### Example 1: Light Green Row (0.15% diff)

```
Date: 2020-07-16
VIX Predicted: 1.38% | Actual: 1.50% | Diff: +0.12%

- Highlighted: ✅ Yes (green)
- V2/V3 classification: "Overestimated" (0.12% < 0.2%)
- V4/V5 classification: "Overestimated" (0.12% < 0.4/0.5%)
- Trading impact: Minimal, VIX was very accurate
```

### Example 2: Medium Green Row (0.35% diff)

```
Date: Example
VIX Predicted: 0.80% | Actual: 1.15% | Diff: +0.35%

- Highlighted: ✅ Yes (green)
- V2/V3 classification: "Underestimated" (0.35% > 0.2%)
- V4/V5 classification: "Overestimated" (0.35% < 0.4/0.5%)
- Trading impact: Noticeable, widen strikes by ~90 points
```

### Example 3: NOT Green (0.65% diff)

```
Date: 2020-07-30
VIX Predicted: 1.26% | Actual: 1.91% | Diff: +0.65%

- Highlighted: ❌ No (exceeds 0.5% threshold)
- All versions: "Underestimated"
- Trading impact: Major, VIX badly missed
- NIFTY equivalent: ~165 points at 25,000 levels
```

## Filtering in Excel

### To see only green highlighted rows:
1. Open file in Excel
2. Click any cell in the data
3. Data → Filter
4. Click filter dropdown on any column
5. Filter by Color → Green

### To see only extreme misses (>0.5%):
1. Select `diff_pct` column
2. Filter → Number Filters → Greater Than
3. Enter: 0.5

## Regenerating Files

If you modify the CSV files and want to regenerate the Excel formatting:

```bash
# Format a specific version
python3 .claude/skills/nifty-expiry-vix-backtest/scripts/format_excel_with_colors.py vix_all_expiries_results_v5.csv

# Format with custom output name
python3 .claude/skills/nifty-expiry-vix-backtest/scripts/format_excel_with_colors.py vix_all_expiries_results_v5.csv -o my_formatted.xlsx

# Format all versions
for v in v2 v3 v4 v5; do
  python3 .claude/skills/nifty-expiry-vix-backtest/scripts/format_excel_with_colors.py vix_all_expiries_results_${v}.csv
done
```

## Key Takeaway

**Green = VIX's "acceptable miss" zone**
- 120 out of 317 days (37.9%)
- 0-125 points difference at NIFTY 25,000
- Useful guidance from VIX, but widen margins slightly
- Not crisis-level underestimation

---

**Generated**: July 25, 2026
**Tool**: format_excel_with_colors.py
**Applies to**: All versions (V2, V3, V4, V5)
