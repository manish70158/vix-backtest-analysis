# Getting Started with Kite Options Volume Alert

A simple guide to monitor options volume and get alerts when volume spikes.

## What This Does

Watches a specific option contract (like "NIFTY 24500 CE July 2026") and alerts you when the 5-minute volume breaks previous highs.

**Perfect for**: Catching volume breakouts in options while trading.

---

## Quick Start (Easiest Way)

### Step 1: Make Sure You're Logged Into Kite

Ask Claude:
```
"Login to Kite"
```

Click the authorization link Claude provides and approve access.

### Step 2: Start Monitoring

Just ask Claude in natural language:
```
"Monitor volume for NIFTY 24500 CE July 2026"
"Alert me when BANKNIFTY 52000 PE weekly volume increases"
"Track options volume for NIFTY 24000 CE monthly"
```

That's it! Claude will:
- Find the exact option contract
- Start checking volume every 5 minutes
- Alert you when volume breaks previous highs

---

## Understanding the Alerts

### What You'll See

When volume increases:
```
🚨 VOLUME ALERT 🚨
New 5-min volume high detected for NFO:NIFTY26JUL24500CE!
Current: 45,230 | Previous High: 38,750 | +16.7%
```

You'll also get:
- Desktop notification (pop-up on screen)
- Sound alert (3 beeps)

### What It Means

- **New high detected** = Current 5-min volume is higher than ALL previous 5-min volumes since you started monitoring
- **Percentage** = How much higher than the previous high
- **Indicates** = Increased interest in this strike

---

## Common Usage Examples

### Monitor NIFTY Call Option
```
"Monitor NIFTY 24500 CE July expiry"
```

### Monitor BANKNIFTY Put Option (Weekly)
```
"Monitor BANKNIFTY 52000 PE weekly expiry"
```

### Monitor Multiple Options
Ask for each separately:
```
"Monitor NIFTY 24500 CE July"
"Monitor NIFTY 24000 PE July"
```
Claude will run them independently.

---

## Option Input Formats

The skill understands these formats:

| What You Say | What It Understands |
|--------------|-------------------|
| `"NIFTY 24500 CE July 2026"` | Full specification |
| `"NIFTY 24500 CE July"` | Short month |
| `"BANKNIFTY 52000 PE weekly"` | Weekly expiry |
| `"NIFTY 24000 CE monthly"` | Monthly expiry |

**Must include**:
- ✅ Underlying (NIFTY, BANKNIFTY, FINNIFTY, etc.)
- ✅ Strike price (24500, 52000, etc.)
- ✅ Type (CE for Call, PE for Put)
- ✅ Expiry (July, weekly, monthly, etc.)

---

## Stopping Monitoring

To stop, tell Claude:
```
"Stop monitoring"
```

You'll see a summary:
```
--- Monitoring Summary ---
Total checks: 15
Highest volume: 52,340
Lowest volume: 12,450
Average volume: 28,765
```

---

## Running the Script Directly (Advanced)

If you want to run the Python script yourself:

### Step 1: Navigate to the skill folder
```bash
cd .claude/skills/kite-options-volume-alert
```

### Step 2: Run the script
```bash
python scripts/options_volume_monitor.py "NIFTY 24500 CE July 2026"
```

### Options
```bash
# Check every 2 minutes instead of 5
python scripts/options_volume_monitor.py "NIFTY 24500 CE July 2026" --interval 120

# Verbose mode (more detailed output)
python scripts/options_volume_monitor.py "NIFTY 24500 CE July 2026" --verbose

# Stop monitoring
Press Ctrl+C
```

**Note**: Running the script directly requires MCP integration setup. Easier to just ask Claude to monitor for you.

---

## Troubleshooting

### "Could not find instrument"

**Problem**: Option doesn't exist or wrong format

**Fix**:
- ✅ Check spelling: `NIFTY` not `Nifty`
- ✅ Verify expiry exists (check NSE website)
- ✅ Try `"weekly"` or `"monthly"` instead of specific month

### "Session expired" or "Not logged in"

**Problem**: Kite authorization expired

**Fix**:
```
Ask Claude: "Login to Kite"
```
Click the link and authorize again.

### "No alerts appearing"

