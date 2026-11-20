import streamlit as st

st.set_page_config(
    page_title="RetailPulse | Retail Intelligence",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_global_styles():
    try:
        with open("assets/style.css", encoding="utf-8") as css_file:
            st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_global_styles()

pages = [
    st.Page("pages/Home.py", title="Overview", default=True),
    st.Page("pages/_Sales_Analytics.py", title="Sales Analytics"),
    st.Page("pages/Customer_Segmentation.py", title="Customer Intelligence"),
    st.Page("pages/Demand_Forecasting.py", title="Demand Forecasting"),
    st.Page("pages/Inventory_Optimization.py", title="Inventory"),
    st.Page("pages/AI_Insights.py", title="Business Insights"),
]

current_page = st.navigation(pages, position="top")
current_page.run()
