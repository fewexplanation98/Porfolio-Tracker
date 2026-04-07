import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Portfolio Tracker', page_icon='📈', layout='wide')

ASSETS = [
    {'name': 'Savings', 'category': 'Savings', 'subcategory': 'Savings TR', 'bucket': 'Savings', 'pac': 0},
    {'name': 'Core MSCI World', 'category': 'ETF', 'subcategory': 'ETF Stock', 'bucket': 'Stocks', 'pac': 640},
    {'name': 'AI & Big Data', 'category': 'ETF', 'subcategory': 'ETF Stock', 'bucket': 'Stocks', 'pac': 0},
    {'name': 'Physical Gold', 'category': 'ETF', 'subcategory': 'ETF Gold', 'bucket': 'Defensive', 'pac': 220},
    {'name': 'Global Gov Bond', 'category': 'ETF', 'subcategory': 'ETF Bond', 'bucket': 'Defensive', 'pac': 52},
    {'name': 'Core EUR Corp Bond', 'category': 'ETF', 'subcategory': 'ETF Bond', 'bucket': 'Defensive', 'pac': 54},
    {'name': 'MSCI World Value', 'category': 'ETF', 'subcategory': 'ETF Stock', 'bucket': 'Stocks', 'pac': 180},
    {'name': 'MSCI EM', 'category': 'ETF', 'subcategory': 'ETF Stock', 'bucket': 'Stocks', 'pac': 400},
    {'name': 'Defence Tech', 'category': 'ETF', 'subcategory': 'ETF Stock', 'bucket': 'Stocks', 'pac': 0},
]

MONTH_END_SEED = [
    ('Oct/25', 'Savings', 34010.01), ('Oct/25', 'Core MSCI World', 11058), ('Oct/25', 'AI & Big Data', 3265),
    ('Oct/25', 'Physical Gold', 1792), ('Oct/25', 'Global Gov Bond', 1456), ('Oct/25', 'Core EUR Corp Bond', 1456),
    ('Oct/25', 'MSCI World Value', 1439), ('Oct/25', 'MSCI EM', 1233), ('Oct/25', 'Defence Tech', 483.20),
    ('Nov/25', 'Savings', 35690.22), ('Nov/25', 'Core MSCI World', 11303), ('Nov/25', 'AI & Big Data', 3177),
    ('Nov/25', 'Physical Gold', 1875), ('Nov/25', 'Global Gov Bond', 1470), ('Nov/25', 'Core EUR Corp Bond', 1478),
    ('Nov/25', 'MSCI World Value', 1499), ('Nov/25', 'MSCI EM', 1225), ('Nov/25', 'Defence Tech', 383.76),
    ('Dec/25', 'Savings', 37889.16), ('Dec/25', 'Core MSCI World', 11866), ('Dec/25', 'AI & Big Data', 3256),
    ('Dec/25', 'Physical Gold', 2001), ('Dec/25', 'Global Gov Bond', 1547), ('Dec/25', 'Core EUR Corp Bond', 1534),
    ('Dec/25', 'MSCI World Value', 1651), ('Dec/25', 'MSCI EM', 1306), ('Dec/25', 'Defence Tech', 402.89),
    ('Jan/26', 'Savings', 38095), ('Jan/26', 'Core MSCI World', 12365), ('Jan/26', 'AI & Big Data', 3215),
    ('Jan/26', 'Physical Gold', 2214), ('Jan/26', 'Global Gov Bond', 1568), ('Jan/26', 'Core EUR Corp Bond', 1592),
    ('Jan/26', 'MSCI World Value', 1824), ('Jan/26', 'MSCI EM', 1419), ('Jan/26', 'Defence Tech', 452.33),
    ('Feb/26', 'Savings', 37801), ('Feb/26', 'Core MSCI World', 13001), ('Feb/26', 'AI & Big Data', 3108),
    ('Feb/26', 'Physical Gold', 2540), ('Feb/26', 'Global Gov Bond', 1640), ('Feb/26', 'Core EUR Corp Bond', 1649),
    ('Feb/26', 'MSCI World Value', 2007), ('Feb/26', 'MSCI EM', 1544), ('Feb/26', 'Defence Tech', 450.32),
    ('Mar/26', 'Savings', 39883), ('Mar/26', 'Core MSCI World', 13914), ('Mar/26', 'AI & Big Data', 2970),
    ('Mar/26', 'Physical Gold', 2493), ('Mar/26', 'Global Gov Bond', 1666), ('Mar/26', 'Core EUR Corp Bond', 1679),
    ('Mar/26', 'MSCI World Value', 2387), ('Mar/26', 'MSCI EM', 2033), ('Mar/26', 'Defence Tech', 439.71),
]

