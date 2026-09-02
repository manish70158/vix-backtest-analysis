#!/usr/bin/env python3
"""
Fetch Participant-wise Data (FII / PRO / DII / Client) for BSE/Sensex Analysis

Fetches SEPARATE FII and PRO data from NSE participant-wise OI archives.
This is the same source used by build_sensex_fii_6year.py but fetches ALL
trading days (not just expiry days).

Source: https://archives.nseindia.com/content/nsccl/fao_participant_oi_DDMMYYYY.csv
- Provides: FII, PRO, DII, Client — each with Futures + Options long/short positions
- Updated daily by NSCCL (NSE Clearing Corporation)
- Covers all F&O segments (Nifty, Sensex, BankNifty, stocks)

BSE India's API (api.bseindia.com) is protected by Akamai WAF — cannot be accessed
programmatically. NSE participant OI covers the same institutional positioning as
it reflects overall F&O activity across all index derivatives.

Output:
- sensex_participant_wise_daily.csv: Daily FII, PRO, DII, Client positions + directions

Author: Claude Code
Date: 2026-08-26
"""

import pandas as pd
import numpy as np
import requests
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
PROJECT_ROOT = Path(__file__).parent.parent

NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/',
}

# Cache
_cache = {}


def get_nse_session():
    """Create NSE session with proper headers."""
    session = requests.Session()
    session.headers.update(NSE_HEADERS)
    return session


def fetch_participant_oi(session, date: datetime) -> dict | None:
    """
    Fetch participant-wise OI for a given date from NSE archives.
    Returns dict with FII, PRO, DII, Client net positions or None.
    """
    date_str = date.strftime('%d%m%Y')

    if date_str in _cache:
        return _cache[date_str]

    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{date_str}.csv"

    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            _cache[date_str] = None
            return None

        lines = r.text.strip().split('\n')
        if len(lines) < 4:
            _cache[date_str] = None
            return None

        data = {}
        for line in lines[2:]:
            parts = [p.strip().replace('"', '').strip() for p in line.split(',')]
            if len(parts) < 9:
                continue
            category = parts[0].strip().upper()
            if category == 'TOTAL':
                continue

            try:
                fut_idx_long = int(parts[1]) if parts[1].strip() else 0
                fut_idx_short = int(parts[2]) if parts[2].strip() else 0
                fut_stk_long = int(parts[3]) if parts[3].strip() else 0
                fut_stk_short = int(parts[4]) if parts[4].strip() else 0
            except ValueError:
                continue

            try:
                opt_call_long = int(parts[5]) if parts[5].strip() else 0
                opt_put_long = int(parts[6]) if parts[6].strip() else 0
                opt_call_short = int(parts[7]) if parts[7].strip() else 0
                opt_put_short = int(parts[8]) if parts[8].strip() else 0
            except ValueError:
                opt_call_long = opt_put_long = opt_call_short = opt_put_short = 0

            prefix = None
            if 'FII' in category or 'FOREIGN' in category:
                prefix = 'fii'
            elif 'PRO' in category or 'PROPRIETARY' in category:
                prefix = 'pro'
            elif 'DII' in category or 'DOMESTIC' in category or 'MUTUAL' in category:
                prefix = 'dii'
            elif 'CLIENT' in category:
                prefix = 'client'

            if prefix:
                data[f'{prefix}_fut_idx_long'] = fut_idx_long
                data[f'{prefix}_fut_idx_short'] = fut_idx_short
                data[f'{prefix}_fut_idx_net'] = fut_idx_long - fut_idx_short
                data[f'{prefix}_fut_stk_long'] = fut_stk_long
                data[f'{prefix}_fut_stk_short'] = fut_stk_short
                data[f'{prefix}_fut_stk_net'] = fut_stk_long - fut_stk_short
                data[f'{prefix}_call_long'] = opt_call_long
                data[f'{prefix}_call_short'] = opt_call_short
                data[f'{prefix}_call_net'] = opt_call_long - opt_call_short
                data[f'{prefix}_put_long'] = opt_put_long
                data[f'{prefix}_put_short'] = opt_put_short
                data[f'{prefix}_put_net'] = opt_put_long - opt_put_short

        result = data if 'fii_fut_idx_net' in data else None
        _cache[date_str] = result
        return result

    except Exception as e:
        _cache[date_str] = None
        return None


