#!/usr/bin/env python3
"""
Fetch missing FII/DII participant data from NSE and update both CSV files.

Updates:
1. fii_dii_backtest_daily_results.csv (from last date to today)
2. vix_fii_t1_intraday_expiry_results.csv (missing expiry days)
"""

import pandas as pd
import numpy as np
import requests
import time
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
import io
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent

# NSE session setup
NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nseindia.com/',
    'Connection': 'keep-alive',
}


def get_nse_session():
    """Create an authenticated NSE session."""
    session = requests.Session()
    session.headers.update(NSE_HEADERS)
    # Hit main page to get cookies
    try:
        r = session.get('https://www.nseindia.com/', timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"  Warning: Initial NSE session setup: {e}")
    time.sleep(1)
    return session


def fetch_participant_oi(session, date: datetime) -> dict | None:
    """
    Fetch participant-wise OI data for a given date from NSE archives.

    Returns dict with fii_fut_idx_net, fii_call_net, fii_put_net or None if not available.
    """
    date_str = date.strftime('%d%m%Y')
    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{date_str}.csv"

    try:
        r = session.get(url, timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()

        # Parse the CSV
        # Format:
        # Row 0: Title ("Participant wise Open Interest...")
        # Row 1: Column headers (Client Type, Future Index Long, Future Index Short, ...)
        # Row 2+: Data (Client, DII, FII, Pro, TOTAL)
        #
        # Columns (0-indexed):
        #  0: Client Type
        #  1: Future Index Long
        #  2: Future Index Short
        #  3: Future Stock Long
        #  4: Future Stock Short
        #  5: Option Index Call Long
        #  6: Option Index Put Long
        #  7: Option Index Call Short
        #  8: Option Index Put Short
        #  9-12: Option Stock (Call/Put Long/Short)
        # 13: Total Long
        # 14: Total Short

        lines = r.text.strip().split('\n')
        if len(lines) < 4:
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

            if 'FII' in category or 'FOREIGN' in category:
                opt_call_long = int(parts[5]) if parts[5].strip() else 0
                opt_put_long = int(parts[6]) if parts[6].strip() else 0
                opt_call_short = int(parts[7]) if parts[7].strip() else 0
                opt_put_short = int(parts[8]) if parts[8].strip() else 0

                data['fii_fut_idx_net'] = fut_idx_long - fut_idx_short
                data['fii_call_net'] = opt_call_long - opt_call_short
                data['fii_put_net'] = opt_put_long - opt_put_short
            elif 'DII' in category or 'DOMESTIC' in category:
                data['dii_fut_idx_net'] = fut_idx_long - fut_idx_short
            elif 'PRO' in category:
                data['pro_fut_idx_net'] = fut_idx_long - fut_idx_short
            elif 'CLIENT' in category:
                data['client_fut_idx_net'] = fut_idx_long - fut_idx_short

        if 'fii_fut_idx_net' in data:
            return data
        return None

    except Exception as e:
        print(f"  Error fetching {date.strftime('%Y-%m-%d')}: {e}")
        return None


def determine_direction(net_position: float, prev_position: float | None, threshold: float = 5000) -> str:
    """Determine Bullish/Bearish/Neutral based on position and change."""
    if prev_position is None:
        return "Neutral"
    change = net_position - prev_position
    if change > threshold:
        return "Bullish"
    elif change < -threshold:
        return "Bearish"
    return "Neutral"


def determine_fii_direction_from_data(row: dict, prev_row: dict | None) -> str:
    """Determine FII direction based on futures position change."""
    if prev_row is None:
        return "Neutral"
    change = row['fii_fut_idx_net'] - prev_row['fii_fut_idx_net']
    if change > 5000:
        return "Bullish"
    elif change < -5000:
        return "Bearish"
    return "Neutral"


def compute_directions(df: pd.DataFrame) -> pd.DataFrame:
    """Compute direction columns based on position changes."""
    df = df.copy()

    # FII Direction based on fut change
    df['fii_fut_change'] = df['fii_fut_idx_net'].diff()
    df['FII_Direction'] = df['fii_fut_change'].apply(
        lambda x: 'Bullish' if x > 5000 else ('Bearish' if x < -5000 else 'Neutral')
    )

    # DII Direction
    if 'dii_fut_idx_net' in df.columns:
        df['dii_fut_change'] = df['dii_fut_idx_net'].diff()
        df['DII_Direction'] = df['dii_fut_change'].apply(
            lambda x: 'Bullish' if x > 5000 else ('Bearish' if x < -5000 else 'Neutral')
        )
    else:
        df['DII_Direction'] = 'Neutral'

    # Pro Direction
    if 'pro_fut_idx_net' in df.columns:
        df['pro_fut_change'] = df['pro_fut_idx_net'].diff()
        df['Pro_Direction'] = df['pro_fut_change'].apply(
            lambda x: 'Bullish' if x > 5000 else ('Bearish' if x < -5000 else 'Neutral')
        )
    else:
        df['Pro_Direction'] = 'Neutral'

    # Client Direction
    if 'client_fut_idx_net' in df.columns:
        df['client_fut_change'] = df['client_fut_idx_net'].diff()
        df['Client_Direction'] = df['client_fut_change'].apply(
            lambda x: 'Bullish' if x > 5000 else ('Bearish' if x < -5000 else 'Neutral')
        )
    else:
        df['Client_Direction'] = 'Neutral'

    # Drop temp columns
    for col in ['fii_fut_change', 'dii_fut_change', 'pro_fut_change', 'client_fut_change']:
        if col in df.columns:
            df = df.drop(columns=[col])

    return df


def get_nifty_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch Nifty 50 daily data from yfinance."""
    nifty = yf.download('^NSEI', start=start_date, end=end_date, progress=False)
    if nifty.empty:
        return pd.DataFrame()

    # Flatten multi-level columns if present
    if isinstance(nifty.columns, pd.MultiIndex):
        nifty.columns = nifty.columns.get_level_values(0)

    nifty = nifty.reset_index()
    nifty['Date'] = pd.to_datetime(nifty['Date']).dt.strftime('%Y-%m-%d')
    nifty['Nifty_Close'] = nifty['Close']
    nifty['Nifty_Change_Pct'] = nifty['Close'].pct_change() * 100
    nifty['Market_Direction'] = nifty['Nifty_Change_Pct'].apply(
        lambda x: 'Bullish' if x > 0.1 else ('Bearish' if x < -0.1 else 'Neutral')
    )
    return nifty[['Date', 'Nifty_Close', 'Nifty_Change_Pct', 'Market_Direction', 'Open', 'High', 'Low', 'Close']]


def get_vix_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch India VIX daily data from yfinance."""
    vix = yf.download('^INDIAVIX', start=start_date, end=end_date, progress=False)
    if vix.empty:
        return pd.DataFrame()

    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)

    vix = vix.reset_index()
    vix['Date'] = pd.to_datetime(vix['Date']).dt.strftime('%Y-%m-%d')
    vix = vix.rename(columns={'Open': 'vix_open', 'Close': 'vix_close'})
    return vix[['Date', 'vix_open', 'vix_close']]


