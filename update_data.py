#!/usr/bin/env python3
"""
UPDATE ALL DATA — Single script to keep everything up-to-date.

Run this weekly (or after each expiry) to update:
1. fii_dii_backtest_daily_results.csv (daily FII/DII positions from NSE)
2. vix_fii_t1_intraday_expiry_results.csv (expiry day analysis with VIX + FII + PRO)

Usage:
    python3 update_data.py

What it does:
    Step 1: Fetches new daily FII/DII participant data from NSE archives
            (from last date in CSV to today)
    Step 2: Adds new expiry days to the expiry results CSV
            (correctly computes close_vs_prev_range using previous TRADING day)
    Step 3: Fetches T-1 FII + PRO data for new expiry days

Requirements:
    pip install pandas yfinance requests
"""

import pandas as pd
import numpy as np
import requests
import time
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent

NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/',
}

nse_cache = {}


def get_nse_session():
    """Create NSE session with cookies."""
    session = requests.Session()
    session.headers.update(NSE_HEADERS)
    try:
        session.get('https://www.nseindia.com/', timeout=10)
    except Exception:
        pass
    time.sleep(1)
    return session


def fetch_participant_oi(session, date: datetime) -> dict | None:
    """Fetch participant-wise OI for a date. Returns FII + PRO net positions."""
    date_str = date.strftime('%d%m%Y')
    if date_str in nse_cache:
        return nse_cache[date_str]

    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{date_str}.csv"

    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            nse_cache[date_str] = None
            return None

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

            if 'DII' in category or 'DOMESTIC' in category:
                data['dii_fut_idx_net'] = fut_idx_long - fut_idx_short

            if 'CLIENT' in category:
                data['client_fut_idx_net'] = fut_idx_long - fut_idx_short

        result = data if 'fii_fut_idx_net' in data else None
        nse_cache[date_str] = result
        return result

    except Exception:
        nse_cache[date_str] = None
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


# ─── STEP 1: Update FII/DII Daily ────────────────────────────────────────────

def update_fii_daily(session) -> pd.DataFrame:
    """Update fii_dii_backtest_daily_results.csv with missing days."""
    csv_path = PROJECT_ROOT / "fii_dii_backtest_daily_results.csv"
    existing_df = pd.read_csv(csv_path)
    last_date = pd.to_datetime(existing_df['Date'].max())
    today = datetime.now()

    print(f"  Current: {existing_df['Date'].min()} to {existing_df['Date'].max()} ({len(existing_df)} rows)")

    start_fetch = last_date + timedelta(days=1)
    if start_fetch.date() > today.date():
        print("  Already up to date!")
        return existing_df

    # Get Nifty data for trading day reference
    nifty = yf.download('^NSEI',
                        start=start_fetch.strftime('%Y-%m-%d'),
                        end=(today + timedelta(days=1)).strftime('%Y-%m-%d'),
                        progress=False)
    if nifty.empty:
        print("  No new trading days found.")
        return existing_df

    if isinstance(nifty.columns, pd.MultiIndex):
        nifty.columns = nifty.columns.get_level_values(0)
    nifty = nifty.reset_index()

    trading_days = pd.to_datetime(nifty['Date']).dt.tz_localize(None).tolist()
    print(f"  Fetching {len(trading_days)} new trading days...")

    last_fii_fut = existing_df['fii_fut_idx_net'].iloc[-1]
    new_rows = []

    for trade_date in trading_days:
        data = fetch_participant_oi(session, trade_date)
        if data is None:
            time.sleep(0.5)
            continue

        nifty_row = nifty[pd.to_datetime(nifty['Date']).dt.tz_localize(None) == trade_date]
        if nifty_row.empty:
            continue

        nifty_close = float(nifty_row['Close'].values[0])
        prev_close = float(nifty.loc[nifty.index < nifty_row.index[0], 'Close'].iloc[-1]) if nifty_row.index[0] > 0 else nifty_close
        nifty_change = round((nifty_close - prev_close) / prev_close * 100, 2) if prev_close else 0

        market_dir = 'Bullish' if nifty_change > 0.1 else ('Bearish' if nifty_change < -0.1 else 'Neutral')

        fii_fut = data['fii_fut_idx_net']
        fii_change = fii_fut - last_fii_fut
        fii_dir = 'Bullish' if fii_change > 5000 else ('Bearish' if fii_change < -5000 else 'Neutral')

        fii_correct = ''
        if fii_dir in ('Bullish', 'Bearish'):
            fii_correct = 'Correct' if fii_dir == market_dir else 'Incorrect'

        row = {
            'Date': trade_date.strftime('%Y-%m-%d'),
            'fii_fut_idx_net': fii_fut,
            'fii_call_net': data['fii_call_net'],
            'fii_put_net': data['fii_put_net'],
            'FII_Direction': fii_dir,
            'DII_Direction': 'Neutral',
            'Pro_Direction': 'Neutral',
            'Client_Direction': 'Neutral',
            'Nifty_Close': nifty_close,
            'Nifty_Change_Pct': nifty_change,
            'Market_Direction': market_dir,
            'FII_Correct': fii_correct
        }
        new_rows.append(row)
        last_fii_fut = fii_fut
        print(f"    {trade_date.strftime('%Y-%m-%d')}: FII fut={fii_fut:+,} dir={fii_dir}")
        time.sleep(1.0)

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
        print(f"  Updated: {len(existing_df)} → {len(updated_df)} rows")
        return updated_df
    else:
        print("  No new data added.")
        return existing_df


