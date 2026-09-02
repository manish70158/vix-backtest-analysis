#!/usr/bin/env python3
"""
Weekly Sensex Expiry Data Updater

Automated script run by GitHub Actions to update sensex_fii_t1_6year_expiry.csv weekly.

Data Sources:
  - NSE Archives: Aggregate F&O participant OI (for daily change computation, T1-T2)
  - BSE (beta.bseindia.com): BSE-specific participant OI (absolute net positions)
  - Yahoo Finance: Sensex OHLC + India VIX

Phase 1 (pre_expiry - Wednesday 9 PM IST):
  - Fetches T-1 (Wednesday) and T-2 (Tuesday) FII/PRO participant OI from NSE
  - Fetches T-1 BSE-specific participant OI from beta.bseindia.com
  - Computes daily changes, stance, direction
  - Appends a new row with FII/PRO columns filled, Sensex OHLC/VIX empty

Phase 2 (post_expiry - Thursday 7 PM IST):
  - Fetches Thursday's Sensex OHLC from Yahoo Finance
  - Fetches India VIX open/close from Yahoo Finance
  - Computes VIX predicted move, actual range, accuracy metrics
  - Updates the last row of the CSV with market data

Usage:
  python update_weekly_expiry.py --phase pre_expiry
  python update_weekly_expiry.py --phase post_expiry
"""

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf

SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "sensex_fii_t1_6year_expiry.csv"

NSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}

BSE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

BSE_URL = "https://beta.bseindia.com/markets/Derivatives/DeriReports/DeriMarketDisclosures.aspx"


def find_prev_trading_day(date, max_lookback=7):
    """Find previous trading day (skip weekends)."""
    d = date - timedelta(days=1)
    for _ in range(max_lookback):
        if d.weekday() < 5:
            return d
        d -= timedelta(days=1)
    return None


def fetch_participant_oi(session, date):
    """Fetch participant-wise OI for a date from NSE archives."""
    date_str = date.strftime("%d%m%Y")
    url = f"https://archives.nseindia.com/content/nsccl/fao_participant_oi_{date_str}.csv"

    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return None

        lines = r.text.strip().split("\n")
        if len(lines) < 4:
            return None

        data = {}
        for line in lines[2:]:
            parts = [p.strip().replace('"', '').strip() for p in line.split(",")]
            if len(parts) < 9:
                continue
            category = parts[0].strip().upper()
            if category == "TOTAL":
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

            if "FII" in category or "FOREIGN" in category:
                data["fii_fut_idx_net"] = fut_idx_long - fut_idx_short
                data["fii_call_net"] = opt_call_long - opt_call_short
                data["fii_put_net"] = opt_put_long - opt_put_short

            if "PRO" in category or "PROPRIETARY" in category:
                data["pro_fut_idx_net"] = fut_idx_long - fut_idx_short
                data["pro_call_net"] = opt_call_long - opt_call_short
                data["pro_put_net"] = opt_put_long - opt_put_short

        return data if "fii_fut_idx_net" in data else None

    except Exception as e:
        print(f"  Error fetching NSE data for {date}: {e}")
        return None


def _parse_indian_num(s):
    """Parse Indian number format (1,23,456) to int."""
    s = s.strip().replace(",", "")
    if s == "-" or s == "":
        return 0
    return int(s)