**Possible reasons**:
- Volume is declining (no new highs to alert on)
- It's the first few checks (need baseline data)
- Option is illiquid (try ATM strikes)

**Fix**:
- Wait for more data points (10-15 minutes)
- Monitor more liquid strikes (closer to current price)
- Check if market is active (9:15 AM - 3:30 PM IST)

### "Rate limit exceeded"

**Problem**: Too many API calls

**Fix**:
- Use default 5-minute interval (don't go below 1 minute)
- Stop and restart monitoring after a few minutes

---

## Best Practices

### ✅ Do This

- **Monitor during market hours** (9:15 AM - 3:30 PM IST)
- **Start 30 mins after open** (avoid opening volatility)
- **Choose liquid strikes** (ATM or near-ATM options)
- **Keep terminal/chat visible** (don't miss alerts)
- **Use 5-minute intervals** (default is best)

### ❌ Avoid This

- **Don't monitor far OTM** (low liquidity = false alerts)
- **Don't use <1 min intervals** (rate limiting issues)
- **Don't monitor expiry day** (volume is atypical)
- **Don't trade on volume alone** (confirm with price, IV, levels)

---

## Trading Strategy Tips

### When Alert Triggers

1. **Check current price** - Is it moving?
2. **Look at chart** - Breaking key levels?
3. **Check IV** - Is volatility increasing?
4. **Confirm trend** - Multiple timeframes agree?
5. **Enter with plan** - Entry, stop loss, target defined

### Volume Alert Signals

**Strong Signal** (>30% increase):
- Significant institutional interest
- Worth immediate attention
- Consider position entry

**Moderate Signal** (10-30%):
- Building interest
- Monitor closely
- Wait for price confirmation

**Weak Signal** (<10%):
- Minor variation
- Possibly noise
- Continue monitoring

---

## Supported Underlyings

- ✅ NIFTY
- ✅ BANKNIFTY
- ✅ FINNIFTY
- ✅ MIDCPNIFTY
- ✅ SENSEX
- ✅ BANKEX

More can be added on request.

---

## What's Next?

### Learn More

- **SKILL.md** - Complete documentation with advanced features
- **README.md** - Technical details and examples
- **MCP_INTEGRATION.md** - How MCP connection works

### Common Questions

**Q: Can I monitor multiple options at once?**
A: Yes! Ask Claude to monitor each one separately. They'll run independently.

**Q: Does it work after market hours?**
A: No, only during market hours (9:15 AM - 3:30 PM IST).

**Q: Can I get Telegram alerts?**
A: Not yet, but can be added. Currently: console + desktop + sound.

**Q: How much does this cost?**
A: Free! Uses your Kite account (standard brokerage API access).

**Q: Will this execute trades?**
A: No, it's read-only. Only monitors and alerts. You decide on trades.

---

## Example Usage Session

```
You: "Login to Kite"
Claude: [provides authorization link]
You: [clicks and authorizes]

You: "Monitor NIFTY 24500 CE July 2026"
Claude: "Starting volume monitor for NIFTY 24500 CE July..."
        "Found: NFO:NIFTY26JUL24500CE"
        "Monitoring started! Checking every 5 minutes..."

[5 minutes later]
Claude: "Volume check #1: 12,450 (initial reading)"

[5 minutes later]
Claude: "Volume check #2: 15,230 (normal activity)"

[5 minutes later]
Claude: "🚨 VOLUME ALERT 🚨"
        "New high detected: 38,750 vs previous 15,230 (+154%)"
        "This is a significant volume spike!"

You: "What should I do?"
Claude: [provides analysis of the volume spike and trading considerations]

You: "Stop monitoring"
Claude: "Monitoring stopped. Summary: ..."
```

---

## Need Help?

Ask Claude:
- "How do I use the options volume monitor?"
- "Show me examples of monitoring options"
- "What does the volume alert mean?"
- "How do I stop monitoring?"

---

## Summary

**To start**: Just ask Claude "Monitor [option details]"
**To stop**: Tell Claude "Stop monitoring"
**During trading**: Watch for alerts and confirm with price action
**After trading**: Review monitoring summary

That's all you need to know! Start by asking Claude to monitor an option during market hours.
