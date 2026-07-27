#!/usr/bin/env python3
"""
SENSEX Expiry Day VIX vs Movement Backtester (Weekly + Monthly)

Analyzes the relationship between India VIX and actual SENSEX movement on expiry days.

BSE EXPIRY DAY TRANSITIONS:
- Before January 1, 2025: Friday (weekday=4)
- January 1, 2025 - September 3, 2025: Tuesday (weekday=1)
- From September 4, 2025 onwards: Thursday (weekday=3)

Features:
- Visual mini-charts showing intraday OHLC patterns
- Threshold-based classification (0.5% threshold like V5)
- Holiday handling (T-1, T-2, T-3 lookback)
- Weekly AND Monthly expiries

Author: Claude Code
Date: 2026-07-25
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json


class SensexAllExpiriesBacktester:
    """Backtest VIX predictions vs actual SENSEX movement on weekly + monthly expiries."""

    def __init__(self, years: int = 2):
        """
        Initialize backtester.

        Args:
            years: Number of years to backtest (default: 2)
        """
        self.years = years
        # Go back full years plus a buffer to ensure we get all expiries
        self.start_date = datetime.now() - timedelta(days=365 * years + 30)
        self.end_date = datetime.now()

        # India VIX (same as used for NIFTY)
        self.vix_ticker = '^INDIAVIX'
        # SENSEX ticker
        self.sensex_ticker = '^BSESN'

        # VIX to daily move conversion factor (India VIX uses same as NIFTY)
        # VIX / sqrt(252) ≈ VIX / 15.87, but we use 19.1 as calibrated for India VIX
        self.vix_conversion_factor = 19.1

    def get_all_expiries(self, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, str]]:
        """
        Get all expiry dates (weekly + monthly) for the date range.

        BSE Expiry Day Schedule:
        - Before Jan 1, 2025: Friday (weekday=4)
        - Jan 1, 2025 - Sep 3, 2025: Tuesday (weekday=1)
        - From Sep 4, 2025 onwards: Thursday (weekday=3)

        Args:
            start_date: Start date
            end_date: End date

        Returns:
            List of (expiry_date, expiry_type) tuples
        """
        # Transition dates for BSE
        transition_1 = datetime(2025, 1, 1).date()  # Friday → Tuesday
        transition_2 = datetime(2025, 9, 4).date()  # Tuesday → Thursday

        expiries = []
        current_date = start_date

        # Track last monthly expiry to avoid duplicates
        last_monthly_month = None

        while current_date <= end_date:
            # Determine which weekday to use based on current date
            current_date_only = current_date.date()

            if current_date_only < transition_1:
                target_weekday = 4  # Friday (before Jan 1, 2025)
            elif current_date_only < transition_2:
                target_weekday = 1  # Tuesday (Jan 1, 2025 - Sep 3, 2025)
            else:
                target_weekday = 3  # Thursday (from Sep 4, 2025 onwards)

            # Check if this is the target weekday
            if current_date.weekday() == target_weekday:
                # Determine if this is a monthly expiry (last target weekday of the month)
                next_week = current_date + timedelta(days=7)

                # Check if next week is in a different month
                is_monthly = next_week.month != current_date.month

                if is_monthly:
                    # Avoid duplicate monthly expiries
                    if last_monthly_month != current_date.month:
                        expiries.append((current_date, 'monthly'))
                        last_monthly_month = current_date.month
                else:
                    # Weekly expiry
                    expiries.append((current_date, 'weekly'))

            current_date += timedelta(days=1)

        return expiries

    def fetch_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fetch SENSEX and India VIX historical data.

        Returns:
            Tuple of (sensex_df, vix_df)
        """
        print(f"\nFetching SENSEX data...")
        sensex = yf.Ticker(self.sensex_ticker)
        sensex_hist = sensex.history(start=self.start_date, end=self.end_date)

        if sensex_hist.empty:
            raise ValueError(f"No SENSEX data found for ticker {self.sensex_ticker}")

        print(f"✓ Fetched {len(sensex_hist)} days of SENSEX data")

        print(f"Fetching India VIX data...")
        vix = yf.Ticker(self.vix_ticker)
        vix_hist = vix.history(start=self.start_date, end=self.end_date)

        if vix_hist.empty:
            raise ValueError(f"No VIX data found for ticker {self.vix_ticker}")

        print(f"✓ Fetched {len(vix_hist)} days of VIX data")

        return sensex_hist, vix_hist

    @staticmethod
    def generate_chart(open_price: float, high: float, low: float, close: float) -> str:
        """
        Generate a visual mini-chart using Unicode characters.

        Format: O→L→H→C with direction indicators and result emoji

        Args:
            open_price: Opening price
            high: High price
            low: Low price
            close: Closing price

        Returns:
            Unicode chart string
        """
        # Unicode block characters (8 levels)
        blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

        price_range = high - low
        if price_range == 0:
            # No movement
            return "━━━━━━━ ━"

        # Normalize prices to 0-7 scale
        def normalize(price):
            normalized = ((price - low) / price_range) * 7
            return int(round(normalized))

        open_idx = normalize(open_price)
        high_idx = normalize(high)
        low_idx = normalize(low)
        close_idx = normalize(close)

        # Create visual representation O→L→H→C
        chart_parts = []

        # Open
        chart_parts.append(f"{blocks[open_idx]}")

        # Direction from open to low
        if low < open_price:
            chart_parts.append("↓")
        elif low > open_price:
            chart_parts.append("↑")
        else:
            chart_parts.append("→")

        # Low
        chart_parts.append(f"{blocks[low_idx]}")

        # Direction from low to high
        chart_parts.append("↑")

        # High
        chart_parts.append(f"{blocks[high_idx]}")

        # Direction from high to close
        if close < high:
            chart_parts.append("↓")
        elif close > high:
            chart_parts.append("↑")
        else:
            chart_parts.append("→")

        # Close
        chart_parts.append(f"{blocks[close_idx]}")

        # Add result emoji
        if close > open_price:
            chart_parts.append(" 📈")  # Bullish
        elif close < open_price:
            chart_parts.append(" 📉")  # Bearish
        else:
            chart_parts.append(" ━")  # Flat

        return "".join(chart_parts)

    def analyze_expiry_day(self, expiry_date: datetime, expiry_type: str,
                          sensex_data: pd.DataFrame, vix_data: pd.DataFrame) -> Dict:
        """
        Analyze a single expiry day.

        Args:
            expiry_date: Expiry date
            expiry_type: 'weekly' or 'monthly'
            sensex_data: SENSEX historical data
            vix_data: VIX historical data

        Returns:
            Dictionary with analysis results
        """
        expiry_date_only = expiry_date.date()

        # Try to find data for expiry date, check T-1, T-2, T-3 if holiday
        sensex_day = None
        vix_day = None
        actual_trading_date = None

        for days_back in range(4):  # Check expiry day, then 1, 2, 3 days before
            check_date = (expiry_date - timedelta(days=days_back)).date()

            # Check if data exists for this date
            sensex_check = sensex_data[sensex_data.index.date == check_date]
            vix_check = vix_data[vix_data.index.date == check_date]

            if not sensex_check.empty and not vix_check.empty:
                sensex_day = sensex_check.iloc[0]
                vix_day = vix_check.iloc[0]
                actual_trading_date = check_date

                if days_back > 0:
                    print(f"  ℹ️  {expiry_type.capitalize()} expiry {expiry_date_only} was holiday, using {check_date} (T-{days_back})")

                break

        if sensex_day is None or vix_day is None:
            print(f"  ⚠️  No data found for {expiry_type} expiry {expiry_date_only} (checked T-0 to T-3)")
            return None

        # Get VIX close (from previous day or same day)
        vix_close = vix_day['Close']

        # Convert VIX to predicted daily move (%)
        vix_predicted_move_pct = vix_close / self.vix_conversion_factor

        # Calculate actual SENSEX movement
        sensex_open = sensex_day['Open']
        sensex_high = sensex_day['High']
        sensex_low = sensex_day['Low']
        sensex_close = sensex_day['Close']

        # Calculate actual range (high - low)
        actual_range = sensex_high - sensex_low
        actual_range_pct = (actual_range / sensex_open) * 100

        # Calculate open to close move
        open_close_move = sensex_close - sensex_open
        actual_open_close_pct = (open_close_move / sensex_open) * 100

        # Calculate intraday high and low percentages
        intraday_high_pct = ((sensex_high - sensex_open) / sensex_open) * 100
        intraday_low_pct = ((sensex_low - sensex_open) / sensex_open) * 100

        # Ratio: actual/predicted
        range_vs_vix_ratio = actual_range_pct / vix_predicted_move_pct if vix_predicted_move_pct > 0 else 0

        # Get day of week
        day_of_week = expiry_date_only.strftime('%A')  # Full name (Monday, Tuesday, etc.)

        # Threshold-based classification (0.5% like V5)
        # This creates a threshold for EXTREME underestimation
        # 0.5% = ~250 points at SENSEX 50,000 levels
        diff = actual_range_pct - vix_predicted_move_pct
        vix_accuracy = 'Underestimated' if diff > 0.5 else 'Overestimated'

        # Generate visual chart
        chart = self.generate_chart(
            sensex_open,
            sensex_high,
            sensex_low,
            sensex_close
        )

        # Determine result
        result_icon = "📆" if expiry_type == 'weekly' else "📅"

        # Print result
        print(f"{result_icon} {expiry_type.capitalize():7} {expiry_date_only} ({day_of_week[:3]}): "
              f"VIX {vix_close:.2f} → Predicted {vix_predicted_move_pct:.2f}% | "
              f"Actual {actual_range_pct:.2f}% ({vix_accuracy})")

        return {
            'date': expiry_date_only,
            'day_of_week': day_of_week,
            'expiry_type': expiry_type,
            'chart': chart,
            'sensex_open': round(sensex_open, 2),
            'sensex_high': round(sensex_high, 2),
            'sensex_low': round(sensex_low, 2),
            'sensex_close': round(sensex_close, 2),
            'vix_open': round(vix_day['Open'], 2),
            'vix_close': round(vix_close, 2),
            'vix_predicted_move_pct': round(vix_predicted_move_pct, 2),
            'actual_range_pct': round(actual_range_pct, 2),
            'actual_open_close_pct': round(actual_open_close_pct, 2),
            'intraday_high_pct': round(intraday_high_pct, 2),
            'intraday_low_pct': round(intraday_low_pct, 2),
            'range_vs_vix_ratio': round(range_vs_vix_ratio, 2),
            'diff_pct': round(diff, 2),
            'vix_accuracy': vix_accuracy
        }

    def run_backtest(self) -> Dict:
        """
        Run the complete backtest.

        Returns:
            Dictionary with all results
        """
        print("=" * 80)
        print("SENSEX Expiry Day VIX vs Movement Backtester (Weekly + Monthly)")
        print(f"Period: {self.start_date.date()} to {self.end_date.date()}")
        print("=" * 80)

        # Fetch data
        sensex_data, vix_data = self.fetch_data()

        # Get all expiry dates
        expiries = self.get_all_expiries(self.start_date, self.end_date)
        weekly_count = sum(1 for _, t in expiries if t == 'weekly')
        monthly_count = sum(1 for _, t in expiries if t == 'monthly')

        print(f"\n✓ Identified {len(expiries)} expiry dates:")
        print(f"  - Weekly expiries: {weekly_count}")
        print(f"  - Monthly expiries: {monthly_count}")
        print()

        # Analyze each expiry
        results = []
        for expiry_date, expiry_type in expiries:
            result = self.analyze_expiry_day(expiry_date, expiry_type, sensex_data, vix_data)
            if result:
                results.append(result)

        # Calculate statistics
        df = pd.DataFrame(results)

        # Overall stats
        total_days = len(df)
        avg_vix = df['vix_close'].mean()
        avg_predicted = df['vix_predicted_move_pct'].mean()
        avg_actual = df['actual_range_pct'].mean()
        avg_ratio = df['range_vs_vix_ratio'].mean()
        correlation = df['vix_predicted_move_pct'].corr(df['actual_range_pct'])

        # Weekly stats
        weekly_df = df[df['expiry_type'] == 'weekly']
        weekly_avg_vix = weekly_df['vix_close'].mean()
        weekly_avg_predicted = weekly_df['vix_predicted_move_pct'].mean()
        weekly_avg_actual = weekly_df['actual_range_pct'].mean()
        weekly_avg_ratio = weekly_df['range_vs_vix_ratio'].mean()
        weekly_underestimated = (weekly_df['vix_accuracy'] == 'Underestimated').sum()
        weekly_correlation = weekly_df['vix_predicted_move_pct'].corr(weekly_df['actual_range_pct'])

        # Monthly stats
        monthly_df = df[df['expiry_type'] == 'monthly']
        monthly_avg_vix = monthly_df['vix_close'].mean()
        monthly_avg_predicted = monthly_df['vix_predicted_move_pct'].mean()
        monthly_avg_actual = monthly_df['actual_range_pct'].mean()
        monthly_avg_ratio = monthly_df['range_vs_vix_ratio'].mean()
        monthly_underestimated = (monthly_df['vix_accuracy'] == 'Underestimated').sum()
        monthly_correlation = monthly_df['vix_predicted_move_pct'].corr(monthly_df['actual_range_pct'])

        # Print summary
        print("\n" + "=" * 80)
        print("BACKTEST RESULTS: VIX vs SENSEX Expiry Day Movement")
        print("Weekly + Monthly Expiries Combined")
        print("=" * 80)

        print("\n📊 OVERALL STATISTICS (All Expiries)")
        print("-" * 80)
        print(f"Total Expiry Days: {total_days}")
        print(f"Average VIX: {avg_vix:.2f}")
        print(f"Average VIX Predicted Move: {avg_predicted:.2f}%")
        print(f"Average Actual Range: {avg_actual:.2f}%")
        print(f"Average Ratio: {avg_ratio:.2f}x")
        print(f"Correlation: {correlation:.3f}")

        print("\n📆 WEEKLY EXPIRIES")
        print("-" * 80)
        print(f"Total: {len(weekly_df)} days")
        print(f"Average VIX: {weekly_avg_vix:.2f}")
        print(f"Average Predicted: {weekly_avg_predicted:.2f}% | Actual: {weekly_avg_actual:.2f}%")
        print(f"Average Ratio: {weekly_avg_ratio:.2f}x")
        print(f"VIX Underestimated: {weekly_underestimated} ({(weekly_underestimated/len(weekly_df)*100):.1f}%)")
        print(f"Correlation: {weekly_correlation:.3f}")

        print("\n📅 MONTHLY EXPIRIES")
        print("-" * 80)
        print(f"Total: {len(monthly_df)} days")
        print(f"Average VIX: {monthly_avg_vix:.2f}")
        print(f"Average Predicted: {monthly_avg_predicted:.2f}% | Actual: {monthly_avg_actual:.2f}%")
        print(f"Average Ratio: {monthly_avg_ratio:.2f}x")
        print(f"VIX Underestimated: {monthly_underestimated} ({(monthly_underestimated/len(monthly_df)*100):.1f}%)")
        print(f"Correlation: {monthly_correlation:.3f}")

        print("\n⚖️  WEEKLY vs MONTHLY COMPARISON")
        print("-" * 80)
        print(f"Weekly Avg Ratio: {weekly_avg_ratio:.2f}x")
        print(f"Monthly Avg Ratio: {monthly_avg_ratio:.2f}x")
        diff = monthly_avg_ratio - weekly_avg_ratio
        if abs(diff) < 0.05:
            print(f"→ Monthly and weekly expiries have SIMILAR volatility (difference: {diff:.2f}x)")
        elif diff > 0:
            print(f"→ Monthly expiries have MORE volatility (difference: {diff:.2f}x)")
        else:
            print(f"→ Weekly expiries have MORE volatility (difference: {abs(diff):.2f}x)")

        print("\n" + "=" * 80)
        print("\n")

        return {
            'results': results,
            'summary': {
                'total_days': total_days,
                'weekly_count': len(weekly_df),
                'monthly_count': len(monthly_df),
                'avg_vix': round(avg_vix, 2),
                'avg_predicted': round(avg_predicted, 2),
                'avg_actual': round(avg_actual, 2),
                'avg_ratio': round(avg_ratio, 2),
                'correlation': round(correlation, 3),
                'weekly_underestimated': int(weekly_underestimated),
                'monthly_underestimated': int(monthly_underestimated)
            }
        }

    def export_results(self, backtest_results: Dict, filename: str = "vix_sensex_expiries_results.json"):
        """Export results to JSON."""
        with open(filename, 'w') as f:
            # Convert date objects to strings for JSON serialization
            json_results = {
                'results': [
                    {**r, 'date': r['date'].strftime('%Y-%m-%d')}
                    for r in backtest_results['results']
                ],
                'summary': backtest_results['summary']
            }
            json.dump(json_results, f, indent=2)

        print(f"✓ Results exported to {filename}")

    def export_csv(self, backtest_results: Dict, filename: str = "vix_sensex_expiries_results.csv"):
        """Export results to CSV."""
        df = pd.DataFrame(backtest_results['results'])
        # Convert date to string
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df.to_csv(filename, index=False)
        print(f"✓ CSV exported to {filename}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Backtest India VIX vs SENSEX expiry day movement')
    parser.add_argument('--years', type=int, default=2, help='Number of years to backtest (default: 2)')
    parser.add_argument('--json', type=str, default='vix_sensex_expiries_results.json', help='JSON output filename')
    parser.add_argument('--csv', type=str, default='vix_sensex_expiries_results.csv', help='CSV output filename')

    args = parser.parse_args()

    # Run backtest
    backtester = SensexAllExpiriesBacktester(years=args.years)
    results = backtester.run_backtest()

    # Export results
    backtester.export_results(results, args.json)
    backtester.export_csv(results, args.csv)

    print("✅ Backtest complete!")


if __name__ == "__main__":
    main()
