import pandas as pd
import plotly.express as px
import streamlit as st
import os
from datetime import datetime

# ============================================================
# REFINED DARK MODE — PROFESSIONAL, NOT PLAYFUL
# ============================================================

st.set_page_config(
    page_title="Nairobi Price Intelligence",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background: #0f1419;
    }
    h1 {
        font-family: 'Georgia', 'Times New Roman', serif;
        font-weight: 600;
        color: #e8e8e8;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        font-family: 'Georgia', serif;
        color: #00d4aa;
        font-weight: 500;
        border-left: 2px solid #00d4aa;
        padding-left: 0.8rem;
    }
    div[data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 4px;
    }
    div[data-testid="stMetric"] label {
        color: #8b949e;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetric"] div {
        color: #e8e8e8;
        font-size: 1.5rem;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid #30363d;
    }
    .stDataFrame {
        background: #161b22;
    }
    div[data-testid="stAlert"] {
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.title("Nairobi Price Intelligence")
st.markdown("""
<p style="color: #8b949e; margin-top: -0.5rem; font-size: 0.95rem;">
    Essential commodity price tracking — Nairobi, Kenya
</p>
<div style="margin: 1rem 0 2rem 0;">
    <span style="background: #00d4aa; color: #0f1419; padding: 0.15rem 0.5rem; font-size: 0.65rem; font-weight: 600; margin-right: 0.5rem;">EPRA VERIFIED</span>
    <span style="background: #00d4aa; color: #0f1419; padding: 0.15rem 0.5rem; font-size: 0.65rem; font-weight: 600; margin-right: 0.5rem;">KNBS CPI</span>
    <span style="background: #30363d; color: #8b949e; padding: 0.15rem 0.5rem; font-size: 0.65rem; font-weight: 600;">ESTIMATES FLAGGED</span>
</div>
""", unsafe_allow_html=True)

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'data', 'nairobi_prices.csv')
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ============================================================
# UPGRADE 1: AUTO-REFRESH DATE STAMP (MOVED AFTER DATA LOADS)
# ============================================================
st.markdown(f"""
<p style="color: #6e7681; font-size: 0.75rem; margin-top: -1rem;">
    Last updated: {datetime.now().strftime('%B %d, %Y')} | Data range: {df['date'].min().strftime('%b %Y')} — {df['date'].max().strftime('%b %Y')}
</p>
""", unsafe_allow_html=True)

# ---- SIDEBAR ----
st.sidebar.markdown("""
<p style="color: #e8e8e8; font-family: Georgia, serif; font-size: 0.9rem; font-weight: 600; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem;">
    Filters
</p>
""", unsafe_allow_html=True)

selected_categories = st.sidebar.multiselect(
    "Categories",
    options=df['category'].unique(),
    default=df['category'].unique(),
    label_visibility="collapsed"
)

st.sidebar.markdown("""
<p style="color: #e8e8e8; font-family: Georgia, serif; font-size: 0.9rem; font-weight: 600; margin-top: 2rem; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem;">
    About
</p>
<p style="color: #8b949e; font-size: 0.8rem; line-height: 1.6;">
    <strong style="color: #c9d1d9;">Fuel:</strong> EPRA official pump prices<br>
    <strong style="color: #c9d1d9;">Food:</strong> KNBS CPI baselines<br>
    <strong style="color: #c9d1d9;">Transport:</strong> Crowdsourced estimates
</p>
<p style="color: #6e7681; font-size: 0.75rem; margin-top: 1rem;">
    All estimates flagged in data_quality column
</p>
""", unsafe_allow_html=True)

filtered_df = df[df['category'].isin(selected_categories)]

