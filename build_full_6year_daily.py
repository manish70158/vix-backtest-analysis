#!/usr/bin/env python3
"""
Build complete 6-year DAILY CSV files with FII/PRO T-1 data for ALL trading days.

Fetches T-1 participant OI from NSE archives for every trading day (not just expiry).
Creates:
  - vix_fii_t1_intraday_daily_results.csv (Nifty, all trading days)
  - sensex-analysis/sensex_fii_t1_daily_results.csv (Sensex, all trading days)

NSE source: https://archives.nseindia.com/content/nsccl/fao_participant_oi_DDMMYYYY.csv

This script takes ~30-45 minutes due to NSE rate limiting (~3000 requests).
Progress is cached to disk so you can resume if interrupted.
"""

import json
import time
import sys
import warnings
from pathlib import Path
from datetime import datetime, timedelta, date as dt_date
from zoneinfo import ZoneInfo

import pandas as pd
import psycopg2
import requests

warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy.*")

IST = ZoneInfo("Asia/Kolkata")
REPO = Path(__file__).resolve().parent
CACHE_FILE = REPO / ".nse_oi_cache.json"

NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/',
}


# ---------------------------------------------------------------------------
# NSE fetching (same logic as build_full_6year_expiry.py)
# ---------------------------------------------------------------------------
def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


def fetch_participant_oi(session, date_obj, cache):
    """Fetch participant-wise OI for a date. Returns dict or None."""
    date_str = date_obj.strftime('%d%m%Y')
    cache_key = date_str

    if cache_key in cache:
        return cache[cache_key]

    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{date_str}.csv"

    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            cache[cache_key] = None
            return None

        lines = r.text.strip().split('\n')
        if len(lines) < 4:
            cache[cache_key] = None
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

        result = data if 'fii_fut_idx_net' in data else None
        cache[cache_key] = result
        return result

    except Exception:
        cache[cache_key] = None
        return None


def find_prev_trading_day(date_obj, max_lookback=7):
    d = date_obj - timedelta(days=1)
    for _ in range(max_lookback):
        if d.weekday() < 5:
            return d
        d -= timedelta(days=1)
    return None


# ---------------------------------------------------------------------------
# Stance / View classification
# ---------------------------------------------------------------------------
def determine_stance(prefix, fut_d, call_d, put_d):
    if fut_d > 10000 and put_d < -20000:
        return f"{prefix} Bullish (bought fut + sold puts)"
    elif fut_d < -10000 and put_d > 20000:
        return f"{prefix} Very Bearish (sold fut >10K + bought puts >20K)"
    elif fut_d < -10000:
        return f"{prefix} Bearish (sold fut >10K)"
    elif put_d > 20000:
        return f"{prefix} Hedging (bought puts >20K)"
    elif put_d < -20000:
        return f"{prefix} Confident (sold puts >20K)"
    elif fut_d > 10000:
        return f"{prefix} Mildly Bullish"
    elif call_d < -20000:
        return f"{prefix} Mildly Bearish"
    else:
        return f"{prefix} Neutral"


def classify_view(val):
    if val is None or pd.isna(val):
        return None
    val = float(val)
    if val > 100000: return "Strong Bullish"
    elif val > 50000: return "Bullish"
    elif val > 30000: return "Mildly Bullish"
    elif val >= -30000: return "Neutral"
    elif val >= -50000: return "Mildly Bearish"
    elif val >= -100000: return "Bearish"
    else: return "Strong Bearish"