MANUAL_SEED = [
    ('Oct/25', 'Core MSCI World', 690.40), ('Oct/25', 'AI & Big Data', 101), ('Oct/25', 'Physical Gold', 70),
    ('Oct/25', 'Global Gov Bond', 52), ('Oct/25', 'Core EUR Corp Bond', 54), ('Oct/25', 'MSCI World Value', 196.99),
    ('Oct/25', 'MSCI EM', 44), ('Nov/25', 'Core MSCI World', 486), ('Nov/25', 'Physical Gold', 70),
    ('Nov/25', 'Global Gov Bond', 52), ('Nov/25', 'Core EUR Corp Bond', 54), ('Nov/25', 'MSCI World Value', 96),
    ('Nov/25', 'MSCI EM', 44), ('Dec/25', 'Core MSCI World', 486), ('Dec/25', 'Physical Gold', 70),
    ('Dec/25', 'Global Gov Bond', 52), ('Dec/25', 'Core EUR Corp Bond', 54), ('Dec/25', 'MSCI World Value', 96),
    ('Dec/25', 'MSCI EM', 44), ('Jan/26', 'Core MSCI World', 486), ('Jan/26', 'Physical Gold', 70),
    ('Jan/26', 'Global Gov Bond', 52), ('Jan/26', 'Core EUR Corp Bond', 54), ('Jan/26', 'MSCI World Value', 96),
    ('Jan/26', 'MSCI EM', 44), ('Feb/26', 'Core MSCI World', 486), ('Feb/26', 'Physical Gold', 70),
    ('Feb/26', 'Global Gov Bond', 52), ('Feb/26', 'Core EUR Corp Bond', 54), ('Feb/26', 'MSCI World Value', 96),
    ('Feb/26', 'MSCI EM', 44), ('Mar/26', 'Core MSCI World', 1539.76), ('Mar/26', 'Physical Gold', 220.99),
    ('Mar/26', 'Global Gov Bond', 52), ('Mar/26', 'Core EUR Corp Bond', 54), ('Mar/26', 'MSCI World Value', 497),
    ('Mar/26', 'MSCI EM', 645.99),
]

MONTHS = [
    'Oct/25', 'Nov/25', 'Dec/25', 'Jan/26', 'Feb/26', 'Mar/26',
    'Apr/26', 'May/26', 'Jun/26', 'Jul/26', 'Aug/26', 'Sep/26',
    'Oct/26', 'Nov/26', 'Dec/26'
]

MONTH_MAP = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}


def month_sort_value(label: str) -> int:
    month, year = label.split('/')
    return (2000 + int(year)) * 100 + MONTH_MAP[month]


def eur(value: float) -> str:
    sign = '-' if value < 0 else ''
    value = abs(float(value))
    s = f'{value:,.2f}'
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    return f'{sign}€ {s}'


def seed_data():
    assets_df = pd.DataFrame(ASSETS)

    month_end_df = pd.DataFrame(MONTH_END_SEED, columns=['month', 'asset', 'value'])
    manual_df = pd.DataFrame(MANUAL_SEED, columns=['month', 'asset', 'amount'])

    pac_df = assets_df[assets_df['category'] == 'ETF'][['name', 'pac']].copy()
    pac_df.columns = ['asset', 'amount']
    pac_df['month'] = 'Apr/26'
    pac_df['mode'] = pac_df['amount'].apply(lambda x: 'Auto' if x > 0 else 'No')
    pac_df = pac_df[['month', 'asset', 'mode', 'amount']]

    return assets_df, month_end_df, manual_df, pac_df


if 'assets_df' not in st.session_state:
    assets_df, month_end_df, manual_df, pac_df = seed_data()
    st.session_state.assets_df = assets_df
    st.session_state.month_end_df = month_end_df
    st.session_state.manual_df = manual_df
    st.session_state.pac_df = pac_df

assets_df = st.session_state.assets_df.copy()
month_end_df = st.session_state.month_end_df.copy()
manual_df = st.session_state.manual_df.copy()
pac_df = st.session_state.pac_df.copy()

all_assets = assets_df['name'].tolist()
etf_assets = assets_df.loc[assets_df['category'] == 'ETF', 'name'].tolist()

