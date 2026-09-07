#!/usr/bin/env python3
"""
Generate FII-PRO Alignment Report from sensex_fii_t1_daily_results.csv (ALL trading days).

Produces: SENSEX_FII_PRO_ALIGNMENT_DAILY_REPORT.md
"""

import math
import pandas as pd
from pathlib import Path
from io import StringIO

SENSEX_DIR = Path(__file__).resolve().parent
CSV_PATH = SENSEX_DIR / "sensex_fii_t1_daily_results.csv"
OUTPUT_PATH = SENSEX_DIR / "SENSEX_FII_PRO_ALIGNMENT_DAILY_REPORT.md"


# ---------------------------------------------------------------------------
# Classification helpers
# ---------------------------------------------------------------------------
BULLISH_VIEWS = {"Strong Bullish", "Bullish", "Mildly Bullish"}
BEARISH_VIEWS = {"Strong Bearish", "Bearish", "Mildly Bearish"}
STRONG_BULLISH = {"Strong Bullish", "Bullish"}
STRONG_BEARISH = {"Strong Bearish", "Bearish"}


def direction_of(view):
    if view in BULLISH_VIEWS:
        return "bullish"
    if view in BEARISH_VIEWS:
        return "bearish"
    return "neutral"


def alignment_type(fii_dir, pro_dir):
    if fii_dir == "bullish" and pro_dir == "bullish":
        return "Bullish Alignment"
    if fii_dir == "bearish" and pro_dir == "bearish":
        return "Bearish Alignment"
    if {fii_dir, pro_dir} == {"bullish", "bearish"}:
        return "Mixed"
    return "Neutral"


def intraday_pattern(align, move_dir):
    """Worked then Reversed vs Against then Recovered."""
    if align == "Bullish Alignment":
        return "Worked then Reversed" if move_dir == "Top to Down" else "Against then Recovered"
    if align == "Bearish Alignment":
        return "Worked then Reversed" if move_dir == "Down to Up" else "Against then Recovered"
    return None


def close_outcome(align, oc_pct):
    """Did the aligned view win by close?"""
    if align == "Bullish Alignment":
        return "Worked and Remained" if oc_pct > 0 else "Reversed by Close"
    if align == "Bearish Alignment":
        return "Worked and Remained" if oc_pct < 0 else "Reversed by Close"
    return None


def vix_regime(vix_open):
    if pd.isna(vix_open):
        return None
    if vix_open < 15:
        return "Low (<15)"
    if vix_open < 20:
        return "Normal (15-20)"
    if vix_open <= 30:
        return "Elevated (20-30)"
    return "High (>30)"


def pct(num, den):
    return round(num / den * 100, 1) if den > 0 else 0.0


def fmt(val):
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return "-"
    return f"{val:.2f}%"


def neutral_subtype(fii_dir, pro_dir, fii_view, pro_view):
    if fii_dir == "neutral" and pro_dir == "neutral":
        return "Both Neutral"
    if fii_dir == "neutral" and pro_dir == "bullish":
        return "FII Neutral + PRO Bullish"
    if fii_dir == "neutral" and pro_dir == "bearish":
        return "FII Neutral + PRO Bearish"
    if fii_dir == "bullish" and pro_dir == "neutral":
        return "FII Bullish + PRO Neutral"
    if fii_dir == "bearish" and pro_dir == "neutral":
        return "FII Bearish + PRO Neutral"
    return "Other"


def mixed_subtype(fii_dir, pro_dir):
    if fii_dir == "bullish" and pro_dir == "bearish":
        return "FII Bullish + PRO Bearish"
    if fii_dir == "bearish" and pro_dir == "bullish":
        return "FII Bearish + PRO Bullish"
    return "Other"


