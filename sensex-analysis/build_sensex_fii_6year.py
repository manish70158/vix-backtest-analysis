#!/usr/bin/env python3
"""
Build 6-year Sensex + FII/PRO T-1 dataset

Takes the 6-year Sensex VIX backtest data (318 expiries, 2020-2026) and enriches
it with T-1 FII + PRO daily flow data from NSE archives.

Steps:
1. Load vix_sensex_6y_results.csv (318 rows)
2. For each Sensex expiry, fetch T-1 and T-2 FII + PRO participant data from NSE
3. Compute T-1 daily changes, stance, and risk level
4. Output sensex_fii_t1_6year.csv

Author: Claude Code
Date: 2026-08-26
"""

import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = Path(__file__).parent

NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/',
}

# Cache for NSE data
nse_cache = {}


def get_nse_session():
    """Create NSE session."""
    session = requests.Session()
    session.headers.update(NSE_HEADERS)
    return session


def fetch_participant_oi(session, date: datetime) -> dict | None:
    """Fetch participant-wise OI for a date. Returns FII + PRO net positions or None."""
    date_str = date.strftime('%d%m%Y')

    if date_str in nse_cache:
        return nse_cache[date_str]

    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{date_str}.csv"

    try:
        r = session.get(url, timeout=15)
        if r.status_code == 404:
            nse_cache[date_str] = None
            return None
        if r.status_code != 200:
            nse_cache[date_str] = None
            return None
        r.raise_for_status()

        lines = r.text.strip().split('\n')
        if len(lines) < 4:
            nse_cache[date_str] = None
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
            except ValueError:
                continue

            opt_call_long = int(parts[5]) if parts[5].strip() else 0
            opt_put_long = int(parts[6]) if parts[6].strip() else 0
            opt_call_short = int(parts[7]) if parts[7].strip() else 0
            opt_put_short = int(parts[8]) if parts[8].strip() else 0

            if 'FII' in category or 'FOREIGN' in category:
                data['fii_fut_idx_net'] = fut_idx_long - fut_idx_short
                data['fii_call_net'] = opt_call_long - opt_call_short
                data['fii_put_net'] = opt_put_long - opt_put_short

            if 'PRO' in category or 'PROPRIETARY' in category:
                data['pro_fut_idx_net'] = fut_idx_long - fut_idx_short
                data['pro_call_net'] = opt_call_long - opt_call_short
                data['pro_put_net'] = opt_put_long - opt_put_short

            if 'DII' in category or 'DOMESTIC' in category or 'MUTUAL' in category:
                data['dii_fut_idx_net'] = fut_idx_long - fut_idx_short

            if 'CLIENT' in category:
                data['client_fut_idx_net'] = fut_idx_long - fut_idx_short

        result = data if 'fii_fut_idx_net' in data else None
        nse_cache[date_str] = result
        return result

    except Exception:
        nse_cache[date_str] = None
        return None


def find_prev_trading_day(date: datetime, max_lookback: int = 7) -> datetime | None:
    """Find previous trading day (skip weekends)."""
    d = date - timedelta(days=1)
    for _ in range(max_lookback):
        if d.weekday() < 5:
            return d
        d -= timedelta(days=1)
    return None


def determine_fii_stance(fut_daily, call_daily, put_daily):
    """Determine FII stance from T-1 daily changes."""
    has_bought_fut = fut_daily > 10000
    has_sold_fut = fut_daily < -10000
    has_sold_puts = put_daily < -20000
    has_bought_puts = put_daily > 20000
    has_sold_calls = call_daily < -20000

    if has_bought_fut and has_sold_puts:
        return "FII Bullish (bought fut + sold puts)"
    elif has_sold_fut and has_bought_puts:
        return "FII Very Bearish (sold fut >10K + bought puts >20K)"
    elif has_sold_fut:
        return "FII Bearish (sold fut >10K)"
    elif has_bought_puts:
        return "FII Hedging (bought puts >20K)"
    elif has_sold_puts:
        return "FII Confident (sold puts >20K)"
    elif has_bought_fut:
        return "FII Mildly Bullish"
    elif has_sold_calls:
        return "FII Mildly Bearish"
    else:
        return "FII Neutral"