st.title('Portfolio Tracker')
st.caption('Month end update, PAC confirmation, manual transactions and add ETF')

selected_month = st.selectbox('Selected month', options=MONTHS, index=MONTHS.index('Mar/26'))

with st.sidebar:
    st.subheader('Quick actions')
    st.write('1. Confirm PAC')
    st.write('2. Add month end')
    st.write('3. Add manual extra buy')
    st.write('4. Add new ETF')

# Auto-create PAC rows for all future months based on Assets defaults
for month in MONTHS:
    if month_sort_value(month) >= month_sort_value('Apr/26'):
        for _, row in assets_df[assets_df['category'] == 'ETF'].iterrows():
            asset = row['name']
            default_amount = float(row['pac'])
            exists = ((pac_df['month'] == month) & (pac_df['asset'] == asset)).any()
            if not exists:
                pac_df.loc[len(pac_df)] = [
                    month,
                    asset,
                    'Auto' if default_amount > 0 else 'No',
                    default_amount
                ]

st.session_state.pac_df = pac_df

month_end_map = {(r.month, r.asset): float(r.value) for r in month_end_df.itertuples(index=False)}
manual_map = manual_df.groupby(['month', 'asset'], dropna=False)['amount'].sum().to_dict() if not manual_df.empty else {}

pac_effective = pac_df.copy()
pac_effective['effective_amount'] = pac_effective.apply(
    lambda r: 0 if r['mode'] == 'No' else float(r['amount']),
    axis=1
)
pac_map = pac_effective.groupby(['month', 'asset'])['effective_amount'].sum().to_dict() if not pac_effective.empty else {}

selected_idx = MONTHS.index(selected_month)
prev_month = MONTHS[selected_idx - 1] if selected_idx > 0 else None

rows = []
for _, asset_row in assets_df.iterrows():
    asset = asset_row['name']
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
        'Asset': asset,
        'Category': asset_row['category'],
        'Bucket': asset_row['bucket'],
        'End Value': end_value,
        'Prev End': prev_end,
        'PAC Flow': pac_flow,
        'Manual Flow': manual_flow,
        'Total Flow': total_flow,
        'PnL': pnl,
        'Perf %': perf_pct,
    })

summary_df = pd.DataFrame(rows)

portfolio_total = float(summary_df['End Value'].sum())
savings_total = float(summary_df.loc[summary_df['Category'] == 'Savings', 'End Value'].sum())
etf_total = portfolio_total - savings_total
monthly_flow = float(summary_df['Total Flow'].sum())
etf_pnl = float(summary_df.loc[(summary_df['Category'] == 'ETF') & summary_df['PnL'].notna(), 'PnL'].sum())

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('Portfolio Total', eur(portfolio_total))
c2.metric('ETF Total', eur(etf_total))
c3.metric('Savings', eur(savings_total))
c4.metric('Monthly Flow', eur(monthly_flow))
c5.metric('ETF PnL', eur(etf_pnl))

trend_rows = []
for month in MONTHS[: selected_idx + 1]:
    total = month_end_df.loc[month_end_df['month'] == month, 'value'].sum()
    savings = month_end_df.loc[
        (month_end_df['month'] == month) & (month_end_df['asset'] == 'Savings'),
        'value'
    ].sum()
    trend_rows.append({'Month': month, 'Total': total, 'ETF': total - savings, 'Savings': savings})

trend_df = pd.DataFrame(trend_rows)

left, right = st.columns([2, 1])

with left:
    st.subheader('Portfolio trend')
    if not trend_df.empty:
        trend_long = trend_df.melt(
            id_vars='Month',
            value_vars=['Total', 'ETF', 'Savings'],
            var_name='Series',
            value_name='Value'
        )
        fig_trend = px.line(trend_long, x='Month', y='Value', color='Series', markers=True)
        fig_trend.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_trend, use_container_width=True)

with right:
    st.subheader('ETF split')
    pie_df = summary_df[
        (summary_df['Category'] == 'ETF') & (summary_df['End Value'] > 0)
    ][['Asset', 'End Value']]
    if not pie_df.empty:
        fig_pie = px.pie(pie_df, names='Asset', values='End Value', hole=0.55)
        fig_pie.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

left2, right2 = st.columns([2, 1])

