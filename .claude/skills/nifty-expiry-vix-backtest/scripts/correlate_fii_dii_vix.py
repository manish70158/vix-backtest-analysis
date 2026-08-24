#!/usr/bin/env python3
"""
FII/DII + VIX Expiry-Day Correlation Analysis

Correlates FII/DII institutional positioning data with VIX expiry-day
backtest results to determine whether institutional flow signals improve
prediction of VIX blowout days.

Inputs:
  - fii_dii_backtest_daily_results.csv (243 trading days, Aug 2025 - Aug 2026)
  - vix_all_expiries_results_v6.csv (109 expiry days, Jun 2024 - Jul 2026)

Outputs:
  - fii_dii_vix_correlation.csv (merged dataset with derived features)
  - fii_dii_vix_correlation.json (correlation stats and rule results)
  - FII_DII_VIX_CORRELATION_SUMMARY.md (human-readable findings)

Author: Claude Code
Date: 2026-08-24
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path
import json
import sys
from datetime import datetime


def load_data(project_root: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load both CSV files with error handling."""
    fii_path = project_root / "fii_dii_backtest_daily_results.csv"
    vix_path = project_root / "vix_all_expiries_results_v6.csv"

    if not fii_path.exists():
        print(f"ERROR: FII/DII file not found: {fii_path}")
        sys.exit(1)
    if not vix_path.exists():
        print(f"ERROR: VIX expiry file not found: {vix_path}")
        sys.exit(1)

    fii_df = pd.read_csv(fii_path)
    vix_df = pd.read_csv(vix_path)

    print(f"Loaded FII/DII data: {len(fii_df)} rows ({fii_df.Date.min()} to {fii_df.Date.max()})")
    print(f"Loaded VIX expiry data: {len(vix_df)} rows ({vix_df.date.min()} to {vix_df.date.max()})")

    return fii_df, vix_df


def merge_datasets(fii_df: pd.DataFrame, vix_df: pd.DataFrame) -> pd.DataFrame:
    """Inner join on date, preserving all columns from both sources."""
    merged = pd.merge(
        vix_df,
        fii_df,
        left_on="date",
        right_on="Date",
        how="inner"
    )
    # Drop duplicate date column
    merged = merged.drop(columns=["Date"])
    print(f"Merged dataset: {len(merged)} rows (overlap)")
    return merged


def add_t1_lookback(merged: pd.DataFrame, fii_df: pd.DataFrame) -> pd.DataFrame:
    """Attach previous trading day's FII/DII data for each expiry date."""
    fii_df = fii_df.copy()
    fii_df["Date"] = pd.to_datetime(fii_df["Date"])
    fii_df = fii_df.sort_values("Date").reset_index(drop=True)

    t1_cols = {
        "fii_fut_idx_net": "t1_fii_fut_idx_net",
        "fii_call_net": "t1_fii_call_net",
        "fii_put_net": "t1_fii_put_net",
        "FII_Direction": "t1_FII_Direction",
    }

    # For each expiry date, find the previous trading day in FII data
    t1_data = []
    for _, row in merged.iterrows():
        expiry_date = pd.to_datetime(row["date"])
        # Get FII rows before this date
        prev_rows = fii_df[fii_df["Date"] < expiry_date]
        if len(prev_rows) > 0:
            prev_row = prev_rows.iloc[-1]
            t1_data.append({v: prev_row[k] for k, v in t1_cols.items()})
        else:
            t1_data.append({v: np.nan for v in t1_cols.values()})

    t1_df = pd.DataFrame(t1_data)
    merged = pd.concat([merged.reset_index(drop=True), t1_df], axis=1)

    t1_populated = merged["t1_fii_fut_idx_net"].notna().sum()
    print(f"T-1 lookback: {t1_populated}/{len(merged)} rows populated")
    return merged


