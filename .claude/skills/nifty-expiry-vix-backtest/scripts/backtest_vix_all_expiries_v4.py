#!/usr/bin/env python3
"""
NIFTY Expiry Day VIX vs Movement Backtester V4 (Weekly + Monthly)

V4 CHANGES (based on V3):
- Modified threshold to 0.4% (more conservative than V2/V3's 0.2%)
- Only marks as "Underestimated" if actual > predicted by more than 0.4%
- Otherwise marks as "Overestimated" (includes accurate predictions within 0.4%)
- Identifies only SIGNIFICANT VIX failures (>0.4% miss)

V3 CHANGES:
- Adds visual mini-chart column showing intraday OHLC pattern
- Uses Unicode block characters (▁▂▃▄▅▆▇█) for at-a-glance visualization
- Chart format: O→L→H→C with direction indicators

V2 CHANGES:
- Modified underestimation logic with 0.2% threshold
- Adds 'diff_pct' column showing actual difference

Analyzes the relationship between VIX and actual NIFTY movement on BOTH:
- Weekly expiries (Thursday before Sept 1, 2025; Tuesday after)
- Monthly expiries (last expiry day of month)

Author: Claude Code
Date: 2026-07-25
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json


class NiftyAllExpiriesBacktester:
    """Backtest VIX predictions vs actual NIFTY movement on weekly + monthly expiries."""

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

    @staticmethod
    def generate_chart(open_price: float, high: float, low: float, close: float) -> str:
        """
        Generate a visual mini-chart using Unicode block characters.
        Shows OHLC pattern with direction indicators.

        Args:
            open_price: Opening price
            high: High price
            low: Low price
            close: Close price

        Returns:
            Unicode chart string showing intraday movement
        """
        # Unicode block characters (8 levels)
        blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

        # Normalize prices to 0-7 range
        price_range = high - low
        if price_range == 0:
            # Flat day - all same
            return "━━━━"

        def normalize(price):
            """Convert price to 0-7 index"""
            normalized = ((price - low) / price_range) * 7
            return int(round(normalized))

        open_idx = normalize(open_price)
        high_idx = normalize(high)
        low_idx = normalize(low)
        close_idx = normalize(close)

        # Create visual representation
        # Format: O→L→H→C with direction
        chart_parts = []

        # Opening
        chart_parts.append(f"{blocks[open_idx]}")

        # Arrow showing initial direction
        if low_idx < open_idx:
            chart_parts.append("↓")
        elif high_idx > open_idx:
            chart_parts.append("↑")
        else:
            chart_parts.append("→")

        # Low point
        chart_parts.append(f"{blocks[low_idx]}")

        # Up to high
        chart_parts.append("↑")
        chart_parts.append(f"{blocks[high_idx]}")

        # Down to close
        if close_idx < high_idx:
            chart_parts.append("↓")
        else:
            chart_parts.append("→")
        chart_parts.append(f"{blocks[close_idx]}")

        # Add net direction indicator
        if close > open_price:
            chart_parts.append(" 📈")  # Bullish
        elif close < open_price:
            chart_parts.append(" 📉")  # Bearish
        else:
            chart_parts.append(" ━")  # Flat

        return "".join(chart_parts)

    def get_all_expiries(self, start_date: datetime, end_date: datetime) -> List[Tuple[datetime, str]]:
        """
        Get all NIFTY expiry dates in the range.
        IMPORTANT: NIFTY expiries changed from Thursday to Tuesday on Sept 1, 2025.

        Before Sept 1, 2025: Thursday expiries
        From Sept 1, 2025 onwards: Tuesday expiries

        Tags each as 'weekly' or 'monthly' (last expiry day of month).

        Args:
            start_date: Start date for analysis
            end_date: End date for analysis

        Returns:
            List of (expiry_date, expiry_type) tuples
        """
        expiries = []
        current_date = start_date

        # Expiry day changed from Thursday to Tuesday on Sept 1, 2025
        transition_date = datetime(2025, 9, 1).date()

        while current_date <= end_date:
            # Determine which day to use based on date
            if current_date.date() < transition_date:
                target_weekday = 3  # Thursday (before Sept 1, 2025)
            else:
                target_weekday = 1  # Tuesday (from Sept 1, 2025 onwards)

            if current_date.weekday() == target_weekday:
                # Check if this is last expiry day of the month
                # Look ahead up to 7 days - if we find another expiry day in same month, this isn't last
                is_monthly = True
                for day_offset in range(1, 8):
                    future_date = current_date + timedelta(days=day_offset)

                    # Determine target weekday for future date too
                    if future_date.date() < transition_date:
                        future_target_weekday = 3  # Thursday
                    else:
                        future_target_weekday = 1  # Tuesday

                    if future_date.month == current_date.month and future_date.weekday() == future_target_weekday:
                        is_monthly = False
                        break

                expiry_type = 'monthly' if is_monthly else 'weekly'
                expiries.append((current_date, expiry_type))

            current_date += timedelta(days=1)

        return expiries

    def fetch_nifty_data(self) -> pd.DataFrame:
        """Fetch NIFTY 50 historical data."""
        print("Fetching NIFTY 50 data...")
        nifty = yf.Ticker("^NSEI")
        df = nifty.history(start=self.start_date, end=self.end_date)

        if df.empty:
            raise ValueError("Could not fetch NIFTY data")

        print(f"✓ Fetched {len(df)} days of NIFTY data")
        return df

    def fetch_vix_data(self) -> pd.DataFrame:
        """Fetch India VIX historical data."""
        print("Fetching India VIX data...")
        vix = yf.Ticker("^INDIAVIX")
        df = vix.history(start=self.start_date, end=self.end_date)

        if df.empty:
            raise ValueError("Could not fetch VIX data")

        print(f"✓ Fetched {len(df)} days of VIX data")
        return df

    def calculate_daily_movement(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate daily movement metrics."""
        df['Daily_Range'] = df['High'] - df['Low']
        df['Daily_Range_Pct'] = (df['Daily_Range'] / df['Open']) * 100
        df['Open_Close_Move'] = abs(df['Close'] - df['Open'])
        df['Open_Close_Move_Pct'] = (df['Open_Close_Move'] / df['Open']) * 100
        df['Intraday_High_Pct'] = ((df['High'] - df['Open']) / df['Open']) * 100
        df['Intraday_Low_Pct'] = ((df['Open'] - df['Low']) / df['Open']) * 100
        df['Close_Change_Pct'] = df['Close'].pct_change() * 100

        return df

    def analyze_expiry_day(self, nifty_df: pd.DataFrame, vix_df: pd.DataFrame,
                           expiry_date: datetime, expiry_type: str) -> Dict:
        """
        Analyze a specific expiry day.
        If expiry day is a holiday, checks up to 3 days before for trading data.

        Args:
            nifty_df: NIFTY data
            vix_df: VIX data
            expiry_date: Expiry date to analyze
            expiry_type: 'weekly' or 'monthly'

        Returns:
            Dict with analysis results
        """
        # Try to find trading day data, checking up to 3 days back for holidays
        nifty_expiry = None
        vix_expiry = None
        actual_trading_date = None

        for days_back in range(4):  # Check expiry day, then 1, 2, 3 days before
            check_date = (expiry_date - timedelta(days=days_back)).date()

            nifty_check = nifty_df[nifty_df.index.date == check_date]
            vix_check = vix_df[vix_df.index.date == check_date]

            if not nifty_check.empty and not vix_check.empty:
                nifty_expiry = nifty_check
                vix_expiry = vix_check
                actual_trading_date = check_date
                if days_back > 0:
                    print(f"  ℹ️  {expiry_type.capitalize()} expiry {expiry_date.date()} was holiday, using {check_date} (T-{days_back})")
                break

        if nifty_expiry is None or vix_expiry is None or nifty_expiry.empty or vix_expiry.empty:
            return None

        expiry_date_only = actual_trading_date

        # Get VIX from previous day (opening VIX expectation)
        vix_dates = vix_df.index.date
        prev_day_idx = np.where(vix_dates < expiry_date_only)[0]

        if len(prev_day_idx) == 0:
            vix_open = vix_expiry['Open'].iloc[0]
        else:
            vix_open = vix_df.iloc[prev_day_idx[-1]]['Close']

        nifty_data = nifty_expiry.iloc[0]
        vix_close = vix_expiry['Close'].iloc[0]

        # VIX predicts annualized volatility, convert to daily
        vix_predicted_move_pct = vix_open / 19.1

        # Actual movements
        actual_range_pct = nifty_data['Daily_Range_Pct']
        actual_open_close_pct = nifty_data['Open_Close_Move_Pct']

        # Get day of week
        day_of_week = expiry_date_only.strftime('%A')  # Full name (Monday, Tuesday, etc.)

        # V4 Logic: Only mark as Underestimated if difference > 0.4%
        # This creates a threshold for SIGNIFICANT underestimation (more conservative than V2/V3)
        # 0.4% = ~100 points at NIFTY 25000 levels
        diff = actual_range_pct - vix_predicted_move_pct
        vix_accuracy = 'Underestimated' if diff > 0.4 else 'Overestimated'

        # V3: Generate visual chart
        chart = self.generate_chart(
            nifty_data['Open'],
            nifty_data['High'],
            nifty_data['Low'],
            nifty_data['Close']
        )

        result = {
            'date': expiry_date_only.strftime('%Y-%m-%d'),
            'day_of_week': day_of_week,
            'expiry_type': expiry_type,
            'chart': chart,  # V3: Visual mini-chart
            'nifty_open': round(nifty_data['Open'], 2),
            'nifty_high': round(nifty_data['High'], 2),
            'nifty_low': round(nifty_data['Low'], 2),
            'nifty_close': round(nifty_data['Close'], 2),
            'vix_open': round(vix_open, 2),
            'vix_close': round(vix_close, 2),
            'vix_predicted_move_pct': round(vix_predicted_move_pct, 2),
            'actual_range_pct': round(actual_range_pct, 2),
            'actual_open_close_pct': round(actual_open_close_pct, 2),
            'intraday_high_pct': round(nifty_data['Intraday_High_Pct'], 2),
            'intraday_low_pct': round(nifty_data['Intraday_Low_Pct'], 2),
            'range_vs_vix_ratio': round(actual_range_pct / vix_predicted_move_pct, 2),
            'diff_pct': round(diff, 2),
            'vix_accuracy': vix_accuracy
        }

        return result

    def run_backtest(self) -> Dict:
        """Run complete backtest analysis for weekly + monthly expiries."""
        print(f"\n{'='*80}")
        print("NIFTY Expiry Day VIX vs Movement Backtester (Weekly + Monthly)")
        print(f"Period: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        print(f"{'='*80}\n")

        # Fetch data
        nifty_df = self.fetch_nifty_data()
        vix_df = self.fetch_vix_data()

        # Calculate movements
        nifty_df = self.calculate_daily_movement(nifty_df)

        # Get all expiry dates (Thursday before Sept 1, 2025; Tuesday after)
        expiries = self.get_all_expiries(self.start_date, self.end_date)
        weekly_count = sum(1 for _, t in expiries if t == 'weekly')
        monthly_count = sum(1 for _, t in expiries if t == 'monthly')

        print(f"\n✓ Identified {len(expiries)} expiry dates:")
        print(f"  - Weekly expiries: {weekly_count}")
        print(f"  - Monthly expiries: {monthly_count}\n")

        # Analyze each expiry
        results = []
        for expiry_date, expiry_type in expiries:
            analysis = self.analyze_expiry_day(nifty_df, vix_df, expiry_date, expiry_type)
            if analysis:
                results.append(analysis)
                indicator = "📅" if expiry_type == 'monthly' else "📆"
                print(f"{indicator} {expiry_type.capitalize():7} {analysis['date']} ({analysis['day_of_week'][:3]}): "
                      f"VIX {analysis['vix_open']} → Predicted {analysis['vix_predicted_move_pct']:.2f}% | "
                      f"Actual {analysis['actual_range_pct']:.2f}% ({analysis['vix_accuracy']})")

        if not results:
            print("❌ No data available for analysis")
            return None

        # Calculate overall statistics
        df_results = pd.DataFrame(results)

        # Separate weekly and monthly
        df_weekly = df_results[df_results['expiry_type'] == 'weekly']
        df_monthly = df_results[df_results['expiry_type'] == 'monthly']

        # Calculate statistics for each type
        stats = {
            'overall': self._calc_stats(df_results, 'Overall'),
            'weekly': self._calc_stats(df_weekly, 'Weekly') if not df_weekly.empty else None,
            'monthly': self._calc_stats(df_monthly, 'Monthly') if not df_monthly.empty else None
        }

        return {
            'expiry_data': results,
            'statistics': stats,
            'raw_dataframe': df_results
        }

    def _calc_stats(self, df: pd.DataFrame, label: str) -> Dict:
        """Calculate statistics for a subset of data."""
        if df.empty:
            return None

        return {
            'label': label,
            'total_expiry_days': len(df),
            'avg_vix': round(df['vix_open'].mean(), 2),
            'avg_vix_predicted_move': round(df['vix_predicted_move_pct'].mean(), 2),
            'avg_actual_range': round(df['actual_range_pct'].mean(), 2),
            'avg_actual_open_close': round(df['actual_open_close_pct'].mean(), 2),
            'avg_ratio': round(df['range_vs_vix_ratio'].mean(), 2),
            'median_ratio': round(df['range_vs_vix_ratio'].median(), 2),
            'times_underestimated': len(df[df['vix_accuracy'] == 'Underestimated']),
            'times_overestimated': len(df[df['vix_accuracy'] == 'Overestimated']),
            'correlation': round(df['vix_open'].corr(df['actual_range_pct']), 3)
        }

    def generate_report(self, backtest_results: Dict) -> str:
        """Generate readable report from backtest results."""
        if not backtest_results:
            return "No results to report"

        stats = backtest_results['statistics']
        df = backtest_results['raw_dataframe']

        report = []
        report.append("\n" + "="*80)
        report.append("BACKTEST RESULTS: VIX vs NIFTY Expiry Day Movement")
        report.append("Weekly + Monthly Expiries Combined")
        report.append("="*80)

        # Overall stats
        overall = stats['overall']
        report.append("\n📊 OVERALL STATISTICS (All Expiries)")
        report.append("-" * 80)
        report.append(f"Total Expiry Days: {overall['total_expiry_days']}")
        report.append(f"Average VIX: {overall['avg_vix']}")
        report.append(f"Average VIX Predicted Move: {overall['avg_vix_predicted_move']:.2f}%")
        report.append(f"Average Actual Range: {overall['avg_actual_range']:.2f}%")
        report.append(f"Average Ratio: {overall['avg_ratio']:.2f}x")
        report.append(f"Correlation: {overall['correlation']}")

        # Weekly stats
        if stats['weekly']:
            weekly = stats['weekly']
            report.append("\n📆 WEEKLY EXPIRIES")
            report.append("-" * 80)
            report.append(f"Total: {weekly['total_expiry_days']} days")
            report.append(f"Average VIX: {weekly['avg_vix']}")
            report.append(f"Average Predicted: {weekly['avg_vix_predicted_move']:.2f}% | Actual: {weekly['avg_actual_range']:.2f}%")
            report.append(f"Average Ratio: {weekly['avg_ratio']:.2f}x")
            report.append(f"VIX Underestimated: {weekly['times_underestimated']} ({weekly['times_underestimated']/weekly['total_expiry_days']*100:.1f}%)")
            report.append(f"Correlation: {weekly['correlation']}")

        # Monthly stats
        if stats['monthly']:
            monthly = stats['monthly']
            report.append("\n📅 MONTHLY EXPIRIES")
            report.append("-" * 80)
            report.append(f"Total: {monthly['total_expiry_days']} days")
            report.append(f"Average VIX: {monthly['avg_vix']}")
            report.append(f"Average Predicted: {monthly['avg_vix_predicted_move']:.2f}% | Actual: {monthly['avg_actual_range']:.2f}%")
            report.append(f"Average Ratio: {monthly['avg_ratio']:.2f}x")
            report.append(f"VIX Underestimated: {monthly['times_underestimated']} ({monthly['times_underestimated']/monthly['total_expiry_days']*100:.1f}%)")
            report.append(f"Correlation: {monthly['correlation']}")

        # Comparison
        if stats['weekly'] and stats['monthly']:
            report.append("\n⚖️  WEEKLY vs MONTHLY COMPARISON")
            report.append("-" * 80)
            report.append(f"Weekly Avg Ratio: {stats['weekly']['avg_ratio']:.2f}x")
            report.append(f"Monthly Avg Ratio: {stats['monthly']['avg_ratio']:.2f}x")
            ratio_diff = stats['monthly']['avg_ratio'] - stats['weekly']['avg_ratio']
            if abs(ratio_diff) > 0.1:
                higher = "Monthly" if ratio_diff > 0 else "Weekly"
                report.append(f"→ {higher} expiries have MORE volatility (difference: {abs(ratio_diff):.2f}x)")
            else:
                report.append(f"→ Weekly and Monthly expiries have similar volatility")

        report.append("\n" + "="*80 + "\n")
        return "\n".join(report)

    def export_results(self, backtest_results: Dict, filename: str = "vix_all_expiries_results_v4.json"):
        """Export results to JSON file."""
        if not backtest_results:
            print("No results to export")
            return

        export_data = {
            'metadata': {
                'backtest_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'period_start': self.start_date.strftime('%Y-%m-%d'),
                'period_end': self.end_date.strftime('%Y-%m-%d')
            },
            'expiry_data': backtest_results['expiry_data'],
            'statistics': backtest_results['statistics']
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"\n✓ Results exported to {filename}")

    def export_csv(self, backtest_results: Dict, filename: str = "vix_all_expiries_results_v4.csv"):
        """Export results to CSV file."""
        if not backtest_results:
            print("No results to export")
            return

        df = backtest_results['raw_dataframe']
        df.to_csv(filename, index=False)

        print(f"✓ CSV exported to {filename}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Backtest VIX predictions vs NIFTY movement on weekly + monthly expiries',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--years', type=int, default=2, help='Number of years to backtest')
    parser.add_argument('--json', type=str, default='vix_all_expiries_results_v4.json', help='JSON output filename')
    parser.add_argument('--csv', type=str, default='vix_all_expiries_results_v4.csv', help='CSV output filename')

    args = parser.parse_args()

    # Create backtester
    backtester = NiftyAllExpiriesBacktester(years=args.years)

    # Run backtest
    results = backtester.run_backtest()

    if results:
        # Generate and print report
        report = backtester.generate_report(results)
        print(report)

        # Export results
        backtester.export_results(results, args.json)
        backtester.export_csv(results, args.csv)

        print("\n✅ Backtest complete!")
    else:
        print("\n❌ Backtest failed - no data available")


if __name__ == '__main__':
    main()
