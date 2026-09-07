import pandas as pd
import sys
from collections import defaultdict

# Read the CSV
csv_path = '/Users/manishkumar/Documents/learning/18-July-2026-Vix-Analysis-On-Expiry/fii-pro-alignment-analysis/fii_pro_alignment_results.csv'
df = pd.read_csv(csv_path)

print("="*100)
print("COMPREHENSIVE FII VIEW x PRO VIEW ANALYSIS - 6 YEAR DATASET")
print("="*100)
print(f"\nTotal rows in dataset: {len(df)}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# Helper function to clean percentage strings
def clean_pct(val):
    if pd.isna(val):
        return None
    if isinstance(val, str):
        return float(val.replace('%', '').replace('+', '').strip())
    return float(val)

# Clean percentage columns
pct_columns = ['change_pct', 'up_from_open', 'down_from_open', 'actual_range_pct', 
               'intraday_high_pct', 'intraday_low_pct']
for col in pct_columns:
    if col in df.columns:
        df[col + '_clean'] = df[col].apply(clean_pct)

print("\n" + "="*100)
print("STEP 1: ALL UNIQUE FII_VIEW VALUES AND COUNTS")
print("="*100)
fii_view_counts = df['fii_view'].value_counts().sort_index()
for view, count in fii_view_counts.items():
    print(f"{view:25s}: {count:4d} days ({count/len(df)*100:5.2f}%)")

print("\n" + "="*100)
print("STEP 2: DETAILED ANALYSIS BY FII VIEW AND PRO VIEW")
print("="*100)

# Store all combinations for summary table
all_combinations = []

# Get all unique FII views in a sensible order
fii_order = ['Strong Bullish', 'Bullish', 'Mildly Bullish', 'Neutral', 
             'Mildly Bearish', 'Bearish', 'Strong Bearish']
existing_fii_views = [v for v in fii_order if v in df['fii_view'].unique()]
# Add any views not in our predefined order
for v in sorted(df['fii_view'].unique()):
    if v not in existing_fii_views:
        existing_fii_views.append(v)

for fii_view in existing_fii_views:
    fii_df = df[df['fii_view'] == fii_view]
    
    print(f"\n{'='*100}")
    print(f"FII VIEW: {fii_view} ({len(fii_df)} days)")
    print(f"{'='*100}")
    
    # Get all PRO views for this FII view
    pro_views = sorted(fii_df['pro_view'].unique())
    
    for pro_view in pro_views:
        combo_df = fii_df[fii_df['pro_view'] == pro_view]
        
        print(f"\n  PRO VIEW: {pro_view}")
        print(f"  {'-'*90}")
        
        # 1. Total count
        total_days = len(combo_df)
        print(f"  Total Days: {total_days}")
        
        # 2. Green vs Red
        green_count = len(combo_df[combo_df['result'] == 'Green'])
        red_count = len(combo_df[combo_df['result'] == 'Red'])
        green_pct = (green_count / total_days * 100) if total_days > 0 else 0
        red_pct = (red_count / total_days * 100) if total_days > 0 else 0
        print(f"  Green: {green_count:3d} ({green_pct:5.2f}%)  |  Red: {red_count:3d} ({red_pct:5.2f}%)")
        
        # 3. Average change_pct
        avg_change = combo_df['change_pct_clean'].mean()
        print(f"  Average Change%: {avg_change:+.3f}%")
        
        # 4. Average up_from_open and down_from_open
        avg_up = combo_df['up_from_open_clean'].mean()
        avg_down = combo_df['down_from_open_clean'].mean()
        print(f"  Average Up from Open: {avg_up:+.3f}%  |  Average Down from Open: {avg_down:+.3f}%")
        
        # 5. Average actual_range_pct
        avg_range = combo_df['actual_range_pct_clean'].mean()
        print(f"  Average Actual Range%: {avg_range:.3f}%")
        
        # 6. Average intraday_high_pct and intraday_low_pct
        avg_high = combo_df['intraday_high_pct_clean'].mean()
        avg_low = combo_df['intraday_low_pct_clean'].mean()
        print(f"  Average Intraday High%: {avg_high:+.3f}%  |  Average Intraday Low%: {avg_low:+.3f}%")
        
        # 7. Distribution of move_direction
        if 'move_direction' in combo_df.columns:
            move_dist = combo_df['move_direction'].value_counts()
            print(f"  Move Direction Distribution:")
            for move_type, count in move_dist.items():
                pct = count / total_days * 100
                print(f"    {move_type:20s}: {count:3d} ({pct:5.2f}%)")
            dominant_pattern = move_dist.idxmax() if len(move_dist) > 0 else "N/A"
        else:
            dominant_pattern = "N/A"
            print(f"  Move Direction Distribution: N/A (column not found)")
        
        # 8. Expiry vs Non-expiry breakdown
        expiry_df = combo_df[combo_df['is_nifty_expiry'] == 1]
        non_expiry_df = combo_df[combo_df['is_nifty_expiry'] == 0]
        
        print(f"\n  Expiry vs Non-Expiry Breakdown:")
        
        if len(expiry_df) > 0:
            exp_green = len(expiry_df[expiry_df['result'] == 'Green'])
            exp_green_pct = (exp_green / len(expiry_df) * 100)
            exp_avg_change = expiry_df['change_pct_clean'].mean()
            print(f"    Expiry Days: {len(expiry_df):3d} | Green: {exp_green:3d} ({exp_green_pct:5.2f}%) | Avg Change: {exp_avg_change:+.3f}%")
        else:
            exp_green_pct = None
            exp_avg_change = None
            print(f"    Expiry Days: 0")
        
        if len(non_expiry_df) > 0:
            non_exp_green = len(non_expiry_df[non_expiry_df['result'] == 'Green'])
            non_exp_green_pct = (non_exp_green / len(non_expiry_df) * 100)
            non_exp_avg_change = non_expiry_df['change_pct_clean'].mean()
            print(f"    Non-Expiry Days: {len(non_expiry_df):3d} | Green: {non_exp_green:3d} ({non_exp_green_pct:5.2f}%) | Avg Change: {non_exp_avg_change:+.3f}%")
        else:
            non_exp_green_pct = None
            non_exp_avg_change = None
            print(f"    Non-Expiry Days: 0")
        
        # Calculate expiry divergence
        if exp_green_pct is not None and non_exp_green_pct is not None:
            exp_divergence = abs(exp_green_pct - non_exp_green_pct)
        else:
            exp_divergence = None
        
        # Store combination data
        all_combinations.append({
            'fii_view': fii_view,
            'pro_view': pro_view,
            'total_days': total_days,
            'green_count': green_count,
            'red_count': red_count,
            'green_pct': green_pct,
            'avg_change': avg_change,
            'avg_up': avg_up,
            'avg_down': avg_down,
            'avg_range': avg_range,
            'dominant_pattern': dominant_pattern,
            'expiry_days': len(expiry_df),
            'expiry_green_pct': exp_green_pct,
            'expiry_avg_change': exp_avg_change,
            'non_expiry_days': len(non_expiry_df),
            'non_expiry_green_pct': non_exp_green_pct,
            'non_expiry_avg_change': non_exp_avg_change,
            'expiry_divergence': exp_divergence
        })

print("\n" + "="*100)
print("STEP 3: MASTER SUMMARY TABLE - ALL COMBINATIONS")
print("="*100)

# Create DataFrame and sort by Green%
summary_df = pd.DataFrame(all_combinations)
summary_df_sorted = summary_df.sort_values('green_pct', ascending=False)

print(f"\n{'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Green%':>7s} {'Avg Chg%':>9s} {'Dominant Pattern':<20s} {'Exp G%':>7s} {'NExp G%':>7s}")
print("-" * 120)

for _, row in summary_df_sorted.iterrows():
    exp_g_str = f"{row['expiry_green_pct']:.1f}" if row['expiry_green_pct'] is not None else "N/A"
    nexp_g_str = f"{row['non_expiry_green_pct']:.1f}" if row['non_expiry_green_pct'] is not None else "N/A"
    
    print(f"{row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['green_pct']:>7.2f} {row['avg_change']:>+9.3f} {row['dominant_pattern']:<20s} {exp_g_str:>7s} {nexp_g_str:>7s}")

print("\n" + "="*100)
print("STEP 4: TOP 5 BEST COMBINATIONS (Highest Green%, >=5 days)")
print("="*100)

best_combos = summary_df[summary_df['total_days'] >= 5].nlargest(5, 'green_pct')
print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Green%':>7s} {'Avg Chg%':>9s}")
print("-" * 75)
for i, (_, row) in enumerate(best_combos.iterrows(), 1):
    print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['green_pct']:>7.2f} {row['avg_change']:>+9.3f}")

