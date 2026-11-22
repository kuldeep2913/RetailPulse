"""Central configuration for the RetailPulse dashboard."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Shared visual tokens. Keep these aligned with assets/style.css.
COLORS = {
    "ink": "#20232B",
    "muted": "#747987",
    "canvas": "#F4F3EF",
    "surface": "#FFFFFF",
    "lime": "#D7F36A",
    "lavender": "#DCD6FF",
    "dark": "#242631",
    "border": "#E8E6E0",
    "accent": "#687A35",
}
SEGMENT_COLORS = ["#D7F36A", "#DCD6FF", "#A9C5E8", "#F2C9A5", "#B8D9C7"]
ABC_COLORS = {"A": "#D7F36A", "B": "#DCD6FF", "C": "#A9C5E8"}
TEAM = [
    {"name": "Kuldeep Yadav", "role": "Project Lead", "degree": "B.Tech Computer Science Engineering", "college": "Shivalik College of Engineering"},
    {"name": "Prashant", "role": "Team Member", "degree": "B.Tech Computer Science Engineering", "college": "Shivalik College of Engineering"},
]
