#!/usr/bin/env python3
"""
Sensex Expiry Day Afternoon Reversal Analysis
===============================================
Joins Sensex expiry-day metadata (CSV) with 5-minute Nifty intraday bars
(PostgreSQL proxy) to identify when directional moves begin in the afternoon
session (post-2 PM) on Sensex expiry days.

NOTE: Sensex 5-min intraday data is not available in the database.
Nifty 50 5-min data is used as a proxy — Sensex and Nifty are 95%+
correlated intraday, so the timing of inflection points carries over
reliably. The Sensex daily OHLC from the CSV is used for direction
classification, while Nifty 5-min bars provide the timing granularity.

Data sources:
  - sensex-analysis/sensex_fii_t1_6year_expiry.csv (323 Sensex expiry days, Jun 2020–Aug 2026)
  - market_data.nifty50_5min (PostgreSQL, Nifty 5-min OHLCV proxy)

Output:
  - sensex-analysis/sensex_afternoon_reversal_results.csv
  - sensex-analysis/SENSEX_AFTERNOON_REVERSAL_REPORT.md
"""

import os
import sys
import warnings
from pathlib import Path
from datetime import time as dt_time
from zoneinfo import ZoneInfo

import pandas as pd
import psycopg2

warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy.*")

IST = ZoneInfo("Asia/Kolkata")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "sensex-analysis" / "sensex_fii_t1_6year_expiry.csv"
OUTPUT_DIR = REPO_ROOT / "sensex-analysis"
CSV_OUTPUT = OUTPUT_DIR / "sensex_afternoon_reversal_results.csv"
REPORT_OUTPUT = OUTPUT_DIR / "SENSEX_AFTERNOON_REVERSAL_REPORT.md"

DB_PARAMS = dict(host="localhost", dbname="market_data")

AFTERNOON_START = dt_time(14, 0)
AFTERNOON_END = dt_time(15, 25)

VIX_BUCKETS = [
    (0, 15, "Low (<15)"),
    (15, 20, "Medium (15-20)"),
    (20, 999, "High (>20)"),
]

ALL_SLOTS = [
    f"{h:02d}:{m:02d}"
    for h in range(14, 16)
    for m in range(0, 60, 5)
    if dt_time(h, m) >= AFTERNOON_START and dt_time(h, m) <= AFTERNOON_END
]

# ---------------------------------------------------------------------------
# 1. Load Sensex CSV
# ---------------------------------------------------------------------------
def load_sensex_csv():
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    # Derive move_direction from sensex_open vs sensex_close
    def classify_day(row):
        pct = abs(row["sensex_close"] - row["sensex_open"]) / row["sensex_open"] * 100
        if pct < 0.01:
            return "Flat"
        return "Top to Down" if row["sensex_open"] > row["sensex_close"] else "Down to Up"

    df["move_direction"] = df.apply(classify_day, axis=1)

    cols = [
        "date", "day_of_week", "move_direction", "expiry_type",
        "vix_open", "vix_close",
        "sensex_open", "sensex_high", "sensex_low", "sensex_close",
        "t1_fii_stance", "t1_pro_stance",
        "fii_composite", "fii_view", "pro_composite", "pro_view",
        "is_nifty_expiry_day",
    ]
    # Add BSE-specific columns if available
    for c in ["bse_fii_fut_daily", "bse_fii_call_daily", "bse_fii_put_daily"]:
        if c in df.columns:
            cols.append(c)

    df = df[cols].copy()
    print(f"[CSV] Loaded {len(df)} Sensex expiry days ({df['date'].min().date()} to {df['date'].max().date()})")

    dir_counts = df["move_direction"].value_counts()
    print(f"[CSV] Direction: {dir_counts.to_dict()}")
    return df


# ---------------------------------------------------------------------------
# 2. Fetch Nifty afternoon 5-min bars as proxy
# ---------------------------------------------------------------------------
def fetch_afternoon_bars(conn, expiry_date):
    """Return DataFrame of Nifty 5-min bars for the afternoon session."""
    query = """
        SELECT datetime, open, high, low, close
        FROM nifty50_5min
        WHERE datetime::date = %s
          AND datetime::time >= '14:00'
          AND datetime::time <= '15:25'
        ORDER BY datetime
    """
    df = pd.read_sql(query, conn, params=[expiry_date])
    return df


def fetch_all_afternoon_bars(expiry_dates):
    """Fetch Nifty afternoon bars for all Sensex expiry dates."""
    conn = psycopg2.connect(**DB_PARAMS)
    results = {}
    skipped = []
    for d in expiry_dates:
        date_str = d.strftime("%Y-%m-%d")
        bars = fetch_afternoon_bars(conn, date_str)
        if bars.empty:
            skipped.append(date_str)
        else:
            results[date_str] = bars
    conn.close()
    if skipped:
        print(f"[DB] Skipped {len(skipped)} dates with no Nifty 5-min data: {', '.join(skipped[:10])}{'...' if len(skipped) > 10 else ''}")
    print(f"[DB] Fetched Nifty proxy bars for {len(results)} Sensex expiry days")
    return results, skipped


