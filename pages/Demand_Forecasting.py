import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

# --------------------------------------------------
# HIDE STREAMLIT DEFAULT MENU
# --------------------------------------------------

hide_menu = """
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}

</style>
"""

st.markdown(hide_menu, unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown("""
<h1 style='text-align:center;color:#2563EB;'>
 Demand Forecasting
</h1>

<h3 style='text-align:center;color:gray;'>
AI Sales Prediction using Prophet
</h3>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# LOAD FORECAST DATA
# --------------------------------------------------

@st.cache_data
def load_forecast():

    df = pd.read_csv(
        "data/processed/sales_forecast.csv"
    )

    df["ds"] = pd.to_datetime(df["ds"])

    return df

forecast = load_forecast()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

future_days = len(forecast)

forecast_sales = forecast["yhat"].sum()

max_sales = forecast["yhat"].max()

avg_sales = forecast["yhat"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        " Forecast Days",
        future_days
    )

with c2:
    st.metric(
        " Expected Revenue",
        f"₹ {forecast_sales:,.0f}"
    )

with c3:
    st.metric(
        " Peak Forecast",
        f"₹ {max_sales:,.0f}"
    )

with c4:
    st.metric(
        " Average Daily Sales",
        f"₹ {avg_sales:,.0f}"
    )

st.markdown("---")

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.subheader("Forecast Dataset")

st.dataframe(
    forecast.head(),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
# =====================================================
# FORECAST CHART
# =====================================================

st.header(" Sales Forecast")

fig = go.Figure()

# Predicted Sales
fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        mode="lines",
        name="Forecast",
        line=dict(color="#2563EB", width=3)
    )
)

# Upper Confidence
fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_upper"],
        mode="lines",
        line=dict(width=0),
        showlegend=False
    )
)

# Lower Confidence
fig.add_trace(
    go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat_lower"],
        mode="lines",
        fill="tonexty",
        fillcolor="rgba(37,99,235,0.15)",
        line=dict(width=0),
        name="Confidence Interval"
    )
)

fig.update_layout(
    title="Demand Forecast",
    xaxis_title="Date",
    yaxis_title="Predicted Sales",
    hovermode="x unified",
    template="plotly_white",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =====================================================
# NEXT 30 DAYS FORECAST
# =====================================================

st.header(" Next 30 Days Forecast")

future = forecast.tail(30)

fig_future = px.line(
    future,
    x="ds",
    y="yhat",
    markers=True,
    title="Next 30 Days Sales Prediction",
    template="plotly_white"
)

fig_future.update_traces(
    line=dict(color="#16A34A", width=3)
)

st.plotly_chart(
    fig_future,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# MONTHLY FORECAST
# =====================================================

st.header(" Monthly Forecast")

monthly = forecast.copy()

monthly["Month"] = monthly["ds"].dt.to_period("M").astype(str)

monthly = (
    monthly.groupby("Month")["yhat"]
    .sum()
    .reset_index()
)

fig_month = px.bar(
    monthly,
    x="Month",
    y="yhat",
    title="Monthly Forecast Revenue",
    text_auto=".2s",
    template="plotly_white"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DAILY SALES DISTRIBUTION
# =====================================================

st.header(" Forecast Distribution")

fig_hist = px.histogram(
    forecast,
    x="yhat",
    nbins=30,
    title="Distribution of Predicted Daily Sales",
    template="plotly_white"
)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

st.markdown("---")

# =====================================================
# FORECAST TABLE
# =====================================================

st.header(" Forecast Data")

st.dataframe(
    forecast,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
# =====================================================
# FORECAST SUMMARY
# =====================================================

st.header(" Forecast Summary")

highest_day = forecast.loc[
    forecast["yhat"].idxmax()
]

lowest_day = forecast.loc[
    forecast["yhat"].idxmin()
]

col1, col2 = st.columns(2)

with col1:

    st.success(f"""
###  Highest Forecast Day

**Date:** {highest_day['ds'].date()}

**Predicted Sales:** ₹ {highest_day['yhat']:,.2f}
""")

    st.success(f"""
###  Total Forecast Revenue

₹ {forecast['yhat'].sum():,.2f}
""")

with col2:

    st.warning(f"""
###  Lowest Forecast Day

**Date:** {lowest_day['ds'].date()}

**Predicted Sales:** ₹ {lowest_day['yhat']:,.2f}
""")

    st.info(f"""
###  Average Daily Forecast

₹ {forecast['yhat'].mean():,.2f}
""")

st.markdown("---")

# =====================================================
# AI BUSINESS INSIGHTS
# =====================================================

st.header(" AI Forecast Insights")

growth = (
    (forecast.iloc[-1]["yhat"] - forecast.iloc[0]["yhat"])
    / forecast.iloc[0]["yhat"]
) * 100

recommendations = []

if growth > 5:
    recommendations.append(
        " Sales are expected to grow. Prepare additional inventory."
    )
elif growth < -5:
    recommendations.append(
        " Sales may decline. Focus on promotional campaigns."
    )
else:
    recommendations.append(
        " Sales are expected to remain relatively stable."
    )

recommendations.append(
    " Review inventory weekly based on forecasted demand."
)

recommendations.append(
    " Ensure high-demand products remain in stock."
)

recommendations.append(
    " Launch promotional offers during low-demand periods."
)

recommendations.append(
    " Update the forecasting model monthly with new sales data."
)

for item in recommendations:
    st.success(item)

st.markdown("---")

# =====================================================
# FORECAST STATISTICS
# =====================================================

st.header(" Forecast Statistics")

st.dataframe(
    forecast[["yhat", "yhat_lower", "yhat_upper"]]
        .describe()
        .round(2),
    use_container_width=True
)

st.markdown("---")

# =====================================================
# DOWNLOAD FORECAST
# =====================================================

st.header(" Download Forecast Report")

st.download_button(
    label=" Download Forecast CSV",
    data=forecast.to_csv(index=False),
    file_name="sales_forecast.csv",
    mime="text/csv"
)

st.markdown("---")

# =====================================================
# ABOUT DEMAND FORECASTING
# =====================================================

st.header(" About This Page")

st.write("""
This dashboard forecasts future retail sales using **Facebook Prophet**, a time-series forecasting model.

### Features

-  Future Sales Prediction
-  Next 30 Days Forecast
-  Monthly Revenue Forecast
-  Confidence Interval
-  AI Business Insights

### Benefits

- Inventory Planning
- Demand Prediction
- Revenue Estimation
- Business Decision Support
""")

st.markdown("---")

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
<hr>

<div style="text-align:center">

###  Demand Forecasting Dashboard

Built with  using Streamlit, Plotly & Prophet

 2026 RetailPulse

</div>

""",
unsafe_allow_html=True
)