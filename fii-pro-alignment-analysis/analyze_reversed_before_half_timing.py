"""
Analyze WHEN the market reaches its deepest point in the aligned direction
on "Reversed Before Half" days — i.e., when does the bearish low (or bullish
high) peak before reversing, even though it never crosses the VIX half-threshold?

This answers: "By what time should it have reversed before half?"

Uses 5-minute candle data from PostgreSQL (nifty50_5min).
"""

import pandas as pd
import psycopg2
import warnings

warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy.*")

DB_HOST = "localhost"
DB_NAME = "market_data"
TABLE = "nifty50_5min"


def fetch_intraday_candles(dates: list[str]) -> pd.DataFrame:
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME)
    placeholders = ",".join([f"'{d}'" for d in dates])
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


def time_to_session_label(time_str: str) -> str:
    h, m = map(int, time_str.split(":"))
    minutes = h * 60 + m
    if minutes < 9 * 60 + 45:
        return "Opening (9:15-9:44)"
    elif minutes < 10 * 60 + 30:
        return "Early Morning (9:45-10:29)"
    elif minutes < 11 * 60 + 30:
        return "Late Morning (10:30-11:29)"
    elif minutes < 12 * 60 + 30:
        return "Midday (11:30-12:29)"
    elif minutes < 13 * 60 + 30:
        return "Early Afternoon (12:30-13:29)"
    elif minutes < 14 * 60 + 30:
        return "Late Afternoon (13:30-14:29)"
    else:
        return "Closing (14:30-15:30)"


def minutes_from_open(time_str: str) -> int:
    h, m = map(int, time_str.split(":"))
    return (h * 60 + m) - (9 * 60 + 15)


def mins_to_time(m):
    total = int(9 * 60 + 15 + m)
    return f"{total // 60}:{total % 60:02d}"


def find_deepest_point(candles_day: pd.DataFrame, day_open: float,
                       direction: str) -> dict:
    """
    Find the candle where the running high (bullish) or running low (bearish)
    reaches its maximum depth from open — the closest approach to the threshold.

    Also tracks when the market reverses away from that deepest point.
    """
    running_high = day_open
    running_low = day_open

    deepest_move_pct = 0
    deepest_time = None
    deepest_candle_idx = 0

    for idx, (_, candle) in enumerate(candles_day.iterrows()):
        running_high = max(running_high, float(candle["high"]))
        running_low = min(running_low, float(candle["low"]))

        if direction == "bullish":
            move_pct = (running_high - day_open) / day_open * 100
        else:
            move_pct = abs((running_low - day_open) / day_open * 100)

        if move_pct > deepest_move_pct:
            deepest_move_pct = move_pct
            deepest_time = candle["time"]
            deepest_candle_idx = idx

    # Find when the market moves significantly away from deepest point
    # (crosses back past 50% of the deepest move in the opposite direction)
    reversal_time = None
    reversal_minutes = None
    total_candles = len(candles_day)

    if deepest_candle_idx < total_candles - 1:
        remaining = candles_day.iloc[deepest_candle_idx + 1:]
        for _, candle in remaining.iterrows():
            if direction == "bullish":
                # For bullish reversed-before-half, the "reversal" is when
                # price drops back below open (or significantly)
                current = (float(candle["close"]) - day_open) / day_open * 100
                if current < 0:  # crossed below open
                    reversal_time = candle["time"]
                    reversal_minutes = minutes_from_open(candle["time"])
                    break
            else:
                # For bearish reversed-before-half, reversal is when
                # price goes back above open
                current = (float(candle["close"]) - day_open) / day_open * 100
                if current > 0:  # crossed above open
                    reversal_time = candle["time"]
                    reversal_minutes = minutes_from_open(candle["time"])
                    break

    return {
        "deepest_move_pct": round(deepest_move_pct, 3),
        "deepest_time": deepest_time,
        "deepest_minutes": minutes_from_open(deepest_time) if deepest_time else None,
        "deepest_session": time_to_session_label(deepest_time) if deepest_time else "",
        "reversal_time": reversal_time,
        "reversal_minutes": reversal_minutes,
    }


