#!/usr/bin/env python3
"""
FII/DII + Sensex VIX Expiry-Day Correlation Analysis (6-Year)

Correlates FII/DII institutional positioning data with Sensex VIX expiry-day
backtest results over 6 years (2020-2026) to determine whether institutional
flow signals improve prediction of Sensex VIX blowout days.

Inputs:
  - sensex_fii_t1_6year.csv (built by build_sensex_fii_6year.py, ~318 expiry days)
  OR if not available:
  - vix_sensex_6y_results.csv + fii_dii_backtest_daily_results.csv (1-year fallback)

Outputs (in this folder):
  - fii_dii_vix_correlation_sensex.csv (merged dataset with derived features)
  - fii_dii_vix_correlation_sensex.json (correlation stats and rule results)
  - FII_DII_VIX_CORRELATION_SENSEX_SUMMARY.md (human-readable findings)

Author: Claude Code
Date: 2026-08-26
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import json
import sys
from datetime import datetime


OUTPUT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = OUTPUT_DIR.parent


def load_6year_data() -> pd.DataFrame:
    """Load the 6-year Sensex + FII dataset."""
    sixyr_path = OUTPUT_DIR / "sensex_fii_t1_6year.csv"

    if sixyr_path.exists():
        df = pd.read_csv(sixyr_path)
        print(f"Loaded 6-year Sensex+FII data: {len(df)} rows ({df['date'].min()} to {df['date'].max()})")
        # Filter out rows where FII data is all zeros (failed fetches)
        has_fii = (df['t1_fii_fut_daily'] != 0) | (df['t1_fii_call_daily'] != 0) | (df['t1_fii_put_daily'] != 0)
        df_valid = df[has_fii].copy()
        print(f"  With valid FII data: {len(df_valid)} rows (excluded {len(df) - len(df_valid)} with no FII data)")
        return df_valid
    else:
        print(f"ERROR: 6-year dataset not found at: {sixyr_path}")
        print(f"Please run build_sensex_fii_6year.py first to fetch FII data from NSE.")
        sys.exit(1)


def compute_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute derived signals from FII T-1 daily flow data."""
    # FII put-call ratio (using daily flows)
    df["fii_pcr"] = df["t1_fii_put_daily"] / df["t1_fii_call_daily"].abs().replace(0, np.nan)

    # FII net sentiment (higher = more bullish)
    df["fii_net_flow"] = (
        df["t1_fii_fut_daily"] + df["t1_fii_call_daily"] - df["t1_fii_put_daily"]
    )

    # Binary blowout indicator
    df["is_blowout"] = (df["vix_accuracy"] == "Underestimated").astype(int)

    # Derive Sensex market direction from actual_open_close_pct
    df["sensex_direction"] = df["actual_open_close_pct"].apply(
        lambda x: "Bullish" if x > 0.1 else ("Bearish" if x < -0.1 else "Neutral")
    )

    # FII direction matches Sensex direction
    if "t1_fii_direction" in df.columns:
        df["fii_direction_matches_sensex"] = (
            df["t1_fii_direction"] == df["sensex_direction"]
        ).astype(int)

    # Above median range (alternative target with more power)
    df["above_median_range"] = (
        df["actual_range_pct"] > df["actual_range_pct"].median()
    ).astype(int)

    # VIX intraday change
    df["vix_change"] = df["vix_close"] - df["vix_open"]

    # High range (top quartile)
    df["high_range"] = (
        df["actual_range_pct"] > df["actual_range_pct"].quantile(0.75)
    ).astype(int)

    return df