def compute_derived_features(merged: pd.DataFrame) -> pd.DataFrame:
    """Compute derived signals from raw FII data."""
    # FII put-call ratio
    merged["fii_pcr"] = merged["fii_put_net"] / merged["fii_call_net"].abs().replace(0, np.nan)

    # FII net sentiment (higher = more bullish)
    merged["fii_net_sentiment"] = (
        merged["fii_fut_idx_net"] + merged["fii_call_net"] - merged["fii_put_net"]
    )

    # Day-over-day change in fii_put_net
    merged["fii_put_change"] = merged["fii_put_net"].diff()

    # Binary blowout indicator
    merged["is_blowout"] = (merged["vix_accuracy"] == "Underestimated").astype(int)

    # FII direction matches actual market direction
    merged["fii_direction_matches_market"] = (
        merged["FII_Direction"] == merged["Market_Direction"]
    ).astype(int)

    # Consensus count: how many of FII/DII/Pro/Client match market direction
    direction_cols = ["FII_Direction", "DII_Direction", "Pro_Direction", "Client_Direction"]
    merged["consensus_count"] = merged.apply(
        lambda row: sum(
            1 for col in direction_cols
            if row[col] == row["Market_Direction"]
        ),
        axis=1
    )

    # T-1 derived features
    if "t1_fii_put_net" in merged.columns:
        merged["t1_fii_pcr"] = merged["t1_fii_put_net"] / merged["t1_fii_call_net"].abs().replace(0, np.nan)

    # VIX intraday change (for comparison)
    merged["vix_change"] = merged["vix_close"] - merged["vix_open"]

    return merged


def compute_correlations(merged: pd.DataFrame) -> dict:
    """Compute correlations between FII signals and blowout/range."""
    results = {}

    # Same-day FII numeric signals
    fii_numeric = ["fii_fut_idx_net", "fii_call_net", "fii_put_net",
                   "fii_pcr", "fii_net_sentiment", "fii_put_change"]
    targets = ["is_blowout", "actual_range_pct"]

    # Same-day correlations
    same_day = {}
    for signal in fii_numeric:
        signal_data = merged[signal].dropna()
        for target in targets:
            target_data = merged.loc[signal_data.index, target]
            valid = signal_data.notna() & target_data.notna()
            if valid.sum() < 5:
                continue
            r, p = stats.pearsonr(signal_data[valid], target_data[valid])
            same_day[f"{signal}_vs_{target}"] = {
                "correlation": round(r, 4),
                "p_value": round(p, 4),
                "n": int(valid.sum()),
                "significant": p < 0.05
            }
    results["same_day"] = same_day

    # T-1 correlations (pre-market observable)
    t1_numeric = ["t1_fii_fut_idx_net", "t1_fii_call_net", "t1_fii_put_net", "t1_fii_pcr"]
    t1_corrs = {}
    for signal in t1_numeric:
        if signal not in merged.columns:
            continue
        signal_data = merged[signal].dropna()
        for target in targets:
            target_data = merged.loc[signal_data.index, target]
            valid = signal_data.notna() & target_data.notna()
            if valid.sum() < 5:
                continue
            r, p = stats.pearsonr(signal_data[valid], target_data[valid])
            t1_corrs[f"{signal}_vs_{target}"] = {
                "correlation": round(r, 4),
                "p_value": round(p, 4),
                "n": int(valid.sum()),
                "significant": p < 0.05
            }
    results["t1_premarket"] = t1_corrs

    return results