def fetch_bse_participant_oi(date=None):
    """
    Fetch BSE-specific participant-wise OI from beta.bseindia.com.
    Supports historical dates via ASP.NET form postback.

    Args:
        date: datetime object for the date to fetch. If None, fetches latest.

    Returns dict with keys:
      bse_fii_fut_idx_net, bse_fii_call_net, bse_fii_put_net,
      bse_pro_fut_idx_net, bse_pro_call_net, bse_pro_put_net
    or None on failure.
    """
    try:
        session = requests.Session()
        session.headers.update(BSE_HEADERS)

        # GET page for ASP.NET form tokens
        r = session.get(BSE_URL, timeout=20)
        if r.status_code != 200:
            print(f"  BSE fetch failed with status {r.status_code}")
            return None

        html = r.text

        # If no specific date requested, parse data from initial GET response
        if date is None:
            return _parse_bse_oi_from_html(html)

        # For specific dates, POST with form tokens
        viewstate = re.search(r"__VIEWSTATE[^G][^>]*value=\"([^\"]*)\"", html)
        event_val = re.search(r"__EVENTVALIDATION[^>]*value=\"([^\"]*)\"", html)
        viewstate_gen = re.search(r"__VIEWSTATEGENERATOR[^>]*value=\"([^\"]*)\"", html)

        if not viewstate or not event_val:
            print("  BSE: Could not extract form tokens")
            return _parse_bse_oi_from_html(html)

        date_str = date.strftime("%d/%m/%Y")
        form_data = {
            "__VIEWSTATE": viewstate.group(1),
            "__VIEWSTATEGENERATOR": viewstate_gen.group(1) if viewstate_gen else "",
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": event_val.group(1),
            "ctl00$ContentPlaceHolder1$txtDate1": date_str,
            "ctl00$ContentPlaceHolder1$btnTradeArchives": "Submit",
        }

        r2 = session.post(BSE_URL, data=form_data, timeout=20)
        if r2.status_code != 200:
            print(f"  BSE POST failed with status {r2.status_code}")
            return None

        return _parse_bse_oi_from_grid(r2.text)

    except Exception as e:
        print(f"  BSE fetch error: {e}")
        return None


def _parse_bse_oi_from_grid(html):
    """Parse BSE OI data from grvOpenInterst grid span IDs."""
    spans = dict(
        re.findall(r"ContentPlaceHolder1_grvOpenInterst_([^\"]+)\"[^>]*>([^<]+)", html)
    )

    if "Label2_1" not in spans:
        # Fallback to TD-based parsing
        return _parse_bse_oi_from_html(html)

    data = {}
    # Row 1 = FII, Row 3 = Proprietary
    # Column mapping (from header colspan + span ID names):
    #   Label2=IdxFutLong, Label3=IdxFutShort,
    #   Label4=StkFutLong, Label5=StkFutShort,
    #   Label6=IdxOptCallLong, Label7=IdxOptPutLong,
    #   lblND_CL_SHRT_CNTRCTS=IdxOptCallShort, Label8=IdxOptPutShort
    for row_idx, prefix in [(1, "bse_fii"), (3, "bse_pro")]:
        fut_long = _parse_indian_num(spans.get(f"Label2_{row_idx}", "0"))
        fut_short = _parse_indian_num(spans.get(f"Label3_{row_idx}", "0"))
        call_long = _parse_indian_num(spans.get(f"Label6_{row_idx}", "0"))
        call_short = _parse_indian_num(spans.get(f"lblND_CL_SHRT_CNTRCTS_{row_idx}", "0"))
        put_long = _parse_indian_num(spans.get(f"Label7_{row_idx}", "0"))
        put_short = _parse_indian_num(spans.get(f"Label8_{row_idx}", "0"))

        data[f"{prefix}_fut_idx_net"] = fut_long - fut_short
        data[f"{prefix}_call_net"] = call_long - call_short
        data[f"{prefix}_put_net"] = put_long - put_short

    return data if "bse_fii_fut_idx_net" in data else None


def _parse_bse_oi_from_html(html):
    """Fallback: Parse BSE OI data from raw TD cells."""
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
            fut_idx_long = _parse_indian_num(values[0])
            fut_idx_short = _parse_indian_num(values[1])
            call_long = _parse_indian_num(values[4])
            call_short = _parse_indian_num(values[5])
            put_long = _parse_indian_num(values[6])
            put_short = _parse_indian_num(values[7])

            data[f"{prefix}_fut_idx_net"] = fut_idx_long - fut_idx_short
            data[f"{prefix}_call_net"] = call_long - call_short
            data[f"{prefix}_put_net"] = put_long - put_short
        except (IndexError, ValueError) as e:
            print(f"  BSE: Error parsing {cat_name} data: {e}")
            continue

    return data if "bse_fii_fut_idx_net" in data else None


