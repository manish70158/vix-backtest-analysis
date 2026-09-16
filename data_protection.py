#!/usr/bin/env python3
"""
Data Protection Utilities

Enforces the DATA_PROTECTION_POLICY.md rules:
- No overwriting of historical data
- Automatic backups before modifications
- Audit trail for all changes
- Data validation before writes
"""

import pandas as pd
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import json
import hashlib

REPO = Path(__file__).resolve().parent
BACKUP_DIR = REPO / "data-backups"
LOG_DIR = REPO / "modification-logs"

# Create required directories
BACKUP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat(timespec='seconds')


def get_file_hash(df):
    """Generate a hash of the dataframe for integrity checking."""
    content = df.to_csv(index=False)
    return hashlib.md5(content.encode()).hexdigest()


def backup_csv(csv_path):
    """Create a timestamped backup of a CSV file."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        return None
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"{csv_path.stem}_{timestamp}.backup.csv"
    backup_path = BACKUP_DIR / backup_name
    
    try:
        shutil.copy2(csv_path, backup_path)
        log_action(csv_path.name, "BACKUP_CREATED", 
                   info=f"Backup: {backup_name}")
        return backup_path
    except Exception as e:
        log_action(csv_path.name, "BACKUP_FAILED", info=str(e))
        raise


def verify_no_row_loss(original_df, new_df, csv_path):
    """
    Verify that no rows were lost in the update.
    
    Checks:
    1. Row count: new >= original
    2. Original dates all present in new
    3. Date column integrity
    """
    csv_path = Path(csv_path)
    
    if len(new_df) < len(original_df):
        error = (f"Row loss detected in {csv_path.name}: "
                f"{len(original_df)} -> {len(new_df)} rows")
        log_action(csv_path.name, "VALIDATION_FAILED", info=error)
        raise ValueError(error)
    
    # Check date column exists and is consistent
    if 'date' in original_df.columns and 'date' in new_df.columns:
        original_dates = set(pd.to_datetime(original_df['date']).dt.date)
        new_dates = set(pd.to_datetime(new_df['date']).dt.date)
        
        missing_dates = original_dates - new_dates
        if missing_dates:
            error = (f"Missing dates in {csv_path.name}: "
                    f"{len(missing_dates)} dates lost: {sorted(missing_dates)[:5]}...")
            log_action(csv_path.name, "VALIDATION_FAILED", info=error)
            raise ValueError(error)
    
    return True


def log_action(filename, action, rows_added=0, rows_modified=0, info=""):
    """Log a modification action to the audit trail."""
    log_file = LOG_DIR / f"{Path(filename).stem}.log"
    
    timestamp = get_timestamp()
    log_entry = {
        "timestamp": timestamp,
        "action": action,
        "rows_added": rows_added,
        "rows_modified": rows_modified,
        "info": info
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")


def read_csv_with_protection(csv_path, readonly_threshold_days=5):
    """
    Read a CSV file with protection metadata.
    
    Returns: (dataframe, metadata_dict)
    metadata includes: original_hash, original_row_count, last_write_date
    """
    csv_path = Path(csv_path)
    df = pd.read_csv(csv_path)
    
    metadata = {
        'path': str(csv_path),
        'original_hash': get_file_hash(df),
        'original_row_count': len(df),
        'readonly_threshold_days': readonly_threshold_days,
        'read_timestamp': get_timestamp(),
    }
    
    if 'date' in df.columns:
        last_date = pd.to_datetime(df['date']).max().date()
        metadata['last_data_date'] = str(last_date)
        metadata['today'] = str(datetime.now().date())
        metadata['readonly_cutoff'] = str(
            datetime.now().date() - timedelta(days=readonly_threshold_days)
        )
    
    return df, metadata


def write_csv_with_protection(csv_path, new_df, original_df=None, 
                               action_desc="UPDATE"):
    """
    Write a CSV with full protection:
    1. Verify no row loss
    2. Create backup
    3. Write to temp file first
    4. Verify integrity
    5. Move temp to final
    6. Log action
    """
    csv_path = Path(csv_path)
    
    # Step 1: Verify no row loss
    if original_df is not None:
        verify_no_row_loss(original_df, new_df, csv_path)
        rows_added = len(new_df) - len(original_df)
    else:
        rows_added = len(new_df)
    
    # Step 2: Create backup
    backup_path = backup_csv(csv_path)
    
    # Step 3: Write to temp file
    temp_path = csv_path.with_suffix('.tmp.csv')
    try:
        new_df.to_csv(temp_path, index=False)
    except Exception as e:
        error = f"Failed to write temp file: {e}"
        log_action(csv_path.name, "WRITE_FAILED", info=error)
        raise
    
    # Step 4: Verify temp file
    temp_df = pd.read_csv(temp_path)
    if len(temp_df) != len(new_df):
        error = f"Temp file verification failed: {len(temp_df)} != {len(new_df)}"
        log_action(csv_path.name, "VERIFICATION_FAILED", info=error)
        temp_path.unlink()
        raise ValueError(error)
    
    # Step 5: Move temp to final
    try:
        shutil.move(str(temp_path), str(csv_path))
    except Exception as e:
        error = f"Failed to move temp file: {e}"
        log_action(csv_path.name, "MOVE_FAILED", info=error)
        if temp_path.exists():
            temp_path.unlink()
        raise
    
    # Step 6: Log action
    log_action(csv_path.name, f"WRITE_{action_desc}", 
              rows_added=rows_added, info=f"Backup: {backup_path.name if backup_path else 'N/A'}")
    
    return True


def restore_from_backup(csv_name, backup_timestamp="latest"):
    """Restore a CSV from a backup."""
    backup_dir = BACKUP_DIR
    
    # Find matching backups
    pattern = f"{Path(csv_name).stem}_*.backup.csv"
    backups = sorted(backup_dir.glob(pattern))
    
    if not backups:
        print(f"No backups found for {csv_name}")
        return False
    
    if backup_timestamp == "latest":
        backup_path = backups[-1]
    else:
        matching = [b for b in backups if backup_timestamp in b.name]
        if not matching:
            print(f"No backup matching timestamp: {backup_timestamp}")
            return False
        backup_path = matching[-1]
    
    csv_path = REPO / csv_name
    if csv_path.exists():
        # Backup current (broken) version
        broken_backup = csv_path.with_stem(f"{csv_path.stem}_BROKEN_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(csv_path, broken_backup)
        print(f"Backed up broken version to: {broken_backup}")
    
    # Restore from backup
    shutil.copy2(backup_path, csv_path)
    log_action(csv_name, "RESTORED_FROM_BACKUP", 
               info=f"Restored from: {backup_path.name}")
    print(f"Restored {csv_name} from {backup_path.name}")
    return True


def check_data_integrity(csv_path):
    """Check integrity of a CSV file."""
    csv_path = Path(csv_path)
    
    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        
        # Check for missing values in date column
        if 'date' in df.columns:
            null_dates = df['date'].isna().sum()
            if null_dates > 0:
                print(f"⚠️  {null_dates} rows with missing dates")
                return False
        
        # Check for duplicates
        if 'date' in df.columns:
            dup_dates = df['date'].duplicated().sum()
            if dup_dates > 0:
                print(f"⚠️  {dup_dates} duplicate dates found")
                return False
        
        print(f"✓ {csv_path.name}: {len(df)} rows, OK")
        
        # List recent changes
        log_file = LOG_DIR / f"{csv_path.stem}.log"
        if log_file.exists():
            with open(log_file, 'r') as f:
                entries = [json.loads(line) for line in f if line.strip()]
            recent = sorted(entries, key=lambda x: x['timestamp'], reverse=True)[:3]
            print(f"  Recent actions:")
            for entry in recent:
                print(f"    - {entry['timestamp']}: {entry['action']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error checking {csv_path.name}: {e}")
        return False


def get_backup_list(csv_name=None):
    """List all available backups."""
    if csv_name:
        pattern = f"{Path(csv_name).stem}_*.backup.csv"
        backups = sorted(BACKUP_DIR.glob(pattern))
    else:
        backups = sorted(BACKUP_DIR.glob("*.backup.csv"))
    
    if not backups:
        print("No backups found")
        return
    
    print(f"Available backups ({len(backups)}):")
    for backup in backups:
        size = backup.stat().st_size / (1024 * 1024)  # MB
        print(f"  {backup.name} ({size:.2f} MB)")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 data_protection.py check <csv_path>")
        print("  python3 data_protection.py backups [csv_name]")
        print("  python3 data_protection.py restore <csv_name> [timestamp]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "check" and len(sys.argv) > 2:
        check_data_integrity(sys.argv[2])
    elif command == "backups":
        csv_name = sys.argv[2] if len(sys.argv) > 2 else None
        get_backup_list(csv_name)
    elif command == "restore" and len(sys.argv) > 2:
        csv_name = sys.argv[2]
        timestamp = sys.argv[3] if len(sys.argv) > 3 else "latest"
        restore_from_backup(csv_name, timestamp)
    else:
        print("Unknown command")
        sys.exit(1)
