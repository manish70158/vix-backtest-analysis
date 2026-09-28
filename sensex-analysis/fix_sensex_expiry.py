#!/usr/bin/env python3
import csv
from datetime import datetime
import shutil
import os

infile='sensex_fii_t1_daily_results.csv'
outfile=infile + '.tmp'

# Backup
bak = infile + '.bak_' + datetime.now().strftime('%Y%m%dT%H%M%S')
shutil.copy2(infile, bak)
print('Backup created:', bak)

count=0
with open(infile, newline='') as fin, open(outfile,'w',newline='') as fout:
    reader=csv.DictReader(fin)
    fieldnames=reader.fieldnames
    writer=csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    for r in reader:
        try:
            d = datetime.strptime(r['date'], '%Y-%m-%d').date()
        except Exception:
            writer.writerow(r)
            continue
        if d < datetime(2025,1,1).date():
            target='Friday'
        elif datetime(2025,1,1).date() <= d <= datetime(2025,9,3).date():
            target='Tuesday'
        else:
            target='Thursday'
        dow = r.get('day_of_week','').strip()
        if dow == target:
            r['is_sensex_expiry']='1'
        else:
            r['is_sensex_expiry']='0'
            if '(sensex)' in (r.get('expiry_type') or ''):
                r['expiry_type']=''
        writer.writerow(r)
        count += 1

# Replace original
shutil.move(outfile, infile)
print('Processed rows:', count)
# Print sample row for 2024-06-06
with open(infile) as f:
    for line in f:
        if line.startswith('2024-06-06'):
            print('Row:', line.strip())
            break