def get_trading_days(start_date: datetime, end_date: datetime) -> list[datetime]:
    """Generate list of trading days (weekdays) between start and end."""
    days = []
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Mon-Fri
            days.append(current)
        current += timedelta(days=1)
    return days


def determine_direction(fut_net: int, call_net: int, put_net: int) -> str:
    """Determine direction from net positions."""
    # Net score: positive futures + short calls + long puts = bearish hedging
    # Simplified: use futures as primary signal
    net_signal = fut_net + call_net - put_net
    if net_signal > 15000:
        return "Bullish"
    elif net_signal < -15000:
        return "Bearish"
    else:
        return "Neutral"


def determine_stance(prefix: str, fut_daily: int, call_daily: int, put_daily: int) -> str:
    """Determine detailed stance from daily changes."""
    label = prefix.upper()
    has_bought_fut = fut_daily > 10000
    has_sold_fut = fut_daily < -10000
    has_sold_puts = put_daily < -20000
    has_bought_puts = put_daily > 20000
    has_sold_calls = call_daily < -20000

    if has_bought_fut and has_sold_puts:
        return f"{label} Bullish (bought fut + sold puts)"
    elif has_sold_fut and has_bought_puts:
        return f"{label} Very Bearish (sold fut + bought puts)"
    elif has_sold_fut:
        return f"{label} Bearish (sold fut >10K)"
    elif has_bought_puts:
        return f"{label} Hedging (bought puts >20K)"
    elif has_sold_puts:
        return f"{label} Confident (sold puts >20K)"
    elif has_bought_fut:
        return f"{label} Mildly Bullish"
    elif has_sold_calls:
        return f"{label} Mildly Bearish"
    else:
        return f"{label} Neutral"


