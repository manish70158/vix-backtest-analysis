#!/usr/bin/env python3
"""
Sensex Daily Afternoon Reversal Analysis (ALL Trading Days)
=============================================================
Analyzes the post-2 PM directional move on EVERY trading day,
using Nifty 5-minute bars as proxy, and tags Sensex expiry days
to compare Sensex-expiry vs non-Sensex-expiry behaviour.

Data sources:
  - market_data.nifty50_5min (PostgreSQL, Nifty 5-min proxy)
  - sensex-analysis/sensex_fii_t1_6year_expiry.csv (to tag Sensex expiry days)

Output:
  - sensex-analysis/sensex_daily_afternoon_reversal_results.csv
  - sensex-analysis/SENSEX_DAILY_AFTERNOON_REVERSAL_REPORT.md
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
SENSEX_CSV = REPO_ROOT / "sensex-analysis" / "sensex_fii_t1_6year_expiry.csv"
NIFTY_CSV = REPO_ROOT / "vix_fii_t1_intraday_expiry_results.csv"
OUTPUT_DIR = REPO_ROOT / "sensex-analysis"
CSV_OUTPUT = OUTPUT_DIR / "sensex_daily_afternoon_reversal_results.csv"
REPORT_OUTPUT = OUTPUT_DIR / "SENSEX_DAILY_AFTERNOON_REVERSAL_REPORT.md"

DB_PARAMS = dict(host="localhost", dbname="market_data")

ALL_SLOTS = [
    f"{h:02d}:{m:02d}"
    for h in range(14, 16)
    for m in range(0, 60, 5)
    if dt_time(h, m) >= dt_time(14, 0) and dt_time(h, m) <= dt_time(15, 25)
]


# ---------------------------------------------------------------------------
# 1. Load expiry dates for tagging
# ---------------------------------------------------------------------------
def load_expiry_dates():
    sensex_df = pd.read_csv(SENSEX_CSV, parse_dates=["date"])
    sensex_expiry = {}
    for _, row in sensex_df.iterrows():
        d = row["date"].strftime("%Y-%m-%d")
        sensex_expiry[d] = {
            "expiry_type": row["expiry_type"],
            "vix_open": float(row["vix_open"]),
            "t1_fii_stance": row["t1_fii_stance"],
            "is_nifty_expiry_day": int(row["is_nifty_expiry_day"]),
        }

    nifty_df = pd.read_csv(NIFTY_CSV, parse_dates=["date"])
    nifty_expiry_dates = set(nifty_df["date"].dt.strftime("%Y-%m-%d"))

    print(f"[CSV] Loaded {len(sensex_expiry)} Sensex expiry dates, {len(nifty_expiry_dates)} Nifty expiry dates")
    return sensex_expiry, nifty_expiry_dates


# ---------------------------------------------------------------------------
# 2. Batch-fetch from PostgreSQL
# ---------------------------------------------------------------------------
def fetch_all_data():
    conn = psycopg2.connect(**DB_PARAMS)

    print("[DB] Fetching daily open/close...")
    daily_df = pd.read_sql("""
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
    """, conn)
    print(f"[DB] Got {len(daily_df)} trading days")

    print("[DB] Fetching afternoon bars...")
    afternoon_df = pd.read_sql("""
        SELECT datetime, open, high, low, close
        FROM nifty50_5min
        WHERE datetime::time >= '14:00'
          AND datetime::time <= '15:25'
        ORDER BY datetime
    """, conn)
    conn.close()

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
def analyze_all_days(daily_df, afternoon_df, sensex_expiry, nifty_expiry_dates):
    import datetime as dt_mod
    rows = []
    grouped = afternoon_df.groupby("date")

    for _, day_row in daily_df.iterrows():
        raw_dt = day_row["dt"]
        date_str = str(raw_dt)
        dt_date = dt_mod.date.fromisoformat(date_str) if isinstance(raw_dt, str) else raw_dt

        day_open = float(day_row["day_open"])
        day_close = float(day_row["day_close"])

        daily_pct = abs(day_close - day_open) / day_open * 100
        if daily_pct < 0.01:
            daily_direction = "Flat"
        elif day_open > day_close:
            daily_direction = "Top to Down"
        else:
            daily_direction = "Down to Up"

        if dt_date not in grouped.groups:
            continue
        bars = grouped.get_group(dt_date).sort_values("datetime")
        if len(bars) < 2:
            continue

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

        if afternoon_direction == "Flat":
            concordance = "Flat"
        elif afternoon_direction == daily_direction:
            concordance = "Match"
        else:
            concordance = "Mismatch"

        move_from_inflection_pct = (
            abs(session_close - inflection_price) / inflection_price * 100
            if inflection_price else 0
        )

        sx = sensex_expiry.get(date_str)
        is_sensex_expiry = 1 if sx else 0
        is_nifty_expiry = 1 if date_str in nifty_expiry_dates else 0
        is_dual_expiry = 1 if is_sensex_expiry and is_nifty_expiry else 0

        if is_sensex_expiry:
            day_type = "Sensex Expiry"
            if is_dual_expiry:
                day_type = "Dual Expiry (Sensex+Nifty)"
        elif is_nifty_expiry:
            day_type = "Nifty-Only Expiry"
        else:
            day_type = "No Expiry"

        expiry_type = sx["expiry_type"] if sx else "non-expiry"
        vix_open = sx["vix_open"] if sx else None
        fii_stance = sx["t1_fii_stance"] if sx else None
        dow = dt_date.strftime("%A")

        rows.append({
            "date": date_str,
            "day_of_week": dow,
            "is_sensex_expiry": is_sensex_expiry,
            "is_nifty_expiry": is_nifty_expiry,
            "is_dual_expiry": is_dual_expiry,
            "day_type": day_type,
            "expiry_type": expiry_type,
            "daily_direction": daily_direction,
            "afternoon_direction": afternoon_direction,
            "concordance": concordance,
            "day_open": round(day_open, 2),
            "day_close": round(day_close, 2),
            "daily_move_pct": round((day_close - day_open) / day_open * 100, 3),
            "price_at_2pm": round(price_at_2pm, 2),
            "session_close": round(session_close, 2),
            "move_from_2pm_pct": round(afternoon_pct, 3),
            "inflection_time": inflection_time,
            "inflection_price": round(inflection_price, 2) if inflection_price else None,
            "move_from_inflection_pct": round(move_from_inflection_pct, 3),
            "vix_open": round(vix_open, 2) if vix_open else None,
            "t1_fii_stance": fii_stance,
        })

    results_df = pd.DataFrame(rows)
    sx_exp = results_df["is_sensex_expiry"].sum()
    nx_exp = results_df["is_nifty_expiry"].sum()
    dual = results_df["is_dual_expiry"].sum()
    no_exp = len(results_df) - sx_exp - (nx_exp - dual)
    print(f"[Analysis] {len(results_df)} trading days: "
          f"Sensex-only expiry {sx_exp - dual}, Nifty-only expiry {nx_exp - dual}, "
          f"Dual expiry {dual}, No expiry {no_exp}")
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

    for dtype in ["Sensex Expiry", "Dual Expiry (Sensex+Nifty)", "Nifty-Only Expiry", "No Expiry"]:
        sub = df[df["day_type"] == dtype]
        if len(sub) >= 10:
            d, _ = timing_distribution(sub, dtype)
            all_dists.append(d)

    for dow in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        sub = df[df["day_of_week"] == dow]
        if len(sub) >= 10:
            d, _ = timing_distribution(sub, f"Day: {dow}")
            all_dists.append(d)

    return all_dists


def move_magnitude_table(df):
    non_flat = df[df["afternoon_direction"] != "Flat"]
    stats = (
        non_flat.groupby(["afternoon_direction", "day_type"])["move_from_2pm_pct"]
        .agg(["mean", "median", "min", "max", "count"])
        .round(3)
        .reset_index()
    )
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


def top_times(v, n=3):
    if v.empty:
        return pd.Series(dtype=int)
    return v["inflection_time"].value_counts().head(n)


def to_15min_bucket(t):
    if not t:
        return None
    h, m = int(t[:2]), int(t[3:])
    return f"{h:02d}:{(m // 15) * 15:02d}"


def conc_stats(subset):
    c = subset[subset["concordance"].isin(["Match", "Mismatch"])]
    m = len(c[c["concordance"] == "Match"])
    t = len(c)
    return m, t, round(m / t * 100, 1) if t > 0 else 0


def reversal_breakdown_md(subset, label):
    """Generate continuation/reversal breakdown for a subset."""
    conc_sub = subset[subset["concordance"].isin(["Match", "Mismatch"])]
    match_sub = conc_sub[conc_sub["concordance"] == "Match"]
    mismatch_sub = conc_sub[conc_sub["concordance"] == "Mismatch"]
    m_count, mm_count = len(match_sub), len(mismatch_sub)
    t = m_count + mm_count
    if t == 0:
        return ""
    m_pct = round(m_count / t * 100, 1)

    lines = []
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

    return "\n".join(lines)


def generate_report(df, all_dists, mag_stats):
    total = len(df)
    valid = df[df["inflection_time"].notna()]

    sensex_exp = df[df["is_sensex_expiry"] == 1]
    nifty_only_exp = df[(df["is_nifty_expiry"] == 1) & (df["is_sensex_expiry"] == 0)]
    dual_exp = df[df["is_dual_expiry"] == 1]
    no_exp = df[(df["is_sensex_expiry"] == 0) & (df["is_nifty_expiry"] == 0)]
    any_exp = df[(df["is_sensex_expiry"] == 1) | (df["is_nifty_expiry"] == 1)]
    non_any_exp = df[(df["is_sensex_expiry"] == 0) & (df["is_nifty_expiry"] == 0)]

    flat_all = len(df[df["afternoon_direction"] == "Flat"])
    ttd_all = len(df[df["afternoon_direction"] == "Top to Down"])
    dtu_all = len(df[df["afternoon_direction"] == "Down to Up"])

    all_top3 = top_times(valid)

    valid_copy = valid.copy()
    valid_copy["bucket_15m"] = valid_copy["inflection_time"].apply(to_15min_bucket)
    bucket_counts = valid_copy["bucket_15m"].value_counts()
    top_bucket = bucket_counts.index[0] if not bucket_counts.empty else "N/A"
    top_bucket_count = bucket_counts.iloc[0] if not bucket_counts.empty else 0
    top_bucket_pct = round(top_bucket_count / len(valid) * 100, 1) if len(valid) > 0 else 0

    lines = []
    lines.append("# Sensex Daily Afternoon Reversal Analysis — ALL Trading Days")
    lines.append("")
    lines.append(f"**Analyzed {total} trading days** (Nifty 5-min proxy for intraday timing)")
    lines.append(f"**Date range**: {df['date'].min()} to {df['date'].max()}")
    lines.append("")
    lines.append("> Uses Nifty 5-min data as timing proxy. Sensex expiry dates tagged from CSV.")
    lines.append("")

    # Day type counts
    dt_counts = df["day_type"].value_counts()
    lines.append("**Day type breakdown:**")
    for dtype, cnt in dt_counts.items():
        lines.append(f"- {dtype}: {cnt}")
    lines.append("")

    # === 1. Executive Summary ===
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(f"Across **all {total} trading days**:")
    lines.append(f"- Top to Down afternoons: {ttd_all} ({round(ttd_all/total*100,1)}%)")
    lines.append(f"- Down to Up afternoons: {dtu_all} ({round(dtu_all/total*100,1)}%)")
    lines.append(f"- Flat afternoons: {flat_all} ({round(flat_all/total*100,1)}%)")
    lines.append("")
    lines.append(f"**Primary reversal zone:** `{top_bucket}` — {top_bucket_count} of {len(valid)} days ({top_bucket_pct}%)")
    lines.append("")
    if not all_top3.empty:
        lines.append("**Top 3 inflection times:**")
        lines.append("")
        lines.append("| Time | Count | % |")
        lines.append("|------|------:|----:|")
        for t, c in all_top3.items():
            lines.append(f"| {t} | {c} | {round(c/len(valid)*100,1)}% |")
        lines.append("")

    # === 2. Four-Way Comparison ===
    lines.append("## 2. Four-Way Day Type Comparison")
    lines.append("")

    day_types = [
        ("Sensex Expiry (all)", sensex_exp),
        ("  - Sensex-Only", df[(df["is_sensex_expiry"] == 1) & (df["is_dual_expiry"] == 0)]),
        ("  - Dual (Sensex+Nifty)", dual_exp),
        ("Nifty-Only Expiry", nifty_only_exp),
        ("No Expiry", no_exp),
        ("All Days", df),
    ]

    lines.append("| Metric | " + " | ".join(l for l, _ in day_types) + " |")
    lines.append("|--------| " + " | ".join("---:" for _ in day_types) + " |")

    # Total
    lines.append("| Total | " + " | ".join(str(len(s)) for _, s in day_types) + " |")

    # TTD %
    vals = []
    for _, s in day_types:
        t = len(s)
        ttd = len(s[s["afternoon_direction"] == "Top to Down"])
        vals.append(f"{round(ttd/t*100,1)}%" if t > 0 else "—")
    lines.append("| TTD % | " + " | ".join(vals) + " |")

    # DTU %
    vals = []
    for _, s in day_types:
        t = len(s)
        dtu = len(s[s["afternoon_direction"] == "Down to Up"])
        vals.append(f"{round(dtu/t*100,1)}%" if t > 0 else "—")
    lines.append("| DTU % | " + " | ".join(vals) + " |")

    # Concordance
    vals = []
    for _, s in day_types:
        _, _, pct = conc_stats(s)
        vals.append(f"{pct}%")
    lines.append("| Concordance | " + " | ".join(vals) + " |")

    # Avg move
    vals = []
    for _, s in day_types:
        nf = s[s["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
        vals.append(f"{round(nf.mean(),3)}%" if len(nf) > 0 else "—")
    lines.append("| Avg move % | " + " | ".join(vals) + " |")

    # Median move
    vals = []
    for _, s in day_types:
        nf = s[s["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
        vals.append(f"{round(nf.median(),3)}%" if len(nf) > 0 else "—")
    lines.append("| Median move % | " + " | ".join(vals) + " |")

    lines.append("")

    # Top inflection times per type
    lines.append("### Top 3 Inflection Times by Day Type")
    lines.append("")
    for label, subset in day_types[:5]:  # skip "All Days"
        v = subset[subset["inflection_time"].notna()]
        t3 = top_times(v)
        if not t3.empty:
            t3_str = ", ".join(f"{t} ({c})" for t, c in t3.items())
            lines.append(f"- **{label.strip()}**: {t3_str}")
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

    # === 5. By Day Type ===
    lines.append("## 5. Timing Distribution by Day Type")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label in ["Sensex Expiry", "Dual Expiry (Sensex+Nifty)", "Nifty-Only Expiry", "No Expiry"]:
            lines.append(dist_table_md(d, label))

    # === 6. By Day of Week ===
    lines.append("## 6. Timing Distribution by Day of Week")
    lines.append("")
    for d in all_dists:
        label = d["group"].iloc[0]
        if label.startswith("Day:"):
            lines.append(dist_table_md(d, label))

    # === 7. Move Magnitude ===
    lines.append("## 7. Move Magnitude from 2 PM to Close by Day Type")
    lines.append("")
    if not mag_stats.empty:
        lines.append("| Direction | Day Type | Avg % | Median % | Min % | Max % | Count |")
        lines.append("|-----------|----------|------:|---------:|------:|------:|------:|")
        for _, r in mag_stats.iterrows():
            lines.append(f"| {r['afternoon_direction']} | {r['day_type']} | {r['mean']} | {r['median']} | {r['min']} | {r['max']} | {int(r['count'])} |")
        lines.append("")

    # === 8. Continuation vs Reversal ===
    lines.append("## 8. Continuation vs Reversal Breakdown")
    lines.append("")
    lines.append("**Continuation** = afternoon moves in SAME direction as daily open→close")
    lines.append("**Reversal** = afternoon moves OPPOSITE to daily open→close")
    lines.append("")

    lines.append(reversal_breakdown_md(df, "All Days"))
    lines.append(reversal_breakdown_md(sensex_exp, "Sensex Expiry Days"))
    lines.append(reversal_breakdown_md(nifty_only_exp, "Nifty-Only Expiry Days"))
    lines.append(reversal_breakdown_md(no_exp, "No Expiry Days"))

    # === 9. Day of Week ===
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
        nf = sub[sub["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
        avg_m = round(nf.mean(), 3) if len(nf) > 0 else 0
        _, _, cp = conc_stats(sub)
        lines.append(f"| {dow} | {t} | {ttd} | {dtu} | {fl} | {round(ttd/t*100,1)}% | {round(dtu/t*100,1)}% | {avg_m}% | {cp}% |")
    lines.append("")

    # === 10. Key Findings ===
    lines.append("## 10. Key Findings and Trading Implications")
    lines.append("")

    findings = []

    findings.append(
        f"**The {top_bucket} inflection zone dominates across ALL trading days** ({top_bucket_pct}%). "
        f"This is a general market microstructure pattern, not Sensex-expiry-specific."
    )

    # Compare Sensex expiry vs no expiry
    _, _, sx_conc = conc_stats(sensex_exp)
    _, _, no_conc = conc_stats(no_exp)
    sx_avg = round(sensex_exp[sensex_exp["afternoon_direction"] != "Flat"]["move_from_2pm_pct"].mean(), 3)
    no_avg = round(no_exp[no_exp["afternoon_direction"] != "Flat"]["move_from_2pm_pct"].mean(), 3)

    findings.append(
        f"**Concordance**: Sensex expiry {sx_conc}% vs No-expiry {no_conc}%. "
        + (f"{'Sensex expiry' if sx_conc > no_conc else 'Non-expiry'} days show slightly higher trend persistence."
           if abs(sx_conc - no_conc) > 2 else
           "Virtually identical — Sensex expiry doesn't change afternoon behaviour.")
    )

    if sx_avg > no_avg * 1.1:
        findings.append(
            f"**Sensex expiry days produce {round((sx_avg/no_avg-1)*100,0)}% larger afternoon moves** "
            f"({sx_avg}% vs {no_avg}%)."
        )
    elif no_avg > sx_avg * 1.1:
        findings.append(
            f"**Non-expiry days produce larger afternoon moves** ({no_avg}% vs {sx_avg}%)."
        )
    else:
        findings.append(
            f"**Move magnitudes are similar**: Sensex expiry {sx_avg}% vs No-expiry {no_avg}%."
        )

    # Dual vs single expiry
    if len(dual_exp) >= 10:
        dual_avg = round(dual_exp[dual_exp["afternoon_direction"] != "Flat"]["move_from_2pm_pct"].mean(), 3)
        sx_only = df[(df["is_sensex_expiry"] == 1) & (df["is_dual_expiry"] == 0)]
        sx_only_avg = round(sx_only[sx_only["afternoon_direction"] != "Flat"]["move_from_2pm_pct"].mean(), 3)
        if dual_avg > sx_only_avg * 1.1:
            findings.append(
                f"**Dual expiry days (Sensex+Nifty) produce larger moves** ({dual_avg}%) "
                f"vs Sensex-only expiry ({sx_only_avg}%). Double expiry amplifies volatility."
            )
        else:
            findings.append(
                f"**Dual expiry ({dual_avg}%) vs Sensex-only ({sx_only_avg}%)**: "
                f"No meaningful difference in afternoon move size."
            )

    # Reversal pattern
    sx_mm = sensex_exp[sensex_exp["concordance"] == "Mismatch"]
    no_mm = no_exp[no_exp["concordance"] == "Mismatch"]
    if len(sx_mm) > 0 and len(no_mm) > 0:
        sx_rec = len(sx_mm[(sx_mm["daily_direction"] == "Top to Down") & (sx_mm["afternoon_direction"] == "Down to Up")])
        no_rec = len(no_mm[(no_mm["daily_direction"] == "Top to Down") & (no_mm["afternoon_direction"] == "Down to Up")])
        sx_rec_pct = round(sx_rec / len(sx_mm) * 100, 1)
        no_rec_pct = round(no_rec / len(no_mm) * 100, 1)
        findings.append(
            f"**Reversal pattern**: On Sensex expiry days, {sx_rec_pct}% of reversals are morning sell-offs "
            f"recovering after 2 PM. On no-expiry days: {no_rec_pct}%. "
            + ("Sensex expiry favours afternoon recovery." if sx_rec_pct > no_rec_pct + 5 else
               "Similar reversal mix." if abs(sx_rec_pct - no_rec_pct) <= 5 else
               "Non-expiry days favour afternoon recovery more.")
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
    print("Sensex Daily Afternoon Reversal Analysis — ALL Trading Days")
    print("(Nifty 5-min proxy, Sensex expiry tagging)")
    print("=" * 70)

    sensex_expiry, nifty_expiry_dates = load_expiry_dates()
    daily_df, afternoon_df = fetch_all_data()
    results_df = analyze_all_days(daily_df, afternoon_df, sensex_expiry, nifty_expiry_dates)

    m, t, pct = conc_stats(results_df)
    print(f"[Concordance] Afternoon confirms daily: {m}/{t} ({pct}%)")

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
        print(f"\n[Summary] Top 3 inflection times:")
        for t_val, c in top3.items():
            print(f"  {t_val}: {c} days ({round(c/len(valid)*100,1)}%)")

    # Comparison
    for dtype in ["Sensex Expiry", "Dual Expiry (Sensex+Nifty)", "Nifty-Only Expiry", "No Expiry"]:
        sub = results_df[results_df["day_type"] == dtype]
        nf = sub[sub["afternoon_direction"] != "Flat"]["move_from_2pm_pct"]
        if len(nf) > 0:
            print(f"[{dtype}] Avg move: {round(nf.mean(),3)}%, count: {len(sub)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