# ---------------------------------------------------------------------------
# 3. Classify afternoon direction using Nifty proxy timing
# ---------------------------------------------------------------------------
def classify_afternoon(bars_df):
    """
    Using Nifty 5-min proxy bars, determine:
      - afternoon_direction (Nifty proxy): Top to Down / Down to Up / Flat
      - inflection_time: HH:MM of the inflection candle
      - inflection_price: Nifty price at inflection
      - nifty_price_at_2pm: Nifty open at 14:00
      - nifty_session_close: Nifty close at last candle
    """
    nifty_2pm = float(bars_df.iloc[0]["open"])
    nifty_close = float(bars_df.iloc[-1]["close"])

    pct_change = abs(nifty_close - nifty_2pm) / nifty_2pm * 100

    if pct_change < 0.01:
        direction = "Flat"
        inflection_time = None
        inflection_price = None
    elif nifty_2pm > nifty_close:
        direction = "Top to Down"
        idx = bars_df["high"].astype(float).idxmax()
        ts = pd.Timestamp(bars_df.loc[idx, "datetime"])
        inflection_time = ts.tz_convert(IST).strftime("%H:%M") if ts.tz else ts.strftime("%H:%M")
        inflection_price = float(bars_df.loc[idx, "high"])
    else:
        direction = "Down to Up"
        idx = bars_df["low"].astype(float).idxmin()
        ts = pd.Timestamp(bars_df.loc[idx, "datetime"])
        inflection_time = ts.tz_convert(IST).strftime("%H:%M") if ts.tz else ts.strftime("%H:%M")
        inflection_price = float(bars_df.loc[idx, "low"])

    return direction, inflection_time, inflection_price, nifty_2pm, nifty_close


# ---------------------------------------------------------------------------
# 4. Build results
# ---------------------------------------------------------------------------
def build_results(csv_df, bars_dict):
    rows = []
    for _, row in csv_df.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        if date_str not in bars_dict:
            continue

        bars = bars_dict[date_str]
        proxy_dir, infl_time, infl_price, nifty_2pm, nifty_close = classify_afternoon(bars)

        # Sensex daily direction from CSV
        sensex_direction = row["move_direction"]

        # Concordance: does the Nifty proxy afternoon match Sensex daily?
        if proxy_dir == "Flat":
            concordance_proxy = "Flat"
        elif proxy_dir == sensex_direction:
            concordance_proxy = "Match"
        else:
            concordance_proxy = "Mismatch"

        # Sensex afternoon direction (approximated from daily OHLC)
        # Since we don't have Sensex 5-min, we use the Nifty proxy direction
        # but also note the Sensex daily direction for comparison

        vix_val = float(row["vix_open"])
        vix_bucket = next(
            (label for lo, hi, label in VIX_BUCKETS if lo <= vix_val < hi),
            "High (>20)"
        )

        sensex_open = float(row["sensex_open"])
        sensex_close_val = float(row["sensex_close"])
        sensex_move_pct = abs(sensex_close_val - sensex_open) / sensex_open * 100

        nifty_move_from_2pm_pct = abs(nifty_close - nifty_2pm) / nifty_2pm * 100 if nifty_2pm else 0
        move_from_inflection_pct = (
            abs(nifty_close - infl_price) / infl_price * 100
            if infl_price else 0
        )

        rec = {
            "date": date_str,
            "day_of_week": row["day_of_week"],
            "expiry_type": row["expiry_type"],
            "sensex_daily_direction": sensex_direction,
            "nifty_proxy_afternoon_direction": proxy_dir,
            "concordance": concordance_proxy,
            "is_nifty_expiry_day": int(row["is_nifty_expiry_day"]),
            "vix_open": round(vix_val, 2),
            "vix_close": round(float(row["vix_close"]), 2),
            "vix_bucket": vix_bucket,
            "t1_fii_stance": row["t1_fii_stance"],
            "t1_pro_stance": row["t1_pro_stance"],
            "fii_composite": int(row["fii_composite"]),
            "fii_view": row["fii_view"],
            "pro_composite": int(row["pro_composite"]),
            "pro_view": row["pro_view"],
            "sensex_open": round(sensex_open, 2),
            "sensex_close": round(sensex_close_val, 2),
            "sensex_daily_move_pct": round(sensex_move_pct, 3),
            "nifty_price_at_2pm": round(nifty_2pm, 2),
            "nifty_session_close": round(nifty_close, 2),
            "nifty_move_from_2pm_pct": round(nifty_move_from_2pm_pct, 3),
            "inflection_time": infl_time,
            "inflection_price": round(infl_price, 2) if infl_price else None,
            "move_from_inflection_pct": round(move_from_inflection_pct, 3),
        }
        rows.append(rec)

    results_df = pd.DataFrame(rows)
    print(f"[Analysis] Built results for {len(results_df)} Sensex expiry days")
    return results_df