def main():
    alignment_df = pd.read_csv("fii_pro_alignment_results.csv", dtype={"date": str})

    reversed_before = alignment_df[
        alignment_df["vix_exhaustion"] == "Reversed Before Half"
    ].copy()

    all_dates = reversed_before["date"].tolist()
    print(f"Fetching 5-min candles for {len(all_dates)} 'Reversed Before Half' days...")
    candles = fetch_intraday_candles(all_dates)
    print(f"  Got {len(candles)} candles")

    results = []
    for _, row in reversed_before.iterrows():
        date = row["date"]
        alignment = row["alignment"]
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
        info = find_deepest_point(day_candles, day_open, direction)

        results.append({
            "date": date,
            "alignment": alignment,
            "close_outcome": close_outcome,
            "vix_predicted_pct": vix_predicted,
            "half_threshold_pct": round(half_threshold, 3),
            "deepest_move_pct": info["deepest_move_pct"],
            "threshold_reached_pct": round(info["deepest_move_pct"] / half_threshold * 100, 1),
            "deepest_time": info["deepest_time"],
            "deepest_minutes": info["deepest_minutes"],
            "deepest_session": info["deepest_session"],
            "reversal_time": info["reversal_time"],
            "reversal_minutes": info["reversal_minutes"],
            "actual_open_close_pct": row["actual_open_close_pct"],
            "intraday_high_pct": row["intraday_high_pct"],
            "intraday_low_pct": row["intraday_low_pct"],
            "is_nifty_expiry": row["is_nifty_expiry"],
            "vix_open": row["vix_open"],
            "vix_regime": row["vix_regime"],
            "year": row["year"],
        })

    df = pd.DataFrame(results)
    df.to_csv("reversed_before_half_timing_results.csv", index=False)
    print(f"Saved {len(df)} rows to reversed_before_half_timing_results.csv")

    # ── Generate Report ──
    lines = []
    lines.append("# Reversed Before Half: Timing Analysis")
    lines.append("")
    lines.append("> On days when the aligned move NEVER reached half the VIX-predicted range,")
    lines.append("> when did the market reach its deepest point before reversing?")
    lines.append("> And when did the reversal become apparent (price crossing back past open)?")
    lines.append("")

    for align_label, align_filter, direction_desc in [
        ("Bearish Alignment", "Bearish Alignment", "bearish low from open"),
        ("Bullish Alignment", "Bullish Alignment", "bullish high from open"),
    ]:
        subset = df[df["alignment"] == align_filter].copy()
        if len(subset) == 0:
            continue

        lines.append(f"## {align_label} — Reversed Before Half ({len(subset)} days)")
        lines.append("")
        lines.append(f"The {direction_desc} never crossed the VIX half-threshold.")
        lines.append("")

        # ── Deepest point timing ──
        lines.append("### When Did the Aligned Move Reach Its Deepest Point?")
        lines.append("")
        lines.append("This is the candle where the running high (bullish) or running low (bearish)")
        lines.append("hit its maximum — the closest it ever got to the threshold before fading.")
        lines.append("")

        avg_m = subset["deepest_minutes"].mean()
        med_m = subset["deepest_minutes"].median()
        p25 = subset["deepest_minutes"].quantile(0.25)
        p75 = subset["deepest_minutes"].quantile(0.75)
        min_m = subset["deepest_minutes"].min()
        max_m = subset["deepest_minutes"].max()

        lines.append("| Statistic | Clock Time | Minutes from 9:15 |")
        lines.append("|-----------|:----------:|-------------------:|")
        lines.append(f"| Median | **{mins_to_time(med_m)}** | {med_m:.0f} min |")
        lines.append(f"| Average | {mins_to_time(avg_m)} | {avg_m:.0f} min |")
        lines.append(f"| 25th percentile | {mins_to_time(p25)} | {p25:.0f} min |")
        lines.append(f"| 75th percentile | {mins_to_time(p75)} | {p75:.0f} min |")
        lines.append(f"| Earliest | {mins_to_time(min_m)} | {min_m:.0f} min |")
        lines.append(f"| Latest | {mins_to_time(max_m)} | {max_m:.0f} min |")
        lines.append("")

        # How close did they get to the threshold?
        avg_reached = subset["threshold_reached_pct"].mean()
        med_reached = subset["threshold_reached_pct"].median()
        lines.append("### How Close Did They Get to the Threshold?")
        lines.append("")
        lines.append(f"| Statistic | % of Half-Threshold Reached |")
        lines.append(f"|-----------|---------------------------:|")
        lines.append(f"| Average | {avg_reached:.1f}% |")
        lines.append(f"| Median | {med_reached:.1f}% |")
        lines.append(f"| < 25% of threshold | {len(subset[subset['threshold_reached_pct'] < 25])} days ({len(subset[subset['threshold_reached_pct'] < 25])/len(subset)*100:.1f}%) |")
        lines.append(f"| 25-50% of threshold | {len(subset[(subset['threshold_reached_pct'] >= 25) & (subset['threshold_reached_pct'] < 50)])} days ({len(subset[(subset['threshold_reached_pct'] >= 25) & (subset['threshold_reached_pct'] < 50)])/len(subset)*100:.1f}%) |")
        lines.append(f"| 50-75% of threshold | {len(subset[(subset['threshold_reached_pct'] >= 50) & (subset['threshold_reached_pct'] < 75)])} days ({len(subset[(subset['threshold_reached_pct'] >= 50) & (subset['threshold_reached_pct'] < 75)])/len(subset)*100:.1f}%) |")
        lines.append(f"| 75-100% of threshold | {len(subset[(subset['threshold_reached_pct'] >= 75) & (subset['threshold_reached_pct'] < 100)])} days ({len(subset[(subset['threshold_reached_pct'] >= 75) & (subset['threshold_reached_pct'] < 100)])/len(subset)*100:.1f}%) |")
        lines.append("")

        # Session distribution of deepest point
        lines.append("### Deepest Point Session Distribution")
        lines.append("")
        session_order = [
            "Opening (9:15-9:44)", "Early Morning (9:45-10:29)",
            "Late Morning (10:30-11:29)", "Midday (11:30-12:29)",
            "Early Afternoon (12:30-13:29)", "Late Afternoon (13:30-14:29)",
            "Closing (14:30-15:30)",
        ]
        session_counts = subset["deepest_session"].value_counts()

        lines.append("| Session | Count | % | Avg % of Threshold Reached |")
        lines.append("|---------|------:|--:|---------------------------:|")
        for session in session_order:
            s_df = subset[subset["deepest_session"] == session]
            count = len(s_df)
            if count == 0:
                continue
            pct = round(count / len(subset) * 100, 1)
            avg_reach = round(s_df["threshold_reached_pct"].mean(), 1)
            lines.append(f"| {session} | {count} | {pct}% | {avg_reach}% |")
        lines.append("")

        # ── Reversal timing ──
        has_reversal = subset[subset["reversal_time"].notna()].copy()
        no_reversal = subset[subset["reversal_time"].isna()]

        lines.append("### When Did the Reversal Become Apparent?")
        lines.append("")
        lines.append("The reversal point is when the close of a 5-min candle crosses back past the open price")
        lines.append("(bullish: drops below open; bearish: rises above open) after the deepest point.")
        lines.append("")
        lines.append(f"- **{len(has_reversal)}** days ({len(has_reversal)/len(subset)*100:.1f}%): price crossed back past open (clear reversal)")
        lines.append(f"- **{len(no_reversal)}** days ({len(no_reversal)/len(subset)*100:.1f}%): price never crossed back past open (aligned direction held weakly)")
        lines.append("")

        if len(has_reversal) > 0:
            rev_avg = has_reversal["reversal_minutes"].mean()
            rev_med = has_reversal["reversal_minutes"].median()
            rev_p25 = has_reversal["reversal_minutes"].quantile(0.25)
            rev_p75 = has_reversal["reversal_minutes"].quantile(0.75)

            lines.append(f"#### Reversal Timing (price crosses back past open)")
            lines.append("")
            lines.append("| Statistic | Clock Time | Minutes from 9:15 |")
            lines.append("|-----------|:----------:|-------------------:|")
            lines.append(f"| Median | **{mins_to_time(rev_med)}** | {rev_med:.0f} min |")
            lines.append(f"| Average | {mins_to_time(rev_avg)} | {rev_avg:.0f} min |")
            lines.append(f"| 25th percentile | {mins_to_time(rev_p25)} | {rev_p25:.0f} min |")
            lines.append(f"| 75th percentile | {mins_to_time(rev_p75)} | {rev_p75:.0f} min |")
            lines.append("")

            # Time from deepest to reversal
            has_reversal = has_reversal.copy()
            has_reversal["gap"] = has_reversal["reversal_minutes"] - has_reversal["deepest_minutes"]
            avg_gap = has_reversal["gap"].mean()
            med_gap = has_reversal["gap"].median()
            lines.append(f"#### Time from Deepest Point to Reversal")
            lines.append("")
            lines.append(f"| Statistic | Minutes |")
            lines.append(f"|-----------|--------:|")
            lines.append(f"| Average gap | {avg_gap:.0f} min |")
            lines.append(f"| Median gap | {med_gap:.0f} min |")
            lines.append("")

        # ── Close outcome by deepest point timing ──
        lines.append("### Close Outcome by Deepest Point Timing")
        lines.append("")
        lines.append("If the deepest aligned-direction move happens early and is shallow,")
        lines.append("what's the probability the market reverses by close?")
        lines.append("")

        # Split by morning vs afternoon deepest point
        morning = subset[subset["deepest_minutes"] <= 120]  # by 11:15
        afternoon = subset[subset["deepest_minutes"] > 120]

        lines.append("| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |")
        lines.append("|---------------|------:|------------------:|-----:|--------------------:|----:|")
        for label, s in [("Before 11:15 AM", morning), ("After 11:15 AM", afternoon)]:
            if len(s) == 0:
                continue
            rev = len(s[s["close_outcome"] == "Reversed by Close"])
            wr = len(s[s["close_outcome"] == "Worked and Remained"])
            rev_pct = round(rev / len(s) * 100, 1)
            wr_pct = round(wr / len(s) * 100, 1)
            lines.append(f"| {label} | {len(s)} | {rev} | {rev_pct}% | {wr} | {wr_pct}% |")
        lines.append("")

        # Split by first hour vs rest
        first_hour = subset[subset["deepest_minutes"] <= 60]
        after_first = subset[subset["deepest_minutes"] > 60]

        lines.append("| Deepest Point | Count | Reversed by Close | Rev% | Worked and Remained | WR% |")
        lines.append("|---------------|------:|------------------:|-----:|--------------------:|----:|")
        for label, s in [("Within first hour (by 10:15)", first_hour), ("After first hour", after_first)]:
            if len(s) == 0:
                continue
            rev = len(s[s["close_outcome"] == "Reversed by Close"])
            wr = len(s[s["close_outcome"] == "Worked and Remained"])
            rev_pct = round(rev / len(s) * 100, 1)
            wr_pct = round(wr / len(s) * 100, 1)
            lines.append(f"| {label} | {len(s)} | {rev} | {rev_pct}% | {wr} | {wr_pct}% |")
        lines.append("")

        # ── Top examples ──
        lines.append("### Examples: Shallowest Moves (Least Momentum)")
        lines.append("")
        lines.append("Days where the aligned move barely got started:")
        lines.append("")
        lines.append("| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |")
        lines.append("|------|------:|------:|------:|------:|:----------:|------:|")
        shallowest = subset.nsmallest(10, "deepest_move_pct")
        for _, r in shallowest.iterrows():
            lines.append(f"| {r['date']} | {r['vix_predicted_pct']}% | {r['half_threshold_pct']}% | "
                         f"{r['deepest_move_pct']}% | {r['threshold_reached_pct']}% | "
                         f"{r['deepest_time']} | {r['actual_open_close_pct']}% |")
        lines.append("")

        lines.append("### Examples: Closest to Threshold (Near Misses)")
        lines.append("")
        lines.append("Days that almost crossed the threshold but fell just short:")
        lines.append("")
        lines.append("| Date | VIX Predicted% | Half Threshold | Deepest Move% | % Reached | Deepest Time | Close% |")
        lines.append("|------|------:|------:|------:|------:|:----------:|------:|")
        closest = subset.nlargest(10, "threshold_reached_pct")
        for _, r in closest.iterrows():
            lines.append(f"| {r['date']} | {r['vix_predicted_pct']}% | {r['half_threshold_pct']}% | "
                         f"{r['deepest_move_pct']}% | {r['threshold_reached_pct']}% | "
                         f"{r['deepest_time']} | {r['actual_open_close_pct']}% |")
        lines.append("")

        lines.append("---")
        lines.append("")

    report = "\n".join(lines)
    with open("REVERSED_BEFORE_HALF_TIMING_REPORT.md", "w") as f:
        f.write(report)
    print(f"Saved report to REVERSED_BEFORE_HALF_TIMING_REPORT.md")


if __name__ == "__main__":
    main()