# ---------------------------------------------------------------------------
# Main analysis
# ---------------------------------------------------------------------------
def main():
    df = pd.read_csv(CSV_PATH)
    total_rows = len(df)

    # Filter to rows with both FII and PRO view
    df = df[df["fii_view"].notna() & df["pro_view"].notna()].copy()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    # Classify
    df["fii_dir"] = df["fii_view"].apply(direction_of)
    df["pro_dir"] = df["pro_view"].apply(direction_of)
    df["align"] = df.apply(lambda r: alignment_type(r["fii_dir"], r["pro_dir"]), axis=1)
    df["pattern"] = df.apply(lambda r: intraday_pattern(r["align"], r["move_direction"]), axis=1)
    df["close_out"] = df.apply(lambda r: close_outcome(r["align"], r["actual_open_close_pct"]), axis=1)

    # VIX predicted move (annualized VIX / sqrt(252) = daily expected move %)
    df["vix_predicted_pct"] = df["vix_open"].apply(
        lambda x: round(x / math.sqrt(252), 2) if pd.notna(x) else None
    )

    # VIX exhaustion
    def calc_vix_exhaustion(r):
        if pd.isna(r.get("vix_predicted_pct")) or r["align"] not in ("Bullish Alignment", "Bearish Alignment"):
            return None
        half = r["vix_predicted_pct"] / 2
        if r["align"] == "Bullish Alignment":
            aligned_move = r["intraday_high_pct"]
        else:
            aligned_move = abs(r["intraday_low_pct"])
        return "Exceeded Half then Reversed" if aligned_move > half else "Reversed Before Half"

    df["vix_exhaust"] = df.apply(calc_vix_exhaustion, axis=1)
    df["vix_regime"] = df["vix_open"].apply(vix_regime)

    # Is expiry day
    df["is_expiry"] = ((df["is_nifty_expiry"] == 1) | (df["is_sensex_expiry"] == 1)).astype(int)

    # Subsets
    aligned = df[df["align"].isin(["Bullish Alignment", "Bearish Alignment"])]
    bull_aligned = df[df["align"] == "Bullish Alignment"]
    bear_aligned = df[df["align"] == "Bearish Alignment"]
    mixed = df[df["align"] == "Mixed"]
    neutral = df[df["align"] == "Neutral"]

    n_total = len(df)
    n_aligned = len(aligned)
    n_bull = len(bull_aligned)
    n_bear = len(bear_aligned)
    n_mixed = len(mixed)
    n_neutral = len(neutral)

    first_date = df["date"].min().strftime("%Y-%m-%d")
    last_date = df["date"].max().strftime("%Y-%m-%d")

    # Build report
    out = StringIO()
    w = out.write

    # =====================================================================
    # HEADER
    # =====================================================================
    w("# FII-PRO Alignment Analysis — All Trading Days (Sensex Daily CSV)\n\n")
    w("> **Retrospective study**: FII/PRO views are derived from T+1 settlement data,\n")
    w("> so alignment is known only after the trading day. This analysis identifies\n")
    w("> historical patterns, not real-time predictive signals.\n")
    w(">\n")
    w("> **Intraday direction proxy**: `move_direction` captures the dominant intraday\n")
    w("> pattern (open→high→low→close sequence) but does not precisely split the session\n")
    w("> at a fixed time boundary.\n\n")

    # =====================================================================
    # OVERALL SUMMARY
    # =====================================================================
    w("## Overall Summary\n\n")
    w("| Metric | Count | % of Total |\n")
    w("|--------|------:|----------:|\n")
    w(f"| Total Trading Days | {n_total} | 100.0% |\n")
    w(f"| **Aligned Days (Bullish + Bearish)** | **{n_aligned}** | **{pct(n_aligned, n_total)}%** |\n")
    w(f"| Bullish Alignment | {n_bull} | {pct(n_bull, n_total)}% |\n")
    w(f"| Bearish Alignment | {n_bear} | {pct(n_bear, n_total)}% |\n")
    w(f"| Mixed (opposing views) | {n_mixed} | {pct(n_mixed, n_total)}% |\n")
    w(f"| Neutral/Unclear | {n_neutral} | {pct(n_neutral, n_total)}% |\n\n")

    # =====================================================================
    # ALIGNMENT OUTCOME BREAKDOWN
    # =====================================================================
    w("## Alignment Outcome Breakdown\n\n")
    w("When FII and PRO align, does the first half move in their direction and then reverse?\n\n")

    def outcome_table(subset, label):
        w(f"### {label}\n\n")
        worked = subset[subset["pattern"] == "Worked then Reversed"]
        against = subset[subset["pattern"] == "Against then Recovered"]
        n = len(subset)
        w("| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |\n")
        w("|---------|------:|--:|----------:|---------:|----------------:|\n")
        if len(worked) > 0:
            w(f"| Worked then Reversed | {len(worked)} | {pct(len(worked), n)}% "
              f"| {fmt(worked['intraday_high_pct'].mean())} "
              f"| {fmt(worked['intraday_low_pct'].mean())} "
              f"| {fmt(worked['actual_open_close_pct'].mean())} |\n")
        if len(against) > 0:
            w(f"| Against then Recovered | {len(against)} | {pct(len(against), n)}% "
              f"| {fmt(against['intraday_high_pct'].mean())} "
              f"| {fmt(against['intraday_low_pct'].mean())} "
              f"| {fmt(against['actual_open_close_pct'].mean())} |\n")
        w("\n")

    outcome_table(aligned, f"All Aligned Days ({n_aligned} days)")
    outcome_table(bull_aligned, f"Bullish Alignment ({n_bull} days)")
    outcome_table(bear_aligned, f"Bearish Alignment ({n_bear} days)")

    # =====================================================================
    # WORKED AND REMAINED
    # =====================================================================
    w("## Worked and Remained: Did the Aligned View Win by Close?\n\n")
    w("A different lens: regardless of intraday path, did the market **close** in the aligned direction?\n\n")
    w("- **Worked and Remained**: Close was in the aligned direction (bullish alignment + close > open, or bearish alignment + close < open)\n")
    w("- **Reversed by Close**: Close was against the aligned direction\n\n")

    def close_outcome_table(subset, label):
        w(f"### {label}\n\n")
        wr = subset[subset["close_out"] == "Worked and Remained"]
        rev = subset[subset["close_out"] == "Reversed by Close"]
        n = len(subset)
        w("| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg Range% |\n")
        w("|---------------|------:|--:|----------------:|----------:|---------:|-----------:|\n")
        if len(wr) > 0:
            w(f"| Worked and Remained | {len(wr)} | {pct(len(wr), n)}% "
              f"| {fmt(wr['actual_open_close_pct'].mean())} "
              f"| {fmt(wr['intraday_high_pct'].mean())} "
              f"| {fmt(wr['intraday_low_pct'].mean())} "
              f"| {fmt(wr['actual_range_pct'].mean())} |\n")
        if len(rev) > 0:
            w(f"| Reversed by Close | {len(rev)} | {pct(len(rev), n)}% "
              f"| {fmt(rev['actual_open_close_pct'].mean())} "
              f"| {fmt(rev['intraday_high_pct'].mean())} "
              f"| {fmt(rev['intraday_low_pct'].mean())} "
              f"| {fmt(rev['actual_range_pct'].mean())} |\n")
        w("\n")

    close_outcome_table(aligned, f"Overall ({n_aligned} aligned days)")

    # Bullish / Bearish
    for sub, label in [(bull_aligned, f"Bullish Alignment ({n_bull} days)"),
                       (bear_aligned, f"Bearish Alignment ({n_bear} days)")]:
        w(f"### {label}\n\n")
        wr = sub[sub["close_out"] == "Worked and Remained"]
        rev = sub[sub["close_out"] == "Reversed by Close"]
        n = len(sub)
        w("| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |\n")
        w("|---------------|------:|--:|----------------:|----------:|---------:|\n")
        if len(wr) > 0:
            w(f"| Worked and Remained | {len(wr)} | {pct(len(wr), n)}% "
              f"| {fmt(wr['actual_open_close_pct'].mean())} "
              f"| {fmt(wr['intraday_high_pct'].mean())} "
              f"| {fmt(wr['intraday_low_pct'].mean())} |\n")
        if len(rev) > 0:
            w(f"| Reversed by Close | {len(rev)} | {pct(len(rev), n)}% "
              f"| {fmt(rev['actual_open_close_pct'].mean())} "
              f"| {fmt(rev['intraday_high_pct'].mean())} "
              f"| {fmt(rev['intraday_low_pct'].mean())} |\n")
        w("\n")

    # Expiry vs Non-Expiry
    w("### Worked and Remained: Expiry vs Non-Expiry\n\n")
    w("| Context | Aligned | Worked and Remained | % | Reversed by Close | % |\n")
    w("|---------|--------:|--------------------:|--:|------------------:|--:|\n")
    for ctx, mask in [("Expiry Days", aligned["is_expiry"] == 1),
                      ("Non-Expiry Days", aligned["is_expiry"] == 0)]:
        sub = aligned[mask]
        n = len(sub)
        wr = len(sub[sub["close_out"] == "Worked and Remained"])
        rev = len(sub[sub["close_out"] == "Reversed by Close"])
        if n > 0:
            w(f"| {ctx} | {n} | {wr} | {pct(wr, n)}% | {rev} | {pct(rev, n)}% |\n")
        else:
            w(f"| {ctx} | 0 | 0 | - | 0 | - |\n")
    w("\n")

    # VIX Regime
    w("### Worked and Remained: VIX Regime\n\n")
    w("| VIX Regime | Aligned | Worked and Remained | % | Reversed by Close | % |\n")
    w("|------------|--------:|--------------------:|--:|------------------:|--:|\n")
    for regime in ["Low (<15)", "Normal (15-20)", "Elevated (20-30)", "High (>30)"]:
        sub = aligned[aligned["vix_regime"] == regime]
        n = len(sub)
        wr = len(sub[sub["close_out"] == "Worked and Remained"])
        rev = len(sub[sub["close_out"] == "Reversed by Close"])
        if n > 0:
            w(f"| {regime} | {n} | {wr} | {pct(wr, n)}% | {rev} | {pct(rev, n)}% |\n")
        else:
            w(f"| {regime} | 0 | 0 | - | 0 | - |\n")
    w("\n")

    # Year-over-Year
    w("### Worked and Remained: Year-over-Year\n\n")
    w("| Year | Aligned | Worked and Remained | % | Reversed by Close | % |\n")
    w("|------|--------:|--------------------:|--:|------------------:|--:|\n")
    for year in sorted(aligned["year"].unique()):
        sub = aligned[aligned["year"] == year]
        n = len(sub)
        wr = len(sub[sub["close_out"] == "Worked and Remained"])
        rev = len(sub[sub["close_out"] == "Reversed by Close"])
        w(f"| {year} | {n} | {wr} | {pct(wr, n)}% | {rev} | {pct(rev, n)}% |\n")
    w("\n")

    # =====================================================================
    # VIX HALF-RANGE EXHAUSTION
    # =====================================================================
    vix_aligned = aligned[aligned["vix_exhaust"].notna()]
    n_vix = len(vix_aligned)

    if n_vix > 0:
        w("## VIX Half-Range Exhaustion: Did the Move Exhaust Before Reversing?\n\n")
        w("Compares the first-half move in the aligned direction against **half of the VIX-predicted range**.\n")
        w("If the move exceeded half the predicted range, it suggests momentum exhaustion before reversal.\n")
        w("If it reversed before reaching half, the reversal happened without significant momentum.\n\n")
        w("- **Exceeded Half then Reversed**: Aligned-direction move > ½ × VIX predicted range\n")
        w("- **Reversed Before Half**: Aligned-direction move ≤ ½ × VIX predicted range\n\n")

        w(f"### Overall ({n_vix} aligned days with VIX data)\n\n")
        w("| VIX Exhaustion | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg VIX Predicted% |\n")
        w("|----------------|------:|--:|----------------:|----------:|---------:|-------------------:|\n")
        for ex_type in ["Exceeded Half then Reversed", "Reversed Before Half"]:
            sub = vix_aligned[vix_aligned["vix_exhaust"] == ex_type]
            n = len(sub)
            if n > 0:
                w(f"| {ex_type} | {n} | {pct(n, n_vix)}% "
                  f"| {fmt(sub['actual_open_close_pct'].mean())} "
                  f"| {fmt(sub['intraday_high_pct'].mean())} "
                  f"| {fmt(sub['intraday_low_pct'].mean())} "
                  f"| {fmt(sub['vix_predicted_pct'].mean())} |\n")
        w("\n")

        # Cross-tab
        w("### Cross-Tab: VIX Exhaustion × Close Outcome\n\n")
        w("Does exceeding half the VIX range predict whether the aligned view wins by close?\n\n")
        w("| VIX Exhaustion | Worked and Remained | % | Reversed by Close | % | Total |\n")
        w("|----------------|--------------------:|--:|------------------:|--:|------:|\n")
        for ex_type in ["Exceeded Half then Reversed", "Reversed Before Half"]:
            sub = vix_aligned[vix_aligned["vix_exhaust"] == ex_type]
            n = len(sub)
            wr = len(sub[sub["close_out"] == "Worked and Remained"])
            rev = len(sub[sub["close_out"] == "Reversed by Close"])
            if n > 0:
                w(f"| {ex_type} | {wr} | {pct(wr, n)}% | {rev} | {pct(rev, n)}% | {n} |\n")
        w("\n")

        # Bullish / Bearish VIX exhaustion
        for sub_df, label in [(vix_aligned[vix_aligned["align"] == "Bullish Alignment"],
                                f"Bullish Alignment ({len(vix_aligned[vix_aligned['align'] == 'Bullish Alignment'])} days)"),
                               (vix_aligned[vix_aligned["align"] == "Bearish Alignment"],
                                f"Bearish Alignment ({len(vix_aligned[vix_aligned['align'] == 'Bearish Alignment'])} days)")]:
            w(f"### {label}\n\n")
            w("| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |\n")
            w("|----------------|------:|--:|--------------------:|----:|----------------:|\n")
            n = len(sub_df)
            for ex_type in ["Exceeded Half then Reversed", "Reversed Before Half"]:
                ex = sub_df[sub_df["vix_exhaust"] == ex_type]
                ne = len(ex)
                wr = len(ex[ex["close_out"] == "Worked and Remained"])
                if ne > 0:
                    w(f"| {ex_type} | {ne} | {pct(ne, n)}% "
                      f"| {wr} | {pct(wr, ne)}% "
                      f"| {fmt(ex['actual_open_close_pct'].mean())} |\n")
            w("\n")

        # VIX Exhaustion by VIX Regime
        w("### VIX Exhaustion by VIX Regime\n\n")
        w("| VIX Regime | Total | Exceeded Half | % | Reversed Before Half | % |\n")
        w("|------------|------:|--------------:|--:|---------------------:|--:|\n")
        for regime in ["Low (<15)", "Normal (15-20)", "Elevated (20-30)", "High (>30)"]:
            sub = vix_aligned[vix_aligned["vix_regime"] == regime]
            n = len(sub)
            exc = len(sub[sub["vix_exhaust"] == "Exceeded Half then Reversed"])
            rev = len(sub[sub["vix_exhaust"] == "Reversed Before Half"])
            if n > 0:
                w(f"| {regime} | {n} | {exc} | {pct(exc, n)}% | {rev} | {pct(rev, n)}% |\n")
            else:
                w(f"| {regime} | 0 | 0 | - | 0 | - |\n")
        w("\n")

    # =====================================================================
    # STRONG ALIGNMENT
    # =====================================================================
    w("## Strong Alignment Analysis\n\n")
    w("Strong alignment = both FII and PRO have Bullish/Strong Bullish or Bearish/Strong Bearish\n")
    w("(excluding Mildly variants).\n\n")

    strong_bull = aligned[(aligned["fii_view"].isin(STRONG_BULLISH)) & (aligned["pro_view"].isin(STRONG_BULLISH))]
    strong_bear = aligned[(aligned["fii_view"].isin(STRONG_BEARISH)) & (aligned["pro_view"].isin(STRONG_BEARISH))]
    strong_all = pd.concat([strong_bull, strong_bear])

    w("| Category | Total | Worked then Reversed | % | Against then Recovered | % |\n")
    w("|----------|------:|---------------------:|--:|-----------------------:|--:|\n")
    for label, sub in [("Strong Bullish", strong_bull), ("Strong Bearish", strong_bear), ("All Strong Aligned", strong_all)]:
        n = len(sub)
        wk = len(sub[sub["pattern"] == "Worked then Reversed"])
        ag = len(sub[sub["pattern"] == "Against then Recovered"])
        if n > 0:
            w(f"| {label} | {n} | {wk} | {pct(wk, n)}% | {ag} | {pct(ag, n)}% |\n")
        else:
            w(f"| {label} | 0 | 0 | - | 0 | - |\n")
    w("\n")

    # =====================================================================
    # MIXED DAYS
    # =====================================================================
    w("## Mixed Days: When FII and PRO Oppose Each Other\n\n")
    w("When FII and PRO have opposing directional views (one bullish, one bearish),\n")
    w("whose view wins by close?\n\n")

    mixed["mix_sub"] = mixed.apply(lambda r: mixed_subtype(r["fii_dir"], r["pro_dir"]), axis=1)

    w(f"### Overview ({n_mixed} mixed days)\n\n")
    w("| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |\n")
    w("|----------|-----:|----------:|----------:|----------------:|-----------:|\n")
    for st in ["FII Bullish + PRO Bearish", "FII Bearish + PRO Bullish", "All Mixed"]:
        sub = mixed[mixed["mix_sub"] == st] if st != "All Mixed" else mixed
        n = len(sub)
        ttd = len(sub[sub["move_direction"] == "Top to Down"])
        dtu = len(sub[sub["move_direction"] == "Down to Up"])
        flat = n - ttd - dtu
        if n > 0:
            w(f"| {st} | {n} | {ttd} ({pct(ttd, n)}%) | {dtu} ({pct(dtu, n)}%) "
              f"| {fmt(sub['actual_open_close_pct'].mean())} "
              f"| {fmt(sub['actual_range_pct'].mean())} |\n")
    w("\n")

    w("### Who Won by Close?\n\n")
    w("| Sub-Type | Days | FII Correct | FII% | PRO Correct | PRO% |\n")
    w("|----------|-----:|------------:|-----:|------------:|-----:|\n")
    for st in ["FII Bullish + PRO Bearish", "FII Bearish + PRO Bullish"]:
        sub = mixed[mixed["mix_sub"] == st]
        n = len(sub)
        if n > 0:
            if st == "FII Bullish + PRO Bearish":
                fii_correct = len(sub[sub["actual_open_close_pct"] > 0])
                pro_correct = len(sub[sub["actual_open_close_pct"] < 0])
            else:
                fii_correct = len(sub[sub["actual_open_close_pct"] < 0])
                pro_correct = len(sub[sub["actual_open_close_pct"] > 0])
            w(f"| {st} | {n} | {fii_correct} | {pct(fii_correct, n)}% "
              f"| {pro_correct} | {pct(pro_correct, n)}% |\n")
    w("\n")

    # Mixed: Expiry vs Non-Expiry
    w("### Mixed Days: Expiry vs Non-Expiry\n\n")
    w("| Context | Days | Avg Open→Close% | Avg Range% |\n")
    w("|---------|-----:|----------------:|-----------:|\n")
    for ctx, mask in [("Expiry", mixed["is_expiry"] == 1),
                      ("Non-Expiry", mixed["is_expiry"] == 0)]:
        sub = mixed[mask]
        n = len(sub)
        if n > 0:
            w(f"| {ctx} | {n} | {fmt(sub['actual_open_close_pct'].mean())} "
              f"| {fmt(sub['actual_range_pct'].mean())} |\n")
        else:
            w(f"| {ctx} | 0 | - | - |\n")
    w("\n")

    # =====================================================================
    # NEUTRAL DAYS
    # =====================================================================
    w("## Neutral Days: When One or Both Sides Have No View\n\n")
    w("When one or both participants are Neutral, there is no directional consensus.\n")
    w("Does a solo directional view from one side carry any weight?\n\n")

    neutral["neut_sub"] = neutral.apply(lambda r: neutral_subtype(r["fii_dir"], r["pro_dir"], r["fii_view"], r["pro_view"]), axis=1)

    w(f"### Overview ({n_neutral} neutral days)\n\n")
    w("| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |\n")
    w("|----------|-----:|----------:|----------:|----------------:|-----------:|\n")
    for st in ["Both Neutral", "FII Neutral + PRO Bullish", "FII Neutral + PRO Bearish",
                "FII Bullish + PRO Neutral", "FII Bearish + PRO Neutral", "All Neutral/Unclear"]:
        sub = neutral[neutral["neut_sub"] == st] if st != "All Neutral/Unclear" else neutral
        n = len(sub)
        ttd = len(sub[sub["move_direction"] == "Top to Down"])
        dtu = len(sub[sub["move_direction"] == "Down to Up"])
        if n > 0:
            w(f"| {st} | {n} | {ttd} ({pct(ttd, n)}%) | {dtu} ({pct(dtu, n)}%) "
              f"| {fmt(sub['actual_open_close_pct'].mean())} "
              f"| {fmt(sub['actual_range_pct'].mean())} |\n")
    w("\n")

    # Solo view accuracy
    w("### Solo View Accuracy: Did the One Directional Side Win?\n\n")
    w("| Sub-Type | Days | View Correct | % | Avg Open→Close% |\n")
    w("|----------|-----:|-------------:|--:|----------------:|\n")
    for st in ["FII Neutral + PRO Bullish", "FII Neutral + PRO Bearish",
                "FII Bullish + PRO Neutral", "FII Bearish + PRO Neutral"]:
        sub = neutral[neutral["neut_sub"] == st]
        n = len(sub)
        if n > 0:
            if "Bullish" in st:
                correct = len(sub[sub["actual_open_close_pct"] > 0])
            else:
                correct = len(sub[sub["actual_open_close_pct"] < 0])
            w(f"| {st} | {n} | {correct} | {pct(correct, n)}% "
              f"| {fmt(sub['actual_open_close_pct'].mean())} |\n")
    w("\n")

    # =====================================================================
    # RANGE COMPARISON
    # =====================================================================
    w("### Range Comparison: Aligned vs Mixed vs Neutral\n\n")
    w("| Category | Days | Avg Range% | Avg High% | Avg Low% |\n")
    w("|----------|-----:|-----------:|----------:|---------:|\n")
    for label, sub in [("Aligned", aligned), ("Mixed", mixed), ("Neutral/Unclear", neutral)]:
        n = len(sub)
        if n > 0:
            w(f"| {label} | {n} | {fmt(sub['actual_range_pct'].mean())} "
              f"| {fmt(sub['intraday_high_pct'].mean())} "
              f"| {fmt(sub['intraday_low_pct'].mean())} |\n")
    w("\n")

    # =====================================================================
    # EXPIRY VS NON-EXPIRY
    # =====================================================================
    w("## Expiry vs Non-Expiry\n\n")
    w("| Context | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg High% | Avg Low% |\n")
    w("|---------|-------------:|---------------------:|--:|-----------------------:|--:|----------:|---------:|\n")
    for ctx, mask in [("Expiry Days", aligned["is_expiry"] == 1),
                      ("Non-Expiry Days", aligned["is_expiry"] == 0)]:
        sub = aligned[mask]
        n = len(sub)
        wk = len(sub[sub["pattern"] == "Worked then Reversed"])
        ag = len(sub[sub["pattern"] == "Against then Recovered"])
        if n > 0:
            w(f"| {ctx} | {n} | {wk} | {pct(wk, n)}% | {ag} | {pct(ag, n)}% "
              f"| {fmt(sub['intraday_high_pct'].mean())} "
              f"| {fmt(sub['intraday_low_pct'].mean())} |\n")
        else:
            w(f"| {ctx} | 0 | 0 | - | 0 | - | - | - |\n")
    w("\n")

    # =====================================================================
    # VIX REGIME ANALYSIS
    # =====================================================================
    w("## VIX Regime Analysis\n\n")
    w("| VIX Regime | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg Range% |\n")
    w("|------------|-------------:|---------------------:|--:|-----------------------:|--:|-----------:|\n")
    for regime in ["Low (<15)", "Normal (15-20)", "Elevated (20-30)", "High (>30)"]:
        sub = aligned[aligned["vix_regime"] == regime]
        n = len(sub)
        wk = len(sub[sub["pattern"] == "Worked then Reversed"])
        ag = len(sub[sub["pattern"] == "Against then Recovered"])
        if n > 0:
            w(f"| {regime} | {n} | {wk} | {pct(wk, n)}% | {ag} | {pct(ag, n)}% "
              f"| {fmt(sub['actual_range_pct'].mean())} |\n")
        else:
            w(f"| {regime} | 0 | 0 | - | 0 | - | - |\n")
    w("\n")

    # =====================================================================
    # YEAR-OVER-YEAR
    # =====================================================================
    w("## Year-over-Year Trends\n\n")
    w("| Year | Trading Days | Aligned Days | Alignment% | Bullish Aligned | Bearish Aligned | Worked then Reversed | Reversal% |\n")
    w("|------|------------:|-------------:|-----------:|----------------:|----------------:|---------------------:|----------:|\n")
    for year in sorted(df["year"].unique()):
        yr = df[df["year"] == year]
        yr_al = aligned[aligned["year"] == year]
        yr_bull = bull_aligned[bull_aligned["year"] == year]
        yr_bear = bear_aligned[bear_aligned["year"] == year]
        yr_wk = yr_al[yr_al["pattern"] == "Worked then Reversed"]
        n = len(yr)
        na = len(yr_al)
        w(f"| {year} | {n} | {na} | {pct(na, n)}% "
          f"| {len(yr_bull)} | {len(yr_bear)} "
          f"| {len(yr_wk)} | {pct(len(yr_wk), na) if na > 0 else '-'}% |\n")
    w("\n")

    # =====================================================================
    # DETAILED BULLISH / BEARISH
    # =====================================================================
    w("## Detailed: Bullish Alignment Days\n\n")
    w("When FII+PRO both lean bullish:\n\n")
    w("- **Top to Down** (Worked then Reversed): Market rose in first half (aligned), then sold off\n")
    w("- **Down to Up** (Against then Recovered): Market fell in first half (against view), then recovered\n\n")
    w("| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |\n")
    w("|---------|------:|--:|-------------------:|-------------------:|-----------------:|\n")
    for pat in ["Worked then Reversed (Top→Down)", "Against then Recovered (Down→Up)"]:
        if "Worked" in pat:
            sub = bull_aligned[bull_aligned["pattern"] == "Worked then Reversed"]
        else:
            sub = bull_aligned[bull_aligned["pattern"] == "Against then Recovered"]
        n = len(sub)
        if n > 0:
            w(f"| {pat} | {n} | {pct(n, n_bull)}% "
              f"| {fmt(sub['intraday_high_pct'].mean())} "
              f"| {fmt(sub['intraday_low_pct'].mean())} "
              f"| {fmt(sub['actual_open_close_pct'].mean())} |\n")
    w("\n")

    w("## Detailed: Bearish Alignment Days\n\n")
    w("When FII+PRO both lean bearish:\n\n")
    w("- **Down to Up** (Worked then Reversed): Market fell in first half (aligned), then recovered\n")
    w("- **Top to Down** (Against then Recovered): Market rose in first half (against view), then sold off\n\n")
    w("| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |\n")
    w("|---------|------:|--:|-------------------:|-------------------:|-----------------:|\n")
    for pat in ["Worked then Reversed (Down→Up)", "Against then Recovered (Top→Down)"]:
        if "Worked" in pat:
            sub = bear_aligned[bear_aligned["pattern"] == "Worked then Reversed"]
        else:
            sub = bear_aligned[bear_aligned["pattern"] == "Against then Recovered"]
        n = len(sub)
        if n > 0:
            w(f"| {pat} | {n} | {pct(n, n_bear)}% "
              f"| {fmt(sub['intraday_high_pct'].mean())} "
              f"| {fmt(sub['intraday_low_pct'].mean())} "
              f"| {fmt(sub['actual_open_close_pct'].mean())} |\n")
    w("\n")

    # =====================================================================
    # KEY FINDINGS
    # =====================================================================
    w("## Key Findings\n\n")

    wr_all = len(aligned[aligned["pattern"] == "Worked then Reversed"])
    ag_all = len(aligned[aligned["pattern"] == "Against then Recovered"])
    wr_pct_all = pct(wr_all, n_aligned)
    co_wr = len(aligned[aligned["close_out"] == "Worked and Remained"])
    co_wr_pct = pct(co_wr, n_aligned)

    bull_wr = len(bull_aligned[bull_aligned["pattern"] == "Worked then Reversed"])
    bear_wr = len(bear_aligned[bear_aligned["pattern"] == "Worked then Reversed"])

    exp_aligned = aligned[aligned["is_expiry"] == 1]
    nonexp_aligned = aligned[aligned["is_expiry"] == 0]
    exp_wr = len(exp_aligned[exp_aligned["pattern"] == "Worked then Reversed"])
    nonexp_wr = len(nonexp_aligned[nonexp_aligned["pattern"] == "Worked then Reversed"])

    strong_wr = len(strong_all[strong_all["pattern"] == "Worked then Reversed"])

    w(f"1. **Alignment frequency**: FII and PRO aligned on {n_aligned} of {n_total} days "
      f"({pct(n_aligned, n_total)}%). Bullish alignment ({n_bull}) vs Bearish alignment ({n_bear}).\n\n")

    w(f"2. **Reversal is {'the dominant pattern' if wr_pct_all > 50 else 'common but not dominant'}**: "
      f"On alignment days, \"Worked then Reversed\" occurred {wr_pct_all}% of the time "
      f"({wr_all}/{n_aligned} days). This means when institutions agree, the first half tends "
      f"to move in their direction but the second half {'often' if wr_pct_all > 40 else 'sometimes'} reverses.\n\n")

    w(f"3. **Worked and Remained (close validated view)**: On {co_wr_pct}% of alignment days "
      f"({co_wr}/{n_aligned}), the market closed in the aligned direction — meaning the institutional "
      f"consensus was ultimately correct by end of day. The remaining {pct(n_aligned - co_wr, n_aligned)}% "
      f"closed against the aligned view.\n\n")

    if n_vix > 0:
        exc_half = vix_aligned[vix_aligned["vix_exhaust"] == "Exceeded Half then Reversed"]
        rev_half = vix_aligned[vix_aligned["vix_exhaust"] == "Reversed Before Half"]
        exc_wr = len(exc_half[exc_half["close_out"] == "Worked and Remained"])
        rev_wr = len(rev_half[rev_half["close_out"] == "Worked and Remained"])
        w(f"4. **VIX half-range exhaustion**: {pct(len(exc_half), n_vix)}% of alignment days with VIX data "
          f"exceeded half the VIX-predicted range ({len(exc_half)}/{n_vix}). "
          f"Among those, {pct(exc_wr, len(exc_half)) if len(exc_half) > 0 else 0}% closed in the aligned direction "
          f"vs {pct(rev_wr, len(rev_half)) if len(rev_half) > 0 else 0}% for days that reversed before half range.\n\n")
    else:
        w("4. **VIX half-range exhaustion**: No VIX data available for aligned days.\n\n")

    w(f"5. **Bullish vs Bearish reversal**: Bullish alignment reversal rate = "
      f"{pct(bull_wr, n_bull) if n_bull > 0 else 0}%, "
      f"Bearish alignment reversal rate = {pct(bear_wr, n_bear) if n_bear > 0 else 0}%.\n\n")

    if len(exp_aligned) > 0 and len(nonexp_aligned) > 0:
        w(f"6. **Expiry effect**: Reversal rate on expiry days = "
          f"{pct(exp_wr, len(exp_aligned))}% vs non-expiry = "
          f"{pct(nonexp_wr, len(nonexp_aligned))}%.\n\n")
    else:
        w(f"6. **Expiry effect**: Expiry reversal rate = "
          f"{pct(exp_wr, len(exp_aligned)) if len(exp_aligned) > 0 else '-'}%, "
          f"non-expiry = {pct(nonexp_wr, len(nonexp_aligned)) if len(nonexp_aligned) > 0 else '-'}%.\n\n")

    n_strong = len(strong_all)
    w(f"7. **Strong alignment signal**: When both have strong views (excluding Mildly), "
      f"reversal rate = {pct(strong_wr, n_strong) if n_strong > 0 else 0}% "
      f"({strong_wr}/{n_strong} days). "
      f"{'Stronger conviction shows lower reversal tendency.' if n_strong > 0 and pct(strong_wr, n_strong) < wr_pct_all else ''}\n\n")

    # Mixed findings
    if n_mixed > 0:
        fii_b_pro_be = mixed[mixed["mix_sub"] == "FII Bullish + PRO Bearish"]
        fii_be_pro_b = mixed[mixed["mix_sub"] == "FII Bearish + PRO Bullish"]
        w(f"8. **Mixed days (opposing views)**: {n_mixed} days where FII and PRO disagreed. ")
        if len(fii_b_pro_be) > 0:
            fii_correct = len(fii_b_pro_be[fii_b_pro_be["actual_open_close_pct"] > 0])
            w(f"When FII bullish + PRO bearish ({len(fii_b_pro_be)} days): FII correct "
              f"{pct(fii_correct, len(fii_b_pro_be))}%. ")
        if len(fii_be_pro_b) > 0:
            pro_correct = len(fii_be_pro_b[fii_be_pro_b["actual_open_close_pct"] > 0])
            w(f"When FII bearish + PRO bullish ({len(fii_be_pro_b)} days): PRO correct "
              f"{pct(pro_correct, len(fii_be_pro_b))}%.")
        w("\n\n")

    # Neutral findings
    if n_neutral > 0:
        both_neut = neutral[neutral["neut_sub"] == "Both Neutral"]
        fii_bear_solo = neutral[neutral["neut_sub"] == "FII Bearish + PRO Neutral"]
        fii_bull_solo = neutral[neutral["neut_sub"] == "FII Bullish + PRO Neutral"]
        w(f"9. **Neutral days (no consensus)**: {n_neutral} days ({pct(n_neutral, n_total)}%) "
          f"where one or both sides had no view. ")
        if len(fii_bear_solo) > 0:
            correct = len(fii_bear_solo[fii_bear_solo["actual_open_close_pct"] < 0])
            w(f"FII solo bearish correct {pct(correct, len(fii_bear_solo))}% ({len(fii_bear_solo)} days). ")
        if len(fii_bull_solo) > 0:
            correct = len(fii_bull_solo[fii_bull_solo["actual_open_close_pct"] > 0])
            w(f"FII solo bullish correct {pct(correct, len(fii_bull_solo))}% ({len(fii_bull_solo)} days). ")
        w(f"Avg range on neutral days: {fmt(neutral['actual_range_pct'].mean())}.\n\n")

    # =====================================================================
    # TRADING IMPLICATIONS
    # =====================================================================
    w("## Trading Implications\n\n")
    w("- When FII and PRO align, the first-half move in their direction is not reliable for holding through the full session\n")
    w("- Consider booking profits in the first half if positioned in the direction of institutional alignment\n")
    w("- The second-half reversal pattern suggests mean-reversion trades may be viable after the initial directional move\n")
    w("- Expiry days and high-VIX regimes may amplify or dampen these patterns — check the breakdowns above\n")
    w("- Non-expiry days now included provide a broader sample for validation\n")
    w("- **This is retrospective analysis using T+1 data** — use as a framework for understanding institutional behavior, not as a standalone entry signal\n\n")

    # =====================================================================
    # DETAILED TABLES (last 6 years)
    # =====================================================================
    w("## Last 6 Years: All Examples\n\n")
    w(f"*{first_date} to {last_date} ({n_total} trading days)*\n\n")

    def detail_row(r):
        vix_pred = f"{r['vix_predicted_pct']}%" if pd.notna(r.get("vix_predicted_pct")) else "-"
        vix_ex = r.get("vix_exhaust", "-") or "-"
        return (f"| {r['date'].strftime('%Y-%m-%d')} | {r['fii_view']} | {r['pro_view']} "
                f"| {r['align']} | {r['move_direction']} | {r['pattern']} | {r['close_out']} "
                f"| {vix_ex} | {vix_pred} "
                f"| {fmt(r['actual_range_pct'])} | {fmt(r['intraday_high_pct'])} "
                f"| {fmt(r['intraday_low_pct'])} | {fmt(r['actual_open_close_pct'])} |\n")

    detail_header = ("| Date | FII View | PRO View | Alignment | Direction | Intraday Path "
                     "| Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |\n"
                     "|------|----------|----------|-----------|-----------|---------------"
                     "|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|\n")

    # Worked then Reversed
    worked = aligned[aligned["pattern"] == "Worked then Reversed"].sort_values("date", ascending=False)
    w(f"### Worked then Reversed (first half aligned, second half reversed)\n\n")
    w(detail_header)
    for _, r in worked.iterrows():
        w(detail_row(r))
    w("\n")

    # Against then Recovered
    against = aligned[aligned["pattern"] == "Against then Recovered"].sort_values("date", ascending=False)
    w(f"### Against then Recovered (first half against view, second half recovered)\n\n")
    w(detail_header)
    for _, r in against.iterrows():
        w(detail_row(r))
    w("\n")

    # Exceeded Half + Worked and Remained (strongest signal)
    if n_vix > 0:
        best = vix_aligned[(vix_aligned["vix_exhaust"] == "Exceeded Half then Reversed") &
                           (vix_aligned["close_out"] == "Worked and Remained")].sort_values("date", ascending=False)
        if len(best) > 0:
            exc_wr_pct = pct(len(best), n_vix)
            w(f"### Exceeded Half VIX Range + Worked and Remained ({len(best)} days — strongest signal)\n\n")
            w(detail_header)
            for _, r in best.iterrows():
                w(detail_row(r))
            w("\n")

        # Reversed Before Half + Reversed by Close (weak signal)
        worst = vix_aligned[(vix_aligned["vix_exhaust"] == "Reversed Before Half") &
                            (vix_aligned["close_out"] == "Reversed by Close")].sort_values("date", ascending=False)
        if len(worst) > 0:
            w(f"### Reversed Before Half VIX Range + Reversed by Close ({len(worst)} days — weak alignment)\n\n")
            w(detail_header)
            for _, r in worst.iterrows():
                w(detail_row(r))
            w("\n")

    # Mixed days detail
    if n_mixed > 0:
        w(f"### Mixed Days (FII vs PRO opposing) — {n_mixed} days\n\n")
        w("| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |\n")
        w("|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|\n")
        for _, r in mixed.sort_values("date", ascending=False).iterrows():
            vix_pred = f"{r['vix_predicted_pct']}%" if pd.notna(r.get("vix_predicted_pct")) else "-"
            w(f"| {r['date'].strftime('%Y-%m-%d')} | {r['fii_view']} | {r['pro_view']} "
              f"| {r['move_direction']} | {vix_pred} "
              f"| {fmt(r['actual_range_pct'])} | {fmt(r['intraday_high_pct'])} "
              f"| {fmt(r['intraday_low_pct'])} | {fmt(r['actual_open_close_pct'])} |\n")
        w("\n")

    # FII Solo View
    fii_solo = neutral[neutral["neut_sub"].isin(["FII Bullish + PRO Neutral", "FII Bearish + PRO Neutral"])]
    if len(fii_solo) > 0:
        w(f"### FII Solo View (PRO Neutral) — {len(fii_solo)} days\n\n")
        w("| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |\n")
        w("|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|\n")
        for _, r in fii_solo.sort_values("date", ascending=False).iterrows():
            vix_pred = f"{r['vix_predicted_pct']}%" if pd.notna(r.get("vix_predicted_pct")) else "-"
            w(f"| {r['date'].strftime('%Y-%m-%d')} | {r['fii_view']} | {r['pro_view']} "
              f"| {r['move_direction']} | {vix_pred} "
              f"| {fmt(r['actual_range_pct'])} | {fmt(r['intraday_high_pct'])} "
              f"| {fmt(r['intraday_low_pct'])} | {fmt(r['actual_open_close_pct'])} |\n")
        w("\n")

    w("\n---\n")
    w(f"*Generated from {n_total} trading days ({first_date} to {last_date})*\n")

    # Write file
    report = out.getvalue()
    OUTPUT_PATH.write_text(report)
    print(f"Report written to: {OUTPUT_PATH}")
    print(f"  Total days analyzed: {n_total}")
    print(f"  Aligned: {n_aligned} | Mixed: {n_mixed} | Neutral: {n_neutral}")
    print(f"  Bullish: {n_bull} | Bearish: {n_bear}")
    print(f"  Days with VIX: {n_vix}")


if __name__ == "__main__":
    main()