# ---------------------------------------------------------------------------
# Database queries
# ---------------------------------------------------------------------------
def fetch_all_trading_days():
    """Get all trading dates and daily OHLC from 5-min data."""
    conn = psycopg2.connect(host="localhost", dbname="market_data")
    df = pd.read_sql("""
        WITH day_bounds AS (
            SELECT datetime::date AS dt,
                   MIN(datetime) AS first_bar,
                   MAX(datetime) AS last_bar,
                   MAX(high) AS day_high,
                   MIN(low) AS day_low
            FROM nifty50_5min
            GROUP BY datetime::date
        )
        SELECT db.dt AS date,
               first.open AS nifty_open,
               db.day_high AS nifty_high,
               db.day_low AS nifty_low,
               last.close AS nifty_close
        FROM day_bounds db
        JOIN nifty50_5min first ON first.datetime = db.first_bar
        JOIN nifty50_5min last ON last.datetime = db.last_bar
        ORDER BY db.dt
    """, conn)
    conn.close()
    return df


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("BUILD 6-YEAR DAILY FII/PRO DATA (ALL TRADING DAYS)")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

    # 1. Get all trading days
    print("\n[1] Fetching trading days from DB...")
    daily_ohlc = fetch_all_trading_days()
    all_dates = [pd.Timestamp(d).to_pydatetime().date() if not isinstance(d, dt_date) else d
                 for d in daily_ohlc["date"]]
    print(f"    {len(all_dates)} trading days ({all_dates[0]} to {all_dates[-1]})")

    # 2. Load expiry info
    print("\n[2] Loading expiry metadata...")
    nifty_exp_df = pd.read_csv(REPO / "vix_fii_t1_intraday_expiry_results.csv", parse_dates=["date"])
    nifty_exp = {}
    for _, r in nifty_exp_df.iterrows():
        d = r["date"].date()
        nifty_exp[d] = {
            "expiry_type": r["expiry_type"],
            "vix_open": r["vix_open"],
            "vix_close": r["vix_close"],
        }

    sensex_exp_df = pd.read_csv(REPO / "sensex-analysis" / "sensex_fii_t1_6year_expiry.csv", parse_dates=["date"])
    sensex_exp = {}
    for _, r in sensex_exp_df.iterrows():
        d = r["date"].date()
        sensex_exp[d] = {
            "expiry_type": r["expiry_type"],
            "sensex_open": r["sensex_open"], "sensex_high": r["sensex_high"],
            "sensex_low": r["sensex_low"], "sensex_close": r["sensex_close"],
            "vix_open": r["vix_open"], "vix_close": r["vix_close"],
        }
    print(f"    Nifty expiry days: {len(nifty_exp)}, Sensex expiry days: {len(sensex_exp)}")

    # 3. Build sorted list of all dates we need OI for (each day + its prev day)
    print("\n[3] Loading NSE OI cache...")
    cache = load_cache()
    cached_count = sum(1 for v in cache.values() if v is not None)
    print(f"    Cache has {len(cache)} entries ({cached_count} with data)")

    # Collect all dates we need to fetch (T-1 and T-2 for each trading day)
    dates_needed = set()
    for d in all_dates:
        t1 = find_prev_trading_day(datetime.combine(d, datetime.min.time()))
        if t1:
            dates_needed.add(t1.date() if isinstance(t1, datetime) else t1)
            t2 = find_prev_trading_day(t1)
            if t2:
                dates_needed.add(t2.date() if isinstance(t2, datetime) else t2)

    already_cached = sum(1 for d in dates_needed if d.strftime('%d%m%Y') in cache)
    to_fetch = len(dates_needed) - already_cached
    print(f"    Need OI for {len(dates_needed)} unique dates, {already_cached} already cached, {to_fetch} to fetch")

    # 4. Fetch all missing OI data from NSE
    if to_fetch > 0:
        print(f"\n[4] Fetching {to_fetch} dates from NSE archives...")
        print(f"    Estimated time: ~{to_fetch * 0.8 / 60:.0f} minutes (rate limited)")

        session = requests.Session()
        session.headers.update(NSE_HEADERS)

        fetched = 0
        failed = 0
        sorted_dates = sorted(dates_needed)
        for i, d in enumerate(sorted_dates):
            key = d.strftime('%d%m%Y')
            if key in cache:
                continue

            dt_obj = datetime.combine(d, datetime.min.time())
            result = fetch_participant_oi(session, dt_obj, cache)
            fetched += 1
            if result is None:
                failed += 1

            # Rate limiting
            time.sleep(0.7)

            # Progress + periodic cache save
            if fetched % 50 == 0:
                save_cache(cache)
                pct = round(fetched / to_fetch * 100, 1)
                print(f"    [{fetched}/{to_fetch}] {pct}% — last: {d} — failed: {failed}")

            if fetched % 200 == 0:
                # Refresh session to avoid stale connections
                session = requests.Session()
                session.headers.update(NSE_HEADERS)

        save_cache(cache)
        print(f"    Done! Fetched {fetched}, failed {failed}")
    else:
        print("\n[4] All OI data already cached — skipping fetch")

    # 5. Build daily results
    print("\n[5] Computing T-1 daily changes for all trading days...")
    rows = []
    success = 0
    no_data = 0

    for idx, ohlc_row in daily_ohlc.iterrows():
        d = ohlc_row["date"]
        if isinstance(d, str):
            d = pd.Timestamp(d).date()
        elif hasattr(d, "date"):
            d = d.date() if not isinstance(d, dt_date) else d

        o = float(ohlc_row["nifty_open"])
        h = float(ohlc_row["nifty_high"])
        l = float(ohlc_row["nifty_low"])
        c = float(ohlc_row["nifty_close"])

        actual_range_pct = round((h - l) / o * 100, 2)
        actual_oc_pct = round((c - o) / o * 100, 2)
        intraday_high_pct = round((h - o) / o * 100, 2)
        intraday_low_pct = round((l - o) / o * 100, 2)
        move_direction = "Top to Down" if o > c else ("Down to Up" if o < c else "Flat")
        dow = d.strftime("%A")

        # T-1 participant data
        dt_obj = datetime.combine(d, datetime.min.time())
        t1_date = find_prev_trading_day(dt_obj)
        t2_date = find_prev_trading_day(t1_date) if t1_date else None

        fii_fut_d = fii_call_d = fii_put_d = None
        pro_fut_d = pro_call_d = pro_put_d = None

        if t1_date and t2_date:
            t1_key = (t1_date.date() if isinstance(t1_date, datetime) else t1_date).strftime('%d%m%Y')
            t2_key = (t2_date.date() if isinstance(t2_date, datetime) else t2_date).strftime('%d%m%Y')
            t1_data = cache.get(t1_key)
            t2_data = cache.get(t2_key)

            if t1_data and t2_data:
                fii_fut_d = t1_data['fii_fut_idx_net'] - t2_data['fii_fut_idx_net']
                fii_call_d = t1_data['fii_call_net'] - t2_data['fii_call_net']
                fii_put_d = t1_data['fii_put_net'] - t2_data['fii_put_net']

                if 'pro_fut_idx_net' in t1_data and 'pro_fut_idx_net' in t2_data:
                    pro_fut_d = t1_data['pro_fut_idx_net'] - t2_data['pro_fut_idx_net']
                    pro_call_d = t1_data['pro_call_net'] - t2_data['pro_call_net']
                    pro_put_d = t1_data['pro_put_net'] - t2_data['pro_put_net']

                success += 1
            else:
                no_data += 1
        else:
            no_data += 1

        # Stance and composite
        fii_stance = determine_stance("FII", fii_fut_d, fii_call_d, fii_put_d) if fii_fut_d is not None else None
        pro_stance = determine_stance("PRO", pro_fut_d, pro_call_d, pro_put_d) if pro_fut_d is not None else None
        fii_comp = int(fii_fut_d + fii_call_d - fii_put_d) if fii_fut_d is not None else None
        pro_comp = int(pro_fut_d + pro_call_d - pro_put_d) if pro_fut_d is not None else None

        # Expiry info
        nex = nifty_exp.get(d)
        sxe = sensex_exp.get(d)
        is_nifty_expiry = 1 if nex else 0
        is_sensex_expiry = 1 if sxe else 0
        vix_open = nex["vix_open"] if nex else (sxe["vix_open"] if sxe else None)
        vix_close = nex["vix_close"] if nex else (sxe["vix_close"] if sxe else None)

        rows.append({
            "date": str(d),
            "day_of_week": dow,
            "is_nifty_expiry": is_nifty_expiry,
            "is_sensex_expiry": is_sensex_expiry,
            "expiry_type": nex["expiry_type"] if nex else (sxe["expiry_type"] if sxe else None),
            "nifty_open": round(o, 2),
            "nifty_high": round(h, 2),
            "nifty_low": round(l, 2),
            "nifty_close": round(c, 2),
            "sensex_open": round(float(sxe["sensex_open"]), 2) if sxe else None,
            "sensex_high": round(float(sxe["sensex_high"]), 2) if sxe else None,
            "sensex_low": round(float(sxe["sensex_low"]), 2) if sxe else None,
            "sensex_close": round(float(sxe["sensex_close"]), 2) if sxe else None,
            "actual_range_pct": actual_range_pct,
            "actual_open_close_pct": actual_oc_pct,
            "intraday_high_pct": intraday_high_pct,
            "intraday_low_pct": intraday_low_pct,
            "move_direction": move_direction,
            "vix_open": round(float(vix_open), 2) if vix_open is not None else None,
            "vix_close": round(float(vix_close), 2) if vix_close is not None else None,
            "t1_fii_fut_daily": int(fii_fut_d) if fii_fut_d is not None else None,
            "t1_fii_call_daily": int(fii_call_d) if fii_call_d is not None else None,
            "t1_fii_put_daily": int(fii_put_d) if fii_put_d is not None else None,
            "t1_fii_stance": fii_stance,
            "fii_composite": fii_comp,
            "fii_view": classify_view(fii_comp),
            "t1_pro_fut_daily": int(pro_fut_d) if pro_fut_d is not None else None,
            "t1_pro_call_daily": int(pro_call_d) if pro_call_d is not None else None,
            "t1_pro_put_daily": int(pro_put_d) if pro_put_d is not None else None,
            "t1_pro_stance": pro_stance,
            "pro_composite": pro_comp,
            "pro_view": classify_view(pro_comp),
        })

    result_df = pd.DataFrame(rows)
    print(f"    Success: {success}, No data: {no_data}")

    # 6. Write Nifty daily CSV
    nifty_cols = [c for c in result_df.columns if c != "is_sensex_expiry" and not c.startswith("sensex_")]
    nifty_df = result_df[nifty_cols].copy()
    nifty_path = REPO / "vix_fii_t1_intraday_daily_results.csv"
    nifty_df.to_csv(nifty_path, index=False)
    has_fii = nifty_df["fii_composite"].notna().sum()
    print(f"\n[6] Nifty daily: {nifty_path.name}")
    print(f"    {len(nifty_df)} rows, {has_fii} with FII/PRO data")
    print(f"    FII View: {nifty_df['fii_view'].value_counts().to_dict()}")

    # 7. Write Sensex daily CSV
    sensex_path = REPO / "sensex-analysis" / "sensex_fii_t1_daily_results.csv"
    result_df.to_csv(sensex_path, index=False)
    print(f"\n[7] Sensex daily: {sensex_path.name}")
    print(f"    {len(result_df)} rows")

    print("\n" + "=" * 70)
    print("DONE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
