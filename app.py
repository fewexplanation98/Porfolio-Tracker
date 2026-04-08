import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Portfolio Tracker", page_icon="📈", layout="wide")

ASSETS = [
    {"name": "Savings", "category": "Savings", "subcategory": "Savings", "bucket": "Savings", "pac": 0, "active": "No"},
    {"name": "Core MSCI World", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 640, "active": "Yes"},
    {"name": "AI & Big Data", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 160, "active": "Yes"},
    {"name": "Physical Gold", "category": "ETF", "subcategory": "ETF Gold", "bucket": "Defensive", "pac": 108, "active": "Yes"},
    {"name": "Global Gov Bond", "category": "ETF", "subcategory": "ETF Bond", "bucket": "Defensive", "pac": 80, "active": "Yes"},
    {"name": "Core EUR Corp Bond", "category": "ETF", "subcategory": "ETF Bond", "bucket": "Defensive", "pac": 108, "active": "Yes"},
    {"name": "MSCI World Value", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 180, "active": "Yes"},
    {"name": "MSCI EM", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 164, "active": "Yes"},
    {"name": "Defence Tech", "category": "ETF", "subcategory": "ETF Stock", "bucket": "Stocks", "pac": 60, "active": "Yes"},
]

MONTH_END_SEED = [
    ("Oct/25", "Savings", 34010.01), ("Oct/25", "Core MSCI World", 11058), ("Oct/25", "AI & Big Data", 3265),
    ("Oct/25", "Physical Gold", 1792), ("Oct/25", "Global Gov Bond", 1456), ("Oct/25", "Core EUR Corp Bond", 1456),
    ("Oct/25", "MSCI World Value", 1439), ("Oct/25", "MSCI EM", 1233), ("Oct/25", "Defence Tech", 483.20),
    ("Nov/25", "Savings", 35690.22), ("Nov/25", "Core MSCI World", 11303), ("Nov/25", "AI & Big Data", 3177),
    ("Nov/25", "Physical Gold", 1875), ("Nov/25", "Global Gov Bond", 1470), ("Nov/25", "Core EUR Corp Bond", 1478),
    ("Nov/25", "MSCI World Value", 1499), ("Nov/25", "MSCI EM", 1225), ("Nov/25", "Defence Tech", 383.76),
    ("Dec/25", "Savings", 37889.16), ("Dec/25", "Core MSCI World", 11866), ("Dec/25", "AI & Big Data", 3256),
    ("Dec/25", "Physical Gold", 2001), ("Dec/25", "Global Gov Bond", 1547), ("Dec/25", "Core EUR Corp Bond", 1534),
    ("Dec/25", "MSCI World Value", 1651), ("Dec/25", "MSCI EM", 1306), ("Dec/25", "Defence Tech", 402.89),
    ("Jan/26", "Savings", 38095), ("Jan/26", "Core MSCI World", 12365), ("Jan/26", "AI & Big Data", 3215),
    ("Jan/26", "Physical Gold", 2214), ("Jan/26", "Global Gov Bond", 1568), ("Jan/26", "Core EUR Corp Bond", 1592),
    ("Jan/26", "MSCI World Value", 1824), ("Jan/26", "MSCI EM", 1419), ("Jan/26", "Defence Tech", 452.33),
    ("Feb/26", "Savings", 37801), ("Feb/26", "Core MSCI World", 13001), ("Feb/26", "AI & Big Data", 3108),
    ("Feb/26", "Physical Gold", 2540), ("Feb/26", "Global Gov Bond", 1640), ("Feb/26", "Core EUR Corp Bond", 1649),
    ("Feb/26", "MSCI World Value", 2007), ("Feb/26", "MSCI EM", 1544), ("Feb/26", "Defence Tech", 450.32),
    ("Mar/26", "Savings", 39883), ("Mar/26", "Core MSCI World", 13914), ("Mar/26", "AI & Big Data", 2970),
    ("Mar/26", "Physical Gold", 2493), ("Mar/26", "Global Gov Bond", 1666), ("Mar/26", "Core EUR Corp Bond", 1679),
    ("Mar/26", "MSCI World Value", 2387), ("Mar/26", "MSCI EM", 2033), ("Mar/26", "Defence Tech", 439.71),
]