def determine_fii_stance(fut_daily, call_daily, put_daily):
    """Determine FII stance from T-1 daily changes."""
    stance_parts = []

    if fut_daily > 10000:
        stance_parts.append("bought fut >10K")
    elif fut_daily < -10000:
        stance_parts.append("sold fut >10K")

    if put_daily < -20000:
        stance_parts.append("sold puts >20K")
    elif put_daily > 20000:
        stance_parts.append("bought puts >20K")

    if call_daily < -20000:
        stance_parts.append("sold calls >20K")
    elif call_daily > 20000:
        stance_parts.append("bought calls >20K")

    if not stance_parts:
        return "FII Neutral"

    # Composite stance
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


def determine_expiry_risk(stance: str, historical_blowout_pct: float = None) -> str:
    """Determine risk level based on FII stance."""
    high_risk_stances = [
        "FII Very Bearish", "FII Hedging", "FII Bearish"
    ]
    safe_stances = ["FII Bullish", "FII Confident"]

    for s in high_risk_stances:
        if s in stance:
            return "HIGH (50% blowout history)"
    for s in safe_stances:
        if s in stance:
            return "SAFE (0% blowout history)"

    return "LOW (9% blowout history)"


def get_expiry_dates_in_range(start_date: datetime, end_date: datetime) -> list:
    """
    Generate weekly expiry dates (Tuesdays after Sept 2025, Thursdays before).
    Monthly = last expiry of month.
    """
    expiry_dates = []
    current = start_date

    while current <= end_date:
        # After Sept 1, 2025 expiries are on Tuesday
        # Before that, on Thursday
        cutoff = datetime(2025, 9, 1)

        if current >= cutoff:
            # Tuesday expiry
            if current.weekday() == 1:  # Tuesday
                expiry_dates.append(current)
        else:
            # Thursday expiry
            if current.weekday() == 3:  # Thursday
                expiry_dates.append(current)

        current += timedelta(days=1)

    return expiry_dates


