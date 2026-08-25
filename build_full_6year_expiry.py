#!/usr/bin/env python3
"""
Build complete 6-year vix_fii_t1_intraday_expiry_results.csv

Takes the existing 6-year VIX backtest data and enriches it with T-1 FII + PRO data
from NSE archives for every expiry day.

Steps:
1. Load vix_all_expiries_results_v6_6years.csv (317 rows)
2. Add recent expiry days (Jul 2026 to today) from yfinance
3. Fix close_vs_prev_range using actual previous TRADING day's high/low
4. For each expiry, fetch T-1 and T-2 FII + PRO participant data from NSE
5. Compute T-1 daily changes, stance, and risk level for both FII and PRO
6. Output complete vix_fii_t1_intraday_expiry_results.csv
"""

import pandas as pd
import numpy as np
import requests
import time
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).parent

NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/',
}

# Cache for NSE data to avoid re-fetching
nse_cache = {}


def get_nse_session():
    """Create NSE session."""
    session = requests.Session()
    session.headers.update(NSE_HEADERS)
    return session


def fetch_participant_oi(session, date: datetime) -> dict | None:
    """Fetch participant-wise OI for a date. Returns FII + PRO net positions or None."""
    date_str = date.strftime('%d%m%Y')

    # Check cache
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
        for line in lines[2:]:  # Skip title + header
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
        if d.weekday() < 5:  # Mon-Fri
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
    has_bought_calls = call_daily > 20000

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
    has_bought_calls = call_daily > 20000

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


def determine_expiry_risk(stance: str) -> str:
    """Determine risk level based on FII stance."""
    high_risk = ["FII Very Bearish", "FII Hedging", "FII Bearish"]
    safe = ["FII Bullish", "FII Confident"]

    for s in high_risk:
        if s in stance:
            return "HIGH (50% blowout history)"
    for s in safe:
        if s in stance:
            return "SAFE (0% blowout history)"

    if "Mildly Bearish" in stance:
        return "MODERATE (33% blowout history)"

    return "LOW (9% blowout history)"


def get_observation(vix_accuracy, move_direction, actual_range_pct, vix_predicted_move_pct, diff_pct):
    """Generate observation text."""
    if vix_accuracy == "Underestimated":
        return f"BLOWOUT {move_direction} | Actual {actual_range_pct}% vs VIX predicted {vix_predicted_move_pct}% (miss: +{diff_pct}%)"
    else:
        return "Normal day | VIX prediction was accurate within 0.5%"