MANUAL_SEED = [
    ("Oct/25", "Core MSCI World", 690.40), ("Oct/25", "AI & Big Data", 101), ("Oct/25", "Physical Gold", 70),
    ("Oct/25", "Global Gov Bond", 52), ("Oct/25", "Core EUR Corp Bond", 54), ("Oct/25", "MSCI World Value", 196.99),
    ("Oct/25", "MSCI EM", 44), ("Nov/25", "Core MSCI World", 486), ("Nov/25", "Physical Gold", 70),
    ("Nov/25", "Global Gov Bond", 52), ("Nov/25", "Core EUR Corp Bond", 54), ("Nov/25", "MSCI World Value", 96),
    ("Nov/25", "MSCI EM", 44), ("Dec/25", "Core MSCI World", 486), ("Dec/25", "Physical Gold", 70),
    ("Dec/25", "Global Gov Bond", 52), ("Dec/25", "Core EUR Corp Bond", 54), ("Dec/25", "MSCI World Value", 96),
    ("Dec/25", "MSCI EM", 44), ("Jan/26", "Core MSCI World", 486), ("Jan/26", "Physical Gold", 70),
    ("Jan/26", "Global Gov Bond", 52), ("Jan/26", "Core EUR Corp Bond", 54), ("Jan/26", "MSCI World Value", 96),
    ("Jan/26", "MSCI EM", 44), ("Feb/26", "Core MSCI World", 486), ("Feb/26", "Physical Gold", 70),
    ("Feb/26", "Global Gov Bond", 52), ("Feb/26", "Core EUR Corp Bond", 54), ("Feb/26", "MSCI World Value", 96),
    ("Feb/26", "MSCI EM", 44), ("Mar/26", "Core MSCI World", 1539.76), ("Mar/26", "Physical Gold", 220.99),
    ("Mar/26", "Global Gov Bond", 52), ("Mar/26", "Core EUR Corp Bond", 54), ("Mar/26", "MSCI World Value", 497),
    ("Mar/26", "MSCI EM", 645.99),
]

MONTHS = [
    "Oct/25", "Nov/25", "Dec/25", "Jan/26", "Feb/26", "Mar/26",
    "Apr/26", "May/26", "Jun/26", "Jul/26", "Aug/26", "Sep/26",
    "Oct/26", "Nov/26", "Dec/26"
]

MONTH_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}


def month_sort_value(label: str) -> int:
    month, year = label.split("/")
    return (2000 + int(year)) * 100 + MONTH_MAP[month]


def eur0(value: float) -> str:
    sign = "-" if value < 0 else ""
    value = abs(float(value))
    s = f"{value:,.0f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sign}€ {s}"


def pct1(value: float) -> str:
    return f"{value:.1f}%"


def perf_color(value):
    if value is None or pd.isna(value):
        return "#94a3b8"
    return "#22c55e" if value >= 0 else "#ef4444"


def perf_arrow_html(value):
    if value is None or pd.isna(value):
        return ""
    if value >= 0:
        return '<span style="color:#22c55e;font-size:18px;font-weight:800;">↗</span>'
    return '<span style="color:#ef4444;font-size:18px;font-weight:800;">↘</span>'


def seed_data():
    assets_df = pd.DataFrame(ASSETS)
    month_end_df = pd.DataFrame(MONTH_END_SEED, columns=["month", "asset", "value"])
    manual_df = pd.DataFrame(MANUAL_SEED, columns=["month", "asset", "amount"])

    pac_rows = []
    for month in MONTHS:
        if month_sort_value(month) >= month_sort_value("Apr/26"):
            for _, row in assets_df[assets_df["category"] == "ETF"].iterrows():
                pac_rows.append({
                    "month": month,
                    "asset": row["name"],
                    "mode": "Auto" if float(row["pac"]) > 0 else "No",
                    "amount": float(row["pac"])
                })
    pac_df = pd.DataFrame(pac_rows)
    return assets_df, month_end_df, manual_df, pac_df


def calc_month_perf(asset, month, month_end_map, pac_map, manual_map):
    idx = MONTHS.index(month)
    if idx == 0:
        return None
    prev = MONTHS[idx - 1]
    end = month_end_map.get((month, asset), 0)
    prev_end = month_end_map.get((prev, asset), 0)
    flow = pac_map.get((month, asset), 0) + manual_map.get((month, asset), 0)

    if prev_end > 0 and end > 0:
        pnl = end - prev_end - flow
        base = prev_end + flow / 2
        if base != 0:
            return pnl / base * 100
    return None


