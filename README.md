# VIX Expiry Analysis & Trading Skills

## VIX Expiry Day Analysis — Keeping Data Updated

### Data Files

| File | Description |
|------|-------------|
| `fii_dii_backtest_daily_results.csv` | Daily FII/DII participant positions from NSE (since Aug 2025) |
| `vix_fii_t1_intraday_expiry_results.csv` | Expiry day analysis: VIX prediction vs actual move + T-1 FII/PRO stance |
| `vix_all_expiries_results_v6_6years.csv` | Base 6-year backtest data (Jul 2020 – Jul 2026, read-only source) |

### How to Update (Run After Each Expiry)

```bash
python3 update_data.py
```

This single command does:
1. Fetches new daily FII/DII positions from NSE archives (incremental)
2. Adds new expiry days to the expiry results CSV
3. Correctly computes `close_vs_prev_range` using the previous **trading day's** high/low
4. Fetches T-1 FII + PRO data for new expiry days

### Full Rebuild (Only If Data Seems Wrong)

If you need to regenerate the entire expiry CSV from scratch (fixes all historical data):

```bash
python3 build_full_6year_expiry.py
```

This takes ~10-15 minutes (NSE rate limiting) and:
- Recomputes `close_vs_prev_range` and `prev_close_to_close_pct` for ALL rows using actual previous trading day data from yfinance
- Fetches T-1 FII + PRO data from NSE archives for all 320+ expiry days

### Key Columns Explained

| Column | Meaning |
|--------|---------|
| `close_vs_prev_range` | Is expiry close Above High / Within Range / Below Low of **previous trading day** |
| `prev_close_to_close_pct` | % change from previous trading day's close to expiry close |
| `t1_fii_fut_daily` | FII futures position change on T-1 day |
| `t1_fii_stance` | FII positioning interpretation (Bullish/Bearish/Hedging/etc.) |
| `t1_pro_fut_daily` | PRO (Proprietary) futures position change on T-1 day |
| `t1_pro_stance` | PRO positioning interpretation |
| `expiry_risk_level` | Blowout risk based on FII stance (HIGH/MODERATE/LOW/SAFE) |

### Requirements

```bash
pip install pandas yfinance requests
```

---

## Trading Skills

Two custom skills for Indian stock and options trading with real-time monitoring and screening.

## Skills Included

### 1. Nifty 50 Volume & Lower Low Filter
Screen Nifty 50 stocks for bearish patterns (volume surge + lower lows).

**Location**: `.claude/skills/nifty50-volume-filter/`

### 2. Kite Options Volume Alert
Real-time monitoring of options volume with alerts on new 5-minute highs.

**Location**: `.claude/skills/kite-options-volume-alert/`

---

## Quick Start Guides

### Nifty 50 Volume Filter

#### What It Does
Finds Nifty 50 stocks showing:
- Volume > 7-day average (selling pressure)
- Recent swing low < Previous swing low (bearish pattern)

#### How to Use

**Option 1: Via Claude**
```
Ask: "Scan Nifty 50 for high volume stocks with lower lows"
```

**Option 2: Run Script**
```bash
/opt/homebrew/bin/python3 .claude/skills/nifty50-volume-filter/scripts/nifty50_volume_filter.py
```

#### Sample Output
```
| Symbol     | Current Vol | 7D Avg Vol | Ratio | Recent Low | Previous Low |
|------------|-------------|------------|-------|------------|--------------|
| RELIANCE   | 18.3M       | 12.8M      | 1.43  | ₹1271.60   | ₹1290.00     |
| TATASTEEL  | 15.2M       | 8.1M       | 1.88  | ₹125.30    | ₹127.50      |
```

**Exported to**: `nifty50_filtered.csv`

#### Requirements
- Python 3.7+
- `yfinance` and `pandas` packages
```bash
/opt/homebrew/bin/pip3 install yfinance pandas
```

---

### Kite Options Volume Alert

#### What It Does
Monitors a specific option contract and alerts when 5-minute volume breaks previous highs.

#### How to Use

**Step 1: Login to Kite**
```
Ask Claude: "Login to Kite"
```
Click the authorization link.

**Step 2: Start Monitoring**
```
Ask Claude: "Monitor volume for NIFTY 24500 CE July 2026"
```

#### Sample Alert
```
🚨 VOLUME ALERT 🚨
New 5-min volume high detected for NFO:NIFTY26JUL24500CE!
Current: 45,230 | Previous High: 38,750 | +16.7%
```

Plus: Desktop notification + Sound beeps

#### Supported Formats
- `"NIFTY 24500 CE July 2026"` - Full specification
- `"BANKNIFTY 52000 PE weekly"` - Weekly expiry
- `"FINNIFTY 22000 CE monthly"` - Monthly expiry

#### Requirements
- Kite MCP server configured
- Python 3.7+
- Kite login authorization

---

## Installation & Setup

### 1. Python Dependencies

Both skills need Python packages:

```bash
# Using Homebrew Python (recommended for this setup)
/opt/homebrew/bin/pip3 install yfinance pandas

# OR using system Python
pip3 install --break-system-packages yfinance pandas
```

### 2. Kite Setup (For Options Monitoring Only)

The options volume alert skill requires Kite MCP:

1. Ensure Kite MCP server is configured in Claude Code
2. Login when prompted:
   ```
   Ask Claude: "Login to Kite"
   ```
3. Authorize access via the browser link

### 3. Verify Installation

**Test Nifty 50 Filter**:
```bash
/opt/homebrew/bin/python3 .claude/skills/nifty50-volume-filter/scripts/nifty50_volume_filter.py --help
```

