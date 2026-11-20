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
header {visibility:hidden;}
</style>
"""

st.markdown(hide_menu, unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.markdown("""
<h1 style='text-align:center;color:#2563EB;'>
 Inventory Optimization
</h1>

<h3 style='text-align:center;color:gray;'>
AI-Powered Inventory Analytics
</h3>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

 df = pd.read_csv(
 "data/processed/cleaned_retail.csv"
 )

 df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

 return df

df = load_data()

# =====================================================
# PRODUCT SUMMARY
# =====================================================

inventory = (
 df.groupby("Description")
 .agg(
 Quantity=("Quantity","sum"),
 Revenue=("TotalPrice","sum"),
 Orders=("InvoiceNo","nunique")
 )
 .reset_index()
)

# =====================================================
# KPI CARDS
# =====================================================

total_products = len(inventory)

total_quantity = inventory["Quantity"].sum()

total_revenue = inventory["Revenue"].sum()

avg_quantity = inventory["Quantity"].mean()

c1,c2,c3,c4 = st.columns(4)

with c1:
 st.metric(" Products", total_products)

with c2:
 st.metric(" Quantity Sold", f"{total_quantity:,}")

with c3:
 st.metric(" Revenue", f"₹ {total_revenue:,.0f}")

with c4:
 st.metric(" Avg Quantity", f"{avg_quantity:.1f}")

st.markdown("---")

# =====================================================
# DATA PREVIEW
# =====================================================

st.subheader("Inventory Dataset")

st.dataframe(
 inventory.head(),
 use_container_width=True,
 hide_index=True
)

st.markdown("---")
# =====================================================
# TOP 10 SELLING PRODUCTS
# =====================================================

st.header(" Top 10 Best Selling Products")

top_products = (
 inventory.sort_values("Revenue", ascending=False)
 .head(10)
)

fig_top = px.bar(
 top_products,
 x="Revenue",
 y="Description",
 orientation="h",
 color="Revenue",
 title="Top 10 Products by Revenue",
 text_auto=".2s",
 template="plotly_white"
)

fig_top.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig_top, use_container_width=True)

st.markdown("---")

# =====================================================
# BOTTOM 10 PRODUCTS
# =====================================================

st.header(" Lowest Selling Products")

bottom_products = (
 inventory.sort_values("Revenue", ascending=True)
 .head(10)
)

fig_bottom = px.bar(
 bottom_products,
 x="Revenue",
 y="Description",
 orientation="h",
 color="Revenue",
 title="Lowest Selling Products",
 text_auto=".2s",
 template="plotly_white"
)

fig_bottom.update_layout(yaxis=dict(categoryorder="total ascending"))

st.plotly_chart(fig_bottom, use_container_width=True)

st.markdown("---")

# =====================================================
# REVENUE CONTRIBUTION
# =====================================================

st.header(" Revenue Contribution")

top15 = (
 inventory.sort_values("Revenue", ascending=False)
 .head(15)
)

fig_pie = px.pie(
 top15,
 names="Description",
 values="Revenue",
 hole=0.45,
 title="Top 15 Products Revenue Share"
)

fig_pie.update_traces(textposition="inside")

st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# =====================================================
# QUANTITY DISTRIBUTION
# =====================================================

st.header(" Product Quantity Distribution")

