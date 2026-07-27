---
name: kite-options-volume-alert
description: Monitor real-time options volume via Kite and alert when new 5-minute volume highs are detected. Accepts natural language option descriptions (e.g., "NIFTY 24500 CE July 2026") and provides console, desktop, and sound alerts. Use when user wants to track option volume, monitor options activity, set up volume alerts for options trading, or watch for unusual options volume. Trigger on phrases like "monitor option volume", "alert me on options volume", "track NIFTY options", "watch option activity", "volume alert for options", "kite options monitoring".
---

# Kite Options Volume Alert

Real-time monitoring of options volume through Kite, with alerts when new 5-minute volume highs are detected.

## Purpose

This skill helps options traders:
- **Monitor specific options contracts** in real-time
- **Track volume patterns** across 5-minute intervals
- **Get instant alerts** when volume breaks previous highs
- **Identify unusual activity** in options without constant chart watching

Perfect for:
- Intraday options trading
- Detecting sudden interest in specific strikes
- Volume breakout strategies
- Options scalping with volume confirmation

## When to Use This Skill

Use this skill when the user wants to:
- Monitor volume for a specific options contract
- Get alerts on increasing options activity
- Track real-time volume changes
- Set up automated volume monitoring
- Watch for volume spikes in options

**Trigger phrases**: "monitor NIFTY options volume", "alert me when option volume increases", "track options activity", "watch for volume spike in options", "monitor call option volume", "set up options alert"

## How It Works

### Volume Monitoring Logic

The script:
1. **Parses natural language input** to identify the option (underlying, strike, expiry, CE/PE)
2. **Searches Kite instruments** to find the exact contract
3. **Polls volume data** every 5 minutes (configurable)
4. **Tracks historical highs** since monitoring started
5. **Alerts immediately** when current 5-min volume exceeds all previous readings

**Alert Condition**: Current 5-minute volume > Maximum of all previous 5-minute volumes

### Natural Language Parsing

The skill understands various formats:

**Supported Formats**:
- `"NIFTY 24500 CE July 2026"` - Full specification with month/year
- `"BANKNIFTY 52000 PE weekly"` - Weekly expiry
- `"FINNIFTY 22000 CE monthly"` - Monthly expiry
- `"NIFTY 24000 PE Jul 26"` - Short format

**Components Extracted**:
- **Underlying**: NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY, SENSEX, BANKEX
- **Strike**: Any numeric value (e.g., 24500, 52000)
- **Type**: CE (Call) or PE (Put)
- **Expiry**: weekly, monthly, or specific month/year

### Alert Channels

When a new volume high is detected, you receive:

1. **Console Alert** (Color-coded terminal output)
   ```
   ================================================================================
   🚨 VOLUME ALERT 🚨
   New 5-min volume high detected for NFO:NIFTY26JUL24500CE!
   Current: 45,230 | Previous High: 38,750 | +16.7%
   Volume: 45,230
   ================================================================================
   ```

2. **Desktop Notification** (macOS native notification with sound)
   - Appears in notification center
   - Includes contract name and volume details
   - Plays "Glass" sound

3. **Sound Alert** (System beeps)
   - Three distinct beeps
   - Works on all platforms

## Running the Skill

### Prerequisites

1. **Kite MCP Server** must be configured and accessible
2. **Login to Kite** before monitoring:
   ```bash
   # User must authorize Kite access first
   # Claude will prompt for authorization if needed
   ```

3. **Python 3.7+** installed

### Basic Usage

When the user asks to monitor an option, run:

```bash
python .claude/skills/kite-options-volume-alert/scripts/options_volume_monitor.py "NIFTY 24500 CE July 2026"
```

### Command Options

**Monitor with default 5-minute interval**:
```bash
python options_volume_monitor.py "NIFTY 24500 CE July 2026"
```

**Custom check interval** (e.g., every 2 minutes):
```bash
python options_volume_monitor.py "NIFTY 24500 CE July 2026" --interval 120
```

**Verbose mode** (more detailed logging):
```bash
python options_volume_monitor.py "NIFTY 24500 CE July 2026" --verbose
```

