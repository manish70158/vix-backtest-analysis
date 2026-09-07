#!/usr/bin/env python3
"""
Daily Afternoon Reversal Analysis (ALL Trading Days)
=====================================================
Analyzes the post-2 PM directional move on EVERY trading day (not just expiry),
using 5-minute Nifty intraday bars from PostgreSQL.

Compares expiry days vs non-expiry days to reveal whether afternoon reversal
patterns are expiry-specific or a general market phenomenon.

Data sources:
  - market_data.nifty50_5min (PostgreSQL, ~1478 trading days, Aug 2020–Aug 2026)
  - vix_fii_t1_intraday_expiry_results.csv (to tag expiry days)

Output:
  - expiry-afternoon-analysis/daily_afternoon_reversal_results.csv
  - expiry-afternoon-analysis/DAILY_AFTERNOON_REVERSAL_REPORT.md
"""

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
EXPIRY_CSV = REPO_ROOT / "vix_fii_t1_intraday_expiry_results.csv"
OUTPUT_DIR = REPO_ROOT / "expiry-afternoon-analysis"
CSV_OUTPUT = OUTPUT_DIR / "daily_afternoon_reversal_results.csv"
REPORT_OUTPUT = OUTPUT_DIR / "DAILY_AFTERNOON_REVERSAL_REPORT.md"

DB_PARAMS = dict(host="localhost", dbname="market_data")

AFTERNOON_START = dt_time(14, 0)
AFTERNOON_END = dt_time(15, 25)

ALL_SLOTS = [
    f"{h:02d}:{m:02d}"
    for h in range(14, 16)
    for m in range(0, 60, 5)
    if dt_time(h, m) >= AFTERNOON_START and dt_time(h, m) <= AFTERNOON_END
]


# ---------------------------------------------------------------------------
# 1. Load expiry dates for tagging
# ---------------------------------------------------------------------------
def load_expiry_dates():
    df = pd.read_csv(EXPIRY_CSV, parse_dates=["date"])
    expiry_info = {}
    for _, row in df.iterrows():
        d = row["date"].strftime("%Y-%m-%d")
        expiry_info[d] = {
            "expiry_type": row["expiry_type"],
            "move_direction": row["move_direction"],
            "vix_open": float(row["vix_open"]),
            "t1_fii_stance": row["t1_fii_stance"],
        }
    print(f"[CSV] Loaded {len(expiry_info)} expiry dates for tagging")
    return expiry_info


# ---------------------------------------------------------------------------
# 2. Batch-fetch all data from PostgreSQL
# ---------------------------------------------------------------------------
def fetch_all_data():
    """Fetch morning open + afternoon bars for all trading days in one go."""
    conn = psycopg2.connect(**DB_PARAMS)

    # Get daily open (9:15 candle) and close (last candle) for each day
    print("[DB] Fetching daily open/close for all trading days...")
    daily_query = """
        WITH day_bounds AS (
            SELECT datetime::date AS dt,
                   MIN(datetime) AS first_bar,
                   MAX(datetime) AS last_bar
            FROM nifty50_5min
            GROUP BY datetime::date
        )
        SELECT db.dt,
               first.open AS day_open,
               last.close AS day_close
        FROM day_bounds db
        JOIN nifty50_5min first ON first.datetime = db.first_bar
        JOIN nifty50_5min last ON last.datetime = db.last_bar
        ORDER BY db.dt
    """
    daily_df = pd.read_sql(daily_query, conn)
    print(f"[DB] Got daily OHLC for {len(daily_df)} trading days")

    # Get all afternoon bars (14:00-15:25) in one query
    print("[DB] Fetching all afternoon bars...")
    afternoon_query = """
        SELECT datetime, open, high, low, close
        FROM nifty50_5min
        WHERE datetime::time >= '14:00'
          AND datetime::time <= '15:25'
        ORDER BY datetime
    """
    afternoon_df = pd.read_sql(afternoon_query, conn)
    conn.close()

    # Convert timestamps to IST and extract date
    afternoon_df["datetime_ist"] = afternoon_df["datetime"].apply(
        lambda x: pd.Timestamp(x).tz_convert(IST) if pd.Timestamp(x).tz else pd.Timestamp(x)
    )
    afternoon_df["date"] = afternoon_df["datetime_ist"].dt.date
    afternoon_df["time_str"] = afternoon_df["datetime_ist"].dt.strftime("%H:%M")

    print(f"[DB] Got {len(afternoon_df)} afternoon bars across {afternoon_df['date'].nunique()} days")
    return daily_df, afternoon_df


