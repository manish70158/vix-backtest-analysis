"""
Generate a TradingView Pine Script (v5) that labels each NIFTY daily candle with
that SAME day's FII_view / PRO_view PLUS the cumulative FII / PRO / CLIENT
positions, all embedded from the CSV.

TradingView has no access to FII/PRO data, so we bake it into the script as
compact delimited strings and rebuild parallel arrays on the first bar:
  - keys : "YYYYMMDD" per day (comma-joined)
  - recs : "Fcode,Pcode,<pos0..posN>" per day
           (fields comma-joined; records semicolon-joined)
A day is found with array.indexof(keys, ds); its record is str.split on ",".

View codes:
  B = Strong Bullish  U = Bullish  u = Mildly Bullish
  X = Strong Bearish  D = Bearish  d = Mildly Bearish  N = Neutral

The nine position columns are the cumulative T-1 FII / PRO / CLIENT fut/call/put
daily positions. (Client has no view, only positions.)

Source: "vix_fii_t1_intraday_daily_results copy.csv"
Output: nifty_prior_fii_pro_views.pine
"""

import pandas as pd

SRC = "vix_fii_t1_intraday_daily_results copy.csv"
OUT = "nifty_prior_fii_pro_views.pine"
MAX_DAYS = 500  # TradingView label cap: 1 combined label per candle => fits 500

# Cumulative-position columns put into each record (fut/call/put per participant).
# Order matters: the Pine side reads them by index (FII 2-4, PRO 5-7, CLIENT 8-10).
POS_COLS = [
    "cum_t1_fii_fut_daily",
    "cum_t1_fii_call_daily",
    "cum_t1_fii_put_daily",
    "cum_t1_pro_fut_daily",
    "cum_t1_pro_call_daily",
    "cum_t1_pro_put_daily",
    "cum_t1_client_fut_daily",
    "cum_t1_client_call_daily",
    "cum_t1_client_put_daily",
]


def code(view: str) -> str:
    v = str(view).lower()
    if "strong bull" in v: return "B"   # Strong Bullish
    if "strong bear" in v: return "X"   # Strong Bearish
    if "mildly bull" in v: return "u"
    if "mildly bear" in v: return "d"
    if "bull" in v: return "U"
    if "bear" in v: return "D"
    return "N"  # neutral / nan / other


def num(x) -> str:
    """Compact integer string (no decimals); 0 when missing. No ',' or ';'."""
    if pd.isna(x):
        return "0"
    return str(int(round(float(x))))


def chunk_on_delim(s: str, delim: str, max_chars: int = 3800):
    """Split s (delim-joined tokens) into chunks <= max_chars, never breaking a
    token. Each returned chunk is itself delim-joined tokens, safe as a Pine
    string literal (< 4096) that str.split rebuilds exactly."""
    tokens = s.split(delim)
    chunks, cur = [], ""
    for t in tokens:
        add = t if cur == "" else delim + t
        if len(cur) + len(add) > max_chars and cur:
            chunks.append(cur)
            cur = t
        else:
            cur += add
    if cur:
        chunks.append(cur)
    return chunks


