import pandas as pd

print("=" * 100)
print("CHECKING DATA STRUCTURE")
print("=" * 100)

# Load the two CSV files
timing_df = pd.read_csv('/Users/manishkumar/Documents/learning/18-July-2026-Vix-Analysis-On-Expiry/fii-pro-alignment-analysis/vix_threshold_timing_results.csv')
fii_pro_df = pd.read_csv('/Users/manishkumar/Documents/learning/18-July-2026-Vix-Analysis-On-Expiry/fii-pro-alignment-analysis/fii_pro_alignment_results.csv')

print("\n1. TIMING DATA FILE:")
print(f"   Shape: {timing_df.shape}")
print(f"   Columns: {list(timing_df.columns)}")
print(f"\n   First few rows:")
print(timing_df.head())
print(f"\n   Alignment values: {timing_df['alignment'].value_counts().to_dict()}")
print(f"   VIX Exhaustion values: {timing_df['vix_exhaustion'].value_counts().to_dict()}")
print(f"   Cross Session values: {timing_df['cross_session'].value_counts().to_dict()}")

print("\n\n2. FII-PRO DATA FILE:")
print(f"   Shape: {fii_pro_df.shape}")
print(f"   Columns: {list(fii_pro_df.columns)}")
print(f"\n   First few rows:")
print(fii_pro_df.head())

# Join them
merged_df = timing_df.merge(fii_pro_df[['date', 'fii_view', 'pro_view']], on='date', how='left')
print(f"\n\n3. MERGED DATA:")
print(f"   Shape: {merged_df.shape}")
print(f"\n   First few rows:")
print(merged_df.head())

# Check for bearish late-morning crosses
bearish = merged_df[merged_df['alignment'] == 'Bearish']
print(f"\n\n4. BEARISH DATA:")
print(f"   Total Bearish: {len(bearish)}")
if len(bearish) > 0:
    print(f"   VIX Exhaustion in Bearish: {bearish['vix_exhaustion'].value_counts().to_dict()}")
    print(f"   Cross Sessions in Bearish: {bearish['cross_session'].value_counts().to_dict()}")
    
    exceeded = bearish[bearish['vix_exhaustion'] == 'Exceeded Half']
    print(f"\n   Bearish Exceeded Half: {len(exceeded)}")
    if len(exceeded) > 0:
        print(f"   Sessions: {exceeded['cross_session'].value_counts().to_dict()}")
        
    late_morning = bearish[bearish['cross_session'] == 'Late Morning']
    print(f"\n   Bearish Late Morning: {len(late_morning)}")
    if len(late_morning) > 0:
        print(f"   VIX Exhaustion: {late_morning['vix_exhaustion'].value_counts().to_dict()}")
