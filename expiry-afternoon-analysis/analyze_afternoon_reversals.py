#!/usr/bin/env python3
"""
Expiry Day Afternoon Reversal Analysis
========================================
Joins Nifty expiry-day metadata (CSV) with 5-minute intraday bars (PostgreSQL)
to identify when directional moves begin in the afternoon session (post-2 PM)
on expiry days.

Data sources:
  - vix_fii_t1_intraday_expiry_results.csv (322 expiry days, Jul 2020–Aug 2026)
  - market_data.nifty50_5min (PostgreSQL, 5-min OHLCV, Aug 2020–Aug 2026)

Output:
  - expiry-afternoon-analysis/afternoon_reversal_results.csv
  - expiry-afternoon-analysis/EXPIRY_AFTERNOON_REVERSAL_REPORT.md
"""

import os
import sys
import warnings
from pathlib import Path
from datetime import time as dt_time
from zoneinfo import ZoneInfo

import pandas as pd
import psycopg2

IST = ZoneInfo("Asia/Kolkata")
warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy.*")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "vix_fii_t1_intraday_expiry_results.csv"
OUTPUT_DIR = REPO_ROOT / "expiry-afternoon-analysis"
CSV_OUTPUT = OUTPUT_DIR / "afternoon_reversal_results.csv"
REPORT_OUTPUT = OUTPUT_DIR / "EXPIRY_AFTERNOON_REVERSAL_REPORT.md"

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
# 1. Load CSV
# ---------------------------------------------------------------------------
def load_expiry_csv():
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    cols = [
        "date", "day_of_week", "move_direction", "expiry_type",
        "vix_open", "vix_close",
        "t1_fii_stance", "t1_pro_stance",
        "fii_composite", "fii_view", "pro_composite", "pro_view",
        "nifty_open", "nifty_high", "nifty_low", "nifty_close",
    ]
    df = df[cols].copy()
    print(f"[CSV] Loaded {len(df)} expiry days ({df['date'].min().date()} to {df['date'].max().date()})")
    return df


# ---------------------------------------------------------------------------
# 2. Fetch afternoon 5-min bars from PostgreSQL
# ---------------------------------------------------------------------------
def fetch_afternoon_bars(conn, expiry_date):
    """Return DataFrame of 5-min bars for the afternoon session of a single date."""
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
    """Fetch afternoon bars for all expiry dates. Returns dict[date] -> DataFrame."""
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
        print(f"[DB] Skipped {len(skipped)} dates with no 5-min data: {', '.join(skipped)}")
    print(f"[DB] Fetched afternoon bars for {len(results)} expiry days")
    return results, skipped


# ---------------------------------------------------------------------------
# 3. Classify afternoon direction & detect inflection
# ---------------------------------------------------------------------------
def classify_afternoon(bars_df):
    """
    Given afternoon 5-min bars for a single day, return:
      - afternoon_direction: 'Top to Down', 'Down to Up', or 'Flat'
      - inflection_time: HH:MM string of the inflection candle
      - inflection_price: price at inflection
      - price_at_2pm: open of the 14:00 candle
      - session_close: close of the last candle
    """
    price_at_2pm = float(bars_df.iloc[0]["open"])
    session_close = float(bars_df.iloc[-1]["close"])

    pct_change = abs(session_close - price_at_2pm) / price_at_2pm * 100

    if pct_change < 0.01:
        direction = "Flat"
        inflection_time = None
        inflection_price = None
    elif price_at_2pm > session_close:
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

    return direction, inflection_time, inflection_price, price_at_2pm, session_close


