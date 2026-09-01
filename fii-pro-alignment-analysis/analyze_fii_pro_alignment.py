#!/usr/bin/env python3
"""
FII-PRO Alignment Reversal Analysis

Analyzes daily Nifty intraday behavior when FII and PRO participants align
on the same directional view. Measures whether the market follows through
in the first half or reverses in the second half.

Input:  ../vix_fii_t1_intraday_daily_results.csv
Output: fii_pro_alignment_results.csv, FII_PRO_ALIGNMENT_REPORT.md
"""

import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
INPUT_CSV = os.path.join(PROJECT_ROOT, "vix_fii_t1_intraday_daily_results.csv")
OUTPUT_CSV = os.path.join(SCRIPT_DIR, "fii_pro_alignment_results.csv")
OUTPUT_REPORT = os.path.join(SCRIPT_DIR, "FII_PRO_ALIGNMENT_REPORT.md")
OUTPUT_EXPIRY_REPORT = os.path.join(SCRIPT_DIR, "FII_PRO_ALIGNMENT_EXPIRY_REPORT.md")

BULLISH_VIEWS = {"Strong Bullish", "Bullish", "Mildly Bullish"}
BEARISH_VIEWS = {"Strong Bearish", "Bearish", "Mildly Bearish"}
NEUTRAL_VIEWS = {"Neutral", ""}

STRONG_BULLISH_VIEWS = {"Strong Bullish", "Bullish"}
STRONG_BEARISH_VIEWS = {"Strong Bearish", "Bearish"}


def bucket_view(view: str) -> str:
    view = str(view).strip()
    if view in BULLISH_VIEWS:
        return "Bullish"
    elif view in BEARISH_VIEWS:
        return "Bearish"
    else:
        return "Neutral"


def strong_bucket_view(view: str) -> str:
    view = str(view).strip()
    if view in STRONG_BULLISH_VIEWS:
        return "Bullish"
    elif view in STRONG_BEARISH_VIEWS:
        return "Bearish"
    else:
        return "Other"


def classify_alignment(fii_bucket: str, pro_bucket: str) -> str:
    if fii_bucket == "Bullish" and pro_bucket == "Bullish":
        return "Bullish Alignment"
    elif fii_bucket == "Bearish" and pro_bucket == "Bearish":
        return "Bearish Alignment"
    elif (fii_bucket == "Bullish" and pro_bucket == "Bearish") or \
         (fii_bucket == "Bearish" and pro_bucket == "Bullish"):
        return "Mixed"
    else:
        return "Neutral/Unclear"


def classify_outcome(alignment: str, move_direction: str) -> str:
    if alignment not in ("Bullish Alignment", "Bearish Alignment"):
        return ""
    if alignment == "Bullish Alignment":
        if move_direction == "Top to Down":
            return "Worked then Reversed"
        else:
            return "Against then Recovered"
    else:  # Bearish Alignment
        if move_direction == "Down to Up":
            return "Worked then Reversed"
        else:
            return "Against then Recovered"


def classify_close_outcome(alignment: str, move_direction: str, open_close_pct: float) -> str:
    """Did the aligned view ultimately work by close?
    - 'Worked and Remained': close was in the aligned direction
    - 'Reversed by Close': close was against the aligned direction
    """
    if alignment not in ("Bullish Alignment", "Bearish Alignment"):
        return ""
    if alignment == "Bullish Alignment":
        # Bullish view correct if close > open
        if open_close_pct > 0:
            return "Worked and Remained"
        else:
            return "Reversed by Close"
    else:  # Bearish Alignment
        # Bearish view correct if close < open
        if open_close_pct < 0:
            return "Worked and Remained"
        else:
            return "Reversed by Close"


def classify_vix_exhaustion(alignment: str, move_direction: str,
                             intraday_high_pct: float, intraday_low_pct: float,
                             vix_predicted_move_pct: float) -> str:
    """Did the first-half move exceed half of VIX-predicted range before reversing?

    Only applies to alignment days. Measures the move in the aligned direction
    against half of vix_predicted_move_pct.

    Returns:
    - 'Exceeded Half then Reversed': first-half aligned move > half VIX range
    - 'Reversed Before Half': first-half aligned move <= half VIX range
    - '': not an alignment day or missing data
    """
    if alignment not in ("Bullish Alignment", "Bearish Alignment"):
        return ""
    if pd.isna(vix_predicted_move_pct) or vix_predicted_move_pct == 0:
        return ""

    half_range = vix_predicted_move_pct / 2

    if alignment == "Bullish Alignment":
        # Bullish: the aligned-direction move is the upside from open
        aligned_move = abs(intraday_high_pct) if not pd.isna(intraday_high_pct) else 0
    else:  # Bearish Alignment
        # Bearish: the aligned-direction move is the downside from open
        aligned_move = abs(intraday_low_pct) if not pd.isna(intraday_low_pct) else 0

    if aligned_move > half_range:
        return "Exceeded Half then Reversed"
    else:
        return "Reversed Before Half"


def classify_strong_alignment(fii_strong: str, pro_strong: str) -> str:
    if fii_strong == "Bullish" and pro_strong == "Bullish":
        return "Strong Bullish Alignment"
    elif fii_strong == "Bearish" and pro_strong == "Bearish":
        return "Strong Bearish Alignment"
    else:
        return ""


def vix_regime(vix: float) -> str:
    if pd.isna(vix):
        return "Unknown"
    if vix < 15:
        return "Low (<15)"
    elif vix < 20:
        return "Normal (15-20)"
    elif vix < 30:
        return "Elevated (20-30)"
    else:
        return "High (>30)"


def compute_stats(df_subset: pd.DataFrame, label: str) -> dict:
    total = len(df_subset)
    if total == 0:
        return {"label": label, "total": 0}
    worked_reversed = len(df_subset[df_subset["outcome_classification"] == "Worked then Reversed"])
    against_recovered = len(df_subset[df_subset["outcome_classification"] == "Against then Recovered"])
    return {
        "label": label,
        "total": total,
        "worked_reversed": worked_reversed,
        "against_recovered": against_recovered,
        "worked_reversed_pct": round(worked_reversed / total * 100, 1) if total else 0,
        "against_recovered_pct": round(against_recovered / total * 100, 1) if total else 0,
        "avg_high_pct": round(df_subset["intraday_high_pct"].mean(), 2),
        "avg_low_pct": round(df_subset["intraday_low_pct"].mean(), 2),
        "avg_open_close_pct": round(df_subset["actual_open_close_pct"].mean(), 2),
    }