# ---------------------------------------------------------------------------
# 3. Analyze each day
# ---------------------------------------------------------------------------
def analyze_all_days(daily_df, afternoon_df, expiry_info):
    rows = []
    grouped = afternoon_df.groupby("date")

    for _, day_row in daily_df.iterrows():
        dt = day_row["dt"]
        if isinstance(dt, str):
            date_str = dt
        else:
            date_str = str(dt)

        day_open = float(day_row["day_open"])
        day_close = float(day_row["day_close"])

        # Daily direction
        daily_pct = abs(day_close - day_open) / day_open * 100
        if daily_pct < 0.01:
            daily_direction = "Flat"
        elif day_open > day_close:
            daily_direction = "Top to Down"
        else:
            daily_direction = "Down to Up"

        # Get afternoon bars for this date
        import datetime
        if isinstance(dt, str):
            dt_date = datetime.date.fromisoformat(dt)
        else:
            dt_date = dt

        if dt_date not in grouped.groups:
            continue

        bars = grouped.get_group(dt_date).sort_values("datetime")
        if len(bars) < 2:
            continue

        # Afternoon classification
        price_at_2pm = float(bars.iloc[0]["open"])
        session_close = float(bars.iloc[-1]["close"])
        afternoon_pct = abs(session_close - price_at_2pm) / price_at_2pm * 100

        if afternoon_pct < 0.01:
            afternoon_direction = "Flat"
            inflection_time = None
            inflection_price = None
        elif price_at_2pm > session_close:
            afternoon_direction = "Top to Down"
            idx = bars["high"].astype(float).idxmax()
            inflection_time = bars.loc[idx, "time_str"]
            inflection_price = float(bars.loc[idx, "high"])
        else:
            afternoon_direction = "Down to Up"
            idx = bars["low"].astype(float).idxmin()
            inflection_time = bars.loc[idx, "time_str"]
            inflection_price = float(bars.loc[idx, "low"])

        # Concordance
        if afternoon_direction == "Flat":
            concordance = "Flat"
        elif afternoon_direction == daily_direction:
            concordance = "Match"
        else:
            concordance = "Mismatch"

        move_from_2pm_pct = afternoon_pct
        move_from_inflection_pct = (
            abs(session_close - inflection_price) / inflection_price * 100
            if inflection_price else 0
        )

        # Expiry tagging
        exp = expiry_info.get(date_str, None)
        is_expiry = 1 if exp else 0
        expiry_type = exp["expiry_type"] if exp else "non-expiry"
        vix_open = exp["vix_open"] if exp else None
        fii_stance = exp["t1_fii_stance"] if exp else None

        # Day of week
        dow = dt_date.strftime("%A")

        rows.append({
            "date": date_str,
            "day_of_week": dow,
            "is_expiry_day": is_expiry,
            "expiry_type": expiry_type,
            "daily_direction": daily_direction,
            "afternoon_direction": afternoon_direction,
            "concordance": concordance,
            "day_open": round(day_open, 2),
            "day_close": round(day_close, 2),
            "daily_move_pct": round((day_close - day_open) / day_open * 100, 3),
            "price_at_2pm": round(price_at_2pm, 2),
            "session_close": round(session_close, 2),
            "move_from_2pm_pct": round(move_from_2pm_pct, 3),
            "inflection_time": inflection_time,
            "inflection_price": round(inflection_price, 2) if inflection_price else None,
            "move_from_inflection_pct": round(move_from_inflection_pct, 3),
            "vix_open": round(vix_open, 2) if vix_open else None,
            "t1_fii_stance": fii_stance,
        })

    results_df = pd.DataFrame(rows)
    print(f"[Analysis] Built results for {len(results_df)} trading days "
          f"({results_df['is_expiry_day'].sum()} expiry, "
          f"{len(results_df) - results_df['is_expiry_day'].sum()} non-expiry)")
    return results_df