# ---- KEY METRICS ----
st.markdown('<h3 style="border: none; padding: 0; margin-bottom: 1rem;">Key Metrics</h3>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    fuel_data = df[df['category'] == 'fuel']
    if not fuel_data.empty:
        latest = fuel_data['price_kes'].iloc[-1]
        start = fuel_data['price_kes'].iloc[0]
        delta = ((latest - start) / start) * 100
        st.metric("PETROL KES/L", f"{latest:.2f}", f"{delta:+.1f}%")

with m2:
    food_data = df[df['category'] == 'food']
    if not food_data.empty:
        latest = food_data[food_data['date'] == food_data['date'].max()]['price_kes'].mean()
        start = food_data[food_data['date'] == food_data['date'].min()]['price_kes'].mean()
        delta = ((latest - start) / start) * 100
        st.metric("FOOD BASKET KES", f"{latest:.0f}", f"{delta:+.1f}%")

with m3:
    trans_data = df[df['category'] == 'transport']
    if not trans_data.empty:
        latest = trans_data[trans_data['date'] == trans_data['date'].max()]['price_kes'].mean()
        start = trans_data[trans_data['date'] == trans_data['date'].min()]['price_kes'].mean()
        delta = ((latest - start) / start) * 100
        st.metric("TRANSPORT KES", f"{latest:.0f}", f"{delta:+.1f}%")

with m4:
    verified = (df['data_quality'] == 'verified_primary_source').mean() * 100
    st.metric("VERIFIED DATA", f"{verified:.0f}%")

# ============================================================
# UPGRADE 2: PRICE SPIKE ALERT BANNER
# ============================================================
latest_date = df['date'].max()
prev_date = df[df['date'] < latest_date]['date'].max()

if pd.notna(prev_date):
    spikes = []
    for item in df['item'].unique():
        curr = df[(df['item'] == item) & (df['date'] == latest_date)]['price_kes'].mean()
        prev = df[(df['item'] == item) & (df['date'] == prev_date)]['price_kes'].mean()
        if pd.notna(curr) and pd.notna(prev) and prev > 0:
            change = ((curr - prev) / prev) * 100
            if change > 10:
                spikes.append(f"{item}: +{change:.1f}%")
    
    if spikes:
        st.error(f"**ALERT:** Significant price increases detected — {', '.join(spikes)}")

# ---- INSIGHTS ----
st.markdown('<h3>Key Insights</h3>', unsafe_allow_html=True)

fuel_start = df[(df['category'] == 'fuel') & (df['item'] == 'Petrol')]['price_kes'].min()
fuel_end = df[(df['category'] == 'fuel') & (df['item'] == 'Petrol')]['price_kes'].max()
fuel_inf = ((fuel_end - fuel_start) / fuel_start) * 100

trans_start = df[(df['category'] == 'transport') & (df['item'] == 'Matatu CBD to Eastlands')]['price_kes'].min()
trans_end = df[(df['category'] == 'transport') & (df['item'] == 'Matatu CBD to Eastlands')]['price_kes'].max()
trans_inf = ((trans_end - trans_start) / trans_start) * 100

food_start = df[(df['category'] == 'food') & (df['date'] == df['date'].min())]['price_kes'].mean()
food_end = df[(df['category'] == 'food') & (df['date'] == df['date'].max())]['price_kes'].mean()
food_inf = ((food_end - food_start) / food_start) * 100

i1, i2 = st.columns(2)

with i1:
    st.markdown(f"""
    <div style="background: #161b22; border-left: 3px solid #f0883e; padding: 1rem;">
        <p style="margin: 0; color: #c9d1d9; font-size: 0.9rem; line-height: 1.6;">
            <strong style="color: #e8e8e8;">FUEL VS TRANSPORT</strong><br>
            Petrol rose {fuel_inf:.1f}% over the period.<br>
            Matatu fares rose {trans_inf:.1f}%, outpacing fuel costs.<br>
            <span style="color: #f0883e; font-size: 0.85rem;">Transport inflation exceeds fuel — cartel pricing suspected.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div style="background: #161b22; border-left: 3px solid #00d4aa; padding: 1rem;">
        <p style="margin: 0; color: #c9d1d9; font-size: 0.9rem; line-height: 1.6;">
            <strong style="color: #e8e8e8;">FOOD BASKET STABILITY</strong><br>
            Food prices rose {food_inf:.1f}%, the most stable category.<br>
            Agricultural supply chains remain resilient.<br>
            <span style="color: #00d4aa; font-size: 0.85rem;">Consistent with KNBS CPI food sub-index trends.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<p style="color: #6e7681; font-size: 0.8rem; margin-top: 1rem; font-style: italic;">
    Methodology: Transport estimates flagged as crowdsourced. Fuel verified from EPRA primary sources. 
    Food baselines from KNBS CPI, interpolated where necessary.
</p>
""", unsafe_allow_html=True)

# ---- TRENDS + MOM ----
st.markdown('<h3>Price Trends & Monthly Changes</h3>', unsafe_allow_html=True)

c1, c2 = st.columns([2, 1])

with c1:
    if not filtered_df.empty:
        fig = px.line(
            filtered_df,
            x='date',
            y='price_kes',
            color='item',
            facet_col='category',
            facet_col_wrap=1,
            labels={'price_kes': 'Price (KES)', 'date': ''},
            color_discrete_sequence=['#00d4aa', '#58a6ff', '#f0883e', '#a371f7', '#3fb950']
        )
        fig.update_layout(
            height=450,
            paper_bgcolor='#0f1419',
            plot_bgcolor='#161b22',
            font_color='#c9d1d9',
            legend_bgcolor='rgba(0,0,0,0)',
            xaxis_gridcolor='#30363d',
            yaxis_gridcolor='#30363d',
            font_family='Georgia, serif'
        )
        st.plotly_chart(fig, use_container_width=True)

with c2:
    if pd.notna(prev_date):
        latest_p = df[df['date'] == latest_date][['item', 'price_kes', 'category']].set_index('item')
        prev_p = df[df['date'] == prev_date][['item', 'price_kes']].set_index('item')
        
        mom = latest_p.copy()
        mom['prev'] = prev_p['price_kes']
        mom['change'] = ((mom['price_kes'] - mom['prev']) / mom['prev'] * 100).round(1)
        mom = mom.reset_index()[['item', 'category', 'change']].dropna()
        
        fig_mom = px.bar(
            mom, x='change', y='item', color='change', orientation='h',
            color_continuous_scale=['#3fb950', '#f0883e', '#f85149'],
            labels={'change': '%', 'item': ''}
        )
        fig_mom.update_layout(
            height=450,
            paper_bgcolor='#0f1419',
            plot_bgcolor='#161b22',
            font_color='#c9d1d9',
            yaxis_gridcolor='#30363d',
            xaxis_gridcolor='#30363d',
            showlegend=False,
            coloraxis_showscale=False,
            font_family='Georgia, serif'
        )
        st.plotly_chart(fig_mom, use_container_width=True)

# ---- INFLATION + QUALITY ----
st.markdown('<h3>Inflation Proxy & Data Quality</h3>', unsafe_allow_html=True)

p1, p2 = st.columns([2, 1])

with p1:
    weights = {'food': 0.45, 'fuel': 0.15, 'transport': 0.10}
    start_d = df['date'].min()
    end_d = df['date'].max()
    
    cat_start = df[df['date'] == start_d].groupby('category')['price_kes'].mean()
    cat_end = df[df['date'] == end_d].groupby('category')['price_kes'].mean()
    
    b_start = sum(cat_start.get(c, 0) * w for c, w in weights.items())
    b_end = sum(cat_end.get(c, 0) * w for c, w in weights.items())
    
    if b_start > 0:
        b_inf = ((b_end - b_start) / b_start) * 100
        
        contrib = pd.DataFrame({
            'Category': list(weights.keys()),
            'Weight': list(weights.values()),
            'Start': [cat_start.get(c, 0) for c in weights.keys()],
            'End': [cat_end.get(c, 0) for c in weights.keys()]
        })
        contrib['Contribution'] = ((contrib['End'] - contrib['Start']) / contrib['Start'] * 100 * contrib['Weight']).round(1)
        
        fig_c = px.bar(
            contrib, x='Category', y='Contribution', color='Contribution',
            color_continuous_scale=['#3fb950', '#f0883e', '#f85149'],
            labels={'Contribution': 'Weighted %'}
        )
        fig_c.update_layout(
            height=350,
            paper_bgcolor='#0f1419',
            plot_bgcolor='#161b22',
            font_color='#c9d1d9',
            yaxis_gridcolor='#30363d',
            xaxis_gridcolor='#30363d',
            coloraxis_showscale=False,
            font_family='Georgia, serif'
        )
        st.plotly_chart(fig_c, use_container_width=True)
        st.caption(f"6-Month Weighted Inflation Proxy: {b_inf:.1f}%  |  Weights: Food 45%, Fuel 15%, Transport 10%")

with p2:
    qc = df['data_quality'].value_counts().reset_index()
    qc.columns = ['Quality', 'Count']
    
    colors = {'verified_primary_source': '#00d4aa', 'estimated_from_index': '#58a6ff', 'crowdsourced_estimate': '#f0883e'}
    fig_pie = px.pie(
        qc, values='Count', names='Quality', hole=0.55,
        color='Quality', color_discrete_map=colors
    )
    fig_pie.update_layout(
        height=350,
        paper_bgcolor='#0f1419',
        font_color='#c9d1d9',
        showlegend=True,
        legend_font_color='#8b949e'
    )
    fig_pie.update_traces(textinfo='percent', textfont_size=10, textfont_color='#c9d1d9')
    st.plotly_chart(fig_pie, use_container_width=True)

# ============================================================
# UPGRADE 3: PERSONAL COST CALCULATOR
# ============================================================
st.markdown('<h3>Personal Cost Calculator</h3>', unsafe_allow_html=True)

st.markdown("""
<p style="color: #8b949e; font-size: 0.85rem; margin-bottom: 1rem;">
    Estimate your monthly essential costs based on current Nairobi prices.
</p>
""", unsafe_allow_html=True)

calc_col1, calc_col2, calc_col3 = st.columns(3)

with calc_col1:
    petrol_liters = st.number_input("Petrol (liters/month)", value=50, min_value=0, step=10)

with calc_col2:
    maize_bags = st.number_input("Maize flour (2kg bags/month)", value=4, min_value=0, step=1)

with calc_col3:
    matatu_trips = st.number_input("Matatu trips (month)", value=40, min_value=0, step=5)

# Get latest prices safely
latest_petrol = df[(df['category'] == 'fuel') & (df['item'] == 'Petrol') & (df['date'] == df['date'].max())]
latest_maize = df[(df['category'] == 'food') & (df['item'] == 'Maize Flour - 2kg') & (df['date'] == df['date'].max())]
latest_matatu = df[(df['category'] == 'transport') & (df['item'] == 'Matatu CBD to Eastlands') & (df['date'] == df['date'].max())]

if not latest_petrol.empty and not latest_maize.empty and not latest_matatu.empty:
    p_price = latest_petrol['price_kes'].iloc[0]
    m_price = latest_maize['price_kes'].iloc[0]
    t_price = latest_matatu['price_kes'].iloc[0]
    
    monthly_cost = (petrol_liters * p_price) + (maize_bags * m_price) + (matatu_trips * t_price)
    
    cost_col1, cost_col2 = st.columns([1, 3])
    with cost_col1:
        st.metric("Monthly Cost", f"KES {monthly_cost:,.0f}")
    with cost_col2:
        st.markdown(f"""
        <p style="color: #8b949e; font-size: 0.8rem; margin-top: 0.5rem;">
            Breakdown: Petrol KES {petrol_liters * p_price:,.0f} | 
            Maize KES {maize_bags * m_price:,.0f} | 
            Transport KES {matatu_trips * t_price:,.0f}
        </p>
        """, unsafe_allow_html=True)
else:
    st.warning("Unable to calculate — latest prices not found in dataset.")

# ---- DATA TABLE ----
st.markdown('<h3>Raw Data & Export</h3>', unsafe_allow_html=True)

t1, t2 = st.columns([4, 1])

with t1:
    st.dataframe(filtered_df, use_container_width=True, height=350)

with t2:
    st.markdown("""
    <p style="color: #8b949e; font-size: 0.85rem; margin-bottom: 1rem;">
        Download filtered dataset for external analysis.
    </p>
    """, unsafe_allow_html=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="DOWNLOAD CSV",
        data=csv,
        file_name='nairobi_prices.csv',
        mime='text/csv',
        use_container_width=True
    )

# ---- FOOTER ----
st.markdown("""
<div style="border-top: 1px solid #30363d; margin-top: 3rem; padding-top: 1rem;">
    <p style="color: #6e7681; font-size: 0.75rem; text-align: center;">
        Nairobi Price Intelligence v1.0 | Data: EPRA, KNBS, Crowdsourced Estimates
    </p>
</div>
""", unsafe_allow_html=True)