# ---------------------------------------------------------------------------
# 4. Build the analysis results
# ---------------------------------------------------------------------------
def build_results(csv_df, bars_dict):
    rows = []
    for _, row in csv_df.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        if date_str not in bars_dict:
            continue

        bars = bars_dict[date_str]
        direction, infl_time, infl_price, p2pm, sess_close = classify_afternoon(bars)

        concordance = "Match" if direction == row["move_direction"] else "Mismatch"
        if direction == "Flat":
            concordance = "Flat"

        vix_val = float(row["vix_open"])
        vix_bucket = next(
            (label for lo, hi, label in VIX_BUCKETS if lo <= vix_val < hi),
            "High (>20)"
        )

        move_from_2pm_pct = abs(sess_close - p2pm) / p2pm * 100 if p2pm else 0
        move_from_inflection_pct = (
            abs(sess_close - infl_price) / infl_price * 100
            if infl_price else 0
        )

        rows.append({
            "date": date_str,
            "day_of_week": row["day_of_week"],
            "expiry_type": row["expiry_type"],
            "csv_move_direction": row["move_direction"],
            "afternoon_direction": direction,
            "concordance": concordance,
            "vix_open": round(vix_val, 2),
            "vix_close": round(float(row["vix_close"]), 2),
            "vix_bucket": vix_bucket,
            "t1_fii_stance": row["t1_fii_stance"],
            "t1_pro_stance": row["t1_pro_stance"],
            "fii_composite": int(row["fii_composite"]),
            "fii_view": row["fii_view"],
            "pro_composite": int(row["pro_composite"]),
            "pro_view": row["pro_view"],
            "price_at_2pm": round(p2pm, 2),
            "session_close": round(sess_close, 2),
            "inflection_time": infl_time,
            "inflection_price": round(infl_price, 2) if infl_price else None,
            "move_from_inflection_pct": round(move_from_inflection_pct, 3),
            "move_from_2pm_pct": round(move_from_2pm_pct, 3),
        })

    results_df = pd.DataFrame(rows)
    print(f"[Analysis] Built results for {len(results_df)} expiry days")
    return results_df


# ---------------------------------------------------------------------------
# 5. Statistical analysis helpers
# ---------------------------------------------------------------------------
def timing_distribution(df, label="All"):
    """Count inflection times across 5-min slots."""
    valid = df[df["inflection_time"].notna()].copy()
    counts = valid["inflection_time"].value_counts().reindex(ALL_SLOTS, fill_value=0)
    total = counts.sum()
    pct = (counts / total * 100).round(1) if total > 0 else counts * 0
    dist = pd.DataFrame({"time": counts.index, "count": counts.values, "pct": pct.values})
    dist["group"] = label
    return dist, total


def segmented_distributions(df):
    """Build timing distributions for various segments."""
    all_dists = []

    # Overall
    d, _ = timing_distribution(df, "All Expiry Days")
    all_dists.append(d)

    # By direction
    for direction in ["Top to Down", "Down to Up"]:
        sub = df[df["afternoon_direction"] == direction]
        d, _ = timing_distribution(sub, direction)
        all_dists.append(d)

    # By expiry type
    for etype in ["weekly", "monthly"]:
        sub = df[df["expiry_type"] == etype]
        d, _ = timing_distribution(sub, f"Expiry: {etype}")
        all_dists.append(d)

    # By VIX bucket
    for _, _, label in VIX_BUCKETS:
        sub = df[df["vix_bucket"] == label]
        d, _ = timing_distribution(sub, f"VIX: {label}")
        all_dists.append(d)

    # By FII stance (top categories only)
    for stance in df["t1_fii_stance"].value_counts().head(6).index:
        sub = df[df["t1_fii_stance"] == stance]
        if len(sub) >= 5:
            d, _ = timing_distribution(sub, f"FII: {stance}")
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
    """
    For each 15-min marker (14:00, 14:15, 14:30, 14:45, 15:00),
    compute stats of |candle_open - session_close| / candle_open * 100.
    """
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
    """Cross-tabulation of VIX bucket × FII stance → modal inflection time + avg magnitude."""
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
    """Format a timing distribution DataFrame as a markdown table."""
    lines = [f"### {title}\n"]
    # Only show non-zero rows for compactness, but always show the full table
    lines.append("| Time | Count | % |")
    lines.append("|------|------:|----:|")
    for _, r in dist_df.iterrows():
        lines.append(f"| {r['time']} | {int(r['count'])} | {r['pct']}% |")
    lines.append("")
    return "\n".join(lines)


