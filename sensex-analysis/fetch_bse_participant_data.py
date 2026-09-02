#!/usr/bin/env python3
"""
Fetch Participant-wise Data (FII / PRO) for BSE/Sensex Analysis - T-1 Format

Fetches FII and PRO data from TWO sources:
1. NSE participant-wise OI archives (aggregate F&O across all segments)
2. BSE beta.bseindia.com (Sensex-specific derivatives OI)

T-1 Format:
- Each row's date = day T (e.g., 2026-08-28)
- Positions = T-1's closing positions (e.g., 2026-08-27's EOD)
- Daily changes = (T-1) minus (T-2)
- This shows what positions were held BEFORE market opened on day T

Sources:
  NSE: https://archives.nseindia.com/content/nsccl/fao_participant_oi_DDMMYYYY.csv
  BSE: https://beta.bseindia.com/markets/Derivatives/DeriReports/DeriMarketDisclosures.aspx

Output:
- sensex_bse_participant_wise_daily.csv: Daily FII, PRO T-1 positions + directions
  (NSE aggregate + BSE Sensex-specific columns)

Author: Claude Code
Date: 2026-09-02
"""

import re
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

BSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
}

BSE_URL = "https://beta.bseindia.com/markets/Derivatives/DeriReports/DeriMarketDisclosures.aspx"

# Cache
_cache = {}
_bse_cache = {}


def get_nse_session():
    """Create NSE session with proper headers."""
    session = requests.Session()
    session.headers.update(NSE_HEADERS)
    return session


def _parse_indian_num(s):
    """Parse Indian number format (1,23,456) to int."""
    s = s.strip().replace(",", "")
    if s == "-" or s == "":
        return 0
    return int(s)


def _parse_bse_oi_from_grid(html):
    """Parse BSE OI data from grvOpenInterst grid span IDs."""
    spans = dict(
        re.findall(r"ContentPlaceHolder1_grvOpenInterst_([^\"]+)\"[^>]*>([^<]+)", html)
    )

    if "Label2_1" not in spans:
        return _parse_bse_oi_from_html(html)

    data = {}
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


def fetch_bse_participant_oi(date=None):
    """
    Fetch BSE-specific participant-wise OI from beta.bseindia.com.
    Supports historical dates via ASP.NET form postback.

    Returns dict with bse_fii_*/bse_pro_* net positions or None.
    """
    cache_key = date.strftime('%d%m%Y') if date else 'latest'
    if cache_key in _bse_cache:
        return _bse_cache[cache_key]

    try:
        session = requests.Session()
        session.headers.update(BSE_HEADERS)

        r = session.get(BSE_URL, timeout=20)
        if r.status_code != 200:
            _bse_cache[cache_key] = None
            return None

        html = r.text

        if date is None:
            result = _parse_bse_oi_from_html(html)
            _bse_cache[cache_key] = result
            return result

        viewstate = re.search(r"__VIEWSTATE[^G][^>]*value=\"([^\"]*)\"", html)
        event_val = re.search(r"__EVENTVALIDATION[^>]*value=\"([^\"]*)\"", html)
        viewstate_gen = re.search(r"__VIEWSTATEGENERATOR[^>]*value=\"([^\"]*)\"", html)

        if not viewstate or not event_val:
            result = _parse_bse_oi_from_html(html)
            _bse_cache[cache_key] = result
            return result

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
            _bse_cache[cache_key] = None
            return None

        result = _parse_bse_oi_from_grid(r2.text)
        _bse_cache[cache_key] = result
        return result

    except Exception as e:
        _bse_cache[cache_key] = None
        return None


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