def determine_pro_stance(fut_daily, call_daily, put_daily):
    """Determine PRO stance from T-1 daily changes."""
    has_bought_fut = fut_daily > 10000
    has_sold_fut = fut_daily < -10000
    has_sold_puts = put_daily < -20000
    has_bought_puts = put_daily > 20000
    has_sold_calls = call_daily < -20000

    if has_bought_fut and has_sold_puts:
        return "PRO Bullish (bought fut + sold puts)"
    elif has_sold_fut and has_bought_puts:
        return "PRO Very Bearish (sold fut >10K + bought puts >20K)"
    elif has_sold_fut:
        return "PRO Bearish (sold fut >10K)"
    elif has_bought_puts:
        return "PRO Hedging (bought puts >20K)"
    elif has_sold_puts:
        return "PRO Confident (sold puts >20K)"
    elif has_bought_fut:
        return "PRO Mildly Bullish"
    elif has_sold_calls:
        return "PRO Mildly Bearish"
    else:
        return "PRO Neutral"


def determine_fii_direction(fut_daily, call_daily, put_daily):
    """Simplified FII direction: Bullish/Bearish/Neutral."""
    net = fut_daily + call_daily - put_daily
    if net > 15000:
        return "Bullish"
    elif net < -15000:
        return "Bearish"
    else:
        return "Neutral"


