"""Load the shared RetailPulse visual theme."""
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "style.css"


def apply_theme() -> None:
    if CSS_PATH.exists():
        st.markdown(f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
