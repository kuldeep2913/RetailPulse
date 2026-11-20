import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================

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
 background:#F8FAFC;
 border-radius:12px;
 padding:18px;
 border:1px solid #E5E7EB;
 box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

 rfm = pd.read_csv("data/processed/customer_segments.csv")

 return rfm

rfm = load_data()

# =====================================================
# PAGE TITLE
# =====================================================

st.title(" Customer Segmentation")

st.write("""
Analyze customer purchasing behavior using **RFM Analysis**
and **K-Means Clustering**.
""")

st.markdown("---")

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Customer Filters")

segments = sorted(rfm["CustomerSegment"].unique())

selected_segments = st.sidebar.multiselect(
 "Customer Segment",
 options=segments,
 default=segments
)

rfm = rfm[
 rfm["CustomerSegment"].isin(selected_segments)
]

clusters = sorted(rfm["Cluster"].unique())

selected_clusters = st.sidebar.multiselect(
 "Cluster",
 options=clusters,
 default=clusters
)

rfm = rfm[
 rfm["Cluster"].isin(selected_clusters)
]

st.sidebar.markdown("---")

st.sidebar.write(
 f"Showing **{len(rfm)}** customers"
)

# =====================================================
# KPI CARDS
# =====================================================

total_customers = rfm["CustomerID"].nunique()

avg_recency = rfm["Recency"].mean()

avg_frequency = rfm["Frequency"].mean()

avg_monetary = rfm["Monetary"].mean()

c1,c2,c3,c4 = st.columns(4)

with c1:

 st.metric(
 " Customers",
 f"{total_customers:,}"
 )

with c2:

 st.metric(
 " Avg Recency",
 f"{avg_recency:.1f} Days"
 )

with c3:

 st.metric(
 " Avg Frequency",
 f"{avg_frequency:.1f}"
 )

with c4:

 st.metric(
 " Avg Monetary",
 f"₹ {avg_monetary:,.0f}"
 )

st.markdown("---")

# =====================================================
# SEGMENT SUMMARY
# =====================================================

st.subheader(" Customer Segment Summary")

segment_summary = (
 rfm.groupby("CustomerSegment")
 .agg(
 Customers=("CustomerID","count"),
 AvgRecency=("Recency","mean"),
 AvgFrequency=("Frequency","mean"),
 AvgMonetary=("Monetary","mean")
 )
 .reset_index()
)

st.dataframe(
 segment_summary,
 use_container_width=True,
 hide_index=True
)

st.markdown("---")
# =====================================================
# SEGMENT DISTRIBUTION
# =====================================================

st.header(" Customer Segment Distribution")

segment_count = (
 rfm["CustomerSegment"]
 .value_counts()
 .reset_index()
)

segment_count.columns = ["CustomerSegment", "Customers"]

fig_segment = px.pie(
 segment_count,
 names="CustomerSegment",
 values="Customers",
 hole=0.45,
 title="Customer Segments"
)

fig_segment.update_traces(textposition="inside", textinfo="percent+label")

# =====================================================
# CLUSTER DISTRIBUTION
# =====================================================

cluster_count = (
 rfm["Cluster"]
 .value_counts()
 .sort_index()
 .reset_index()
)

cluster_count.columns = ["Cluster", "Customers"]

fig_cluster = px.bar(
 cluster_count,
 x="Cluster",
 y="Customers",
 text_auto=True,
 title="Cluster Distribution",
 template="plotly_white"
)

left, right = st.columns(2)

with left:
 st.plotly_chart(fig_segment, use_container_width=True)

with right:
 st.plotly_chart(fig_cluster, use_container_width=True)

st.markdown("---")

# =====================================================
# RECENCY VS MONETARY
# =====================================================

fig_scatter = px.scatter(
 rfm,
 x="Recency",
 y="Monetary",
 color="CustomerSegment",
 hover_data=["CustomerID"],
 title="Recency vs Monetary",
 template="plotly_white",
 render_mode="svg"
)

fig_scatter.update_layout(
 height=500,
 title_x=0.5
)

# =====================================================
# FREQUENCY VS MONETARY
# =====================================================

fig_frequency = px.scatter(
 rfm,
 x="Frequency",
 y="Monetary",
 color="CustomerSegment",
 hover_data=["CustomerID"],
 title="Frequency vs Monetary",
 template="plotly_white",
 render_mode="svg"
)

fig_frequency.update_layout(
 height=500,
 title_x=0.5
)

left, right = st.columns(2)

with left:
 st.plotly_chart(
 fig_scatter,
 use_container_width=True,
 config={"displayModeBar": False}
 )

with right:
 st.plotly_chart(
 fig_frequency,
 use_container_width=True,
 config={"displayModeBar": False}
 )

st.markdown("---")
# =====================================================
# RECENCY DISTRIBUTION
# =====================================================

fig_recency = px.histogram(
 rfm,
 x="Recency",
 nbins=30,
 color="CustomerSegment",
 title="Recency Distribution",
 template="plotly_white"
)

# =====================================================
# MONETARY DISTRIBUTION
# =====================================================

fig_monetary = px.histogram(
 rfm,
 x="Monetary",
 nbins=40,
 color="CustomerSegment",
 title="Monetary Distribution",
 template="plotly_white"
)

left, right = st.columns(2)

