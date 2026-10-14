#!/usr/bin/env python3
"""Regenerate the embedded data arrays in nifty_prior_fii_pro_views.pine from
the most recent 500 trading days of vix_fii_t1_intraday_daily_results.csv.

Each record = "Fcode,Pcode,fFut,fCall,fPut,pFut,pCall,pPut,cFut,cCall,cPut"
  - Fcode/Pcode : that day's fii_view / pro_view compressed to a 1-char code
  - the 9 positions : the cum_t1_* raw net OI (Long-Short) at end of T-1

Keeps everything before the "Embedded data" marker (header + inputs, with the
date range refreshed) and everything from the "Helpers" marker onward (logic)
untouched; only the data arrays in between are rebuilt. Literals are chunked so
each str.split string stays well under Pine's 4096-char limit.
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CSV = REPO / "vix_fii_t1_intraday_daily_results.csv"
PINE = HERE / "nifty_prior_fii_pro_views.pine"
MAX_DAYS = 500
CHUNK_LIMIT = 3800  # chars inside one str.split literal (< 4096 Pine cap)

VIEW_CODE = {
    "Strong Bullish": "B", "Bullish": "U", "Mildly Bullish": "u",
    "Strong Bearish": "X", "Bearish": "D", "Mildly Bearish": "d",
    "Neutral": "N",
}
POS_COLS = [
    "cum_t1_fii_fut_daily", "cum_t1_fii_call_daily", "cum_t1_fii_put_daily",
    "cum_t1_pro_fut_daily", "cum_t1_pro_call_daily", "cum_t1_pro_put_daily",
    "cum_t1_client_fut_daily", "cum_t1_client_call_daily",
    "cum_t1_client_put_daily",
]


def code(view):
    return VIEW_CODE.get(str(view).strip(), "N")


def ival(x):
    return "0" if pd.isna(x) else str(int(round(float(x))))


def chunk(items, sep):
    """Group items so each sep-joined chunk stays under CHUNK_LIMIT chars."""
    chunks, cur, cur_len = [], [], 0
    for it in items:
        add = len(it) + (1 if cur else 0)
        if cur and cur_len + add > CHUNK_LIMIT:
            chunks.append(cur)
            cur, cur_len = [], 0
            add = len(it)
        cur.append(it)
        cur_len += add
    if cur:
        chunks.append(cur)
    return chunks


def main():
    df = pd.read_csv(CSV)
    # Need date + views + all 9 position columns present
    df = df[df["date"].notna() & df[POS_COLS].notna().all(axis=1)]
    df = df.sort_values("date").tail(MAX_DAYS).reset_index(drop=True)

    keys, recs = [], []
    for _, r in df.iterrows():
        keys.append(str(r["date"]).replace("-", ""))
        rec = [code(r["fii_view"]), code(r["pro_view"])] + [ival(r[c]) for c in POS_COLS]
        recs.append(",".join(rec))

    d0 = df["date"].iloc[0]
    d1 = df["date"].iloc[-1]

    # Build the data section
    lines = []
    lines.append("// ----- Embedded data (parallel arrays, rebuilt on the first bar) -----")
    lines.append('// keys[i] = "YYYYMMDD"; recs[i] = "Fcode,Pcode,fFut,fCall,fPut,pFut,pCall,pPut,cFut,cCall,cPut".')
    lines.append("// Literals are kept < 4096 chars and str.split immediately into arrays.")
    lines.append("var keys = array.new_string()")
    lines.append("var recs = array.new_string()")
    for ch in chunk(keys, ","):
        lines.append("if barstate.isfirst")
        lines.append('    keys := array.concat(keys, str.split("' + ",".join(ch) + '", ","))')
    for ch in chunk(recs, ";"):
        lines.append("if barstate.isfirst")
        lines.append('    recs := array.concat(recs, str.split("' + ";".join(ch) + '", ";"))')
    data_block = "\n".join(lines) + "\n"

    # Read current file, splice in the new header date-range + data block
    text = PINE.read_text()
    pre, _, rest = text.partition("// ----- Embedded data")
    _, _, logic = rest.partition("// ----- Helpers")
    logic = "// ----- Helpers" + logic

    # Refresh the date-range line in the header comment
    import re
    pre = re.sub(r"\(\d{4}-\d{2}-\d{2} -> \d{4}-\d{2}-\d{2}\)",
                 f"({d0} -> {d1})", pre)

    PINE.write_text(pre + data_block + "\n" + logic)
    print(f"Rebuilt {PINE.name}: {len(keys)} days ({d0} -> {d1}), "
          f"{len(chunk(keys, ','))} key-chunks, {len(chunk(recs, ';'))} rec-chunks")


if __name__ == "__main__":
    main()
