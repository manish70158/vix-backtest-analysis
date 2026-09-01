"""
Analyze WHEN during the trading day the VIX half-threshold is exceeded.

Uses 5-minute candle data from PostgreSQL (nifty50_5min) combined with
the FII-PRO alignment results to determine the exact time the bullish
high or bearish low first crosses half the VIX-predicted range.

Output:
  - vix_threshold_timing_results.csv  (per-day timing data)
  - VIX_THRESHOLD_TIMING_REPORT.md    (summary with distributions)
"""

import pandas as pd
import psycopg2
import warnings
from collections import defaultdict

warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy.*")

DB_HOST = "localhost"
DB_NAME = "market_data"
TABLE = "nifty50_5min"


def fetch_intraday_candles(dates: list[str]) -> pd.DataFrame:
    """Fetch 5-min candles for given dates from PostgreSQL."""
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME)
    placeholders = ",".join([f"'{d}'" for d in dates])
    # Cast to IST explicitly to avoid UTC conversion by pandas
    query = f"""
        SELECT datetime AT TIME ZONE 'Asia/Kolkata' AS datetime,
               open, high, low, close, volume
        FROM {TABLE}
        WHERE datetime::date IN ({placeholders})
        ORDER BY datetime
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["date"] = df["datetime"].dt.date.astype(str)
    df["time"] = df["datetime"].dt.strftime("%H:%M")
    return df


def find_threshold_time(candles_day: pd.DataFrame, day_open: float,
                        half_threshold: float, direction: str) -> dict:
    """
    Find the first 5-min candle where the cumulative high (bullish) or
    cumulative low (bearish) from open exceeds the half-threshold.

    Returns dict with timing info or None if never exceeded.
    """
    running_high = day_open
    running_low = day_open

    for _, candle in candles_day.iterrows():
        running_high = max(running_high, float(candle["high"]))
        running_low = min(running_low, float(candle["low"]))

        if direction == "bullish":
            move_pct = (running_high - day_open) / day_open * 100
            if move_pct > half_threshold:
                return {
                    "exceeded": True,
                    "time": candle["time"],
                    "datetime": candle["datetime"],
                    "move_pct_at_cross": round(move_pct, 3),
                    "candle_high": float(candle["high"]),
                    "running_high": running_high,
                }
        else:  # bearish
            move_pct = abs((running_low - day_open) / day_open * 100)
            if move_pct > half_threshold:
                return {
                    "exceeded": True,
                    "time": candle["time"],
                    "datetime": candle["datetime"],
                    "move_pct_at_cross": round(move_pct, 3),
                    "candle_low": float(candle["low"]),
                    "running_low": running_low,
                }

    return {"exceeded": False}


def time_to_session_label(time_str: str) -> str:
    """Classify time into session buckets."""
    h, m = map(int, time_str.split(":"))
    minutes = h * 60 + m
    if minutes < 9 * 60 + 45:    # 9:15 - 9:44
        return "Opening (9:15-9:44)"
    elif minutes < 10 * 60 + 30:  # 9:45 - 10:29
        return "Early Morning (9:45-10:29)"
    elif minutes < 11 * 60 + 30:  # 10:30 - 11:29
        return "Late Morning (10:30-11:29)"
    elif minutes < 12 * 60 + 30:  # 11:30 - 12:29
        return "Midday (11:30-12:29)"
    elif minutes < 13 * 60 + 30:  # 12:30 - 13:29
        return "Early Afternoon (12:30-13:29)"
    elif minutes < 14 * 60 + 30:  # 13:30 - 14:29
        return "Late Afternoon (13:30-14:29)"
    else:                          # 14:30 - 15:30
        return "Closing (14:30-15:30)"


def minutes_from_open(time_str: str) -> int:
    """Minutes elapsed since 9:15 AM."""
    h, m = map(int, time_str.split(":"))
    return (h * 60 + m) - (9 * 60 + 15)


def main():
    # Load alignment results
    alignment_df = pd.read_csv(
        "fii_pro_alignment_results.csv",
        dtype={"date": str}
    )

    # Filter to alignment days with VIX exhaustion data
    exceeded = alignment_df[
        alignment_df["vix_exhaustion"] == "Exceeded Half then Reversed"
    ].copy()

    bullish_exceeded = exceeded[exceeded["alignment"] == "Bullish Alignment"]
    bearish_exceeded = exceeded[exceeded["alignment"] == "Bearish Alignment"]

    # Also get "Reversed Before Half" to see if they ever got close
    reversed_before = alignment_df[
        alignment_df["vix_exhaustion"] == "Reversed Before Half"
    ].copy()
    bullish_reversed = reversed_before[reversed_before["alignment"] == "Bullish Alignment"]
    bearish_reversed = reversed_before[reversed_before["alignment"] == "Bearish Alignment"]

    all_dates = alignment_df[alignment_df["vix_exhaustion"].isin([
        "Exceeded Half then Reversed", "Reversed Before Half"
    ])]["date"].tolist()

    print(f"Fetching 5-min candles for {len(all_dates)} alignment days...")
    candles = fetch_intraday_candles(all_dates)
    print(f"  Got {len(candles)} candles")

    # Process each day
    results = []
    for _, row in alignment_df[alignment_df["vix_exhaustion"].notna() &
                                (alignment_df["vix_exhaustion"] != "")].iterrows():
        date = row["date"]
        alignment = row["alignment"]
        vix_exhaustion = row["vix_exhaustion"]
        vix_predicted = row["vix_predicted_move_pct"]
        close_outcome = row["close_outcome"]

        if pd.isna(vix_predicted) or vix_predicted == 0:
            continue

        half_threshold = vix_predicted / 2
        direction = "bullish" if alignment == "Bullish Alignment" else "bearish"

        day_candles = candles[candles["date"] == date].sort_values("datetime")
        if len(day_candles) == 0:
            continue

        day_open = float(day_candles.iloc[0]["open"])

        timing = find_threshold_time(day_candles, day_open, half_threshold, direction)

        result = {
            "date": date,
            "alignment": alignment,
            "vix_exhaustion": vix_exhaustion,
            "close_outcome": close_outcome,
            "vix_predicted_pct": vix_predicted,
            "half_threshold_pct": round(half_threshold, 3),
            "day_open": day_open,
            "exceeded": timing["exceeded"],
            "cross_time": timing.get("time", ""),
            "cross_minutes_from_open": minutes_from_open(timing["time"]) if timing["exceeded"] else None,
            "cross_session": time_to_session_label(timing["time"]) if timing["exceeded"] else "",
            "move_pct_at_cross": timing.get("move_pct_at_cross", None),
            "intraday_high_pct": row["intraday_high_pct"],
            "intraday_low_pct": row["intraday_low_pct"],
            "actual_open_close_pct": row["actual_open_close_pct"],
            "is_nifty_expiry": row["is_nifty_expiry"],
            "vix_open": row["vix_open"],
            "vix_regime": row["vix_regime"],
            "year": row["year"],
        }
        results.append(result)

    results_df = pd.DataFrame(results)
    results_df.to_csv("vix_threshold_timing_results.csv", index=False)
    print(f"\nSaved {len(results_df)} rows to vix_threshold_timing_results.csv")

    # ── Generate Report ──
    lines = []
    lines.append("# VIX Half-Threshold Timing Analysis")
    lines.append("")
    lines.append("> **Question**: By what time during the trading day does the market")
    lines.append("> exceed half the VIX-predicted range in the aligned direction?")
    lines.append(">")
    lines.append("> Uses 5-minute candle data from PostgreSQL to find the exact candle")
    lines.append("> where the threshold was first crossed.")
    lines.append("")

    exceeded_df = results_df[results_df["exceeded"] == True].copy()
    not_exceeded_df = results_df[results_df["exceeded"] == False].copy()

    # ── Overall Summary ──
    lines.append("## Overall Summary")
    lines.append("")
    lines.append(f"| Metric | Count |")
    lines.append(f"|--------|------:|")
    lines.append(f"| Total alignment days analyzed | {len(results_df)} |")
    lines.append(f"| Exceeded half-threshold | {len(exceeded_df)} ({round(len(exceeded_df)/len(results_df)*100,1)}%) |")
    lines.append(f"| Never exceeded | {len(not_exceeded_df)} ({round(len(not_exceeded_df)/len(results_df)*100,1)}%) |")
    lines.append("")

    # ── Timing Distribution: All Exceeded ──
    for label, subset_filter, direction_label in [
        ("All Exceeded Days", exceeded_df, "aligned"),
        ("Bullish Alignment — Exceeded Half",
         exceeded_df[exceeded_df["alignment"] == "Bullish Alignment"], "bullish (high from open)"),
        ("Bearish Alignment — Exceeded Half",
         exceeded_df[exceeded_df["alignment"] == "Bearish Alignment"], "bearish (low from open)"),
    ]:
        subset = subset_filter.copy()
        if len(subset) == 0:
            continue

        lines.append(f"## {label} ({len(subset)} days)")
        lines.append("")
        lines.append(f"When did the {direction_label} move first cross half the VIX-predicted range?")
        lines.append("")

        # Time distribution
        avg_mins = subset["cross_minutes_from_open"].mean()
        median_mins = subset["cross_minutes_from_open"].median()
        p25 = subset["cross_minutes_from_open"].quantile(0.25)
        p75 = subset["cross_minutes_from_open"].quantile(0.75)
        min_mins = subset["cross_minutes_from_open"].min()
        max_mins = subset["cross_minutes_from_open"].max()

        def mins_to_time(m):
            total = int(9 * 60 + 15 + m)
            return f"{total // 60}:{total % 60:02d}"

        lines.append("### Timing Statistics")
        lines.append("")
        lines.append(f"| Statistic | Minutes from Open | Clock Time |")
        lines.append(f"|-----------|------------------:|-----------:|")
        lines.append(f"| Average | {avg_mins:.0f} min | ~{mins_to_time(avg_mins)} |")
        lines.append(f"| Median | {median_mins:.0f} min | ~{mins_to_time(median_mins)} |")
        lines.append(f"| 25th percentile | {p25:.0f} min | ~{mins_to_time(p25)} |")
        lines.append(f"| 75th percentile | {p75:.0f} min | ~{mins_to_time(p75)} |")
        lines.append(f"| Earliest | {min_mins:.0f} min | ~{mins_to_time(min_mins)} |")
        lines.append(f"| Latest | {max_mins:.0f} min | ~{mins_to_time(max_mins)} |")
        lines.append("")

        # Session bucket distribution
        lines.append("### Session Distribution")
        lines.append("")
        session_order = [
            "Opening (9:15-9:44)",
            "Early Morning (9:45-10:29)",
            "Late Morning (10:30-11:29)",
            "Midday (11:30-12:29)",
            "Early Afternoon (12:30-13:29)",
            "Late Afternoon (13:30-14:29)",
            "Closing (14:30-15:30)",
        ]
        session_counts = subset["cross_session"].value_counts()

        lines.append("| Session | Count | % | Cumulative % |")
        lines.append("|---------|------:|--:|-----------:|")
        cumulative = 0
        for session in session_order:
            count = session_counts.get(session, 0)
            pct = round(count / len(subset) * 100, 1)
            cumulative += pct
            bar = "█" * int(pct / 2)
            lines.append(f"| {session} | {count} | {pct}% | {cumulative:.1f}% |")
        lines.append("")

        # WR% by session
        lines.append("### Win Rate by Cross Time")
        lines.append("")
        lines.append("Does earlier crossing predict higher win rate?")
        lines.append("")
        lines.append("| Session | Count | Worked and Remained | WR% |")
        lines.append("|---------|------:|--------------------:|----:|")
        for session in session_order:
            s_df = subset[subset["cross_session"] == session]
            if len(s_df) == 0:
                continue
            wr = len(s_df[s_df["close_outcome"] == "Worked and Remained"])
            wr_pct = round(wr / len(s_df) * 100, 1)
            lines.append(f"| {session} | {len(s_df)} | {wr} | {wr_pct}% |")
        lines.append("")

        # 30-minute bucket distribution
        lines.append("### 30-Minute Bucket Distribution")
        lines.append("")
        lines.append("| Time Window | Count | % | WR% |")
        lines.append("|-------------|------:|--:|----:|")
        buckets = [
            ("09:15-09:44", 0, 30),
            ("09:45-10:14", 30, 60),
            ("10:15-10:44", 60, 90),
            ("10:45-11:14", 90, 120),
            ("11:15-11:44", 120, 150),
            ("11:45-12:14", 150, 180),
            ("12:15-12:44", 180, 210),
            ("12:45-13:14", 210, 240),
            ("13:15-13:44", 240, 270),
            ("13:45-14:14", 270, 300),
            ("14:15-14:44", 300, 330),
            ("14:45-15:14", 330, 360),
            ("15:15-15:30", 360, 375),
        ]
        for label_b, start, end in buckets:
            b_df = subset[(subset["cross_minutes_from_open"] >= start) &
                          (subset["cross_minutes_from_open"] < end)]
            if len(b_df) == 0:
                continue
            pct = round(len(b_df) / len(subset) * 100, 1)
            wr = len(b_df[b_df["close_outcome"] == "Worked and Remained"])
            wr_pct = round(wr / len(b_df) * 100, 1)
            lines.append(f"| {label_b} | {len(b_df)} | {pct}% | {wr_pct}% |")
        lines.append("")

        # Expiry vs Non-Expiry timing
        expiry = subset[subset["is_nifty_expiry"] == 1]
        non_expiry = subset[subset["is_nifty_expiry"] == 0]
        if len(expiry) > 0 and len(non_expiry) > 0:
            lines.append("### Expiry vs Non-Expiry Timing")
            lines.append("")
            lines.append("| Context | Count | Avg Minutes | Avg Time | Median Minutes | Median Time |")
            lines.append("|---------|------:|------------:|---------:|---------------:|------------:|")
            for ctx_label, ctx_df in [("Expiry", expiry), ("Non-Expiry", non_expiry)]:
                avg_m = ctx_df["cross_minutes_from_open"].mean()
                med_m = ctx_df["cross_minutes_from_open"].median()
                lines.append(f"| {ctx_label} | {len(ctx_df)} | {avg_m:.0f} | ~{mins_to_time(avg_m)} | {med_m:.0f} | ~{mins_to_time(med_m)} |")
            lines.append("")

        # VIX regime timing
        lines.append("### VIX Regime Timing")
        lines.append("")
        lines.append("| VIX Regime | Count | Avg Minutes | Avg Time | Median Time |")
        lines.append("|------------|------:|------------:|---------:|------------:|")
        for regime in ["Low (<15)", "Normal (15-20)", "Elevated (20-30)"]:
            r_df = subset[subset["vix_regime"] == regime]
            if len(r_df) == 0:
                continue
            avg_m = r_df["cross_minutes_from_open"].mean()
            med_m = r_df["cross_minutes_from_open"].median()
            lines.append(f"| {regime} | {len(r_df)} | {avg_m:.0f} | ~{mins_to_time(avg_m)} | ~{mins_to_time(med_m)} |")
        lines.append("")

        # Year-over-year timing
        lines.append("### Year-over-Year Timing")
        lines.append("")
        lines.append("| Year | Count | Avg Minutes | Avg Time | Median Time |")
        lines.append("|------|------:|------------:|---------:|------------:|")
        for year in sorted(subset["year"].unique()):
            y_df = subset[subset["year"] == year]
            avg_m = y_df["cross_minutes_from_open"].mean()
            med_m = y_df["cross_minutes_from_open"].median()
            lines.append(f"| {year} | {len(y_df)} | {avg_m:.0f} | ~{mins_to_time(avg_m)} | ~{mins_to_time(med_m)} |")
        lines.append("")

        # Top 10 fastest crosses
        lines.append("### Fastest Threshold Crosses (Top 10)")
        lines.append("")
        lines.append("| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |")
        lines.append("|------|-----------|--------:|---------------:|---------------:|-------:|---------|")
        fastest = subset.nsmallest(10, "cross_minutes_from_open")
        for _, r in fastest.iterrows():
            outcome = "Worked" if r["close_outcome"] == "Worked and Remained" else "Failed"
            lines.append(f"| {r['date']} | {r['cross_time']} | {r['cross_minutes_from_open']:.0f} | "
                         f"{r['move_pct_at_cross']}% | {r['vix_predicted_pct']}% | "
                         f"{r['actual_open_close_pct']}% | {outcome} |")
        lines.append("")

        # Top 10 slowest crosses
        lines.append("### Slowest Threshold Crosses (Top 10)")
        lines.append("")
        lines.append("| Date | Cross Time | Minutes | Move% at Cross | VIX Predicted% | Close% | Outcome |")
        lines.append("|------|-----------|--------:|---------------:|---------------:|-------:|---------|")
        slowest = subset.nlargest(10, "cross_minutes_from_open")
        for _, r in slowest.iterrows():
            outcome = "Worked" if r["close_outcome"] == "Worked and Remained" else "Failed"
            lines.append(f"| {r['date']} | {r['cross_time']} | {r['cross_minutes_from_open']:.0f} | "
                         f"{r['move_pct_at_cross']}% | {r['vix_predicted_pct']}% | "
                         f"{r['actual_open_close_pct']}% | {outcome} |")
        lines.append("")

    # ── Early vs Late Cross: Predictive Power ──
    lines.append("## Early vs Late Cross: Does Timing Predict Close Outcome?")
    lines.append("")
    lines.append("Split at the median cross time for each alignment type.")
    lines.append("")

    for align_label, align_filter in [
        ("Bullish", "Bullish Alignment"),
        ("Bearish", "Bearish Alignment"),
    ]:
        a_df = exceeded_df[exceeded_df["alignment"] == align_filter]
        if len(a_df) == 0:
            continue
        median_m = a_df["cross_minutes_from_open"].median()
        early = a_df[a_df["cross_minutes_from_open"] <= median_m]
        late = a_df[a_df["cross_minutes_from_open"] > median_m]

        lines.append(f"### {align_label} Alignment (Median: {median_m:.0f} min = ~{mins_to_time(median_m)})")
        lines.append("")
        lines.append("| Timing | Count | Worked and Remained | WR% | Avg Close% |")
        lines.append("|--------|------:|--------------------:|----:|-----------:|")
        for t_label, t_df in [("Early (≤ median)", early), ("Late (> median)", late)]:
            wr = len(t_df[t_df["close_outcome"] == "Worked and Remained"])
            wr_pct = round(wr / len(t_df) * 100, 1) if len(t_df) > 0 else 0
            avg_close = round(t_df["actual_open_close_pct"].mean(), 3)
            lines.append(f"| {t_label} | {len(t_df)} | {wr} | {wr_pct}% | {avg_close}% |")
        lines.append("")

    # ── First Hour Check ──
    lines.append("## First Hour Rule: Cross Before 10:15 AM")
    lines.append("")
    lines.append("If the threshold is crossed within the first hour (by 10:15 AM), is the signal stronger?")
    lines.append("")
    for align_label, align_filter in [
        ("Bullish", "Bullish Alignment"),
        ("Bearish", "Bearish Alignment"),
    ]:
        a_df = exceeded_df[exceeded_df["alignment"] == align_filter]
        if len(a_df) == 0:
            continue
        first_hour = a_df[a_df["cross_minutes_from_open"] <= 60]
        after_first = a_df[a_df["cross_minutes_from_open"] > 60]

        lines.append(f"### {align_label} Alignment")
        lines.append("")
        lines.append("| Timing | Count | % | Worked and Remained | WR% | Avg Close% |")
        lines.append("|--------|------:|--:|--------------------:|----:|-----------:|")
        for t_label, t_df in [("Within first hour (≤10:15)", first_hour),
                               ("After first hour (>10:15)", after_first)]:
            pct = round(len(t_df) / len(a_df) * 100, 1)
            wr = len(t_df[t_df["close_outcome"] == "Worked and Remained"])
            wr_pct = round(wr / len(t_df) * 100, 1) if len(t_df) > 0 else 0
            avg_close = round(t_df["actual_open_close_pct"].mean(), 3)
            lines.append(f"| {t_label} | {len(t_df)} | {pct}% | {wr} | {wr_pct}% | {avg_close}% |")
        lines.append("")

    # ── Practical Interpretation ──
    lines.append("## Practical Interpretation")
    lines.append("")

    bull_exceeded = exceeded_df[exceeded_df["alignment"] == "Bullish Alignment"]
    bear_exceeded = exceeded_df[exceeded_df["alignment"] == "Bearish Alignment"]

    if len(bull_exceeded) > 0:
        bull_med = bull_exceeded["cross_minutes_from_open"].median()
        lines.append(f"**Bullish Alignment**: Median threshold cross at **{mins_to_time(bull_med)}** "
                     f"({bull_med:.0f} minutes from open)")
    if len(bear_exceeded) > 0:
        bear_med = bear_exceeded["cross_minutes_from_open"].median()
        lines.append(f"")
        lines.append(f"**Bearish Alignment**: Median threshold cross at **{mins_to_time(bear_med)}** "
                     f"({bear_med:.0f} minutes from open)")

    lines.append("")
    lines.append("```")
    lines.append("Caveat: FII/PRO alignment is only known after T+1 settlement.")
    lines.append("The timing analysis answers: IF you knew the alignment,")
    lines.append("by what time would the VIX threshold typically be crossed?")
    lines.append("This is useful for post-hoc pattern recognition, not real-time trading.")
    lines.append("```")
    lines.append("")

    report = "\n".join(lines)
    with open("VIX_THRESHOLD_TIMING_REPORT.md", "w") as f:
        f.write(report)
    print(f"Saved report to VIX_THRESHOLD_TIMING_REPORT.md")


if __name__ == "__main__":
    main()
