# Kite Options Volume Alert

Real-time options volume monitoring with alerts on new 5-minute highs.

## Quick Start

### Using with Claude Code (Recommended)

Simply ask Claude:
```
"Monitor volume for NIFTY 24500 CE July 2026"
"Alert me when BANKNIFTY 52000 PE weekly volume spikes"
"Track options volume for NIFTY 24000 CE"
```

Claude will:
1. Parse your natural language input
2. Search for the exact option contract via Kite MCP
3. Start monitoring volume every 5 minutes
4. Alert you with console, desktop notification, and sound when volume breaks previous highs

### Manual Usage

```bash
python .claude/skills/kite-options-volume-alert/scripts/options_volume_monitor.py "NIFTY 24500 CE July 2026"
```

**Options**:
- `--interval SECONDS` - Check interval (default: 300 = 5 minutes)
- `--verbose` - Detailed logging

## What It Does

1. **Parses natural language** option descriptions
   - "NIFTY 24500 CE July 2026"
   - "BANKNIFTY 52000 PE weekly"

2. **Finds the contract** via Kite MCP server
   - Searches by underlying + strike + type + expiry
   - Returns exact instrument token

3. **Monitors volume** every 5 minutes
   - Fetches 5-minute candle data
   - Tracks all volumes since monitoring started

4. **Alerts on new highs**
   - When current 5-min volume > all previous readings
   - Console output + Desktop notification + Sound beep

## Prerequisites

1. **Kite MCP Server** configured in Claude Code
2. **Kite login** - Run once to authorize:
   ```
   Ask Claude: "Login to Kite"
   ```
3. **Python 3.7+** installed
4. **macOS** (for desktop notifications - optional)

## Examples

### Monitor NIFTY Call Option
```bash
python options_volume_monitor.py "NIFTY 24500 CE July 2026"
```

### Monitor BANKNIFTY Put (Weekly)
```bash
python options_volume_monitor.py "BANKNIFTY 52000 PE weekly"
```

### Custom 2-Minute Checks
```bash
python options_volume_monitor.py "NIFTY 24500 CE July 2026" --interval 120
```

### Verbose Mode
```bash
python options_volume_monitor.py "NIFTY 24500 CE July 2026" --verbose
```

## Alert Example

When volume breaks previous high:
```
================================================================================
🚨 VOLUME ALERT 🚨
New 5-min volume high detected for NFO:NIFTY26JUL24500CE!
Current: 45,230 | Previous High: 38,750 | +16.7%
Volume: 45,230
================================================================================
```

Plus:
- Desktop notification (with sound)
- Three system beeps

## Supported Underlyings

- NIFTY
- BANKNIFTY
- FINNIFTY
- MIDCPNIFTY
- SENSEX
- BANKEX

## Input Format

The script understands various formats:

| Format | Example |
|--------|---------|
| Full specification | `"NIFTY 24500 CE July 2026"` |
| Weekly expiry | `"BANKNIFTY 52000 PE weekly"` |
| Monthly expiry | `"FINNIFTY 22000 CE monthly"` |
| Short format | `"NIFTY 24000 PE Jul 26"` |

**Required components**:
- Underlying (NIFTY, BANKNIFTY, etc.)
- Strike price (numeric)
- Option type (CE or PE)
- Expiry (month/year, weekly, or monthly)

## Stopping

Press `Ctrl+C` to stop. You'll see a summary:
```
--- Monitoring Summary ---
Total checks: 15
Highest volume: 52,340
Lowest volume: 12,450
Average volume: 28,765
```

## Troubleshooting

### "Could not identify underlying"
✓ Use: NIFTY, BANKNIFTY (all caps, no spaces)
✗ Avoid: Nifty, Bank Nifty

### "Could not identify strike"
✓ Use: "NIFTY 24500 CE"
✗ Avoid: "NIFTY CE" (missing strike)

### "Could not identify option type"
✓ Use: CE or PE
✗ Avoid: CALL, PUT (use CE/PE instead)

### No alerts
- Volume may be declining
- Try more liquid strikes (closer to ATM)
- Increase monitoring period

### Rate limiting
- Default 5-min interval is safe
- Don't use intervals < 60 seconds
- Kite has rate limits on API calls

## MCP Integration

### Important Note

The script uses Kite MCP tools:
- `mcp__kite__search_instruments` - Find option contracts
- `mcp__kite__get_historical_data` - Fetch 5-minute volume

**Running through Claude Code**: Claude automatically has access to these MCP tools

**Running standalone**: Requires MCP server setup (advanced - see SKILL.md for details)

## Files

```
kite-options-volume-alert/
├── SKILL.md                          # Full documentation
├── README.md                         # This file
└── scripts/
    └── options_volume_monitor.py    # Main monitoring script
```

## Use Cases

### Intraday Trading
Monitor ATM options during active hours to catch volume breakouts

### Event Monitoring
Track specific strikes before earnings, policy announcements

### Scalping
Use 2-3 minute intervals for rapid volume-based entries

### Multi-Strike Tracking
Run multiple instances to monitor several strikes simultaneously

## Limitations

- **5-minute granularity** (no tick data)
- **Single contract per instance** (run multiple for multi-option monitoring)
- **Market hours only** (no pre-market data)
- **macOS notifications** (Linux/Windows may need adjustments)

## Tips

1. **Start after market open** - First 30 minutes can be noisy
2. **ATM options** - Better liquidity = more meaningful alerts
3. **5-min intervals** - Good balance between responsiveness and noise
4. **Keep terminal visible** - Don't miss console alerts

## License

Created with Claude Code - Free to use and modify

---

For detailed methodology, troubleshooting, and extensions, see `SKILL.md`.
