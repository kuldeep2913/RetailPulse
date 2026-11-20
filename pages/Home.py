import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

# =====================================================
# LOAD CUSTOM CSS
# =====================================================

def load_css():
    try:
        with open("assets/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass

load_css()

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
# USE THE COMPLETE DATASET ON THE OVERVIEW PAGE
# =====================================================

# No country or date filters are applied on this page.
# Detailed filtering remains available in the relevant analytics modules.

# =====================================================
# HERO SECTION
# =====================================================

logo_col, title_col = st.columns([1, 5])

with logo_col:

    st.image("assets/logo.png", width=120)

with title_col:

    st.title(" RetailPulse")

    st.caption("AI-Powered Retail Analytics Platform")

st.image(
    "assets/banner.png",
    use_container_width=True
)

st.divider()

# =====================================================
# INTRODUCTION
# =====================================================

st.header(" Welcome to RetailPulse")

st.write(
    """
RetailPulse is an AI-powered Retail Analytics platform that helps businesses
analyze sales performance, customer behavior, inventory trends, and future demand.

The dashboard transforms raw retail transaction data into meaningful insights
using Data Analytics and Machine Learning.
"""
)

info1, info2, info3 = st.columns(3)

with info1:

    st.success(" Sales Dashboard")

    st.write("Monitor revenue, orders and sales trends.")

with info2:

    st.success(" Customer Analytics")

    st.write("Analyze customer behaviour and loyalty.")

with info3:

    st.success(" AI Insights")

    st.write("Forecast sales and generate recommendations.")

st.divider()

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_sales = df["TotalPrice"].sum()

total_orders = df["InvoiceNo"].nunique()

total_customers = df["CustomerID"].nunique()

avg_order = (
    total_sales / total_orders
    if total_orders > 0 else 0
)

total_products = df["Description"].nunique()

total_countries = df["Country"].nunique()

# =====================================================
# KPI SECTION
# =====================================================

st.header(" Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        " Total Revenue",
        f"₹ {total_sales:,.0f}"
    )

with kpi2:
    st.metric(
        " Orders",
        f"{total_orders:,}"
    )

with kpi3:
    st.metric(
        " Customers",
        f"{total_customers:,}"
    )

with kpi4:
    st.metric(
        " Avg Order",
        f"₹ {avg_order:,.2f}"
    )

st.divider()

# =====================================================
# BUSINESS OVERVIEW
# =====================================================

st.header(" Business Overview")

overview1, overview2, overview3 = st.columns(3)

with overview1:

    st.info(" Countries")

    st.metric(
        "Operating Countries",
        total_countries
    )

with overview2:

    st.info(" Products")

    st.metric(
        "Unique Products",
        total_products
    )

with overview3:

    st.info(" Transactions")

    st.metric(
        "Total Records",
        len(df)
    )

st.divider()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.header(" Executive Summary")

best_country = (
    df.groupby("Country")["TotalPrice"]
      .sum()
      .idxmax()
)

best_product = (
    df.groupby("Description")["TotalPrice"]
      .sum()
      .idxmax()
)

highest_day = (
    df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"]
      .sum()
      .idxmax()
)

highest_sales = (
    df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"]
      .sum()
      .max()
)

left, right = st.columns(2)

with left:

    st.success(
        f"""
###  Best Country

{best_country}
"""
    )

    st.success(
        f"""
###  Best Product

{best_product}
"""
    )

with right:

    st.info(
        f"""
###  Highest Sales Day

{highest_day}
"""
    )

    st.info(
        f"""
###  Highest Daily Revenue

₹ {highest_sales:,.2f}
"""
    )

st.divider()

# =====================================================
# BUSINESS HEALTH
# =====================================================

st.header(" Business Health")

health1, health2, health3 = st.columns(3)

with health1:

    st.success(" Revenue")

    st.write(
        "Sales performance is healthy."
    )

with health2:

    st.success(" Customer Base")

    st.write(
        f"{total_customers:,} active customers."
    )

with health3:

    st.success(" Orders")

    st.write(
        f"{total_orders:,} successful orders."
    )

st.divider()

# =====================================================
# PERFORMANCE SCORECARD
# =====================================================

st.header(" Performance Scorecard")

score1, score2, score3, score4 = st.columns(4)

with score1:

    st.metric(
        " Countries",
        total_countries
    )

with score2:

    st.metric(
        " Products",
        total_products
    )

with score3:

    st.metric(
        " Customers",
        total_customers
    )

with score4:

    st.metric(
        " Transactions",
        len(df)
    )

st.divider()

# =====================================================
# DAILY SALES TREND
# =====================================================

st.header(" Sales Analytics")

daily_sales = (
    df.groupby(df["InvoiceDate"].dt.date)["TotalPrice"]
      .sum()
      .reset_index()
)

fig_daily = px.line(
    daily_sales,
    x="InvoiceDate",
    y="TotalPrice",
    title="Daily Sales Trend",
    markers=True
)

fig_daily.update_layout(
    xaxis_title="Date",
    yaxis_title="Revenue",
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
    title="Monthly Revenue",
    text_auto=".2s"
)

fig_month.update_layout(
    template="plotly_white",
    xaxis_title="Month",
    yaxis_title="Revenue"
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
    title="Top 10 Countries"
)

fig_country.update_layout(template="plotly_white")

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

fig_product = px.bar(
    top_products,
    x="TotalPrice",
    y="Description",
    orientation="h",
    title="Top 10 Products"
)

fig_product.update_layout(template="plotly_white")

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

fig_customer = px.bar(
    top_customers,
    x="CustomerID",
    y="TotalPrice",
    title="Top 10 Customers"
)

fig_customer.update_layout(template="plotly_white")

# =====================================================
# SALES DISTRIBUTION
# =====================================================

fig_hist = px.histogram(
    df,
    x="TotalPrice",
    nbins=40,
    title="Sales Distribution"
)

fig_hist.update_layout(template="plotly_white")

# =====================================================
# WORLD SALES MAP
# =====================================================

country_map = (
    df.groupby("Country")["TotalPrice"]
      .sum()
      .reset_index()
)

fig_map = px.choropleth(
    country_map,
    locations="Country",
    locationmode="country names",
    color="TotalPrice",
    hover_name="Country",
    color_continuous_scale="Blues",
    title="Global Revenue Distribution"
)

# =====================================================
# DASHBOARD LAYOUT
# =====================================================

row1, row2 = st.columns(2)

with row1:
    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )

