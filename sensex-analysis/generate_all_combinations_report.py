#!/usr/bin/env python3
"""
Generate FII View x PRO View "All Combinations" analysis reports for SENSEX,
mirroring fii-pro-alignment-analysis/FII_PRO_ALL_COMBINATIONS_6YEAR_ANALYSIS.md
but driven by Sensex data.

Produces two reports in sensex-analysis/:
  - SENSEX_FII_PRO_ALL_COMBINATIONS_DAILY.md   (from sensex_fii_t1_daily_results.csv,
        split by expiry vs non-expiry via is_sensex_expiry)
  - SENSEX_FII_PRO_ALL_COMBINATIONS_EXPIRY.md  (from sensex_fii_t1_6year_expiry.csv,
        split by weekly vs monthly expiry via expiry_type)

Green day = sensex closes >= open (actual_open_close_pct >= 0).
"""

from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent

VIEW_ORDER = [
    "Strong Bullish", "Bullish", "Mildly Bullish", "Neutral",
    "Mildly Bearish", "Bearish", "Strong Bearish",
]


def prepare(df):
    """Normalise a dataframe to the columns the report needs."""
    df = df.copy()
    # Drop rows without a computed view or without price (e.g. forward-signal rows)
    df = df[df["fii_view"].notna() & df["pro_view"].notna()]
    df = df[df["actual_open_close_pct"].notna()]
    df = df[df["sensex_open"].notna() & df["sensex_close"].notna()]

    df["chg"] = pd.to_numeric(df["actual_open_close_pct"], errors="coerce")
    df["rng"] = pd.to_numeric(df.get("actual_range_pct"), errors="coerce")
    df["green"] = df["chg"] >= 0
    df["move"] = df["green"].map({True: "Down to Up", False: "Top to Down"})
    # Points moved above open / below open
    o = pd.to_numeric(df["sensex_open"], errors="coerce")
    hi = pd.to_numeric(df["sensex_high"], errors="coerce")
    lo = pd.to_numeric(df["sensex_low"], errors="coerce")
    df["up_pts"] = hi - o
    df["down_pts"] = o - lo
    return df.dropna(subset=["chg"])


def dominant_move(sub):
    g = sub["green"].mean() * 100
    if g >= 55:
        return f"Down to Up ({g:.0f}%)"
    if g <= 45:
        return f"Top to Down ({100 - g:.0f}%)"
    return "Mixed"


def combo_stats(sub):
    return {
        "days": len(sub),
        "green": sub["green"].mean() * 100,
        "chg": sub["chg"].mean(),
        "rng": sub["rng"].mean(),
        "up": sub["up_pts"].mean(),
        "down": sub["down_pts"].mean(),
        "move": dominant_move(sub),
    }


