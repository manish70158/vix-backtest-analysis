#!/usr/bin/env python3
"""
Generate/update daily CSV files with FII/PRO data.

Fetches data from web sources (no PostgreSQL needed):
  - Nifty 50 OHLC from NSE (via yfinance ^NSEI)
  - Sensex OHLC from BSE (via yfinance ^BSESN)
  - India VIX from NSE (via yfinance ^INDIAVIX)
  - FII/PRO participant OI from NSE archives
  - BSE-specific participant OI from beta.bseindia.com

Reads existing CSVs and only fetches data for missing dates.

Updates:
  - vix_fii_t1_intraday_daily_results.csv
  - sensex-analysis/sensex_fii_t1_daily_results.csv
  - sensex-analysis/bse_fii_t1_daily.csv (BSE participant OI daily)
  - sensex-analysis/sensex_fii_t1_6year_expiry.csv (expiry-day rows for Thursdays)
"""

import json
import re
import time
import warnings
from math import sqrt
from pathlib import Path
from datetime import datetime, timedelta, date as dt_date
from zoneinfo import ZoneInfo

import pandas as pd
import requests
import yfinance as yf

warnings.filterwarnings("ignore")

IST = ZoneInfo("Asia/Kolkata")
REPO = Path(__file__).resolve().parent
CACHE_FILE = REPO / ".nse_oi_cache.json"
BSE_CACHE_FILE = REPO / ".bse_oi_cache.json"

NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.nseindia.com/',
}

BSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

BSE_URL = (
    "https://beta.bseindia.com/markets/Derivatives/"
    "DeriReports/DeriMarketDisclosures.aspx"
)


# ---------------------------------------------------------------------------
# Classification (same as build_full_6year_daily.py for consistency)
# ---------------------------------------------------------------------------
def determine_stance(prefix, fut_d, call_d, put_d):
    if fut_d is None or call_d is None or put_d is None:
        return None
    fut_d, call_d, put_d = float(fut_d), float(call_d), float(put_d)
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
    if val > 100000:
        return "Strong Bullish"
    elif val > 50000:
        return "Bullish"
    elif val > 30000:
        return "Mildly Bullish"
    elif val >= -30000:
        return "Neutral"
    elif val >= -50000:
        return "Mildly Bearish"
    elif val >= -100000:
        return "Bearish"
    else:
        return "Strong Bearish"


def determine_fii_direction(fut_d, call_d, put_d):
    """Simplified FII direction: Bullish/Bearish/Neutral."""
    if fut_d is None or call_d is None or put_d is None:
        return None
    net = float(fut_d) + float(call_d) - float(put_d)
    if net > 15000:
        return "Bullish"
    elif net < -15000:
        return "Bearish"
    return "Neutral"


# ---------------------------------------------------------------------------
# NSE Participant OI (cached)
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
    """Fetch participant-wise OI for a date from NSE archives."""
    date_str = date_obj.strftime('%d%m%Y')
    if date_str in cache:
        return cache[date_str]

    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{date_str}.csv"
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            cache[date_str] = None
            return None

        lines = r.text.strip().split('\n')
        if len(lines) < 4:
            cache[date_str] = None
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
                fut_long = int(parts[1]) if parts[1].strip() else 0
                fut_short = int(parts[2]) if parts[2].strip() else 0
            except ValueError:
                continue

            call_long = int(parts[5]) if parts[5].strip() else 0
            put_long = int(parts[6]) if parts[6].strip() else 0
            call_short = int(parts[7]) if parts[7].strip() else 0
            put_short = int(parts[8]) if parts[8].strip() else 0

            if 'FII' in category or 'FOREIGN' in category:
                data['fii_fut_idx_net'] = fut_long - fut_short
                data['fii_call_net'] = call_long - call_short
                data['fii_put_net'] = put_long - put_short
            if 'PRO' in category or 'PROPRIETARY' in category:
                data['pro_fut_idx_net'] = fut_long - fut_short
                data['pro_call_net'] = call_long - call_short
                data['pro_put_net'] = put_long - put_short

        result = data if 'fii_fut_idx_net' in data else None
        cache[date_str] = result
        return result
    except Exception:
        cache[date_str] = None
        return None


def find_prev_trading_day(date_obj, max_lookback=7):
    """Find previous weekday (rough proxy for trading day)."""
    d = date_obj - timedelta(days=1)
    for _ in range(max_lookback):
        if d.weekday() < 5:
            return d
        d -= timedelta(days=1)
    return None