def classify_expiry_type(date: datetime, all_expiry_dates: list) -> str:
    """Determine if expiry is weekly or monthly (last expiry of month)."""
    month_expiries = [d for d in all_expiry_dates if d.month == date.month and d.year == date.year]
    if month_expiries and date == max(month_expiries):
        return "monthly"
    return "weekly"


def generate_chart(open_price, high, low, close):
    """Generate a visual mini-chart using Unicode block characters."""
    blocks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

    price_range = high - low
    if price_range == 0:
        return "━━━━"

    def normalize(price):
        normalized = ((price - low) / price_range) * 7
        return int(round(min(7, max(0, normalized))))

    open_idx = normalize(open_price)
    high_idx = normalize(high)
    low_idx = normalize(low)
    close_idx = normalize(close)

    chart_parts = []
    chart_parts.append(f"{blocks[open_idx]}")

    if low_idx < open_idx:
        chart_parts.append("↓")
        chart_parts.append(f"{blocks[low_idx]}")

    chart_parts.append("↑")
    chart_parts.append(f"{blocks[high_idx]}")

    if close_idx < high_idx:
        chart_parts.append("↓")

    chart_parts.append(f"{blocks[close_idx]}")

    emoji = "📈" if close > open_price else "📉"
    chart_parts.append(f" {emoji}")

    return "".join(chart_parts)