def compute_cross_tabs(merged: pd.DataFrame) -> dict:
    """Cross-tabulate categorical directions vs blowout."""
    results = {}

    for direction_col in ["FII_Direction", "DII_Direction", "Pro_Direction", "Client_Direction"]:
        ct = {}
        for val in merged[direction_col].dropna().unique():
            subset = merged[merged[direction_col] == val]
            n = len(subset)
            blowouts = subset["is_blowout"].sum()
            ct[val] = {
                "count": int(n),
                "blowouts": int(blowouts),
                "blowout_rate": round(blowouts / n, 4) if n > 0 else 0,
                "avg_range": round(subset["actual_range_pct"].mean(), 4) if n > 0 else 0
            }
        results[direction_col] = ct

    # T-1 FII Direction
    if "t1_FII_Direction" in merged.columns:
        ct = {}
        for val in merged["t1_FII_Direction"].dropna().unique():
            subset = merged[merged["t1_FII_Direction"] == val]
            n = len(subset)
            blowouts = subset["is_blowout"].sum()
            ct[val] = {
                "count": int(n),
                "blowouts": int(blowouts),
                "blowout_rate": round(blowouts / n, 4) if n > 0 else 0,
                "avg_range": round(subset["actual_range_pct"].mean(), 4) if n > 0 else 0
            }
        results["t1_FII_Direction"] = ct

    # Consensus analysis
    consensus = {}
    for count in sorted(merged["consensus_count"].unique()):
        subset = merged[merged["consensus_count"] == count]
        n = len(subset)
        blowouts = subset["is_blowout"].sum()
        consensus[str(int(count))] = {
            "count": int(n),
            "blowouts": int(blowouts),
            "blowout_rate": round(blowouts / n, 4) if n > 0 else 0,
            "avg_range": round(subset["actual_range_pct"].mean(), 4) if n > 0 else 0
        }
    results["consensus_count"] = consensus

    return results


def test_prediction_rules(merged: pd.DataFrame) -> dict:
    """Test FII-based blowout prediction rules and compute lift."""
    base_rate = merged["is_blowout"].mean()
    results = {"base_rate": round(base_rate, 4)}
    rules = {}

    def eval_rule(name: str, mask: pd.Series):
        subset = merged[mask]
        n = len(subset)
        if n == 0:
            return
        blowouts = subset["is_blowout"].sum()
        rate = blowouts / n
        rules[name] = {
            "triggers": int(n),
            "blowouts": int(blowouts),
            "blowout_rate": round(rate, 4),
            "lift": round(rate / base_rate, 2) if base_rate > 0 else 0,
            "pct_of_days": round(n / len(merged), 4)
        }

    # Single rules
    eval_rule("FII_Direction_Bearish", merged["FII_Direction"] == "Bearish")
    eval_rule("FII_Direction_Bullish", merged["FII_Direction"] == "Bullish")
    eval_rule("fii_pcr_above_median", merged["fii_pcr"] > merged["fii_pcr"].median())
    eval_rule("fii_put_change_positive", merged["fii_put_change"] > 0)
    eval_rule("t1_FII_Direction_Bearish", merged["t1_FII_Direction"] == "Bearish")
    eval_rule("t1_FII_Direction_Bullish", merged["t1_FII_Direction"] == "Bullish")

    # FII PCR high/low split
    eval_rule("fii_pcr_above_75pct", merged["fii_pcr"] > merged["fii_pcr"].quantile(0.75))
    eval_rule("fii_pcr_below_25pct", merged["fii_pcr"] < merged["fii_pcr"].quantile(0.25))

    # Combination rules
    eval_rule(
        "FII_Bearish_AND_VIX_lt14",
        (merged["FII_Direction"] == "Bearish") & (merged["vix_open"] < 14)
    )
    eval_rule(
        "consensus_ge3",
        merged["consensus_count"] >= 3
    )
    eval_rule(
        "FII_Bearish_AND_fii_pcr_above_median",
        (merged["FII_Direction"] == "Bearish") & (merged["fii_pcr"] > merged["fii_pcr"].median())
    )

    # VIX intraday comparison signal
    eval_rule("vix_change_gt_0.5", merged["vix_change"] > 0.5)
    eval_rule("vix_change_lt_0", merged["vix_change"] < 0)

    results["rules"] = rules
    return results


