#!/usr/bin/env python3
"""
Nifty 50 Volume & Lower Low Filter

Filters Nifty 50 stocks based on:
1. Current volume > 7-day average volume
2. Making a lower low (recent swing low < previous swing low)

Author: Claude Code
Date: 2026-07-18
"""

import yfinance as yf
import pandas as pd
import argparse
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Nifty50VolumeFilter:
    """Filter Nifty 50 stocks based on volume and lower low patterns."""

    def __init__(self, window: int = 5, min_volume_ratio: float = 1.0, verbose: bool = False):
        """
        Initialize the filter.

        Args:
            window: Window size for swing low detection (default: 5 bars)
            min_volume_ratio: Minimum volume ratio threshold (default: 1.0)
            verbose: Show detailed progress (default: False)
        """
        self.window = window
        self.min_volume_ratio = min_volume_ratio
        self.verbose = verbose
        self.constituents = self._load_constituents()

    def _load_constituents(self) -> List[Dict]:
        """Load Nifty 50 constituents from JSON file."""
        script_dir = Path(__file__).parent
        json_path = script_dir.parent / 'data' / 'nifty50_constituents.json'

        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
                return data['constituents']
        except FileNotFoundError:
            print(f"❌ Error: Constituents file not found at {json_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in constituents file: {e}")
            return []

    def fetch_stock_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        Fetch OHLCV data for a stock.

        Args:
            symbol: NSE stock symbol (without .NS suffix)

        Returns:
            DataFrame with OHLCV data or None if fetch fails
        """
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            # Fetch 30 days of data for swing low detection
            hist = ticker.history(period="1mo")

            if hist.empty or len(hist) < 10:
                if self.verbose:
                    print(f"⚠️  {symbol}: Insufficient data")
                return None

            return hist

        except Exception as e:
            if self.verbose:
                print(f"❌ {symbol}: Error fetching data - {str(e)}")
            return None

    def check_volume_filter(self, df: pd.DataFrame) -> Tuple[bool, float, float, float]:
        """
        Check if current volume > 7-day average.

        Args:
            df: DataFrame with volume data

        Returns:
            Tuple of (passes_filter, current_volume, avg_volume, ratio)
        """
        if len(df) < 8:
            return False, 0, 0, 0

        # Calculate 7-day average volume
        vol_7d_avg = df['Volume'].iloc[-7:].mean()
        current_vol = df['Volume'].iloc[-1]

        # Calculate ratio
        volume_ratio = current_vol / vol_7d_avg if vol_7d_avg > 0 else 0

        # Check if passes filter
        passes = volume_ratio >= self.min_volume_ratio

        return passes, current_vol, vol_7d_avg, volume_ratio

    def detect_swing_lows(self, df: pd.DataFrame) -> List[Tuple[datetime, float]]:
        """
        Identify swing lows in price data.

        A swing low is a local minimum where:
        - Low[i] is the minimum value in the window [i-window, i+window]

        Args:
            df: DataFrame with OHLC data

        Returns:
            List of (date, price) tuples for swing lows
        """
        swing_lows = []
        lows = df['Low'].values
        dates = df.index

        # Need at least window*2 + 1 bars to detect swing lows
        if len(lows) < (self.window * 2 + 1):
            return swing_lows

        # Iterate through possible swing low positions
        for i in range(self.window, len(lows) - self.window):
            # Check if this low is the minimum in its window
            window_values = lows[i - self.window:i + self.window + 1]
            if lows[i] == min(window_values):
                # Only add if it's actually a local minimum (not just equal to surrounding values)
                if lows[i] < min(lows[i-self.window:i]) or lows[i] < min(lows[i+1:i+self.window+1]):
                    swing_lows.append((dates[i], lows[i]))

        return swing_lows

    def check_lower_low_pattern(self, df: pd.DataFrame) -> Tuple[bool, Optional[float], Optional[float]]:
        """
        Check if recent swing low < previous swing low.

        Args:
            df: DataFrame with OHLC data

        Returns:
            Tuple of (passes_filter, recent_swing_low, previous_swing_low)
        """
        swing_lows = self.detect_swing_lows(df)

        if len(swing_lows) < 2:
            return False, None, None

        # Get two most recent swing lows
        recent_low = swing_lows[-1][1]
        previous_low = swing_lows[-2][1]

        # Check if making lower low
        passes = recent_low < previous_low

        return passes, recent_low, previous_low

    def analyze_stock(self, stock_info: Dict) -> Optional[Dict]:
        """
        Analyze a single stock for volume and lower low filters.

        Args:
            stock_info: Dict with symbol, name, sector

        Returns:
            Dict with analysis results or None if stock doesn't pass filters
        """
        symbol = stock_info['symbol']

        # Fetch data
        df = self.fetch_stock_data(symbol)
        if df is None:
            return None

        # Check volume filter
        vol_passes, current_vol, avg_vol, vol_ratio = self.check_volume_filter(df)

        if not vol_passes:
            if self.verbose:
                print(f"⊘  {symbol}: Volume filter failed ({vol_ratio:.2f}x)")
            return None

        # Check lower low pattern
        ll_passes, recent_low, previous_low = self.check_lower_low_pattern(df)

        if not ll_passes:
            if self.verbose:
                print(f"⊘  {symbol}: Lower low filter failed")
            return None

        # Stock passes both filters
        current_price = df['Close'].iloc[-1]

        result = {
            'symbol': symbol,
            'name': stock_info['name'],
            'sector': stock_info['sector'],
            'current_volume': int(current_vol),
            'avg_volume_7d': int(avg_vol),
            'volume_ratio': round(vol_ratio, 2),
            'recent_swing_low': round(recent_low, 2),
            'previous_swing_low': round(previous_low, 2),
            'current_price': round(current_price, 2),
            'low_diff': round(previous_low - recent_low, 2),
            'low_diff_pct': round(((previous_low - recent_low) / previous_low) * 100, 2)
        }

        print(f"✓  {symbol}: Passes both filters (Vol: {vol_ratio:.2f}x, Low: ₹{recent_low:.2f} < ₹{previous_low:.2f})")

        return result

    def scan_all_stocks(self, max_workers: int = 10) -> List[Dict]:
        """
        Scan all Nifty 50 stocks in parallel.

        Args:
            max_workers: Number of parallel threads

        Returns:
            List of stocks that pass both filters
        """
        results = []
        total = len(self.constituents)

        print(f"\n🔍 Scanning {total} Nifty 50 stocks...")
        print(f"📊 Filters: Volume > {self.min_volume_ratio}x 7-day avg, Recent swing low < Previous swing low")
        print(f"🔧 Swing low window: {self.window} bars\n")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_stock = {
                executor.submit(self.analyze_stock, stock): stock
                for stock in self.constituents
            }

            completed = 0
            for future in as_completed(future_to_stock):
                completed += 1
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    stock = future_to_stock[future]
                    print(f"❌ {stock['symbol']}: Unexpected error - {str(e)}")

                if not self.verbose and completed % 10 == 0:
                    print(f"Progress: {completed}/{total} stocks scanned...")

        # Sort by volume ratio (descending)
        results.sort(key=lambda x: x['volume_ratio'], reverse=True)

        return results

    def format_large_number(self, num: int) -> str:
        """Format large numbers with M/K suffix."""
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)

    def generate_report(self, results: List[Dict]) -> str:
        """
        Generate markdown report of filtered stocks.

        Args:
            results: List of filtered stock results

        Returns:
            Markdown formatted report
        """
        report = []
        report.append("# Nifty 50 Volume & Lower Low Filter Results")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M IST')}\n")

        report.append("## Summary")
        report.append(f"- Total stocks scanned: {len(self.constituents)}")
        report.append(f"- Stocks meeting criteria: {len(results)}")
        report.append(f"- Filter 1: Volume > {self.min_volume_ratio}x 7-day average")
        report.append(f"- Filter 2: Recent swing low < Previous swing low ({self.window}-bar window)\n")

        if not results:
            report.append("## No stocks match the filters")
            report.append("This could indicate:")
            report.append("- Market is in uptrend (few lower lows)")
            report.append("- Low volume day across the board")
            report.append("- Try adjusting --min-volume-ratio or --window parameters\n")
            return "\n".join(report)

        report.append("## Filtered Stocks\n")

        # Table header
        report.append("| Symbol | Company | Current Vol | 7D Avg Vol | Ratio | Recent Low | Previous Low | Diff | Current Price |")
        report.append("|--------|---------|-------------|------------|-------|------------|--------------|------|---------------|")

        # Table rows
        for stock in results:
            report.append(
                f"| {stock['symbol']:<10} | "
                f"{stock['name'][:30]:<30} | "
                f"{self.format_large_number(stock['current_volume']):>10} | "
                f"{self.format_large_number(stock['avg_volume_7d']):>10} | "
                f"{stock['volume_ratio']:>5.2f} | "
                f"₹{stock['recent_swing_low']:>7.2f} | "
                f"₹{stock['previous_swing_low']:>7.2f} | "
                f"-{stock['low_diff_pct']:>4.1f}% | "
                f"₹{stock['current_price']:>7.2f} |"
            )

        report.append("\n## Interpretation")
        report.append("- **Volume Ratio > 2.0**: Strong volume surge, heightened interest")
        report.append("- **Lower Low Pattern**: Bearish technical signal, downtrend formation")
        report.append("- **Larger Diff %**: More significant breakdown from previous support")
        report.append("- **Context Matters**: Always check broader market trend and sector performance\n")

        return "\n".join(report)

    def export_to_csv(self, results: List[Dict], output_path: str):
        """
        Export filtered stocks to CSV.

        Args:
            results: List of filtered stock results
            output_path: Path to output CSV file
        """
        if not results:
            print("⚠️  No results to export")
            return

        df = pd.DataFrame(results)

        # Reorder columns for better readability
        column_order = [
            'symbol', 'name', 'sector',
            'current_volume', 'avg_volume_7d', 'volume_ratio',
            'recent_swing_low', 'previous_swing_low', 'low_diff', 'low_diff_pct',
            'current_price'
        ]
        df = df[column_order]

        df.to_csv(output_path, index=False)
        print(f"\n📁 Results exported to: {output_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Filter Nifty 50 stocks based on volume and lower low patterns',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (default settings)
  python nifty50_volume_filter.py

  # Custom output file
  python nifty50_volume_filter.py --output my_results.csv

  # Adjust swing low window size
  python nifty50_volume_filter.py --window 7

  # Only show stocks with volume > 1.5x average
  python nifty50_volume_filter.py --min-volume-ratio 1.5

  # Verbose mode (show all progress)
  python nifty50_volume_filter.py --verbose
        """
    )

    parser.add_argument(
        '--output',
        type=str,
        default='nifty50_filtered.csv',
        help='Output CSV file path (default: nifty50_filtered.csv)'
    )

    parser.add_argument(
        '--window',
        type=int,
        default=5,
        help='Window size for swing low detection in bars (default: 5)'
    )

    parser.add_argument(
        '--min-volume-ratio',
        type=float,
        default=1.0,
        help='Minimum volume ratio threshold (default: 1.0)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed progress for each stock'
    )

    args = parser.parse_args()

    # Create filter instance
    filter_tool = Nifty50VolumeFilter(
        window=args.window,
        min_volume_ratio=args.min_volume_ratio,
        verbose=args.verbose
    )

    # Scan all stocks
    results = filter_tool.scan_all_stocks(max_workers=10)

    # Generate and print report
    report = filter_tool.generate_report(results)
    print("\n" + "="*80)
    print(report)
    print("="*80 + "\n")

    # Export to CSV
    filter_tool.export_to_csv(results, args.output)

    print(f"\n✅ Scan complete! Found {len(results)} stocks matching criteria.")


if __name__ == '__main__':
    main()