if "assets_df" not in st.session_state:
    assets_df, month_end_df, manual_df, pac_df = seed_data()
    st.session_state.assets_df = assets_df
    st.session_state.month_end_df = month_end_df
    st.session_state.manual_df = manual_df
    st.session_state.pac_df = pac_df

assets_df = st.session_state.assets_df.copy()
month_end_df = st.session_state.month_end_df.copy()
manual_df = st.session_state.manual_df.copy()
pac_df = st.session_state.pac_df.copy()

all_assets = assets_df["name"].tolist()
etf_assets = assets_df.loc[assets_df["category"] == "ETF", "name"].tolist()

st.markdown(
    """
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1.25rem;
    max-width: 1500px;
}
.stSelectbox label {
    font-size: 13px !important;
    color: #cbd5e1 !important;
}
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
}
div[data-baseweb="tag"] {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}
.kpi-card {
    background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(17,24,39,0.88));
    border: 1px solid rgba(148,163,184,0.16);
    border-radius: 18px;
    padding: 16px 16px;
    min-height: 108px;
    box-shadow: 0 14px 32px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.04);
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-label {
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 10px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.kpi-value {
    font-size: 24px;
    line-height: 1.1;
    font-weight: 700;
    color: #f8fafc;
    white-space: nowrap;
    text-align: center;
}
.kpi-pos { color: #16a34a; }
.kpi-neg { color: #dc2626; }
.etf-row-card {
    background: linear-gradient(180deg, rgba(15,23,42,0.56), rgba(15,23,42,0.38));
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 12px;
    padding: 8px 12px;
    margin-bottom: 6px;
}
.etf-name {
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.15;
}
.etf-sub {
    font-size: 11px;
    color: #94a3b8;
    margin-top: 2px;
}
.etf-perf-head {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94a3b8;
    text-align: center;
    margin-bottom: 2px;
}
.etf-perf-pos {
    font-size: 18px;
    font-weight: 700;
    color: #22c55e;
    text-align: center;
}
.etf-perf-neg {
    font-size: 18px;
    font-weight: 700;
    color: #ef4444;
    text-align: center;
}
.etf-perf-na {
    font-size: 18px;
    font-weight: 700;
    color: #94a3b8;
    text-align: center;
}
.spark-head {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94a3b8;
    margin-bottom: 4px;
}
</style>
""",
    unsafe_allow_html=True,
)

header_left, header_right = st.columns([8, 1.6])
with header_left:
    st.title("Portfolio Tracker")
with header_right:
    st.markdown("##### Selected month")
    selected_month = st.selectbox(
        "Selected month",
        options=MONTHS,
        index=MONTHS.index("Mar/26"),
        label_visibility="collapsed"
    )

st.caption("Month end update, PAC confirmation, manual transactions and add ETF")

month_end_map = {(r.month, r.asset): float(r.value) for r in month_end_df.itertuples(index=False)}
manual_map = manual_df.groupby(["month", "asset"], dropna=False)["amount"].sum().to_dict() if not manual_df.empty else {}

pac_effective = pac_df.copy()
pac_effective["effective_amount"] = pac_effective.apply(
    lambda r: 0 if r["mode"] == "No" else float(r["amount"]),
    axis=1
)
pac_map = pac_effective.groupby(["month", "asset"])["effective_amount"].sum().to_dict() if not pac_effective.empty else {}

selected_idx = MONTHS.index(selected_month)
prev_month = MONTHS[selected_idx - 1] if selected_idx > 0 else None

rows = []
for _, asset_row in assets_df.iterrows():
    asset = asset_row["name"]
    end_value = month_end_map.get((selected_month, asset), 0)
    prev_end = month_end_map.get((prev_month, asset), 0) if prev_month else 0
    pac_flow = pac_map.get((selected_month, asset), 0)
    manual_flow = manual_map.get((selected_month, asset), 0)
    total_flow = pac_flow + manual_flow

    pnl = None
    perf_pct = None
    if end_value != 0 and prev_end != 0:
        pnl = end_value - prev_end - total_flow
        base = prev_end + total_flow / 2
        if base != 0:
            perf_pct = pnl / base * 100

    rows.append({
        "Asset": asset,
        "Category": asset_row["category"],
        "Bucket": asset_row["bucket"],
        "Subcategory": asset_row["subcategory"],
        "End Value": end_value,
        "Prev End": prev_end,
        "PAC Flow": pac_flow,
        "Manual Flow": manual_flow,
        "Total Flow": total_flow,
        "PnL": pnl,
        "Perf %": perf_pct,
    })

