import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container{
    padding-top:1rem;
}

div[data-testid="metric-container"]{
    background-color:#F8FAFC;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:18px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/processed/cleaned_retail.csv")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df


df = load_data()

# =====================================================
# PAGE TITLE
# =====================================================

st.title("📊 Sales Analytics")

st.write(
"""
This page provides a detailed analysis of retail sales,
customer purchases, product performance and revenue trends.
"""
)

st.markdown("---")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Sales Filters")

countries = sorted(df["Country"].unique())

selected_country = st.sidebar.multiselect(
    "🌍 Country",
    countries,
    default=countries
)

df = df[df["Country"].isin(selected_country)]

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(min_date, max_date)
)

if len(date_range) == 2:

    start_date, end_date = date_range

    df = df[
        (df["InvoiceDate"].dt.date >= start_date) &
        (df["InvoiceDate"].dt.date <= end_date)
    ]

# =====================================================
# KPI CARDS
# =====================================================

total_sales = df["TotalPrice"].sum()

total_orders = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

average_order = total_sales / total_orders

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "💰 Total Sales",
        f"₹ {total_sales:,.0f}"
    )

with c2:

    st.metric(
        "🛒 Orders",
        f"{total_orders:,}"
    )

with c3:

    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with c4:

    st.metric(
        "📦 Avg Order",
        f"₹ {average_order:.2f}"
    )

st.markdown("---")
# =====================================================
# DAILY SALES TREND
# =====================================================

daily_sales = (
    df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"]
      .sum()
      .reset_index()
)

fig_daily = px.line(
    daily_sales,
    x="InvoiceDate",
    y="TotalPrice",
    title="📈 Daily Sales Trend",
    markers=True,
    template="plotly_white"
)

# =====================================================
# MONTHLY SALES
# =====================================================

monthly_sales = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
      .sum()
      .reset_index()
)

monthly_sales["InvoiceDate"] = monthly_sales["InvoiceDate"].astype(str)

fig_month = px.bar(
    monthly_sales,
    x="InvoiceDate",
    y="TotalPrice",
    title="📅 Monthly Revenue",
    text_auto=".2s",
    template="plotly_white"
)

# =====================================================
# TOP COUNTRIES
# =====================================================

