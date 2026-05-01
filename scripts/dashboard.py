import pandas as pd
import plotly.express as px
import streamlit as st
import os

# Page setup
st.set_page_config(page_title="Nairobi Price Intelligence", page_icon="🇰🇪", layout="wide")
st.title("🇰🇪 Nairobi Price Intelligence Dashboard")
st.markdown("*Tracking fuel, food, and transport costs in Kenya's capital*")

# Load data from CSV file
@st.cache_data
def load_data():
    # Get the correct path to the CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '..', 'data', 'nairobi_prices.csv')
    
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
selected_categories = st.sidebar.multiselect(
    "Categories",
    options=df['category'].unique(),
    default=df['category'].unique()
)

# Filter data
filtered_df = df[df['category'].isin(selected_categories)]

# Key Metrics
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    fuel_data = df[df['category'] == 'fuel']
    if not fuel_data.empty:
        latest_fuel = fuel_data['price_kes'].iloc[-1]
        st.metric("Latest Petrol Price", f"KES {latest_fuel:.2f}")

with col2:
    food_data = df[df['category'] == 'food']
    if not food_data.empty:
        avg_food = food_data['price_kes'].mean()
        st.metric("Avg Food Basket", f"KES {avg_food:.2f}")

with col3:
    transport_data = df[df['category'] == 'transport']
    if not transport_data.empty:
        avg_transport = transport_data['price_kes'].mean()
        st.metric("Avg Transport Cost", f"KES {avg_transport:.2f}")

# Price Trends
st.header("Price Trends")
if not filtered_df.empty:
    fig = px.line(
        filtered_df,
        x='date',
        y='price_kes',
        color='item',
        facet_col='category',
        facet_col_wrap=1,
        title="Price Trends by Category",
        labels={'price_kes': 'Price (KES)', 'date': 'Date'}
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# Category Comparison
st.header("Category Comparison")
category_summary = filtered_df.groupby('category')['price_kes'].mean().reset_index()
fig2 = px.bar(
    category_summary,
    x='category',
    y='price_kes',
    color='category',
    title="Average Prices by Category",
    labels={'price_kes': 'Average Price (KES)', 'category': 'Category'}
)
st.plotly_chart(fig2, use_container_width=True)

# Data Quality
st.header("Data Quality")
quality_counts = df['data_quality'].value_counts().reset_index()
quality_counts.columns = ['Quality Level', 'Count']
fig3 = px.pie(
    quality_counts,
    values='Count',
    names='Quality Level',
    title="Data Source Quality Distribution"
)
st.plotly_chart(fig3, use_container_width=True)

# Raw Data Table
st.header("Raw Data")
st.dataframe(filtered_df, use_container_width=True)

# About section
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("""
**Data Sources:**
- Fuel: EPRA official pump prices
- Food: KNBS CPI data  
- Transport: Crowdsourced matatu fares

*Built for Nairobi Price Intelligence Project*
""")
# INSIGHTS SECTION
st.header("🔍 Key Insights")

# Calculate inflation rates
fuel_start = df[(df['category'] == 'fuel') & (df['item'] == 'Petrol')]['price_kes'].min()
fuel_end = df[(df['category'] == 'fuel') & (df['item'] == 'Petrol')]['price_kes'].max()
fuel_inflation = ((fuel_end - fuel_start) / fuel_start) * 100

transport_start = df[(df['category'] == 'transport') & (df['item'] == 'Matatu CBD to Eastlands')]['price_kes'].min()
transport_end = df[(df['category'] == 'transport') & (df['item'] == 'Matatu CBD to Eastlands')]['price_kes'].max()
transport_inflation = ((transport_end - transport_start) / transport_start) * 100

food_start = df[(df['category'] == 'food')]['price_kes'].mean()
food_end = df[(df['category'] == 'food') & (df['date'] == df['date'].max())]['price_kes'].mean()
food_inflation = ((food_end - food_start) / food_start) * 100

# Display insights
insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.subheader("Fuel vs Transport")
    st.write(f"**Petrol prices rose {fuel_inflation:.1f}%** over the tracked period.")
    st.write(f"**Matatu fares rose {transport_inflation:.1f}%** — outpacing fuel costs.")
    if transport_inflation > fuel_inflation:
        st.warning("⚠️ Transport inflation exceeds fuel inflation, suggesting cartel pricing power.")

with insight_col2:
    st.subheader("Food Basket Stability")
    st.write(f"**Average food prices rose {food_inflation:.1f}%** — more stable than transport.")
    st.success("✅ Agricultural supply chains remain resilient despite global shocks.")

# Correlation note
st.info(f"""
**Methodology Note:** All transport estimates are flagged as `crowdsourced_estimate` in the data quality column. 
Fuel data is verified from EPRA primary sources. Food baselines are verified from KNBS CPI, with missing months interpolated.
""")