def main():
    df = pd.read_csv(SRC, dtype={"date": str})
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Same-day labelling: each candle shows ITS OWN day's views + positions.
    df = df.dropna(subset=["fii_view", "pro_view"])
    df = df.tail(MAX_DAYS).reset_index(drop=True)  # most recent 500 trading days

    keys, recs = [], []
    for _, r in df.iterrows():
        keys.append(r["date"].strftime("%Y%m%d"))
        fields = [code(r["fii_view"]), code(r["pro_view"])] + [num(r[c]) for c in POS_COLS]
        recs.append(",".join(fields))

    keys_blob = ",".join(keys)       # dates, comma-joined
    recs_blob = ";".join(recs)       # records, semicolon-joined (fields comma-joined)

    # Each Pine string literal must be < 4096 chars, and a built-up string VALUE
    # must stay < 4096 at runtime. So we embed the data as several literals that
    # are str.split immediately and array.concat'd (arrays have no 4096 limit).
    key_chunks = chunk_on_delim(keys_blob, ",")
    rec_chunks = chunk_on_delim(recs_blob, ";")

    # Each concat gets its OWN `if barstate.isfirst` block: Pine caps how much
    # code a single local (if) block may contain, and 11 huge string literals in
    # one block overflows it ("if statement is too long"). Separate top-level if
    # blocks keep each one short while still running only on the first bar.
    build_lines = []
    for c in key_chunks:
        build_lines.append("if barstate.isfirst")
        build_lines.append(f'    keys := array.concat(keys, str.split("{c}", ","))')
    for c in rec_chunks:
        build_lines.append("if barstate.isfirst")
        build_lines.append(f'    recs := array.concat(recs, str.split("{c}", ";"))')
    data_build = "\n".join(build_lines)

    pine = f'''//@version=5
// NIFTY daily candles labelled with that SAME day's FII & PRO views PLUS the
// cumulative FII / PRO / CLIENT positions (fut / call / put). Data embedded from
// vix_fii_t1_intraday_daily_results — most recent {len(df)} trading days
// ({df['date'].min().date()} -> {df['date'].max().date()}).
// Apply on a NIFTY *Daily* chart (e.g. NSE:NIFTY). One label per candle, so all
// {len(df)} days fit under TradingView's 500-label cap.
// View codes: B=StrongBullish U=Bullish u=MildlyBullish X=StrongBearish D=Bearish d=MildlyBearish N=Neutral.
// (Client has no view in the data, so it appears as positions only.)
indicator("NIFTY Daily FII & PRO Views + Positions", overlay=true, max_labels_count=500)

// ----- Inputs -----
showLabels  = input.bool(true, "Show same-day FII/PRO labels on candles")
showPos     = input.bool(true, "Show FII / PRO / CLIENT positions on hover (tooltip)")
onlyChanges = input.bool(true, "Show the big P/F text only when the view CHANGES (unchanged days keep a hover dot)", tooltip="Declutters the text so identical views don't stack into a wall. EVERY day still gets a hoverable marker with its views + positions. Turn off to show the full text box on every day.")
showBg      = input.bool(true, "Shade background by same-day PRO bias")
showDebug   = input.bool(true, "Show debug panel (top-right)")

// ----- Embedded data (parallel arrays, rebuilt on the first bar) -----
// keys[i] = "YYYYMMDD"; recs[i] = "Fcode,Pcode,fFut,fCall,fPut,pFut,pCall,pPut,cFut,cCall,cPut".
// Literals are kept < 4096 chars and str.split immediately into arrays.
var keys = array.new_string()
var recs = array.new_string()
{data_build}

// ----- Helpers (single-line ternaries: Pine mis-parses multi-line ones) -----
longName(string c) => c == "B" ? "Strong Bullish" : c == "U" ? "Bullish" : c == "u" ? "Mildly Bullish" : c == "X" ? "Strong Bearish" : c == "D" ? "Bearish" : c == "d" ? "Mildly Bearish" : "Neutral"

biasColor(string c) => (c == "B" or c == "U" or c == "u") ? color.new(color.teal, 0) : (c == "X" or c == "D" or c == "d") ? color.new(color.red, 0) : color.new(color.gray, 0)

// ----- Lookup current bar's date -----
// Build YYYYMMDD with str.format so there are no separators / stray chars.
ds      = str.format("{{0,number,0000}}{{1,number,00}}{{2,number,00}}", year(time), month(time), dayofmonth(time))
idx     = array.indexof(keys, ds)
hasData = idx >= 0

string fCode = na
string pCode = na
string fFut = na
string fCall = na
string fPut = na
string pFut = na
string pCall = na
string pPut = na
string cFut = na
string cCall = na
string cPut = na
if hasData
    f = str.split(array.get(recs, idx), ",")
    fCode := array.get(f, 0)
    pCode := array.get(f, 1)
    fFut  := array.get(f, 2)
    fCall := array.get(f, 3)
    fPut  := array.get(f, 4)
    pFut  := array.get(f, 5)
    pCall := array.get(f, 6)
    pPut  := array.get(f, 7)
    cFut  := array.get(f, 8)
    cCall := array.get(f, 9)
    cPut  := array.get(f, 10)

// ----- Background bias by same-day PRO view (bold enough to be obvious) -----
bgcolor(showBg and hasData ? color.new(biasColor(pCode), 70) : na)

// ----- Decide what each candle shows -----
// EVERY day with data gets a hoverable label, so no candle is ever "missing"
// its data. To avoid a wall of text boxes, the big P/F text is only drawn when
// the view CHANGES from the prior trading day (onlyChanges, default on); the
// other days get a tiny dot that still carries the full tooltip on hover.
// fCode[1]/pCode[1] are the prior bar's codes.
viewChanged = na(fCode[1]) or na(pCode[1]) or fCode != fCode[1] or pCode != pCode[1]
drawLabel   = hasData and showLabels
showText    = not onlyChanges or viewChanged

// ----- One label per day so hover data is ALWAYS available -----
// The tooltip (hover) always lists the P/F views plus the nine cumulative
// positions. Change-days render the full P/F text box; unchanged days render a
// small dot carrying the same tooltip, so every candle stays hoverable.
if drawLabel
    tip = "P: " + longName(pCode) + "   F: " + longName(fCode)
    if showPos
        tip := tip + "\\nFII     Fut: " + fFut + "   Call: " + fCall + "   Put: " + fPut
        tip := tip + "\\nPRO     Fut: " + pFut + "   Call: " + pCall + "   Put: " + pPut
        tip := tip + "\\nCLIENT  Fut: " + cFut + "   Call: " + cCall + "   Put: " + cPut
    if showText
        txt = "P: " + longName(pCode) + "\\nF: " + longName(fCode)
        label.new(bar_index, high, txt, style=label.style_label_down, yloc=yloc.abovebar, color=biasColor(pCode), textcolor=color.white, size=size.small, tooltip=tip)
    else
        label.new(bar_index, high, "", style=label.style_circle, yloc=yloc.abovebar, color=biasColor(pCode), size=size.tiny, tooltip=tip)

// ----- Debug panel: confirms the script runs and whether the date matched -----
var int matchCount = 0
if hasData
    matchCount := matchCount + 1
var int labelCount = 0
if drawLabel
    labelCount := labelCount + 1
var int textCount = 0
if drawLabel and showText
    textCount := textCount + 1
var table dbg = table.new(position.top_right, 2, 5, border_width=1)
if showDebug and barstate.islast
    table.cell(dbg, 0, 0, "days loaded",   text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 1, 0, str.tostring(array.size(keys)), text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 0, 1, "today key",     text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 1, 1, ds,              text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 0, 2, "found today",   text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 1, 2, hasData ? "yes" : "no", text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 0, 3, "days matched",  text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 1, 3, str.tostring(matchCount), text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 0, 4, "hover / text",  text_color=color.white, bgcolor=color.gray)
    table.cell(dbg, 1, 4, str.tostring(labelCount) + " / " + str.tostring(textCount), text_color=color.white, bgcolor=color.gray)
'''

    with open(OUT, "w") as fh:
        fh.write(pine)

    print(f"Wrote {OUT}")
    print(f"  {len(df)} days embedded ({df['date'].min().date()} -> {df['date'].max().date()})")
    print(f"  keys blob {len(keys_blob)} chars in {len(key_chunks)} literal(s); "
          f"recs blob {len(recs_blob)} chars in {len(rec_chunks)} literal(s)")


if __name__ == "__main__":
    main()
