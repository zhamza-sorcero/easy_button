import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import altair as alt
import plotly.express as px

# Set page config
st.set_page_config(layout="wide", page_title="Easy Dashboard Demo")

# Create a centered title with custom styling
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin-bottom: 30px;'>
    <h1 style='color: #1E88E5; font-size: 50px; font-weight: bold;'>Look how easy this is!</h1>
</div>
""", unsafe_allow_html=True)

# Function to generate mock time series data
def generate_time_series(days=90, trend=0.5, seasonality=0.2, noise=0.3, start_value=100):
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates = sorted(dates)
    
    # Create a trend component
    trend_component = np.linspace(0, trend * days, days)
    
    # Create a seasonality component (weekly pattern)
    seasonality_component = [seasonality * np.sin(i/7 * 2 * np.pi) for i in range(days)]
    
    # Create a noise component
    noise_component = np.random.normal(0, noise, days)
    
    # Combine components
    values = start_value + trend_component + seasonality_component + noise_component
    
    return dates, values

# Function to generate mock categorical data
def generate_categorical_data(categories, mean_value=50, std_dev=15):
    values = [max(0, np.random.normal(mean_value, std_dev)) for _ in categories]
    return categories, values

# Create a two-column layout
col1, col2 = st.columns(2)

# CHART 1: Time series line chart
with col1:
    st.subheader("Revenue Trends (Last 90 Days)")
    dates, values = generate_time_series(days=90, trend=1, start_value=1000)
    df_time = pd.DataFrame({"Date": dates, "Revenue": values})
    
    # Plot using Altair
    chart = alt.Chart(df_time).mark_line(color='#1E88E5').encode(
        x='Date:T',
        y=alt.Y('Revenue:Q', scale=alt.Scale(zero=False))
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)

# CHART 2: Bar chart
with col2:
    st.subheader("Sales by Product Category")
    categories, values = generate_categorical_data(['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports'])
    df_cat = pd.DataFrame({"Category": categories, "Sales": values})
    
    # Plot using Plotly
    fig = px.bar(df_cat, x='Category', y='Sales', color_discrete_sequence=['#FF9800'])
    st.plotly_chart(fig, use_container_width=True)

# CHART 3: Pie chart
col3, col4 = st.columns(2)
with col3:
    st.subheader("Market Share Distribution")
    companies = ['Company A', 'Company B', 'Company C', 'Company D', 'Others']
    market_share = [30, 25, 15, 10, 20]
    
    # Create a pie chart using Matplotlib
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(market_share, labels=companies, autopct='%1.1f%%', startangle=90,
           colors=['#1E88E5', '#42A5F5', '#90CAF9', '#E3F2FD', '#BBDEFB'])
    ax.axis('equal')
    st.pyplot(fig)

# CHART 4: Heatmap
with col4:
    st.subheader("Weekly Activity Heatmap")
    
    # Generate mock weekly activity data
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = ['Morning', 'Afternoon', 'Evening', 'Night']
    
    data = np.random.randint(10, 100, size=(len(hours), len(days)))
    df_heatmap = pd.DataFrame(data, index=hours, columns=days)
    
    # Create heatmap using Seaborn
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df_heatmap, annot=True, cmap="YlGnBu", fmt="d", ax=ax)
    st.pyplot(fig)

# CHART 5: Scatter plot with trend line - full width
st.subheader("Customer Relationship: Spending vs. Loyalty")

# Generate mock scatter data
n_points = 100
x = np.random.normal(50, 15, n_points)
y = x * 0.7 + np.random.normal(20, 15, n_points)
df_scatter = pd.DataFrame({"Loyalty Score": x, "Average Spending": y})

# Create scatter plot with trend line using Plotly
fig = px.scatter(df_scatter, x="Loyalty Score", y="Average Spending", 
                trendline="ols", 
                color_discrete_sequence=['#4CAF50'])
st.plotly_chart(fig, use_container_width=True)

# CHART 6: Interactive geographic data
st.subheader("Regional Performance Map")

# Generate mock location data
regions = ["North", "South", "East", "West", "Central"]
lat = [41.5, 31.0, 39.0, 34.0, 37.5]
lon = [-87.0, -100.0, -75.0, -118.0, -95.0]
performance = np.random.randint(50, 100, len(regions))

df_geo = pd.DataFrame({
    "Region": regions,
    "Latitude": lat,
    "Longitude": lon,
    "Performance": performance
})

# Create a map
fig = px.scatter_geo(
    df_geo,
    lat="Latitude",
    lon="Longitude",
    text="Region",
    size="Performance",
    projection="natural earth",
    color="Performance",
    color_continuous_scale=px.colors.sequential.Viridis,
    size_max=20
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Add a footer
st.markdown("---")
st.markdown("*This dashboard was created with Streamlit using mock data for demonstration purposes.*")
st.markdown("""
### Deployment Instructions:
1. Create a GitHub repository and push both this file (`dashboard.py`) and the `requirements.txt` file to it
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and this file path
6. Click "Deploy"
""")

# Add a sidebar with some controls (just for show)
st.sidebar.title("Dashboard Controls")
st.sidebar.date_input("Select Date Range Start", datetime.now() - timedelta(days=90))
st.sidebar.date_input("Select Date Range End", datetime.now())
st.sidebar.multiselect("Filter by Category", ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports'], 
                         default=['Electronics', 'Clothing', 'Home & Kitchen'])
st.sidebar.slider("Confidence Threshold", 0, 100, 50)
st.sidebar.button("Update Dashboard")