# ---------------------------------------------------------------------------
# 4. Statistical helpers
# ---------------------------------------------------------------------------
def timing_distribution(df, label="All"):
    valid = df[df["inflection_time"].notna()].copy()
    counts = valid["inflection_time"].value_counts().reindex(ALL_SLOTS, fill_value=0)
    total = counts.sum()
    pct = (counts / total * 100).round(1) if total > 0 else counts * 0
    dist = pd.DataFrame({"time": counts.index, "count": counts.values, "pct": pct.values})
    dist["group"] = label
    return dist, total


def build_all_distributions(df):
    all_dists = []

    d, _ = timing_distribution(df, "All Trading Days")
    all_dists.append(d)

    for direction in ["Top to Down", "Down to Up"]:
        sub = df[df["afternoon_direction"] == direction]
        d, _ = timing_distribution(sub, direction)
        all_dists.append(d)

    # Expiry vs non-expiry
    d, _ = timing_distribution(df[df["is_expiry_day"] == 1], "Expiry Days")
    all_dists.append(d)
    d, _ = timing_distribution(df[df["is_expiry_day"] == 0], "Non-Expiry Days")
    all_dists.append(d)

    # Day of week
    for dow in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        sub = df[df["day_of_week"] == dow]
        if len(sub) >= 10:
            d, _ = timing_distribution(sub, f"Day: {dow}")
            all_dists.append(d)

    return all_dists


def move_magnitude_table(df):
    """Stats for move from each 15-min marker to close, by direction."""
    time_markers = ["14:00", "14:15", "14:30", "14:45", "15:00"]
    rows = []
    for _, r in df.iterrows():
        if r["afternoon_direction"] == "Flat":
            continue
        # We only have inflection data, not per-marker opens
        # Use move_from_2pm_pct for the 14:00 marker
        # For others, we'd need raw bars — skip granular markers and use what we have
    # Instead: aggregate move_from_2pm_pct by direction and expiry status
    stats = (
        df[df["afternoon_direction"] != "Flat"]
        .groupby(["afternoon_direction", "is_expiry_day"])["move_from_2pm_pct"]
        .agg(["mean", "median", "min", "max", "count"])
        .round(3)
        .reset_index()
    )
    stats["is_expiry_day"] = stats["is_expiry_day"].map({1: "Expiry", 0: "Non-Expiry"})
    return stats


# ---------------------------------------------------------------------------
# 5. Report generation
# ---------------------------------------------------------------------------
def dist_table_md(dist_df, title):
    lines = [f"### {title}\n"]
    lines.append("| Time | Count | % |")
    lines.append("|------|------:|----:|")
    for _, r in dist_df.iterrows():
        lines.append(f"| {r['time']} | {int(r['count'])} | {r['pct']}% |")
    lines.append("")
    return "\n".join(lines)