def compute_correlations(df: pd.DataFrame) -> dict:
    """Compute correlations between FII signals and blowout/range."""
    results = {}

    fii_numeric = ["t1_fii_fut_daily", "t1_fii_call_daily", "t1_fii_put_daily",
                   "fii_pcr", "fii_net_flow"]
    targets = ["is_blowout", "actual_range_pct", "above_median_range", "high_range"]

    correlations = {}
    for signal in fii_numeric:
        signal_data = df[signal].dropna()
        for target in targets:
            target_data = df.loc[signal_data.index, target]
            valid = signal_data.notna() & target_data.notna()
            if valid.sum() < 10:
                continue
            r, p = stats.pearsonr(signal_data[valid], target_data[valid])
            correlations[f"{signal}_vs_{target}"] = {
                "correlation": round(r, 4),
                "p_value": round(p, 4),
                "n": int(valid.sum()),
                "significant": p < 0.05
            }
    results["fii_correlations"] = correlations

    # PRO correlations
    pro_numeric = ["t1_pro_fut_daily", "t1_pro_call_daily", "t1_pro_put_daily"]
    pro_corrs = {}
    for signal in pro_numeric:
        if signal not in df.columns:
            continue
        signal_data = df[signal].dropna()
        for target in targets:
            target_data = df.loc[signal_data.index, target]
            valid = signal_data.notna() & target_data.notna()
            if valid.sum() < 10:
                continue
            r, p = stats.pearsonr(signal_data[valid], target_data[valid])
            pro_corrs[f"{signal}_vs_{target}"] = {
                "correlation": round(r, 4),
                "p_value": round(p, 4),
                "n": int(valid.sum()),
                "significant": p < 0.05
            }
    results["pro_correlations"] = pro_corrs

    return results


def compute_cross_tabs(df: pd.DataFrame) -> dict:
    """Cross-tabulate FII stance/direction vs blowout."""
    results = {}

    # FII Stance
    if "t1_fii_stance" in df.columns:
        ct = {}
        for val in df["t1_fii_stance"].dropna().unique():
            subset = df[df["t1_fii_stance"] == val]
            n = len(subset)
            blowouts = subset["is_blowout"].sum()
            above_med = subset["above_median_range"].sum()
            ct[val] = {
                "count": int(n),
                "blowouts": int(blowouts),
                "blowout_rate": round(blowouts / n, 4) if n > 0 else 0,
                "above_median_rate": round(above_med / n, 4) if n > 0 else 0,
                "avg_range": round(subset["actual_range_pct"].mean(), 4) if n > 0 else 0,
                "small_sample": n < 10
            }
        results["t1_fii_stance"] = ct

    # FII Direction
    if "t1_fii_direction" in df.columns:
        ct = {}
        for val in df["t1_fii_direction"].dropna().unique():
            subset = df[df["t1_fii_direction"] == val]
            n = len(subset)
            blowouts = subset["is_blowout"].sum()
            above_med = subset["above_median_range"].sum()
            ct[val] = {
                "count": int(n),
                "blowouts": int(blowouts),
                "blowout_rate": round(blowouts / n, 4) if n > 0 else 0,
                "above_median_rate": round(above_med / n, 4) if n > 0 else 0,
                "avg_range": round(subset["actual_range_pct"].mean(), 4) if n > 0 else 0,
                "small_sample": n < 10
            }
        results["t1_fii_direction"] = ct

    # PRO Stance
    if "t1_pro_stance" in df.columns:
        ct = {}
        for val in df["t1_pro_stance"].dropna().unique():
            subset = df[df["t1_pro_stance"] == val]
            n = len(subset)
            blowouts = subset["is_blowout"].sum()
            above_med = subset["above_median_range"].sum()
            ct[val] = {
                "count": int(n),
                "blowouts": int(blowouts),
                "blowout_rate": round(blowouts / n, 4) if n > 0 else 0,
                "above_median_rate": round(above_med / n, 4) if n > 0 else 0,
                "avg_range": round(subset["actual_range_pct"].mean(), 4) if n > 0 else 0,
                "small_sample": n < 10
            }
        results["t1_pro_stance"] = ct

    # Nifty co-expiry
    if "is_nifty_expiry_day" in df.columns:
        ct = {}
        for val in [0, 1]:
            label = "nifty_co_expiry" if val == 1 else "sensex_only"
            subset = df[df["is_nifty_expiry_day"] == val]
            n = len(subset)
            if n == 0:
                continue
            blowouts = subset["is_blowout"].sum()
            above_med = subset["above_median_range"].sum()
            ct[label] = {
                "count": int(n),
                "blowouts": int(blowouts),
                "blowout_rate": round(blowouts / n, 4) if n > 0 else 0,
                "above_median_rate": round(above_med / n, 4) if n > 0 else 0,
                "avg_range": round(subset["actual_range_pct"].mean(), 4) if n > 0 else 0,
            }
        results["nifty_co_expiry"] = ct

    return results