def fix_close_vs_prev_range(base_df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix close_vs_prev_range and prev_close_to_close_pct by comparing
    against the actual previous TRADING day's high/low/close (not previous expiry day).
    """
    print("\nFetching full Nifty daily data to fix close_vs_prev_range...")

    # Get date range with buffer
    start_date = pd.to_datetime(base_df['date'].min()) - timedelta(days=10)
    end_date = pd.to_datetime(base_df['date'].max()) + timedelta(days=1)

    nifty_daily = yf.download('^NSEI',
                              start=start_date.strftime('%Y-%m-%d'),
                              end=end_date.strftime('%Y-%m-%d'),
                              progress=False)

    if isinstance(nifty_daily.columns, pd.MultiIndex):
        nifty_daily.columns = nifty_daily.columns.get_level_values(0)

    nifty_daily = nifty_daily.reset_index()
    nifty_daily['Date'] = pd.to_datetime(nifty_daily['Date']).dt.tz_localize(None)
    nifty_daily = nifty_daily.sort_values('Date').reset_index(drop=True)

    print(f"  Fetched {len(nifty_daily)} trading days ({nifty_daily['Date'].min().strftime('%Y-%m-%d')} to {nifty_daily['Date'].max().strftime('%Y-%m-%d')})")

    # Build lookup: for each expiry date, find previous trading day
    new_close_in_prev_range = []
    new_prev_close_to_close_pct = []
    new_close_vs_prev_range = []

    fixed_count = 0
    for idx, row in base_df.iterrows():
        expiry_date = pd.to_datetime(row['date'])
        nifty_close = row['nifty_close']

        # Find previous trading day in full daily data
        prev_days = nifty_daily[nifty_daily['Date'] < expiry_date].sort_values('Date')

        if len(prev_days) == 0:
            new_close_in_prev_range.append("N/A")
            new_prev_close_to_close_pct.append(None)
            new_close_vs_prev_range.append("N/A")
            continue

        prev_day = prev_days.iloc[-1]
        prev_high = float(prev_day['High'])
        prev_low = float(prev_day['Low'])
        prev_close = float(prev_day['Close'])

        # Compute prev_close_to_close_pct (from previous trading day's close)
        pct = round((nifty_close - prev_close) / prev_close * 100, 2)
        new_prev_close_to_close_pct.append(pct)

        # Compute close_in_prev_range
        if prev_low <= nifty_close <= prev_high:
            new_close_in_prev_range.append("Yes")
        else:
            new_close_in_prev_range.append("No")

        # Compute close_vs_prev_range
        if nifty_close > prev_high:
            new_close_vs_prev_range.append("Above High")
        elif nifty_close < prev_low:
            new_close_vs_prev_range.append("Below Low")
        else:
            new_close_vs_prev_range.append("Within Range")

        # Track fixes
        old_val = row.get('close_vs_prev_range', 'N/A')
        if old_val != new_close_vs_prev_range[-1]:
            fixed_count += 1

    base_df['close_in_prev_range'] = new_close_in_prev_range
    base_df['prev_close_to_close_pct'] = new_prev_close_to_close_pct
    base_df['close_vs_prev_range'] = new_close_vs_prev_range

    print(f"  Fixed {fixed_count} rows where close_vs_prev_range was incorrect")
    print(f"  Max |prev_close_to_close_pct| = {max(abs(x) for x in new_prev_close_to_close_pct if x is not None):.2f}%")

    return base_df


def main():
    print("=" * 70)
    print("BUILD COMPLETE 6-YEAR VIX + FII + PRO EXPIRY RESULTS")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()

    # Step 1: Load 6-year VIX backtest data
    v6_path = PROJECT_ROOT / "vix_all_expiries_results_v6_6years.csv"
    base_df = pd.read_csv(v6_path)
    print(f"Loaded base data: {len(base_df)} expiry days ({base_df['date'].min()} to {base_df['date'].max()})")

    # Step 2: Add recent expiry days not in base (after Jul 21 2026)
    last_date = pd.to_datetime(base_df['date'].max())
    today = datetime.now()

    # Check for recent expiry days to add
    # Expiry days after Sep 2025 are Tuesdays
    recent_expiries = []
    d = last_date + timedelta(days=1)
    while d <= today:
        if d.weekday() == 1:  # Tuesday
            recent_expiries.append(d)
        d += timedelta(days=1)

    if recent_expiries:
        print(f"Adding {len(recent_expiries)} recent expiry days...")
        # Fetch Nifty + VIX data
        nifty = yf.download('^NSEI',
                            start=(last_date - timedelta(days=10)).strftime('%Y-%m-%d'),
                            end=(today + timedelta(days=1)).strftime('%Y-%m-%d'),
                            progress=False)
        vix = yf.download('^INDIAVIX',
                          start=(last_date - timedelta(days=10)).strftime('%Y-%m-%d'),
                          end=(today + timedelta(days=1)).strftime('%Y-%m-%d'),
                          progress=False)

        if isinstance(nifty.columns, pd.MultiIndex):
            nifty.columns = nifty.columns.get_level_values(0)
        if isinstance(vix.columns, pd.MultiIndex):
            vix.columns = vix.columns.get_level_values(0)

        nifty = nifty.reset_index()
        vix = vix.reset_index()

        # Find all expiry dates for monthly classification
        all_recent_tuesdays = recent_expiries

        new_rows = []
        for exp_date in recent_expiries:
            date_str = exp_date.strftime('%Y-%m-%d')
            n_row = nifty[nifty['Date'].dt.strftime('%Y-%m-%d') == date_str]
            v_row = vix[vix['Date'].dt.strftime('%Y-%m-%d') == date_str]

            if n_row.empty or v_row.empty:
                continue

            nifty_open = float(n_row['Open'].values[0])
            nifty_high = float(n_row['High'].values[0])
            nifty_low = float(n_row['Low'].values[0])
            nifty_close = float(n_row['Close'].values[0])
            vix_open = float(v_row['Open'].values[0])
            vix_close = float(v_row['Close'].values[0])

            vix_predicted = round(vix_open / (252 ** 0.5), 2)
            actual_range = round((nifty_high - nifty_low) / nifty_open * 100, 2)
            actual_oc = round(abs(nifty_close - nifty_open) / nifty_open * 100, 2)
            intraday_high = round((nifty_high - nifty_open) / nifty_open * 100, 2)
            intraday_low = round((nifty_open - nifty_low) / nifty_open * 100, 2)
            range_vs_vix = round(actual_range / vix_predicted, 2) if vix_predicted > 0 else 0
            diff = round(actual_range - vix_predicted, 2)
            vix_accuracy = "Underestimated" if diff > 0.5 else "Overestimated"
            move_dir = "Down to Up" if nifty_close > nifty_open else "Top to Down"

            # Expiry type: monthly if last Tuesday of month
            month_tuesdays = [d for d in all_recent_tuesdays if d.month == exp_date.month and d.year == exp_date.year]
            expiry_type = "monthly" if exp_date == max(month_tuesdays) else "weekly"

            # Chart
            blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
            pr = nifty_high - nifty_low
            if pr > 0:
                def norm(p):
                    return int(round(min(7, max(0, ((p - nifty_low) / pr) * 7))))
                oi, hi, li, ci = norm(nifty_open), norm(nifty_high), norm(nifty_low), norm(nifty_close)
                chart = f"{blocks[oi]}↓{blocks[li]}↑{blocks[hi]}↓{blocks[ci]}"
                chart += " 📈" if nifty_close > nifty_open else " 📉"
            else:
                chart = "━━━━"

            row = {
                'date': date_str,
                'day_of_week': exp_date.strftime('%A'),
                'expiry_type': expiry_type,
                'chart': chart,
                'nifty_open': nifty_open,
                'nifty_high': nifty_high,
                'nifty_low': nifty_low,
                'nifty_close': nifty_close,
                'vix_open': vix_open,
                'vix_close': vix_close,
                'vix_predicted_move_pct': vix_predicted,
                'actual_range_pct': actual_range,
                'actual_open_close_pct': actual_oc,
                'intraday_high_pct': intraday_high,
                'intraday_low_pct': intraday_low,
                'range_vs_vix_ratio': range_vs_vix,
                'diff_pct': diff,
                'vix_accuracy': vix_accuracy,
                'move_direction': move_dir,
                'close_in_prev_range': "N/A",  # Will be fixed in Step 3
                'prev_close_to_close_pct': None,  # Will be fixed in Step 3
                'close_vs_prev_range': "N/A",  # Will be fixed in Step 3
            }
            new_rows.append(row)

        if new_rows:
            new_df = pd.DataFrame(new_rows)
            base_df = pd.concat([base_df, new_df], ignore_index=True)
            print(f"  Added {len(new_rows)} recent expiry days. Total: {len(base_df)}")

    print(f"\nTotal expiry days: {len(base_df)} ({base_df['date'].min()} to {base_df['date'].max()})")

    # Step 3: Fix close_vs_prev_range using actual previous trading day data
    base_df = fix_close_vs_prev_range(base_df)

    # Step 4: Fetch T-1 FII + PRO data from NSE for each expiry
    print(f"\nFetching T-1 FII + PRO data from NSE archives for {len(base_df)} expiry days...")
    print("(This will take ~10-15 minutes due to rate limiting)")
    print()

    session = get_nse_session()

    # Also load existing FII daily data for fast lookup where available
    fii_daily_path = PROJECT_ROOT / "fii_dii_backtest_daily_results.csv"
    fii_daily_df = pd.read_csv(fii_daily_path)
    fii_daily_df['Date'] = pd.to_datetime(fii_daily_df['Date'])
    fii_daily_df = fii_daily_df.sort_values('Date').reset_index(drop=True)
    fii_daily_min = fii_daily_df['Date'].min()
    fii_daily_max = fii_daily_df['Date'].max()
    print(f"FII daily data available: {fii_daily_min.strftime('%Y-%m-%d')} to {fii_daily_max.strftime('%Y-%m-%d')}")
    print()

    t1_fut_daily = []
    t1_call_daily = []
    t1_put_daily = []
    t1_stances = []
    t1_risks = []
    # PRO data lists
    t1_pro_fut_daily = []
    t1_pro_call_daily = []
    t1_pro_put_daily = []
    t1_pro_stances = []
    observations = []

    total = len(base_df)
    fetched_from_nse = 0
    fetched_from_local = 0
    failed = 0

    for idx, row in base_df.iterrows():
        expiry_date = pd.to_datetime(row['date'])

        # Check if we can use local FII daily data (only has FII, not PRO raw data)
        if fii_daily_min <= expiry_date <= fii_daily_max + timedelta(days=1):
            prev_days = fii_daily_df[fii_daily_df['Date'] < expiry_date].sort_values('Date')
            if len(prev_days) >= 2:
                t1 = prev_days.iloc[-1]
                t2 = prev_days.iloc[-2]
                fut_d = int(t1['fii_fut_idx_net'] - t2['fii_fut_idx_net'])
                call_d = int(t1['fii_call_net'] - t2['fii_call_net'])
                put_d = int(t1['fii_put_net'] - t2['fii_put_net'])

                t1_fut_daily.append(fut_d)
                t1_call_daily.append(call_d)
                t1_put_daily.append(put_d)

                stance = determine_fii_stance(fut_d, call_d, put_d)
                t1_stances.append(stance)
                t1_risks.append(determine_expiry_risk(stance))
                observations.append(get_observation(
                    row['vix_accuracy'], row['move_direction'],
                    row['actual_range_pct'], row['vix_predicted_move_pct'], row['diff_pct']
                ))

                # PRO data not available in local file - fetch from NSE
                t1_date = prev_days.iloc[-1]['Date'].to_pydatetime()
                t2_date = prev_days.iloc[-2]['Date'].to_pydatetime()
                t1_data = fetch_participant_oi(session, t1_date)
                time.sleep(0.3)
                t2_data = fetch_participant_oi(session, t2_date)
                time.sleep(0.3)

                if t1_data and t2_data and 'pro_fut_idx_net' in t1_data and 'pro_fut_idx_net' in t2_data:
                    pro_fut_d = int(t1_data['pro_fut_idx_net'] - t2_data['pro_fut_idx_net'])
                    pro_call_d = int(t1_data['pro_call_net'] - t2_data['pro_call_net'])
                    pro_put_d = int(t1_data['pro_put_net'] - t2_data['pro_put_net'])
                else:
                    pro_fut_d = 0
                    pro_call_d = 0
                    pro_put_d = 0

                t1_pro_fut_daily.append(pro_fut_d)
                t1_pro_call_daily.append(pro_call_d)
                t1_pro_put_daily.append(pro_put_d)
                t1_pro_stances.append(determine_pro_stance(pro_fut_d, pro_call_d, pro_put_d))

                fetched_from_local += 1

                if (idx + 1) % 50 == 0:
                    print(f"  [{idx+1}/{total}] {row['date']} - from local data (FII) + NSE (PRO)")
                continue

        # Need to fetch from NSE
        t1_date = find_prev_trading_day(expiry_date)
        t2_date = find_prev_trading_day(t1_date) if t1_date else None

        if t1_date is None or t2_date is None:
            t1_fut_daily.append(0)
            t1_call_daily.append(0)
            t1_put_daily.append(0)
            t1_stances.append("FII Neutral")
            t1_risks.append("LOW (9% blowout history)")
            t1_pro_fut_daily.append(0)
            t1_pro_call_daily.append(0)
            t1_pro_put_daily.append(0)
            t1_pro_stances.append("PRO Neutral")
            observations.append(get_observation(
                row['vix_accuracy'], row['move_direction'],
                row['actual_range_pct'], row['vix_predicted_move_pct'], row['diff_pct']
            ))
            failed += 1
            continue

        # Fetch T-1 and T-2 from NSE
        t1_data = fetch_participant_oi(session, t1_date)
        time.sleep(0.8)
        t2_data = fetch_participant_oi(session, t2_date)
        time.sleep(0.8)

        # If T-1 failed, try the day before (might be a holiday)
        if t1_data is None:
            t1_date = find_prev_trading_day(t1_date)
            if t1_date:
                t1_data = fetch_participant_oi(session, t1_date)
                time.sleep(0.8)

        if t2_data is None:
            t2_date = find_prev_trading_day(t2_date)
            if t2_date:
                t2_data = fetch_participant_oi(session, t2_date)
                time.sleep(0.8)

        if t1_data and t2_data:
            fut_d = t1_data['fii_fut_idx_net'] - t2_data['fii_fut_idx_net']
            call_d = t1_data['fii_call_net'] - t2_data['fii_call_net']
            put_d = t1_data['fii_put_net'] - t2_data['fii_put_net']

            # PRO data
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
        t1_risks.append(determine_expiry_risk(stance))
        t1_pro_stances.append(determine_pro_stance(pro_fut_d, pro_call_d, pro_put_d))
        observations.append(get_observation(
            row['vix_accuracy'], row['move_direction'],
            row['actual_range_pct'], row['vix_predicted_move_pct'], row['diff_pct']
        ))

        if (idx + 1) % 10 == 0 or idx < 5:
            print(f"  [{idx+1}/{total}] {row['date']} - T1={t1_date.strftime('%Y-%m-%d') if t1_date else 'N/A'} "
                  f"fut={int(fut_d):+,} call={int(call_d):+,} put={int(put_d):+,} → {stance}")

    # Step 5: Add columns to base_df
    base_df['t1_fii_fut_daily'] = t1_fut_daily
    base_df['t1_fii_call_daily'] = t1_call_daily
    base_df['t1_fii_put_daily'] = t1_put_daily
    base_df['t1_fii_stance'] = t1_stances
    base_df['t1_pro_fut_daily'] = t1_pro_fut_daily
    base_df['t1_pro_call_daily'] = t1_pro_call_daily
    base_df['t1_pro_put_daily'] = t1_pro_put_daily
    base_df['t1_pro_stance'] = t1_pro_stances
    base_df['expiry_risk_level'] = t1_risks
    base_df['observation'] = observations

    # Step 6: Save
    output_path = PROJECT_ROOT / "vix_fii_t1_intraday_expiry_results.csv"
    base_df.to_csv(output_path, index=False)

    print()
    print("=" * 70)
    print(f"COMPLETE!")
    print(f"  Output: {output_path.name}")
    print(f"  Total rows: {len(base_df)}")
    print(f"  Date range: {base_df['date'].min()} to {base_df['date'].max()}")
    print(f"  FII data from local: {fetched_from_local}")
    print(f"  FII data from NSE: {fetched_from_nse}")
    print(f"  FII data failed/NA: {failed}")
    print()
    # Print close_vs_prev_range distribution
    print("  close_vs_prev_range distribution:")
    dist = base_df['close_vs_prev_range'].value_counts()
    for k, v in dist.items():
        print(f"    {k}: {v} ({v/len(base_df)*100:.1f}%)")
    print("=" * 70)


if __name__ == "__main__":
    main()