with left:
 st.plotly_chart(fig_recency, use_container_width=True)

with right:
 st.plotly_chart(fig_monetary, use_container_width=True)

st.markdown("---")

# =====================================================
# BOX PLOTS
# =====================================================

fig_box1 = px.box(
 rfm,
 x="CustomerSegment",
 y="Recency",
 color="CustomerSegment",
 title="Recency by Segment",
 template="plotly_white"
)

fig_box2 = px.box(
 rfm,
 x="CustomerSegment",
 y="Monetary",
 color="CustomerSegment",
 title="Monetary by Segment",
 template="plotly_white"
)

left, right = st.columns(2)

with left:
 st.plotly_chart(fig_box1, use_container_width=True)

with right:
 st.plotly_chart(fig_box2, use_container_width=True)

st.markdown("---")

# =====================================================
# TREEMAP
# =====================================================

fig_tree = px.treemap(
 rfm,
 path=["CustomerSegment"],
 values="Monetary",
 color="Monetary",
 title="Revenue Contribution by Segment"
)

st.plotly_chart(fig_tree, use_container_width=True)

st.markdown("---")

# =====================================================
# CLUSTER SUMMARY
# =====================================================

st.header(" Cluster Summary")

cluster_summary = (
 rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]]
 .mean()
 .round(2)
 .reset_index()
)

st.dataframe(
 cluster_summary,
 use_container_width=True,
 hide_index=True
)

st.markdown("---")
# =====================================================
# AI BUSINESS INSIGHTS
# =====================================================

st.header(" AI Customer Insights")

best_segment = (
 rfm.groupby("CustomerSegment")["Monetary"]
 .mean()
 .idxmax()
)

highest_value = (
 rfm.groupby("CustomerSegment")["Monetary"]
 .mean()
 .max()
)

lowest_segment = (
 rfm.groupby("CustomerSegment")["Monetary"]
 .mean()
 .idxmin()
)

col1, col2 = st.columns(2)

with col1:

 st.success(f"""
### Highest Value Segment

**{best_segment}**

Average Spend: ₹ {highest_value:,.2f}
""")

 st.success(f"""
### Total Customers

**{total_customers:,}**
""")

with col2:

 st.warning(f"""
### Lowest Value Segment

**{lowest_segment}**
""")

 st.info(f"""
### Average Customer Value

₹ {avg_monetary:,.2f}
""")

st.markdown("---")

# =====================================================
# SEGMENT RECOMMENDATIONS
# =====================================================

st.header(" AI Recommendations")

recommendations = []

recommendations.append(
 f" Focus marketing campaigns on **{best_segment}** customers."
)

recommendations.append(
 " Offer loyalty rewards to Regular customers to increase repeat purchases."
)

recommendations.append(
 " Re-engage At-Risk customers using personalized email campaigns."
)

recommendations.append(
 " Provide premium membership benefits for Loyal customers."
)

recommendations.append(
 " Recommend complementary products to increase basket value."
)

for rec in recommendations:
 st.success(rec)

st.markdown("---")

# =====================================================
# TOP CUSTOMERS
# =====================================================

st.header(" Top 20 Customers")

top20 = (
 rfm.sort_values("Monetary", ascending=False)
 .head(20)
)

st.dataframe(
 top20,
 use_container_width=True,
 hide_index=True
)

st.markdown("---")

# =====================================================
# CUSTOMER SEARCH
# =====================================================

st.header(" Search Customer")

customer_ids = sorted(rfm["CustomerID"].unique())

selected_customer = st.selectbox(
 "Select Customer ID",
 customer_ids
)

customer = rfm[
 rfm["CustomerID"] == selected_customer
]

st.dataframe(
 customer,
 use_container_width=True,
 hide_index=True
)

st.markdown("---")

# =====================================================
# FULL DATASET
# =====================================================

st.header(" Customer Segmentation Dataset")

st.dataframe(
 rfm,
 use_container_width=True,
 height=450
)

st.markdown("---")

# =====================================================
# DOWNLOAD REPORT
# =====================================================

st.header(" Download Report")

st.download_button(
 label=" Download Customer Segmentation Report",
 data=rfm.to_csv(index=False),
 file_name="customer_segmentation.csv",
 mime="text/csv"
)

st.markdown("---")

# =====================================================
# RFM STATISTICS
# =====================================================

st.header(" RFM Statistics")

st.dataframe(
 rfm[["Recency","Frequency","Monetary"]].describe().round(2),
 use_container_width=True
)

st.markdown("---")

# =====================================================
# ABOUT THIS PAGE
# =====================================================

st.header(" About Customer Segmentation")

st.write("""

This dashboard segments customers using **RFM Analysis**
and **K-Means Clustering**.

### RFM Meaning

- **Recency** → Days since last purchase
- **Frequency** → Number of purchases
- **Monetary** → Total amount spent

### Customer Segments

- Loyal Customers
- Regular Customers
- At-Risk Customers
- VIP Customers

This analysis helps businesses improve marketing campaigns,
increase customer retention, and maximize revenue.

""")

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
<hr>

<div style="text-align:center">

### Customer Segmentation Dashboard

Built with using Streamlit, Plotly & Scikit-Learn

 2026 RetailPulse

</div>

""",
unsafe_allow_html=True
)