def determine_fii_stance(fut_daily, call_daily, put_daily):
    """Determine FII stance from T-1 daily changes."""
    if fut_daily > 10000 and put_daily < -20000:
        return "FII Bullish (bought fut + sold puts)"
    elif fut_daily < -10000 and put_daily > 20000:
        return "FII Very Bearish (sold fut >10K + bought puts >20K)"
    elif fut_daily < -10000:
        return "FII Bearish (sold fut >10K)"
    elif put_daily > 20000:
        return "FII Hedging (bought puts >20K)"
    elif put_daily < -20000:
        return "FII Confident (sold puts >20K)"
    elif fut_daily > 10000:
        return "FII Mildly Bullish"
    elif call_daily < -20000:
        return "FII Mildly Bearish"
    else:
        return "FII Neutral"


def determine_pro_stance(fut_daily, call_daily, put_daily):
    """Determine PRO stance from T-1 daily changes."""
    if fut_daily > 10000 and put_daily < -20000:
        return "PRO Bullish (bought fut + sold puts)"
    elif fut_daily < -10000 and put_daily > 20000:
        return "PRO Very Bearish (sold fut >10K + bought puts >20K)"
    elif fut_daily < -10000:
        return "PRO Bearish (sold fut >10K)"
    elif put_daily > 20000:
        return "PRO Hedging (bought puts >20K)"
    elif put_daily < -20000:
        return "PRO Confident (sold puts >20K)"
    elif fut_daily > 10000:
        return "PRO Mildly Bullish"
    elif call_daily < -20000:
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


def generate_chart_sparkline(open_price, high, low, close):
    """Generate a sparkline chart representation."""
    if not all([open_price, high, low, close]):
        return ""

    price_range = high - low
    if price_range == 0:
        return ""

    blocks = "▁▂▃▄▅▆▇█"

    def to_block(price):
        idx = int((price - low) / price_range * 7)
        return blocks[min(idx, 7)]

    open_b = to_block(open_price)
    high_b = "█"
    low_b = "▁"
    close_b = to_block(close)

    trend = "📈" if close > open_price else "📉" if close < open_price else "➡️"
    return f"{open_b}↓{low_b}↑{high_b}↓{close_b} {trend}"


def determine_expiry_type(date):
    """Determine if this is a weekly or monthly expiry."""
    # Monthly expiry = last Thursday of the month
    next_week = date + timedelta(days=7)
    if next_week.month != date.month:
        return "monthly"
    return "weekly"


def get_next_thursday(from_date=None):
    """Get the next Thursday from a given date (or today)."""
    if from_date is None:
        from_date = datetime.now()
    days_ahead = 3 - from_date.weekday()  # Thursday = 3
    if days_ahead <= 0:
        days_ahead += 7
    return from_date + timedelta(days=days_ahead)