print("\n" + "="*100)
print("STEP 5: TOP 5 WORST COMBINATIONS (Lowest Green%, >=5 days)")
print("="*100)

worst_combos = summary_df[summary_df['total_days'] >= 5].nsmallest(5, 'green_pct')
print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Green%':>7s} {'Avg Chg%':>9s}")
print("-" * 75)
for i, (_, row) in enumerate(worst_combos.iterrows(), 1):
    print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['green_pct']:>7.2f} {row['avg_change']:>+9.3f}")

print("\n" + "="*100)
print("STEP 6: TOP 5 HIGHEST AVG CHANGE COMBINATIONS (>=5 days)")
print("="*100)

high_change = summary_df[summary_df['total_days'] >= 5].nlargest(5, 'avg_change')
print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Avg Chg%':>9s} {'Green%':>7s}")
print("-" * 75)
for i, (_, row) in enumerate(high_change.iterrows(), 1):
    print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['avg_change']:>+9.3f} {row['green_pct']:>7.2f}")

print("\n" + "="*100)
print("STEP 7: TOP 5 LOWEST AVG CHANGE COMBINATIONS (>=5 days)")
print("="*100)

low_change = summary_df[summary_df['total_days'] >= 5].nsmallest(5, 'avg_change')
print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Avg Chg%':>9s} {'Green%':>7s}")
print("-" * 75)
for i, (_, row) in enumerate(low_change.iterrows(), 1):
    print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['avg_change']:>+9.3f} {row['green_pct']:>7.2f}")