def build_report(df, title, dataset_line, split_col, split_a, split_b,
                 split_a_label, split_b_label):
    lines = []
    P = lines.append

    P(f"# {title}")
    P("")
    P(dataset_line)
    P("")

    # FII View Distribution
    P("## FII View Distribution")
    P("")
    P("| FII View | Days | % of Total |")
    P("|---|---|---|")
    total = len(df)
    for view, cnt in df["fii_view"].value_counts().items():
        P(f"| {view} | {cnt} | {cnt / total * 100:.2f}% |")
    P("")
    P("---")
    P("")

    # Build all combos
    combos = []
    for fii in df["fii_view"].unique():
        for pro in df[df["fii_view"] == fii]["pro_view"].unique():
            sub = df[(df["fii_view"] == fii) & (df["pro_view"] == pro)]
            if sub.empty:
                continue
            s = combo_stats(sub)
            # split green%
            a = sub[sub[split_col] == split_a]
            b = sub[sub[split_col] == split_b]
            s["a_days"], s["b_days"] = len(a), len(b)
            s["a_green"] = a["green"].mean() * 100 if len(a) else None
            s["b_green"] = b["green"].mean() * 100 if len(b) else None
            s["fii"], s["pro"] = fii, pro
            combos.append(s)

    # Master Summary Table (sorted by green% desc)
    P("## Master Summary Table (Sorted by Green% Descending)")
    P("")
    P(f"| FII View | PRO View | Days | Green% | Avg Chg% | Dominant Pattern "
      f"| {split_a_label} G% | {split_b_label} G% |")
    P("|---|---|---|---|---|---|---|---|")
    for c in sorted(combos, key=lambda x: x["green"], reverse=True):
        ag = f"{c['a_green']:.1f}%" if c["a_green"] is not None else "-"
        bg = f"{c['b_green']:.1f}%" if c["b_green"] is not None else "-"
        P(f"| {c['fii']} | {c['pro']} | {c['days']} | {c['green']:.2f}% "
          f"| {c['chg']:+.3f}% | {c['move'].split(' (')[0]} | {ag} | {bg} |")
    P("")
    P("---")
    P("")

    # Per-FII sections
    sec = 0
    for fii in VIEW_ORDER:
        fii_df = df[df["fii_view"] == fii]
        if fii_df.empty:
            continue
        sec += 1
        P(f"## Section {sec}: FII {fii.upper()} ({len(fii_df)} days)")
        P("")
        P("| PRO View | Days | Green% | Avg Chg% | Avg Range% "
          "| Up Pts | Down Pts | Dominant Move |")
        P("|---|---|---|---|---|---|---|---|")
        rows = []
        for pro in fii_df["pro_view"].unique():
            sub = fii_df[fii_df["pro_view"] == pro]
            s = combo_stats(sub)
            s["pro"] = pro
            rows.append(s)
        rows.sort(key=lambda x: x["green"], reverse=True)
        for s in rows:
            P(f"| {s['pro']} | {s['days']} | {s['green']:.2f}% | {s['chg']:+.3f}% "
              f"| {s['rng']:.3f}% | {s['up']:.0f} | {s['down']:.0f} | {s['move']} |")
        P("")
        best = max(rows, key=lambda x: x["green"])
        worst = min(rows, key=lambda x: x["green"])
        P(f"**Pattern**: {fii} FII works best with {best['pro']} PRO "
          f"({best['green']:.0f}% Green, {best['days']} days). "
          f"Worst with {worst['pro']} PRO "
          f"({worst['green']:.0f}% Green, {worst['days']} days).")
        P("")
        P("---")
        P("")

    # Top/bottom lists (>=5 days)
    big = [c for c in combos if c["days"] >= 5]

    def top_table(header, key, reverse, fmt_key, extra_key, extra_hdr):
        P(header)
        P("")
        P(f"| Rank | FII View | PRO View | Days | {fmt_key} | {extra_hdr} |")
        P("|---|---|---|---|---|---|")
        ranked = sorted(big, key=lambda x: x[key], reverse=reverse)[:5]
        for i, c in enumerate(ranked, 1):
            if fmt_key == "Green%":
                main = f"**{c['green']:.2f}%**"
                extra = f"{c['chg']:+.3f}%"
            else:
                main = f"**{c['chg']:+.3f}%**"
                extra = f"{c['green']:.2f}%"
            P(f"| {i} | {c['fii']} | {c['pro']} | {c['days']} | {main} | {extra} |")
        P("")

    top_table("## Top 5 Best Combinations (>=5 days)", "green", True,
              "Green%", "chg", "Avg Chg%")
    top_table("## Top 5 Worst Combinations (>=5 days)", "green", False,
              "Green%", "chg", "Avg Chg%")
    top_table("## Top 5 Highest Avg Change (>=5 days)", "chg", True,
              "Avg Chg%", "green", "Green%")
    top_table("## Top 5 Lowest Avg Change (>=5 days)", "chg", False,
              "Avg Chg%", "green", "Green%")

    # Split divergence (>15%, >=3 days each side)
    P("---")
    P("")
    P(f"## {split_a_label} vs {split_b_label} Divergence "
      f"(>15%, >=3 days each side)")
    P("")
    P(f"| FII View | PRO View | {split_a_label} Days | {split_a_label} G% "
      f"| {split_b_label} Days | {split_b_label} G% | Divergence |")
    P("|---|---|---|---|---|---|---|")
    div = []
    for c in combos:
        if (c["a_green"] is not None and c["b_green"] is not None
                and c["a_days"] >= 3 and c["b_days"] >= 3):
            d = abs(c["a_green"] - c["b_green"])
            if d > 15:
                div.append((c, d))
    for c, d in sorted(div, key=lambda x: x[1], reverse=True):
        P(f"| {c['fii']} | {c['pro']} | {c['a_days']} | {c['a_green']:.1f}% "
          f"| {c['b_days']} | {c['b_green']:.1f}% | **{d:.1f}%** |")
    P("")

    # Conclusion (data-driven, >=5 days)
    P("---")
    P("")
    P("## Conclusion")
    P("")
    longs = sorted([c for c in big if c["green"] >= 65],
                   key=lambda x: x["green"], reverse=True)
    shorts = sorted([c for c in big if c["green"] <= 40],
                    key=lambda x: x["green"])
    if longs:
        P("**Go long (>=65% Green, >=5 days):**")
        P("")
        for c in longs:
            P(f"- {c['fii']} + {c['pro']} — {c['green']:.0f}% Green, "
              f"{c['chg']:+.3f}% avg ({c['days']}d)")
        P("")
    if shorts:
        P("**Avoid longs / consider shorts (<=40% Green, >=5 days):**")
        P("")
        for c in shorts:
            P(f"- {c['fii']} + {c['pro']} — {c['green']:.0f}% Green, "
              f"{c['chg']:+.3f}% avg ({c['days']}d)")
        P("")
    P(f"**Split note:** {split_a_label}/{split_b_label} divergence above "
      "flags setups whose direction flips by segment — size down where they diverge.")
    P("")

    return "\n".join(lines) + "\n"