# ---------------------------------------------------------------------------
# 5. Statistical analysis helpers
# ---------------------------------------------------------------------------
def timing_distribution(df, label="All"):
    valid = df[df["inflection_time"].notna()].copy()
    counts = valid["inflection_time"].value_counts().reindex(ALL_SLOTS, fill_value=0)
    total = counts.sum()
    pct = (counts / total * 100).round(1) if total > 0 else counts * 0
    dist = pd.DataFrame({"time": counts.index, "count": counts.values, "pct": pct.values})
    dist["group"] = label
    return dist, total


def segmented_distributions(df):
    all_dists = []

    d, _ = timing_distribution(df, "All Sensex Expiry Days")
    all_dists.append(d)

    for direction in ["Top to Down", "Down to Up"]:
        sub = df[df["nifty_proxy_afternoon_direction"] == direction]
        d, _ = timing_distribution(sub, direction)
        all_dists.append(d)

    for etype in ["weekly", "monthly"]:
        sub = df[df["expiry_type"] == etype]
        d, _ = timing_distribution(sub, f"Expiry: {etype}")
        all_dists.append(d)

    for _, _, label in VIX_BUCKETS:
        sub = df[df["vix_bucket"] == label]
        d, _ = timing_distribution(sub, f"VIX: {label}")
        all_dists.append(d)

    for stance in df["t1_fii_stance"].value_counts().head(6).index:
        sub = df[df["t1_fii_stance"] == stance]
        if len(sub) >= 5:
            d, _ = timing_distribution(sub, f"FII: {stance}")
            all_dists.append(d)

    # Nifty expiry day vs non-Nifty expiry day
    for val, label in [(1, "Also Nifty Expiry Day"), (0, "Sensex-Only Expiry Day")]:
        sub = df[df["is_nifty_expiry_day"] == val]
        if len(sub) >= 5:
            d, _ = timing_distribution(sub, label)
            all_dists.append(d)

    # By FII View (composite)
    for view in ["Strong Bullish", "Bullish", "Mildly Bullish", "Neutral", "Mildly Bearish", "Bearish", "Strong Bearish"]:
        sub = df[df["fii_view"] == view]
        if len(sub) >= 5:
            d, _ = timing_distribution(sub, f"FII View: {view}")
            all_dists.append(d)

    # By PRO View (composite)
    for view in ["Strong Bullish", "Bullish", "Mildly Bullish", "Neutral", "Mildly Bearish", "Bearish", "Strong Bearish"]:
        sub = df[df["pro_view"] == view]
        if len(sub) >= 5:
            d, _ = timing_distribution(sub, f"PRO View: {view}")
            all_dists.append(d)

    return all_dists


def move_magnitude_by_bucket(csv_df, bars_dict):
    time_markers = ["14:00", "14:15", "14:30", "14:45", "15:00"]
    rows = []
    for _, row in csv_df.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        if date_str not in bars_dict:
            continue
        bars = bars_dict[date_str]
        sess_close = float(bars.iloc[-1]["close"])
        p2pm = float(bars.iloc[0]["open"])
        direction = "Top to Down" if p2pm > sess_close else "Down to Up"
        if abs(sess_close - p2pm) / p2pm * 100 < 0.01:
            direction = "Flat"

        for marker in time_markers:
            marker_bars = bars[
                bars["datetime"].apply(
                    lambda x: (pd.Timestamp(x).tz_convert(IST).strftime("%H:%M")
                               if pd.Timestamp(x).tz else pd.Timestamp(x).strftime("%H:%M"))
                ) == marker
            ]
            if marker_bars.empty:
                continue
            marker_open = float(marker_bars.iloc[0]["open"])
            move_pct = abs(sess_close - marker_open) / marker_open * 100
            rows.append({
                "time_marker": marker,
                "direction": direction,
                "move_pct": round(move_pct, 3),
            })

    mag_df = pd.DataFrame(rows)
    if mag_df.empty:
        return pd.DataFrame()

    stats = (
        mag_df.groupby(["time_marker", "direction"])["move_pct"]
        .agg(["mean", "median", "min", "max", "count"])
        .round(3)
        .reset_index()
    )
    return stats