print("\n" + "="*100)
print("STEP 8: STRONG EXPIRY vs NON-EXPIRY DIVERGENCE (>15% difference, >=3 days each)")
print("="*100)

divergent = summary_df[
    (summary_df['expiry_divergence'].notna()) & 
    (summary_df['expiry_divergence'] > 15) &
    (summary_df['expiry_days'] >= 3) &
    (summary_df['non_expiry_days'] >= 3)
].sort_values('expiry_divergence', ascending=False)

if len(divergent) > 0:
    print(f"\n{'FII View':<20s} {'PRO View':<20s} {'Exp Days':>8s} {'Exp G%':>7s} {'NExp Days':>9s} {'NExp G%':>8s} {'Divergence':>11s}")
    print("-" * 100)
    for _, row in divergent.iterrows():
        print(f"{row['fii_view']:<20s} {row['pro_view']:<20s} {row['expiry_days']:>8d} {row['expiry_green_pct']:>7.1f} {row['non_expiry_days']:>9d} {row['non_expiry_green_pct']:>8.1f} {row['expiry_divergence']:>11.1f}")
else:
    print("\nNo combinations found with >15% divergence and >=3 days on each side.")

print("\n" + "="*100)
print("ANALYSIS COMPLETE")
print("="*100)

# Save to file
output_file = '/Users/manishkumar/Documents/learning/18-July-2026-Vix-Analysis-On-Expiry/fii_pro_6year_combinations_output.txt'
print(f"\nSaving detailed output to: {output_file}")

# Redirect stdout to file and re-run the analysis
import io
import contextlib

output_buffer = io.StringIO()