def run_pre_expiry():
    """Phase 1: Add new row with FII/PRO T-1 data (run on Wednesday or Thursday)."""
    print("=" * 60)
    print("PHASE 1: PRE-EXPIRY")
    print("=" * 60)

    today = datetime.now()
    # Determine the expiry date (Thursday)
    if today.weekday() == 3:  # Thursday — expiry is today
        expiry_date = today
    elif today.weekday() == 2:  # Wednesday — expiry is tomorrow
        expiry_date = today + timedelta(days=1)
    else:
        # For manual runs on other days, find the nearest Thursday
        # (upcoming if Mon/Tue, most recent if Fri/Sat/Sun)
        days_to_thu = (3 - today.weekday()) % 7
        if days_to_thu == 0:
            days_to_thu = 7
        expiry_date = today + timedelta(days=days_to_thu)

    # T-1 = day before expiry (typically Wednesday)
    t1_date = find_prev_trading_day(expiry_date)
    t2_date = find_prev_trading_day(t1_date)

    print(f"  Expiry date (Thursday): {expiry_date.strftime('%Y-%m-%d')}")
    print(f"  T-1 date: {t1_date.strftime('%Y-%m-%d')}")
    print(f"  T-2 date: {t2_date.strftime('%Y-%m-%d')}")

    # Load CSV
    df = pd.read_csv(CSV_PATH)

    # Check if this expiry already exists
    expiry_str = expiry_date.strftime("%Y-%m-%d")
    if expiry_str in df["date"].values:
        print(f"  WARNING: Expiry {expiry_str} already exists in CSV. Skipping.")
        return

    # Fetch participant data from NSE
    print("\n  Fetching NSE participant OI data...")
    session = requests.Session()
    session.headers.update(NSE_HEADERS)

    t1_data = fetch_participant_oi(session, t1_date)
    if t1_data is None:
        # Try previous day if T-1 is a holiday
        alt_t1 = find_prev_trading_day(t1_date)
        if alt_t1:
            print(f"  T-1 ({t1_date.date()}) unavailable, trying {alt_t1.date()}...")
            t1_data = fetch_participant_oi(session, alt_t1)
            t1_date = alt_t1
            # Recompute T-2 based on resolved T-1
            t2_date = find_prev_trading_day(t1_date)
            print(f"  T-2 recomputed: {t2_date.strftime('%Y-%m-%d')}")

    t2_data = fetch_participant_oi(session, t2_date)
    if t2_data is None:
        alt_t2 = find_prev_trading_day(t2_date)
        if alt_t2:
            print(f"  T-2 ({t2_date.date()}) unavailable, trying {alt_t2.date()}...")
            t2_data = fetch_participant_oi(session, alt_t2)

    if t1_data is None or t2_data is None:
        print("  ERROR: Could not fetch participant data from NSE.")
        print(f"    T-1 data: {'OK' if t1_data else 'FAILED'}")
        print(f"    T-2 data: {'OK' if t2_data else 'FAILED'}")
        sys.exit(1)

    # Compute daily changes
    fii_fut_d = t1_data["fii_fut_idx_net"] - t2_data["fii_fut_idx_net"]
    fii_call_d = t1_data["fii_call_net"] - t2_data["fii_call_net"]
    fii_put_d = t1_data["fii_put_net"] - t2_data["fii_put_net"]

    pro_fut_d = (t1_data.get("pro_fut_idx_net", 0) - t2_data.get("pro_fut_idx_net", 0))
    pro_call_d = (t1_data.get("pro_call_net", 0) - t2_data.get("pro_call_net", 0))
    pro_put_d = (t1_data.get("pro_put_net", 0) - t2_data.get("pro_put_net", 0))

    fii_stance = determine_fii_stance(fii_fut_d, fii_call_d, fii_put_d)
    fii_direction = determine_fii_direction(fii_fut_d, fii_call_d, fii_put_d)
    pro_stance = determine_pro_stance(pro_fut_d, pro_call_d, pro_put_d)

    print(f"\n  [NSE] FII: fut={fii_fut_d:+,} call={fii_call_d:+,} put={fii_put_d:+,}")
    print(f"  [NSE] FII Stance: {fii_stance}")
    print(f"  [NSE] FII Direction: {fii_direction}")
    print(f"  [NSE] PRO: fut={pro_fut_d:+,} call={pro_call_d:+,} put={pro_put_d:+,}")
    print(f"  [NSE] PRO Stance: {pro_stance}")

    # Fetch BSE-specific participant data (daily change = T1 - T2)
    print(f"\n  Fetching BSE participant OI (Sensex-specific)...")
    print(f"    T-1: {t1_date.date()}, T-2: {t2_date.date()}")
    bse_t1 = fetch_bse_participant_oi(date=t1_date)
    bse_t2 = fetch_bse_participant_oi(date=t2_date)

    bse_daily = {}
    if bse_t1 and bse_t2:
        bse_daily["bse_fii_fut_daily"] = bse_t1["bse_fii_fut_idx_net"] - bse_t2.get("bse_fii_fut_idx_net", 0)
        bse_daily["bse_fii_call_daily"] = bse_t1["bse_fii_call_net"] - bse_t2.get("bse_fii_call_net", 0)
        bse_daily["bse_fii_put_daily"] = bse_t1["bse_fii_put_net"] - bse_t2.get("bse_fii_put_net", 0)
        bse_daily["bse_pro_fut_daily"] = bse_t1.get("bse_pro_fut_idx_net", 0) - bse_t2.get("bse_pro_fut_idx_net", 0)
        bse_daily["bse_pro_call_daily"] = bse_t1.get("bse_pro_call_net", 0) - bse_t2.get("bse_pro_call_net", 0)
        bse_daily["bse_pro_put_daily"] = bse_t1.get("bse_pro_put_net", 0) - bse_t2.get("bse_pro_put_net", 0)
        print(f"  [BSE] FII daily: fut={bse_daily['bse_fii_fut_daily']:+,} "
              f"call={bse_daily['bse_fii_call_daily']:+,} "
              f"put={bse_daily['bse_fii_put_daily']:+,}")
        print(f"  [BSE] PRO daily: fut={bse_daily['bse_pro_fut_daily']:+,} "
              f"call={bse_daily['bse_pro_call_daily']:+,} "
              f"put={bse_daily['bse_pro_put_daily']:+,}")
    else:
        print("  [BSE] WARNING: Could not fetch BSE data. BSE columns will be empty.")
        if not bse_t1:
            print("    T-1 BSE data: FAILED")
        if not bse_t2:
            print("    T-2 BSE data: FAILED")

    # Build new row
    new_row = {
        "date": expiry_str,
        "day_of_week": expiry_date.strftime("%A"),
        "expiry_type": determine_expiry_type(expiry_date),
        "chart": "",
        "sensex_open": "",
        "sensex_high": "",
        "sensex_low": "",
        "sensex_close": "",
        "vix_open": "",
        "vix_close": "",
        "vix_predicted_move_pct": "",
        "actual_range_pct": "",
        "actual_open_close_pct": "",
        "intraday_high_pct": "",
        "intraday_low_pct": "",
        "range_vs_vix_ratio": "",
        "diff_pct": "",
        "vix_accuracy": "",
        "t1_fii_fut_daily": int(fii_fut_d),
        "t1_fii_call_daily": int(fii_call_d),
        "t1_fii_put_daily": int(fii_put_d),
        "t1_fii_stance": fii_stance,
        "t1_fii_direction": fii_direction,
        "t1_pro_fut_daily": int(pro_fut_d),
        "t1_pro_call_daily": int(pro_call_d),
        "t1_pro_put_daily": int(pro_put_d),
        "t1_pro_stance": pro_stance,
        "is_nifty_expiry_day": 1 if expiry_date.weekday() == 3 else 0,
        # BSE-specific daily changes (Sensex derivatives only, T1 - T2)
        "bse_fii_fut_daily": bse_daily.get("bse_fii_fut_daily", ""),
        "bse_fii_call_daily": bse_daily.get("bse_fii_call_daily", ""),
        "bse_fii_put_daily": bse_daily.get("bse_fii_put_daily", ""),
        "bse_pro_fut_daily": bse_daily.get("bse_pro_fut_daily", ""),
        "bse_pro_call_daily": bse_daily.get("bse_pro_call_daily", ""),
        "bse_pro_put_daily": bse_daily.get("bse_pro_put_daily", ""),
    }

    # Append row
    new_df = pd.DataFrame([new_row])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

    print(f"\n  Row appended for {expiry_str}")
    print(f"  CSV now has {len(df)} rows")
    print("=" * 60)