def main():
    # ---- Daily report ----
    daily = prepare(pd.read_csv(HERE / "sensex_fii_t1_daily_results.csv"))
    daily["is_sensex_expiry"] = pd.to_numeric(
        daily["is_sensex_expiry"], errors="coerce").fillna(0).astype(int)
    d0, d1 = daily["date"].min(), daily["date"].max()
    daily_md = build_report(
        daily,
        "SENSEX: FII VIEW x PRO VIEW — All Combinations Analysis (Daily)",
        f"**Dataset**: {len(daily)} days | {d0} to {d1} | "
        f"{daily.groupby(['fii_view', 'pro_view']).ngroups} unique combinations",
        split_col="is_sensex_expiry", split_a=1, split_b=0,
        split_a_label="Exp", split_b_label="Non-Exp",
    )
    (HERE / "SENSEX_FII_PRO_ALL_COMBINATIONS_DAILY.md").write_text(daily_md)
    print("Wrote SENSEX_FII_PRO_ALL_COMBINATIONS_DAILY.md "
          f"({len(daily)} days)")

    # ---- Expiry report ----
    exp = prepare(pd.read_csv(HERE / "sensex_fii_t1_6year_expiry.csv"))
    exp["expiry_type"] = exp["expiry_type"].fillna("").str.lower()
    e0, e1 = exp["date"].min(), exp["date"].max()
    exp_md = build_report(
        exp,
        "SENSEX: FII VIEW x PRO VIEW — All Combinations Analysis (Expiry Days)",
        f"**Dataset**: {len(exp)} expiry days | {e0} to {e1} | "
        f"{exp.groupby(['fii_view', 'pro_view']).ngroups} unique combinations",
        split_col="expiry_type", split_a="weekly", split_b="monthly",
        split_a_label="Weekly", split_b_label="Monthly",
    )
    (HERE / "SENSEX_FII_PRO_ALL_COMBINATIONS_EXPIRY.md").write_text(exp_md)
    print("Wrote SENSEX_FII_PRO_ALL_COMBINATIONS_EXPIRY.md "
          f"({len(exp)} expiry days)")


if __name__ == "__main__":
    main()