with contextlib.redirect_stdout(output_buffer):
    print("="*100)
    print("COMPREHENSIVE FII VIEW x PRO VIEW ANALYSIS - 6 YEAR DATASET")
    print("="*100)
    print(f"\nTotal rows in dataset: {len(df)}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    
    print("\n" + "="*100)
    print("STEP 1: ALL UNIQUE FII_VIEW VALUES AND COUNTS")
    print("="*100)
    for view, count in fii_view_counts.items():
        print(f"{view:25s}: {count:4d} days ({count/len(df)*100:5.2f}%)")
    
    print("\n" + "="*100)
    print("STEP 2: DETAILED ANALYSIS BY FII VIEW AND PRO VIEW")
    print("="*100)
    
    for fii_view in existing_fii_views:
        fii_df = df[df['fii_view'] == fii_view]
        
        print(f"\n{'='*100}")
        print(f"FII VIEW: {fii_view} ({len(fii_df)} days)")
        print(f"{'='*100}")
        
        pro_views = sorted(fii_df['pro_view'].unique())
        
        for pro_view in pro_views:
            combo_df = fii_df[fii_df['pro_view'] == pro_view]
            
            print(f"\n  PRO VIEW: {pro_view}")
            print(f"  {'-'*90}")
            
            total_days = len(combo_df)
            print(f"  Total Days: {total_days}")
            
            green_count = len(combo_df[combo_df['result'] == 'Green'])
            red_count = len(combo_df[combo_df['result'] == 'Red'])
            green_pct = (green_count / total_days * 100) if total_days > 0 else 0
            red_pct = (red_count / total_days * 100) if total_days > 0 else 0
            print(f"  Green: {green_count:3d} ({green_pct:5.2f}%)  |  Red: {red_count:3d} ({red_pct:5.2f}%)")
            
            avg_change = combo_df['change_pct_clean'].mean()
            print(f"  Average Change%: {avg_change:+.3f}%")
            
            avg_up = combo_df['up_from_open_clean'].mean()
            avg_down = combo_df['down_from_open_clean'].mean()
            print(f"  Average Up from Open: {avg_up:+.3f}%  |  Average Down from Open: {avg_down:+.3f}%")
            
            avg_range = combo_df['actual_range_pct_clean'].mean()
            print(f"  Average Actual Range%: {avg_range:.3f}%")
            
            avg_high = combo_df['intraday_high_pct_clean'].mean()
            avg_low = combo_df['intraday_low_pct_clean'].mean()
            print(f"  Average Intraday High%: {avg_high:+.3f}%  |  Average Intraday Low%: {avg_low:+.3f}%")
            
            if 'move_direction' in combo_df.columns:
                move_dist = combo_df['move_direction'].value_counts()
                print(f"  Move Direction Distribution:")
                for move_type, count in move_dist.items():
                    pct = count / total_days * 100
                    print(f"    {move_type:20s}: {count:3d} ({pct:5.2f}%)")
            else:
                print(f"  Move Direction Distribution: N/A (column not found)")
            
            expiry_df = combo_df[combo_df['is_nifty_expiry'] == 1]
            non_expiry_df = combo_df[combo_df['is_nifty_expiry'] == 0]
            
            print(f"\n  Expiry vs Non-Expiry Breakdown:")
            
            if len(expiry_df) > 0:
                exp_green = len(expiry_df[expiry_df['result'] == 'Green'])
                exp_green_pct = (exp_green / len(expiry_df) * 100)
                exp_avg_change = expiry_df['change_pct_clean'].mean()
                print(f"    Expiry Days: {len(expiry_df):3d} | Green: {exp_green:3d} ({exp_green_pct:5.2f}%) | Avg Change: {exp_avg_change:+.3f}%")
            else:
                print(f"    Expiry Days: 0")
            
            if len(non_expiry_df) > 0:
                non_exp_green = len(non_expiry_df[non_expiry_df['result'] == 'Green'])
                non_exp_green_pct = (non_exp_green / len(non_expiry_df) * 100)
                non_exp_avg_change = non_expiry_df['change_pct_clean'].mean()
                print(f"    Non-Expiry Days: {len(non_expiry_df):3d} | Green: {non_exp_green:3d} ({non_exp_green_pct:5.2f}%) | Avg Change: {non_exp_avg_change:+.3f}%")
            else:
                print(f"    Non-Expiry Days: 0")
    
    print("\n" + "="*100)
    print("STEP 3: MASTER SUMMARY TABLE - ALL COMBINATIONS")
    print("="*100)
    
    print(f"\n{'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Green%':>7s} {'Avg Chg%':>9s} {'Dominant Pattern':<20s} {'Exp G%':>7s} {'NExp G%':>7s}")
    print("-" * 120)
    
    for _, row in summary_df_sorted.iterrows():
        exp_g_str = f"{row['expiry_green_pct']:.1f}" if row['expiry_green_pct'] is not None else "N/A"
        nexp_g_str = f"{row['non_expiry_green_pct']:.1f}" if row['non_expiry_green_pct'] is not None else "N/A"
        
        print(f"{row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['green_pct']:>7.2f} {row['avg_change']:>+9.3f} {row['dominant_pattern']:<20s} {exp_g_str:>7s} {nexp_g_str:>7s}")
    
    print("\n" + "="*100)
    print("STEP 4: TOP 5 BEST COMBINATIONS (Highest Green%, >=5 days)")
    print("="*100)
    
    print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Green%':>7s} {'Avg Chg%':>9s}")
    print("-" * 75)
    for i, (_, row) in enumerate(best_combos.iterrows(), 1):
        print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['green_pct']:>7.2f} {row['avg_change']:>+9.3f}")
    
    print("\n" + "="*100)
    print("STEP 5: TOP 5 WORST COMBINATIONS (Lowest Green%, >=5 days)")
    print("="*100)
    
    print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Green%':>7s} {'Avg Chg%':>9s}")
    print("-" * 75)
    for i, (_, row) in enumerate(worst_combos.iterrows(), 1):
        print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['green_pct']:>7.2f} {row['avg_change']:>+9.3f}")
    
    print("\n" + "="*100)
    print("STEP 6: TOP 5 HIGHEST AVG CHANGE COMBINATIONS (>=5 days)")
    print("="*100)
    
    print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Avg Chg%':>9s} {'Green%':>7s}")
    print("-" * 75)
    for i, (_, row) in enumerate(high_change.iterrows(), 1):
        print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['avg_change']:>+9.3f} {row['green_pct']:>7.2f}")
    
    print("\n" + "="*100)
    print("STEP 7: TOP 5 LOWEST AVG CHANGE COMBINATIONS (>=5 days)")
    print("="*100)
    
    print(f"\n{'Rank':<5s} {'FII View':<20s} {'PRO View':<20s} {'Days':>5s} {'Avg Chg%':>9s} {'Green%':>7s}")
    print("-" * 75)
    for i, (_, row) in enumerate(low_change.iterrows(), 1):
        print(f"{i:<5d} {row['fii_view']:<20s} {row['pro_view']:<20s} {row['total_days']:>5d} {row['avg_change']:>+9.3f} {row['green_pct']:>7.2f}")
    
    print("\n" + "="*100)
    print("STEP 8: STRONG EXPIRY vs NON-EXPIRY DIVERGENCE (>15% difference, >=3 days each)")
    print("="*100)
    
    if len(divergent) > 0:
        print(f"\n{'FII View':<20s} {'PRO View':<20s} {'Exp Days':>8s} {'Exp G%':>7s} {'NExp Days':>9s} {'NExp G%':>8s} {'Divergence':>11s}")
        print("-" * 100)
        for _, row in divergent.iterrows():
            print(f"{row['fii_view']:<20s} {row['pro_view']:<20s} {row['expiry_days']:>8d} {row['expiry_green_pct']:>7.1f} {row['non_expiry_days']:>9d} {row['non_expiry_green_pct']:>8.1f} {row['expiry_divergence']:>11.1f}")
    else:
        print("\nNo combinations found with >15% divergence and >=3 days on each side.")
    
    print("\n" + "="*100)
    print("ANALYSIS COMPLETE")
    print("="*100)

# Write to file
with open(output_file, 'w') as f:
    f.write(output_buffer.getvalue())

print(f"Output saved successfully to: {output_file}")