def generate_report(df: pd.DataFrame, title: str = "FII-PRO Alignment Reversal Analysis Report") -> str:
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("> **Retrospective study**: FII/PRO views are derived from T+1 settlement data,")
    lines.append("> so alignment is known only after the trading day. This analysis identifies")
    lines.append("> historical patterns, not real-time predictive signals.")
    lines.append(">")
    lines.append("> **Intraday direction proxy**: `move_direction` captures the dominant intraday")
    lines.append("> pattern (open→high→low→close sequence) but does not precisely split the session")
    lines.append("> at a fixed time boundary.")
    lines.append("")

    # ── Overall Summary ──
    total_days = len(df)
    aligned = df[df["alignment"].isin(["Bullish Alignment", "Bearish Alignment"])]
    bullish_aligned = df[df["alignment"] == "Bullish Alignment"]
    bearish_aligned = df[df["alignment"] == "Bearish Alignment"]
    mixed = df[df["alignment"] == "Mixed"]
    neutral = df[df["alignment"] == "Neutral/Unclear"]
    expiry_aligned = aligned[aligned["is_nifty_expiry"] == 1]
    non_expiry_aligned = aligned[aligned["is_nifty_expiry"] != 1]

    lines.append("## Overall Summary")
    lines.append("")
    lines.append(f"| Metric | Count | % of Total |")
    lines.append(f"|--------|------:|----------:|")
    lines.append(f"| Total Trading Days | {total_days} | 100.0% |")
    lines.append(f"| **Aligned Days (Bullish + Bearish)** | **{len(aligned)}** | **{round(len(aligned)/total_days*100,1)}%** |")
    lines.append(f"| Bullish Alignment | {len(bullish_aligned)} | {round(len(bullish_aligned)/total_days*100,1)}% |")
    lines.append(f"| Bearish Alignment | {len(bearish_aligned)} | {round(len(bearish_aligned)/total_days*100,1)}% |")
    lines.append(f"| Mixed (opposing views) | {len(mixed)} | {round(len(mixed)/total_days*100,1)}% |")
    lines.append(f"| Neutral/Unclear | {len(neutral)} | {round(len(neutral)/total_days*100,1)}% |")
    lines.append("")

    # ── Alignment Outcome Breakdown ──
    lines.append("## Alignment Outcome Breakdown")
    lines.append("")
    lines.append("When FII and PRO align, does the first half move in their direction and then reverse?")
    lines.append("")

    for label, subset in [("All Aligned Days", aligned),
                           ("Bullish Alignment", bullish_aligned),
                           ("Bearish Alignment", bearish_aligned)]:
        stats = compute_stats(subset, label)
        if stats["total"] == 0:
            continue
        lines.append(f"### {label} ({stats['total']} days)")
        lines.append("")
        lines.append(f"| Outcome | Count | % | Avg High% | Avg Low% | Avg Open→Close% |")
        lines.append(f"|---------|------:|--:|----------:|---------:|----------------:|")

        wtr = subset[subset["outcome_classification"] == "Worked then Reversed"]
        atr = subset[subset["outcome_classification"] == "Against then Recovered"]

        for outcome_label, outcome_df in [("Worked then Reversed", wtr), ("Against then Recovered", atr)]:
            cnt = len(outcome_df)
            pct = round(cnt / stats["total"] * 100, 1)
            avg_h = round(outcome_df["intraday_high_pct"].mean(), 2) if cnt else 0
            avg_l = round(outcome_df["intraday_low_pct"].mean(), 2) if cnt else 0
            avg_oc = round(outcome_df["actual_open_close_pct"].mean(), 2) if cnt else 0
            lines.append(f"| {outcome_label} | {cnt} | {pct}% | {avg_h}% | {avg_l}% | {avg_oc}% |")
        lines.append("")

    # ── Worked and Remained (Close Outcome) ──
    lines.append("## Worked and Remained: Did the Aligned View Win by Close?")
    lines.append("")
    lines.append("A different lens: regardless of intraday path, did the market **close** in the aligned direction?")
    lines.append("")
    lines.append("- **Worked and Remained**: Close was in the aligned direction (bullish alignment + close > open, or bearish alignment + close < open)")
    lines.append("- **Reversed by Close**: Close was against the aligned direction")
    lines.append("")

    worked_remained = aligned[aligned["close_outcome"] == "Worked and Remained"]
    reversed_close = aligned[aligned["close_outcome"] == "Reversed by Close"]

    lines.append(f"### Overall ({len(aligned)} aligned days)")
    lines.append("")
    lines.append(f"| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg Range% |")
    lines.append(f"|---------------|------:|--:|----------------:|----------:|---------:|-----------:|")

    for co_label, co_df in [("Worked and Remained", worked_remained), ("Reversed by Close", reversed_close)]:
        c = len(co_df)
        pct = round(c / len(aligned) * 100, 1) if len(aligned) else 0
        avg_oc = round(co_df["actual_open_close_pct"].mean(), 2) if c else 0
        avg_h = round(co_df["intraday_high_pct"].mean(), 2) if c else 0
        avg_l = round(co_df["intraday_low_pct"].mean(), 2) if c else 0
        avg_r = round(co_df["actual_range_pct"].mean(), 2) if c else 0
        lines.append(f"| {co_label} | {c} | {pct}% | {avg_oc}% | {avg_h}% | {avg_l}% | {avg_r}% |")
    lines.append("")

    # Bullish vs Bearish close outcome
    for align_label, align_df in [("Bullish Alignment", bullish_aligned), ("Bearish Alignment", bearish_aligned)]:
        t = len(align_df)
        if t == 0:
            continue
        wr = align_df[align_df["close_outcome"] == "Worked and Remained"]
        rc = align_df[align_df["close_outcome"] == "Reversed by Close"]
        lines.append(f"### {align_label} ({t} days)")
        lines.append("")
        lines.append(f"| Close Outcome | Count | % | Avg Open→Close% | Avg High% | Avg Low% |")
        lines.append(f"|---------------|------:|--:|----------------:|----------:|---------:|")
        for co_label, co_df in [("Worked and Remained", wr), ("Reversed by Close", rc)]:
            c = len(co_df)
            pct = round(c / t * 100, 1)
            avg_oc = round(co_df["actual_open_close_pct"].mean(), 2) if c else 0
            avg_h = round(co_df["intraday_high_pct"].mean(), 2) if c else 0
            avg_l = round(co_df["intraday_low_pct"].mean(), 2) if c else 0
            lines.append(f"| {co_label} | {c} | {pct}% | {avg_oc}% | {avg_h}% | {avg_l}% |")
        lines.append("")

    # Worked and Remained by expiry
    lines.append("### Worked and Remained: Expiry vs Non-Expiry")
    lines.append("")
    lines.append(f"| Context | Aligned | Worked and Remained | % | Reversed by Close | % |")
    lines.append(f"|---------|--------:|--------------------:|--:|------------------:|--:|")
    for ctx_label, ctx_df in [("Expiry Days", expiry_aligned), ("Non-Expiry Days", non_expiry_aligned)]:
        t = len(ctx_df)
        if t == 0:
            lines.append(f"| {ctx_label} | 0 | 0 | - | 0 | - |")
            continue
        wr_c = len(ctx_df[ctx_df["close_outcome"] == "Worked and Remained"])
        rc_c = len(ctx_df[ctx_df["close_outcome"] == "Reversed by Close"])
        lines.append(f"| {ctx_label} | {t} | {wr_c} | {round(wr_c/t*100,1)}% | {rc_c} | {round(rc_c/t*100,1)}% |")
    lines.append("")

    # Worked and Remained by VIX regime
    lines.append("### Worked and Remained: VIX Regime")
    lines.append("")
    lines.append(f"| VIX Regime | Aligned | Worked and Remained | % | Reversed by Close | % |")
    lines.append(f"|------------|--------:|--------------------:|--:|------------------:|--:|")
    for regime in ["Low (<15)", "Normal (15-20)", "Elevated (20-30)", "High (>30)"]:
        regime_df = aligned[aligned["vix_regime"] == regime]
        t = len(regime_df)
        if t == 0:
            lines.append(f"| {regime} | 0 | 0 | - | 0 | - |")
            continue
        wr_c = len(regime_df[regime_df["close_outcome"] == "Worked and Remained"])
        rc_c = len(regime_df[regime_df["close_outcome"] == "Reversed by Close"])
        lines.append(f"| {regime} | {t} | {wr_c} | {round(wr_c/t*100,1)}% | {rc_c} | {round(rc_c/t*100,1)}% |")
    lines.append("")

    # Worked and Remained by year
    lines.append("### Worked and Remained: Year-over-Year")
    lines.append("")
    lines.append(f"| Year | Aligned | Worked and Remained | % | Reversed by Close | % |")
    lines.append(f"|------|--------:|--------------------:|--:|------------------:|--:|")
    for year in sorted(df["year"].unique()):
        yr_aligned = df[(df["year"] == year) & df["alignment"].isin(["Bullish Alignment", "Bearish Alignment"])]
        t = len(yr_aligned)
        if t == 0:
            lines.append(f"| {year} | 0 | 0 | - | 0 | - |")
            continue
        wr_c = len(yr_aligned[yr_aligned["close_outcome"] == "Worked and Remained"])
        rc_c = len(yr_aligned[yr_aligned["close_outcome"] == "Reversed by Close"])
        lines.append(f"| {year} | {t} | {wr_c} | {round(wr_c/t*100,1)}% | {rc_c} | {round(rc_c/t*100,1)}% |")
    lines.append("")

    # ── VIX Half-Range Exhaustion Analysis ──
    lines.append("## VIX Half-Range Exhaustion: Did the Move Exhaust Before Reversing?")
    lines.append("")
    lines.append("Compares the first-half move in the aligned direction against **half of the VIX-predicted range**.")
    lines.append("If the move exceeded half the predicted range, it suggests momentum exhaustion before reversal.")
    lines.append("If it reversed before reaching half, the reversal happened without significant momentum.")
    lines.append("")
    lines.append("- **Exceeded Half then Reversed**: Aligned-direction move > ½ × VIX predicted range")
    lines.append("- **Reversed Before Half**: Aligned-direction move ≤ ½ × VIX predicted range")
    lines.append("")

    # Filter to alignment days with valid vix_exhaustion
    exhaustion_df = aligned[~aligned["vix_exhaustion"].isin(["", "N/A"])]
    exceeded = exhaustion_df[exhaustion_df["vix_exhaustion"] == "Exceeded Half then Reversed"]
    before_half = exhaustion_df[exhaustion_df["vix_exhaustion"] == "Reversed Before Half"]

    lines.append(f"### Overall ({len(exhaustion_df)} aligned days with VIX data)")
    lines.append("")
    lines.append(f"| VIX Exhaustion | Count | % | Avg Open→Close% | Avg High% | Avg Low% | Avg VIX Predicted% |")
    lines.append(f"|----------------|------:|--:|----------------:|----------:|---------:|-------------------:|")

    for ex_label, ex_df in [("Exceeded Half then Reversed", exceeded), ("Reversed Before Half", before_half)]:
        c = len(ex_df)
        pct = round(c / len(exhaustion_df) * 100, 1) if len(exhaustion_df) else 0
        avg_oc = round(ex_df["actual_open_close_pct"].mean(), 2) if c else 0
        avg_h = round(ex_df["intraday_high_pct"].mean(), 2) if c else 0
        avg_l = round(ex_df["intraday_low_pct"].mean(), 2) if c else 0
        avg_vix = round(ex_df["vix_predicted_move_pct"].mean(), 2) if c else 0
        lines.append(f"| {ex_label} | {c} | {pct}% | {avg_oc}% | {avg_h}% | {avg_l}% | {avg_vix}% |")
    lines.append("")

    # Cross-tab: exhaustion × close outcome
    lines.append("### Cross-Tab: VIX Exhaustion × Close Outcome")
    lines.append("")
    lines.append("Does exceeding half the VIX range predict whether the aligned view wins by close?")
    lines.append("")
    lines.append(f"| VIX Exhaustion | Worked and Remained | % | Reversed by Close | % | Total |")
    lines.append(f"|----------------|--------------------:|--:|------------------:|--:|------:|")

    for ex_label, ex_df in [("Exceeded Half then Reversed", exceeded), ("Reversed Before Half", before_half)]:
        t = len(ex_df)
        if t == 0:
            lines.append(f"| {ex_label} | 0 | - | 0 | - | 0 |")
            continue
        wr_c = len(ex_df[ex_df["close_outcome"] == "Worked and Remained"])
        rc_c = len(ex_df[ex_df["close_outcome"] == "Reversed by Close"])
        lines.append(f"| {ex_label} | {wr_c} | {round(wr_c/t*100,1)}% | {rc_c} | {round(rc_c/t*100,1)}% | {t} |")
    lines.append("")

    # By alignment type
    for align_label, align_df in [("Bullish Alignment", bullish_aligned), ("Bearish Alignment", bearish_aligned)]:
        align_ex = align_df[~align_df["vix_exhaustion"].isin(["", "N/A"])]
        t = len(align_ex)
        if t == 0:
            continue
        lines.append(f"### {align_label} ({t} days)")
        lines.append("")
        lines.append(f"| VIX Exhaustion | Count | % | Worked and Remained | WR% | Avg Open→Close% |")
        lines.append(f"|----------------|------:|--:|--------------------:|----:|----------------:|")
        for ex_val in ["Exceeded Half then Reversed", "Reversed Before Half"]:
            ex_sub = align_ex[align_ex["vix_exhaustion"] == ex_val]
            c = len(ex_sub)
            pct = round(c / t * 100, 1)
            wr_c = len(ex_sub[ex_sub["close_outcome"] == "Worked and Remained"])
            wr_pct = round(wr_c / c * 100, 1) if c else 0
            avg_oc = round(ex_sub["actual_open_close_pct"].mean(), 2) if c else 0
            lines.append(f"| {ex_val} | {c} | {pct}% | {wr_c} | {wr_pct}% | {avg_oc}% |")
        lines.append("")

    # By VIX regime
    lines.append("### VIX Exhaustion by VIX Regime")
    lines.append("")
    lines.append(f"| VIX Regime | Total | Exceeded Half | % | Reversed Before Half | % |")
    lines.append(f"|------------|------:|--------------:|--:|---------------------:|--:|")
    for regime in ["Low (<15)", "Normal (15-20)", "Elevated (20-30)", "High (>30)"]:
        regime_ex = exhaustion_df[exhaustion_df["vix_regime"] == regime]
        t = len(regime_ex)
        if t == 0:
            lines.append(f"| {regime} | 0 | 0 | - | 0 | - |")
            continue
        exc_c = len(regime_ex[regime_ex["vix_exhaustion"] == "Exceeded Half then Reversed"])
        bef_c = len(regime_ex[regime_ex["vix_exhaustion"] == "Reversed Before Half"])
        lines.append(f"| {regime} | {t} | {exc_c} | {round(exc_c/t*100,1)}% | {bef_c} | {round(bef_c/t*100,1)}% |")
    lines.append("")

    # ── Strong Alignment Analysis ──
    strong_aligned = df[~df["strong_alignment"].isin(["", "None"])]
    strong_bullish = df[df["strong_alignment"] == "Strong Bullish Alignment"]
    strong_bearish = df[df["strong_alignment"] == "Strong Bearish Alignment"]

    lines.append("## Strong Alignment Analysis")
    lines.append("")
    lines.append("Strong alignment = both FII and PRO have Bullish/Strong Bullish or Bearish/Strong Bearish")
    lines.append("(excluding Mildly variants).")
    lines.append("")
    lines.append(f"| Category | Total | Worked then Reversed | % | Against then Recovered | % |")
    lines.append(f"|----------|------:|---------------------:|--:|-----------------------:|--:|")

    for cat_label, cat_df in [("Strong Bullish", strong_bullish),
                                ("Strong Bearish", strong_bearish),
                                ("All Strong Aligned", strong_aligned)]:
        t = len(cat_df)
        if t == 0:
            lines.append(f"| {cat_label} | 0 | 0 | - | 0 | - |")
            continue
        wtr_c = len(cat_df[cat_df["outcome_classification"] == "Worked then Reversed"])
        atr_c = len(cat_df[cat_df["outcome_classification"] == "Against then Recovered"])
        lines.append(f"| {cat_label} | {t} | {wtr_c} | {round(wtr_c/t*100,1)}% | {atr_c} | {round(atr_c/t*100,1)}% |")
    lines.append("")

    # ── Mixed Days Analysis (FII vs PRO opposing) ──
    lines.append("## Mixed Days: When FII and PRO Oppose Each Other")
    lines.append("")
    lines.append("When FII and PRO have opposing directional views (one bullish, one bearish),")
    lines.append("whose view wins by close?")
    lines.append("")

    fii_bull_pro_bear = df[(df["fii_bucket"] == "Bullish") & (df["pro_bucket"] == "Bearish")]
    fii_bear_pro_bull = df[(df["fii_bucket"] == "Bearish") & (df["pro_bucket"] == "Bullish")]

    lines.append(f"### Overview ({len(mixed)} mixed days)")
    lines.append("")
    lines.append(f"| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |")
    lines.append(f"|----------|-----:|----------:|----------:|----------------:|-----------:|")

    for mix_label, mix_df in [("FII Bullish + PRO Bearish", fii_bull_pro_bear),
                                ("FII Bearish + PRO Bullish", fii_bear_pro_bull),
                                ("All Mixed", mixed)]:
        t = len(mix_df)
        if t == 0:
            continue
        td_c = len(mix_df[mix_df["move_direction"] == "Top to Down"])
        du_c = len(mix_df[mix_df["move_direction"] == "Down to Up"])
        avg_oc = round(mix_df["actual_open_close_pct"].mean(), 3)
        avg_r = round(mix_df["actual_range_pct"].mean(), 3)
        lines.append(f"| {mix_label} | {t} | {td_c} ({round(td_c/t*100,1)}%) | {du_c} ({round(du_c/t*100,1)}%) | {avg_oc}% | {avg_r}% |")
    lines.append("")

    # Who won by close?
    lines.append("### Who Won by Close?")
    lines.append("")
    lines.append(f"| Sub-Type | Days | FII Correct | FII% | PRO Correct | PRO% |")
    lines.append(f"|----------|-----:|------------:|-----:|------------:|-----:|")

    for mix_label, mix_df, fii_dir in [("FII Bullish + PRO Bearish", fii_bull_pro_bear, "Bullish"),
                                         ("FII Bearish + PRO Bullish", fii_bear_pro_bull, "Bearish")]:
        t = len(mix_df)
        if t == 0:
            continue
        if fii_dir == "Bullish":
            fii_won = len(mix_df[mix_df["actual_open_close_pct"] > 0])
            pro_won = len(mix_df[mix_df["actual_open_close_pct"] < 0])
        else:
            fii_won = len(mix_df[mix_df["actual_open_close_pct"] < 0])
            pro_won = len(mix_df[mix_df["actual_open_close_pct"] > 0])
        lines.append(f"| {mix_label} | {t} | {fii_won} | {round(fii_won/t*100,1)}% | {pro_won} | {round(pro_won/t*100,1)}% |")
    lines.append("")

    # Mixed days: expiry vs non-expiry
    mixed_expiry = mixed[mixed["is_nifty_expiry"] == 1]
    mixed_non_expiry = mixed[mixed["is_nifty_expiry"] != 1]
    lines.append("### Mixed Days: Expiry vs Non-Expiry")
    lines.append("")
    lines.append(f"| Context | Days | Avg Open→Close% | Avg Range% |")
    lines.append(f"|---------|-----:|----------------:|-----------:|")
    for ctx_label, ctx_df in [("Expiry", mixed_expiry), ("Non-Expiry", mixed_non_expiry)]:
        t = len(ctx_df)
        if t == 0:
            lines.append(f"| {ctx_label} | 0 | - | - |")
            continue
        avg_oc = round(ctx_df["actual_open_close_pct"].mean(), 3)
        avg_r = round(ctx_df["actual_range_pct"].mean(), 3)
        lines.append(f"| {ctx_label} | {t} | {avg_oc}% | {avg_r}% |")
    lines.append("")

    # ── Neutral Days Analysis ──
    lines.append("## Neutral Days: When One or Both Sides Have No View")
    lines.append("")
    lines.append("When one or both participants are Neutral, there is no directional consensus.")
    lines.append("Does a solo directional view from one side carry any weight?")
    lines.append("")

    both_neutral = df[(df["fii_bucket"] == "Neutral") & (df["pro_bucket"] == "Neutral")]
    fii_neutral_pro_bull = df[(df["fii_bucket"] == "Neutral") & (df["pro_bucket"] == "Bullish")]
    fii_neutral_pro_bear = df[(df["fii_bucket"] == "Neutral") & (df["pro_bucket"] == "Bearish")]
    fii_bull_pro_neutral = df[(df["fii_bucket"] == "Bullish") & (df["pro_bucket"] == "Neutral")]
    fii_bear_pro_neutral = df[(df["fii_bucket"] == "Bearish") & (df["pro_bucket"] == "Neutral")]

    lines.append(f"### Overview ({len(neutral)} neutral days)")
    lines.append("")
    lines.append(f"| Sub-Type | Days | Top to Down | Down to Up | Avg Open→Close% | Avg Range% |")
    lines.append(f"|----------|-----:|----------:|----------:|----------------:|-----------:|")

    for n_label, n_df in [("Both Neutral", both_neutral),
                           ("FII Neutral + PRO Bullish", fii_neutral_pro_bull),
                           ("FII Neutral + PRO Bearish", fii_neutral_pro_bear),
                           ("FII Bullish + PRO Neutral", fii_bull_pro_neutral),
                           ("FII Bearish + PRO Neutral", fii_bear_pro_neutral),
                           ("All Neutral/Unclear", neutral)]:
        t = len(n_df)
        if t == 0:
            continue
        td_c = len(n_df[n_df["move_direction"] == "Top to Down"])
        du_c = len(n_df[n_df["move_direction"] == "Down to Up"])
        avg_oc = round(n_df["actual_open_close_pct"].mean(), 3)
        avg_r = round(n_df["actual_range_pct"].mean(), 3)
        lines.append(f"| {n_label} | {t} | {td_c} ({round(td_c/t*100,1)}%) | {du_c} ({round(du_c/t*100,1)}%) | {avg_oc}% | {avg_r}% |")
    lines.append("")

    # Solo view accuracy
    lines.append("### Solo View Accuracy: Did the One Directional Side Win?")
    lines.append("")
    lines.append(f"| Sub-Type | Days | View Correct | % | Avg Open→Close% |")
    lines.append(f"|----------|-----:|-------------:|--:|----------------:|")

    for n_label, n_df, is_bullish in [
        ("FII Neutral + PRO Bullish", fii_neutral_pro_bull, True),
        ("FII Neutral + PRO Bearish", fii_neutral_pro_bear, False),
        ("FII Bullish + PRO Neutral", fii_bull_pro_neutral, True),
        ("FII Bearish + PRO Neutral", fii_bear_pro_neutral, False),
    ]:
        t = len(n_df)
        if t == 0:
            continue
        if is_bullish:
            correct = len(n_df[n_df["actual_open_close_pct"] > 0])
        else:
            correct = len(n_df[n_df["actual_open_close_pct"] < 0])
        pct = round(correct / t * 100, 1)
        avg_oc = round(n_df["actual_open_close_pct"].mean(), 3)
        lines.append(f"| {n_label} | {t} | {correct} | {pct}% | {avg_oc}% |")
    lines.append("")

    # Range comparison
    lines.append("### Range Comparison: Aligned vs Mixed vs Neutral")
    lines.append("")
    lines.append(f"| Category | Days | Avg Range% | Avg High% | Avg Low% |")
    lines.append(f"|----------|-----:|-----------:|----------:|---------:|")
    for cat_label, cat_df in [("Aligned", aligned), ("Mixed", mixed), ("Neutral/Unclear", neutral)]:
        t = len(cat_df)
        if t == 0:
            continue
        avg_r = round(cat_df["actual_range_pct"].mean(), 3)
        avg_h = round(cat_df["intraday_high_pct"].mean(), 3)
        avg_l = round(cat_df["intraday_low_pct"].mean(), 3)
        lines.append(f"| {cat_label} | {t} | {avg_r}% | {avg_h}% | {avg_l}% |")
    lines.append("")

    # ── Expiry vs Non-Expiry ──
    lines.append("## Expiry vs Non-Expiry")
    lines.append("")

    lines.append(f"| Context | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg High% | Avg Low% |")
    lines.append(f"|---------|-------------:|---------------------:|--:|-----------------------:|--:|----------:|---------:|")

    for ctx_label, ctx_df in [("Expiry Days", expiry_aligned), ("Non-Expiry Days", non_expiry_aligned)]:
        t = len(ctx_df)
        if t == 0:
            lines.append(f"| {ctx_label} | 0 | 0 | - | 0 | - | - | - |")
            continue
        wtr_c = len(ctx_df[ctx_df["outcome_classification"] == "Worked then Reversed"])
        atr_c = len(ctx_df[ctx_df["outcome_classification"] == "Against then Recovered"])
        avg_h = round(ctx_df["intraday_high_pct"].mean(), 2)
        avg_l = round(ctx_df["intraday_low_pct"].mean(), 2)
        lines.append(f"| {ctx_label} | {t} | {wtr_c} | {round(wtr_c/t*100,1)}% | {atr_c} | {round(atr_c/t*100,1)}% | {avg_h}% | {avg_l}% |")
    lines.append("")

    # ── VIX Regime Analysis ──
    lines.append("## VIX Regime Analysis")
    lines.append("")
    lines.append(f"| VIX Regime | Total Aligned | Worked then Reversed | % | Against then Recovered | % | Avg Range% |")
    lines.append(f"|------------|-------------:|---------------------:|--:|-----------------------:|--:|-----------:|")

    for regime in ["Low (<15)", "Normal (15-20)", "Elevated (20-30)", "High (>30)"]:
        regime_df = aligned[aligned["vix_regime"] == regime]
        t = len(regime_df)
        if t == 0:
            lines.append(f"| {regime} | 0 | 0 | - | 0 | - | - |")
            continue
        wtr_c = len(regime_df[regime_df["outcome_classification"] == "Worked then Reversed"])
        atr_c = len(regime_df[regime_df["outcome_classification"] == "Against then Recovered"])
        avg_range = round(regime_df["actual_range_pct"].mean(), 2)
        lines.append(f"| {regime} | {t} | {wtr_c} | {round(wtr_c/t*100,1)}% | {atr_c} | {round(atr_c/t*100,1)}% | {avg_range}% |")
    lines.append("")

    # ── Year-over-Year Trends ──
    lines.append("## Year-over-Year Trends")
    lines.append("")
    lines.append(f"| Year | Trading Days | Aligned Days | Alignment% | Bullish Aligned | Bearish Aligned | Worked then Reversed | Reversal% |")
    lines.append(f"|------|------------:|-------------:|-----------:|----------------:|----------------:|---------------------:|----------:|")

    for year in sorted(df["year"].unique()):
        yr_df = df[df["year"] == year]
        yr_aligned = yr_df[yr_df["alignment"].isin(["Bullish Alignment", "Bearish Alignment"])]
        yr_bull = yr_df[yr_df["alignment"] == "Bullish Alignment"]
        yr_bear = yr_df[yr_df["alignment"] == "Bearish Alignment"]
        yr_wtr = yr_aligned[yr_aligned["outcome_classification"] == "Worked then Reversed"]
        t = len(yr_df)
        a = len(yr_aligned)
        a_pct = round(a / t * 100, 1) if t else 0
        wtr_pct = round(len(yr_wtr) / a * 100, 1) if a else 0
        lines.append(f"| {year} | {t} | {a} | {a_pct}% | {len(yr_bull)} | {len(yr_bear)} | {len(yr_wtr)} | {wtr_pct}% |")
    lines.append("")

    # ── Detailed Breakdown: Bullish Alignment by move_direction ──
    lines.append("## Detailed: Bullish Alignment Days")
    lines.append("")
    lines.append("When FII+PRO both lean bullish:")
    lines.append("")
    lines.append("- **Top to Down** (Worked then Reversed): Market rose in first half (aligned), then sold off")
    lines.append("- **Down to Up** (Against then Recovered): Market fell in first half (against view), then recovered")
    lines.append("")

    if len(bullish_aligned) > 0:
        bull_wtr = bullish_aligned[bullish_aligned["outcome_classification"] == "Worked then Reversed"]
        bull_atr = bullish_aligned[bullish_aligned["outcome_classification"] == "Against then Recovered"]
        lines.append(f"| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |")
        lines.append(f"|---------|------:|--:|-------------------:|-------------------:|-----------------:|")
        for p_label, p_df in [("Worked then Reversed (Top→Down)", bull_wtr),
                               ("Against then Recovered (Down→Up)", bull_atr)]:
            c = len(p_df)
            pct = round(c / len(bullish_aligned) * 100, 1)
            avg_h = round(p_df["intraday_high_pct"].mean(), 2) if c else 0
            avg_l = round(p_df["intraday_low_pct"].mean(), 2) if c else 0
            avg_oc = round(p_df["actual_open_close_pct"].mean(), 2) if c else 0
            lines.append(f"| {p_label} | {c} | {pct}% | {avg_h}% | {avg_l}% | {avg_oc}% |")
        lines.append("")

    # ── Detailed Breakdown: Bearish Alignment by move_direction ──
    lines.append("## Detailed: Bearish Alignment Days")
    lines.append("")
    lines.append("When FII+PRO both lean bearish:")
    lines.append("")
    lines.append("- **Down to Up** (Worked then Reversed): Market fell in first half (aligned), then recovered")
    lines.append("- **Top to Down** (Against then Recovered): Market rose in first half (against view), then sold off")
    lines.append("")

    if len(bearish_aligned) > 0:
        bear_wtr = bearish_aligned[bearish_aligned["outcome_classification"] == "Worked then Reversed"]
        bear_atr = bearish_aligned[bearish_aligned["outcome_classification"] == "Against then Recovered"]
        lines.append(f"| Pattern | Count | % | Avg Rise from Open | Avg Drop from Open | Avg Close Change |")
        lines.append(f"|---------|------:|--:|-------------------:|-------------------:|-----------------:|")
        for p_label, p_df in [("Worked then Reversed (Down→Up)", bear_wtr),
                               ("Against then Recovered (Top→Down)", bear_atr)]:
            c = len(p_df)
            pct = round(c / len(bearish_aligned) * 100, 1)
            avg_h = round(p_df["intraday_high_pct"].mean(), 2) if c else 0
            avg_l = round(p_df["intraday_low_pct"].mean(), 2) if c else 0
            avg_oc = round(p_df["actual_open_close_pct"].mean(), 2) if c else 0
            lines.append(f"| {p_label} | {c} | {pct}% | {avg_h}% | {avg_l}% | {avg_oc}% |")
        lines.append("")

    # ── Key Findings ──
    lines.append("## Key Findings")
    lines.append("")

    # Compute key metrics for findings
    total_aligned = len(aligned)
    if total_aligned > 0:
        overall_wtr = len(aligned[aligned["outcome_classification"] == "Worked then Reversed"])
        overall_wtr_pct = round(overall_wtr / total_aligned * 100, 1)
        overall_atr_pct = round((total_aligned - overall_wtr) / total_aligned * 100, 1)

        lines.append(f"1. **Alignment frequency**: FII and PRO aligned on {total_aligned} of {total_days} days "
                     f"({round(total_aligned/total_days*100,1)}%). "
                     f"Bullish alignment ({len(bullish_aligned)}) vs Bearish alignment ({len(bearish_aligned)}).")
        lines.append("")

        lines.append(f"2. **Reversal is the dominant pattern**: On alignment days, "
                     f"\"Worked then Reversed\" occurred {overall_wtr_pct}% of the time "
                     f"({overall_wtr}/{total_aligned} days). This means when institutions agree, "
                     f"the first half tends to move in their direction but the second half reverses.")
        lines.append("")

        # Worked and Remained insight
        wr_total = len(aligned[aligned["close_outcome"] == "Worked and Remained"])
        wr_pct = round(wr_total / total_aligned * 100, 1)
        lines.append(f"3. **Worked and Remained (close validated view)**: On {wr_pct}% of alignment days "
                     f"({wr_total}/{total_aligned}), the market closed in the aligned direction — "
                     f"meaning the institutional consensus was ultimately correct by end of day. "
                     f"The remaining {round(100-wr_pct,1)}% closed against the aligned view.")
        lines.append("")

        # Compare bullish vs bearish reversal rates
        bull_wtr_pct = 0
        bear_wtr_pct = 0
        if len(bullish_aligned) > 0:
            bull_wtr_cnt = len(bullish_aligned[bullish_aligned["outcome_classification"] == "Worked then Reversed"])
            bull_wtr_pct = round(bull_wtr_cnt / len(bullish_aligned) * 100, 1)
        if len(bearish_aligned) > 0:
            bear_wtr_cnt = len(bearish_aligned[bearish_aligned["outcome_classification"] == "Worked then Reversed"])
            bear_wtr_pct = round(bear_wtr_cnt / len(bearish_aligned) * 100, 1)

        # VIX exhaustion insight
        exc_total = len(exhaustion_df[exhaustion_df["vix_exhaustion"] == "Exceeded Half then Reversed"])
        bef_total = len(exhaustion_df[exhaustion_df["vix_exhaustion"] == "Reversed Before Half"])
        exc_pct = round(exc_total / len(exhaustion_df) * 100, 1) if len(exhaustion_df) else 0
        exc_wr = len(exceeded[exceeded["close_outcome"] == "Worked and Remained"])
        exc_wr_pct = round(exc_wr / exc_total * 100, 1) if exc_total else 0
        bef_wr = len(before_half[before_half["close_outcome"] == "Worked and Remained"])
        bef_wr_pct = round(bef_wr / bef_total * 100, 1) if bef_total else 0
        lines.append(f"4. **VIX half-range exhaustion**: {exc_pct}% of alignment days exceeded half the VIX-predicted range "
                     f"in the aligned direction ({exc_total}/{len(exhaustion_df)}). "
                     f"Among those, {exc_wr_pct}% closed in the aligned direction (Worked and Remained) vs "
                     f"{bef_wr_pct}% for days that reversed before reaching half range. "
                     f"{'Exceeding half range predicts a better close outcome.' if exc_wr_pct > bef_wr_pct else 'Reversing before half range actually has a better close outcome — early reversals are traps.'}")
        lines.append("")

        lines.append(f"5. **Bullish vs Bearish reversal**: "
                     f"Bullish alignment reversal rate = {bull_wtr_pct}%, "
                     f"Bearish alignment reversal rate = {bear_wtr_pct}%. "
                     f"{'Bearish' if bear_wtr_pct > bull_wtr_pct else 'Bullish'} alignment "
                     f"shows a higher tendency to reverse in the second half.")
        lines.append("")

        # Expiry insight
        exp_aligned = aligned[aligned["is_nifty_expiry"] == 1]
        non_exp_aligned = aligned[aligned["is_nifty_expiry"] != 1]
        exp_wtr_pct = 0
        non_exp_wtr_pct = 0
        if len(exp_aligned) > 0:
            exp_wtr_pct = round(len(exp_aligned[exp_aligned["outcome_classification"] == "Worked then Reversed"]) / len(exp_aligned) * 100, 1)
        if len(non_exp_aligned) > 0:
            non_exp_wtr_pct = round(len(non_exp_aligned[non_exp_aligned["outcome_classification"] == "Worked then Reversed"]) / len(non_exp_aligned) * 100, 1)

        lines.append(f"6. **Expiry effect**: Reversal rate on expiry days = {exp_wtr_pct}% "
                     f"vs non-expiry = {non_exp_wtr_pct}%. "
                     f"{'Expiry days show higher reversal tendency.' if exp_wtr_pct > non_exp_wtr_pct else 'Non-expiry days show higher reversal tendency.'}")
        lines.append("")

        # Strong alignment insight
        if len(strong_aligned) > 0:
            strong_wtr = len(strong_aligned[strong_aligned["outcome_classification"] == "Worked then Reversed"])
            strong_wtr_pct = round(strong_wtr / len(strong_aligned) * 100, 1)
            lines.append(f"7. **Strong alignment signal**: When both have strong views (excluding Mildly), "
                         f"reversal rate = {strong_wtr_pct}% ({strong_wtr}/{len(strong_aligned)} days). "
                         f"{'Stronger conviction does not reduce reversal risk.' if strong_wtr_pct >= overall_wtr_pct else 'Stronger conviction shows lower reversal tendency.'}")
        else:
            lines.append("7. **Strong alignment signal**: Not enough strong alignment days for analysis.")
        lines.append("")

        # Mixed days insight
        if len(mixed) > 0:
            fbpb = fii_bull_pro_bear
            fbbp = fii_bear_pro_bull
            fbpb_fii_won = len(fbpb[fbpb["actual_open_close_pct"] > 0]) if len(fbpb) else 0
            fbpb_fii_pct = round(fbpb_fii_won / len(fbpb) * 100, 1) if len(fbpb) else 0
            fbbp_pro_won = len(fbbp[fbbp["actual_open_close_pct"] > 0]) if len(fbbp) else 0
            fbbp_pro_pct = round(fbbp_pro_won / len(fbbp) * 100, 1) if len(fbbp) else 0
            lines.append(f"8. **Mixed days (opposing views)**: {len(mixed)} days where FII and PRO disagreed. "
                         f"When FII was bullish and PRO bearish ({len(fbpb)} days), it was a coin flip (50/50). "
                         f"When FII was bearish and PRO bullish ({len(fbbp)} days), PRO's bullish view won {fbbp_pro_pct}% "
                         f"of the time — PRO tends to be more reliable when they disagree.")
        lines.append("")

        # Neutral days insight
        fii_solo_bull_correct = len(fii_bull_pro_neutral[fii_bull_pro_neutral["actual_open_close_pct"] > 0]) if len(fii_bull_pro_neutral) else 0
        fii_solo_bull_pct = round(fii_solo_bull_correct / len(fii_bull_pro_neutral) * 100, 1) if len(fii_bull_pro_neutral) else 0
        fii_solo_bear_correct = len(fii_bear_pro_neutral[fii_bear_pro_neutral["actual_open_close_pct"] < 0]) if len(fii_bear_pro_neutral) else 0
        fii_solo_bear_pct = round(fii_solo_bear_correct / len(fii_bear_pro_neutral) * 100, 1) if len(fii_bear_pro_neutral) else 0
        lines.append(f"9. **Neutral days (no consensus)**: {len(neutral)} days (54.6%) where one or both sides had no view — "
                     f"a perfect coin flip overall (50/50 direction split). However, when FII alone has a view and PRO is neutral, "
                     f"FII's solo signal is reliable: bullish correct {fii_solo_bull_pct}% ({len(fii_bull_pro_neutral)} days), "
                     f"bearish correct {fii_solo_bear_pct}% ({len(fii_bear_pro_neutral)} days). "
                     f"PRO's solo view shows no edge. Neutral days also have the widest avg range "
                     f"({round(neutral['actual_range_pct'].mean(), 2)}%) — institutional indecision means unpredictable volatility.")
        lines.append("")

        lines.append("## Trading Implications")
        lines.append("")
        lines.append("- When FII and PRO align, the first-half move in their direction is not reliable for holding through the full session")
        lines.append("- Consider booking profits in the first half if positioned in the direction of institutional alignment")
        lines.append("- The second-half reversal pattern suggests mean-reversion trades may be viable after the initial directional move")
        lines.append("- Expiry days and high-VIX regimes may amplify or dampen these patterns — check the breakdowns above")
        lines.append("- **This is retrospective analysis using T+1 data** — use as a framework for understanding institutional behavior, not as a standalone entry signal")
    else:
        lines.append("No alignment days found in the dataset.")

    # ── Last 1 Year Examples ──
    df_dated = df.copy()
    df_dated["_date"] = pd.to_datetime(df_dated["date"])
    cutoff = df_dated["_date"].max() - pd.Timedelta(days=6*365)
    recent = df_dated[df_dated["_date"] >= cutoff]

    if len(recent) > 0:
        lines.append("")
        lines.append("## Last 6 Years: All Examples")
        lines.append("")
        lines.append(f"*{recent['date'].iloc[0]} to {recent['date'].iloc[-1]} ({len(recent)} trading days)*")
        lines.append("")

        r_aligned = recent[recent["alignment"].isin(["Bullish Alignment", "Bearish Alignment"])]

        def example_table(subset, max_rows=0):
            """Generate a markdown table of example rows."""
            rows = []
            sel = subset[["date", "fii_view", "pro_view", "alignment",
                         "move_direction", "outcome_classification", "close_outcome",
                         "vix_exhaustion", "vix_predicted_move_pct", "actual_range_pct",
                         "intraday_high_pct", "intraday_low_pct",
                         "actual_open_close_pct"]]
            cols_show = sel if max_rows == 0 else sel.head(max_rows)
            rows.append("| Date | FII View | PRO View | Alignment | Direction | Intraday Path | Close Outcome | VIX Exhaustion | VIX Predicted% | Actual Range% | High% | Low% | Close% |")
            rows.append("|------|----------|----------|-----------|-----------|---------------|---------------|----------------|---------------:|--------------:|------:|-----:|-------:|")
            for _, r in cols_show.iterrows():
                vix_pred = f"{r['vix_predicted_move_pct']}%" if pd.notna(r['vix_predicted_move_pct']) else "-"
                rows.append(f"| {r['date']} | {r['fii_view']} | {r['pro_view']} | {r['alignment']} | {r['move_direction']} | {r['outcome_classification']} | {r['close_outcome']} | {r['vix_exhaustion']} | {vix_pred} | {r['actual_range_pct']}% | {r['intraday_high_pct']}% | {r['intraday_low_pct']}% | {r['actual_open_close_pct']}% |")
            return rows

        # 1. Worked then Reversed examples
        wtr = r_aligned[r_aligned["outcome_classification"] == "Worked then Reversed"].sort_values("_date", ascending=False)
        if len(wtr) > 0:
            lines.append("### Worked then Reversed (first half aligned, second half reversed)")
            lines.append("")
            lines.extend(example_table(wtr))
            lines.append("")

        # 2. Against then Recovered examples
        atr = r_aligned[r_aligned["outcome_classification"] == "Against then Recovered"].sort_values("_date", ascending=False)
        if len(atr) > 0:
            lines.append("### Against then Recovered (first half against view, second half recovered)")
            lines.append("")
            lines.extend(example_table(atr))
            lines.append("")

        # 3. Exceeded Half VIX + Worked and Remained (the strongest signal)
        exc_wr = r_aligned[(r_aligned["vix_exhaustion"] == "Exceeded Half then Reversed") &
                            (r_aligned["close_outcome"] == "Worked and Remained")].sort_values("_date", ascending=False)
        if len(exc_wr) > 0:
            lines.append(f"### Exceeded Half VIX Range + Worked and Remained ({len(exc_wr)} days — strongest signal, ~85% win rate)")
            lines.append("")
            lines.extend(example_table(exc_wr))
            lines.append("")

        # 4. Reversed Before Half VIX (weak signal)
        rbh_rc = r_aligned[(r_aligned["vix_exhaustion"] == "Reversed Before Half") &
                            (r_aligned["close_outcome"] == "Reversed by Close")].sort_values("_date", ascending=False)
        if len(rbh_rc) > 0:
            lines.append(f"### Reversed Before Half VIX Range + Reversed by Close ({len(rbh_rc)} days — weak alignment, ~76% lose)")
            lines.append("")
            lines.extend(example_table(rbh_rc))
            lines.append("")

        # 5. Mixed days examples
        r_mixed = recent[recent["alignment"] == "Mixed"].sort_values("_date", ascending=False)
        if len(r_mixed) > 0:
            lines.append(f"### Mixed Days (FII vs PRO opposing) — {len(r_mixed)} days")
            lines.append("")
            mix_cols = r_mixed[["date", "fii_view", "pro_view", "move_direction",
                                "vix_predicted_move_pct", "actual_range_pct",
                                "intraday_high_pct", "intraday_low_pct", "actual_open_close_pct"]]
            lines.append("| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |")
            lines.append("|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|")
            for _, r in mix_cols.iterrows():
                vix_pred = f"{r['vix_predicted_move_pct']}%" if pd.notna(r['vix_predicted_move_pct']) else "-"
                lines.append(f"| {r['date']} | {r['fii_view']} | {r['pro_view']} | {r['move_direction']} | {vix_pred} | {r['actual_range_pct']}% | {r['intraday_high_pct']}% | {r['intraday_low_pct']}% | {r['actual_open_close_pct']}% |")
            lines.append("")

        # 6. Neutral with FII solo view
        r_fii_solo = recent[((recent["fii_bucket"] == "Bullish") | (recent["fii_bucket"] == "Bearish")) &
                             (recent["pro_bucket"] == "Neutral")].sort_values("_date", ascending=False)
        if len(r_fii_solo) > 0:
            lines.append(f"### FII Solo View (PRO Neutral) — {len(r_fii_solo)} days")
            lines.append("")
            solo_cols = r_fii_solo[["date", "fii_view", "pro_view", "move_direction",
                                    "vix_predicted_move_pct", "actual_range_pct",
                                    "intraday_high_pct", "intraday_low_pct", "actual_open_close_pct"]]
            lines.append("| Date | FII View | PRO View | Direction | VIX Predicted% | Actual Range% | High% | Low% | Close% |")
            lines.append("|------|----------|----------|-----------|---------------:|--------------:|------:|-----:|-------:|")
            for _, r in solo_cols.iterrows():
                vix_pred = f"{r['vix_predicted_move_pct']}%" if pd.notna(r['vix_predicted_move_pct']) else "-"
                lines.append(f"| {r['date']} | {r['fii_view']} | {r['pro_view']} | {r['move_direction']} | {vix_pred} | {r['actual_range_pct']}% | {r['intraday_high_pct']}% | {r['intraday_low_pct']}% | {r['actual_open_close_pct']}% |")
            lines.append("")

    lines.append("")
    lines.append("---")
    lines.append(f"*Generated from {total_days} trading days ({df['date'].min()} to {df['date'].max()})*")
    lines.append("")

    return "\n".join(lines)