def run_post_expiry():
    """Phase 2: Fill Sensex OHLC + VIX data (run on Thursday evening)."""
    print("=" * 60)
    print("PHASE 2: POST-EXPIRY (Thursday)")
    print("=" * 60)

    today = datetime.now()
    # If today is Thursday, the expiry is today
    if today.weekday() == 3:  # Thursday
        expiry_date = today
    else:
        # For manual runs, find the most recent Thursday
        days_back = (today.weekday() - 3) % 7
        expiry_date = today - timedelta(days=days_back)

    expiry_str = expiry_date.strftime("%Y-%m-%d")
    print(f"  Expiry date: {expiry_str}")

    # Load CSV
    df = pd.read_csv(CSV_PATH)

    # Find the row to update (last row or matching date)
    if df.iloc[-1]["date"] == expiry_str:
        row_idx = len(df) - 1
    elif expiry_str in df["date"].values:
        row_idx = df[df["date"] == expiry_str].index[-1]
    else:
        print(f"  ERROR: No row found for {expiry_str}. Run pre_expiry first.")
        sys.exit(1)

    # Check if already filled
    if pd.notna(df.at[row_idx, "sensex_close"]) and df.at[row_idx, "sensex_close"] != "":
        print(f"  WARNING: Row for {expiry_str} already has Sensex data. Skipping.")
        return

    # Fetch Sensex OHLC from Yahoo Finance
    print("\n  Fetching Sensex OHLC from Yahoo Finance (^BSESN)...")
    start_date = expiry_date.strftime("%Y-%m-%d")
    end_date = (expiry_date + timedelta(days=1)).strftime("%Y-%m-%d")

    sensex = yf.download("^BSESN", start=start_date, end=end_date, progress=False)
    # Flatten MultiIndex columns if present (newer yfinance versions)
    if hasattr(sensex.columns, "nlevels") and sensex.columns.nlevels > 1:
        sensex.columns = sensex.columns.droplevel(1)

    if sensex.empty:
        print("  ERROR: No Sensex data available for this date.")
        print("  Market may be closed or data not yet available.")
        sys.exit(1)

    sensex_open = round(float(sensex["Open"].iloc[0]), 2)
    sensex_high = round(float(sensex["High"].iloc[0]), 2)
    sensex_low = round(float(sensex["Low"].iloc[0]), 2)
    sensex_close = round(float(sensex["Close"].iloc[0]), 2)

    print(f"  Sensex: O={sensex_open} H={sensex_high} L={sensex_low} C={sensex_close}")

    # Fetch India VIX from Yahoo Finance
    print("  Fetching India VIX from Yahoo Finance (^INDIAVIX)...")
    vix = yf.download("^INDIAVIX", start=start_date, end=end_date, progress=False)
    if hasattr(vix.columns, "nlevels") and vix.columns.nlevels > 1:
        vix.columns = vix.columns.droplevel(1)

    if vix.empty:
        print("  WARNING: No VIX data available. Using previous day's VIX.")
        # Try fetching a range
        vix = yf.download(
            "^INDIAVIX",
            start=(expiry_date - timedelta(days=5)).strftime("%Y-%m-%d"),
            end=end_date,
            progress=False,
        )
        if hasattr(vix.columns, "nlevels") and vix.columns.nlevels > 1:
            vix.columns = vix.columns.droplevel(1)

        if not vix.empty:
            vix_open = round(float(vix["Open"].iloc[-1]), 2)
            vix_close = round(float(vix["Close"].iloc[-1]), 2)
        else:
            print("  ERROR: Cannot fetch VIX data at all.")
            sys.exit(1)
    else:
        vix_open = round(float(vix["Open"].iloc[0]), 2)
        vix_close = round(float(vix["Close"].iloc[0]), 2)

    print(f"  VIX: Open={vix_open} Close={vix_close}")

    # Compute metrics
    # VIX predicted move = vix_open / sqrt(252) * (1/sqrt(expiry_periods))
    # For weekly expiry (1 day), use vix/sqrt(252)
    vix_predicted_move_pct = round(vix_open / np.sqrt(252), 2)

    # Actual range % = (high - low) / open * 100
    actual_range_pct = round((sensex_high - sensex_low) / sensex_open * 100, 2)

    # Actual open-close % = (close - open) / open * 100
    actual_open_close_pct = round((sensex_close - sensex_open) / sensex_open * 100, 2)

    # Intraday high % = (high - open) / open * 100
    intraday_high_pct = round((sensex_high - sensex_open) / sensex_open * 100, 2)

    # Intraday low % = (low - open) / open * 100
    intraday_low_pct = round((sensex_low - sensex_open) / sensex_open * 100, 2)

    # Range vs VIX ratio = actual_range_pct / vix_predicted_move_pct
    range_vs_vix_ratio = round(actual_range_pct / vix_predicted_move_pct, 2) if vix_predicted_move_pct != 0 else 0

    # Diff % = actual_range_pct - vix_predicted_move_pct
    diff_pct = round(actual_range_pct - vix_predicted_move_pct, 2)

    # VIX accuracy
    if actual_range_pct > vix_predicted_move_pct:
        vix_accuracy = "Underestimated"
    else:
        vix_accuracy = "Overestimated"

    # Chart sparkline
    chart = generate_chart_sparkline(sensex_open, sensex_high, sensex_low, sensex_close)

    # Expiry type
    expiry_type = determine_expiry_type(expiry_date)

    print(f"\n  VIX predicted move: {vix_predicted_move_pct}%")
    print(f"  Actual range: {actual_range_pct}%")
    print(f"  Range vs VIX ratio: {range_vs_vix_ratio}")
    print(f"  VIX accuracy: {vix_accuracy}")

    # Update row
    df.at[row_idx, "expiry_type"] = expiry_type
    df.at[row_idx, "chart"] = chart
    df.at[row_idx, "sensex_open"] = sensex_open
    df.at[row_idx, "sensex_high"] = sensex_high
    df.at[row_idx, "sensex_low"] = sensex_low
    df.at[row_idx, "sensex_close"] = sensex_close
    df.at[row_idx, "vix_open"] = vix_open
    df.at[row_idx, "vix_close"] = vix_close
    df.at[row_idx, "vix_predicted_move_pct"] = vix_predicted_move_pct
    df.at[row_idx, "actual_range_pct"] = actual_range_pct
    df.at[row_idx, "actual_open_close_pct"] = actual_open_close_pct
    df.at[row_idx, "intraday_high_pct"] = intraday_high_pct
    df.at[row_idx, "intraday_low_pct"] = intraday_low_pct
    df.at[row_idx, "range_vs_vix_ratio"] = range_vs_vix_ratio
    df.at[row_idx, "diff_pct"] = diff_pct
    df.at[row_idx, "vix_accuracy"] = vix_accuracy

    df.to_csv(CSV_PATH, index=False)

    print(f"\n  Row updated for {expiry_str}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Weekly Sensex Expiry Data Updater")
    parser.add_argument(
        "--phase",
        required=True,
        choices=["pre_expiry", "post_expiry"],
        help="Phase to run: pre_expiry (Wednesday) or post_expiry (Thursday)",
    )
    args = parser.parse_args()

    if not CSV_PATH.exists():
        print(f"ERROR: CSV not found at {CSV_PATH}")
        sys.exit(1)

    if args.phase == "pre_expiry":
        run_pre_expiry()
    else:
        run_post_expiry()


if __name__ == "__main__":
    main()