**Weekly/Monthly options**:
```bash
# Weekly expiry
python options_volume_monitor.py "BANKNIFTY 52000 PE weekly"

# Monthly expiry
python options_volume_monitor.py "NIFTY 24000 CE monthly"
```

### Stopping Monitoring

Press `Ctrl+C` to stop monitoring. The script will display a summary:
```
--- Monitoring Summary ---
Total checks: 15
Highest volume: 52,340
Lowest volume: 12,450
Average volume: 28,765
```

## Typical Workflow

### Scenario 1: Monitor Single Option

**User**: "Monitor volume for NIFTY 24500 CE July expiry"

**Your Response**:
```
I'll set up volume monitoring for the NIFTY 24500 CE July option.

[Run the script]

Monitoring started! The script will:
- Check volume every 5 minutes
- Alert you when volume breaks previous highs
- Show desktop notifications and sound alerts
- Run until you press Ctrl+C

Keep the terminal window open to receive alerts.
```

### Scenario 2: Detect Volume Spike

When volume alert triggers:
```
🚨 VOLUME ALERT 🚨
New 5-min volume high detected for NFO:NIFTY26JUL24500CE!
Current: 45,230 | Previous High: 38,750 | +16.7%

This indicates increased interest in this strike. You may want to:
- Check the current price and IV
- Look for related news or market moves
- Consider if this aligns with your trading strategy
```

### Scenario 3: Multiple Options

If user wants to monitor multiple options:
```
For monitoring multiple options, I'll need to run separate instances.
Let me start monitors for each:

1. NIFTY 24500 CE July 2026
2. NIFTY 24000 PE July 2026

Each will run in a separate terminal window with independent alerts.
```

## Interpreting Alerts

### High-Value Alerts

**Strong Signal** (>30% increase from previous high):
- Significant new interest
- Potential breakout or breakdown
- May indicate institutional activity
- Worth immediate attention

**Moderate Signal** (10-30% increase):
- Increasing activity
- Building momentum
- Monitor closely

**Weak Signal** (<10% increase):
- Minor uptick
- Normal variation
- May be noise

### Context Matters

Always consider:
1. **Overall market direction** - Is the index moving significantly?
2. **Time of day** - Opening/closing hours typically see higher volume
3. **News events** - Earnings, policy announcements, etc.
4. **Options expiry proximity** - Near expiry sees higher volume

### False Signals

- **First few readings**: Initial volumes might be low, making subsequent readings appear as "highs"
- **Market open**: First 15-30 minutes can be volatile
- **Low liquidity strikes**: Far OTM options may show erratic volume

## Best Practices

### Timing

- **Start monitoring 30 minutes after market open** - Avoids opening volatility
- **Run during active hours** (9:45 AM - 3:15 PM IST)
- **Stop before expiry day chaos** - Last day volumes are atypical

### Strike Selection

- **ATM and near-ATM** options have better liquidity and meaningful volume
- **Deep ITM/OTM** may have sparse volume (many false alerts)
- **Focus on liquid underlyings** - NIFTY, BANKNIFTY have best volume

### Interval Selection

- **5 minutes (default)**: Good for intraday scalping
- **2-3 minutes**: More frequent alerts, higher noise
- **10-15 minutes**: Longer-term monitoring, clearer trends

### Multiple Options

To monitor multiple strikes simultaneously:
1. Open separate terminal windows
2. Run script for each option
3. Position windows to see all alerts
4. Or use a terminal multiplexer (tmux/screen)

## Integration with Trading

### Volume + Price Confirmation

When alert triggers:
1. **Check current price** - Use `/trade-quick NIFTY` or similar
2. **Review technical levels** - Support/resistance nearby?
3. **Check IV** - Is implied volatility increasing?
4. **Verify with chart** - Visual confirmation helps

### Strategy Examples

**Volume Breakout Strategy**:
```
1. Set up monitor on ATM options
2. When volume alert triggers AND price breaks key level → Enter
3. Stop loss below breakout point
4. Target based on options premium movement
```

**Contrarian Strategy**:
```
1. Monitor extreme OTM options
2. Unusual volume spike → Possible hedge/large position
3. Consider counter-trend position with tight risk
```

## Troubleshooting

### "Could not identify underlying"
- Ensure spelling: NIFTY (not Nifty), BANKNIFTY (not Bank Nifty)
- Supported: NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY, SENSEX, BANKEX