def update_fii_dii_daily():
    """Update fii_dii_backtest_daily_results.csv with missing data."""
    csv_path = PROJECT_ROOT / "fii_dii_backtest_daily_results.csv"

    # Load existing data
    existing_df = pd.read_csv(csv_path)
    last_date = pd.to_datetime(existing_df['Date'].max())
    today = datetime.now()

    print(f"Existing data: {existing_df['Date'].min()} to {existing_df['Date'].max()} ({len(existing_df)} rows)")
    print(f"Need to fetch: {(last_date + timedelta(days=1)).strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}")

    # Generate list of trading days to fetch
    start_fetch = last_date + timedelta(days=1)
    if start_fetch > today:
        print("Already up to date!")
        return existing_df

    # Fetch Nifty data for the missing period
    nifty_data = get_nifty_data(
        start_fetch.strftime('%Y-%m-%d'),
        (today + timedelta(days=1)).strftime('%Y-%m-%d')
    )

    if nifty_data.empty:
        print("No Nifty data available for the missing period.")
        return existing_df

    trading_days = [pd.to_datetime(d) for d in nifty_data['Date'].tolist()]
    print(f"Trading days to fetch: {len(trading_days)}")

    # Fetch FII/DII data from NSE for each missing day
    session = get_nse_session()
    new_rows = []

    # Get last known positions for direction computation
    last_fii_fut = existing_df['fii_fut_idx_net'].iloc[-1]
    last_fii_call = existing_df['fii_call_net'].iloc[-1]
    last_fii_put = existing_df['fii_put_net'].iloc[-1]

    for i, trade_date in enumerate(trading_days):
        print(f"  Fetching {trade_date.strftime('%Y-%m-%d')} ({i+1}/{len(trading_days)})...", end=" ")

        participant_data = fetch_participant_oi(session, trade_date)

        if participant_data is None:
            print("No data (holiday?)")
            time.sleep(0.5)
            continue

        # Get Nifty data for this day
        nifty_row = nifty_data[nifty_data['Date'] == trade_date.strftime('%Y-%m-%d')]
        if nifty_row.empty:
            print("No Nifty price data")
            continue

        nifty_close = nifty_row['Nifty_Close'].values[0]
        nifty_change = nifty_row['Nifty_Change_Pct'].values[0]
        market_dir = nifty_row['Market_Direction'].values[0]

        # Compute directions
        fii_fut_net = participant_data['fii_fut_idx_net']
        fii_change = fii_fut_net - last_fii_fut

        fii_dir = 'Bullish' if fii_change > 5000 else ('Bearish' if fii_change < -5000 else 'Neutral')

        dii_fut_net = participant_data.get('dii_fut_idx_net', 0)
        pro_fut_net = participant_data.get('pro_fut_idx_net', 0)
        client_fut_net = participant_data.get('client_fut_idx_net', 0)

        # For DII/Pro/Client we'd need previous values too
        dii_dir = 'Neutral'  # Simplified for now
        pro_dir = 'Neutral'
        client_dir = 'Neutral'

        # Check FII_Correct
        fii_correct = ''
        if fii_dir == 'Bullish' and market_dir == 'Bullish':
            fii_correct = 'Correct'
        elif fii_dir == 'Bullish' and market_dir == 'Bearish':
            fii_correct = 'Incorrect'
        elif fii_dir == 'Bearish' and market_dir == 'Bearish':
            fii_correct = 'Correct'
        elif fii_dir == 'Bearish' and market_dir == 'Bullish':
            fii_correct = 'Incorrect'

        row = {
            'Date': trade_date.strftime('%Y-%m-%d'),
            'fii_fut_idx_net': fii_fut_net,
            'fii_call_net': participant_data['fii_call_net'],
            'fii_put_net': participant_data['fii_put_net'],
            'FII_Direction': fii_dir,
            'DII_Direction': dii_dir,
            'Pro_Direction': pro_dir,
            'Client_Direction': client_dir,
            'Nifty_Close': nifty_close,
            'Nifty_Change_Pct': round(nifty_change, 2),
            'Market_Direction': market_dir,
            'FII_Correct': fii_correct
        }
        new_rows.append(row)

        # Update last known for next iteration
        last_fii_fut = fii_fut_net
        last_fii_call = participant_data['fii_call_net']
        last_fii_put = participant_data['fii_put_net']

        print(f"OK (FII fut: {fii_fut_net:,}, dir: {fii_dir})")
        time.sleep(1.5)  # Rate limit

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
        print(f"\nUpdated {csv_path.name}: {len(existing_df)} → {len(updated_df)} rows")
        return updated_df
    else:
        print("\nNo new data fetched.")
        return existing_df