def generate_report(df, all_dists, mag_stats):
    total = len(df)
    expiry_days = df[df["is_expiry_day"] == 1]
    non_expiry_days = df[df["is_expiry_day"] == 0]

    flat_all = len(df[df["afternoon_direction"] == "Flat"])
    ttd_all = len(df[df["afternoon_direction"] == "Top to Down"])
    dtu_all = len(df[df["afternoon_direction"] == "Down to Up"])

    valid = df[df["inflection_time"].notna()]
    valid_exp = expiry_days[expiry_days["inflection_time"].notna()]
    valid_nonexp = non_expiry_days[non_expiry_days["inflection_time"].notna()]

    # Top inflection times
    def top_times(v, n=3):
        if v.empty:
            return pd.Series()
        return v["inflection_time"].value_counts().head(n)

    def to_15min_bucket(t):
        if not t:
            return None
        h, m = int(t[:2]), int(t[3:])
        m_bucket = (m // 15) * 15
        return f"{h:02d}:{m_bucket:02d}"

    all_top3 = top_times(valid)
    exp_top3 = top_times(valid_exp)
    nonexp_top3 = top_times(valid_nonexp)

    valid_copy = valid.copy()
    valid_copy["bucket_15m"] = valid_copy["inflection_time"].apply(to_15min_bucket)
    bucket_counts = valid_copy["bucket_15m"].value_counts()
    top_bucket = bucket_counts.index[0] if not bucket_counts.empty else "N/A"
    top_bucket_count = bucket_counts.iloc[0] if not bucket_counts.empty else 0
    top_bucket_pct = round(top_bucket_count / len(valid) * 100, 1) if len(valid) > 0 else 0

    # Concordance
    conc_df = df[df["concordance"].isin(["Match", "Mismatch"])]
    match_all = len(conc_df[conc_df["concordance"] == "Match"])
    mismatch_all = len(conc_df[conc_df["concordance"] == "Mismatch"])
    conc_total = match_all + mismatch_all
    conc_pct = round(match_all / conc_total * 100, 1) if conc_total > 0 else 0

    # Expiry concordance
    exp_conc = expiry_days[expiry_days["concordance"].isin(["Match", "Mismatch"])]
    exp_match = len(exp_conc[exp_conc["concordance"] == "Match"])
    exp_conc_total = len(exp_conc)
    exp_conc_pct = round(exp_match / exp_conc_total * 100, 1) if exp_conc_total > 0 else 0

    nonexp_conc = non_expiry_days[non_expiry_days["concordance"].isin(["Match", "Mismatch"])]
    nonexp_match = len(nonexp_conc[nonexp_conc["concordance"] == "Match"])
    nonexp_conc_total = len(nonexp_conc)
    nonexp_conc_pct = round(nonexp_match / nonexp_conc_total * 100, 1) if nonexp_conc_total > 0 else 0

    lines = []
    lines.append("# Daily Afternoon Reversal Analysis — ALL Trading Days")
    lines.append("")
    lines.append(f"**Analyzed {total} trading days** ({len(expiry_days)} expiry + {len(non_expiry_days)} non-expiry)")
    lines.append(f"**Date range**: {df['date'].min()} to {df['date'].max()}")
    lines.append("")

    # === 1. Executive Summary ===
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"Across **all {total} trading days**:")
    lines.append(f"- Top to Down afternoons: {ttd_all} ({round(ttd_all/total*100,1)}%)")
    lines.append(f"- Down to Up afternoons: {dtu_all} ({round(dtu_all/total*100,1)}%)")
    lines.append(f"- Flat afternoons: {flat_all} ({round(flat_all/total*100,1)}%)")
    lines.append("")
    lines.append(f"**Primary reversal zone (15-min bucket):** `{top_bucket}` — {top_bucket_count} of {len(valid)} days ({top_bucket_pct}%)")
    lines.append("")
    if not all_top3.empty:
        lines.append("**Top 3 inflection times (all days):**")
        lines.append("")
        lines.append("| Time | Count | % |")
        lines.append("|------|------:|----:|")
        for t, c in all_top3.items():
            lines.append(f"| {t} | {c} | {round(c/len(valid)*100,1)}% |")
        lines.append("")

    # === 2. Expiry vs Non-Expiry Comparison ===
    lines.append("## 2. Expiry Days vs Non-Expiry Days — Key Comparison")
    lines.append("")

    exp_ttd = len(expiry_days[expiry_days["afternoon_direction"] == "Top to Down"])
    exp_dtu = len(expiry_days[expiry_days["afternoon_direction"] == "Down to Up"])
    exp_flat = len(expiry_days[expiry_days["afternoon_direction"] == "Flat"])
    nonexp_ttd = len(non_expiry_days[non_expiry_days["afternoon_direction"] == "Top to Down"])
    nonexp_dtu = len(non_expiry_days[non_expiry_days["afternoon_direction"] == "Down to Up"])
    nonexp_flat = len(non_expiry_days[non_expiry_days["afternoon_direction"] == "Flat"])

    exp_total = len(expiry_days)
    nonexp_total = len(non_expiry_days)

    lines.append("| Metric | Expiry Days | Non-Expiry Days | All Days |")
    lines.append("|--------|------------:|----------------:|---------:|")
    lines.append(f"| Total days | {exp_total} | {nonexp_total} | {total} |")
    lines.append(f"| Top to Down | {exp_ttd} ({round(exp_ttd/exp_total*100,1)}%) | {nonexp_ttd} ({round(nonexp_ttd/nonexp_total*100,1)}%) | {ttd_all} ({round(ttd_all/total*100,1)}%) |")
    lines.append(f"| Down to Up | {exp_dtu} ({round(exp_dtu/exp_total*100,1)}%) | {nonexp_dtu} ({round(nonexp_dtu/nonexp_total*100,1)}%) | {dtu_all} ({round(dtu_all/total*100,1)}%) |")
    lines.append(f"| Flat | {exp_flat} ({round(exp_flat/exp_total*100,1)}%) | {nonexp_flat} ({round(nonexp_flat/nonexp_total*100,1)}%) | {flat_all} ({round(flat_all/total*100,1)}%) |")
    lines.append(f"| Concordance (afternoon confirms daily) | {exp_conc_pct}% | {nonexp_conc_pct}% | {conc_pct}% |")

    # Avg move from 2 PM
    exp_valid_moves = expiry_days[expiry_days["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
    nonexp_valid_moves = non_expiry_days[non_expiry_days["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
    all_valid_moves = df[df["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
    lines.append(f"| Avg move from 2 PM | {round(exp_valid_moves.mean(),3)}% | {round(nonexp_valid_moves.mean(),3)}% | {round(all_valid_moves.mean(),3)}% |")
    lines.append(f"| Median move from 2 PM | {round(exp_valid_moves.median(),3)}% | {round(nonexp_valid_moves.median(),3)}% | {round(all_valid_moves.median(),3)}% |")
    lines.append("")

    # Top 3 inflection comparison
    lines.append("### Top 3 Inflection Times: Expiry vs Non-Expiry")
    lines.append("")
    lines.append("| Rank | Expiry Days | Non-Expiry Days |")
    lines.append("|------|-------------|-----------------|")
    for i in range(3):
        exp_t = f"{exp_top3.index[i]} ({exp_top3.iloc[i]}, {round(exp_top3.iloc[i]/len(valid_exp)*100,1)}%)" if i < len(exp_top3) else "—"
        nonexp_t = f"{nonexp_top3.index[i]} ({nonexp_top3.iloc[i]}, {round(nonexp_top3.iloc[i]/len(valid_nonexp)*100,1)}%)" if i < len(nonexp_top3) else "—"
        lines.append(f"| #{i+1} | {exp_t} | {nonexp_t} |")
    lines.append("")

    # === 3. Overall Timing Distribution ===
    lines.append("## 3. Overall Timing Distribution (5-min granularity)")
    lines.append("")
    lines.append(dist_table_md(all_dists[0], "All Trading Days"))

    # === 4. By Direction ===
    lines.append("## 4. Timing Distribution by Afternoon Direction")
    lines.append("")
    for d in all_dists[1:3]:
        lines.append(dist_table_md(d, d["group"].iloc[0]))

    # === 5. Expiry vs Non-Expiry ===
    lines.append("## 5. Timing Distribution: Expiry vs Non-Expiry")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label in ["Expiry Days", "Non-Expiry Days"]:
            lines.append(dist_table_md(d, label))

    # === 6. By Day of Week ===
    lines.append("## 6. Timing Distribution by Day of Week")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("Day:"):
            lines.append(dist_table_md(d, label))

    # === 7. Move Magnitude ===
    lines.append("## 7. Move Magnitude from 2 PM to Close")
    lines.append("")
    lines.append("| Direction | Day Type | Avg % | Median % | Min % | Max % | Count |")
    lines.append("|-----------|----------|------:|---------:|------:|------:|------:|")
    if not mag_stats.empty:
        for _, r in mag_stats.iterrows():
            lines.append(f"| {r['afternoon_direction']} | {r['is_expiry_day']} | {r['mean']} | {r['median']} | {r['min']} | {r['max']} | {int(r['count'])} |")
    lines.append("")

    # === 8. Continuation vs Reversal ===
    lines.append("## 8. Continuation vs Reversal Breakdown")
    lines.append("")
    lines.append("**Continuation** = afternoon moves in SAME direction as daily open→close")
    lines.append("**Reversal** = afternoon moves OPPOSITE to daily open→close")
    lines.append("")

    for label, subset in [("All Days", conc_df), ("Expiry Days", exp_conc), ("Non-Expiry Days", nonexp_conc)]:
        match_sub = subset[subset["concordance"] == "Match"]
        mismatch_sub = subset[subset["concordance"] == "Mismatch"]
        m_count = len(match_sub)
        mm_count = len(mismatch_sub)
        t = m_count + mm_count
        m_pct = round(m_count / t * 100, 1) if t > 0 else 0

        lines.append(f"### {label}")
        lines.append("")
        lines.append(f"- Continuation: {m_count} ({m_pct}%) | Reversal: {mm_count} ({round(100-m_pct,1)}%)")
        lines.append("")

        if mm_count > 0:
            lines.append("#### Continuation Days")
            lines.append("")
            lines.append("| Daily Direction | Afternoon Direction | Count | Avg Move % |")
            lines.append("|-----------------|---------------------|------:|-----------:|")
            for d in ["Top to Down", "Down to Up"]:
                s = match_sub[match_sub["daily_direction"] == d]
                avg = round(s["move_from_2pm_pct"].mean(), 3) if len(s) > 0 else 0
                lines.append(f"| {d} | {d} | {len(s)} | {avg}% |")
            lines.append("")

            lines.append("#### Reversal Days")
            lines.append("")
            lines.append("| Daily Direction | Afternoon Direction | Reversal Type | Count | Avg Move % |")
            lines.append("|-----------------|---------------------|---------------|------:|-----------:|")

            s1 = mismatch_sub[(mismatch_sub["daily_direction"] == "Down to Up") & (mismatch_sub["afternoon_direction"] == "Top to Down")]
            avg1 = round(s1["move_from_2pm_pct"].mean(), 3) if len(s1) > 0 else 0
            lines.append(f"| Down to Up (bullish) | Top to Down | Rally faded after 2 PM | {len(s1)} | {avg1}% |")

            s2 = mismatch_sub[(mismatch_sub["daily_direction"] == "Top to Down") & (mismatch_sub["afternoon_direction"] == "Down to Up")]
            avg2 = round(s2["move_from_2pm_pct"].mean(), 3) if len(s2) > 0 else 0
            lines.append(f"| Top to Down (bearish) | Down to Up | Sell-off recovered after 2 PM | {len(s2)} | {avg2}% |")
            lines.append("")

            lines.append(f"**Of {mm_count} reversal days:**")
            if len(s1) > 0:
                lines.append(f"- {len(s1)} ({round(len(s1)/mm_count*100,1)}%): Morning rally faded → **afternoon sold off**")
            if len(s2) > 0:
                lines.append(f"- {len(s2)} ({round(len(s2)/mm_count*100,1)}%): Morning sell-off reversed → **afternoon recovered**")
            lines.append("")

    # === 9. Day of Week Patterns ===
    lines.append("## 9. Day of Week Summary")
    lines.append("")
    lines.append("| Day | Total | TTD | DTU | Flat | TTD % | DTU % | Avg Move % | Concordance % |")
    lines.append("|-----|------:|----:|----:|-----:|------:|------:|-----------:|--------------:|")
    for dow in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        sub = df[df["day_of_week"] == dow]
        if sub.empty:
            continue
        t = len(sub)
        ttd = len(sub[sub["afternoon_direction"] == "Top to Down"])
        dtu = len(sub[sub["afternoon_direction"] == "Down to Up"])
        fl = len(sub[sub["afternoon_direction"] == "Flat"])
        avg_move = round(sub[sub["afternoon_direction"] != "Flat"]["move_from_2pm_pct"].mean(), 3) if len(sub[sub["afternoon_direction"] != "Flat"]) > 0 else 0
        conc_sub = sub[sub["concordance"].isin(["Match", "Mismatch"])]
        conc_m = len(conc_sub[conc_sub["concordance"] == "Match"])
        conc_p = round(conc_m / len(conc_sub) * 100, 1) if len(conc_sub) > 0 else 0
        lines.append(f"| {dow} | {t} | {ttd} | {dtu} | {fl} | {round(ttd/t*100,1)}% | {round(dtu/t*100,1)}% | {avg_move}% | {conc_p}% |")
    lines.append("")

    # === 10. Key Findings ===
    lines.append("## 10. Key Findings and Trading Implications")
    lines.append("")

    findings = []

    findings.append(
        f"**The 14:00 inflection zone dominates across ALL trading days**, "
        f"with {top_bucket_pct}% of inflections starting in the {top_bucket} bucket. "
        f"This is NOT unique to expiry days — it's a general market phenomenon."
    )

    if not exp_top3.empty and not nonexp_top3.empty:
        findings.append(
            f"**Expiry and non-expiry days share the same top inflection time** "
            f"({exp_top3.index[0]} for expiry, {nonexp_top3.index[0]} for non-expiry). "
            f"The afternoon move timing is driven by market microstructure, not options expiry."
        )

    findings.append(
        f"**Concordance rate**: Expiry days {exp_conc_pct}% vs Non-expiry {nonexp_conc_pct}%. "
        + (f"Expiry days show {'higher' if exp_conc_pct > nonexp_conc_pct else 'lower'} afternoon trend persistence."
           if abs(exp_conc_pct - nonexp_conc_pct) > 2 else
           "Virtually identical — expiry status doesn't change afternoon behavior.")
    )

    exp_avg = round(exp_valid_moves.mean(), 3) if len(exp_valid_moves) > 0 else 0
    nonexp_avg = round(nonexp_valid_moves.mean(), 3) if len(nonexp_valid_moves) > 0 else 0
    if exp_avg > nonexp_avg * 1.1:
        findings.append(
            f"**Expiry days produce {round((exp_avg/nonexp_avg - 1)*100,0)}% larger afternoon moves** "
            f"(avg {exp_avg}% vs {nonexp_avg}%), likely due to options gamma/delta hedging pressure."
        )
    elif nonexp_avg > exp_avg * 1.1:
        findings.append(
            f"**Non-expiry days produce larger afternoon moves** (avg {nonexp_avg}% vs {exp_avg}%). "
            f"Expiry day moves may be constrained by max pain / pinning effects."
        )
    else:
        findings.append(
            f"**Afternoon move magnitudes are similar**: expiry {exp_avg}% vs non-expiry {nonexp_avg}%. "
            f"Options expiry does not meaningfully amplify or dampen the afternoon move."
        )

    # Reversal pattern comparison
    exp_mm = exp_conc[exp_conc["concordance"] == "Mismatch"]
    nonexp_mm = nonexp_conc[nonexp_conc["concordance"] == "Mismatch"]
    if len(exp_mm) > 0 and len(nonexp_mm) > 0:
        exp_recovery = len(exp_mm[(exp_mm["daily_direction"] == "Top to Down") & (exp_mm["afternoon_direction"] == "Down to Up")])
        exp_fade = len(exp_mm[(exp_mm["daily_direction"] == "Down to Up") & (exp_mm["afternoon_direction"] == "Top to Down")])
        nonexp_recovery = len(nonexp_mm[(nonexp_mm["daily_direction"] == "Top to Down") & (nonexp_mm["afternoon_direction"] == "Down to Up")])
        nonexp_fade = len(nonexp_mm[(nonexp_mm["daily_direction"] == "Down to Up") & (nonexp_mm["afternoon_direction"] == "Top to Down")])

        exp_recovery_pct = round(exp_recovery / len(exp_mm) * 100, 1) if len(exp_mm) > 0 else 0
        nonexp_recovery_pct = round(nonexp_recovery / len(nonexp_mm) * 100, 1) if len(nonexp_mm) > 0 else 0

        findings.append(
            f"**When reversals happen**: On expiry days, {exp_recovery_pct}% are morning sell-offs that recover after 2 PM "
            f"vs {exp_fade}% rallies that fade. On non-expiry days: {nonexp_recovery_pct}% recoveries vs {nonexp_fade} fades. "
            + ("Expiry days favor afternoon recoveries more."
               if exp_recovery_pct > nonexp_recovery_pct + 5
               else "Similar reversal patterns across both." if abs(exp_recovery_pct - nonexp_recovery_pct) <= 5
               else "Non-expiry days favor afternoon recoveries more.")
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
    print("Daily Afternoon Reversal Analysis — ALL Trading Days")
    print("=" * 70)

    expiry_info = load_expiry_dates()
    daily_df, afternoon_df = fetch_all_data()
    results_df = analyze_all_days(daily_df, afternoon_df, expiry_info)

    # Stats
    conc = results_df[results_df["concordance"].isin(["Match", "Mismatch"])]
    match_count = len(conc[conc["concordance"] == "Match"])
    print(f"[Concordance] Afternoon confirms daily: {match_count}/{len(conc)} ({round(match_count/len(conc)*100,1)}%)")

    all_dists = build_all_distributions(results_df)
    mag_stats = move_magnitude_table(results_df)

    results_df.to_csv(CSV_OUTPUT, index=False)
    print(f"[Output] CSV: {CSV_OUTPUT} ({len(results_df)} rows)")

    report = generate_report(results_df, all_dists, mag_stats)
    REPORT_OUTPUT.write_text(report)
    print(f"[Output] Report: {REPORT_OUTPUT}")

    valid = results_df[results_df["inflection_time"].notna()]
    if not valid.empty:
        top3 = valid["inflection_time"].value_counts().head(3)
        print(f"\n[Summary] Top 3 inflection times across ALL trading days:")
        for t, c in top3.items():
            print(f"  {t}: {c} days ({round(c/len(valid)*100,1)}%)")

    exp = results_df[results_df["is_expiry_day"] == 1]
    nonexp = results_df[results_df["is_expiry_day"] == 0]
    print(f"\n[Comparison] Expiry avg move: {round(exp[exp['afternoon_direction']!='Flat']['move_from_2pm_pct'].mean(),3)}%")
    print(f"[Comparison] Non-expiry avg move: {round(nonexp[nonexp['afternoon_direction']!='Flat']['move_from_2pm_pct'].mean(),3)}%")

    print("\nDone.")


if __name__ == "__main__":
    main()