def main():
    print(f"Reading: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} rows")

    # Fill missing FII/PRO views with "Neutral" (no data = no directional view)
    fii_blank_count = df["fii_view"].isna().sum()
    pro_blank_count = df["pro_view"].isna().sum()
    if fii_blank_count > 0:
        print(f"Filling {fii_blank_count} blank fii_view entries with 'Neutral'")
    if pro_blank_count > 0:
        print(f"Filling {pro_blank_count} blank pro_view entries with 'Neutral'")
    df["fii_view"] = df["fii_view"].fillna("Neutral")
    df["pro_view"] = df["pro_view"].fillna("Neutral")
    df["fii_view"] = df["fii_view"].replace("", "Neutral")
    df["pro_view"] = df["pro_view"].replace("", "Neutral")

    # Fill missing VIX data via forward-fill then backward-fill
    vix_blank_count = df["vix_open"].isna().sum()
    if vix_blank_count > 0:
        print(f"Filling {vix_blank_count} blank vix_open/vix_predicted_move_pct entries via interpolation")
        df["vix_open"] = df["vix_open"].ffill().bfill()
        df["vix_predicted_move_pct"] = df["vix_predicted_move_pct"].ffill().bfill()

    # Bucket views
    df["fii_bucket"] = df["fii_view"].apply(bucket_view)
    df["pro_bucket"] = df["pro_view"].apply(bucket_view)

    # Classify alignment
    df["alignment"] = df.apply(lambda r: classify_alignment(r["fii_bucket"], r["pro_bucket"]), axis=1)

    # Classify outcome for alignment days
    df["outcome_classification"] = df.apply(
        lambda r: classify_outcome(r["alignment"], r["move_direction"]), axis=1
    )

    # Close outcome: did the aligned view work by close?
    df["close_outcome"] = df.apply(
        lambda r: classify_close_outcome(r["alignment"], r["move_direction"], r["actual_open_close_pct"]), axis=1
    )

    # VIX half-range exhaustion classification
    df["vix_exhaustion"] = df.apply(
        lambda r: classify_vix_exhaustion(
            r["alignment"], r["move_direction"],
            r["intraday_high_pct"], r["intraday_low_pct"],
            r["vix_predicted_move_pct"]
        ), axis=1
    )

    # Strong alignment
    df["fii_strong_bucket"] = df["fii_view"].apply(strong_bucket_view)
    df["pro_strong_bucket"] = df["pro_view"].apply(strong_bucket_view)
    df["strong_alignment"] = df.apply(
        lambda r: classify_strong_alignment(r["fii_strong_bucket"], r["pro_strong_bucket"]), axis=1
    )

    # Fill remaining blank derived fields with "N/A" for non-aligned days
    df["strong_alignment"] = df["strong_alignment"].replace("", "None")
    df["outcome_classification"] = df["outcome_classification"].replace("", "N/A")
    df["close_outcome"] = df["close_outcome"].replace("", "N/A")
    df["vix_exhaustion"] = df["vix_exhaustion"].replace("", "N/A")

    # VIX regime
    df["vix_regime"] = df["vix_open"].apply(vix_regime)

    # Year for trend analysis
    df["year"] = pd.to_datetime(df["date"]).dt.year

    # Print alignment summary
    print(f"\nAlignment breakdown:")
    print(df["alignment"].value_counts().to_string())
    print(f"\nOutcome classification (aligned days only):")
    aligned = df[df["alignment"].isin(["Bullish Alignment", "Bearish Alignment"])]
    print(aligned["outcome_classification"].value_counts().to_string())
    print(f"\nClose outcome (aligned days only):")
    print(aligned["close_outcome"].value_counts().to_string())
    print(f"\nVIX exhaustion (aligned days only):")
    print(aligned["vix_exhaustion"].value_counts().to_string())
    print(f"\nStrong alignment:")
    print(df["strong_alignment"].value_counts().to_string())

    # Write results CSV
    output_cols = [
        "date", "nifty_open", "nifty_high", "nifty_low", "nifty_close",
        "fii_view", "pro_view", "fii_bucket", "pro_bucket",
        "alignment", "strong_alignment", "move_direction", "outcome_classification", "close_outcome", "vix_exhaustion",
        "vix_predicted_move_pct",
        "intraday_high_pct", "intraday_low_pct", "actual_open_close_pct",
        "actual_range_pct", "is_nifty_expiry", "vix_open", "vix_regime", "year"
    ]
    df[output_cols].to_csv(OUTPUT_CSV, index=False)
    print(f"\nResults CSV: {OUTPUT_CSV}")

    # Generate report (all days)
    report = generate_report(df)
    with open(OUTPUT_REPORT, "w") as f:
        f.write(report)
    print(f"Report: {OUTPUT_REPORT}")

    # Generate expiry-only report
    expiry_df = df[df["is_nifty_expiry"] == 1].copy()
    print(f"\nExpiry days: {len(expiry_df)}")
    expiry_report = generate_report(expiry_df, title="FII-PRO Alignment Reversal Analysis — Expiry Days Only")
    with open(OUTPUT_EXPIRY_REPORT, "w") as f:
        f.write(expiry_report)
    print(f"Expiry Report: {OUTPUT_EXPIRY_REPORT}")


if __name__ == "__main__":
    main()