### "Could not identify strike price"
- Must include numeric strike: "24500", "52000"
- Use space-separated format: "NIFTY 24500 CE" (not "NIFTY24500CE")

### "Could not identify option type"
- Include CE (call) or PE (put)
- Capitalization doesn't matter: "ce", "CE", "Ce" all work

### "No instruments found"
- Option may not exist yet (future expiry dates)
- Check expiry calendar on NSE website
- Try "weekly" or "monthly" instead of specific month

### No alerts appearing
- Volume might be declining (no new highs)
- Increase monitoring period to see more data
- Try a more liquid strike (closer to ATM)

### Rate limiting / API errors
- Default 5-minute interval is safe
- Intervals <60 seconds may hit Kite rate limits
- If errors persist, increase interval or contact Kite support

## Technical Details

### Data Source
- **Real-time data**: Kite MCP server via `get_historical_data`
- **Interval**: 5-minute candles
- **Latency**: ~15-30 seconds (depends on Kite API)

### Volume Calculation
- Uses completed 5-minute candle volume
- Does not include current incomplete candle
- All volume comparisons are apples-to-apples (5-min to 5-min)

### Kite MCP Tools Used

1. **search_instruments** (via `underlying` filter)
   - Finds options contracts for specified underlying
   - Returns instrument token and tradingsymbol

2. **get_historical_data** (5-minute intervals)
   - Fetches recent volume data
   - Returns OHLCV candles for specified timeframe

### Resource Usage
- **CPU**: Minimal (polling only)
- **Memory**: <50MB
- **Network**: One API call per interval (5 min = 12 calls/hour)
- **Kite API limits**: Well within normal quotas

### File Locations
- Script: `.claude/skills/kite-options-volume-alert/scripts/options_volume_monitor.py`
- No configuration files needed (runtime parameters only)

## Limitations

### Data Limitations
- **No tick-by-tick data**: 5-minute granularity only
- **Historical context**: Only tracks since monitoring started (not full day history)
- **Single contract**: Can only monitor one option per script instance

### Alert Limitations
- **Desktop notifications**: macOS only (Linux support possible with modifications)
- **Sound alerts**: Basic system beep (not customizable)
- **No external integrations**: No Telegram, email, or webhook alerts (can be added)

### Market Limitations
- **Market hours only**: Outside market hours, data won't update
- **Liquidity dependent**: Low-volume options may have stale data
- **No pre-market**: Pre-market options activity not captured

## Extending the Skill

### Adding More Alert Channels

**Telegram Bot** (add to script):
```python
import requests

def send_telegram_alert(message):
    bot_token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message})
```

**Email Alert**:
```python
import smtplib

def send_email_alert(message):
    # SMTP configuration
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("your_email@gmail.com", "password")
    server.send_message(subject="Options Alert", body=message)
```

### Volume Spike Detection (Alternative Logic)

Instead of "breaking previous high", detect spikes vs average:
```python
# In get_5min_volume, after fetching volume:
if len(self.volume_history) >= 6:
    avg_volume = sum(self.volume_history[-6:]) / 6
    if volume > avg_volume * 1.5:  # 50% above average
        self.send_alert(f"Volume spike: {volume} vs avg {avg_volume}")
```

### Multi-Option Monitoring

Create a wrapper script to monitor multiple options:
```python
import subprocess

options = [
    "NIFTY 24500 CE July 2026",
    "NIFTY 24000 PE July 2026"
]

for option in options:
    subprocess.Popen([
        'python', 'options_volume_monitor.py', option
    ])
```

## Summary

This skill provides automated, real-time monitoring of options volume through Kite's MCP server. It's designed for active options traders who want to catch volume breakouts without constantly watching charts.

**Key Features**:
- Natural language option input
- Real-time 5-minute volume tracking
- Multi-channel alerts (console + desktop + sound)
- Historical high tracking
- Easy to use, runs standalone

**Best For**:
- Intraday options trading
- Volume breakout strategies
- Monitoring specific strikes during events
- Detecting unusual options activity

Remember: Volume is just one indicator. Always combine with price action, technical levels, and market context for trading decisions.