country_sales = (
    df.groupby("Country")["TotalPrice"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_country = px.bar(
    country_sales,
    x="TotalPrice",
    y="Country",
    orientation="h",
    title="🌍 Top 10 Countries",
    text_auto=".2s",
    template="plotly_white"
)

# =====================================================
# TOP PRODUCTS
# =====================================================

top_products = (
    df.groupby("Description")["TotalPrice"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_products = px.bar(
    top_products,
    x="TotalPrice",
    y="Description",
    orientation="h",
    title="🛍 Top 10 Products",
    text_auto=".2s",
    template="plotly_white"
)

# =====================================================
# TOP CUSTOMERS
# =====================================================

top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_customers = px.bar(
    top_customers,
    x="CustomerID",
    y="TotalPrice",
    title="👑 Top Customers",
    text_auto=".2s",
    template="plotly_white"
)

# =====================================================
# SALES DISTRIBUTION
# =====================================================

fig_distribution = px.histogram(
    df,
    x="TotalPrice",
    nbins=50,
    title="📦 Sales Distribution",
    template="plotly_white"
)

# =====================================================
# REVENUE BY WEEKDAY
# =====================================================

weekday_sales = df.copy()

weekday_sales["Weekday"] = weekday_sales["InvoiceDate"].dt.day_name()

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_sales["Weekday"] = pd.Categorical(
    weekday_sales["Weekday"],
    categories=weekday_order,
    ordered=True
)

weekday_sales = (
    weekday_sales.groupby("Weekday")["TotalPrice"]
    .sum()
    .reset_index()
)

fig_weekday = px.bar(
    weekday_sales,
    x="Weekday",
    y="TotalPrice",
    title="📅 Revenue by Weekday",
    text_auto=".2s",
    template="plotly_white"
)

# =====================================================
# DISPLAY CHARTS
# =====================================================

left, right = st.columns(2)

with left:
    st.plotly_chart(fig_daily, use_container_width=True)

with right:
    st.plotly_chart(fig_month, use_container_width=True)

left, right = st.columns(2)

with left:
    st.plotly_chart(fig_country, use_container_width=True)

with right:
    st.plotly_chart(fig_products, use_container_width=True)

left, right = st.columns(2)

with left:
    st.plotly_chart(fig_customers, use_container_width=True)

with right:
    st.plotly_chart(fig_distribution, use_container_width=True)

st.plotly_chart(fig_weekday, use_container_width=True)

st.markdown("---")
# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.header("📊 Executive Summary")

best_country = country_sales.iloc[0]["Country"]
best_product = top_products.iloc[0]["Description"]

highest_sales_day = daily_sales.loc[
    daily_sales["TotalPrice"].idxmax(),
    "InvoiceDate"
]

highest_sales_amount = daily_sales["TotalPrice"].max()

lowest_sales_day = daily_sales.loc[
    daily_sales["TotalPrice"].idxmin(),
    "InvoiceDate"
]

lowest_sales_amount = daily_sales["TotalPrice"].min()

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
### 🌍 Best Performing Country

**{best_country}**
""")

    st.success(f"""
### 🛍 Best Selling Product

**{best_product}**
""")

    st.success(f"""
### 💰 Total Revenue

₹ **{total_sales:,.2f}**
""")

with col2:

    st.info(f"""
### 📈 Highest Sales Day

**{highest_sales_day}**

Revenue : ₹ **{highest_sales_amount:,.2f}**
""")

    st.warning(f"""
### 📉 Lowest Sales Day

**{lowest_sales_day}**

Revenue : ₹ **{lowest_sales_amount:,.2f}**
""")

st.markdown("---")

# =====================================================
# AI BUSINESS RECOMMENDATIONS
# =====================================================

st.header("🤖 AI Business Recommendations")

recommendations = []

if total_sales > 8000000:
    recommendations.append(
        "✅ Revenue is strong. Continue investing in top-selling products."
    )

if average_order < 500:
    recommendations.append(
        "📦 Increase Average Order Value using product bundles."
    )

if total_customers < 5000:
    recommendations.append(
        "📢 Launch marketing campaigns to acquire more customers."
    )

recommendations.append(
    f"🌍 Expand marketing in **{best_country}**, your strongest market."
)

recommendations.append(
    f"⭐ Maintain sufficient inventory for **{best_product}**."
)

recommendations.append(
    "📈 Use demand forecasting to improve inventory planning."
)

for rec in recommendations:
    st.success(rec)

st.markdown("---")

# =====================================================
# TOP PRODUCTS TABLE
# =====================================================

st.header("🏆 Top 10 Best Selling Products")

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================================
# TOP CUSTOMERS TABLE
# =====================================================

st.header("👑 Top 10 Customers")

st.dataframe(
    top_customers,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================================
# DATA PREVIEW
# =====================================================

st.header("📄 Retail Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DATASET SUMMARY
# =====================================================

st.header("📈 Statistical Summary")

st.dataframe(
    df.describe(),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DOWNLOAD REPORTS
# =====================================================

st.header("📥 Download Reports")

download_col1, download_col2 = st.columns(2)

with download_col1:

    st.download_button(
        label="📄 Download Clean Dataset",
        data=df.to_csv(index=False),
        file_name="cleaned_retail.csv",
        mime="text/csv"
    )

with download_col2:

    try:

        forecast = pd.read_csv(
            "data/processed/sales_forecast.csv"
        )

        st.download_button(
            label="📈 Download Sales Forecast",
            data=forecast.to_csv(index=False),
            file_name="sales_forecast.csv",
            mime="text/csv"
        )

    except:

        st.info("Forecast file not available.")

st.markdown("---")

# =====================================================
# PROJECT INFORMATION
# =====================================================

st.header("ℹ️ About RetailPulse")

st.write("""

RetailPulse is an AI-powered Retail Analytics Platform that helps businesses analyze customer behavior, monitor sales performance, forecast demand, and optimize inventory.

### Tech Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Scikit-Learn
- Prophet
- XGBoost

### Features

- Sales Analytics
- Customer Segmentation
- Demand Forecasting
- Inventory Optimization
- Interactive Dashboard
- AI Business Insights

""")

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
<hr>

<div style='text-align:center;'>

<h4>📊 RetailPulse</h4>

<p>
AI-Powered Retail Analytics Platform
</p>

<p>
Built using ❤️ Streamlit • Plotly • Python
</p>

<p>
© 2026 Kuldeep Yadav
</p>

</div>

""",
unsafe_allow_html=True
)