with left2:
    st.subheader('ETF monthly performance')
    perf_df = summary_df[
        (summary_df['Category'] == 'ETF') & summary_df['Perf %'].notna()
    ][['Asset', 'Perf %']].copy()

    if not perf_df.empty:
        perf_df['Color'] = perf_df['Perf %'].apply(lambda x: 'Positive' if x >= 0 else 'Negative')
        fig_bar = px.bar(
            perf_df,
            x='Asset',
            y='Perf %',
            color='Color',
            color_discrete_map={'Positive': '#3b82f6', 'Negative': '#ef4444'}
        )
        fig_bar.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

with right2:
    st.subheader('Current month detail')
    detail_df = summary_df[summary_df['Category'] == 'ETF'][
        ['Asset', 'End Value', 'Total Flow', 'PnL', 'Perf %']
    ].copy()

    if not detail_df.empty:
        detail_df['End Value'] = detail_df['End Value'].apply(eur)
        detail_df['Total Flow'] = detail_df['Total Flow'].apply(eur)
        detail_df['PnL'] = detail_df['PnL'].apply(lambda x: '' if pd.isna(x) else eur(x))
        detail_df['Perf %'] = detail_df['Perf %'].apply(lambda x: '' if pd.isna(x) else f'{x:.1f}%')
        st.dataframe(detail_df, use_container_width=True, hide_index=True)

st.divider()

update_tab, pac_tab, manual_tab, asset_tab = st.tabs(
    ['Update Month End', 'Confirm PAC', 'Manual Transaction', 'Add ETF']
)

with update_tab:
    st.subheader('Insert month end values')
    draft_month = st.selectbox('Month to update', options=MONTHS, index=MONTHS.index('Apr/26'), key='draft_month_end')

    with st.form('month_end_form'):
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
                    format='%.2f',
                    key=f'month_end_{draft_month}_{asset}'
                )

        save_month_end = st.form_submit_button('Save month end', use_container_width=True)

        if save_month_end:
            updated_rows = []
            for asset, value in month_end_inputs.items():
                updated_rows.append({'month': draft_month, 'asset': asset, 'value': float(value)})

            month_end_df = month_end_df[month_end_df['month'] != draft_month]
            month_end_df = pd.concat([month_end_df, pd.DataFrame(updated_rows)], ignore_index=True)
            month_end_df['sort'] = month_end_df['month'].apply(month_sort_value)
            month_end_df = month_end_df.sort_values(['sort', 'asset']).drop(columns='sort').reset_index(drop=True)

            st.session_state.month_end_df = month_end_df
            st.success(f'Month end saved for {draft_month}')
            st.rerun()

with pac_tab:
    st.subheader('Confirm monthly PAC')
    pac_month = st.selectbox('PAC month', options=MONTHS, index=MONTHS.index('Apr/26'), key='draft_pac_month')
    pac_view = pac_df[pac_df['month'] == pac_month].copy().sort_values('asset')

    with st.form('pac_form'):
        pac_updates = []

        for asset in etf_assets:
            asset_default = float(assets_df.loc[assets_df['name'] == asset, 'pac'].iloc[0])
            existing = pac_view[pac_view['asset'] == asset]

            mode_default = existing['mode'].iloc[0] if not existing.empty else ('Auto' if asset_default > 0 else 'No')
            amount_default = float(existing['amount'].iloc[0]) if not existing.empty else asset_default

            c1, c2, c3 = st.columns([2, 1, 1])

            with c1:
                st.markdown(f'**{asset}**  \nDefault PAC: {eur(asset_default)}')

            with c2:
                mode = st.selectbox(
                    f'Mode - {asset}',
                    ['Auto', 'Edited', 'No'],
                    index=['Auto', 'Edited', 'No'].index(mode_default),
                    key=f'mode_{pac_month}_{asset}'
                )

            with c3:
                amount = st.number_input(
                    f'Amount - {asset}',
                    min_value=0.0,
                    value=float(amount_default),
                    step=50.0,
                    format='%.2f',
                    key=f'amount_{pac_month}_{asset}'
                )

            pac_updates.append({
                'month': pac_month,
                'asset': asset,
                'mode': mode,
                'amount': amount
            })

        save_pac = st.form_submit_button('Save PAC', use_container_width=True)

        if save_pac:
            pac_df = pac_df[pac_df['month'] != pac_month]
            pac_df = pd.concat([pac_df, pd.DataFrame(pac_updates)], ignore_index=True)
            pac_df['sort'] = pac_df['month'].apply(month_sort_value)
            pac_df = pac_df.sort_values(['sort', 'asset']).drop(columns='sort').reset_index(drop=True)

            # Update also the default PAC in Assets for that ETF if current mode is Auto/Edited
            for row in pac_updates:
                assets_df.loc[assets_df['name'] == row['asset'], 'pac'] = float(row['amount'])

            st.session_state.pac_df = pac_df
            st.session_state.assets_df = assets_df
            st.success(f'PAC saved for {pac_month}')
            st.rerun()