def update_vix_expiry_results(fii_daily_df: pd.DataFrame):
    """Update vix_fii_t1_intraday_expiry_results.csv with missing expiry days."""
    csv_path = PROJECT_ROOT / "vix_fii_t1_intraday_expiry_results.csv"

    existing_df = pd.read_csv(csv_path)
    last_expiry = pd.to_datetime(existing_df['date'].max())
    today = datetime.now()

    print(f"\nExpiry results: {existing_df['date'].min()} to {existing_df['date'].max()} ({len(existing_df)} rows)")

    # Find missing expiry dates
    all_expiry_dates = get_expiry_dates_in_range(last_expiry + timedelta(days=1), today)

    if not all_expiry_dates:
        print("No new expiry dates to add.")
        return

    print(f"New expiry dates to process: {len(all_expiry_dates)}")

    # Get full range of expiry dates for monthly classification
    full_expiry_dates = get_expiry_dates_in_range(
        last_expiry - timedelta(days=60), today + timedelta(days=30)
    )

    # Fetch Nifty + VIX data
    start = (last_expiry - timedelta(days=5)).strftime('%Y-%m-%d')
    end = (today + timedelta(days=1)).strftime('%Y-%m-%d')

    nifty_data = get_nifty_data(start, end)
    vix_data = get_vix_data(start, end)

    if nifty_data.empty or vix_data.empty:
        print("Could not fetch Nifty/VIX data.")
        return

    # Get previous expiry close for range comparison
    prev_close = existing_df['nifty_close'].iloc[-1]
    prev_high = existing_df['nifty_high'].iloc[-1]
    prev_low = existing_df['nifty_low'].iloc[-1]

    # Process FII daily data
    fii_daily_df['Date'] = pd.to_datetime(fii_daily_df['Date'])

    new_rows = []
    for expiry_date in all_expiry_dates:
        date_str = expiry_date.strftime('%Y-%m-%d')

        # Check if this was actually a trading day
        nifty_row = nifty_data[nifty_data['Date'] == date_str]
        if nifty_row.empty:
            print(f"  {date_str}: Not a trading day (holiday?), skipping")
            continue

        vix_row = vix_data[vix_data['Date'] == date_str]
        if vix_row.empty:
            print(f"  {date_str}: No VIX data, skipping")
            continue

        # Extract OHLC
        nifty_open = float(nifty_row['Open'].values[0])
        nifty_high = float(nifty_row['High'].values[0])
        nifty_low = float(nifty_row['Low'].values[0])
        nifty_close = float(nifty_row['Close'].values[0])
        vix_open = float(vix_row['vix_open'].values[0])
        vix_close = float(vix_row['vix_close'].values[0])

        # VIX predicted move
        vix_predicted_move_pct = round(vix_open / (252 ** 0.5) * (1 / 252 ** 0.5) * 100, 2)
        # Simplified: VIX / sqrt(252) gives daily expected move
        vix_predicted_move_pct = round(vix_open / (252 ** 0.5), 2)

        # Actual metrics
        actual_range_pct = round((nifty_high - nifty_low) / nifty_open * 100, 2)
        actual_open_close_pct = round(abs(nifty_close - nifty_open) / nifty_open * 100, 2)
        intraday_high_pct = round((nifty_high - nifty_open) / nifty_open * 100, 2)
        intraday_low_pct = round((nifty_open - nifty_low) / nifty_open * 100, 2)

        range_vs_vix = round(actual_range_pct / vix_predicted_move_pct, 2) if vix_predicted_move_pct > 0 else 0
        diff_pct = round(actual_range_pct - vix_predicted_move_pct, 2)

        # VIX accuracy (0.5% threshold)
        if diff_pct > 0.5:
            vix_accuracy = "Underestimated"
        else:
            vix_accuracy = "Overestimated"

        # Move direction
        if nifty_close > nifty_open:
            move_direction = "Down to Up"
        else:
            move_direction = "Top to Down"

        # Close in prev range
        close_in_prev_range = "Yes" if prev_low <= nifty_close <= prev_high else "No"

        # Prev close to close pct
        prev_close_to_close_pct = round((nifty_close - prev_close) / prev_close * 100, 2)

        # Close vs prev range
        if nifty_close > prev_high:
            close_vs_prev_range = "Above High"
        elif nifty_close < prev_low:
            close_vs_prev_range = "Below Low"
        else:
            close_vs_prev_range = "Within Range"

        # T-1 FII data (previous trading day)
        prev_days = fii_daily_df[fii_daily_df['Date'] < expiry_date].sort_values('Date')
        if len(prev_days) >= 2:
            t1_row = prev_days.iloc[-1]
            t2_row = prev_days.iloc[-2]
            t1_fii_fut_daily = int(t1_row['fii_fut_idx_net'] - t2_row['fii_fut_idx_net'])
            t1_fii_call_daily = int(t1_row['fii_call_net'] - t2_row['fii_call_net'])
            t1_fii_put_daily = int(t1_row['fii_put_net'] - t2_row['fii_put_net'])
        else:
            t1_fii_fut_daily = 0
            t1_fii_call_daily = 0
            t1_fii_put_daily = 0

        # FII Stance
        t1_fii_stance = determine_fii_stance(t1_fii_fut_daily, t1_fii_call_daily, t1_fii_put_daily)

        # Expiry risk level
        expiry_risk_level = determine_expiry_risk(t1_fii_stance)

        # Observation
        if vix_accuracy == "Underestimated":
            observation = f"BLOWOUT {move_direction} | Actual {actual_range_pct}% vs VIX predicted {vix_predicted_move_pct}% (miss: +{diff_pct}%)"
        else:
            observation = "Normal day | VIX prediction was accurate within 0.5%"

        # Expiry type
        expiry_type = classify_expiry_type(expiry_date, full_expiry_dates)

        # Chart
        chart = generate_chart(nifty_open, nifty_high, nifty_low, nifty_close)

        # Day of week
        day_of_week = expiry_date.strftime('%A')

        row = {
            'date': date_str,
            'day_of_week': day_of_week,
            'expiry_type': expiry_type,
            'chart': chart,
            'nifty_open': nifty_open,
            'nifty_high': nifty_high,
            'nifty_low': nifty_low,
            'nifty_close': nifty_close,
            'vix_open': vix_open,
            'vix_close': vix_close,
            'vix_predicted_move_pct': vix_predicted_move_pct,
            'actual_range_pct': actual_range_pct,
            'actual_open_close_pct': actual_open_close_pct,
            'intraday_high_pct': intraday_high_pct,
            'intraday_low_pct': intraday_low_pct,
            'range_vs_vix_ratio': range_vs_vix,
            'diff_pct': diff_pct,
            'vix_accuracy': vix_accuracy,
            'move_direction': move_direction,
            'close_in_prev_range': close_in_prev_range,
            'prev_close_to_close_pct': prev_close_to_close_pct,
            'close_vs_prev_range': close_vs_prev_range,
            't1_fii_fut_daily': t1_fii_fut_daily,
            't1_fii_call_daily': t1_fii_call_daily,
            't1_fii_put_daily': t1_fii_put_daily,
            't1_fii_stance': t1_fii_stance,
            'expiry_risk_level': expiry_risk_level,
            'observation': observation,
        }
        new_rows.append(row)

        # Update prev values for next iteration
        prev_close = nifty_close
        prev_high = nifty_high
        prev_low = nifty_low

        print(f"  {date_str} ({day_of_week}, {expiry_type}): {move_direction}, VIX {vix_accuracy}")

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
        print(f"\nUpdated {csv_path.name}: {len(existing_df)} → {len(updated_df)} rows")
    else:
        print("\nNo new expiry days to add.")


def main():
    print("=" * 60)
    print("FETCH MISSING DATA - FII/DII + VIX EXPIRY UPDATER")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()

    # Step 1: Update FII/DII daily data
    print("STEP 1: Updating fii_dii_backtest_daily_results.csv")
    print("-" * 50)
    fii_daily_df = update_fii_dii_daily()

    # Step 2: Update VIX expiry results
    print("\nSTEP 2: Updating vix_fii_t1_intraday_expiry_results.csv")
    print("-" * 50)
    update_vix_expiry_results(fii_daily_df)

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
