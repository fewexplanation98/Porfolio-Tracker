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

st.markdown("""
<style>
.block-container {
    padding-top: 1.0rem;
    padding-bottom: 1.2rem;
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
.kpi-card {
    background: rgba(255,255,255,0.92);
    border: 1px solid rgba(15, 23, 42, 0.08);
    border-radius: 18px;
    padding: 14px 16px;
    min-height: 106px;
    box-shadow: 0 10px 28px rgba(2, 6, 23, 0.18);
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.kpi-label {
    font-size: 12px;
    color: #64748b;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 25px;
    line-height: 1.1;
    font-weight: 700;
    color: #0f172a;
    white-space: nowrap;
}
.kpi-pos {
    color: #16a34a;
}
.kpi-neg {
    color: #dc2626;
}
.spark-wrapper {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 10px 12px 6px 12px;
}
.spark-name {
    font-size: 13px;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 2px;
}
.spark-val-pos {
    font-size: 13px;
    font-weight: 700;
    color: #16a34a;
    margin-bottom: 4px;
}
.spark-val-neg {
    font-size: 13px;
    font-weight: 700;
    color: #dc2626;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

header_left, header_right = st.columns([8, 1.5])
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

st.write("")

p1, p2, p3 = st.columns([1, 1, 1.25])

with p1:
    st.subheader("ETF vs Savings")
    split_df = pd.DataFrame({
        "Type": ["ETF", "Savings"],
        "Value": [etf_total, savings_total]
    })
    split_df["Type"] = pd.Categorical(split_df["Type"], categories=["ETF", "Savings"], ordered=True)
    split_df = split_df.sort_values("Type")
    fig_split = px.pie(
        split_df,
        names="Type",
        values="Value",
        hole=0.64,
        color="Type",
        color_discrete_map={"ETF": "#1f2937", "Savings": "#9ca3af"}
    )
    fig_split.update_traces(textinfo="percent")
    fig_split.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, x=0.18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_split, use_container_width=True)

with p2:
    st.subheader("ETF Stock vs Defensive")
    bucket_df = summary_df[summary_df["Category"] == "ETF"].groupby("Bucket")["End Value"].sum().reset_index()
    bucket_df["Bucket"] = pd.Categorical(bucket_df["Bucket"], categories=["Stocks", "Defensive"], ordered=True)
    bucket_df = bucket_df.sort_values("Bucket")
    fig_bucket = px.pie(
        bucket_df,
        names="Bucket",
        values="End Value",
        hole=0.64,
        color="Bucket",
        color_discrete_map={"Stocks": "#334155", "Defensive": "#94a3b8"}
    )
    fig_bucket.update_traces(textinfo="percent")
    fig_bucket.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, x=0.10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bucket, use_container_width=True)

with p3:
    st.subheader("ETF Split")
    pie_df = summary_df[(summary_df["Category"] == "ETF") & (summary_df["End Value"] > 0)][["Asset", "End Value"]]
    fig_pie = px.pie(pie_df, names="Asset", values="End Value", hole=0.64)
    fig_pie.update_traces(textinfo="percent")
    fig_pie.update_layout(
        height=260,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.24, x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Portfolio Trend MoM")

trend_rows = []
for month in MONTHS[: selected_idx + 1]:
    total = month_end_df.loc[month_end_df["month"] == month, "value"].sum()
    savings = month_end_df.loc[
        (month_end_df["month"] == month) & (month_end_df["asset"] == "Savings"),
        "value"
    ].sum()
    etf = total - savings
    trend_rows.append({"Month": month, "Savings": savings, "ETF": etf, "Total": total})

trend_df = pd.DataFrame(trend_rows)

if not trend_df.empty:
    line_color = "#16a34a"
    if len(trend_df) >= 2 and trend_df.iloc[-1]["Total"] < trend_df.iloc[-2]["Total"]:
        line_color = "#dc2626"

    fig_combo = go.Figure()

    fig_combo.add_bar(
        x=trend_df["Month"],
        y=trend_df["ETF"],
        name="ETF",
        marker_color="#1f2937",
        width=0.34
    )

    fig_combo.add_bar(
        x=trend_df["Month"],
        y=trend_df["Savings"],
        name="Savings",
        marker_color="#9ca3af",
        width=0.34
    )

    fig_combo.add_trace(
        go.Scatter(
            x=trend_df["Month"],
            y=trend_df["Total"],
            mode="lines+markers+text",
            name="Portfolio Total",
            line=dict(color=line_color, width=3),
            marker=dict(size=7, color=line_color),
            text=[eur0(v) for v in trend_df["Total"]],
            textposition="top center"
        )
    )

    fig_combo.update_layout(
        barmode="stack",
        height=430,
        bargap=0.58,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=1.08, x=0),
        yaxis_title="",
        xaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)"
    )
    fig_combo.update_yaxes(showgrid=True, gridcolor="rgba(203,213,225,0.18)", tickformat=",.0f")
    fig_combo.update_xaxes(showgrid=False)

    st.plotly_chart(fig_combo, use_container_width=True)

st.subheader("ETF Monthly Performance")

perf_rows = []
months_3m = MONTHS[max(0, selected_idx - 2): selected_idx + 1]

for asset in etf_assets:
    current_row = summary_df[summary_df["Asset"] == asset].iloc[0]
    current_perf = current_row["Perf %"]

    spark_perf = []
    spark_months = []

    for i in range(1, len(months_3m)):
        m = months_3m[i]
        prev = months_3m[i - 1]

        end = month_end_map.get((m, asset), 0)
        prev_end = month_end_map.get((prev, asset), 0)
        flow = pac_map.get((m, asset), 0) + manual_map.get((m, asset), 0)

        if prev_end > 0 and end > 0:
            pnl = end - prev_end - flow
            base = prev_end + flow / 2
            if base != 0:
                spark_perf.append(pnl / base * 100)
                spark_months.append(m)

    perf_rows.append({
        "asset": asset,
        "current_perf": current_perf,
        "spark_months": spark_months,
        "spark_perf": spark_perf
    })

perf_rows = sorted(
    perf_rows,
    key=lambda x: -999 if pd.isna(x["current_perf"]) else x["current_perf"],
    reverse=True
)

for i in range(0, len(perf_rows), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j >= len(perf_rows):
            continue

        row = perf_rows[i + j]
        asset = row["asset"]
        current_perf = row["current_perf"]
        spark_months = row["spark_months"]
        spark_perf = row["spark_perf"]

        with cols[j]:
            st.markdown('<div class="spark-wrapper">', unsafe_allow_html=True)

            top_left, top_right = st.columns([3.3, 1])
            with top_left:
                st.markdown(f'<div class="spark-name">{asset}</div>', unsafe_allow_html=True)
            with top_right:
                if pd.isna(current_perf):
                    st.markdown('<div class="spark-val-neg">-</div>', unsafe_allow_html=True)
                else:
                    cls = "spark-val-pos" if current_perf >= 0 else "spark-val-neg"
                    st.markdown(f'<div class="{cls}">{pct1(current_perf)}</div>', unsafe_allow_html=True)

            if len(spark_perf) > 0:
                spark_df = pd.DataFrame({"Month": spark_months, "Perf": spark_perf})
                color = "#16a34a" if (spark_perf[-1] >= 0) else "#dc2626"

                fig_spark = go.Figure()
                fig_spark.add_trace(
                    go.Scatter(
                        x=spark_df["Month"],
                        y=spark_df["Perf"],
                        mode="lines",
                        line=dict(color=color, width=2.2),
                        fill="tozeroy",
                        fillcolor="rgba(34,197,94,0.10)" if color == "#16a34a" else "rgba(239,68,68,0.10)",
                        showlegend=False
                    )
                )
                fig_spark.update_layout(
                    height=70,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(visible=False),
                    yaxis=dict(visible=False),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig_spark, use_container_width=True, config={"displayModeBar": False})
            else:
                st.caption("No 3M data")

            st.markdown('</div>', unsafe_allow_html=True)

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
    for i in range(1, len(months_to_show)):
        m = months_to_show[i]
        prev = months_to_show[i - 1]

        end = month_end_map.get((m, asset), 0)
        prev_end = month_end_map.get((prev, asset), 0)
        flow = pac_map.get((m, asset), 0) + manual_map.get((m, asset), 0)

        if prev_end > 0 and end > 0:
            pnl = end - prev_end - flow
            base = prev_end + flow / 2
            if base != 0:
                perf = pnl / base * 100
                mom_data.append({
                    "Month": m,
                    "Asset": asset,
                    "Perf": perf
                })

mom_df = pd.DataFrame(mom_data)

if not mom_df.empty:
    fig_track = px.line(
        mom_df,
        x="Month",
        y="Perf",
        color="Asset",
        markers=True
    )
    fig_track.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        yaxis_title="%",
        xaxis_title="",
        legend=dict(orientation="h", y=-0.18, x=0)
    )
    fig_track.update_yaxes(showgrid=True, gridcolor="rgba(203,213,225,0.18)")
    st.plotly_chart(fig_track, use_container_width=True)

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
            updated_rows = []
            for asset, value in month_end_inputs.items():
                updated_rows.append({"month": draft_month, "asset": asset, "value": float(value)})

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
                    "value": float(first_end_value),
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

with st.expander("Data tables"):
    st.write("Assets")
    st.dataframe(assets_df, use_container_width=True, hide_index=True)

    st.write("Month End")
    month_end_show = month_end_df.copy()
    month_end_show["sort"] = month_end_show["month"].apply(month_sort_value)
    month_end_show = month_end_show.sort_values(["sort", "asset"]).drop(columns="sort")
    st.dataframe(month_end_show, use_container_width=True, hide_index=True)

    st.write("PAC")
    pac_show = pac_df.copy()
    pac_show["sort"] = pac_show["month"].apply(month_sort_value)
    pac_show = pac_show.sort_values(["sort", "asset"]).drop(columns="sort")
    st.dataframe(pac_show, use_container_width=True, hide_index=True)

    st.write("Manual Transactions")
    manual_show = manual_df.copy()
    if not manual_show.empty:
        manual_show["sort"] = manual_show["month"].apply(month_sort_value)
        manual_show = manual_show.sort_values(["sort", "asset"]).drop(columns="sort")
    st.dataframe(manual_show, use_container_width=True, hide_index=True)
