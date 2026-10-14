"""
Daily NIFTY candlestick chart (last 6 years) with each candle labelled by the
FII_view and PRO_view from ONE DAY PRIOR to that candle.

Why prior-day: the FII/PRO positioning is known at T-1 and is used to anticipate
day T's candle, so each candle is annotated with the previous session's views.

Source: "vix_fii_t1_intraday_daily_results copy.csv"
Output: candles_prior_views.html   (interactive — scroll/zoom; hover for detail)

Readability + scrollability:
  - Non-trading days (weekends/holidays) are removed so candles are contiguous.
  - Chart opens zoomed to the most recent ~3 months (big, readable candles).
  - Range buttons (1m/3m/6m/1y/All) + bottom range-slider to scroll the 6 years.
  - Short prior-day bias codes sit above (PRO) and below (FII) each candle,
    colour-coded, and become legible as you zoom in. Full views are in the hover.
"""

import pandas as pd
import plotly.graph_objects as go

SRC = "vix_fii_t1_intraday_daily_results copy.csv"
OUT = "candles_prior_views.html"
YEARS = 6


def bias_color(view: str) -> str:
    v = str(view).lower()
    if "bull" in v:
        return "#26a69a"   # green
    if "bear" in v:
        return "#ef5350"   # red
    return "#9e9e9e"       # neutral/grey


def short_view(view: str) -> str:
    v = str(view).lower()
    if "strong bull" in v: return "sBull"
    if "strong bear" in v: return "sBear"
    if "mildly bull" in v: return "mBull"
    if "mildly bear" in v: return "mBear"
    if "bull" in v: return "Bull"
    if "bear" in v: return "Bear"
    if "neutral" in v or "nan" in v: return "Neut"
    return str(view)[:4]


def main():
    df = pd.read_csv(SRC, dtype={"date": str})
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # Prior-day (T-1) views attached to each candle
    df["prior_fii_view"] = df["fii_view"].shift(1)
    df["prior_pro_view"] = df["pro_view"].shift(1)
    df["prior_date"] = df["date"].shift(1)

    # Last 6 years
    cutoff = df["date"].max() - pd.DateOffset(years=YEARS)
    df = df[df["date"] >= cutoff].reset_index(drop=True)

    # Hover text: current candle OHLC + the PRIOR day's FII / PRO views
    def hover(r):
        pd_str = r["prior_date"].strftime("%Y-%m-%d") if pd.notna(r["prior_date"]) else "n/a"
        return (
            f"<b>{r['date'].strftime('%Y-%m-%d')} ({r['day_of_week']})</b><br>"
            f"O {r['nifty_open']:.1f}  H {r['nifty_high']:.1f}<br>"
            f"L {r['nifty_low']:.1f}  C {r['nifty_close']:.1f}<br>"
            f"Chg {r['actual_open_close_pct']:+.2f}%<br>"
            f"<br><b>Prior day ({pd_str}) views:</b><br>"
            f"FII: <b>{r['prior_fii_view']}</b><br>"
            f"PRO: <b>{r['prior_pro_view']}</b>"
        )

    df["hover"] = df.apply(hover, axis=1)
    df["pro_color"] = df["prior_pro_view"].apply(bias_color)
    df["fii_color"] = df["prior_fii_view"].apply(bias_color)
    df["pro_short"] = df["prior_pro_view"].apply(short_view)
    df["fii_short"] = df["prior_fii_view"].apply(short_view)
    df["pro_y"] = df["nifty_high"] * 1.006   # PRO label above the candle
    df["fii_y"] = df["nifty_low"] * 0.994    # FII label below the candle

    # Remove non-trading days so candles are contiguous (big readability win)
    all_days = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    present = set(df["date"])
    missing = [d for d in all_days if d not in present]

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["date"],
        open=df["nifty_open"], high=df["nifty_high"],
        low=df["nifty_low"], close=df["nifty_close"],
        name="NIFTY",
        increasing_line_color="#26a69a", decreasing_line_color="#ef5350",
        text=df["hover"], hoverinfo="text",
    ))

    # Prior-day PRO bias — label above each candle
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["pro_y"],
        mode="markers+text",
        marker=dict(size=5, color=df["pro_color"], symbol="triangle-down"),
        text=df["pro_short"], textposition="top center",
        textfont=dict(size=8, color=df["pro_color"]),
        name="Prior-day PRO view", hovertext=df["hover"], hoverinfo="text",
    ))

    # Prior-day FII bias — label below each candle
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["fii_y"],
        mode="markers+text",
        marker=dict(size=5, color=df["fii_color"], symbol="triangle-up"),
        text=df["fii_short"], textposition="bottom center",
        textfont=dict(size=8, color=df["fii_color"]),
        name="Prior-day FII view", hovertext=df["hover"], hoverinfo="text",
    ))

    # Default view = most recent ~3 months (readable), scroll back via slider/buttons
    end = df["date"].max()
    start = end - pd.DateOffset(months=3)

    fig.update_layout(
        title=(f"NIFTY Daily Candles — last {YEARS} years · "
               f"PRO (▽ above) & FII (△ below) labels are the PRIOR day's view · "
               f"hover for full detail"),
        template="plotly_dark",
        height=840,
        hovermode="x",
        legend=dict(orientation="h", y=1.03, x=0),
        dragmode="pan",
    )
    fig.update_xaxes(
        range=[start, end],
        rangebreaks=[dict(values=missing)],   # drop weekends/holidays → contiguous
        rangeslider=dict(visible=True, thickness=0.06),
        rangeselector=dict(
            buttons=[
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all", label="All"),
            ],
            bgcolor="#2a2a2a", activecolor="#555",
        ),
    )
    fig.update_yaxes(title="NIFTY", fixedrange=False)

    config = {"scrollZoom": True, "displayModeBar": True}
    fig.write_html(OUT, include_plotlyjs="cdn", config=config)
    print(f"Wrote {OUT} with {len(df)} candles "
          f"({df['date'].min().date()} → {df['date'].max().date()})")
    print("Opens on the last 3 months. Scroll with the slider / range buttons; "
          "drag to pan, scroll-wheel to zoom. Hover any candle for the T-1 FII/PRO view.")


if __name__ == "__main__":
    main()