summary_df = pd.DataFrame(rows)

portfolio_total = float(summary_df["End Value"].sum())
savings_total = float(summary_df.loc[summary_df["Category"] == "Savings", "End Value"].sum())
etf_total = portfolio_total - savings_total
monthly_etf_transactions = float(summary_df.loc[summary_df["Category"] == "ETF", "Total Flow"].sum())
etf_abs_perf = float(summary_df.loc[(summary_df["Category"] == "ETF") & summary_df["PnL"].notna(), "PnL"].sum())

etf_prev_end = float(summary_df.loc[summary_df["Category"] == "ETF", "Prev End"].sum())
etf_total_flow = float(summary_df.loc[summary_df["Category"] == "ETF", "Total Flow"].sum())
etf_perf_pct = None
if etf_prev_end > 0:
    etf_perf_pct = etf_abs_perf / (etf_prev_end + etf_total_flow / 2) * 100


def render_kpi(col, title, value, tone="default"):
    cls = "kpi-value"
    if tone == "pos":
        cls += " kpi-pos"
    elif tone == "neg":
        cls += " kpi-neg"

    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{title}</div>
            <div class="{cls}">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


k1, k2, k3, k4, k5, k6 = st.columns(6)
render_kpi(k1, "Portfolio Total", eur0(portfolio_total))
render_kpi(k2, "ETF Total", eur0(etf_total))
render_kpi(k3, "Savings", eur0(savings_total))
render_kpi(k4, "Monthly ETF Transactions", eur0(monthly_etf_transactions))
render_kpi(k5, "ETF Abs Performance", eur0(etf_abs_perf), "pos" if etf_abs_perf >= 0 else "neg")
render_kpi(
    k6,
    "ETF % Performance",
    "-" if etf_perf_pct is None else pct1(etf_perf_pct),
    "default" if etf_perf_pct is None else ("pos" if etf_perf_pct >= 0 else "neg")
)

# frecce a destra del dato
k5_arrow = "↗" if etf_abs_perf >= 0 else "↘"
k5_arrow_color = "#22c55e" if etf_abs_perf >= 0 else "#ef4444"

if etf_perf_pct is None:
    k6_arrow = ""
    k6_arrow_color = "#94a3b8"
else:
    k6_arrow = "↗" if etf_perf_pct >= 0 else "↘"
    k6_arrow_color = "#22c55e" if etf_perf_pct >= 0 else "#ef4444"

k5.markdown(
    (
        "<div style='margin-top:-66px; margin-left:120px; text-align:left; "
        f"font-size:18px; font-weight:800; color:{k5_arrow_color};'>{k5_arrow}</div>"
    ),
    unsafe_allow_html=True,
)

k6.markdown(
    (
        "<div style='margin-top:-66px; margin-left:114px; text-align:left; "
        f"font-size:18px; font-weight:800; color:{k6_arrow_color};'>{k6_arrow}</div>"
    ),
    unsafe_allow_html=True,
)

st.write("")

# pie charts
p1, p2, p3 = st.columns([0.92, 0.92, 1.46], vertical_alignment="top")

with p1:
    st.subheader("ETF vs Savings")
    split_df = pd.DataFrame({"Type": ["ETF", "Savings"], "Value": [etf_total, savings_total]})
    fig_split = go.Figure(data=[go.Pie(
        labels=split_df["Type"],
        values=split_df["Value"],
        hole=0.66,
        sort=False,
        direction="clockwise",
        rotation=180,
        marker=dict(colors=["#1f2937", "#9ca3af"]),
        textposition="inside",
        textinfo="percent"
    )])
    fig_split.update_traces(textfont_size=13, showlegend=True)
    fig_split.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=34, b=28),
        legend=dict(orientation="h", y=-0.10, x=0.18, traceorder="normal", font=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_split, use_container_width=True, config={"displayModeBar": False})