def test_prediction_rules(df: pd.DataFrame) -> dict:
    """Test FII-based blowout prediction rules and compute lift."""
    base_rate = df["is_blowout"].mean()
    alt_base_rate = df["above_median_range"].mean()
    results = {
        "base_rate": round(base_rate, 4),
        "alt_base_rate_above_median_range": round(alt_base_rate, 4),
        "blowout_count": int(df["is_blowout"].sum()),
        "total_days": len(df)
    }
    rules = {}

    def eval_rule(name: str, mask: pd.Series):
        subset = df[mask]
        n = len(subset)
        if n == 0:
            return
        blowouts = subset["is_blowout"].sum()
        rate = blowouts / n
        above_med = subset["above_median_range"].sum()
        alt_rate = above_med / n
        high_range_count = subset["high_range"].sum()
        rules[name] = {
            "triggers": int(n),
            "blowouts": int(blowouts),
            "blowout_rate": round(rate, 4),
            "lift_vs_base": round(rate / base_rate, 2) if base_rate > 0 else 0,
            "above_median_range_count": int(above_med),
            "above_median_range_rate": round(alt_rate, 4),
            "alt_lift": round(alt_rate / alt_base_rate, 2) if alt_base_rate > 0 else 0,
            "high_range_count": int(high_range_count),
            "high_range_rate": round(high_range_count / n, 4),
            "avg_range": round(subset["actual_range_pct"].mean(), 4),
            "pct_of_days": round(n / len(df), 4),
            "small_sample": n < 10
        }

    # FII Direction rules
    if "t1_fii_direction" in df.columns:
        eval_rule("FII_Direction_Bearish", df["t1_fii_direction"] == "Bearish")
        eval_rule("FII_Direction_Bullish", df["t1_fii_direction"] == "Bullish")
        eval_rule("FII_Direction_Neutral", df["t1_fii_direction"] == "Neutral")

    # FII Stance rules
    if "t1_fii_stance" in df.columns:
        eval_rule("FII_Bearish_stance",
                  df["t1_fii_stance"].str.contains("Bearish", na=False))
        eval_rule("FII_Hedging_stance",
                  df["t1_fii_stance"].str.contains("Hedging", na=False))
        eval_rule("FII_Bullish_stance",
                  df["t1_fii_stance"].str.contains("Bullish", na=False))
        eval_rule("FII_Confident_stance",
                  df["t1_fii_stance"].str.contains("Confident", na=False))

    # Numeric signal rules
    eval_rule("fii_pcr_above_median", df["fii_pcr"] > df["fii_pcr"].median())
    eval_rule("fii_pcr_above_75pct", df["fii_pcr"] > df["fii_pcr"].quantile(0.75))
    eval_rule("fii_pcr_below_25pct", df["fii_pcr"] < df["fii_pcr"].quantile(0.25))
    eval_rule("fii_net_flow_negative", df["fii_net_flow"] < 0)
    eval_rule("fii_net_flow_very_negative", df["fii_net_flow"] < df["fii_net_flow"].quantile(0.25))
    eval_rule("fii_put_buying_heavy", df["t1_fii_put_daily"] > 20000)
    eval_rule("fii_fut_selling_heavy", df["t1_fii_fut_daily"] < -10000)

    # Combination rules
    eval_rule(
        "FII_Bearish_AND_VIX_lt14",
        (df.get("t1_fii_direction", pd.Series(dtype=str)) == "Bearish") & (df["vix_open"] < 14)
    )
    eval_rule(
        "FII_Bearish_AND_VIX_lt16",
        (df.get("t1_fii_direction", pd.Series(dtype=str)) == "Bearish") & (df["vix_open"] < 16)
    )

    # Nifty co-expiry combinations
    if "is_nifty_expiry_day" in df.columns:
        eval_rule("is_nifty_expiry_day", df["is_nifty_expiry_day"] == 1)
        eval_rule("sensex_only_expiry", df["is_nifty_expiry_day"] == 0)
        if "t1_fii_direction" in df.columns:
            eval_rule(
                "FII_Bearish_AND_nifty_expiry",
                (df["t1_fii_direction"] == "Bearish") & (df["is_nifty_expiry_day"] == 1)
            )

    # VIX intraday comparison signal
    eval_rule("vix_change_gt_0.5", df["vix_change"] > 0.5)
    eval_rule("vix_change_gt_1.0", df["vix_change"] > 1.0)
    eval_rule("vix_change_lt_0", df["vix_change"] < 0)

    results["rules"] = rules
    return results