# ─── STEP 2: Update Expiry Results ───────────────────────────────────────────

def update_expiry_results(session, fii_daily_df: pd.DataFrame):
    """Update vix_fii_t1_intraday_expiry_results.csv with new expiry days."""
    csv_path = PROJECT_ROOT / "vix_fii_t1_intraday_expiry_results.csv"
    existing_df = pd.read_csv(csv_path)
    last_expiry = pd.to_datetime(existing_df['date'].max())
    today = datetime.now()

    print(f"  Current: {existing_df['date'].min()} to {existing_df['date'].max()} ({len(existing_df)} rows)")

    # Find new expiry Tuesdays after last date
    new_expiry_dates = []
    d = last_expiry + timedelta(days=1)
    while d.date() <= today.date():
        if d.weekday() == 1:  # Tuesday (expiry day since Sep 2025)
            new_expiry_dates.append(d)
        d += timedelta(days=1)

    if not new_expiry_dates:
        print("  No new expiry dates to add.")
        return

    print(f"  New expiry dates: {len(new_expiry_dates)}")

    # Fetch Nifty + VIX data for the period (with buffer for prev day lookup)
    start = (last_expiry - timedelta(days=10)).strftime('%Y-%m-%d')
    end = (today + timedelta(days=1)).strftime('%Y-%m-%d')

    nifty_daily = yf.download('^NSEI', start=start, end=end, progress=False)
    vix_daily = yf.download('^INDIAVIX', start=start, end=end, progress=False)

    if nifty_daily.empty or vix_daily.empty:
        print("  Could not fetch Nifty/VIX data.")
        return

    for df in [nifty_daily, vix_daily]:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

    nifty_daily = nifty_daily.reset_index()
    nifty_daily['Date'] = pd.to_datetime(nifty_daily['Date']).dt.tz_localize(None)
    vix_daily = vix_daily.reset_index()
    vix_daily['Date'] = pd.to_datetime(vix_daily['Date']).dt.tz_localize(None)

    # FII daily for T-1 lookups
    fii_daily_df = fii_daily_df.copy()
    fii_daily_df['Date'] = pd.to_datetime(fii_daily_df['Date'])

    # All expiry dates for monthly classification
    all_recent_tuesdays = new_expiry_dates

    new_rows = []
    for exp_date in new_expiry_dates:
        date_str = exp_date.strftime('%Y-%m-%d')

        # Get expiry day data
        n_row = nifty_daily[nifty_daily['Date'] == exp_date]
        v_row = vix_daily[vix_daily['Date'] == exp_date]

        if n_row.empty or v_row.empty:
            print(f"    {date_str}: No data (holiday?), skipping")
            continue

        nifty_open = float(n_row['Open'].values[0])
        nifty_high = float(n_row['High'].values[0])
        nifty_low = float(n_row['Low'].values[0])
        nifty_close = float(n_row['Close'].values[0])
        vix_open = float(v_row['Open'].values[0])
        vix_close = float(v_row['Close'].values[0])

        # Previous TRADING day (for close_vs_prev_range)
        prev_days = nifty_daily[nifty_daily['Date'] < exp_date].sort_values('Date')
        if len(prev_days) == 0:
            continue
        prev_day = prev_days.iloc[-1]
        prev_high = float(prev_day['High'])
        prev_low = float(prev_day['Low'])
        prev_close = float(prev_day['Close'])

        # Compute metrics
        vix_predicted = round(vix_open / (252 ** 0.5), 2)
        actual_range = round((nifty_high - nifty_low) / nifty_open * 100, 2)
        actual_oc = round(abs(nifty_close - nifty_open) / nifty_open * 100, 2)
        intraday_high = round((nifty_high - nifty_open) / nifty_open * 100, 2)
        intraday_low = round((nifty_open - nifty_low) / nifty_open * 100, 2)
        range_vs_vix = round(actual_range / vix_predicted, 2) if vix_predicted > 0 else 0
        diff = round(actual_range - vix_predicted, 2)
        vix_accuracy = "Underestimated" if diff > 0.5 else "Overestimated"
        move_dir = "Down to Up" if nifty_close > nifty_open else "Top to Down"

        # Close vs previous TRADING day's range
        prev_close_pct = round((nifty_close - prev_close) / prev_close * 100, 2)
        close_in_prev = "Yes" if prev_low <= nifty_close <= prev_high else "No"
        if nifty_close > prev_high:
            close_vs = "Above High"
        elif nifty_close < prev_low:
            close_vs = "Below Low"
        else:
            close_vs = "Within Range"

        # Expiry type
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

        # T-1 FII + PRO data
        fii_prev = fii_daily_df[fii_daily_df['Date'] < exp_date].sort_values('Date')
        if len(fii_prev) >= 2:
            t1 = fii_prev.iloc[-1]
            t2 = fii_prev.iloc[-2]
            t1_fii_fut = int(t1['fii_fut_idx_net'] - t2['fii_fut_idx_net'])
            t1_fii_call = int(t1['fii_call_net'] - t2['fii_call_net'])
            t1_fii_put = int(t1['fii_put_net'] - t2['fii_put_net'])
        else:
            t1_fii_fut = t1_fii_call = t1_fii_put = 0

        # PRO from NSE
        t1_date_dt = fii_prev.iloc[-1]['Date'].to_pydatetime() if len(fii_prev) >= 1 else None
        t2_date_dt = fii_prev.iloc[-2]['Date'].to_pydatetime() if len(fii_prev) >= 2 else None

        pro_fut_d = pro_call_d = pro_put_d = 0
        if t1_date_dt and t2_date_dt:
            t1_data = fetch_participant_oi(session, t1_date_dt)
            time.sleep(0.3)
            t2_data = fetch_participant_oi(session, t2_date_dt)
            time.sleep(0.3)
            if t1_data and t2_data and 'pro_fut_idx_net' in t1_data and 'pro_fut_idx_net' in t2_data:
                pro_fut_d = int(t1_data['pro_fut_idx_net'] - t2_data['pro_fut_idx_net'])
                pro_call_d = int(t1_data['pro_call_net'] - t2_data['pro_call_net'])
                pro_put_d = int(t1_data['pro_put_net'] - t2_data['pro_put_net'])

        fii_stance = determine_fii_stance(t1_fii_fut, t1_fii_call, t1_fii_put)
        pro_stance = determine_pro_stance(pro_fut_d, pro_call_d, pro_put_d)
        risk = determine_expiry_risk(fii_stance)

        if vix_accuracy == "Underestimated":
            obs = f"BLOWOUT {move_dir} | Actual {actual_range}% vs VIX predicted {vix_predicted}% (miss: +{diff}%)"
        else:
            obs = "Normal day | VIX prediction was accurate within 0.5%"

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
            'close_in_prev_range': close_in_prev,
            'prev_close_to_close_pct': prev_close_pct,
            'close_vs_prev_range': close_vs,
            't1_fii_fut_daily': t1_fii_fut,
            't1_fii_call_daily': t1_fii_call,
            't1_fii_put_daily': t1_fii_put,
            't1_fii_stance': fii_stance,
            't1_pro_fut_daily': pro_fut_d,
            't1_pro_call_daily': pro_call_d,
            't1_pro_put_daily': pro_put_d,
            't1_pro_stance': pro_stance,
            'expiry_risk_level': risk,
            'observation': obs,
        }
        new_rows.append(row)
        print(f"    {date_str} ({expiry_type}): {move_dir}, close_vs_prev={close_vs}, {fii_stance}")

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
        print(f"  Updated: {len(existing_df)} → {len(updated_df)} rows")
    else:
        print("  No new expiry days added.")