with p2:
    st.subheader("ETF Stock vs Defensive")
    bucket_df = summary_df[summary_df["Category"] == "ETF"].groupby("Bucket")["End Value"].sum().reset_index()
    bucket_df["Bucket"] = pd.Categorical(bucket_df["Bucket"], categories=["Stocks", "Defensive"], ordered=True)
    bucket_df = bucket_df.sort_values("Bucket")
    fig_bucket = go.Figure(data=[go.Pie(
        labels=bucket_df["Bucket"],
        values=bucket_df["End Value"],
        hole=0.66,
        sort=False,
        direction="clockwise",
        rotation=180,
        marker=dict(colors=["#334155", "#cbd5e1"]),
        textposition="inside",
        textinfo="percent"
    )])
    fig_bucket.update_traces(textfont_size=13, showlegend=True)
    fig_bucket.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=34, b=28),
        legend=dict(orientation="h", y=-0.10, x=0.09, traceorder="normal", font=dict(size=11)),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bucket, use_container_width=True, config={"displayModeBar": False})

with p3:
    st.subheader("ETF Split")
    pie_df = summary_df[(summary_df["Category"] == "ETF") & (summary_df["End Value"] > 0)][["Asset", "End Value"]].copy()
    pie_colors = {
        "Core MSCI World": "#86c5f8",
        "AI & Big Data": "#1273de",
        "Physical Gold": "#f6a6a6",
        "MSCI World Value": "#ff3131",
        "MSCI EM": "#7ae39d",
        "Core EUR Corp Bond": "#33b4ad",
        "Global Gov Bond": "#f4c95d",
        "Defence Tech": "#ff9800",
    }
    pie_df["Color"] = pie_df["Asset"].map(pie_colors)

    fig_pie = go.Figure(data=[go.Pie(
        labels=pie_df["Asset"],
        values=pie_df["End Value"],
        hole=0.58,
        sort=False,
        textinfo="percent",
        textfont_size=12,
        marker=dict(colors=pie_df["Color"]),
        showlegend=False
    )])
    fig_pie.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=34, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    legend_items = []
    for _, r in pie_df.iterrows():
        legend_items.append(
            f"<div style='display:flex; align-items:center; gap:8px; min-width:0; white-space:nowrap;'><span style='display:inline-block; width:12px; height:12px; border-radius:0; background:{r['Color']};'></span><span style='font-size:11px; color:#e5e7eb;'>{r['Asset']}</span></div>"
        )
    legend_html = "".join(legend_items)
    st.markdown(
        f"<div style='display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:10px 18px; margin-top:2px; width:100%;'>{legend_html}</div>",
        unsafe_allow_html=True,
    )

# trend
st.subheader("Portfolio Trend MoM")

trend_rows = []
for i, month in enumerate(MONTHS[: selected_idx + 1]):
    total = month_end_df.loc[month_end_df["month"] == month, "value"].sum()
    savings = month_end_df.loc[(month_end_df["month"] == month) & (month_end_df["asset"] == "Savings"), "value"].sum()
    etf = total - savings
    mom = None
    if i > 0:
        prev_total = trend_rows[-1]["Total"]
        if prev_total > 0:
            mom = (total - prev_total) / prev_total * 100
    trend_rows.append({"Month": month, "Savings": savings, "ETF": etf, "Total": total, "MoM %": mom})

trend_df = pd.DataFrame(trend_rows)