fig_hist = px.histogram(
 inventory,
 x="Quantity",
 nbins=40,
 title="Distribution of Product Quantity Sold",
 template="plotly_white"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")

# =====================================================
# TOP PRODUCTS TABLE
# =====================================================

st.header(" Top Products")

st.dataframe(
 top_products,
 use_container_width=True,
 hide_index=True
)

st.markdown("---")

# =====================================================
# ABC INVENTORY ANALYSIS
# =====================================================

st.header(" ABC Inventory Classification")

inventory = inventory.sort_values(
 "Revenue",
 ascending=False
)

inventory["RevenuePercent"] = (
 inventory["Revenue"] /
 inventory["Revenue"].sum()
)

inventory["Cumulative"] = (
 inventory["RevenuePercent"]
 .cumsum()
)

def abc_class(value):
 if value <= 0.80:
 return "A"
 elif value <= 0.95:
 return "B"
 else:
 return "C"

inventory["ABC"] = (
 inventory["Cumulative"]
 .apply(abc_class)
)

abc_summary = (
 inventory.groupby("ABC")
 .agg(
 Products=("Description", "count"),
 Revenue=("Revenue", "sum")
 )
 .reset_index()
)

fig_abc = px.bar(
 abc_summary,
 x="ABC",
 y="Revenue",
 color="ABC",
 text_auto=".2s",
 title="ABC Inventory Analysis",
 template="plotly_white"
)

st.plotly_chart(
 fig_abc,
 use_container_width=True
)

st.markdown("---")
# =====================================================
# AI INVENTORY INSIGHTS
# =====================================================

st.header(" AI Inventory Insights")

highest_product = inventory.iloc[0]
lowest_product = inventory.iloc[-1]

col1, col2 = st.columns(2)

with col1:
 st.success(f"""
### Best Performing Product

**{highest_product['Description']}**

Revenue: ₹ {highest_product['Revenue']:,.2f}

Quantity Sold: {highest_product['Quantity']:,}
""")

with col2:
 st.warning(f"""
### Lowest Performing Product

**{lowest_product['Description']}**

Revenue: ₹ {lowest_product['Revenue']:,.2f}

Quantity Sold: {lowest_product['Quantity']:,}
""")

st.markdown("---")

# =====================================================
# LOW STOCK ALERTS
# =====================================================

st.header(" Low Stock / Low Sales Products")

low_stock = inventory[inventory["Quantity"] < inventory["Quantity"].quantile(0.25)]

st.dataframe(
 low_stock,
 use_container_width=True,
 hide_index=True
)

st.markdown("---")

# =====================================================
# REORDER RECOMMENDATIONS
# =====================================================

st.header(" Reorder Recommendations")

recommend = inventory.sort_values(
 "Revenue",
 ascending=False
).head(15)

st.dataframe(
 recommend[["Description", "Revenue", "Quantity", "Orders", "ABC"]],
 use_container_width=True,
 hide_index=True
)

st.info(
"""
Products in **ABC Category A** contribute the highest revenue.
Maintain sufficient inventory levels and prioritize timely restocking
to avoid stockouts.
"""
)

st.markdown("---")

# =====================================================
# INVENTORY STATISTICS
# =====================================================

st.header(" Inventory Statistics")

stats = inventory[
 ["Quantity", "Revenue", "Orders"]
].describe().round(2)

st.dataframe(
 stats,
 use_container_width=True
)

st.markdown("---")

# =====================================================
# DOWNLOAD REPORT
# =====================================================

st.header(" Download Inventory Report")

csv = inventory.to_csv(index=False).encode("utf-8")

st.download_button(
 label=" Download Inventory Report",
 data=csv,
 file_name="inventory_report.csv",
 mime="text/csv"
)

st.markdown("---")

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.header(" Executive Summary")

category_a = (inventory["ABC"] == "A").sum()
category_b = (inventory["ABC"] == "B").sum()
category_c = (inventory["ABC"] == "C").sum()

st.success(f" Total Products Analysed: {len(inventory):,}")
st.success(f" Category A Products: {category_a}")
st.success(f" Category B Products: {category_b}")
st.success(f" Category C Products: {category_c}")

st.markdown("---")

# =====================================================
# BUSINESS RECOMMENDATIONS
# =====================================================

st.header(" Business Recommendations")

recommendations = [
 " Prioritize Category A products for inventory planning.",
 " Monitor Category B products regularly to prevent stock shortages.",
 " Reduce excess inventory of Category C products.",
 " Automate reorder points for high-demand products.",
 " Review inventory trends every month.",
 " Integrate demand forecasting with inventory planning.",
 " Focus promotional campaigns on slow-moving products."
]

for rec in recommendations:
 st.success(rec)

st.markdown("---")

# =====================================================
# ABOUT THIS PAGE
# =====================================================

st.header(" About Inventory Optimization")

st.write("""
This dashboard helps businesses optimize inventory using sales analytics.

### Features

- Product Performance Analysis
- ABC Inventory Classification
- Low Performing Product Detection
- Revenue Contribution Analysis
- Reorder Recommendations
- AI Business Insights

### Benefits

- Reduce stock shortages
- Improve warehouse efficiency
- Increase revenue
- Lower inventory holding costs
""")

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
<hr>

<div style='text-align:center;'>

### Inventory Optimization Dashboard

Built with using Streamlit, Plotly & Pandas

 2026 RetailPulse

</div>
""",
unsafe_allow_html=True
)
