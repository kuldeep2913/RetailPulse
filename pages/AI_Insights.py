import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

hide_menu = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

</style>
"""

st.markdown(hide_menu, unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<h1 style='text-align:center;color:#2563EB;'>
 AI Business Insights
</h1>

<h3 style='text-align:center;color:gray;'>
Executive Decision Dashboard
</h3>
""", unsafe_allow_html=True)

st.markdown("---")

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
# EXECUTIVE KPIs
# =====================================================

total_sales = df["TotalPrice"].sum()

orders = df["InvoiceNo"].nunique()

customers = df["CustomerID"].nunique()

products = df["Description"].nunique()

avg_order = total_sales / orders

col1,col2,col3,col4,col5 = st.columns(5)

with col1:
    st.metric(" Revenue",f"₹ {total_sales:,.0f}")

with col2:
    st.metric(" Orders",f"{orders:,}")

with col3:
    st.metric(" Customers",f"{customers:,}")

with col4:
    st.metric(" Products",products)

with col5:
    st.metric(" Avg Order",f"₹ {avg_order:.2f}")

st.markdown("---")

# =====================================================
# MONTHLY SALES
# =====================================================

monthly = df.copy()

monthly["Month"] = monthly["InvoiceDate"].dt.to_period("M").astype(str)

monthly = (
    monthly.groupby("Month")["TotalPrice"]
           .sum()
           .reset_index()
)

fig = px.line(
    monthly,
    x="Month",
    y="TotalPrice",
    markers=True,
    title="Monthly Revenue Trend",
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
# =====================================================
# AI EXECUTIVE SUMMARY
# =====================================================

st.header(" AI Executive Summary")

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

best_customer = (
    df.groupby("CustomerID")["TotalPrice"]
      .sum()
      .idxmax()
)

highest_sale = df["TotalPrice"].max()

lowest_sale = df["TotalPrice"].min()

left, right = st.columns(2)

with left:

    st.success(f"""
###  Best Performing Country

**{best_country}**
""")

    st.success(f"""
###  Best Selling Product

**{best_product}**
""")

    st.success(f"""
###  Highest Spending Customer

**Customer ID:** {int(best_customer)}
""")

with right:

    st.info(f"""
###  Total Revenue

₹ {total_sales:,.2f}
""")

    st.info(f"""
###  Highest Order Value

₹ {highest_sale:,.2f}
""")

    st.info(f"""
###  Lowest Order Value

₹ {lowest_sale:,.2f}
""")

st.markdown("---")

# =====================================================
# TOP 10 PRODUCTS
# =====================================================

st.header(" Top 10 Products")

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
    color="TotalPrice",
    title="Top Revenue Generating Products",
    text_auto=".2s",
    template="plotly_white"
)

fig_products.update_layout(
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig_products, use_container_width=True)

st.markdown("---")

# =====================================================
# COUNTRY PERFORMANCE
# =====================================================

st.header(" Country Performance")

country_sales = (
    df.groupby("Country")["TotalPrice"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_country = px.bar(
    country_sales,
    x="Country",
    y="TotalPrice",
    color="TotalPrice",
    text_auto=".2s",
    title="Top 10 Countries by Revenue",
    template="plotly_white"
)

st.plotly_chart(fig_country, use_container_width=True)

st.markdown("---")

# =====================================================
# CUSTOMER DISTRIBUTION
# =====================================================

st.header(" Top Customers")

top_customers = (
    df.groupby("CustomerID")["TotalPrice"]
      .sum()
      .sort_values(ascending=False)
      .head(15)
      .reset_index()
)

fig_customer = px.bar(
    top_customers,
    x="CustomerID",
    y="TotalPrice",
    color="TotalPrice",
    text_auto=".2s",
    title="Top 15 Customers by Revenue",
    template="plotly_white"
)

st.plotly_chart(fig_customer, use_container_width=True)

st.markdown("---")

# =====================================================
# SALES DISTRIBUTION
# =====================================================

st.header(" Sales Distribution")

fig_hist = px.histogram(
    df,
    x="TotalPrice",
    nbins=40,
    title="Distribution of Order Values",
    template="plotly_white"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")
# =====================================================
# AI BUSINESS RECOMMENDATIONS
# =====================================================

st.header(" AI Business Recommendations")

recommendations = [
    " Expand marketing efforts in the highest-performing countries to maximize revenue.",
    " Maintain sufficient inventory for the top-selling products to avoid stockouts.",
    " Reward high-value customers with exclusive loyalty programs and personalized offers.",
    " Identify low-selling products and consider discounts, bundles, or discontinuation.",
    " Use demand forecasting to improve inventory planning and reduce excess stock.",
    " Increase average order value through cross-selling and product recommendations.",
    " Monitor inventory weekly and automate reorder points for fast-moving products.",
    " Track monthly KPIs regularly to evaluate business performance."
]

for rec in recommendations:
    st.success(rec)

st.markdown("---")

# =====================================================
# SWOT ANALYSIS
# =====================================================

st.header(" Business SWOT Analysis")

col1, col2 = st.columns(2)

with col1:

    st.info("""
###  Strengths

- Strong customer base
- High revenue from top products
- Consistent monthly sales
- Good repeat customers
""")

    st.warning("""
###  Weaknesses

- Few products generate most revenue
- Some products have very low sales
- Revenue concentrated in limited regions
""")

with col2:

    st.success("""
###  Opportunities

- Expand into new markets
- Introduce customer loyalty programs
- Personalized recommendations
- AI-driven inventory optimization
""")

    st.error("""
###  Threats

- Demand fluctuations
- Inventory shortages
- Customer churn
- Competitive pricing
""")

st.markdown("---")

# =====================================================
# EXECUTIVE REPORT
# =====================================================

st.header(" Executive Summary Report")

summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Orders",
        "Total Customers",
        "Total Products",
        "Average Order Value",
        "Best Country",
        "Best Product",
        "Highest Spending Customer"
    ],
    "Value": [
        f"₹ {total_sales:,.2f}",
        orders,
        customers,
        products,
        f"₹ {avg_order:,.2f}",
        best_country,
        best_product,
        int(best_customer)
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# =====================================================
# DOWNLOAD EXECUTIVE REPORT
# =====================================================

st.header(" Download Executive Report")

csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    label=" Download Executive Report",
    data=csv,
    file_name="executive_business_report.csv",
    mime="text/csv"
)

st.markdown("---")

# =====================================================
# PROJECT OVERVIEW
# =====================================================

st.header(" About RetailPulse")

st.write("""
**RetailPulse** is an AI-powered Retail Analytics Platform designed to help businesses make data-driven decisions.

### Key Modules

-  Sales Dashboard
-  Customer Segmentation (RFM + K-Means)
-  Demand Forecasting (Prophet)
-  Inventory Optimization
-  AI Business Insights

### Technologies Used

- Python
- Streamlit
- Plotly
- Pandas
- Scikit-Learn
- Prophet
- NumPy

### Business Value

- Customer Segmentation
- Sales Forecasting
- Inventory Planning
- Executive Reporting
- Business Intelligence
""")

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
<hr>

<div style="text-align:center; padding:10px">

<h4> RetailPulse - AI Powered Retail Analytics Platform</h4>

Built with  using Streamlit, Plotly, Pandas, Scikit-Learn & Prophet

 2026 Kuldeep Yadav & Prashant | RetailPulse

</div>
""",
unsafe_allow_html=True
)