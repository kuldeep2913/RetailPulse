"""RetailPulse — retail analytics dashboard entry point."""
import streamlit as st

from core.config import ASSETS_DIR
from ui.theme import apply_theme

st.set_page_config(
    page_title="RetailPulse | Retail Intelligence",
    page_icon=str(ASSETS_DIR / "favicon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()

logo_path = ASSETS_DIR / "logo.png"
if logo_path.exists():
    st.logo(str(logo_path), icon_image=str(ASSETS_DIR / "favicon.png"), size="large")

pages = [
    st.Page("views/overview.py", title="Overview", icon=":material/dashboard:", default=True),
    st.Page("views/sales_analytics.py", title="Sales Analytics", icon=":material/bar_chart:", url_path="sales-analytics"),
    st.Page("views/customer_segmentation.py", title="Customer Intelligence", icon=":material/groups:", url_path="customer-intelligence"),
    st.Page("views/demand_forecasting.py", title="Demand Forecasting", icon=":material/query_stats:", url_path="demand-forecasting"),
    st.Page("views/inventory_optimization.py", title="Inventory", icon=":material/inventory_2:", url_path="inventory"),
    st.Page("views/ai_insights.py", title="Business Insights", icon=":material/lightbulb:", url_path="business-insights"),
]
st.navigation(pages, position="top").run()