if not trend_df.empty:
    line_color = "#22c55e"
    if len(trend_df) >= 2 and trend_df.iloc[-1]["Total"] < trend_df.iloc[-2]["Total"]:
        line_color = "#ef4444"

    fig_combo = go.Figure()

    fig_combo.add_bar(
        x=trend_df["Month"],
        y=trend_df["ETF"],
        name="ETF",
        marker_color="#1f2937",
        width=0.30,
        text=[eur0(v) for v in trend_df["ETF"]],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=12, color="#f8fafc")
    )
    fig_combo.add_bar(
        x=trend_df["Month"],
        y=trend_df["Savings"],
        name="Savings",
        marker_color="#9ca3af",
        width=0.30,
        text=[eur0(v) for v in trend_df["Savings"]],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=12, color="#111827")
    )
    fig_combo.add_trace(
        go.Scatter(
            x=trend_df["Month"],
            y=trend_df["Total"],
            mode="lines+markers",
            name="Portfolio Total",
            line=dict(color=line_color, width=3, dash="dash"),
            marker=dict(size=7, color=line_color)
        )
    )

    total_label_y = trend_df["Total"] + (trend_df["Total"].max() * 0.010)
    fig_combo.add_trace(
        go.Scatter(
            x=trend_df["Month"],
            y=total_label_y,
            mode="text",
            text=[eur0(v) for v in trend_df["Total"]],
            textfont=dict(size=15, color="#f8fafc"),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    pct_x = []
    pct_y = []
    pct_text = []
    for idx, row in trend_df.iterrows():
        if idx == 0 or pd.isna(row["MoM %"]):
            continue
        pct_x.append(row["Month"])
        pct_y.append(row["Total"] + (trend_df["Total"].max() * 0.030))
        pct_text.append(pct1(row["MoM %"]))

    fig_combo.add_trace(
        go.Scatter(
            x=pct_x,
            y=pct_y,
            mode="text",
            text=pct_text,
            textfont=dict(color="#cbd5e1", size=13),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    fig_combo.update_layout(
        barmode="stack",
        height=440,
        bargap=0.62,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.08, x=0),
        yaxis_title="",
        xaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)"
    )
    fig_combo.update_yaxes(showgrid=True, gridcolor="rgba(203,213,225,0.18)", tickformat=",.0f")
    fig_combo.update_xaxes(showgrid=False)
    st.plotly_chart(fig_combo, use_container_width=True, config={"displayModeBar": False})

# Monthly performance + track affiancati
left_perf_col, right_track_col = st.columns([0.52, 0.48], vertical_alignment="top")

# dati monthly performance
etf_perf_table = []
months_5m = MONTHS[max(0, selected_idx - 4): selected_idx + 1]

for asset in etf_assets:
    current_perf = calc_month_perf(asset, selected_month, month_end_map, pac_map, manual_map)
    spark_vals = []
    spark_months = []

    for m in months_5m:
        p = calc_month_perf(asset, m, month_end_map, pac_map, manual_map)
        if p is not None:
            spark_vals.append(p)
            spark_months.append(m)

    meta = assets_df.loc[assets_df["name"] == asset].iloc[0]
    etf_perf_table.append({
        "asset": asset,
        "subcategory": meta["subcategory"],
        "bucket": meta["bucket"],
        "current_perf": current_perf,
        "spark_months": spark_months,
        "spark_vals": spark_vals
    })

etf_perf_table = sorted(
    etf_perf_table,
    key=lambda x: -999 if x["current_perf"] is None else x["current_perf"],
    reverse=True
)

with left_perf_col:
    st.subheader("ETF Monthly Performance")
    st.caption("Compact monthly snapshot")

    for row in etf_perf_table:
        asset = row["asset"]
        current_perf = row["current_perf"]
        spark_months = row["spark_months"]
        spark_vals = row["spark_vals"]

        outer1, outer2, outer3 = st.columns([0.95, 0.38, 0.82], vertical_alignment="center")

        with outer1:
            st.markdown(
                f"""
                <div class="etf-row-card" style="display:inline-block; padding:8px 14px; min-width:220px;">
                    <div class="etf-name">{asset}</div>
                    <div class="etf-sub">{row['bucket']} - {row['subcategory']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with outer2:
            perf_cls = "etf-perf-na"
            perf_text = "-"
            if current_perf is not None:
                perf_cls = "etf-perf-pos" if current_perf >= 0 else "etf-perf-neg"
                perf_text = f"{'↗' if current_perf >= 0 else '↘'} {pct1(current_perf)}"

            st.markdown(
                f"""
                <div class="etf-row-card" style="min-height:58px; display:flex; flex-direction:column; justify-content:center; align-items:center; padding:6px 10px; text-align:center;">
                    <div class="etf-perf-head">{selected_month}</div>
                    <div class="{perf_cls}">{perf_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with outer3:
            st.markdown(
                '<div class="spark-head" style="margin-bottom:4px;">Sparkline last 5 months</div>',
                unsafe_allow_html=True
            )

            if len(spark_vals) >= 2:
                s_df = pd.DataFrame({"Month": spark_months, "Perf": spark_vals})
                s_color = perf_color(spark_vals[-1])
                fill = "rgba(34,197,94,0.16)" if s_color == "#22c55e" else "rgba(239,68,68,0.14)"

                fig_spark = go.Figure()
                fig_spark.add_trace(
                    go.Scatter(
                        x=s_df["Month"],
                        y=s_df["Perf"],
                        mode="lines+markers",
                        line=dict(color=s_color, width=2.2, shape="linear"),
                        marker=dict(size=4, color=s_color, symbol="diamond"),
                        fill="tozeroy",
                        fillcolor=fill,
                        showlegend=False
                    )
                )
                fig_spark.update_layout(
                    height=70,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(255,255,255,0.02)"
                )
                st.plotly_chart(fig_spark, use_container_width=True, config={"displayModeBar": False})
            else:
                st.caption("No 5M data")

with right_track_col:
    st.subheader("MoM ETF Performance Track")

    months_to_show = MONTHS[max(0, selected_idx - 5):selected_idx + 1]
    default_selection = [x for x in ["Core MSCI World", "MSCI EM", "MSCI World Value", "Physical Gold"] if x in etf_assets]

    selected_track_etfs = st.multiselect(
        "ETF selection",
        options=etf_assets,
        default=default_selection
    )

    mom_data = []
    for asset in selected_track_etfs:
        for m in months_to_show:
            p = calc_month_perf(asset, m, month_end_map, pac_map, manual_map)
            if p is not None:
                mom_data.append({"Month": m, "Asset": asset, "Perf": p})

    mom_df = pd.DataFrame(mom_data)

    if not mom_df.empty:
        fig_track = px.line(mom_df, x="Month", y="Perf", color="Asset", markers=True)
        fig_track.update_traces(line=dict(width=2.4, shape="linear"), marker=dict(size=5))
        fig_track.update_layout(
            height=820,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.02)",
            yaxis_title="%",
            xaxis_title="",
            legend=dict(orientation="h", y=-0.10, x=0)
        )
        fig_track.update_yaxes(showgrid=True, gridcolor="rgba(203,213,225,0.18)")
        st.plotly_chart(fig_track, use_container_width=True, config={"displayModeBar": False})

st.divider()

update_tab, pac_tab, manual_tab, asset_tab = st.tabs(
    ["Update Month End", "Confirm PAC", "Manual Transaction", "Add ETF"]
)

with update_tab:
    st.subheader("Insert month end values")
    draft_month = st.selectbox("Month to update", options=MONTHS, index=MONTHS.index("Apr/26"), key="draft_month_end")

    with st.form("month_end_form"):
        month_end_inputs = {}
        cols = st.columns(3)

        for i, asset in enumerate(all_assets):
            current_value = month_end_map.get((draft_month, asset), 0)
            with cols[i % 3]:
                month_end_inputs[asset] = st.number_input(
                    asset,
                    min_value=0.0,
                    value=float(current_value),
                    step=100.0,
                    format="%.2f",
                    key=f"month_end_{draft_month}_{asset}"
                )

        save_month_end = st.form_submit_button("Save month end", use_container_width=True)
        if save_month_end:
            updated_rows = [{"month": draft_month, "asset": asset, "value": float(value)} for asset, value in month_end_inputs.items()]
            month_end_df = month_end_df[month_end_df["month"] != draft_month]
            month_end_df = pd.concat([month_end_df, pd.DataFrame(updated_rows)], ignore_index=True)
            month_end_df["sort"] = month_end_df["month"].apply(month_sort_value)
            month_end_df = month_end_df.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)
            st.session_state.month_end_df = month_end_df
            st.success(f"Month end saved for {draft_month}")
            st.rerun()

with pac_tab:
    st.subheader("Confirm monthly PAC")
    pac_month = st.selectbox("PAC month", options=MONTHS, index=MONTHS.index("Apr/26"), key="draft_pac_month")
    pac_view = pac_df[pac_df["month"] == pac_month].copy().sort_values("asset")

    with st.form("pac_form"):
        pac_updates = []

        for asset in etf_assets:
            asset_default = float(assets_df.loc[assets_df["name"] == asset, "pac"].iloc[0])
            existing = pac_view[pac_view["asset"] == asset]
            mode_default = existing["mode"].iloc[0] if not existing.empty else ("Auto" if asset_default > 0 else "No")
            amount_default = float(existing["amount"].iloc[0]) if not existing.empty else asset_default

            c1, c2, c3 = st.columns([2, 1, 1])

            with c1:
                st.markdown(f"**{asset}**  \nDefault PAC: {eur0(asset_default)}")

            with c2:
                mode = st.selectbox(
                    f"Mode - {asset}",
                    ["Auto", "Edited", "No"],
                    index=["Auto", "Edited", "No"].index(mode_default),
                    key=f"mode_{pac_month}_{asset}"
                )

            with c3:
                amount = st.number_input(
                    f"Amount - {asset}",
                    min_value=0.0,
                    value=float(amount_default),
                    step=10.0,
                    format="%.2f",
                    key=f"amount_{pac_month}_{asset}"
                )

            pac_updates.append({
                "month": pac_month,
                "asset": asset,
                "mode": mode,
                "amount": amount
            })

        save_pac = st.form_submit_button("Save PAC", use_container_width=True)

        if save_pac:
            pac_df = pac_df[pac_df["month"] != pac_month]
            pac_df = pd.concat([pac_df, pd.DataFrame(pac_updates)], ignore_index=True)
            pac_df["sort"] = pac_df["month"].apply(month_sort_value)
            pac_df = pac_df.sort_values(["sort", "asset"]).drop(columns="sort").reset_index(drop=True)

            for row in pac_updates:
                assets_df.loc[assets_df["name"] == row["asset"], "pac"] = float(row["amount"])

            st.session_state.pac_df = pac_df
            st.session_state.assets_df = assets_df
            st.success(f"PAC saved for {pac_month}")
            st.rerun()

with manual_tab:
    st.subheader("Add manual transaction")
    with st.form("manual_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            manual_month = st.selectbox("Month", options=MONTHS, index=MONTHS.index("Apr/26"))
        with c2:
            manual_asset = st.selectbox("ETF", options=etf_assets)
        with c3:
            manual_amount = st.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")

        add_manual = st.form_submit_button("Add transaction", use_container_width=True)
        if add_manual and manual_amount > 0:
            manual_df.loc[len(manual_df)] = [manual_month, manual_asset, float(manual_amount)]
            st.session_state.manual_df = manual_df
            st.success("Manual transaction added")
            st.rerun()

with asset_tab:
    st.subheader("Add ETF to portfolio")
    st.caption("Creates the ETF in Assets and lets you set first month end value and PAC immediately.")

    with st.form("add_etf_form"):
        c1, c2 = st.columns(2)
        with c1:
            new_name = st.text_input("ETF name")
            new_subcategory = st.selectbox("Subcategory", ["ETF Stock", "ETF Bond", "ETF Gold"])
            new_bucket = st.selectbox("Bucket", ["Stocks", "Defensive"])
        with c2:
            first_month = st.selectbox("First month", options=MONTHS, index=MONTHS.index("Apr/26"))
            first_end_value = st.number_input("First end value", min_value=0.0, step=100.0, format="%.2f")
            new_pac = st.number_input("Monthly PAC", min_value=0.0, step=10.0, format="%.2f")

        add_etf = st.form_submit_button("Add ETF", use_container_width=True)

        if add_etf:
            cleaned_name = new_name.strip()
            if cleaned_name == "":
                st.error("ETF name is required")
            elif cleaned_name in assets_df["name"].tolist():
                st.error("This ETF already exists")
            else:
                assets_df.loc[len(assets_df)] = {
                    "name": cleaned_name,
                    "category": "ETF",
                    "subcategory": new_subcategory,
                    "bucket": new_bucket,
                    "pac": float(new_pac),
                    "active": "Yes"
                }
                month_end_df.loc[len(month_end_df)] = {
                    "month": first_month,
                    "asset": cleaned_name,
                    "value": float(first_end_value)
                }

                for month in MONTHS:
                    if month_sort_value(month) >= month_sort_value(first_month):
                        pac_df.loc[len(pac_df)] = {
                            "month": month,
                            "asset": cleaned_name,
                            "mode": "Auto" if float(new_pac) > 0 else "No",
                            "amount": float(new_pac),
                        }

                st.session_state.assets_df = assets_df
                st.session_state.month_end_df = month_end_df
                st.session_state.pac_df = pac_df
                st.success(f"{cleaned_name} added to portfolio")
                st.rerun()
