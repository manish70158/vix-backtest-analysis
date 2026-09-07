import pandas as pd
import numpy as np
from datetime import datetime

# Load the two CSV files
timing_df = pd.read_csv('/Users/manishkumar/Documents/learning/18-July-2026-Vix-Analysis-On-Expiry/fii-pro-alignment-analysis/vix_threshold_timing_results.csv')
fii_pro_df = pd.read_csv('/Users/manishkumar/Documents/learning/18-July-2026-Vix-Analysis-On-Expiry/fii-pro-alignment-analysis/fii_pro_alignment_results.csv')

# Join on date
merged_df = timing_df.merge(fii_pro_df[['date', 'fii_view', 'pro_view', 'fii_bucket', 'pro_bucket']], on='date', how='left')

# Create FII-PRO combination column
merged_df['fii_pro_combo'] = merged_df['fii_view'] + ' + ' + merged_df['pro_view']

# Clean up session names - remove time ranges in parentheses
merged_df['session'] = merged_df['cross_session'].str.replace(r'\s*\(.*\)', '', regex=True)

# Define success criteria
def is_success(outcome):
    return outcome in ['Worked', 'Remained']

merged_df['success'] = merged_df['close_outcome'].apply(is_success)

print("=" * 100)
print("BEARISH LATE-MORNING (10:30-11:29) DANGER ZONE ANALYSIS")
print("=" * 100)
print()

# ============================================================================
# PART 1: Deep Dive into the Bearish Late-Morning Crosses
# ============================================================================

print("=" * 100)
print("PART 1: DEEP DIVE INTO BEARISH LATE-MORNING (10:30-11:29) CROSSES")
print("=" * 100)
print()

# Filter for bearish alignment, exceeded half threshold, and late morning session
bearish_late_morning = merged_df[
    (merged_df['alignment'] == 'Bearish Alignment') & 
    (merged_df['vix_exhaustion'] == 'Exceeded Half then Reversed') &
    (merged_df['session'] == 'Late Morning')
].copy()

print(f"Total Bearish Late-Morning Crosses: {len(bearish_late_morning)}")
print()

