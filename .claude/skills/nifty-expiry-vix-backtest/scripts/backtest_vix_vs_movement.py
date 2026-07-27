#!/usr/bin/env python3
"""
NIFTY Expiry Day VIX vs Movement Backtester

Analyzes the relationship between VIX (India VIX) and actual NIFTY movement
on expiry days over the last 2 years.

Tests hypothesis: Does VIX accurately predict expiry day volatility?

Author: Claude Code
Date: 2026-07-25
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json


class NiftyExpiryBacktester:
    """Backtest VIX predictions vs actual NIFTY movement on expiry days."""

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

    def get_expiry_dates(self, start_date: datetime, end_date: datetime) -> List[datetime]:
        """
        Get all NIFTY monthly expiry dates in the range.
        NIFTY expiries are on the last Thursday of each month.

        Args:
            start_date: Start date for analysis
            end_date: End date for analysis

        Returns:
            List of expiry dates
        """
        expiry_dates = []
        current_date = start_date

        while current_date <= end_date:
            # Get last day of current month
            if current_date.month == 12:
                next_month = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                next_month = current_date.replace(month=current_date.month + 1, day=1)

            last_day = next_month - timedelta(days=1)

            # Find last Thursday of the month (Thursday = weekday 3)
            # Start from last day and go backwards to find Thursday
            last_thursday = last_day
            while last_thursday.weekday() != 3:  # 3 = Thursday
                last_thursday = last_thursday - timedelta(days=1)

            # Only include if within our date range
            if start_date.date() <= last_thursday.date() <= end_date.date():
                expiry_dates.append(last_thursday)

            current_date = next_month

        return expiry_dates

    def fetch_nifty_data(self) -> pd.DataFrame:
        """
        Fetch NIFTY 50 historical data.

        Returns:
            DataFrame with NIFTY OHLCV data
        """
        print("Fetching NIFTY 50 data...")
        nifty = yf.Ticker("^NSEI")
        df = nifty.history(start=self.start_date, end=self.end_date)

        if df.empty:
            raise ValueError("Could not fetch NIFTY data")

        print(f"✓ Fetched {len(df)} days of NIFTY data")
        return df

    def fetch_vix_data(self) -> pd.DataFrame:
        """
        Fetch India VIX historical data.

        Returns:
            DataFrame with VIX data
        """
        print("Fetching India VIX data...")
        vix = yf.Ticker("^INDIAVIX")
        df = vix.history(start=self.start_date, end=self.end_date)

        if df.empty:
            raise ValueError("Could not fetch VIX data")

        print(f"✓ Fetched {len(df)} days of VIX data")
        return df

    def calculate_daily_movement(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily movement metrics.

        Args:
            df: OHLC DataFrame

        Returns:
            DataFrame with movement metrics
        """
        df['Daily_Range'] = df['High'] - df['Low']
        df['Daily_Range_Pct'] = (df['Daily_Range'] / df['Open']) * 100
        df['Open_Close_Move'] = abs(df['Close'] - df['Open'])
        df['Open_Close_Move_Pct'] = (df['Open_Close_Move'] / df['Open']) * 100
        df['Intraday_High_Pct'] = ((df['High'] - df['Open']) / df['Open']) * 100
        df['Intraday_Low_Pct'] = ((df['Open'] - df['Low']) / df['Open']) * 100
        df['Close_Change_Pct'] = df['Close'].pct_change() * 100

        return df

    def analyze_expiry_day(self, nifty_df: pd.DataFrame, vix_df: pd.DataFrame,
                           expiry_date: datetime) -> Dict:
        """
        Analyze a specific expiry day.
        If expiry day is a holiday, checks up to 3 days before for trading data.

        Args:
            nifty_df: NIFTY data
            vix_df: VIX data
            expiry_date: Expiry date to analyze

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
                    print(f"  ℹ️  Expiry {expiry_date.date()} was holiday, using {check_date} (T-{days_back})")
                break

        if nifty_expiry is None or vix_expiry is None or nifty_expiry.empty or vix_expiry.empty:
            print(f"  ⚠️  No data found for expiry {expiry_date.date()} (checked up to 3 days back)")
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
        # Daily expected move = VIX / sqrt(365) ≈ VIX / 19.1
        vix_predicted_move_pct = vix_open / 19.1

        # Actual movements
        actual_range_pct = nifty_data['Daily_Range_Pct']
        actual_open_close_pct = nifty_data['Open_Close_Move_Pct']

        result = {
            'date': expiry_date_only.strftime('%Y-%m-%d'),
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
            'vix_accuracy': 'Underestimated' if actual_range_pct > vix_predicted_move_pct else 'Overestimated'
        }

        return result

    def run_backtest(self) -> Dict:
        """
        Run complete backtest analysis.

        Returns:
            Dict with backtest results and statistics
        """
        print(f"\n{'='*80}")
        print("NIFTY Expiry Day VIX vs Movement Backtester")
        print(f"Period: {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        print(f"{'='*80}\n")

        # Fetch data
        nifty_df = self.fetch_nifty_data()
        vix_df = self.fetch_vix_data()

        # Calculate movements
        nifty_df = self.calculate_daily_movement(nifty_df)

        # Get expiry dates
        expiry_dates = self.get_expiry_dates(self.start_date, self.end_date)
        print(f"\n✓ Identified {len(expiry_dates)} expiry dates\n")

        # Analyze each expiry
        results = []
        for expiry_date in expiry_dates:
            analysis = self.analyze_expiry_day(nifty_df, vix_df, expiry_date)
            if analysis:
                results.append(analysis)
                print(f"✓ Analyzed {analysis['date']}: "
                      f"VIX {analysis['vix_open']} → Predicted {analysis['vix_predicted_move_pct']:.2f}% | "
                      f"Actual {analysis['actual_range_pct']:.2f}% ({analysis['vix_accuracy']})")

        if not results:
            print("❌ No data available for analysis")
            return None

        # Calculate statistics
        df_results = pd.DataFrame(results)

        statistics = {
            'total_expiry_days': len(results),
            'avg_vix': round(df_results['vix_open'].mean(), 2),
            'avg_vix_predicted_move': round(df_results['vix_predicted_move_pct'].mean(), 2),
            'avg_actual_range': round(df_results['actual_range_pct'].mean(), 2),
            'avg_actual_open_close': round(df_results['actual_open_close_pct'].mean(), 2),
            'avg_ratio': round(df_results['range_vs_vix_ratio'].mean(), 2),
            'median_ratio': round(df_results['range_vs_vix_ratio'].median(), 2),
            'times_underestimated': len(df_results[df_results['vix_accuracy'] == 'Underestimated']),
            'times_overestimated': len(df_results[df_results['vix_accuracy'] == 'Overestimated']),
            'max_vix_day': df_results.loc[df_results['vix_open'].idxmax()].to_dict(),
            'max_movement_day': df_results.loc[df_results['actual_range_pct'].idxmax()].to_dict(),
            'correlation': round(df_results['vix_open'].corr(df_results['actual_range_pct']), 3)
        }

        return {
            'expiry_data': results,
            'statistics': statistics,
            'raw_dataframe': df_results
        }

    def generate_report(self, backtest_results: Dict) -> str:
        """
        Generate readable report from backtest results.

        Args:
            backtest_results: Results from run_backtest()

        Returns:
            Formatted report string
        """
        if not backtest_results:
            return "No results to report"

        stats = backtest_results['statistics']
        df = backtest_results['raw_dataframe']

        report = []
        report.append("\n" + "="*80)
        report.append("BACKTEST RESULTS: VIX vs NIFTY Expiry Day Movement")
        report.append("="*80)

        report.append("\n📊 SUMMARY STATISTICS")
        report.append("-" * 80)
        report.append(f"Total Expiry Days Analyzed: {stats['total_expiry_days']}")
        report.append(f"Average VIX Level: {stats['avg_vix']}")
        report.append(f"Average VIX Predicted Move: {stats['avg_vix_predicted_move']:.2f}%")
        report.append(f"Average Actual Range: {stats['avg_actual_range']:.2f}%")
        report.append(f"Average Actual Open-Close: {stats['avg_actual_open_close']:.2f}%")

        report.append(f"\n🎯 VIX ACCURACY")
        report.append("-" * 80)
        report.append(f"Average Actual/Predicted Ratio: {stats['avg_ratio']:.2f}x")
        report.append(f"Median Ratio: {stats['median_ratio']:.2f}x")
        report.append(f"VIX Underestimated Movement: {stats['times_underestimated']} times "
                     f"({stats['times_underestimated']/stats['total_expiry_days']*100:.1f}%)")
        report.append(f"VIX Overestimated Movement: {stats['times_overestimated']} times "
                     f"({stats['times_overestimated']/stats['total_expiry_days']*100:.1f}%)")
        report.append(f"Correlation (VIX vs Movement): {stats['correlation']}")

        report.append(f"\n🔥 EXTREME DAYS")
        report.append("-" * 80)
        max_vix = stats['max_vix_day']
        report.append(f"Highest VIX Day: {max_vix['date']}")
        report.append(f"  VIX: {max_vix['vix_open']} | Predicted: {max_vix['vix_predicted_move_pct']:.2f}% | "
                     f"Actual: {max_vix['actual_range_pct']:.2f}%")

        max_move = stats['max_movement_day']
        report.append(f"\nHighest Movement Day: {max_move['date']}")
        report.append(f"  VIX: {max_move['vix_open']} | Predicted: {max_move['vix_predicted_move_pct']:.2f}% | "
                     f"Actual: {max_move['actual_range_pct']:.2f}%")

        report.append(f"\n📈 INTERPRETATION")
        report.append("-" * 80)

        if stats['avg_ratio'] > 1.2:
            report.append("⚠️  VIX consistently UNDERESTIMATES expiry day movement")
            report.append("    → Expiry days are MORE volatile than VIX suggests")
        elif stats['avg_ratio'] < 0.8:
            report.append("⚠️  VIX consistently OVERESTIMATES expiry day movement")
            report.append("    → Expiry days are LESS volatile than VIX suggests")
        else:
            report.append("✓  VIX is fairly accurate at predicting expiry day movement")

        if stats['correlation'] > 0.6:
            report.append(f"✓  Strong positive correlation ({stats['correlation']}) - VIX is a good predictor")
        elif stats['correlation'] > 0.3:
            report.append(f"~  Moderate correlation ({stats['correlation']}) - VIX has some predictive value")
        else:
            report.append(f"✗  Weak correlation ({stats['correlation']}) - VIX is not a reliable predictor")

        report.append(f"\n📋 DETAILED EXPIRY DAY DATA")
        report.append("-" * 80)
        report.append(f"{'Date':<12} {'VIX':<6} {'Predicted':<10} {'Actual':<10} {'Ratio':<8} {'Accuracy':<15}")
        report.append("-" * 80)

        for _, row in df.iterrows():
            report.append(f"{row['date']:<12} {row['vix_open']:<6.2f} "
                         f"{row['vix_predicted_move_pct']:<10.2f} {row['actual_range_pct']:<10.2f} "
                         f"{row['range_vs_vix_ratio']:<8.2f} {row['vix_accuracy']:<15}")

        report.append("="*80 + "\n")

        return "\n".join(report)

    def export_results(self, backtest_results: Dict, filename: str = "vix_backtest_results.json"):
        """
        Export results to JSON file.

        Args:
            backtest_results: Results from run_backtest()
            filename: Output filename
        """
        if not backtest_results:
            print("No results to export")
            return

        # Prepare for JSON serialization
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

    def export_csv(self, backtest_results: Dict, filename: str = "vix_backtest_results.csv"):
        """
        Export results to CSV file.

        Args:
            backtest_results: Results from run_backtest()
            filename: Output filename
        """
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
        description='Backtest VIX predictions vs actual NIFTY movement on expiry days',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default: 2 years backtest
  python backtest_vix_vs_movement.py

  # Custom period (3 years)
  python backtest_vix_vs_movement.py --years 3

  # Export results to custom files
  python backtest_vix_vs_movement.py --json my_results.json --csv my_results.csv
        """
    )

    parser.add_argument(
        '--years',
        type=int,
        default=2,
        help='Number of years to backtest (default: 2)'
    )

    parser.add_argument(
        '--json',
        type=str,
        default='vix_backtest_results.json',
        help='JSON output filename (default: vix_backtest_results.json)'
    )

    parser.add_argument(
        '--csv',
        type=str,
        default='vix_backtest_results.csv',
        help='CSV output filename (default: vix_backtest_results.csv)'
    )

    args = parser.parse_args()

    # Create backtester
    backtester = NiftyExpiryBacktester(years=args.years)

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