with manual_tab:
    st.subheader('Add manual transaction')

    with st.form('manual_form'):
        c1, c2, c3 = st.columns(3)

        with c1:
            manual_month = st.selectbox('Month', options=MONTHS, index=MONTHS.index('Apr/26'))

        with c2:
            manual_asset = st.selectbox('ETF', options=etf_assets)

        with c3:
            manual_amount = st.number_input('Amount', min_value=0.0, step=50.0, format='%.2f')

        add_manual = st.form_submit_button('Add transaction', use_container_width=True)

        if add_manual and manual_amount > 0:
            manual_df.loc[len(manual_df)] = [manual_month, manual_asset, float(manual_amount)]
            st.session_state.manual_df = manual_df
            st.success('Manual transaction added')
            st.rerun()

with asset_tab:
    st.subheader('Add ETF to portfolio')
    st.caption('Creates the ETF in Assets and lets you set first month end value and PAC immediately.')

    with st.form('add_etf_form'):
        c1, c2 = st.columns(2)

        with c1:
            new_name = st.text_input('ETF name')
            new_subcategory = st.selectbox('Subcategory', ['ETF Stock', 'ETF Bond', 'ETF Gold'])
            new_bucket = st.selectbox('Bucket', ['Stocks', 'Defensive'])

        with c2:
            first_month = st.selectbox('First month', options=MONTHS, index=MONTHS.index('Apr/26'))
            first_end_value = st.number_input('First end value', min_value=0.0, step=100.0, format='%.2f')
            new_pac = st.number_input('Monthly PAC', min_value=0.0, step=50.0, format='%.2f')

        add_etf = st.form_submit_button('Add ETF', use_container_width=True)

        if add_etf:
            cleaned_name = new_name.strip()

            if cleaned_name == '':
                st.error('ETF name is required')
            elif cleaned_name in assets_df['name'].tolist():
                st.error('This ETF already exists')
            else:
                assets_df.loc[len(assets_df)] = {
                    'name': cleaned_name,
                    'category': 'ETF',
                    'subcategory': new_subcategory,
                    'bucket': new_bucket,
                    'pac': float(new_pac),
                }

                month_end_df.loc[len(month_end_df)] = {
                    'month': first_month,
                    'asset': cleaned_name,
                    'value': float(first_end_value),
                }

                for month in MONTHS:
                    if month_sort_value(month) >= month_sort_value(first_month):
                        pac_df.loc[len(pac_df)] = {
                            'month': month,
                            'asset': cleaned_name,
                            'mode': 'Auto' if float(new_pac) > 0 else 'No',
                            'amount': float(new_pac),
                        }

                st.session_state.assets_df = assets_df
                st.session_state.month_end_df = month_end_df
                st.session_state.pac_df = pac_df
                st.success(f'{cleaned_name} added to portfolio')
                st.rerun()

st.divider()

with st.expander('Data tables'):
    st.write('Assets')
    st.dataframe(assets_df, use_container_width=True, hide_index=True)

    st.write('Month End')
    month_end_show = month_end_df.copy()
    month_end_show['sort'] = month_end_show['month'].apply(month_sort_value)
    month_end_show = month_end_show.sort_values(['sort', 'asset']).drop(columns='sort')
    st.dataframe(month_end_show, use_container_width=True, hide_index=True)

    st.write('PAC')
    pac_show = pac_df.copy()
    pac_show['sort'] = pac_show['month'].apply(month_sort_value)
    pac_show = pac_show.sort_values(['sort', 'asset']).drop(columns='sort')
    st.dataframe(pac_show, use_container_width=True, hide_index=True)

    st.write('Manual Transactions')
    manual_show = manual_df.copy()
    if not manual_show.empty:
        manual_show['sort'] = manual_show['month'].apply(month_sort_value)
        manual_show = manual_show.sort_values(['sort', 'asset']).drop(columns='sort')
    st.dataframe(manual_show, use_container_width=True, hide_index=True)