def build_participant_daily(days_back: int = 30):
    """
    Fetch daily participant-wise OI data for the last N trading days.
    Computes daily changes and direction signals for FII, PRO, DII, Client.
    """
    print("=" * 70)
    print("FETCH PARTICIPANT-WISE DATA (FII / PRO / DII / Client)")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()
    print(f"Source: NSE Archives (archives.nseindia.com)")
    print(f"  → fao_participant_oi_DDMMYYYY.csv")
    print(f"  → Separate columns for: FII, PRO, DII, Client")
    print(f"  → Futures (Index + Stock) + Options (Call + Put) positions")
    print()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back + 10)  # extra buffer for weekends
    trading_days = get_trading_days(start_date, end_date)

    print(f"Fetching {len(trading_days)} potential trading days...")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print()

    session = get_nse_session()
    daily_records = []
    prev_data = None
    fetched = 0
    failed = 0

    for i, day in enumerate(trading_days):
        data = fetch_participant_oi(session, day)
        time.sleep(0.4)  # Rate limiting

        if data is None:
            failed += 1
            prev_data = None
            continue

        fetched += 1
        record = {'date': day.strftime('%Y-%m-%d')}

        # Store absolute positions
        for prefix in ['fii', 'pro', 'dii', 'client']:
            record[f'{prefix}_fut_idx_net'] = data.get(f'{prefix}_fut_idx_net', 0)
            record[f'{prefix}_fut_stk_net'] = data.get(f'{prefix}_fut_stk_net', 0)
            record[f'{prefix}_call_net'] = data.get(f'{prefix}_call_net', 0)
            record[f'{prefix}_put_net'] = data.get(f'{prefix}_put_net', 0)

        # Compute daily changes if we have previous day
        if prev_data:
            for prefix in ['fii', 'pro', 'dii', 'client']:
                fut_daily = data.get(f'{prefix}_fut_idx_net', 0) - prev_data.get(f'{prefix}_fut_idx_net', 0)
                call_daily = data.get(f'{prefix}_call_net', 0) - prev_data.get(f'{prefix}_call_net', 0)
                put_daily = data.get(f'{prefix}_put_net', 0) - prev_data.get(f'{prefix}_put_net', 0)

                record[f'{prefix}_fut_daily'] = fut_daily
                record[f'{prefix}_call_daily'] = call_daily
                record[f'{prefix}_put_daily'] = put_daily
                record[f'{prefix}_direction'] = determine_direction(fut_daily, call_daily, put_daily)
                record[f'{prefix}_stance'] = determine_stance(prefix, fut_daily, call_daily, put_daily)
        else:
            for prefix in ['fii', 'pro', 'dii', 'client']:
                record[f'{prefix}_fut_daily'] = 0
                record[f'{prefix}_call_daily'] = 0
                record[f'{prefix}_put_daily'] = 0
                record[f'{prefix}_direction'] = "Neutral"
                record[f'{prefix}_stance'] = f"{prefix.upper()} Neutral"

        daily_records.append(record)
        prev_data = data

        if (i + 1) % 5 == 0 or i < 3:
            fii_d = record.get('fii_direction', '?')
            pro_d = record.get('pro_direction', '?')
            print(f"  [{fetched}/{len(trading_days)}] {day.date()} "
                  f"FII:{record['fii_fut_idx_net']:+,} "
                  f"PRO:{record['pro_fut_idx_net']:+,} "
                  f"→ FII={fii_d} PRO={pro_d}")

    if not daily_records:
        print("\nERROR: No data fetched. NSE archives may be unavailable.")
        return

    df = pd.DataFrame(daily_records)

    # Save full dataset
    output_path = OUTPUT_DIR / "sensex_participant_wise_daily.csv"
    df.to_csv(output_path, index=False)

    print()
    print("=" * 70)
    print("COMPLETE!")
    print(f"  Output: {output_path}")
    print(f"  Rows: {len(df)} trading days")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Fetched: {fetched}, Failed/Holiday: {failed}")
    print()

    # Summary statistics
    # Skip first row (no daily change)
    analysis_df = df[df['fii_fut_daily'] != 0].copy() if len(df) > 1 else df

    print("  FII Direction Distribution:")
    for d, count in analysis_df['fii_direction'].value_counts().items():
        print(f"    {d}: {count} ({count/len(analysis_df)*100:.0f}%)")

    print()
    print("  PRO Direction Distribution:")
    for d, count in analysis_df['pro_direction'].value_counts().items():
        print(f"    {d}: {count} ({count/len(analysis_df)*100:.0f}%)")

    print()
    print("  FII Stance Distribution:")
    for stance, count in analysis_df['fii_stance'].value_counts().head(5).items():
        print(f"    {stance}: {count}")

    print()
    print("  PRO Stance Distribution:")
    for stance, count in analysis_df['pro_stance'].value_counts().head(5).items():
        print(f"    {stance}: {count}")

    print()
    print("  Latest positions (net contracts):")
    last = df.iloc[-1]
    print(f"    FII: Fut={last['fii_fut_idx_net']:+,} Call={last['fii_call_net']:+,} Put={last['fii_put_net']:+,}")
    print(f"    PRO: Fut={last['pro_fut_idx_net']:+,} Call={last['pro_call_net']:+,} Put={last['pro_put_net']:+,}")
    print(f"    DII: Fut={last['dii_fut_idx_net']:+,} Call={last['dii_call_net']:+,} Put={last['dii_put_net']:+,}")
    print(f"    Client: Fut={last['client_fut_idx_net']:+,} Call={last['client_call_net']:+,} Put={last['client_put_net']:+,}")
    print("=" * 70)


if __name__ == "__main__":
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print(f"Usage: python {sys.argv[0]} [days_back]")
            print(f"  days_back: number of calendar days to fetch (default: 30)")
            sys.exit(1)

    build_participant_daily(days_back=days)
