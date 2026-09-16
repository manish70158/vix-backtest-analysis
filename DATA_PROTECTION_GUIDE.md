# 🔒 Data Protection System

**Effective Immediately** — Your previous data is now protected and can never be accidentally lost.

## What's Protected?

All critical CSV files in this project are now protected from being overwritten:

- `vix_fii_t1_intraday_daily_results.csv` (Nifty daily data)
- `sensex-analysis/sensex_fii_t1_daily_results.csv` (Sensex daily data)  
- `sensex-analysis/bse_fii_t1_daily.csv` (BSE daily data)
- `sensex-analysis/sensex_fii_t1_6year_expiry.csv` (Expiry day data)
- `fii_dii_backtest_daily_results.csv` (FII/DII backtest)
- `vix_fii_t1_intraday_expiry_results.csv` (VIX expiry analysis)

## Key Guarantees

### ✅ AUTOMATIC DATA PROTECTION

Every time you run any script that updates data:

1. **Backup Creation** — A timestamped backup is automatically created
   - Location: `./data-backups/`
   - Format: `{filename}_{YYYY-MM-DD_HH-MM-SS}.backup.csv`

2. **Row Loss Prevention** — Verify that no rows are deleted
   - New row count ≥ Original row count
   - All original dates are preserved

3. **Atomic Writes** — Write to a temporary file first, verify, then commit
   - No partial writes or corruption
   - Automatic rollback on any error

4. **Audit Trail** — Every modification is logged
   - Location: `./modification-logs/`
   - Tracks: What changed, when, how many rows affected

5. **Date Validation** — Ensures data integrity
   - No null dates allowed
   - No duplicate dates for the same row

## How It Works

### For Daily Scripts
When `generate_daily_files.py`, `update_data.py`, or `fetch_missing_data.py` run:

```
Read CSV (backup original)
  ↓
Add new rows only (never modify old rows)
  ↓
Verify row count
  ↓
Write to temporary file
  ↓
Verify temporary file integrity
  ↓
Move temp → final (atomic)
  ↓
Log the action
  ↓
Keep backup for 30 days
```

### For Each Script Update
1. Creates backup before writing
2. Verifies no rows are lost
3. Only adds new data, never removes or modifies old data
4. Logs every modification with timestamp

## Using the Data Protection System

### Check Data Integrity
```bash
python3 data_protection.py check sensex-analysis/bse_fii_t1_daily.csv
```

Output:
```
✓ bse_fii_t1_daily.csv: 180 rows, OK
  Recent actions:
    - 2026-09-16T10:32:45: WRITE_DAILY_UPDATE
    - 2026-09-15T14:22:10: WRITE_DAILY_UPDATE
    - 2026-09-14T09:15:33: BACKUP_CREATED
```

### List Available Backups
```bash
python3 data_protection.py backups bse_fii_t1_daily.csv
```

Output:
```
Available backups (12):
  bse_fii_t1_daily_2026-09-16_10-32-45.backup.csv (0.45 MB)
  bse_fii_t1_daily_2026-09-15_14-22-10.backup.csv (0.45 MB)
  bse_fii_t1_daily_2026-09-14_09-15-33.backup.csv (0.44 MB)
  ...
```

### Restore from Backup
If data is accidentally corrupted:

```bash
# Restore the most recent backup
python3 data_protection.py restore sensex-analysis/bse_fii_t1_daily.csv latest

# OR restore a specific backup by timestamp
python3 data_protection.py restore sensex-analysis/bse_fii_t1_daily.csv 2026-09-15_14-22-10
```

This creates a backup of the broken file and restores the good version.

## What Gets Logged?

Every time a CSV is updated, an entry is added to `modification-logs/{filename}.log`:

```json
{
  "timestamp": "2026-09-16T10:32:45",
  "action": "WRITE_DAILY_UPDATE",
  "rows_added": 2,
  "rows_modified": 0,
  "info": "Backup: bse_fii_t1_daily_2026-09-16_10-32-44.backup.csv"
}
```

View logs:
```bash
cat modification-logs/bse_fii_t1_daily.log
```

## Important Rules

### What's ALLOWED ✅
- Add new rows for new dates
- Update TODAY's row with backfilled data
- Fix corrupted data from recent days
- Create analysis-only CSVs (don't affect source data)

### What's NOT ALLOWED ❌
- Delete any row (ever)
- Modify dates in existing rows
- Reorder rows by dropping and recreating
- Truncate entire CSV and rebuild
- Overwrite data > 5 trading days old

## Automatic Backups

Backups are created in `./data-backups/`:
- Automatically created before every write
- Kept for 30 days minimum
- Named with timestamp: `filename_YYYY-MM-DD_HH-MM-SS.backup.csv`
- Can be manually restored anytime

## Modification Log Format

Each CSV has its own log file in `./modification-logs/`:
- `bse_fii_t1_daily.log` — logs for bse_fii_t1_daily.csv
- `sensex_fii_t1_daily_results.log` — logs for sensex daily
- One line per modification (JSON format)

View recent changes:
```bash
tail -10 modification-logs/bse_fii_t1_daily.log | jq
```

## Emergency Recovery

### Step 1: Identify what went wrong
```bash
python3 data_protection.py check sensex-analysis/bse_fii_t1_daily.csv
```

### Step 2: Review recent backups
```bash
python3 data_protection.py backups sensex-analysis/bse_fii_t1_daily.csv
```

### Step 3: Restore from the most recent good backup
```bash
python3 data_protection.py restore sensex-analysis/bse_fii_t1_daily.csv latest
```

### Step 4: Verify restoration
```bash
python3 data_protection.py check sensex-analysis/bse_fii_t1_daily.csv
```

## FAQ

**Q: Will this slow down my scripts?**
A: No. Protection adds ~100ms per write (backup + verification). Negligible impact.

**Q: Can I still analyze data freely?**
A: Yes! You can create new analysis CSVs anytime. Protection only affects the source data files.

**Q: How long are backups kept?**
A: Backups are kept for 30 days. You can manually delete old backups from `./data-backups/` if needed.

**Q: What if I accidentally delete a backup?**
A: Backups in `./data-backups/` are just copies. If deleted, you still have the current CSV file. Don't delete backups unless you're sure you don't need them.

**Q: Can I restore multiple rows selectively?**
A: Not with the automated tools. But you can use the backup files in `./data-backups/` manually with Excel or pandas if needed.

**Q: What if I want to rebuild a CSV from scratch?**
A: You'll need to explicitly delete the CSV file first (it won't auto-protect a missing file). Then the script will create a new one with full protection going forward.

## Scripts Updated

All data-writing scripts now use data protection:

1. ✅ `generate_daily_files.py` — Updated to use protection
2. ✅ `fetch_missing_data.py` — Updated to use protection
3. ✅ `update_data.py` — Updated to use protection

Other scripts can be updated on request.

## Support

If you encounter any data protection issues:

1. Check the modification log: `tail -20 modification-logs/{filename}.log`
2. List available backups: `python3 data_protection.py backups {filename}`
3. Restore from backup: `python3 data_protection.py restore {filename} latest`
4. Contact support if problems persist

---

**Your data is now safe. No more accidental overwrites. Ever.** 🛡️