def load_nifty_comparison() -> dict:
    """Load Nifty correlation results for comparison if available."""
    nifty_json = PROJECT_ROOT / "fii_dii_vix_correlation.json"
    if nifty_json.exists():
        with open(nifty_json) as f:
            return json.load(f)
    return {}


def generate_summary(
    df: pd.DataFrame,
    correlations: dict,
    cross_tabs: dict,
    rule_results: dict,
    nifty_results: dict,
):
    """Generate markdown summary report."""
    base_rate = rule_results["base_rate"]
    alt_base = rule_results["alt_base_rate_above_median_range"]
    rules = rule_results["rules"]

    lines = []
    lines.append("# FII/DII + Sensex VIX Expiry-Day Correlation Analysis (6-Year)")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Period**: {df.date.min()} to {df.date.max()}")
    lines.append(f"**Sensex Expiry Days Analyzed**: {len(df)}")
    lines.append(f"**Blowout Base Rate**: {base_rate:.1%} ({df.is_blowout.sum()}/{len(df)} days)")
    lines.append(f"**Above-Median Range Rate**: {alt_base:.1%}")
    lines.append(f"**Nifty Co-Expiry Days**: {df.is_nifty_expiry_day.sum()}/{len(df)} ({df.is_nifty_expiry_day.mean():.0%})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")

    # Best FII signal
    premarket_rules = {k: v for k, v in rules.items()
                       if not k.startswith("vix_change") and v["triggers"] >= 10}
    best_blowout = max(premarket_rules.items(), key=lambda x: x[1]["lift_vs_base"]) if premarket_rules else None
    best_alt = max(premarket_rules.items(), key=lambda x: x[1]["alt_lift"]) if premarket_rules else None
    vix_signal = rules.get("vix_change_gt_0.5", {})

    if best_blowout:
        lines.append(f"**Best FII pre-market signal (blowout)**: `{best_blowout[0]}`")
        lines.append(f"- Blowout rate: {best_blowout[1]['blowout_rate']:.0%} (lift: {best_blowout[1]['lift_vs_base']:.1f}x vs {base_rate:.0%} base)")
        lines.append(f"- Triggers on: {best_blowout[1]['triggers']}/{len(df)} days ({best_blowout[1]['pct_of_days']:.0%})")
        lines.append("")

    if best_alt:
        lines.append(f"**Best FII pre-market signal (above-median range)**: `{best_alt[0]}`")
        lines.append(f"- Above-median rate: {best_alt[1]['above_median_range_rate']:.0%} (lift: {best_alt[1]['alt_lift']:.1f}x)")
        lines.append(f"- Avg range: {best_alt[1]['avg_range']:.2f}%")
        lines.append("")

    if vix_signal:
        lines.append(f"**VIX intraday benchmark**: `vix_change > 0.5`")
        lines.append(f"- Blowout rate: {vix_signal['blowout_rate']:.0%} (lift: {vix_signal['lift_vs_base']:.1f}x)")
        lines.append(f"- Above-median rate: {vix_signal['above_median_range_rate']:.0%} (alt lift: {vix_signal['alt_lift']:.1f}x)")
        lines.append(f"- Triggers on: {vix_signal['triggers']}/{len(df)} days")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Correlations
    lines.append("## Correlation Findings (6-Year)")
    lines.append("")
    lines.append("### FII T-1 Signals vs Blowout")
    lines.append("")
    lines.append("| Signal | Correlation | p-value | Significant? | n |")
    lines.append("|--------|------------|---------|-------------|---|")
    for key, val in sorted(correlations.get("fii_correlations", {}).items(), key=lambda x: abs(x[1]["correlation"]), reverse=True):
        if "is_blowout" in key:
            sig = "Yes" if val["significant"] else "No"
            signal_name = key.replace("_vs_is_blowout", "")
            lines.append(f"| {signal_name} | {val['correlation']:+.3f} | {val['p_value']:.3f} | {sig} | {val['n']} |")
    lines.append("")

    lines.append("### FII T-1 Signals vs Actual Range")
    lines.append("")
    lines.append("| Signal | Correlation | p-value | Significant? | n |")
    lines.append("|--------|------------|---------|-------------|---|")
    for key, val in sorted(correlations.get("fii_correlations", {}).items(), key=lambda x: abs(x[1]["correlation"]), reverse=True):
        if "actual_range_pct" in key:
            sig = "Yes" if val["significant"] else "No"
            signal_name = key.replace("_vs_actual_range_pct", "")
            lines.append(f"| {signal_name} | {val['correlation']:+.3f} | {val['p_value']:.3f} | {sig} | {val['n']} |")
    lines.append("")

    lines.append("### FII T-1 Signals vs Above-Median Range")
    lines.append("")
    lines.append("| Signal | Correlation | p-value | Significant? | n |")
    lines.append("|--------|------------|---------|-------------|---|")
    for key, val in sorted(correlations.get("fii_correlations", {}).items(), key=lambda x: abs(x[1]["correlation"]), reverse=True):
        if "above_median_range" in key:
            sig = "Yes" if val["significant"] else "No"
            signal_name = key.replace("_vs_above_median_range", "")
            lines.append(f"| {signal_name} | {val['correlation']:+.3f} | {val['p_value']:.3f} | {sig} | {val['n']} |")
    lines.append("")

    # PRO correlations
    if correlations.get("pro_correlations"):
        lines.append("### PRO T-1 Signals vs Blowout")
        lines.append("")
        lines.append("| Signal | Correlation | p-value | Significant? | n |")
        lines.append("|--------|------------|---------|-------------|---|")
        for key, val in sorted(correlations.get("pro_correlations", {}).items(), key=lambda x: abs(x[1]["correlation"]), reverse=True):
            if "is_blowout" in key:
                sig = "Yes" if val["significant"] else "No"
                signal_name = key.replace("_vs_is_blowout", "")
                lines.append(f"| {signal_name} | {val['correlation']:+.3f} | {val['p_value']:.3f} | {sig} | {val['n']} |")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Cross-tabs
    lines.append("## FII Stance vs Blowout (6-Year)")
    lines.append("")

    if "t1_fii_stance" in cross_tabs:
        lines.append("| Stance | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |")
        lines.append("|--------|-------|----------|-------------|---------------|-----------|")
        sorted_stances = sorted(cross_tabs["t1_fii_stance"].items(), key=lambda x: x[1]["blowout_rate"], reverse=True)
        for val, data in sorted_stances:
            flag = " ⚠️" if data.get("small_sample") else ""
            lines.append(f"| {val}{flag} | {data['count']} | {data['blowouts']} | {data['blowout_rate']:.0%} | {data['above_median_rate']:.0%} | {data['avg_range']:.2f}% |")
        lines.append("")

    if "t1_fii_direction" in cross_tabs:
        lines.append("### FII Direction vs Blowout")
        lines.append("")
        lines.append("| Direction | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |")
        lines.append("|-----------|-------|----------|-------------|---------------|-----------|")
        for val, data in cross_tabs["t1_fii_direction"].items():
            lines.append(f"| {val} | {data['count']} | {data['blowouts']} | {data['blowout_rate']:.0%} | {data['above_median_rate']:.0%} | {data['avg_range']:.2f}% |")
        lines.append("")

    if "nifty_co_expiry" in cross_tabs:
        lines.append("### Nifty Co-Expiry Effect")
        lines.append("")
        lines.append("| Type | Count | Blowouts | Blowout Rate | Above-Med Rate | Avg Range |")
        lines.append("|------|-------|----------|-------------|---------------|-----------|")
        for val, data in cross_tabs["nifty_co_expiry"].items():
            lines.append(f"| {val} | {data['count']} | {data['blowouts']} | {data['blowout_rate']:.0%} | {data['above_median_rate']:.0%} | {data['avg_range']:.2f}% |")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Rules
    lines.append("## Prediction Rule Testing (6-Year)")
    lines.append("")
    lines.append(f"**Base blowout rate**: {base_rate:.0%} ({df.is_blowout.sum()}/{len(df)} days)")
    lines.append(f"**Above-median range rate**: {alt_base:.0%}")
    lines.append("")
    lines.append("### All Rules Ranked by Blowout Lift")
    lines.append("")
    lines.append("| Rule | Triggers | Blowout Rate | Lift | Above-Med Rate | Alt Lift | Avg Range | Type |")
    lines.append("|------|----------|-------------|------|---------------|----------|-----------|------|")
    sorted_rules = sorted(rules.items(), key=lambda x: x[1]["lift_vs_base"], reverse=True)
    for name, data in sorted_rules:
        rule_type = "Intraday" if "vix_change" in name else "Pre-market"
        flag = " ⚠️" if data.get("small_sample") else ""
        lines.append(f"| {name}{flag} | {data['triggers']} | {data['blowout_rate']:.0%} | {data['lift_vs_base']:.1f}x | {data['above_median_range_rate']:.0%} | {data['alt_lift']:.1f}x | {data['avg_range']:.2f}% | {rule_type} |")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Nifty comparison
    lines.append("## Sensex vs Nifty Comparison")
    lines.append("")
    if nifty_results:
        nifty_meta = nifty_results.get("metadata", {})
        lines.append("| Metric | Sensex (6yr) | Nifty (1yr overlap) |")
        lines.append("|--------|-------------|-------------------|")
        lines.append(f"| Days analyzed | {len(df)} | {nifty_meta.get('expiry_days', 'N/A')} |")
        lines.append(f"| Blowout count | {df.is_blowout.sum()} | {nifty_meta.get('blowout_count', 'N/A')} |")
        lines.append(f"| Blowout rate | {base_rate:.1%} | {nifty_meta.get('base_rate', 0):.1%} |")
        lines.append("")
    else:
        lines.append("*Nifty correlation results not found for comparison.*")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Trading Implications
    lines.append("## Trading Implications")
    lines.append("")

    premarket_lifts = [v["lift_vs_base"] for k, v in rules.items()
                       if not k.startswith("vix_change") and v["triggers"] >= 10]
    max_lift = max(premarket_lifts) if premarket_lifts else 0

    premarket_alt_lifts = [v["alt_lift"] for k, v in rules.items()
                           if not k.startswith("vix_change") and v["triggers"] >= 10]
    max_alt_lift = max(premarket_alt_lifts) if premarket_alt_lifts else 0

    if max_lift >= 1.5:
        lines.append(f"1. **FII signals show meaningful blowout prediction**: Best pre-market signal achieves {max_lift:.1f}x lift over {base_rate:.0%} base rate")
        lines.append("2. FII stance/direction on T-1 adds value for blowout prediction on Sensex expiry days")
    else:
        lines.append(f"1. **FII signals show limited blowout prediction**: Best pre-market signal achieves only {max_lift:.1f}x lift over {base_rate:.0%} base rate")

    if max_alt_lift >= 1.3:
        lines.append(f"3. **FII signals predict higher-than-normal ranges**: Best signal achieves {max_alt_lift:.1f}x lift for above-median range days")
    else:
        lines.append(f"3. **FII signals do not reliably predict range magnitude**: Best alt lift is only {max_alt_lift:.1f}x")

    if vix_signal:
        lines.append(f"4. **VIX intraday remains dominant**: {vix_signal['blowout_rate']:.0%} blowout rate ({vix_signal['lift_vs_base']:.1f}x lift)")

    lines.append("")
    lines.append("### Recommendation")
    lines.append("")
    if max_lift >= 2.0:
        lines.append("FII positioning data provides meaningful pre-market blowout signals for Sensex. Integrate FII stance into the pre-market risk assessment — particularly when FII shows bearish/hedging patterns.")
    elif max_lift >= 1.5:
        lines.append("FII positioning data adds marginal pre-market value for Sensex. Use as a secondary sizing signal alongside VIX intraday confirmation.")
    else:
        lines.append("FII positioning data does NOT reliably predict Sensex VIX blowouts. Continue using VIX intraday behavior as the primary signal.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Analysis based on {len(df)} Sensex expiry days with valid FII T-1 data.*")
    lines.append("")

    summary_path = OUTPUT_DIR / "FII_DII_VIX_CORRELATION_SENSEX_SUMMARY.md"
    summary_path.write_text("\n".join(lines))
    print(f"Written: {summary_path}")