**Test Kite Login**:
```
Ask Claude: "Check Kite login status"
```

---

## Usage Examples

### Example 1: Daily Nifty 50 Screening

Run every morning to find weak stocks:
```bash
cd .claude/skills/nifty50-volume-filter
/opt/homebrew/bin/python3 scripts/nifty50_volume_filter.py --min-volume-ratio 1.5 --output today.csv
```

Review `today.csv` for potential shorts or stocks to avoid.

### Example 2: Intraday Options Trading

Monitor option volume while trading:
```
9:45 AM: Ask Claude: "Monitor NIFTY 24500 CE July"
         Claude starts monitoring...

10:30 AM: 🚨 Volume Alert!
          Check chart → Confirm breakout → Enter trade

3:00 PM: Ask Claude: "Stop monitoring"
         Review summary
```

### Example 3: Combined Strategy

```
1. Morning: Run Nifty 50 filter to find weak stocks
   → Output: RELIANCE showing volume + lower low

2. Identify direction: RELIANCE bearish

3. Check options: RELIANCE 1250 PE showing volume

4. Monitor: "Monitor RELIANCE 1250 PE weekly"
   → Get alerts on volume spikes
   → Enter on confirmation
```

---

## File Structure

```
.claude/skills/
├── nifty50-volume-filter/
│   ├── SKILL.md                      # Full documentation
│   ├── README.md                     # Setup guide
│   ├── data/
│   │   └── nifty50_constituents.json # List of 50 stocks
│   └── scripts/
│       └── nifty50_volume_filter.py  # Main script
│
└── kite-options-volume-alert/
    ├── SKILL.md                      # Full documentation
    ├── README.md                     # Technical guide
    ├── GETTING_STARTED.md            # Quick start
    ├── data/
    │   └── MCP_INTEGRATION.md        # MCP details
    └── scripts/
        └── options_volume_monitor.py # Main script
```

---

## Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'yfinance'"

**Fix**:
```bash
/opt/homebrew/bin/pip3 install yfinance pandas
```

Then use Homebrew Python to run scripts:
```bash
/opt/homebrew/bin/python3 script.py
```

### Issue: "Kite session expired"

**Fix**:
```
Ask Claude: "Login to Kite"
```
Reauthorize access.

### Issue: "No stocks matching criteria" (Nifty Filter)

**Fix**:
- Lower the volume ratio: `--min-volume-ratio 0.8`
- Adjust swing window: `--window 3`
- Run during active market conditions

### Issue: "Could not find instrument" (Options)

**Fix**:
- Check spelling: `NIFTY` not `Nifty`
- Verify expiry: Use `"weekly"` or `"monthly"`
- Check NSE calendar for valid expiry dates

---

## Best Practices

### Nifty 50 Filter
- ✅ Run after market close (3:30 PM IST) for complete data
- ✅ Use with other analysis (fundamentals, news, sector trends)
- ✅ Export to CSV for tracking over days
- ✅ Adjust parameters based on market conditions

### Options Monitor
- ✅ Start monitoring 30 mins after market open
- ✅ Choose liquid strikes (ATM or near-ATM)
- ✅ Use 5-minute default interval (don't go below 1 min)
- ✅ Confirm volume alerts with price action and IV

### General
- ⚠️ Volume alone is not a trading signal
- ⚠️ Always use stop losses
- ⚠️ Verify with multiple indicators
- ⚠️ Paper trade before using real capital

---

## Documentation

### Nifty 50 Filter
- **Full Guide**: `.claude/skills/nifty50-volume-filter/SKILL.md`
- **Quick Ref**: `.claude/skills/nifty50-volume-filter/README.md`

### Options Monitor
- **Full Guide**: `.claude/skills/kite-options-volume-alert/SKILL.md`
- **Quick Start**: `.claude/skills/kite-options-volume-alert/GETTING_STARTED.md`
- **Technical**: `.claude/skills/kite-options-volume-alert/README.md`
- **MCP Setup**: `.claude/skills/kite-options-volume-alert/data/MCP_INTEGRATION.md`

---

## Getting Help

### Ask Claude
Both skills work best through Claude Code:
```
"How do I use the Nifty 50 filter?"
"Show me how to monitor options volume"
"Explain the volume alert I just got"
```

### Manual Help
```bash
# Nifty 50 Filter help
python3 .claude/skills/nifty50-volume-filter/scripts/nifty50_volume_filter.py --help

# Options Monitor help
python3 .claude/skills/kite-options-volume-alert/scripts/options_volume_monitor.py --help
```

---

## Disclaimer

These tools are for educational and informational purposes only. Not financial advice. Trading stocks and options involves risk of loss. Always do your own research and consult with a qualified financial advisor before making trading decisions.

---

## Support & Contributions

- **Issues**: Report bugs or request features by asking Claude
- **Improvements**: Both skills can be extended with additional filters, alerts, and integrations
- **Customization**: Modify scripts to suit your trading style

---

## Quick Reference

### Nifty 50 Filter - One-Liner
```bash
/opt/homebrew/bin/python3 .claude/skills/nifty50-volume-filter/scripts/nifty50_volume_filter.py
```

### Options Monitor - One-Liner
```
Ask Claude: "Monitor NIFTY 24500 CE July"
```

### Check Both Skills Installed
```bash
ls -la .claude/skills/
```

Should show:
- `nifty50-volume-filter/`
- `kite-options-volume-alert/`

---

**Last Updated**: August 25, 2026
**Created with**: Claude Code + Skill Creator