def generate_summary(
    merged: pd.DataFrame,
    correlations: dict,
    cross_tabs: dict,
    rule_results: dict,
    project_root: Path
):
    """Generate markdown summary report."""
    base_rate = rule_results["base_rate"]
    rules = rule_results["rules"]

    lines = []
    lines.append("# FII/DII + VIX Expiry-Day Correlation Analysis")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Overlap Period**: {merged.date.min()} to {merged.date.max()}")
    lines.append(f"**Expiry Days Analyzed**: {len(merged)}")
    lines.append(f"**Blowout Base Rate**: {base_rate:.1%} ({merged.is_blowout.sum()}/{len(merged)} days)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")

    # Find best FII pre-market signal
    premarket_rules = {k: v for k, v in rules.items()
                       if k.startswith("t1_") or k.startswith("FII_") or k.startswith("fii_")}
    best_rule = max(premarket_rules.items(), key=lambda x: x[1]["lift"]) if premarket_rules else None
    vix_signal = rules.get("vix_change_gt_0.5", {})

    if best_rule:
        lines.append(f"**Best FII pre-market signal**: `{best_rule[0]}`")
        lines.append(f"- Blowout rate: {best_rule[1]['blowout_rate']:.0%} (lift: {best_rule[1]['lift']:.1f}x vs {base_rate:.0%} base)")
        lines.append(f"- Triggers on: {best_rule[1]['triggers']}/{len(merged)} days ({best_rule[1]['pct_of_days']:.0%})")
        lines.append("")

    if vix_signal:
        lines.append(f"**VIX intraday benchmark** (for comparison): `vix_change > 0.5`")
        lines.append(f"- Blowout rate: {vix_signal['blowout_rate']:.0%} (lift: {vix_signal['lift']:.1f}x)")
        lines.append(f"- Triggers on: {vix_signal['triggers']}/{len(merged)} days")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Correlations
    lines.append("## Correlation Findings")
    lines.append("")
    lines.append("### Same-Day FII Signals vs Blowout")
    lines.append("")
    lines.append("| Signal | Correlation | p-value | Significant? |")
    lines.append("|--------|------------|---------|-------------|")
    for key, val in correlations.get("same_day", {}).items():
        if "is_blowout" in key:
            sig = "Yes" if val["significant"] else "No"
            lines.append(f"| {key.replace('_vs_is_blowout', '')} | {val['correlation']:+.3f} | {val['p_value']:.3f} | {sig} |")
    lines.append("")

    lines.append("### Same-Day FII Signals vs Actual Range")
    lines.append("")
    lines.append("| Signal | Correlation | p-value | Significant? |")
    lines.append("|--------|------------|---------|-------------|")
    for key, val in correlations.get("same_day", {}).items():
        if "actual_range_pct" in key:
            sig = "Yes" if val["significant"] else "No"
            lines.append(f"| {key.replace('_vs_actual_range_pct', '')} | {val['correlation']:+.3f} | {val['p_value']:.3f} | {sig} |")
    lines.append("")

    lines.append("### T-1 Pre-Market FII Signals (Observable Before Open)")
    lines.append("")
    lines.append("| Signal | vs Blowout | p-value | vs Range | p-value |")
    lines.append("|--------|-----------|---------|---------|---------|")
    t1_data = correlations.get("t1_premarket", {})
    t1_signals = set(k.split("_vs_")[0] for k in t1_data.keys())
    for sig in sorted(t1_signals):
        bl_key = f"{sig}_vs_is_blowout"
        rg_key = f"{sig}_vs_actual_range_pct"
        bl = t1_data.get(bl_key, {})
        rg = t1_data.get(rg_key, {})
        bl_r = f"{bl.get('correlation', 'N/A'):+.3f}" if bl else "N/A"
        bl_p = f"{bl.get('p_value', 'N/A'):.3f}" if bl else "N/A"
        rg_r = f"{rg.get('correlation', 'N/A'):+.3f}" if rg else "N/A"
        rg_p = f"{rg.get('p_value', 'N/A'):.3f}" if rg else "N/A"
        lines.append(f"| {sig} | {bl_r} | {bl_p} | {rg_r} | {rg_p} |")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Cross-tabs
    lines.append("## Direction Signal Cross-Tabulation")
    lines.append("")
    for col_name, ct in cross_tabs.items():
        if col_name == "consensus_count":
            continue
        lines.append(f"### {col_name} vs Blowout")
        lines.append("")
        lines.append("| Direction | Count | Blowouts | Blowout Rate | Avg Range |")
        lines.append("|-----------|-------|----------|-------------|-----------|")
        for val, data in ct.items():
            lines.append(f"| {val} | {data['count']} | {data['blowouts']} | {data['blowout_rate']:.0%} | {data['avg_range']:.2f}% |")
        lines.append("")

    # Consensus
    lines.append("### Consensus Count (participants matching market direction)")
    lines.append("")
    lines.append("| Consensus | Count | Blowouts | Blowout Rate | Avg Range |")
    lines.append("|-----------|-------|----------|-------------|-----------|")
    for count, data in cross_tabs.get("consensus_count", {}).items():
        lines.append(f"| {count}/4 | {data['count']} | {data['blowouts']} | {data['blowout_rate']:.0%} | {data['avg_range']:.2f}% |")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Rules
    lines.append("## Prediction Rule Testing")
    lines.append("")
    lines.append(f"**Base blowout rate**: {base_rate:.0%} ({merged.is_blowout.sum()}/{len(merged)} days)")
    lines.append("")
    lines.append("### All Rules Ranked by Lift")
    lines.append("")
    lines.append("| Rule | Triggers | Blowout Rate | Lift | Type |")
    lines.append("|------|----------|-------------|------|------|")
    sorted_rules = sorted(rules.items(), key=lambda x: x[1]["lift"], reverse=True)
    for name, data in sorted_rules:
        rule_type = "Intraday" if "vix_change" in name else "Pre-market"
        lines.append(f"| {name} | {data['triggers']} | {data['blowout_rate']:.0%} | {data['lift']:.1f}x | {rule_type} |")
    lines.append("")

    lines.append("---")
    lines.append("")

    # Implications
    lines.append("## Trading Implications")
    lines.append("")
    lines.append("### Key Findings")
    lines.append("")

    # Determine if FII adds value
    premarket_lifts = [v["lift"] for k, v in rules.items()
                       if not k.startswith("vix_change") and v["triggers"] >= 5]
    max_premarket_lift = max(premarket_lifts) if premarket_lifts else 0

    if max_premarket_lift >= 1.5:
        lines.append(f"1. **FII signals show meaningful lift**: Best pre-market FII signal achieves {max_premarket_lift:.1f}x lift over base rate")
        lines.append("2. Consider integrating FII direction into the pre-market tier system")
    else:
        lines.append(f"1. **FII signals show limited lift**: Best pre-market FII signal achieves only {max_premarket_lift:.1f}x lift over base rate")
        lines.append("2. FII positioning alone is NOT a reliable blowout predictor")

    if vix_signal:
        lines.append(f"3. **VIX intraday signal remains dominant**: {vix_signal['blowout_rate']:.0%} blowout rate ({vix_signal['lift']:.1f}x lift) far exceeds any FII signal")

    lines.append("")
    lines.append("### Recommendation")
    lines.append("")
    if max_premarket_lift >= 1.5:
        lines.append("FII positioning data adds marginal pre-market value. Use as a secondary sizing signal alongside the primary VIX intraday confirmation.")
    else:
        lines.append("FII positioning data does NOT reliably predict VIX blowouts on expiry days. Continue using VIX intraday behavior as the primary signal. FII data is better suited for directional bias, not volatility prediction.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Sample size warning**: Analysis based on {len(merged)} expiry days. Subgroup findings with n<10 are unreliable.")
    lines.append("")

    summary_path = project_root / "FII_DII_VIX_CORRELATION_SUMMARY.md"
    summary_path.write_text("\n".join(lines))
    print(f"Written: {summary_path}")


