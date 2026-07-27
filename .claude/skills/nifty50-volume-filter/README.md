# Nifty 50 Volume & Lower Low Filter

A technical screening skill for identifying Nifty 50 stocks showing volume surges with lower low patterns.

## Quick Start

### 1. Install Dependencies

The script requires `yfinance` and `pandas`. Since your system has an externally-managed Python environment, you have a few options:

**Option A: Using pipx (Recommended)**
```bash
# Install pipx if you don't have it
brew install pipx

# Create an isolated environment for this script
cd ~/.claude/skills/nifty50-volume-filter/scripts
pipx install yfinance
pipx install pandas
```

**Option B: Create a virtual environment**
```bash
# Create venv in the skill directory
cd ~/.claude/skills/nifty50-volume-filter
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install yfinance pandas

# Run the script (while venv is active)
python scripts/nifty50_volume_filter.py
```

**Option C: Use --break-system-packages (Not recommended)**
```bash
pip3 install --break-system-packages yfinance pandas
```

### 2. Run the Script

**Basic usage**:
```bash
python3 ~/.claude/skills/nifty50-volume-filter/scripts/nifty50_volume_filter.py
```

**With custom options**:
```bash
# Custom output file
python3 nifty50_volume_filter.py --output my_results.csv

# Adjust swing low detection window
python3 nifty50_volume_filter.py --window 7

# Only show stocks with 1.5x volume or more
python3 nifty50_volume_filter.py --min-volume-ratio 1.5

# Verbose mode (show all progress)
python3 nifty50_volume_filter.py --verbose
```

## What It Does

Scans all 50 Nifty stocks and filters those meeting BOTH criteria:

1. **Volume Filter**: Current volume > 7-day average volume
2. **Lower Low Pattern**: Recent swing low < Previous swing low

Results show stocks with potential bearish momentum (selling pressure + technical weakness).

## Output

- **Console**: Summary table with filtered stocks
- **CSV File**: Detailed results exported to `nifty50_filtered.csv` (or custom path)

## Usage with Claude Code

When using Claude Code, you can simply say:

- "Scan Nifty 50 for high volume stocks making lower lows"
- "Which Nifty stocks show volume surge with weakness?"
- "Screen Nifty 50 for breakdown patterns"

Claude will automatically:
1. Run this skill
2. Display the results
3. Offer to analyze the top stocks in detail

## Files

```
nifty50-volume-filter/
├── SKILL.md                           # Full documentation
├── README.md                          # This file
├── scripts/
│   └── nifty50_volume_filter.py      # Main script
└── data/
    └── nifty50_constituents.json     # List of Nifty 50 stocks
```

## Customization

### Update Nifty 50 List

Edit `data/nifty50_constituents.json` to update the stock list (constituents change quarterly).

### Modify Filters

Edit the script to:
- Change volume period (7-day to 10-day or 20-day)
- Adjust swing low window size
- Add additional technical filters (RSI, MACD, etc.)
- Scan different stock universes (Nifty Next 50, sectoral indices)

## Limitations

- Uses Yahoo Finance (end-of-day data, ~15 min delay during market hours)
- Swing low detection is sensitive to window parameter
- Static Nifty 50 list (last updated: 2026-07-18)
- No consideration of corporate actions (splits, bonuses)

## Interpreting Results

**Strong bearish signals**:
- Volume ratio > 2.0 (strong surge)
- Diff % > 2% (significant breakdown)
- Current price near recent low

**Context matters**:
- Check overall market trend
- Review sector performance
- Read recent news
- Verify with other technical indicators

## Troubleshooting

**"ModuleNotFoundError: No module named 'yfinance'"**
→ Install dependencies (see section 1 above)

**"Insufficient data" errors**
→ Stock may be newly listed or have gaps in history

**No results / Empty output**
→ Try lowering `--min-volume-ratio` or adjusting `--window`

**Slow execution**
→ Normal: 20-30 seconds for 50 stocks. Check internet connection if much slower.

## Examples

**Find stocks with strong volume surge**:
```bash
python3 nifty50_volume_filter.py --min-volume-ratio 2.0 --output strong_volume.csv
```

**More sensitive swing low detection**:
```bash
python3 nifty50_volume_filter.py --window 3 --output sensitive.csv
```

**Less sensitive (major swing lows only)**:
```bash
python3 nifty50_volume_filter.py --window 10 --output major_lows.csv
```

## License

Created with Claude Code - Free to use and modify.

---

For detailed methodology and interpretation, see `SKILL.md`.