def classify_view(val):
    """Classify composite value into a view label."""
    if val is None:
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
    Fetch daily participant-wise OI data for the last N trading days in T-1 format.
    Each row's date = day T, but positions = T-1's EOD, daily changes = (T-1) - (T-2).
    """
    print("=" * 70)
    print("FETCH PARTICIPANT-WISE DATA (FII / PRO) - T-1 Format")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()
    print(f"Sources:")
    print(f"  NSE: archives.nseindia.com → fao_participant_oi_DDMMYYYY.csv")
    print(f"  BSE: beta.bseindia.com → Sensex-specific participant OI")
    print(f"  → T-1 Format: Each row date = T, positions = T-1 EOD")
    print(f"  → Daily changes = (T-1) - (T-2)")
    print()

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back + 10)  # extra buffer for weekends
    trading_days = get_trading_days(start_date, end_date)

    print(f"Fetching {len(trading_days)} potential trading days...")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print()

    session = get_nse_session()

    # First, fetch all available NSE data
    all_data = []
    fetched = 0
    failed = 0

    for i, day in enumerate(trading_days):
        data = fetch_participant_oi(session, day)
        time.sleep(0.4)  # Rate limiting

        if data is not None:
            all_data.append({'date': day, 'data': data})
            fetched += 1
        else:
            failed += 1

    if len(all_data) < 2:
        print("\nERROR: Need at least 2 days of data for T-1 format.")
        return

    # Fetch BSE-specific data for all dates
    print(f"\nFetching BSE participant OI (Sensex-specific)...")
    bse_all_data = {}
    bse_fetched = 0
    bse_failed = 0

    for entry in all_data:
        day = entry['date']
        bse_data = fetch_bse_participant_oi(date=day)
        time.sleep(1.0)  # BSE needs more delay (form postback)

        if bse_data is not None:
            bse_all_data[day.strftime('%Y-%m-%d')] = bse_data
            bse_fetched += 1
        else:
            bse_failed += 1

    print(f"  BSE fetched: {bse_fetched}, failed/unavailable: {bse_failed}")

    # Now build records in T-1 format
    daily_records = []

    for i in range(len(all_data) - 1):
        # Current row will have date = T (next day)
        # But positions from T-1 (current day)
        # And daily changes = (T-1) - (T-2)

        t_minus_1_date = all_data[i]['date']
        t_minus_1_data = all_data[i]['data']
        t_date = all_data[i + 1]['date']

        record = {'date': t_date.strftime('%Y-%m-%d')}

        # Store T-1 positions (positions held BEFORE day T opened)
        for prefix in ['fii', 'pro']:
            record[f'{prefix}_fut_idx_net'] = t_minus_1_data.get(f'{prefix}_fut_idx_net', 0)
            record[f'{prefix}_fut_stk_net'] = t_minus_1_data.get(f'{prefix}_fut_stk_net', 0)
            record[f'{prefix}_call_net'] = t_minus_1_data.get(f'{prefix}_call_net', 0)
            record[f'{prefix}_put_net'] = t_minus_1_data.get(f'{prefix}_put_net', 0)

        # Compute NSE daily changes: (T-1) - (T-2)
        if i > 0:
            t_minus_2_data = all_data[i - 1]['data']
            for prefix in ['fii', 'pro']:
                fut_daily = t_minus_1_data.get(f'{prefix}_fut_idx_net', 0) - t_minus_2_data.get(f'{prefix}_fut_idx_net', 0)
                call_daily = t_minus_1_data.get(f'{prefix}_call_net', 0) - t_minus_2_data.get(f'{prefix}_call_net', 0)
                put_daily = t_minus_1_data.get(f'{prefix}_put_net', 0) - t_minus_2_data.get(f'{prefix}_put_net', 0)

                record[f't1_{prefix}_fut_daily'] = fut_daily
                record[f't1_{prefix}_call_daily'] = call_daily
                record[f't1_{prefix}_put_daily'] = put_daily
                record[f't1_{prefix}_direction'] = determine_direction(fut_daily, call_daily, put_daily)
                record[f't1_{prefix}_stance'] = determine_stance(prefix, fut_daily, call_daily, put_daily)
                composite = int(fut_daily + call_daily - put_daily)
                record[f'nse_{prefix}_composite'] = composite
                record[f'nse_{prefix}_view'] = classify_view(composite)
        else:
            # First row: no T-2 data available
            for prefix in ['fii', 'pro']:
                record[f't1_{prefix}_fut_daily'] = 0
                record[f't1_{prefix}_call_daily'] = 0
                record[f't1_{prefix}_put_daily'] = 0
                record[f't1_{prefix}_direction'] = "Neutral"
                record[f't1_{prefix}_stance'] = f"{prefix.upper()} Neutral"
                record[f'nse_{prefix}_composite'] = 0
                record[f'nse_{prefix}_view'] = "Neutral"

        # Compute BSE daily changes: (T-1) - (T-2)
        t1_key = t_minus_1_date.strftime('%Y-%m-%d')
        bse_t1 = bse_all_data.get(t1_key)

        if i > 0:
            t2_key = all_data[i - 1]['date'].strftime('%Y-%m-%d')
            bse_t2 = bse_all_data.get(t2_key)
        else:
            bse_t2 = None

        if bse_t1 and bse_t2:
            for prefix in ['bse_fii', 'bse_pro']:
                fut_d = bse_t1.get(f'{prefix}_fut_idx_net', 0) - bse_t2.get(f'{prefix}_fut_idx_net', 0)
                call_d = bse_t1.get(f'{prefix}_call_net', 0) - bse_t2.get(f'{prefix}_call_net', 0)
                put_d = bse_t1.get(f'{prefix}_put_net', 0) - bse_t2.get(f'{prefix}_put_net', 0)
                record[f'{prefix}_fut_daily'] = fut_d
                record[f'{prefix}_call_daily'] = call_d
                record[f'{prefix}_put_daily'] = put_d
                composite = int(fut_d + call_d - put_d)
                record[f'{prefix}_composite'] = composite
                record[f'{prefix}_view'] = classify_view(composite)
        else:
            for prefix in ['bse_fii', 'bse_pro']:
                record[f'{prefix}_fut_daily'] = ""
                record[f'{prefix}_call_daily'] = ""
                record[f'{prefix}_put_daily'] = ""
                record[f'{prefix}_composite'] = ""
                record[f'{prefix}_view'] = ""

        daily_records.append(record)

        if (i + 1) % 5 == 0 or i < 3:
            fii_d = record.get('t1_fii_direction', '?')
            pro_d = record.get('t1_pro_direction', '?')
            print(f"  [{i+1}/{len(all_data)-1}] Date={t_date.date()} (T-1={t_minus_1_date.date()}) "
                  f"FII:{record['fii_fut_idx_net']:+,} PRO:{record['pro_fut_idx_net']:+,} "
                  f"→ {fii_d}/{pro_d}")

    if not daily_records:
        print("\nERROR: No records built.")
        return

    df = pd.DataFrame(daily_records)

    # Ensure column order: NSE fields, then BSE fields, then composite/view
    nse_cols = ['date',
                'fii_fut_idx_net', 'fii_fut_stk_net', 'fii_call_net', 'fii_put_net',
                'pro_fut_idx_net', 'pro_fut_stk_net', 'pro_call_net', 'pro_put_net',
                't1_fii_fut_daily', 't1_fii_call_daily', 't1_fii_put_daily',
                't1_fii_direction', 't1_fii_stance',
                't1_pro_fut_daily', 't1_pro_call_daily', 't1_pro_put_daily',
                't1_pro_direction', 't1_pro_stance']
    bse_cols = ['bse_fii_fut_daily', 'bse_fii_call_daily', 'bse_fii_put_daily',
                'bse_fii_composite', 'bse_fii_view',
                'bse_pro_fut_daily', 'bse_pro_call_daily', 'bse_pro_put_daily',
                'bse_pro_composite', 'bse_pro_view']
    view_cols = ['nse_fii_composite', 'nse_fii_view', 'nse_pro_composite', 'nse_pro_view']
    ordered_cols = [c for c in nse_cols + bse_cols + view_cols if c in df.columns]
    df = df[ordered_cols]

    # Save full dataset
    output_path = OUTPUT_DIR / "sensex_bse_participant_wise_daily.csv"
    df.to_csv(output_path, index=False)

    print()
    print("=" * 70)
    print("COMPLETE!")
    print(f"  Output: {output_path}")
    print(f"  Rows: {len(df)} trading days (T-1 format)")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  NSE data fetched: {fetched} days, Failed/Holiday: {failed}")
    print(f"  BSE data fetched: {bse_fetched} days, Failed/Holiday: {bse_failed}")
    print()

    # Summary statistics
    # Skip first row (no daily change)
    analysis_df = df[df['t1_fii_fut_daily'] != 0].copy() if len(df) > 1 else df

    print("  FII Direction Distribution:")
    for d, count in analysis_df['t1_fii_direction'].value_counts().items():
        print(f"    {d}: {count} ({count/len(analysis_df)*100:.0f}%)")

    print()
    print("  PRO Direction Distribution:")
    for d, count in analysis_df['t1_pro_direction'].value_counts().items():
        print(f"    {d}: {count} ({count/len(analysis_df)*100:.0f}%)")

    print()
    print("  FII Stance Distribution:")
    for stance, count in analysis_df['t1_fii_stance'].value_counts().head(5).items():
        print(f"    {stance}: {count}")

    print()
    print("  PRO Stance Distribution:")
    for stance, count in analysis_df['t1_pro_stance'].value_counts().head(5).items():
        print(f"    {stance}: {count}")

    print()
    print("  Latest positions (net contracts):")
    last = df.iloc[-1]
    print(f"    FII: Fut={last['fii_fut_idx_net']:+,} Call={last['fii_call_net']:+,} Put={last['fii_put_net']:+,}")
    print(f"    PRO: Fut={last['pro_fut_idx_net']:+,} Call={last['pro_call_net']:+,} Put={last['pro_put_net']:+,}")
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