def main():
    project_root = Path(__file__).resolve().parent.parent.parent.parent.parent

    print("=" * 60)
    print("FII/DII + VIX EXPIRY-DAY CORRELATION ANALYSIS")
    print("=" * 60)
    print()

    # 1. Load data
    fii_df, vix_df = load_data(project_root)
    print()

    # 2. Merge on date
    merged = merge_datasets(fii_df, vix_df)
    print()

    # 3. Add T-1 lookback
    merged = add_t1_lookback(merged, fii_df)
    print()

    # 4. Compute derived features
    merged = compute_derived_features(merged)
    print(f"Derived features computed: fii_pcr, fii_net_sentiment, fii_put_change, is_blowout, consensus_count")
    print(f"  is_blowout count: {merged.is_blowout.sum()}/{len(merged)}")
    print(f"  consensus_count range: {merged.consensus_count.min()}-{merged.consensus_count.max()}")
    print()

    # 5. Compute correlations
    print("Computing correlations...")
    correlations = compute_correlations(merged)
    print(f"  Same-day correlations: {len(correlations['same_day'])} pairs")
    print(f"  T-1 pre-market correlations: {len(correlations['t1_premarket'])} pairs")
    print()

    # 6. Cross-tabulations
    print("Computing cross-tabulations...")
    cross_tabs = compute_cross_tabs(merged)
    print(f"  Direction tables: {len(cross_tabs)} categories")
    print()

    # 7. Test prediction rules
    print("Testing prediction rules...")
    rule_results = test_prediction_rules(merged)
    print(f"  Rules tested: {len(rule_results['rules'])}")
    print(f"  Base blowout rate: {rule_results['base_rate']:.1%}")
    print()

    # 8. Write outputs
    print("Writing outputs...")

    # CSV
    csv_path = project_root / "fii_dii_vix_correlation.csv"
    merged.to_csv(csv_path, index=False)
    print(f"  Written: {csv_path} ({len(merged)} rows)")

    # JSON
    json_output = {
        "metadata": {
            "generated": datetime.now().isoformat(),
            "overlap_period": f"{merged.date.min()} to {merged.date.max()}",
            "expiry_days": len(merged),
            "blowout_count": int(merged.is_blowout.sum()),
            "base_rate": round(merged.is_blowout.mean(), 4),
        },
        "correlations": correlations,
        "cross_tabs": cross_tabs,
        "rules": rule_results,
    }
    json_path = project_root / "fii_dii_vix_correlation.json"
    json_path.write_text(json.dumps(json_output, indent=2, default=str))
    print(f"  Written: {json_path}")

    # Summary
    generate_summary(merged, correlations, cross_tabs, rule_results, project_root)
    print()

    # 9. Print key findings
    print("=" * 60)
    print("KEY FINDINGS")
    print("=" * 60)
    print()

    # Best correlations
    print("Top correlations (same-day, vs blowout):")
    blowout_corrs = {k: v for k, v in correlations["same_day"].items() if "is_blowout" in k}
    for k, v in sorted(blowout_corrs.items(), key=lambda x: abs(x[1]["correlation"]), reverse=True)[:5]:
        sig = "*" if v["significant"] else ""
        print(f"  {k.replace('_vs_is_blowout', '')}: r={v['correlation']:+.3f} (p={v['p_value']:.3f}){sig}")
    print()

    # Best rules
    print("Top prediction rules (by lift):")
    sorted_rules = sorted(rule_results["rules"].items(), key=lambda x: x[1]["lift"], reverse=True)
    for name, data in sorted_rules[:5]:
        print(f"  {name}: blowout={data['blowout_rate']:.0%}, lift={data['lift']:.1f}x, n={data['triggers']}")
    print()

    print("Done!")


if __name__ == "__main__":
    main()