if len(bearish_late_morning) > 0:
    print("-" * 100)
    print("ALL BEARISH LATE-MORNING CROSSES WITH DETAILS:")
    print("-" * 100)
    
    # Sort by date
    bearish_late_morning_sorted = bearish_late_morning.sort_values('date')
    
    for idx, row in bearish_late_morning_sorted.iterrows():
        print(f"\nDate: {row['date']}")
        print(f"  FII View: {row['fii_view']:>15} | PRO View: {row['pro_view']:>15} | Combo: {row['fii_pro_combo']}")
        print(f"  VIX Regime: {row['vix_regime']:>10} | VIX Open: {row['vix_open']:.2f}")
        print(f"  Cross Time: {row['cross_time']:>10} | Session: {row['session']}")
        print(f"  Expiry: {'YES' if row['is_nifty_expiry'] else 'NO':>3}")
        print(f"  Outcome: {row['close_outcome']:>10} | Actual Close %: {row['actual_open_close_pct']:>6.2f}%")
        print(f"  Move at Cross: {row['move_pct_at_cross']:>6.2f}% | Intraday Low: {row['intraday_low_pct']:>6.2f}%")
    
    print()
    print("-" * 100)
    print("FII-PRO COMBINATION BREAKDOWN:")
    print("-" * 100)
    
    combo_stats = bearish_late_morning.groupby('fii_pro_combo').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    combo_stats.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    combo_stats['Win_Rate'] = (combo_stats['Win_Rate'] * 100).round(1)
    combo_stats = combo_stats.sort_values('Total', ascending=False)
    
    print(f"\n{'FII-PRO Combination':<40} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    for combo, row in combo_stats.iterrows():
        print(f"{combo:<40} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    print()
    print("-" * 100)
    print("VIX REGIME BREAKDOWN:")
    print("-" * 100)
    
    regime_stats = bearish_late_morning.groupby('vix_regime').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    regime_stats.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    regime_stats['Win_Rate'] = (regime_stats['Win_Rate'] * 100).round(1)
    regime_stats = regime_stats.sort_values('Total', ascending=False)
    
    print(f"\n{'VIX Regime':<20} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    for regime, row in regime_stats.iterrows():
        print(f"{regime:<20} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    print()
    print("-" * 100)
    print("EXPIRY vs NON-EXPIRY BREAKDOWN:")
    print("-" * 100)
    
    expiry_stats = bearish_late_morning.groupby('is_nifty_expiry').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    expiry_stats.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    expiry_stats['Win_Rate'] = (expiry_stats['Win_Rate'] * 100).round(1)
    
    print(f"\n{'Type':<15} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    for is_expiry, row in expiry_stats.iterrows():
        expiry_label = 'Expiry' if is_expiry else 'Non-Expiry'
        print(f"{expiry_label:<15} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")

print()
print()

# ============================================================================
# PART 2: Compare ALL Sessions for Bearish Exceeded Half
# ============================================================================

print("=" * 100)
print("PART 2: ALL SESSIONS COMPARISON - BEARISH EXCEEDED HALF THRESHOLD")
print("=" * 100)
print()

# Filter for bearish alignment and exceeded half threshold
bearish_exceeded = merged_df[
    (merged_df['alignment'] == 'Bearish Alignment') & 
    (merged_df['vix_exhaustion'] == 'Exceeded Half then Reversed')
].copy()

print(f"Total Bearish Exceeded Half Threshold Cases: {len(bearish_exceeded)}")
print()

# Define session order
session_order = ['Opening', 'Early Morning', 'Late Morning', 'Midday', 'Early Afternoon', 'Late Afternoon', 'Closing']

for session in session_order:
    session_data = bearish_exceeded[bearish_exceeded['session'] == session]
    
    if len(session_data) == 0:
        continue
    
    print("=" * 100)
    print(f"SESSION: {session.upper()}")
    print("=" * 100)
    
    total = len(session_data)
    wins = session_data['success'].sum()
    win_rate = (wins / total * 100) if total > 0 else 0
    avg_close = session_data['actual_open_close_pct'].mean()
    
    print(f"\nOverall: N={total}, Wins={wins}, Win Rate={win_rate:.1f}%, Avg Close%={avg_close:.2f}%")
    
    # FII-PRO Combination Breakdown
    print(f"\n{'FII-PRO Combination':<40} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    
    combo_breakdown = session_data.groupby('fii_pro_combo').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    combo_breakdown.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    combo_breakdown['Win_Rate'] = (combo_breakdown['Win_Rate'] * 100).round(1)
    combo_breakdown = combo_breakdown.sort_values('Total', ascending=False)
    
    for combo, row in combo_breakdown.iterrows():
        print(f"{combo:<40} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    # VIX Regime Breakdown
    print(f"\n{'VIX Regime':<20} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    
    regime_breakdown = session_data.groupby('vix_regime').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    regime_breakdown.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    regime_breakdown['Win_Rate'] = (regime_breakdown['Win_Rate'] * 100).round(1)
    regime_breakdown = regime_breakdown.sort_values('Total', ascending=False)
    
    for regime, row in regime_breakdown.iterrows():
        print(f"{regime:<20} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    # Expiry Effect
    print(f"\n{'Type':<15} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    
    expiry_breakdown = session_data.groupby('is_nifty_expiry').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    expiry_breakdown.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    expiry_breakdown['Win_Rate'] = (expiry_breakdown['Win_Rate'] * 100).round(1)
    
    for is_expiry, row in expiry_breakdown.iterrows():
        expiry_label = 'Expiry' if is_expiry else 'Non-Expiry'
        print(f"{expiry_label:<15} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    print()

print()

# ============================================================================
# PART 3: FII-PRO Combinations with HIGHEST Probability Across ALL Sessions
# ============================================================================

print("=" * 100)
print("PART 3: FII-PRO COMBINATION PROBABILITY MATRIX - BEARISH EXCEEDED HALF")
print("=" * 100)
print()

if len(bearish_exceeded) > 0:
    # Create pivot table: Session x FII-PRO Combination → Win Rate
    print("-" * 150)
    print("WIN RATE MATRIX (%) BY SESSION AND FII-PRO COMBINATION:")
    print("-" * 150)
    
    # Get all unique combinations
    all_combos = sorted(bearish_exceeded['fii_pro_combo'].unique())
    
    # Create matrix
    matrix_data = []
    for session in session_order:
        session_data = bearish_exceeded[bearish_exceeded['session'] == session]
        if len(session_data) == 0:
            continue
        
        row = {'Session': session}
        for combo in all_combos:
            combo_data = session_data[session_data['fii_pro_combo'] == combo]
            if len(combo_data) > 0:
                wr = combo_data['success'].mean() * 100
                n = len(combo_data)
                row[combo] = f"{wr:.1f}% ({n})"
            else:
                row[combo] = "-"
        matrix_data.append(row)
    
    if len(matrix_data) > 0:
        matrix_df = pd.DataFrame(matrix_data)
        # Print in a more readable format
        for _, row in matrix_df.iterrows():
            print(f"\n{row['Session']}:")
            for col in matrix_df.columns:
                if col != 'Session' and row[col] != '-':
                    print(f"  {col:<40} {row[col]:>12}")
    
    print()
    print("-" * 150)
    print("OVERALL WIN RATE BY FII-PRO COMBINATION (ALL BEARISH EXCEEDED HALF SESSIONS):")
    print("-" * 150)
    
    overall_combo_stats = bearish_exceeded.groupby('fii_pro_combo').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    overall_combo_stats.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    overall_combo_stats['Win_Rate_Pct'] = (overall_combo_stats['Win_Rate'] * 100).round(1)
    overall_combo_stats = overall_combo_stats.sort_values('Win_Rate_Pct', ascending=False)
    
    print(f"\n{'FII-PRO Combination':<40} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 150)
    for combo, row in overall_combo_stats.iterrows():
        print(f"{combo:<40} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate_Pct']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    print()
    print("-" * 150)
    print("SAFEST COMBINATIONS (Highest Win Rate, Min 5 occurrences):")
    print("-" * 150)
    
    safest = overall_combo_stats[overall_combo_stats['Total'] >= 5].sort_values('Win_Rate_Pct', ascending=False).head(5)
    if len(safest) > 0:
        print(f"\n{'Rank':<5} {'FII-PRO Combination':<40} {'N':>5} {'WR%':>6}")
        print("-" * 150)
        for i, (combo, row) in enumerate(safest.iterrows(), 1):
            print(f"{i:<5} {combo:<40} {int(row['Total']):>5} {row['Win_Rate_Pct']:>6.1f}")
    else:
        print("\nNot enough data (min 5 occurrences required)")
    
    print()
    print("-" * 150)
    print("MOST DANGEROUS COMBINATIONS IN LATE MORNING (Min 3 occurrences):")
    print("-" * 150)
    
    if len(bearish_late_morning) > 0:
        late_morning_combos = bearish_late_morning.groupby('fii_pro_combo').agg({
            'success': ['count', 'mean']
        }).round(4)
        late_morning_combos.columns = ['Total', 'Win_Rate']
        late_morning_combos['Win_Rate_Pct'] = (late_morning_combos['Win_Rate'] * 100).round(1)
        late_morning_combos = late_morning_combos[late_morning_combos['Total'] >= 3].sort_values('Win_Rate_Pct')
        
        if len(late_morning_combos) > 0:
            print(f"\n{'Rank':<5} {'FII-PRO Combination':<40} {'N':>5} {'WR%':>6}")
            print("-" * 150)
            for i, (combo, row) in enumerate(late_morning_combos.iterrows(), 1):
                print(f"{i:<5} {combo:<40} {int(row['Total']):>5} {row['Win_Rate_Pct']:>6.1f}")
        else:
            print("\nNot enough data (min 3 occurrences required)")
    else:
        print("\nNo late morning data available")
    
    print()
    print("-" * 150)
    print("EXPECTED VALUE ANALYSIS (Probability × Win Rate):")
    print("-" * 150)
    print("\nNote: Expected Value = (Frequency % of Exceeded Half) × Win Rate%")
    print()
    
    # Calculate frequency of each combo in bearish exceeded half
    total_bearish_exceeded = len(bearish_exceeded)
    combo_freq = bearish_exceeded['fii_pro_combo'].value_counts() / total_bearish_exceeded * 100
    
    # Calculate expected value
    ev_data = []
    for combo in overall_combo_stats.index:
        freq_pct = combo_freq.get(combo, 0)
        wr_pct = overall_combo_stats.loc[combo, 'Win_Rate_Pct']
        ev = freq_pct * wr_pct / 100
        n = int(overall_combo_stats.loc[combo, 'Total'])
        ev_data.append({
            'Combo': combo,
            'N': n,
            'Freq%': freq_pct,
            'WR%': wr_pct,
            'EV': ev
        })
    
    if len(ev_data) > 0:
        ev_df = pd.DataFrame(ev_data).sort_values('EV', ascending=False)
        
        print(f"{'FII-PRO Combination':<40} {'N':>5} {'Freq%':>7} {'WR%':>6} {'EV':>8}")
        print("-" * 150)
        for _, row in ev_df.iterrows():
            print(f"{row['Combo']:<40} {row['N']:>5} {row['Freq%']:>6.1f}% {row['WR%']:>6.1f} {row['EV']:>8.2f}")

print()
print()

# ============================================================================
# PART 4: Bullish Comparison
# ============================================================================

print("=" * 100)
print("PART 4: BULLISH COMPARISON - ALL SESSIONS WITH EXCEEDED HALF THRESHOLD")
print("=" * 100)
print()

# Filter for bullish alignment and exceeded half threshold
bullish_exceeded = merged_df[
    (merged_df['alignment'] == 'Bullish Alignment') & 
    (merged_df['vix_exhaustion'] == 'Exceeded Half then Reversed')
].copy()

print(f"Total Bullish Exceeded Half Threshold Cases: {len(bullish_exceeded)}")
print()

for session in session_order:
    session_data = bullish_exceeded[bullish_exceeded['session'] == session]
    
    if len(session_data) == 0:
        continue
    
    print("=" * 100)
    print(f"SESSION: {session.upper()}")
    print("=" * 100)
    
    total = len(session_data)
    wins = session_data['success'].sum()
    win_rate = (wins / total * 100) if total > 0 else 0
    avg_close = session_data['actual_open_close_pct'].mean()
    
    print(f"\nOverall: N={total}, Wins={wins}, Win Rate={win_rate:.1f}%, Avg Close%={avg_close:.2f}%")
    
    # FII-PRO Combination Breakdown
    print(f"\n{'FII-PRO Combination':<40} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    
    combo_breakdown = session_data.groupby('fii_pro_combo').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    combo_breakdown.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    combo_breakdown['Win_Rate'] = (combo_breakdown['Win_Rate'] * 100).round(1)
    combo_breakdown = combo_breakdown.sort_values('Total', ascending=False)
    
    for combo, row in combo_breakdown.iterrows():
        print(f"{combo:<40} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    # VIX Regime Breakdown
    print(f"\n{'VIX Regime':<20} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    
    regime_breakdown = session_data.groupby('vix_regime').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    regime_breakdown.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    regime_breakdown['Win_Rate'] = (regime_breakdown['Win_Rate'] * 100).round(1)
    regime_breakdown = regime_breakdown.sort_values('Total', ascending=False)
    
    for regime, row in regime_breakdown.iterrows():
        print(f"{regime:<20} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    # Expiry Effect
    print(f"\n{'Type':<15} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 100)
    
    expiry_breakdown = session_data.groupby('is_nifty_expiry').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    expiry_breakdown.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    expiry_breakdown['Win_Rate'] = (expiry_breakdown['Win_Rate'] * 100).round(1)
    
    for is_expiry, row in expiry_breakdown.iterrows():
        expiry_label = 'Expiry' if is_expiry else 'Non-Expiry'
        print(f"{expiry_label:<15} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
    
    print()

print()
print("-" * 150)
print("OVERALL WIN RATE BY FII-PRO COMBINATION (ALL BULLISH EXCEEDED HALF SESSIONS):")
print("-" * 150)

if len(bullish_exceeded) > 0:
    overall_bullish_combo_stats = bullish_exceeded.groupby('fii_pro_combo').agg({
        'success': ['count', 'sum', 'mean'],
        'actual_open_close_pct': 'mean'
    }).round(4)
    
    overall_bullish_combo_stats.columns = ['Total', 'Wins', 'Win_Rate', 'Avg_Close_Pct']
    overall_bullish_combo_stats['Win_Rate_Pct'] = (overall_bullish_combo_stats['Win_Rate'] * 100).round(1)
    overall_bullish_combo_stats = overall_bullish_combo_stats.sort_values('Win_Rate_Pct', ascending=False)
    
    print(f"\n{'FII-PRO Combination':<40} {'N':>5} {'Wins':>5} {'WR%':>6} {'Avg Close%':>10}")
    print("-" * 150)
    for combo, row in overall_bullish_combo_stats.iterrows():
        print(f"{combo:<40} {int(row['Total']):>5} {int(row['Wins']):>5} {row['Win_Rate_Pct']:>6.1f} {row['Avg_Close_Pct']:>10.2f}")
else:
    print("\nNo bullish exceeded half data available")

print()
print("=" * 100)
print("ANALYSIS COMPLETE")
print("=" * 100)