# ─── STEP 3: Regenerate FII-PRO Alignment Analysis ─────────────────────────

def update_fii_pro_alignment():
    """Regenerate fii_pro_alignment_results.csv and fii_pro_alignment_results_3year.csv from the daily results CSV."""
    import subprocess
    import sys

    script = PROJECT_ROOT / "fii-pro-alignment-analysis" / "analyze_fii_pro_alignment.py"
    if not script.exists():
        print("  Script not found, skipping.")
        return

    daily_csv = PROJECT_ROOT / "vix_fii_t1_intraday_daily_results.csv"
    if not daily_csv.exists():
        print("  vix_fii_t1_intraday_daily_results.csv not found, skipping.")
        return

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(PROJECT_ROOT),
        capture_output=True, text=True
    )
    if result.returncode == 0:
        # Show last few lines of output
        lines = result.stdout.strip().split('\n')
        for line in lines[-6:]:
            print(f"  {line}")
    else:
        print(f"  Error: {result.stderr[:500]}")


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("UPDATE ALL DATA")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()

    session = get_nse_session()

    # Step 1: Update FII/DII daily
    print("STEP 1: Update fii_dii_backtest_daily_results.csv")
    print("-" * 50)
    fii_df = update_fii_daily(session)

    # Step 2: Update expiry results
    print()
    print("STEP 2: Update vix_fii_t1_intraday_expiry_results.csv")
    print("-" * 50)
    update_expiry_results(session, fii_df)

    # Step 3: Regenerate FII-PRO alignment analysis (full + 3-year + reports)
    print()
    print("STEP 3: Regenerate fii-pro-alignment-analysis/ (full + 3-year CSVs + reports)")
    print("-" * 50)
    update_fii_pro_alignment()

    print()
    print("=" * 60)
    print("ALL DONE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