# ---------------------------------------------------------------------------
# BSE Participant OI (cached)
# ---------------------------------------------------------------------------
def load_bse_cache():
    if BSE_CACHE_FILE.exists():
        with open(BSE_CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_bse_cache(cache):
    with open(BSE_CACHE_FILE, "w") as f:
        json.dump(cache, f)


def _parse_indian_num(s):
    """Parse Indian number format (1,23,456) to int."""
    s = s.strip().replace(",", "")
    if s == "-" or s == "":
        return 0
    return int(s)


def fetch_bse_participant_oi(bse_session, date_obj, bse_cache):
    """Fetch BSE participant OI for a date from beta.bseindia.com."""
    date_str = date_obj.strftime('%d%m%Y')
    if date_str in bse_cache:
        return bse_cache[date_str]

    try:
        r = bse_session.get(BSE_URL, timeout=20)
        if r.status_code != 200:
            bse_cache[date_str] = None
            return None

        html = r.text
        viewstate = re.search(r'__VIEWSTATE[^G][^>]*value="([^"]*)"', html)
        event_val = re.search(r'__EVENTVALIDATION[^>]*value="([^"]*)"', html)
        viewstate_gen = re.search(
            r'__VIEWSTATEGENERATOR[^>]*value="([^"]*)"', html
        )

        if not viewstate or not event_val:
            bse_cache[date_str] = None
            return None

        form_date = date_obj.strftime("%d/%m/%Y")
        form_data = {
            "__VIEWSTATE": viewstate.group(1),
            "__VIEWSTATEGENERATOR": (
                viewstate_gen.group(1) if viewstate_gen else ""
            ),
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": event_val.group(1),
            "ctl00$ContentPlaceHolder1$txtDate1": form_date,
            "ctl00$ContentPlaceHolder1$btnTradeArchives": "Submit",
        }

        r2 = bse_session.post(BSE_URL, data=form_data, timeout=20)
        if r2.status_code != 200:
            bse_cache[date_str] = None
            return None

        result = _parse_bse_oi_from_grid(r2.text)
        if result is None:
            result = _parse_bse_oi_from_html(r2.text)

        bse_cache[date_str] = result
        return result
    except Exception:
        bse_cache[date_str] = None
        return None


def _parse_bse_oi_from_grid(html):
    """Parse BSE OI from grvOpenInterst grid span IDs."""
    spans = dict(
        re.findall(
            r"ContentPlaceHolder1_grvOpenInterst_([^\"]+)\"[^>]*>([^<]+)",
            html,
        )
    )
    if "Label2_1" not in spans:
        return None

    data = {}
    for row_idx, prefix in [(1, "bse_fii"), (3, "bse_pro")]:
        fut_long = _parse_indian_num(spans.get(f"Label2_{row_idx}", "0"))
        fut_short = _parse_indian_num(spans.get(f"Label3_{row_idx}", "0"))
        call_long = _parse_indian_num(spans.get(f"Label6_{row_idx}", "0"))
        call_short = _parse_indian_num(
            spans.get(f"lblND_CL_SHRT_CNTRCTS_{row_idx}", "0")
        )
        put_long = _parse_indian_num(spans.get(f"Label7_{row_idx}", "0"))
        put_short = _parse_indian_num(spans.get(f"Label8_{row_idx}", "0"))

        data[f"{prefix}_fut_idx_net"] = fut_long - fut_short
        data[f"{prefix}_call_net"] = call_long - call_short
        data[f"{prefix}_put_net"] = put_long - put_short

    return data if "bse_fii_fut_idx_net" in data else None


def _parse_bse_oi_from_html(html):
    """Fallback: parse BSE OI from raw TD cells."""
    oi_start = html.find("Participant wise Open Interest")
    if oi_start == -1:
        return None

    oi_section = html[oi_start:oi_start + 20000]
    all_tds = re.findall(r"<td[^>]*>(.*?)</td>", oi_section, re.DOTALL)
    cleaned = [
        re.sub(r"<[^>]+>", "", td).strip().replace("&nbsp;", "")
        for td in all_tds
    ]
    cleaned = [c for c in cleaned if c.strip()]

    if len(cleaned) < 40:
        return None

    data = {}
    categories = {"FII": "bse_fii", "Proprietary": "bse_pro"}

    for cat_name, prefix in categories.items():
        if cat_name not in cleaned:
            continue
        idx = cleaned.index(cat_name) + 1
        values = cleaned[idx:idx + 14]

        try:
            data[f"{prefix}_fut_idx_net"] = (
                _parse_indian_num(values[0]) - _parse_indian_num(values[1])
            )
            data[f"{prefix}_call_net"] = (
                _parse_indian_num(values[4]) - _parse_indian_num(values[5])
            )
            data[f"{prefix}_put_net"] = (
                _parse_indian_num(values[6]) - _parse_indian_num(values[7])
            )
        except (IndexError, ValueError):
            continue

    return data if "bse_fii_fut_idx_net" in data else None


# ---------------------------------------------------------------------------
# Helpers for expiry CSV
# ---------------------------------------------------------------------------
def generate_chart_sparkline(open_price, high, low, close):
    """Generate a sparkline chart representation."""
    if not all([open_price, high, low, close]):
        return ""
    price_range = high - low
    if price_range == 0:
        return ""
    blocks = "\u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588"

    def to_block(price):
        idx = int((price - low) / price_range * 7)
        return blocks[min(idx, 7)]

    open_b = to_block(open_price)
    close_b = to_block(close)
    trend = "\U0001f4c8" if close > open_price else (
        "\U0001f4c9" if close < open_price else "\u27a1\ufe0f"
    )
    return f"{open_b}\u2193\u2581\u2191\u2588\u2193{close_b} {trend}"


def determine_expiry_type(date_obj):
    """Monthly if last Thursday of month, else weekly."""
    next_week = date_obj + timedelta(days=7)
    if next_week.month != date_obj.month:
        return "monthly"
    return "weekly"


# ---------------------------------------------------------------------------
# yfinance helpers
# ---------------------------------------------------------------------------
def flatten_yf_columns(df):
    """Flatten multi-level columns from yfinance if needed."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def yf_val(row, col):
    """Safely extract value from a yfinance row (handles multi-level)."""
    try:
        return float(row[col])
    except (KeyError, TypeError, ValueError):
        return None


def fetch_yfinance_data(start_date, end_date):
    """Fetch Nifty, Sensex, and VIX OHLC from yfinance."""
    end_str = str(end_date + timedelta(days=1))  # yfinance end is exclusive
    start_str = str(start_date)

    print(f"  Fetching ^NSEI (Nifty 50) ...")
    nifty = yf.download("^NSEI", start=start_str, end=end_str, progress=False)
    nifty = flatten_yf_columns(nifty)

    print(f"  Fetching ^BSESN (Sensex) ...")
    sensex = yf.download("^BSESN", start=start_str, end=end_str, progress=False)
    sensex = flatten_yf_columns(sensex)

    print(f"  Fetching ^INDIAVIX (India VIX) ...")
    vix = yf.download("^INDIAVIX", start=start_str, end=end_str, progress=False)
    vix = flatten_yf_columns(vix)

    print(f"  Got: Nifty={len(nifty)}, Sensex={len(sensex)}, VIX={len(vix)} days")
    return nifty, sensex, vix


def to_date_dict(df):
    """Convert yfinance DataFrame to {date: row} dict."""
    result = {}
    for idx, row in df.iterrows():
        d = idx.date() if hasattr(idx, 'date') else pd.Timestamp(idx).date()
        result[d] = row
    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("UPDATE DAILY CSV FILES")
    print("Nifty from NSE | Sensex from BSE | FII/PRO from NSE+BSE Archives")
    print(f"Date: {datetime.now(IST).strftime('%Y-%m-%d %H:%M IST')}")
    print("=" * 70)

    sensex_csv_path = REPO / "sensex-analysis" / "sensex_fii_t1_daily_results.csv"
    nifty_csv_path = REPO / "vix_fii_t1_intraday_daily_results.csv"
    bse_daily_csv_path = REPO / "sensex-analysis" / "bse_fii_t1_daily.csv"
    sensex_6year_csv_path = REPO / "sensex-analysis" / "sensex_fii_t1_6year_expiry.csv"

    # 1. Read existing data
    print("\n[1] Reading existing CSVs...")
    existing_sensex = pd.read_csv(sensex_csv_path)
    existing_nifty = pd.read_csv(nifty_csv_path)

    sensex_columns = list(existing_sensex.columns)
    nifty_columns = list(existing_nifty.columns)

    # BSE daily CSV (may be empty / header-only)
    if bse_daily_csv_path.exists():
        existing_bse_daily = pd.read_csv(bse_daily_csv_path)
        bse_daily_columns = list(existing_bse_daily.columns)
    else:
        existing_bse_daily = pd.DataFrame()
        bse_daily_columns = None

    # Sensex 6year expiry CSV
    existing_6year = pd.read_csv(sensex_6year_csv_path)
    sixyr_columns = list(existing_6year.columns)
    existing_6year_dates = set(existing_6year["date"].astype(str).values)

    last_date = pd.to_datetime(existing_sensex["date"]).max().date()
    today = datetime.now(IST).date()

    print(f"    Sensex daily: {len(existing_sensex)} rows, last: {last_date}")
    print(f"    Nifty daily:  {len(existing_nifty)} rows")
    print(f"    BSE daily:    {len(existing_bse_daily)} rows")
    print(f"    6year expiry: {len(existing_6year)} rows")
    print(f"    Today: {today}")

    if last_date >= today:
        print("\n    Already up to date!")
        return

    start_date = last_date + timedelta(days=1)

    # 2. Fetch OHLC from yfinance
    print(f"\n[2] Fetching OHLC from yfinance ({start_date} -> {today})...")
    nifty_yf, sensex_yf, vix_yf = fetch_yfinance_data(start_date, today)

    if nifty_yf.empty:
        print("\n    No new trading data available yet.")
        return

    sensex_dict = to_date_dict(sensex_yf)
    vix_dict = to_date_dict(vix_yf)

    # 3. Load expiry metadata from existing CSVs
    print("\n[3] Loading expiry metadata from CSVs...")
    nifty_exp = {}
    nifty_exp_path = REPO / "vix_fii_t1_intraday_expiry_results.csv"
    if nifty_exp_path.exists():
        nifty_exp_df = pd.read_csv(nifty_exp_path, parse_dates=["date"])
        for _, r in nifty_exp_df.iterrows():
            d = r["date"].date()
            nifty_exp[d] = {
                "expiry_type": r["expiry_type"],
                "vix_open": r.get("vix_open"),
                "vix_close": r.get("vix_close"),
            }

    sensex_exp = {}
    if sensex_6year_csv_path.exists():
        sensex_exp_df = pd.read_csv(sensex_6year_csv_path, parse_dates=["date"])
        for _, r in sensex_exp_df.iterrows():
            d = r["date"].date()
            sensex_exp[d] = {
                "expiry_type": r["expiry_type"],
                "sensex_open": r.get("sensex_open"),
                "sensex_high": r.get("sensex_high"),
                "sensex_low": r.get("sensex_low"),
                "sensex_close": r.get("sensex_close"),
                "vix_open": r.get("vix_open"),
                "vix_close": r.get("vix_close"),
            }

    print(f"    Nifty expiry dates: {len(nifty_exp)}, Sensex: {len(sensex_exp)}")

    # 4. Fetch FII/PRO participant OI from NSE archives
    print("\n[4] Fetching FII/PRO OI from NSE archives...")
    cache = load_cache()
    session = requests.Session()
    session.headers.update(NSE_HEADERS)

    new_dates = sorted([
        idx.date() if hasattr(idx, 'date') else pd.Timestamp(idx).date()
        for idx in nifty_yf.index
    ])

    # Collect T-1 and T-2 dates needed for daily change computation
    dates_needed = set()
    for d in new_dates:
        dt_obj = datetime.combine(d, datetime.min.time())
        t1 = find_prev_trading_day(dt_obj)
        if t1:
            t1d = t1.date() if isinstance(t1, datetime) else t1
            dates_needed.add(t1d)
            t2 = find_prev_trading_day(t1)
            if t2:
                t2d = t2.date() if isinstance(t2, datetime) else t2
                dates_needed.add(t2d)

    to_fetch = [d for d in sorted(dates_needed)
                if d.strftime('%d%m%Y') not in cache]
    print(f"    Need OI for {len(dates_needed)} dates, "
          f"{len(to_fetch)} to fetch from NSE")

    for i, d in enumerate(to_fetch):
        dt_obj = datetime.combine(d, datetime.min.time())
        fetch_participant_oi(session, dt_obj, cache)
        time.sleep(0.7)
        if (i + 1) % 5 == 0:
            save_cache(cache)
            print(f"    [{i + 1}/{len(to_fetch)}] fetched")
    if to_fetch:
        save_cache(cache)
        print(f"    Done — fetched {len(to_fetch)} dates")

    # 5. Fetch BSE participant OI from beta.bseindia.com
    print("\n[5] Fetching BSE participant OI from beta.bseindia.com...")
    bse_cache = load_bse_cache()
    bse_session = requests.Session()
    bse_session.headers.update(BSE_HEADERS)

    bse_to_fetch = [d for d in sorted(dates_needed)
                    if d.strftime('%d%m%Y') not in bse_cache]
    print(f"    Need BSE OI for {len(dates_needed)} dates, "
          f"{len(bse_to_fetch)} to fetch")

    bse_ok_count = 0
    for i, d in enumerate(bse_to_fetch):
        dt_obj = datetime.combine(d, datetime.min.time())
        result = fetch_bse_participant_oi(bse_session, dt_obj, bse_cache)
        if result:
            bse_ok_count += 1
        time.sleep(1.5)  # BSE is slower, be gentler
        if (i + 1) % 3 == 0:
            save_bse_cache(bse_cache)
            print(f"    [{i + 1}/{len(bse_to_fetch)}] fetched from BSE "
                  f"({bse_ok_count} OK)")
    if bse_to_fetch:
        save_bse_cache(bse_cache)
        print(f"    Done — fetched {len(bse_to_fetch)} from BSE "
              f"({bse_ok_count} with data)")

    # 6. Build new rows
    print(f"\n[6] Building {len(new_dates)} new rows...")
    new_nifty_rows = []
    new_sensex_rows = []
    new_bse_rows = []
    new_6year_rows = []
    fii_ok = 0
    bse_daily_ok = 0

    for idx, row in nifty_yf.iterrows():
        d = idx.date() if hasattr(idx, 'date') else pd.Timestamp(idx).date()

        o = round(float(row["Open"]), 2)
        h = round(float(row["High"]), 2)
        l = round(float(row["Low"]), 2)
        c = round(float(row["Close"]), 2)

        actual_range_pct = round((h - l) / o * 100, 2)
        actual_oc_pct = round((c - o) / o * 100, 2)
        intraday_high_pct = round((h - o) / o * 100, 2)
        intraday_low_pct = round((l - o) / o * 100, 2)
        move_direction = ("Top to Down" if o > c
                          else ("Down to Up" if o < c else "Flat"))

        # Expiry info
        nex = nifty_exp.get(d)
        sxe = sensex_exp.get(d)
        is_nifty_expiry = 1 if nex else 0
        is_sensex_expiry = 1 if sxe else 0
        expiry_type = (nex["expiry_type"] if nex
                       else (sxe["expiry_type"] if sxe else None))

        # VIX — prefer expiry CSV value, fallback to yfinance on expiry days
        vix_open_val = None
        vix_close_val = None
        if nex and nex.get("vix_open") is not None and not pd.isna(nex["vix_open"]):
            vix_open_val = round(float(nex["vix_open"]), 2)
            vix_close_val = round(float(nex["vix_close"]), 2)
        elif sxe and sxe.get("vix_open") is not None and not pd.isna(sxe["vix_open"]):
            vix_open_val = round(float(sxe["vix_open"]), 2)
            vix_close_val = round(float(sxe["vix_close"]), 2)
        elif (is_nifty_expiry or is_sensex_expiry) and d in vix_dict:
            vx = vix_dict[d]
            vo = yf_val(vx, "Open")
            vc = yf_val(vx, "Close")
            if vo is not None:
                vix_open_val = round(vo, 2)
            if vc is not None:
                vix_close_val = round(vc, 2)

        # VIX for all days (used in BSE daily CSV)
        vix_open_all = None
        vix_close_all = None
        if d in vix_dict:
            vx = vix_dict[d]
            vo = yf_val(vx, "Open")
            vc = yf_val(vx, "Close")
            if vo is not None:
                vix_open_all = round(vo, 2)
            if vc is not None:
                vix_close_all = round(vc, 2)

        # Sensex OHLC — prefer expiry CSV, fallback to yfinance
        sx_open = sx_high = sx_low = sx_close = None
        if sxe and sxe.get("sensex_open") is not None:
            sx_open = round(float(sxe["sensex_open"]), 2)
            sx_high = round(float(sxe["sensex_high"]), 2)
            sx_low = round(float(sxe["sensex_low"]), 2)
            sx_close = round(float(sxe["sensex_close"]), 2)
        elif d in sensex_dict:
            sx = sensex_dict[d]
            sx_open = round(yf_val(sx, "Open"), 2) if yf_val(sx, "Open") else None
            sx_high = round(yf_val(sx, "High"), 2) if yf_val(sx, "High") else None
            sx_low = round(yf_val(sx, "Low"), 2) if yf_val(sx, "Low") else None
            sx_close = round(yf_val(sx, "Close"), 2) if yf_val(sx, "Close") else None

        # NSE FII/PRO T-1 daily change (T-1 minus T-2 OI)
        dt_obj = datetime.combine(d, datetime.min.time())
        t1 = find_prev_trading_day(dt_obj)
        t2 = find_prev_trading_day(t1) if t1 else None

        fii_fut_d = fii_call_d = fii_put_d = None
        pro_fut_d = pro_call_d = pro_put_d = None

        if t1 and t2:
            t1_key = (t1.date() if isinstance(t1, datetime) else t1).strftime('%d%m%Y')
            t2_key = (t2.date() if isinstance(t2, datetime) else t2).strftime('%d%m%Y')
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
                fii_ok += 1

        fii_stance = determine_stance("FII", fii_fut_d, fii_call_d, fii_put_d)
        pro_stance = determine_stance("PRO", pro_fut_d, pro_call_d, pro_put_d)
        fii_comp = (int(fii_fut_d + fii_call_d - fii_put_d)
                    if fii_fut_d is not None else None)
        pro_comp = (int(pro_fut_d + pro_call_d - pro_put_d)
                    if pro_fut_d is not None else None)

        # BSE FII/PRO T-1 daily change
        bse_fii_fut_d = bse_fii_call_d = bse_fii_put_d = None
        bse_pro_fut_d = bse_pro_call_d = bse_pro_put_d = None

        if t1 and t2:
            bse_t1_data = bse_cache.get(t1_key)
            bse_t2_data = bse_cache.get(t2_key)

            if bse_t1_data and bse_t2_data:
                bse_fii_fut_d = (
                    bse_t1_data["bse_fii_fut_idx_net"]
                    - bse_t2_data["bse_fii_fut_idx_net"]
                )
                bse_fii_call_d = (
                    bse_t1_data["bse_fii_call_net"]
                    - bse_t2_data["bse_fii_call_net"]
                )
                bse_fii_put_d = (
                    bse_t1_data["bse_fii_put_net"]
                    - bse_t2_data["bse_fii_put_net"]
                )
                bse_pro_fut_d = (
                    bse_t1_data.get("bse_pro_fut_idx_net", 0)
                    - bse_t2_data.get("bse_pro_fut_idx_net", 0)
                )
                bse_pro_call_d = (
                    bse_t1_data.get("bse_pro_call_net", 0)
                    - bse_t2_data.get("bse_pro_call_net", 0)
                )
                bse_pro_put_d = (
                    bse_t1_data.get("bse_pro_put_net", 0)
                    - bse_t2_data.get("bse_pro_put_net", 0)
                )
                bse_daily_ok += 1

        bse_fii_comp = (
            int(bse_fii_fut_d + bse_fii_call_d - bse_fii_put_d)
            if bse_fii_fut_d is not None else None
        )
        bse_pro_comp = (
            int(bse_pro_fut_d + bse_pro_call_d - bse_pro_put_d)
            if bse_pro_fut_d is not None else None
        )

        # ----- Nifty daily row -----
        new_nifty_rows.append({
            "date": str(d),
            "day_of_week": d.strftime("%A"),
            "is_nifty_expiry": is_nifty_expiry,
            "expiry_type": expiry_type,
            "nifty_open": o,
            "nifty_high": h,
            "nifty_low": l,
            "nifty_close": c,
            "actual_range_pct": actual_range_pct,
            "actual_open_close_pct": actual_oc_pct,
            "intraday_high_pct": intraday_high_pct,
            "intraday_low_pct": intraday_low_pct,
            "move_direction": move_direction,
            "vix_open": vix_open_val,
            "vix_close": vix_close_val,
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

        # ----- Sensex daily row -----
        new_sensex_rows.append({
            "date": str(d),
            "day_of_week": d.strftime("%A"),
            "is_nifty_expiry": is_nifty_expiry,
            "is_sensex_expiry": is_sensex_expiry,
            "expiry_type": expiry_type,
            "nifty_open": o,
            "nifty_high": h,
            "nifty_low": l,
            "nifty_close": c,
            "sensex_open": sx_open,
            "sensex_high": sx_high,
            "sensex_low": sx_low,
            "sensex_close": sx_close,
            "actual_range_pct": actual_range_pct,
            "actual_open_close_pct": actual_oc_pct,
            "intraday_high_pct": intraday_high_pct,
            "intraday_low_pct": intraday_low_pct,
            "move_direction": move_direction,
            "vix_open": vix_open_val,
            "vix_close": vix_close_val,
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

        # ----- BSE daily row -----
        sx_range_pct = (
            round((sx_high - sx_low) / sx_open * 100, 2)
            if sx_open and sx_high and sx_low else None
        )
        sx_oc_pct = (
            round((sx_close - sx_open) / sx_open * 100, 2)
            if sx_open and sx_close else None
        )
        sx_move = "Flat"
        if sx_open and sx_close:
            sx_move = ("Top to Down" if sx_open > sx_close
                       else ("Down to Up" if sx_open < sx_close else "Flat"))

        new_bse_rows.append({
            "date": str(d),
            "day_of_week": d.strftime("%A"),
            "sensex_open": sx_open,
            "sensex_high": sx_high,
            "sensex_low": sx_low,
            "sensex_close": sx_close,
            "actual_range_pct": sx_range_pct,
            "actual_open_close_pct": sx_oc_pct,
            "move_direction": sx_move,
            "vix_open": vix_open_all,
            "vix_close": vix_close_all,
            "bse_fii_fut_daily": (
                int(bse_fii_fut_d) if bse_fii_fut_d is not None else None
            ),
            "bse_fii_call_daily": (
                int(bse_fii_call_d) if bse_fii_call_d is not None else None
            ),
            "bse_fii_put_daily": (
                int(bse_fii_put_d) if bse_fii_put_d is not None else None
            ),
            "bse_fii_stance": determine_stance(
                "FII", bse_fii_fut_d, bse_fii_call_d, bse_fii_put_d
            ),
            "bse_fii_composite": bse_fii_comp,
            "bse_fii_view": classify_view(bse_fii_comp),
            "bse_pro_fut_daily": (
                int(bse_pro_fut_d) if bse_pro_fut_d is not None else None
            ),
            "bse_pro_call_daily": (
                int(bse_pro_call_d) if bse_pro_call_d is not None else None
            ),
            "bse_pro_put_daily": (
                int(bse_pro_put_d) if bse_pro_put_d is not None else None
            ),
            "bse_pro_stance": determine_stance(
                "PRO", bse_pro_fut_d, bse_pro_call_d, bse_pro_put_d
            ),
            "bse_pro_composite": bse_pro_comp,
            "bse_pro_view": classify_view(bse_pro_comp),
        })

        # ----- 6year expiry row (Thursdays only) -----
        if d.weekday() == 3 and str(d) not in existing_6year_dates:
            # VIX for expiry — use all-day VIX or expiry VIX
            vix_o = vix_open_val if vix_open_val else vix_open_all
            vix_c = vix_close_val if vix_close_val else vix_close_all

            # VIX metrics
            vix_pred = (
                round(vix_o / sqrt(252), 2) if vix_o else None
            )
            sx_range_exp = (
                round((sx_high - sx_low) / sx_open * 100, 2)
                if sx_open and sx_high and sx_low else None
            )
            sx_oc_exp = (
                round((sx_close - sx_open) / sx_open * 100, 2)
                if sx_open and sx_close else None
            )
            sx_hi_exp = (
                round((sx_high - sx_open) / sx_open * 100, 2)
                if sx_open and sx_high else None
            )
            sx_lo_exp = (
                round((sx_low - sx_open) / sx_open * 100, 2)
                if sx_open and sx_low else None
            )
            rvr = (
                round(sx_range_exp / vix_pred, 2)
                if vix_pred and sx_range_exp else None
            )
            diff = (
                round(sx_range_exp - vix_pred, 2)
                if vix_pred is not None and sx_range_exp is not None
                else None
            )
            accuracy = None
            if vix_pred and sx_range_exp:
                accuracy = ("Underestimated" if sx_range_exp > vix_pred
                            else "Overestimated")

            chart = generate_chart_sparkline(sx_open, sx_high, sx_low, sx_close)
            exp_type = determine_expiry_type(d)
            fii_dir = determine_fii_direction(
                fii_fut_d, fii_call_d, fii_put_d
            )

            new_6year_rows.append({
                "date": str(d),
                "day_of_week": d.strftime("%A"),
                "expiry_type": exp_type,
                "chart": chart,
                "sensex_open": sx_open,
                "sensex_high": sx_high,
                "sensex_low": sx_low,
                "sensex_close": sx_close,
                "vix_open": vix_o,
                "vix_close": vix_c,
                "vix_predicted_move_pct": vix_pred,
                "actual_range_pct": sx_range_exp,
                "actual_open_close_pct": sx_oc_exp,
                "intraday_high_pct": sx_hi_exp,
                "intraday_low_pct": sx_lo_exp,
                "range_vs_vix_ratio": rvr,
                "diff_pct": diff,
                "vix_accuracy": accuracy,
                "t1_fii_fut_daily": (
                    int(fii_fut_d) if fii_fut_d is not None else None
                ),
                "t1_fii_call_daily": (
                    int(fii_call_d) if fii_call_d is not None else None
                ),
                "t1_fii_put_daily": (
                    int(fii_put_d) if fii_put_d is not None else None
                ),
                "t1_fii_stance": fii_stance,
                "t1_fii_direction": fii_dir,
                "t1_pro_fut_daily": (
                    int(pro_fut_d) if pro_fut_d is not None else None
                ),
                "t1_pro_call_daily": (
                    int(pro_call_d) if pro_call_d is not None else None
                ),
                "t1_pro_put_daily": (
                    int(pro_put_d) if pro_put_d is not None else None
                ),
                "t1_pro_stance": pro_stance,
                "is_nifty_expiry_day": 1,
                "bse_fii_fut_daily": (
                    int(bse_fii_fut_d) if bse_fii_fut_d is not None else ""
                ),
                "bse_fii_call_daily": (
                    int(bse_fii_call_d) if bse_fii_call_d is not None else ""
                ),
                "bse_fii_put_daily": (
                    int(bse_fii_put_d) if bse_fii_put_d is not None else ""
                ),
                "bse_pro_fut_daily": (
                    int(bse_pro_fut_d) if bse_pro_fut_d is not None else ""
                ),
                "bse_pro_call_daily": (
                    int(bse_pro_call_d) if bse_pro_call_d is not None else ""
                ),
                "bse_pro_put_daily": (
                    int(bse_pro_put_d) if bse_pro_put_d is not None else ""
                ),
                "fii_composite": fii_comp,
                "pro_composite": pro_comp,
                "fii_view": classify_view(fii_comp),
                "pro_view": classify_view(pro_comp),
            })

    print(f"    Built {len(new_nifty_rows)} rows, {fii_ok} with NSE FII/PRO, "
          f"{bse_daily_ok} with BSE data")
    if new_6year_rows:
        print(f"    New expiry rows for 6year CSV: {len(new_6year_rows)}")

    # 7. Write updated CSVs
    print("\n[7] Writing updated CSVs...")

    # Nifty daily
    new_nifty_df = pd.DataFrame(new_nifty_rows)
    updated_nifty = pd.concat([existing_nifty, new_nifty_df], ignore_index=True)
    updated_nifty = updated_nifty[nifty_columns]
    updated_nifty.to_csv(nifty_csv_path, index=False)
    print(f"    Nifty:      {nifty_csv_path.name} — {len(updated_nifty)} rows "
          f"(+{len(new_nifty_df)} new)")

    # Sensex daily
    new_sensex_df = pd.DataFrame(new_sensex_rows)
    updated_sensex = pd.concat(
        [existing_sensex, new_sensex_df], ignore_index=True
    )
    updated_sensex = updated_sensex[sensex_columns]
    updated_sensex.to_csv(sensex_csv_path, index=False)
    print(f"    Sensex:     {sensex_csv_path.name} — {len(updated_sensex)} rows "
          f"(+{len(new_sensex_df)} new)")

    # BSE daily
    if new_bse_rows:
        new_bse_df = pd.DataFrame(new_bse_rows)
        if not existing_bse_daily.empty:
            updated_bse = pd.concat(
                [existing_bse_daily, new_bse_df], ignore_index=True
            )
            updated_bse = updated_bse[bse_daily_columns]
        else:
            updated_bse = new_bse_df
        updated_bse.to_csv(bse_daily_csv_path, index=False)
        print(f"    BSE daily:  {bse_daily_csv_path.name} — "
              f"{len(updated_bse)} rows (+{len(new_bse_df)} new)")

    # 6year expiry CSV
    if new_6year_rows:
        new_6year_df = pd.DataFrame(new_6year_rows)
        # Deduplicate (shouldn't happen, but be safe)
        new_6year_df = new_6year_df[
            ~new_6year_df["date"].isin(existing_6year_dates)
        ]
        if not new_6year_df.empty:
            updated_6year = pd.concat(
                [existing_6year, new_6year_df], ignore_index=True
            )
            updated_6year = updated_6year[sixyr_columns]
            updated_6year.to_csv(sensex_6year_csv_path, index=False)
            print(f"    6year:      {sensex_6year_csv_path.name} — "
                  f"{len(updated_6year)} rows (+{len(new_6year_df)} expiry)")

    # Summary
    print("\n" + "=" * 70)
    last_new = new_dates[-1]
    print(f"DONE! Updated through {last_new}")
    print(f"  New rows added: {len(new_nifty_rows)}")
    print(f"  With NSE FII/PRO data: {fii_ok}")
    print(f"  With BSE FII/PRO data: {bse_daily_ok}")
    if new_6year_rows:
        print(f"  New expiry rows (6year): {len(new_6year_rows)}")
    if fii_ok < len(new_nifty_rows):
        print(f"  Missing NSE FII/PRO: {len(new_nifty_rows) - fii_ok} "
              f"(archive may not have latest data yet)")
    if bse_daily_ok < len(new_nifty_rows):
        print(f"  Missing BSE data: {len(new_nifty_rows) - bse_daily_ok} "
              f"(BSE website may be unavailable)")
    print("=" * 70)


if __name__ == "__main__":
    main()