def main():
    print("=" * 60)
    print("FII/DII + SENSEX VIX CORRELATION ANALYSIS (6-YEAR)")
    print("=" * 60)
    print()

    # 1. Load data
    df = load_6year_data()
    print()

    # 2. Compute derived features
    df = compute_derived_features(df)
    print(f"Derived features computed:")
    print(f"  is_blowout: {df.is_blowout.sum()}/{len(df)} ({df.is_blowout.mean():.1%})")
    print(f"  above_median_range: {df.above_median_range.sum()}/{len(df)}")
    print(f"  high_range (top 25%): {df.high_range.sum()}/{len(df)}")
    if "t1_fii_direction" in df.columns:
        print(f"  FII direction distribution:")
        for d, count in df["t1_fii_direction"].value_counts().items():
            print(f"    {d}: {count} ({count/len(df)*100:.1f}%)")
    print()

    # 3. Correlations
    print("Computing correlations...")
    correlations = compute_correlations(df)
    print(f"  FII correlations: {len(correlations.get('fii_correlations', {}))} pairs")
    print(f"  PRO correlations: {len(correlations.get('pro_correlations', {}))} pairs")
    print()

    # 4. Cross-tabs
    print("Computing cross-tabulations...")
    cross_tabs = compute_cross_tabs(df)
    print(f"  Categories: {list(cross_tabs.keys())}")
    print()

    # 5. Test rules
    print("Testing prediction rules...")
    rule_results = test_prediction_rules(df)
    print(f"  Rules tested: {len(rule_results['rules'])}")
    print(f"  Base blowout rate: {rule_results['base_rate']:.1%}")
    print(f"  Alt target rate: {rule_results['alt_base_rate_above_median_range']:.1%}")
    print()

    # 6. Nifty comparison
    nifty_results = load_nifty_comparison()
    if nifty_results:
        print(f"Nifty comparison loaded: {nifty_results.get('metadata', {}).get('expiry_days', '?')} days")
    print()

    # 7. Write outputs
    print("Writing outputs...")

    # CSV
    csv_path = OUTPUT_DIR / "fii_dii_vix_correlation_sensex.csv"
    df.to_csv(csv_path, index=False)
    print(f"  Written: {csv_path} ({len(df)} rows)")

    # JSON
    json_output = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "index": "Sensex",
            "period": f"{df.date.min()} to {df.date.max()}",
            "expiry_days": len(df),
            "blowout_count": int(df.is_blowout.sum()),
            "base_rate": round(df.is_blowout.mean(), 4),
            "alt_target_above_median_range": round(df.above_median_range.mean(), 4),
            "data_source": "6-year Sensex VIX + NSE FII T-1 daily flows",
        },
        "correlations": correlations,
        "cross_tabs": cross_tabs,
        "rules": rule_results,
        "nifty_comparison": {
            "available": bool(nifty_results),
            "nifty_base_rate": nifty_results.get("metadata", {}).get("base_rate") if nifty_results else None,
        }
    }
    json_path = OUTPUT_DIR / "fii_dii_vix_correlation_sensex.json"
    json_path.write_text(json.dumps(json_output, indent=2, default=str))
    print(f"  Written: {json_path}")

    # Summary
    generate_summary(df, correlations, cross_tabs, rule_results, nifty_results)
    print()

    # 8. Key findings
    print("=" * 60)
    print("KEY FINDINGS (6-YEAR)")
    print("=" * 60)
    print()

    print(f"Sample: {len(df)} Sensex expiry days, {df.is_blowout.sum()} blowouts ({df.is_blowout.mean():.1%})")
    print()

    print("Top correlations (FII vs blowout):")
    blowout_corrs = {k: v for k, v in correlations.get("fii_correlations", {}).items() if "is_blowout" in k}
    for k, v in sorted(blowout_corrs.items(), key=lambda x: abs(x[1]["correlation"]), reverse=True)[:5]:
        sig = "*" if v["significant"] else ""
        print(f"  {k.replace('_vs_is_blowout', '')}: r={v['correlation']:+.3f} (p={v['p_value']:.3f}){sig}")
    print()

    print("Top correlations (FII vs range):")
    range_corrs = {k: v for k, v in correlations.get("fii_correlations", {}).items() if "actual_range_pct" in k}
    for k, v in sorted(range_corrs.items(), key=lambda x: abs(x[1]["correlation"]), reverse=True)[:5]:
        sig = "*" if v["significant"] else ""
        print(f"  {k.replace('_vs_actual_range_pct', '')}: r={v['correlation']:+.3f} (p={v['p_value']:.3f}){sig}")
    print()

    print("Top prediction rules (by blowout lift, n>=10):")
    valid_rules = {k: v for k, v in rule_results["rules"].items() if v["triggers"] >= 10}
    sorted_rules = sorted(valid_rules.items(), key=lambda x: x[1]["lift_vs_base"], reverse=True)
    for name, data in sorted_rules[:7]:
        print(f"  {name}: blowout={data['blowout_rate']:.0%} (lift={data['lift_vs_base']:.1f}x), "
              f"above_med={data['above_median_range_rate']:.0%}, n={data['triggers']}")
    print()

    print("Done!")


if __name__ == "__main__":
    main()