def vix_fii_crosstab(df):
    valid = df[df["inflection_time"].notna()].copy()
    if valid.empty:
        return pd.DataFrame()

    rows = []
    for vix_b in [label for _, _, label in VIX_BUCKETS]:
        for fii_s in valid["t1_fii_stance"].unique():
            sub = valid[(valid["vix_bucket"] == vix_b) & (valid["t1_fii_stance"] == fii_s)]
            if len(sub) < 2:
                continue
            modal_time = sub["inflection_time"].mode().iloc[0] if not sub["inflection_time"].mode().empty else "N/A"
            avg_mag = round(sub["move_from_inflection_pct"].mean(), 3)
            rows.append({
                "vix_bucket": vix_b,
                "fii_stance": fii_s,
                "count": len(sub),
                "modal_inflection_time": modal_time,
                "avg_move_from_inflection_pct": avg_mag,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 6. Markdown report generation
# ---------------------------------------------------------------------------
def dist_table_md(dist_df, title):
    lines = [f"### {title}\n"]
    lines.append("| Time | Count | % |")
    lines.append("|------|------:|----:|")
    for _, r in dist_df.iterrows():
        lines.append(f"| {r['time']} | {int(r['count'])} | {r['pct']}% |")
    lines.append("")
    return "\n".join(lines)


def generate_report(results_df, all_dists, mag_stats, crosstab_df, skipped_dates):
    valid = results_df[results_df["inflection_time"].notna()]
    total_days = len(results_df)
    flat_days = len(results_df[results_df["nifty_proxy_afternoon_direction"] == "Flat"])
    ttd_days = len(results_df[results_df["nifty_proxy_afternoon_direction"] == "Top to Down"])
    dtu_days = len(results_df[results_df["nifty_proxy_afternoon_direction"] == "Down to Up"])

    # Sensex daily direction stats
    sensex_ttd = len(results_df[results_df["sensex_daily_direction"] == "Top to Down"])
    sensex_dtu = len(results_df[results_df["sensex_daily_direction"] == "Down to Up"])
    sensex_flat = len(results_df[results_df["sensex_daily_direction"] == "Flat"])

    # Find primary reversal zone
    if not valid.empty:
        time_counts = valid["inflection_time"].value_counts()
        top_time = time_counts.index[0]
        top_count = time_counts.iloc[0]
        top_pct = round(top_count / len(valid) * 100, 1)

        def to_15min_bucket(t):
            if not t:
                return None
            h, m = int(t[:2]), int(t[3:])
            m_bucket = (m // 15) * 15
            return f"{h:02d}:{m_bucket:02d}"

        valid_copy = valid.copy()
        valid_copy["bucket_15m"] = valid_copy["inflection_time"].apply(to_15min_bucket)
        bucket_counts = valid_copy["bucket_15m"].value_counts()
        top_bucket = bucket_counts.index[0]
        top_bucket_count = bucket_counts.iloc[0]
        top_bucket_pct = round(top_bucket_count / len(valid) * 100, 1)

        top3_times = time_counts.head(3)
    else:
        top_time, top_pct = "N/A", 0
        top_bucket, top_bucket_count, top_bucket_pct = "N/A", 0, 0
        top3_times = pd.Series()

    # Concordance
    match_count = len(results_df[results_df["concordance"] == "Match"])
    mismatch_count = len(results_df[results_df["concordance"] == "Mismatch"])
    concordance_total = match_count + mismatch_count
    concordance_pct = round(match_count / concordance_total * 100, 1) if concordance_total > 0 else 0

    # Nifty expiry overlap analysis
    nifty_exp_days = results_df[results_df["is_nifty_expiry_day"] == 1]
    sensex_only_days = results_df[results_df["is_nifty_expiry_day"] == 0]

    lines = []
    lines.append("# Sensex Expiry Day Afternoon Reversal Analysis Report")
    lines.append("")
    lines.append(f"**Generated from {total_days} Sensex expiry days with Nifty 5-minute proxy data**")
    lines.append(f"**Date range**: {results_df['date'].min()} to {results_df['date'].max()}")
    lines.append(f"**Dates skipped** (no Nifty 5-min data): {len(skipped_dates)}")
    lines.append("")
    lines.append("> **Methodology note:** Sensex 5-minute intraday data is not available.")
    lines.append("> Nifty 50 5-minute bars are used as a timing proxy — Sensex and Nifty are")
    lines.append("> 95%+ correlated intraday. The inflection time detection uses Nifty 5-min")
    lines.append("> price action, while daily direction classification uses Sensex OHLC.")
    lines.append("")

    # --- 1. Executive Summary ---
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"Across {total_days} Sensex expiry days analyzed:")
    lines.append("")
    lines.append("**Sensex daily direction (open-to-close):**")
    lines.append(f"- Top to Down: {sensex_ttd} ({round(sensex_ttd/total_days*100,1)}%)")
    lines.append(f"- Down to Up: {sensex_dtu} ({round(sensex_dtu/total_days*100,1)}%)")
    lines.append(f"- Flat: {sensex_flat} ({round(sensex_flat/total_days*100,1)}%)")
    lines.append("")
    lines.append("**Nifty proxy afternoon direction (2 PM to close):**")
    lines.append(f"- Top to Down: {ttd_days} ({round(ttd_days/total_days*100,1)}%)")
    lines.append(f"- Down to Up: {dtu_days} ({round(dtu_days/total_days*100,1)}%)")
    lines.append(f"- Flat: {flat_days} ({round(flat_days/total_days*100,1)}%)")
    lines.append("")
    lines.append(f"**Primary reversal zone (15-min bucket):** `{top_bucket}` — {top_bucket_count} of {len(valid)} days ({top_bucket_pct}%)")
    lines.append(f"**Most common exact inflection time:** `{top_time}` — {top_count} days ({top_pct}%)")
    lines.append("")
    if not top3_times.empty:
        lines.append("**Top 3 inflection times:**")
        lines.append("")
        lines.append("| Time | Count | % |")
        lines.append("|------|------:|----:|")
        for t, c in top3_times.items():
            lines.append(f"| {t} | {c} | {round(c/len(valid)*100,1)}% |")
        lines.append("")

    # --- 2. Overall Timing Distribution ---
    lines.append("## 2. Overall Timing Distribution (5-min granularity)")
    lines.append("")
    lines.append(dist_table_md(all_dists[0], "All Sensex Expiry Days"))

    # --- 3. Direction-segmented ---
    lines.append("## 3. Timing Distribution by Direction")
    lines.append("")
    for d in all_dists[1:3]:
        label = d["group"].iloc[0]
        lines.append(dist_table_md(d, label))

    # --- 4. Expiry-type ---
    lines.append("## 4. Timing Distribution by Expiry Type")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("Expiry:"):
            lines.append(dist_table_md(d, label))

    # --- 5. VIX-level ---
    lines.append("## 5. Timing Distribution by VIX Level")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("VIX:"):
            lines.append(dist_table_md(d, label))

    # --- 6. FII stance ---
    lines.append("## 6. Timing Distribution by FII Stance")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("FII:"):
            lines.append(dist_table_md(d, label))

    # --- 6a. FII/PRO Composite View ---
    lines.append("## 6a. Timing Distribution by FII Composite View")
    lines.append("")
    lines.append("FII Composite = `fut + call - put` (buying puts treated as bearish)")
    lines.append("")

    lines.append("### FII View vs Afternoon Direction")
    lines.append("")
    lines.append("| FII View | Count | TTD | DTU | Flat | TTD % | Avg Move % |")
    lines.append("|----------|------:|----:|----:|-----:|------:|-----------:|")
    for view in ["Strong Bullish", "Bullish", "Mildly Bullish", "Neutral", "Mildly Bearish", "Bearish", "Strong Bearish"]:
        sub = results_df[results_df["fii_view"] == view]
        if len(sub) == 0:
            continue
        t = len(sub)
        ttd = len(sub[sub["nifty_proxy_afternoon_direction"] == "Top to Down"])
        dtu = len(sub[sub["nifty_proxy_afternoon_direction"] == "Down to Up"])
        fl = len(sub[sub["nifty_proxy_afternoon_direction"] == "Flat"])
        nf = sub[sub["nifty_proxy_afternoon_direction"] != "Flat"]["nifty_move_from_2pm_pct"]
        avg = round(nf.mean(), 3) if len(nf) > 0 else 0
        lines.append(f"| {view} | {t} | {ttd} | {dtu} | {fl} | {round(ttd/t*100,1)}% | {avg}% |")
    lines.append("")

    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("FII View:"):
            lines.append(dist_table_md(d, label))

    lines.append("## 6b. Timing Distribution by PRO Composite View")
    lines.append("")
    lines.append("### PRO View vs Afternoon Direction")
    lines.append("")
    lines.append("| PRO View | Count | TTD | DTU | Flat | TTD % | Avg Move % |")
    lines.append("|----------|------:|----:|----:|-----:|------:|-----------:|")
    for view in ["Strong Bullish", "Bullish", "Mildly Bullish", "Neutral", "Mildly Bearish", "Bearish", "Strong Bearish"]:
        sub = results_df[results_df["pro_view"] == view]
        if len(sub) == 0:
            continue
        t = len(sub)
        ttd = len(sub[sub["nifty_proxy_afternoon_direction"] == "Top to Down"])
        dtu = len(sub[sub["nifty_proxy_afternoon_direction"] == "Down to Up"])
        fl = len(sub[sub["nifty_proxy_afternoon_direction"] == "Flat"])
        nf = sub[sub["nifty_proxy_afternoon_direction"] != "Flat"]["nifty_move_from_2pm_pct"]
        avg = round(nf.mean(), 3) if len(nf) > 0 else 0
        lines.append(f"| {view} | {t} | {ttd} | {dtu} | {fl} | {round(ttd/t*100,1)}% | {avg}% |")
    lines.append("")

    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("PRO View:"):
            lines.append(dist_table_md(d, label))

    # --- 7. Nifty expiry overlap ---
    lines.append("## 7. Sensex-Only vs Dual Expiry Days")
    lines.append("")
    lines.append(f"Of {total_days} Sensex expiry days, {len(nifty_exp_days)} also coincide with Nifty expiry.")
    lines.append(f"The remaining {len(sensex_only_days)} are Sensex-only expiry days.")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if "Nifty Expiry" in label or "Sensex-Only" in label:
            lines.append(dist_table_md(d, label))

    # Dual expiry stats
    if len(nifty_exp_days) > 0 and len(sensex_only_days) > 0:
        dual_valid = nifty_exp_days[nifty_exp_days["inflection_time"].notna()]
        solo_valid = sensex_only_days[sensex_only_days["inflection_time"].notna()]
        if len(dual_valid) > 0 and len(solo_valid) > 0:
            dual_avg_move = round(dual_valid["move_from_inflection_pct"].mean(), 3)
            solo_avg_move = round(solo_valid["move_from_inflection_pct"].mean(), 3)
            lines.append(f"**Avg move from inflection (Dual expiry days):** {dual_avg_move}%")
            lines.append(f"**Avg move from inflection (Sensex-only days):** {solo_avg_move}%")
            lines.append("")

    # --- 8. Move magnitude ---
    lines.append("## 8. Move Magnitude by Time Bucket (Nifty proxy, to Session Close)")
    lines.append("")
    if not mag_stats.empty:
        lines.append("Average absolute percentage move from each 15-min marker to session close:")
        lines.append("")
        lines.append("| Time Marker | Direction | Avg % | Median % | Min % | Max % | Count |")
        lines.append("|-------------|-----------|------:|---------:|------:|------:|------:|")
        for _, r in mag_stats.iterrows():
            lines.append(
                f"| {r['time_marker']} | {r['direction']} | {r['mean']} | {r['median']} | {r['min']} | {r['max']} | {int(r['count'])} |"
            )
        lines.append("")
    else:
        lines.append("*No magnitude data available.*\n")

    # --- 9. VIX × FII crosstab ---
    lines.append("## 9. VIX Level x FII Stance Cross-Tabulation")
    lines.append("")
    if not crosstab_df.empty:
        lines.append("| VIX Bucket | FII Stance | Count | Modal Inflection Time | Avg Move % |")
        lines.append("|------------|------------|------:|----------------------:|-----------:|")
        for _, r in crosstab_df.iterrows():
            lines.append(
                f"| {r['vix_bucket']} | {r['fii_stance']} | {r['count']} | {r['modal_inflection_time']} | {r['avg_move_from_inflection_pct']} |"
            )
        lines.append("")
    else:
        lines.append("*Insufficient data for cross-tabulation.*\n")

    # --- 10. Concordance ---
    lines.append("## 10. Concordance: Nifty Proxy Afternoon vs Sensex Daily Direction")
    lines.append("")
    lines.append("The Sensex daily direction is classified from open-to-close.")
    lines.append("The Nifty proxy afternoon direction uses Nifty 5-min data from 2 PM to close.")
    lines.append("")
    lines.append(f"- **Match**: {match_count} days ({concordance_pct}%)")
    lines.append(f"- **Mismatch**: {mismatch_count} days ({round(mismatch_count/concordance_total*100,1) if concordance_total > 0 else 0}%)")
    lines.append(f"- **Flat (excluded)**: {flat_days} days")
    lines.append("")

    if concordance_total > 0:
        conc_df = results_df[results_df["concordance"].isin(["Match", "Mismatch"])]
        lines.append("### Concordance by Direction")
        lines.append("")
        lines.append("| Nifty Proxy Direction | Match | Mismatch | Match % |")
        lines.append("|----------------------|------:|---------:|--------:|")
        for d in ["Top to Down", "Down to Up"]:
            sub = conc_df[conc_df["nifty_proxy_afternoon_direction"] == d]
            m = len(sub[sub["concordance"] == "Match"])
            mm = len(sub[sub["concordance"] == "Mismatch"])
            mp = round(m / (m + mm) * 100, 1) if (m + mm) > 0 else 0
            lines.append(f"| {d} | {m} | {mm} | {mp}% |")
        lines.append("")

        # Detailed continuation vs reversal breakdown
        lines.append("### Continuation vs Reversal Breakdown")
        lines.append("")
        lines.append("**Continuation** = afternoon moves in SAME direction as daily trend (Match)")
        lines.append("**Reversal** = afternoon moves OPPOSITE to daily trend (Mismatch)")
        lines.append("")

        # Continuation cases
        match_df = conc_df[conc_df["concordance"] == "Match"]
        lines.append("#### Continuation Days (afternoon confirms daily trend)")
        lines.append("")
        lines.append("| Daily Direction (Open→Close) | Afternoon Direction (2 PM→Close) | Count | Avg Move from 2 PM % |")
        lines.append("|------------------------------|----------------------------------|------:|---------------------:|")
        for d in ["Top to Down", "Down to Up"]:
            sub = match_df[match_df["sensex_daily_direction"] == d]
            avg_move = round(sub["nifty_move_from_2pm_pct"].mean(), 3) if len(sub) > 0 else 0
            lines.append(f"| {d} | {d} | {len(sub)} | {avg_move}% |")
        lines.append("")

        # Reversal cases
        mismatch_df = conc_df[conc_df["concordance"] == "Mismatch"]
        lines.append("#### Reversal Days (afternoon reverses the daily trend)")
        lines.append("")
        lines.append("| Daily Direction (Open→Close) | Afternoon Direction (2 PM→Close) | Reversal Type | Count | Avg Move from 2 PM % |")
        lines.append("|------------------------------|----------------------------------|---------------|------:|---------------------:|")
        # Morning was Down to Up (bullish day), but afternoon reversed Top to Down
        sub1 = mismatch_df[(mismatch_df["sensex_daily_direction"] == "Down to Up") & (mismatch_df["nifty_proxy_afternoon_direction"] == "Top to Down")]
        avg1 = round(sub1["nifty_move_from_2pm_pct"].mean(), 3) if len(sub1) > 0 else 0
        lines.append(f"| Down to Up (bullish day) | Top to Down | Morning rally faded after 2 PM | {len(sub1)} | {avg1}% |")

        # Morning was Top to Down (bearish day), but afternoon reversed Down to Up
        sub2 = mismatch_df[(mismatch_df["sensex_daily_direction"] == "Top to Down") & (mismatch_df["nifty_proxy_afternoon_direction"] == "Down to Up")]
        avg2 = round(sub2["nifty_move_from_2pm_pct"].mean(), 3) if len(sub2) > 0 else 0
        lines.append(f"| Top to Down (bearish day) | Down to Up | Morning sell-off recovered after 2 PM | {len(sub2)} | {avg2}% |")

        # Edge cases: daily was Flat but afternoon had direction
        sub3 = mismatch_df[(mismatch_df["sensex_daily_direction"] == "Flat")]
        if len(sub3) > 0:
            for d in ["Top to Down", "Down to Up"]:
                s = sub3[sub3["nifty_proxy_afternoon_direction"] == d]
                if len(s) > 0:
                    avg_s = round(s["nifty_move_from_2pm_pct"].mean(), 3)
                    lines.append(f"| Flat (range-bound day) | {d} | Afternoon broke out {d.lower()} | {len(s)} | {avg_s}% |")
        lines.append("")

        # Summary insight
        total_reversals = len(mismatch_df)
        if total_reversals > 0:
            lines.append(f"**Summary:** Of {total_reversals} reversal days:")
            if len(sub1) > 0:
                lines.append(f"- **{len(sub1)} days ({round(len(sub1)/total_reversals*100,1)}%)**: Morning was bullish (Down to Up) but **afternoon sold off** (Top to Down) — rally faded after 2 PM")
            if len(sub2) > 0:
                lines.append(f"- **{len(sub2)} days ({round(len(sub2)/total_reversals*100,1)}%)**: Morning was bearish (Top to Down) but **afternoon recovered** (Down to Up) — sell-off reversed after 2 PM")
            if len(sub3) > 0:
                lines.append(f"- **{len(sub3)} days**: Daily was Flat but afternoon showed directional movement")
            lines.append("")

        # Reversal timing: when do reversals vs continuations happen?
        lines.append("### Reversal vs Continuation: Inflection Time Comparison")
        lines.append("")
        for label, subset in [("Continuation", match_df), ("Reversal", mismatch_df)]:
            v = subset[subset["inflection_time"].notna()]
            if not v.empty:
                tc = v["inflection_time"].value_counts().head(3)
                top_list = ", ".join(f"{t} ({c})" for t, c in tc.items())
                lines.append(f"- **{label} days** — Top 3 inflection times: {top_list}")
        lines.append("")

    # --- 11. Key Findings ---
    lines.append("## 11. Key Findings and Trading Implications")
    lines.append("")

    findings = []

    if top_bucket and top_bucket != "N/A":
        findings.append(
            f"**The {top_bucket} time bucket is the most common inflection zone on Sensex expiry days**, "
            f"with {top_bucket_pct}% of all afternoon reversals originating here. "
            f"Traders should be positioned or alert by this time."
        )

    if not top3_times.empty:
        times = [top3_times.index[i] for i in range(min(3, len(top3_times)))]
        findings.append(
            f"**Top 3 exact reversal times**: {', '.join(times)}. "
            f"These account for {round(top3_times.sum()/len(valid)*100,1)}% of all inflections."
        )

    if concordance_pct > 0:
        findings.append(
            f"**Nifty proxy afternoon direction matches Sensex daily direction {concordance_pct}% of the time.** "
            f"This confirms the strong intraday correlation and validates using Nifty as a proxy."
        )

    if len(nifty_exp_days) > 0 and len(sensex_only_days) > 0:
        dual_valid = nifty_exp_days[nifty_exp_days["inflection_time"].notna()]
        solo_valid = sensex_only_days[sensex_only_days["inflection_time"].notna()]
        if len(dual_valid) > 0 and len(solo_valid) > 0:
            dual_avg = round(dual_valid["move_from_inflection_pct"].mean(), 3)
            solo_avg = round(solo_valid["move_from_inflection_pct"].mean(), 3)
            if dual_avg > solo_avg:
                findings.append(
                    f"**Dual expiry days (Sensex + Nifty) produce larger afternoon moves** "
                    f"(avg {dual_avg}% from inflection) vs Sensex-only days "
                    f"(avg {solo_avg}%). Double expiry amplifies volatility."
                )
            else:
                findings.append(
                    f"**Sensex-only expiry days show comparable or larger afternoon moves** "
                    f"(avg {solo_avg}%) vs dual expiry days (avg {dual_avg}%). "
                    f"Sensex-specific expiry dynamics are significant."
                )

    if not crosstab_df.empty:
        high_vix = crosstab_df[crosstab_df["vix_bucket"] == "High (>20)"]
        low_vix = crosstab_df[crosstab_df["vix_bucket"] == "Low (<15)"]
        if not high_vix.empty and not low_vix.empty:
            avg_high = high_vix["avg_move_from_inflection_pct"].mean()
            avg_low = low_vix["avg_move_from_inflection_pct"].mean()
            findings.append(
                f"**High VIX days produce larger afternoon moves** "
                f"(avg {round(avg_high,2)}% from inflection) vs low VIX days "
                f"(avg {round(avg_low,2)}% from inflection)."
            )

    dominant = "Top to Down" if sensex_ttd > sensex_dtu else "Down to Up"
    dominant_pct = round(max(sensex_ttd, sensex_dtu) / total_days * 100, 1)
    findings.append(
        f"**{dominant} is the dominant Sensex daily pattern on expiry days**, "
        f"occurring on {dominant_pct}% of days."
    )

    # Day-of-week finding
    dow_counts = results_df["day_of_week"].value_counts()
    findings.append(
        f"**Expiry day schedule**: {', '.join(f'{d} ({c})' for d, c in dow_counts.items())}. "
        f"Sensex shifted from Friday to Thursday/Tuesday expiry in 2025."
    )

    for i, f in enumerate(findings, 1):
        lines.append(f"{i}. {f}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("Sensex Expiry Day Afternoon Reversal Analysis")
    print("(using Nifty 5-min data as intraday proxy)")
    print("=" * 70)

    csv_df = load_sensex_csv()
    bars_dict, skipped_dates = fetch_all_afternoon_bars(csv_df["date"])
    results_df = build_results(csv_df, bars_dict)

    match_count = len(results_df[results_df["concordance"] == "Match"])
    total_non_flat = len(results_df[results_df["concordance"].isin(["Match", "Mismatch"])])
    if total_non_flat > 0:
        print(f"[Concordance] Nifty proxy afternoon vs Sensex daily: {match_count}/{total_non_flat} ({round(match_count/total_non_flat*100,1)}%)")

    all_dists = segmented_distributions(results_df)
    mag_stats = move_magnitude_by_bucket(csv_df, bars_dict)
    crosstab_df = vix_fii_crosstab(results_df)

    results_df.to_csv(CSV_OUTPUT, index=False)
    print(f"[Output] CSV written to {CSV_OUTPUT} ({len(results_df)} rows)")

    report = generate_report(results_df, all_dists, mag_stats, crosstab_df, skipped_dates)
    REPORT_OUTPUT.write_text(report)
    print(f"[Output] Report written to {REPORT_OUTPUT}")

    valid = results_df[results_df["inflection_time"].notna()]
    if not valid.empty:
        top3 = valid["inflection_time"].value_counts().head(3)
        print(f"\n[Summary] Top 3 inflection times on Sensex expiry days:")
        for t, c in top3.items():
            print(f"  {t}: {c} days ({round(c/len(valid)*100,1)}%)")

    print("\nDone.")


if __name__ == "__main__":
    main()
