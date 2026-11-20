import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    data = pd.read_csv("data/processed/cleaned_retail.csv")
    data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"], errors="coerce")
    data = data.dropna(subset=["InvoiceDate", "TotalPrice"])
    return data

try:
    df = load_data()
except FileNotFoundError:
    st.error("The processed retail dataset could not be found. Check data/processed/cleaned_retail.csv.")
    st.stop()
except Exception as error:
    st.error(f"Unable to load the retail dataset: {error}")
    st.stop()

if df.empty:
    st.warning("There is no valid transaction data to display.")
    st.stop()

# =====================================================
# HERO
# =====================================================

hero_logo, hero_text = st.columns([1, 5], vertical_alignment="center")

with hero_logo:
    try:
        st.image("assets/logo.png", width=115)
    except Exception:
        st.markdown("## RP")

with hero_text:
    st.title("RetailPulse")
    st.caption("AI-powered retail analytics platform")

try:
    st.image("assets/banner.png", use_container_width=True)
except Exception:
    st.info("Explore your retail performance, customers, products, and sales trends.")

st.write(
    "A clear, interactive view of your retail business. Explore the performance "
    "summary below, then switch between trends and product or country insights."
)

# =====================================================
# CORE METRICS — EACH SHOWN ONCE
# =====================================================

total_revenue = df["TotalPrice"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
average_order_value = total_revenue / total_orders if total_orders else 0

st.subheader("Business at a glance")
metric_cols = st.columns(4)

metric_cols[0].metric("Total revenue", f"₹{total_revenue:,.0f}")
metric_cols[1].metric("Orders", f"{total_orders:,}")
metric_cols[2].metric("Customers", f"{total_customers:,}")
metric_cols[3].metric("Average order value", f"₹{average_order_value:,.2f}")

st.divider()

# =====================================================
# INTERACTIVE EXPLORER
# =====================================================

st.subheader("Explore your business")
overview_tab, product_tab, data_tab = st.tabs(
    ["Sales trends", "Products and countries", "Data explorer"]
)

with overview_tab:
    controls = st.columns([1, 1])
    with controls[0]:
        time_view = st.selectbox(
            "Time period",
            ["Monthly", "Daily"],
            key="overview_time_view"
        )
    with controls[1]:
        chart_view = st.selectbox(
            "Chart style",
            ["Line", "Bar"],
            key="overview_chart_view"
        )

    if time_view == "Monthly":
        trend = (
            df.assign(Period=df["InvoiceDate"].dt.to_period("M").dt.to_timestamp())
              .groupby("Period", as_index=False)["TotalPrice"]
              .sum()
        )
        x_title = "Month"
    else:
        trend = (
            df.assign(Period=df["InvoiceDate"].dt.floor("D"))
              .groupby("Period", as_index=False)["TotalPrice"]
              .sum()
        )
        x_title = "Date"

    if chart_view == "Line":
        fig = px.line(
            trend,
            x="Period",
            y="TotalPrice",
            markers=True,
            title=f"{time_view} revenue trend",
            labels={"Period": x_title, "TotalPrice": "Revenue"}
        )
    else:
        fig = px.bar(
            trend,
            x="Period",
            y="TotalPrice",
            title=f"{time_view} revenue",
            labels={"Period": x_title, "TotalPrice": "Revenue"}
        )

    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=15, r=15, t=55, b=15)
    )
    st.plotly_chart(fig, use_container_width=True)

    if not trend.empty:
        best_period = trend.loc[trend["TotalPrice"].idxmax()]
        st.caption(
            f"Highest {time_view.lower()} revenue in the selected view: "
            f"{best_period['Period'].strftime('%d %b %Y')} "
            f"(₹{best_period['TotalPrice']:,.2f})."
        )

with product_tab:
    product_col, country_col = st.columns(2)

    with product_col:
        st.markdown("#### Top products")
        product_sales = (
            df.groupby("Description", dropna=True)["TotalPrice"]
              .sum()
              .nlargest(10)
              .sort_values()
              .reset_index()
        )
        product_fig = px.bar(
            product_sales,
            x="TotalPrice",
            y="Description",
            orientation="h",
            title="Top 10 products by revenue",
            labels={"TotalPrice": "Revenue", "Description": "Product"}
        )
        product_fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(product_fig, use_container_width=True)

    with country_col:
        st.markdown("#### Top countries")
        country_sales = (
            df.groupby("Country", dropna=True)["TotalPrice"]
              .sum()
              .nlargest(10)
              .sort_values()
              .reset_index()
        )
        country_fig = px.bar(
            country_sales,
            x="TotalPrice",
            y="Country",
            orientation="h",
            title="Top 10 countries by revenue",
            labels={"TotalPrice": "Revenue", "Country": "Country"}
        )
        country_fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(country_fig, use_container_width=True)

with data_tab:
    st.markdown("#### Transaction data")
    st.write("Search and sort the underlying transaction records.")
    search_text = st.text_input(
        "Search transactions",
        placeholder="Enter an invoice, country, product, or customer ID"
    )

    filtered = df.copy()
    if search_text.strip():
        query = search_text.strip().lower()
        searchable_columns = [
            column for column in ["InvoiceNo", "Country", "Description", "CustomerID"]
            if column in filtered.columns
        ]
        mask = pd.Series(False, index=filtered.index)
        for column in searchable_columns:
            mask = mask | filtered[column].astype(str).str.lower().str.contains(query, na=False)
        filtered = filtered[mask]

    st.caption(f"Showing {min(len(filtered), 500):,} of {len(filtered):,} matching records.")
    st.dataframe(filtered.head(500), use_container_width=True, hide_index=True)

    st.download_button(
        "Download displayed data (CSV)",
        data=filtered.to_csv(index=False),
        file_name="retailpulse_transactions.csv",
        mime="text/csv"
    )

st.divider()

# =====================================================
# TEAM
# =====================================================

st.subheader("Project team")
team1, team2 = st.columns(2)

with team1:
    st.markdown(
        """
        <div class="team-card">
            <div class="team-role">Project Lead</div>
            <h3>Kuldeep Yadav</h3>
            <p>B.Tech Computer Science Engineering</p>
            <p>Shivalik College of Engineering</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with team2:
    st.markdown(
        """
        <div class="team-card">
            <div class="team-role">Team Member</div>
            <h3>Prashant</h3>
            <p>B.Tech Computer Science Engineering</p>
            <p>Shivalik College of Engineering</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.caption("RetailPulse | Retail intelligence, made actionable")