with row2:
    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

row3, row4 = st.columns(2)

with row3:
    st.plotly_chart(
        fig_country,
        use_container_width=True
    )

with row4:
    st.plotly_chart(
        fig_product,
        use_container_width=True
    )

row5, row6 = st.columns(2)

with row5:
    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )

with row6:
    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

st.plotly_chart(
    fig_map,
    use_container_width=True
)

st.divider()

# =====================================================
# CUSTOMER LEADERBOARD
# =====================================================

st.header(" Customer Leaderboard")

leaderboard = (
    df.groupby("CustomerID")
      .agg(
          Revenue=("TotalPrice", "sum"),
          Orders=("InvoiceNo", "nunique")
      )
      .sort_values("Revenue", ascending=False)
      .head(10)
      .reset_index()
)

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================================
# SALES BY WEEKDAY
# =====================================================

st.header(" Sales by Weekday")

weekday_sales = (
    df.groupby(df["InvoiceDate"].dt.day_name())["TotalPrice"]
      .sum()
      .reindex([
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday"
      ])
      .fillna(0)
      .reset_index()
)

weekday_sales.columns = ["Weekday", "Revenue"]

fig_weekday = px.bar(
    weekday_sales,
    x="Weekday",
    y="Revenue",
    title="Revenue by Weekday",
    color="Revenue"
)

fig_weekday.update_layout(template="plotly_white")

st.plotly_chart(
    fig_weekday,
    use_container_width=True
)

st.divider()

# =====================================================
# AI BUSINESS RECOMMENDATIONS
# =====================================================

st.header(" AI Business Recommendations")

recommendations = []

if total_sales > 5000000:
    recommendations.append(
        " Sales performance is excellent. Continue investing in your best-selling products."
    )

if avg_order < 500:
    recommendations.append(
        " Increase Average Order Value by offering bundles and discounts."
    )

if total_customers < 5000:
    recommendations.append(
        " Acquire more customers using targeted marketing campaigns."
    )

recommendations.append(
    f" Focus your marketing efforts in **{best_country}**."
)

recommendations.append(
    f" Maintain sufficient inventory for **{best_product}**."
)

for rec in recommendations:
    st.success(rec)

st.divider()

# =====================================================
# DOWNLOAD REPORTS
# =====================================================

st.header(" Download Reports")

download1, download2 = st.columns(2)

with download1:

    st.download_button(
        label=" Download Clean Dataset",
        data=df.to_csv(index=False),
        file_name="cleaned_retail.csv",
        mime="text/csv"
    )

with download2:

    try:

        forecast = pd.read_csv(
            "data/processed/sales_forecast.csv"
        )

        st.download_button(
            label=" Download Forecast",
            data=forecast.to_csv(index=False),
            file_name="sales_forecast.csv",
            mime="text/csv"
        )

    except:

        st.warning(
            "Sales forecast file not found."
        )

st.divider()

# =====================================================
# DATA PREVIEW
# =====================================================

st.header(" Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

st.divider()

# =====================================================
# STATISTICAL SUMMARY
# =====================================================

st.header(" Statistical Summary")

st.dataframe(
    df.describe(include="all"),
    use_container_width=True
)

st.divider()

# =====================================================
# MEET THE TEAM
# =====================================================

st.header("Meet the Team")

team1, team2 = st.columns(2)

with team1:
    st.markdown("""
    <div class="team-card">
        <div class="team-role">Project Lead</div>
        <h3>Kuldeep Yadav</h3>
        <p>B.Tech Computer Science Engineering (AI)</p>
        <p>Shivalik College of Engineering</p>
    </div>
    """, unsafe_allow_html=True)

with team2:
    st.markdown("""
    <div class="team-card">
        <div class="team-role">Team Member</div>
        <h3>Prashant</h3>
        <p>B.Tech Computer Science Engineering (AI)</p>
        <p>Shivalik College of Engineering</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =====================================================
# PROJECT FEATURES
# =====================================================

st.header(" Platform Features")

feature1, feature2, feature3 = st.columns(3)

with feature1:

    st.success(" Sales Analytics")

    st.write(" Daily Sales")

    st.write(" Monthly Revenue")

    st.write(" Country Analysis")

with feature2:

    st.success(" Customer Intelligence")

    st.write(" RFM Analysis")

    st.write(" Customer Segmentation")

    st.write(" Top Customers")

with feature3:

    st.success(" AI & Forecasting")

    st.write(" Demand Forecast")

    st.write(" Business Insights")

    st.write(" Report Generation")

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.caption("RetailPulse  2026")

st.caption(
    "Built with  using Streamlit • Plotly • Pandas • Python"
)