def main():
    print("=" * 70)
    print("BUILD 6-YEAR SENSEX + FII/PRO T-1 DATASET")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()

    # Step 1: Load 6-year Sensex VIX data
    sensex_path = OUTPUT_DIR / "vix_sensex_6y_results.csv"
    if not sensex_path.exists():
        print(f"ERROR: Sensex VIX file not found: {sensex_path}")
        sys.exit(1)

    sensex_df = pd.read_csv(sensex_path)
    sensex_df['date'] = pd.to_datetime(sensex_df['date'])
    print(f"Loaded Sensex VIX data: {len(sensex_df)} expiry days ({sensex_df['date'].min().date()} to {sensex_df['date'].max().date()})")

    # Step 2: Check for existing Nifty FII data (reuse where dates overlap)
    nifty_fii_path = PROJECT_ROOT / "vix_fii_t1_intraday_expiry_results.csv"
    nifty_fii_lookup = {}
    if nifty_fii_path.exists():
        nifty_fii = pd.read_csv(nifty_fii_path)
        nifty_fii['date'] = pd.to_datetime(nifty_fii['date'])
        for _, row in nifty_fii.iterrows():
            nifty_fii_lookup[row['date'].date()] = row
        print(f"Loaded Nifty FII lookup: {len(nifty_fii_lookup)} dates available for reuse")

    # Step 3: Fetch T-1 FII + PRO data for each Sensex expiry
    print(f"\nFetching T-1 FII + PRO data from NSE archives for {len(sensex_df)} Sensex expiry days...")
    print("(This will take ~15-20 minutes due to NSE rate limiting)")
    print()

    session = get_nse_session()

    t1_fut_daily = []
    t1_call_daily = []
    t1_put_daily = []
    t1_stances = []
    t1_directions = []
    t1_pro_fut_daily = []
    t1_pro_call_daily = []
    t1_pro_put_daily = []
    t1_pro_stances = []

    total = len(sensex_df)
    fetched_from_nse = 0
    reused_from_nifty = 0
    failed = 0

    for idx, row in sensex_df.iterrows():
        expiry_date = row['date']

        # Find T-1 and T-2 dates
        t1_date = find_prev_trading_day(expiry_date)
        t2_date = find_prev_trading_day(t1_date) if t1_date else None

        if t1_date is None or t2_date is None:
            t1_fut_daily.append(0)
            t1_call_daily.append(0)
            t1_put_daily.append(0)
            t1_stances.append("FII Neutral")
            t1_directions.append("Neutral")
            t1_pro_fut_daily.append(0)
            t1_pro_call_daily.append(0)
            t1_pro_put_daily.append(0)
            t1_pro_stances.append("PRO Neutral")
            failed += 1
            continue

        # Try to fetch from NSE
        t1_data = fetch_participant_oi(session, t1_date)
        time.sleep(0.5)
        t2_data = fetch_participant_oi(session, t2_date)
        time.sleep(0.5)

        # Retry if T-1 failed (might be holiday)
        if t1_data is None:
            alt_t1 = find_prev_trading_day(t1_date)
            if alt_t1:
                t1_data = fetch_participant_oi(session, alt_t1)
                time.sleep(0.5)

        if t2_data is None:
            alt_t2 = find_prev_trading_day(t2_date)
            if alt_t2:
                t2_data = fetch_participant_oi(session, alt_t2)
                time.sleep(0.5)

        if t1_data and t2_data:
            fut_d = t1_data['fii_fut_idx_net'] - t2_data['fii_fut_idx_net']
            call_d = t1_data['fii_call_net'] - t2_data['fii_call_net']
            put_d = t1_data['fii_put_net'] - t2_data['fii_put_net']

            # PRO
            if 'pro_fut_idx_net' in t1_data and 'pro_fut_idx_net' in t2_data:
                pro_fut_d = t1_data['pro_fut_idx_net'] - t2_data['pro_fut_idx_net']
                pro_call_d = t1_data['pro_call_net'] - t2_data['pro_call_net']
                pro_put_d = t1_data['pro_put_net'] - t2_data['pro_put_net']
            else:
                pro_fut_d = 0
                pro_call_d = 0
                pro_put_d = 0

            fetched_from_nse += 1
        else:
            fut_d = 0
            call_d = 0
            put_d = 0
            pro_fut_d = 0
            pro_call_d = 0
            pro_put_d = 0
            failed += 1

        t1_fut_daily.append(int(fut_d))
        t1_call_daily.append(int(call_d))
        t1_put_daily.append(int(put_d))
        t1_pro_fut_daily.append(int(pro_fut_d))
        t1_pro_call_daily.append(int(pro_call_d))
        t1_pro_put_daily.append(int(pro_put_d))

        stance = determine_fii_stance(fut_d, call_d, put_d)
        t1_stances.append(stance)
        t1_directions.append(determine_fii_direction(fut_d, call_d, put_d))
        t1_pro_stances.append(determine_pro_stance(pro_fut_d, pro_call_d, pro_put_d))

        if (idx + 1) % 10 == 0 or idx < 5:
            print(f"  [{idx+1}/{total}] {expiry_date.date()} - T1={t1_date.strftime('%Y-%m-%d')} "
                  f"fut={int(fut_d):+,} call={int(call_d):+,} put={int(put_d):+,} → {stance}")

    # Step 4: Add columns
    sensex_df['t1_fii_fut_daily'] = t1_fut_daily
    sensex_df['t1_fii_call_daily'] = t1_call_daily
    sensex_df['t1_fii_put_daily'] = t1_put_daily
    sensex_df['t1_fii_stance'] = t1_stances
    sensex_df['t1_fii_direction'] = t1_directions
    sensex_df['t1_pro_fut_daily'] = t1_pro_fut_daily
    sensex_df['t1_pro_call_daily'] = t1_pro_call_daily
    sensex_df['t1_pro_put_daily'] = t1_pro_put_daily
    sensex_df['t1_pro_stance'] = t1_pro_stances

    # Mark Nifty co-expiry (Thursday)
    sensex_df['is_nifty_expiry_day'] = (sensex_df['date'].dt.dayofweek == 3).astype(int)

    # Step 5: Save
    output_path = OUTPUT_DIR / "sensex_fii_t1_6year.csv"
    sensex_df['date'] = sensex_df['date'].dt.strftime('%Y-%m-%d')
    sensex_df.to_csv(output_path, index=False)

    print()
    print("=" * 70)
    print("COMPLETE!")
    print(f"  Output: {output_path}")
    print(f"  Total rows: {len(sensex_df)}")
    print(f"  Date range: {sensex_df['date'].min()} to {sensex_df['date'].max()}")
    print(f"  FII data from NSE: {fetched_from_nse}")
    print(f"  FII data failed/NA: {failed}")
    print()
    print("  FII stance distribution:")
    for stance, count in sensex_df['t1_fii_stance'].value_counts().items():
        print(f"    {stance}: {count} ({count/len(sensex_df)*100:.1f}%)")
    print()
    print("  FII direction distribution:")
    for d, count in sensex_df['t1_fii_direction'].value_counts().items():
        print(f"    {d}: {count} ({count/len(sensex_df)*100:.1f}%)")
    print("=" * 70)


if __name__ == "__main__":
    main()
