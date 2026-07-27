#!/usr/bin/env python3
"""
Kite Options Volume Monitor

Monitors real-time volume for a specified option contract and alerts when
a new 5-minute volume high is detected.

Usage:
    python options_volume_monitor.py "NIFTY 24500 CE July 2026"
    python options_volume_monitor.py "BANKNIFTY 52000 PE weekly"

Author: Claude Code
Date: 2026-07-18
"""

import sys
import json
import time
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import subprocess
import os


class OptionsVolumeMonitor:
    """Monitor option volume and alert on new highs."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.volume_history: List[int] = []
        self.monitoring = False

    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            "INFO": "\033[36m",      # Cyan
            "SUCCESS": "\033[32m",    # Green
            "WARNING": "\033[33m",    # Yellow
            "ERROR": "\033[31m",      # Red
            "ALERT": "\033[35m"       # Magenta
        }
        reset = "\033[0m"
        color = colors.get(level, "")
        print(f"{color}[{timestamp}] {level}: {message}{reset}")

    def parse_option_input(self, user_input: str) -> Dict[str, str]:
        """
        Parse natural language option input.

        Examples:
            "NIFTY 24500 CE July 2026" → {underlying: NIFTY, strike: 24500, type: CE, expiry: July 2026}
            "BANKNIFTY 52000 PE weekly" → {underlying: BANKNIFTY, strike: 52000, type: PE, expiry: weekly}

        Args:
            user_input: Natural language description of option

        Returns:
            Dict with underlying, strike, option_type, expiry
        """
        user_input = user_input.upper().strip()

        # Extract underlying (NIFTY, BANKNIFTY, etc.)
        underlying_pattern = r'(NIFTY|BANKNIFTY|FINNIFTY|MIDCPNIFTY|SENSEX|BANKEX)'
        underlying_match = re.search(underlying_pattern, user_input)

        if not underlying_match:
            raise ValueError("Could not identify underlying. Use NIFTY, BANKNIFTY, FINNIFTY, etc.")

        underlying = underlying_match.group(1)

        # Extract strike price (digits)
        strike_pattern = r'(\d+)'
        strike_match = re.search(strike_pattern, user_input)

        if not strike_match:
            raise ValueError("Could not identify strike price")

        strike = strike_match.group(1)

        # Extract option type (CE or PE)
        if 'CE' in user_input:
            option_type = 'CE'
        elif 'PE' in user_input:
            option_type = 'PE'
        else:
            raise ValueError("Could not identify option type. Use CE (Call) or PE (Put)")

        # Extract expiry information
        expiry = ""
        if 'WEEKLY' in user_input or 'WEEK' in user_input:
            expiry = "weekly"
        elif 'MONTHLY' in user_input or 'MONTH' in user_input:
            expiry = "monthly"
        else:
            # Try to extract month/year
            month_pattern = r'(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)'
            month_match = re.search(month_pattern, user_input)

            year_pattern = r'(20\d{2}|\d{2})'
            year_match = re.search(year_pattern, user_input)

            if month_match:
                expiry = month_match.group(1)
                if year_match:
                    expiry += year_match.group(1)

        return {
            'underlying': underlying,
            'strike': strike,
            'option_type': option_type,
            'expiry': expiry
        }

    def search_instrument(self, parsed_option: Dict[str, str]) -> Optional[Dict]:
        """
        Search for instrument using Kite MCP server.

        Args:
            parsed_option: Dict from parse_option_input

        Returns:
            Instrument details with token, tradingsymbol, etc.
        """
        self.log(f"Searching for {parsed_option['underlying']} {parsed_option['strike']} {parsed_option['option_type']} {parsed_option['expiry']}...")

        # Build search query
        # For options, search by underlying first
        underlying = parsed_option['underlying']

        # Convert NSE underlying to NFO for options
        if underlying == 'NIFTY':
            search_query = 'NFO:NIFTY'
        elif underlying == 'BANKNIFTY':
            search_query = 'NFO:BANKNIFTY'
        else:
            search_query = f'NFO:{underlying}'

        try:
            # Use claude CLI to call Kite MCP
            result = self._call_kite_mcp('search_instruments', {
                'query': search_query,
                'filter_on': 'underlying'
            })

            if not result:
                self.log("No instruments found", "ERROR")
                return None

            # Filter results by strike, type, and expiry
            strike = parsed_option['strike']
            option_type = parsed_option['option_type']
            expiry_hint = parsed_option['expiry'].upper()

            matching = []
            for instrument in result:
                tradingsymbol = instrument.get('tradingsymbol', '')
                name = instrument.get('name', '')

                # Check if it matches our criteria
                if (strike in tradingsymbol and
                    option_type in tradingsymbol):

                    # If expiry specified, try to match
                    if expiry_hint and expiry_hint in tradingsymbol:
                        matching.append(instrument)
                    elif not expiry_hint:
                        matching.append(instrument)

            if not matching:
                self.log(f"No exact match found for {strike} {option_type}", "ERROR")
                return None

            # If multiple matches, take the nearest expiry (first one typically)
            selected = matching[0]

            self.log(f"✓ Found: {selected['tradingsymbol']} (Token: {selected['instrument_token']})", "SUCCESS")

            return selected

        except Exception as e:
            self.log(f"Error searching instrument: {str(e)}", "ERROR")
            return None

    def _call_kite_mcp(self, tool_name: str, params: Dict) -> any:
        """
        Call Kite MCP server tool via Claude CLI.

        Args:
            tool_name: MCP tool name (without mcp__kite__ prefix)
            params: Parameters for the tool

        Returns:
            Tool result
        """
        # This is a placeholder - in actual implementation, this would use
        # the MCP protocol to call Kite tools
        # For now, we'll use subprocess to call claude with the MCP tool

        mcp_tool = f"mcp__kite__{tool_name}"

        # Build the prompt for Claude CLI
        prompt = f"Use the {mcp_tool} tool with parameters: {json.dumps(params)}. Return only the raw JSON result, no explanation."

        try:
            # Note: This is a simplified version. In practice, you'd need proper MCP integration
            result = subprocess.run(
                ['claude', '-p', prompt],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # Parse JSON from output
                output = result.stdout.strip()
                return json.loads(output)
            else:
                self.log(f"MCP call failed: {result.stderr}", "ERROR")
                return None

        except Exception as e:
            self.log(f"Error calling MCP: {str(e)}", "ERROR")
            return None

    def get_5min_volume(self, instrument_token: int) -> Optional[int]:
        """
        Get current 5-minute volume for an instrument.

        Args:
            instrument_token: Kite instrument token

        Returns:
            Volume for the current 5-minute candle
        """
        try:
            # Get last 2 five-minute candles
            now = datetime.now()
            to_date = now.strftime("%Y-%m-%d %H:%M:%S")
            from_date = (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

            result = self._call_kite_mcp('get_historical_data', {
                'instrument_token': instrument_token,
                'from_date': from_date,
                'to_date': to_date,
                'interval': '5minute'
            })

            if result and len(result) > 0:
                # Get the most recent complete candle volume
                latest_candle = result[-1]
                volume = latest_candle.get('volume', 0)
                return int(volume)
            else:
                return None

        except Exception as e:
            self.log(f"Error fetching volume: {str(e)}", "ERROR")
            return None

    def send_alert(self, message: str, volume: int):
        """
        Send alert via multiple channels.

        Args:
            message: Alert message
            volume: Volume that triggered the alert
        """
        # Console alert with prominent formatting
        self.log("=" * 80, "ALERT")
        self.log(f"🚨 VOLUME ALERT 🚨", "ALERT")
        self.log(message, "ALERT")
        self.log(f"Volume: {volume:,}", "ALERT")
        self.log(f"Previous High: {max(self.volume_history[:-1]):,}" if len(self.volume_history) > 1 else "First reading", "ALERT")
        self.log("=" * 80, "ALERT")

        # Desktop notification (macOS)
        try:
            subprocess.run([
                'osascript', '-e',
                f'display notification "{message}" with title "Options Volume Alert" sound name "Glass"'
            ], timeout=5)
        except Exception as e:
            if self.verbose:
                self.log(f"Desktop notification failed: {str(e)}", "WARNING")

        # Sound alert (system beep)
        try:
            for _ in range(3):
                print('\a')  # System beep
                time.sleep(0.3)
        except Exception:
            pass

    def monitor(self, option_input: str, interval_seconds: int = 300):
        """
        Start monitoring an option for volume highs.

        Args:
            option_input: Natural language option description
            interval_seconds: Check interval (default 300 = 5 minutes)
        """
        self.log(f"Kite Options Volume Monitor Starting...")
        self.log(f"Monitoring interval: {interval_seconds}s ({interval_seconds//60} minutes)")

        # Parse option input
        try:
            parsed = self.parse_option_input(option_input)
            self.log(f"Parsed: {parsed['underlying']} Strike {parsed['strike']} {parsed['option_type']} Expiry {parsed['expiry']}")
        except ValueError as e:
            self.log(f"Failed to parse option: {str(e)}", "ERROR")
            return

        # Search for instrument
        instrument = self.search_instrument(parsed)
        if not instrument:
            self.log("Could not find instrument. Exiting.", "ERROR")
            return

        instrument_token = instrument['instrument_token']
        tradingsymbol = instrument['tradingsymbol']
        exchange = instrument.get('exchange', 'NFO')

        self.log(f"Monitoring: {exchange}:{tradingsymbol}")
        self.log(f"Press Ctrl+C to stop monitoring\n")

        self.monitoring = True
        check_count = 0

        try:
            while self.monitoring:
                check_count += 1

                # Get current 5-minute volume
                volume = self.get_5min_volume(instrument_token)

                if volume is not None:
                    self.volume_history.append(volume)

                    # Check if this is a new high
                    if len(self.volume_history) > 1:
                        previous_high = max(self.volume_history[:-1])

                        if volume > previous_high:
                            # NEW HIGH! Alert!
                            increase_pct = ((volume - previous_high) / previous_high) * 100
                            self.send_alert(
                                f"New 5-min volume high detected for {tradingsymbol}!\n"
                                f"Current: {volume:,} | Previous High: {previous_high:,} | +{increase_pct:.1f}%",
                                volume
                            )
                        else:
                            # Normal update
                            self.log(f"[Check #{check_count}] Volume: {volume:,} | High: {previous_high:,}")
                    else:
                        # First reading
                        self.log(f"[Check #{check_count}] Initial volume: {volume:,}")
                else:
                    self.log(f"[Check #{check_count}] Could not fetch volume", "WARNING")

                # Wait for next interval
                if self.monitoring:
                    self.log(f"Next check in {interval_seconds}s...")
                    time.sleep(interval_seconds)

        except KeyboardInterrupt:
            self.log("\nMonitoring stopped by user", "WARNING")
            self.monitoring = False
        except Exception as e:
            self.log(f"Error during monitoring: {str(e)}", "ERROR")
            self.monitoring = False

        # Summary
        if self.volume_history:
            self.log("\n--- Monitoring Summary ---")
            self.log(f"Total checks: {check_count}")
            self.log(f"Highest volume: {max(self.volume_history):,}")
            self.log(f"Lowest volume: {min(self.volume_history):,}")
            self.log(f"Average volume: {sum(self.volume_history)//len(self.volume_history):,}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Monitor options volume and alert on new 5-minute highs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor NIFTY call option
  python options_volume_monitor.py "NIFTY 24500 CE July 2026"

  # Monitor BANKNIFTY put option (weekly expiry)
  python options_volume_monitor.py "BANKNIFTY 52000 PE weekly"

  # Custom check interval (2 minutes instead of 5)
  python options_volume_monitor.py "NIFTY 24500 CE July 2026" --interval 120

  # Verbose mode
  python options_volume_monitor.py "NIFTY 24500 CE July 2026" --verbose
        """
    )

    parser.add_argument(
        'option',
        type=str,
        help='Option to monitor in natural language (e.g., "NIFTY 24500 CE July 2026")'
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=300,
        help='Check interval in seconds (default: 300 = 5 minutes)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Validate interval
    if args.interval < 60:
        print("Warning: Interval less than 60 seconds may hit rate limits")

    # Create monitor and start
    monitor = OptionsVolumeMonitor(verbose=args.verbose)
    monitor.monitor(args.option, args.interval)


if __name__ == '__main__':
    main()
