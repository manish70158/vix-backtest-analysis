# Data Protection Policy

## Purpose
Ensure that historical data (previous rows) are **NEVER overwritten or deleted**. Only new rows can be added, and existing rows can only be updated if the data source is more current.

## Rules

### Rule 1: Read-Only Historical Data
- **All rows with dates before TODAY are READ-ONLY**
- These rows can only be updated if:
  1. New data from an authoritative source (NSE/BSE archives) is available
  2. The update fixes corrupted/missing data only
  3. The update is **appended to the log** for audit purposes

### Rule 2: Add-Only Mode for CSV Writes
- Use "append + replace" pattern: Read → Verify → Append Only New → Write All
- Never delete rows
- Never modify dates in existing rows
- Track the date of last data for each CSV

### Rule 3: Backup Before Modification
- Create timestamped backup before any write operation
- Store backups in `./data-backups/` directory
- Format: `{filename}_{YYYY-MM-DD_HH-MM-SS}.backup.csv`

### Rule 4: Atomic Operations
- Write to a temp file first
- Verify the new file has all original rows + new rows
- Only then replace the original file
- Keep the backup regardless of success

### Rule 5: Audit Trail
- Log every CSV modification
- Store logs in `./modification-logs/{filename}.log`
- Format: `{timestamp} | {action} | {rows_added} | {rows_modified} | {status}`

### Rule 6: Data Validation
- Before writing: Verify row count >= original row count
- Before writing: Verify all original dates are present
- Before writing: Compare checksums of common rows (if same date, same content)

## File Protection

### Protected CSVs (Read-Only for Historical Data)
1. `vix_fii_t1_intraday_daily_results.csv` (Nifty daily)
2. `sensex-analysis/sensex_fii_t1_daily_results.csv` (Sensex daily)
3. `sensex-analysis/bse_fii_t1_daily.csv` (BSE daily)
4. `sensex-analysis/sensex_fii_t1_6year_expiry.csv` (Expiry data)
5. `fii_dii_backtest_daily_results.csv` (FII/DII backtest)
6. `vix_fii_t1_intraday_expiry_results.csv` (VIX expiry)

## Allowed Operations

### ✅ ALLOWED
- Add new rows for new dates
- Update columns for TODAY's row (if it exists) to add missing data
- Update recent rows (within last 5 trading days) to backfill OI data
- Fix corrupted data with log entry
- Create new backup CSVs for analysis

### ❌ NOT ALLOWED
- Delete any row
- Modify the date column
- Overwrite data for dates in the past (>5 days ago)
- Truncate and rewrite entire CSV
- Reorder rows by dropping and recreating

## Implementation

All Python scripts must:

1. **Before Reading:**
   ```python
   df = read_csv_with_protection(filepath, readonly_threshold_days=5)
   ```

2. **Before Writing:**
   ```python
   verify_no_row_loss(original_df, new_df, filepath)
   backup_csv(filepath)
   write_csv_atomic(filepath, new_df)
   log_modification(filepath, action, rows_added, rows_modified)
   ```

3. **Update Only Today/Recent:**
   ```python
   # Only update rows from last 5 trading days
   today = datetime.now().date()
   cutoff = today - timedelta(days=30)  # Allow for weekends
   
   for idx, row in df.iterrows():
       row_date = pd.Timestamp(row['date']).date()
       if row_date < cutoff:
           df.at[idx, ...] = ...  # ❌ NOT ALLOWED
   ```

## Monitoring

Check data integrity:
```bash
python3 check_data_integrity.py
```

View modification history:
```bash
cat modification-logs/*.log
```

List available backups:
```bash
ls -lah data-backups/
```

Restore from backup:
```bash
python3 restore_from_backup.py <csv_filename> <backup_timestamp>
```

## Emergency Recovery

If data is accidentally corrupted:
1. Stop all scripts immediately
2. Run: `python3 restore_from_backup.py <filename> latest`
3. Notify immediately
4. Review what caused the corruption
5. Update scripts to prevent recurrence
