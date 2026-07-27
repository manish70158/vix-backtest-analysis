# MCP Integration Guide

The options volume monitor script needs to communicate with the Kite MCP server. There are two approaches:

## Approach 1: Claude-Assisted (Recommended)

When the user asks Claude to monitor options, Claude acts as the integration layer:

1. **User**: "Monitor volume for NIFTY 24500 CE July 2026"

2. **Claude parses the request** and calls MCP tools directly:
   ```python
   # Claude calls these tools internally:
   - mcp__kite__search_instruments (to find the option)
   - mcp__kite__get_historical_data (to fetch volume)
   ```

3. **Claude runs a monitoring loop**:
   - Fetches volume every 5 minutes
   - Compares with previous readings
   - Alerts user when new high detected

4. **Alerts displayed** in the chat conversation

**Advantages**:
- No setup required
- Works immediately
- Claude handles MCP protocol
- Alerts visible in chat

**Disadvantages**:
- Requires Claude to stay active
- Can't run in background independently

## Approach 2: Standalone Script (Advanced)

The `options_volume_monitor.py` script can run independently, but requires MCP server access.

### Current Limitation

The script's `_call_kite_mcp()` method uses a placeholder that calls `claude` CLI:
```python
def _call_kite_mcp(self, tool_name: str, params: Dict) -> any:
    # Placeholder implementation
    subprocess.run(['claude', '-p', prompt], ...)
```

This works if:
- Claude CLI is installed
- Kite MCP server is configured
- User is authenticated

### Making It Work Standalone

To run the script independently, you need to:

1. **Install MCP SDK** (if available for Python)
2. **Configure Kite MCP connection**
3. **Update `_call_kite_mcp()` method** to use direct MCP calls

Example with direct HTTP calls (if Kite MCP exposes HTTP):
```python
import requests

def _call_kite_mcp(self, tool_name: str, params: Dict) -> any:
    url = f"http://localhost:MCP_PORT/kite/{tool_name}"
    response = requests.post(url, json=params)
    return response.json()
```

Or using MCP SDK (when available):
```python
from mcp import Client

def _call_kite_mcp(self, tool_name: str, params: Dict) -> any:
    client = Client("kite")
    return client.call_tool(f"kite__{tool_name}", params)
```

### Workaround: Claude as Proxy

Until direct MCP integration is built, you can use Claude as a proxy:

1. Create a helper script `kite_mcp_proxy.py`:
```python
#!/usr/bin/env python3
"""
Simple proxy that uses Claude to call Kite MCP tools.
"""
import sys
import json
import subprocess

def call_mcp_tool(tool_name, params):
    """Call MCP tool via Claude CLI."""
    prompt = f"""
    Call the mcp__kite__{tool_name} tool with these parameters:
    {json.dumps(params)}

    Return ONLY the raw JSON result, nothing else.
    """

    result = subprocess.run(
        ['claude', '-p', prompt],
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)

if __name__ == '__main__':
    tool_name = sys.argv[1]
    params = json.loads(sys.argv[2])
    result = call_mcp_tool(tool_name, params)
    print(json.dumps(result))
```

2. Update `options_volume_monitor.py` to use the proxy:
```python
def _call_kite_mcp(self, tool_name: str, params: Dict) -> any:
    result = subprocess.run(
        ['python', 'kite_mcp_proxy.py', tool_name, json.dumps(params)],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
```

## Recommended Usage

**For most users**: Use Approach 1 (Claude-Assisted)
- Just ask Claude to monitor options
- No setup needed
- Works immediately

**For advanced users**: Set up Approach 2 (Standalone)
- Create MCP proxy or direct integration
- Run script independently
- Background monitoring capability

## Testing MCP Connection

Test if Kite MCP is accessible:

```bash
# Via Claude Code (easiest)
Ask Claude: "Search for NIFTY options using Kite"

# Via Claude CLI (if installed)
claude -p "Use mcp__kite__search_instruments to search for NFO:NIFTY"
```

If these work, the MCP server is configured correctly.

## Future Improvements

Planned enhancements:
1. Native MCP SDK integration
2. WebSocket streaming for real-time updates
3. Multi-option monitoring in single process
4. Persistent volume history across restarts
5. Advanced alert conditions (volume + price + IV)

## Support

If you encounter MCP integration issues:
1. Verify Kite MCP server is configured in Claude Code
2. Ensure you're logged in to Kite (`mcp__kite__login`)
3. Check MCP server logs for errors
4. Try calling tools directly through Claude first

For now, the recommended approach is to ask Claude to monitor options rather than running the script standalone.