def generate_report(results_df, all_dists, mag_stats, crosstab_df, skipped_dates):
    """Generate the full markdown report."""
    valid = results_df[results_df["inflection_time"].notna()]
    total_days = len(results_df)
    flat_days = len(results_df[results_df["afternoon_direction"] == "Flat"])
    ttd_days = len(results_df[results_df["afternoon_direction"] == "Top to Down"])
    dtu_days = len(results_df[results_df["afternoon_direction"] == "Down to Up"])

    # Find primary reversal zone
    if not valid.empty:
        time_counts = valid["inflection_time"].value_counts()
        top_time = time_counts.index[0]
        top_count = time_counts.iloc[0]
        top_pct = round(top_count / len(valid) * 100, 1)

        # Find the 15-min window with most inflections
        valid_copy = valid.copy()
        valid_copy["infl_hour_min"] = valid_copy["inflection_time"].apply(
            lambda x: x[:4] + "0" if x else None  # round to 15-min: 14:00, 14:10->14:00, etc.
        )
        # Better: group by 15-min buckets
        def to_15min_bucket(t):
            if not t:
                return None
            h, m = int(t[:2]), int(t[3:])
            m_bucket = (m // 15) * 15
            return f"{h:02d}:{m_bucket:02d}"

        valid_copy["bucket_15m"] = valid_copy["inflection_time"].apply(to_15min_bucket)
        bucket_counts = valid_copy["bucket_15m"].value_counts()
        top_bucket = bucket_counts.index[0]
        top_bucket_count = bucket_counts.iloc[0]
        top_bucket_pct = round(top_bucket_count / len(valid) * 100, 1)

        # Top 3 individual times
        top3_times = time_counts.head(3)
    else:
        top_time = "N/A"
        top_pct = 0
        top_bucket = "N/A"
        top_bucket_pct = 0
        top3_times = pd.Series()

    # Concordance stats
    match_count = len(results_df[results_df["concordance"] == "Match"])
    mismatch_count = len(results_df[results_df["concordance"] == "Mismatch"])
    concordance_pct = round(match_count / (match_count + mismatch_count) * 100, 1) if (match_count + mismatch_count) > 0 else 0

    lines = []
    lines.append("# Expiry Day Afternoon Reversal Analysis Report")
    lines.append("")
    lines.append(f"**Generated from {total_days} expiry days with 5-minute intraday data**")
    lines.append(f"**Date range**: {results_df['date'].min()} to {results_df['date'].max()}")
    lines.append(f"**Dates skipped** (no 5-min data): {len(skipped_dates)}")
    lines.append("")

    # --- 1. Executive Summary ---
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"Across {total_days} Nifty expiry days analyzed:")
    lines.append(f"- **Top to Down** afternoons: {ttd_days} ({round(ttd_days/total_days*100,1)}%)")
    lines.append(f"- **Down to Up** afternoons: {dtu_days} ({round(dtu_days/total_days*100,1)}%)")
    lines.append(f"- **Flat** afternoons: {flat_days} ({round(flat_days/total_days*100,1)}%)")
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
    overall_dist = all_dists[0]
    lines.append(dist_table_md(overall_dist, "All Expiry Days"))

    # --- 3. Direction-segmented distributions ---
    lines.append("## 3. Timing Distribution by Direction")
    lines.append("")
    for d in all_dists[1:3]:
        label = d["group"].iloc[0]
        lines.append(dist_table_md(d, label))

    # --- 4. Expiry-type breakdown ---
    lines.append("## 4. Timing Distribution by Expiry Type")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("Expiry:"):
            lines.append(dist_table_md(d, label))

    # --- 5. VIX-level breakdown ---
    lines.append("## 5. Timing Distribution by VIX Level")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("VIX:"):
            lines.append(dist_table_md(d, label))

    # --- 6. FII stance breakdown ---
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

    # FII View summary table
    lines.append("### FII View vs Afternoon Direction")
    lines.append("")
    lines.append("| FII View | Count | TTD | DTU | Flat | TTD % | Avg Move % |")
    lines.append("|----------|------:|----:|----:|-----:|------:|-----------:|")
    for view in ["Strong Bullish", "Bullish", "Mildly Bullish", "Neutral", "Mildly Bearish", "Bearish", "Strong Bearish"]:
        sub = results_df[results_df["fii_view"] == view]
        if len(sub) == 0:
            continue
        t = len(sub)
        ttd = len(sub[sub["afternoon_direction"] == "Top to Down"])
        dtu = len(sub[sub["afternoon_direction"] == "Down to Up"])
        fl = len(sub[sub["afternoon_direction"] == "Flat"])
        nf = sub[sub["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
        avg = round(nf.mean(), 3) if len(nf) > 0 else 0
        lines.append(f"| {view} | {t} | {ttd} | {dtu} | {fl} | {round(ttd/t*100,1)}% | {avg}% |")
    lines.append("")

    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("FII View:"):
            lines.append(dist_table_md(d, label))

    lines.append("## 6b. Timing Distribution by PRO Composite View")
    lines.append("")
    lines.append("PRO Composite = `fut + call - put`")
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
        ttd = len(sub[sub["afternoon_direction"] == "Top to Down"])
        dtu = len(sub[sub["afternoon_direction"] == "Down to Up"])
        fl = len(sub[sub["afternoon_direction"] == "Flat"])
        nf = sub[sub["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
        avg = round(nf.mean(), 3) if len(nf) > 0 else 0
        lines.append(f"| {view} | {t} | {ttd} | {dtu} | {fl} | {round(ttd/t*100,1)}% | {avg}% |")
    lines.append("")

    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("PRO View:"):
            lines.append(dist_table_md(d, label))

    # --- 7. Move magnitude by time bucket ---
    lines.append("## 7. Move Magnitude by Time Bucket (to Session Close)")
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

    # --- 8. VIX × FII cross-tabulation ---
    lines.append("## 8. VIX Level x FII Stance Cross-Tabulation")
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

    # --- 9. Concordance analysis ---
    lines.append("## 9. Concordance: Afternoon vs Full-Day Direction")
    lines.append("")
    lines.append(f"The full-day `move_direction` from the CSV classifies each day based on open-to-close.")
    lines.append(f"The afternoon classification uses only the 2 PM to 3:30 PM session.")
    lines.append("")
    lines.append(f"- **Match**: {match_count} days ({concordance_pct}%)")
    lines.append(f"- **Mismatch**: {mismatch_count} days ({round(mismatch_count/(match_count+mismatch_count)*100,1) if (match_count+mismatch_count)>0 else 0}%)")
    lines.append(f"- **Flat (excluded)**: {flat_days} days")
    lines.append("")
    lines.append("A high concordance rate means the afternoon direction is consistent with the full-day trend.")
    lines.append("A mismatch means the morning session moved opposite to the afternoon — the reversal happened before 2 PM.")
    lines.append("")

    # Concordance by direction
    if match_count + mismatch_count > 0:
        conc_df = results_df[results_df["concordance"].isin(["Match", "Mismatch"])]
        lines.append("### Concordance by Direction")
        lines.append("")
        lines.append("| Afternoon Direction | Match | Mismatch | Match % |")
        lines.append("|---------------------|------:|---------:|--------:|")
        for d in ["Top to Down", "Down to Up"]:
            sub = conc_df[conc_df["afternoon_direction"] == d]
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
            sub = match_df[match_df["csv_move_direction"] == d]
            avg_move = round(sub["move_from_2pm_pct"].mean(), 3) if len(sub) > 0 else 0
            lines.append(f"| {d} | {d} | {len(sub)} | {avg_move}% |")
        lines.append("")

        # Reversal cases
        mismatch_df = conc_df[conc_df["concordance"] == "Mismatch"]
        lines.append("#### Reversal Days (afternoon reverses the daily trend)")
        lines.append("")
        lines.append("| Daily Direction (Open→Close) | Afternoon Direction (2 PM→Close) | Reversal Type | Count | Avg Move from 2 PM % |")
        lines.append("|------------------------------|----------------------------------|---------------|------:|---------------------:|")
        # Morning was Down to Up (bullish day), but afternoon reversed Top to Down
        sub1 = mismatch_df[(mismatch_df["csv_move_direction"] == "Down to Up") & (mismatch_df["afternoon_direction"] == "Top to Down")]
        avg1 = round(sub1["move_from_2pm_pct"].mean(), 3) if len(sub1) > 0 else 0
        lines.append(f"| Down to Up (bullish day) | Top to Down | Morning rally faded after 2 PM | {len(sub1)} | {avg1}% |")

        # Morning was Top to Down (bearish day), but afternoon reversed Down to Up
        sub2 = mismatch_df[(mismatch_df["csv_move_direction"] == "Top to Down") & (mismatch_df["afternoon_direction"] == "Down to Up")]
        avg2 = round(sub2["move_from_2pm_pct"].mean(), 3) if len(sub2) > 0 else 0
        lines.append(f"| Top to Down (bearish day) | Down to Up | Morning sell-off recovered after 2 PM | {len(sub2)} | {avg2}% |")
        lines.append("")

        # Summary insight
        total_reversals = len(mismatch_df)
        if total_reversals > 0:
            lines.append(f"**Summary:** Of {total_reversals} reversal days:")
            if len(sub1) > 0:
                lines.append(f"- **{len(sub1)} days ({round(len(sub1)/total_reversals*100,1)}%)**: Morning was bullish (Down to Up) but **afternoon sold off** (Top to Down) — rally faded after 2 PM")
            if len(sub2) > 0:
                lines.append(f"- **{len(sub2)} days ({round(len(sub2)/total_reversals*100,1)}%)**: Morning was bearish (Top to Down) but **afternoon recovered** (Down to Up) — sell-off reversed after 2 PM")
            lines.append("")

        # Reversal timing
        lines.append("### Reversal vs Continuation: Inflection Time Comparison")
        lines.append("")
        for label, subset in [("Continuation", match_df), ("Reversal", mismatch_df)]:
            v = subset[subset["inflection_time"].notna()]
            if not v.empty:
                tc = v["inflection_time"].value_counts().head(3)
                top_list = ", ".join(f"{t} ({c})" for t, c in tc.items())
                lines.append(f"- **{label} days** — Top 3 inflection times: {top_list}")
        lines.append("")

    # --- 10. Key Findings ---
    lines.append("## 10. Key Findings and Trading Implications")
    lines.append("")

    # Auto-generate key findings
    findings = []

    if top_bucket and top_bucket != "N/A":
        findings.append(
            f"**The {top_bucket} time bucket is the most common inflection zone**, "
            f"with {top_bucket_pct}% of all expiry day afternoon reversals originating here. "
            f"Traders should be positioned or alert by this time."
        )

    if not top3_times.empty:
        t1, t2, t3 = top3_times.index[0], top3_times.index[1] if len(top3_times) > 1 else "N/A", top3_times.index[2] if len(top3_times) > 2 else "N/A"
        findings.append(
            f"**Top 3 exact reversal times**: {t1}, {t2}, {t3}. "
            f"These three times alone account for "
            f"{round(top3_times.sum()/len(valid)*100,1)}% of all inflections."
        )

    if concordance_pct > 0:
        findings.append(
            f"**Afternoon direction matches full-day direction {concordance_pct}% of the time.** "
            f"This means the post-2 PM move usually confirms the daily trend rather than reversing it."
        )

    # VIX-based finding
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

    ttd_pct_val = round(ttd_days / total_days * 100, 1) if total_days > 0 else 0
    dtu_pct_val = round(dtu_days / total_days * 100, 1) if total_days > 0 else 0
    dominant = "Top to Down" if ttd_days > dtu_days else "Down to Up"
    dominant_pct = max(ttd_pct_val, dtu_pct_val)
    findings.append(
        f"**{dominant} is the dominant afternoon pattern**, occurring on {dominant_pct}% of expiry days. "
        f"This aligns with the general tendency of option premium decay pulling prices in the closing hours."
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
    print("Expiry Day Afternoon Reversal Analysis")
    print("=" * 70)

    # 1. Load CSV
    csv_df = load_expiry_csv()

    # 2. Fetch 5-min bars
    bars_dict, skipped_dates = fetch_all_afternoon_bars(csv_df["date"])

    # 3-4. Build results (classification + inflection detection)
    results_df = build_results(csv_df, bars_dict)

    # Print concordance summary
    match_count = len(results_df[results_df["concordance"] == "Match"])
    total_non_flat = len(results_df[results_df["concordance"].isin(["Match", "Mismatch"])])
    if total_non_flat > 0:
        print(f"[Concordance] Afternoon vs full-day direction match: {match_count}/{total_non_flat} ({round(match_count/total_non_flat*100,1)}%)")

    # 5. Statistical analysis
    all_dists = segmented_distributions(results_df)
    mag_stats = move_magnitude_by_bucket(csv_df, bars_dict)
    crosstab_df = vix_fii_crosstab(results_df)

    # 6. Write CSV
    results_df.to_csv(CSV_OUTPUT, index=False)
    print(f"[Output] CSV written to {CSV_OUTPUT} ({len(results_df)} rows)")

    # 7. Generate report
    report = generate_report(results_df, all_dists, mag_stats, crosstab_df, skipped_dates)
    REPORT_OUTPUT.write_text(report)
    print(f"[Output] Report written to {REPORT_OUTPUT}")

    # Summary
    valid = results_df[results_df["inflection_time"].notna()]
    if not valid.empty:
        top3 = valid["inflection_time"].value_counts().head(3)
        print(f"\n[Summary] Top 3 inflection times:")
        for t, c in top3.items():
            print(f"  {t}: {c} days ({round(c/len(valid)*100,1)}%)")

    print("\nDone.")


if __name__ == "__main__":
    main()
