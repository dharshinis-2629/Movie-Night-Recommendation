import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    # Load local dev secrets without requiring users to export env vars manually.
    load_dotenv(override=False)

import streamlit as st

from database.db import create_tables
from components.search_bar import search_bar
from pages.login import login_page
from pages.onboarding import onboarding_page
from pages.home import home_page
from pages.recommendations import recommendations_page
from pages.rate_movies import rate_movies_page
from pages.groups import groups_page

st.set_page_config(
    page_title="Movie Night Recommender",
    page_icon=":clapper:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme state (CSS-driven) -----------------------------------------------------
if "theme_toggle" not in st.session_state:
    st.session_state.theme_toggle = False
theme = "light" if st.session_state.theme_toggle else "dark"
st.session_state.theme = theme

# Require a TMDB key; without it most pages cannot function and will fail silently.
if not os.getenv("TMDB_API_KEY"):
    st.error(
        "Missing required environment variable `TMDB_API_KEY`.\n\n"
        "Add it to a local `.env` file or set it in your shell, then restart Streamlit.\n"
        "Example (PowerShell): `$env:TMDB_API_KEY='your_key_here'`"
    )
    st.stop()

# Initialize database
create_tables()

# Load CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Runtime theme overrides (no JS/iframes; last style wins on rerun)
LIGHT_THEME_CSS = """
/* App chrome */
body, .stApp { background: #f3f6fb !important; color: #0b1220 !important; }
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(circle at 18% 10%, rgba(56, 189, 248, 0.16), transparent 34%),
    radial-gradient(circle at 82% 20%, rgba(59, 130, 246, 0.14), transparent 36%),
    linear-gradient(180deg, #f7faff, #eef3fb) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  color: #0b1220 !important;
  border-right: 1px solid rgba(15, 23, 42, 0.10) !important;
}
[data-testid="stSidebar"] > div:first-child {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(236, 242, 250, 0.92)) !important;
}
.sidebar-brand { color: #0f172a !important; }

/* Sidebar widget labels (toggle text, etc.) */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
  color: #0b1220 !important;
}

/* Headings */
.hero-heading, .home-section-title, .search-section-title, .rate-page-title { color: #0b1220 !important; }
.hero-subheading, .rate-section-label { color: rgba(15, 23, 42, 0.68) !important; }

/* Inputs */
div[data-baseweb="input"] > div {
  background: rgba(255, 255, 255, 0.86) !important;
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
  border-radius: 14px !important;
}
div[data-baseweb="input"] > div:focus-within {
  border-color: rgba(37, 99, 235, 0.32) !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14) !important;
}
div[data-baseweb="input"] input {
  color: #0b1220 !important;
}
div[data-baseweb="input"] input::placeholder {
  color: rgba(15, 23, 42, 0.45) !important;
}
div[data-baseweb="input"] svg,
div[data-baseweb="input"] path {
  color: rgba(15, 23, 42, 0.55) !important;
  fill: rgba(15, 23, 42, 0.55) !important;
}

/* Selects (used in Groups page) */
div[data-baseweb="select"] > div {
  background: rgba(255, 255, 255, 0.90) !important;
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
  border-radius: 14px !important;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06) !important;
}
div[data-baseweb="select"] * {
  color: #0b1220 !important;
}
div[data-baseweb="select"] svg,
div[data-baseweb="select"] path {
  color: rgba(15, 23, 42, 0.60) !important;
  fill: rgba(15, 23, 42, 0.60) !important;
}
/* BaseWeb select dropdown menu (renders in a portal; selectors vary by Streamlit/BaseWeb version) */
div[role="listbox"],
ul[role="listbox"],
div[data-baseweb="menu"],
ul[data-baseweb="menu"] {
  background: rgba(255, 255, 255, 0.98) !important;
  border: 1px solid rgba(15, 23, 42, 0.14) !important;
  border-radius: 14px !important;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12) !important;
}
div[role="option"],
li[role="option"] {
  color: #0b1220 !important;
  background: transparent !important;
}
div[role="option"][aria-selected="true"],
li[role="option"][aria-selected="true"] {
  background: rgba(37, 99, 235, 0.10) !important;
}
div[role="option"]:hover,
li[role="option"]:hover {
  background: rgba(37, 99, 235, 0.08) !important;
}
/* Popover wrapper itself (Streamlit select menu is usually inside this) */
div[data-baseweb="popover"] {
  color: #0b1220 !important;
}
div[data-baseweb="popover"] > div {
  background: rgba(255, 255, 255, 0.98) !important;
  border-radius: 14px !important;
}
div[data-baseweb="popover"] [role="menu"],
div[data-baseweb="popover"] [role="listbox"],
div[data-baseweb="popover"] div[data-baseweb="menu"],
div[data-baseweb="popover"] ul[data-baseweb="menu"] {
  background: rgba(255, 255, 255, 0.98) !important;
  border: 1px solid rgba(15, 23, 42, 0.14) !important;
  border-radius: 14px !important;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12) !important;
}
div[data-baseweb="popover"] [role="menuitem"],
div[data-baseweb="popover"] [role="option"] {
  color: #0b1220 !important;
  background: transparent !important;
}
div[data-baseweb="popover"] [role="menuitem"]:hover,
div[data-baseweb="popover"] [role="option"]:hover {
  background: rgba(37, 99, 235, 0.08) !important;
}

/* Last resort: BaseWeb renders menus inside a "layer" portal in some versions. */
div[data-baseweb="layer"] {
  color: #0b1220 !important;
}
div[data-baseweb="layer"] > div {
  background: rgba(255, 255, 255, 0.98) !important;
  border: 1px solid rgba(15, 23, 42, 0.14) !important;
  border-radius: 14px !important;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12) !important;
}
div[data-baseweb="layer"] [role="listbox"],
div[data-baseweb="layer"] [role="menu"],
div[data-baseweb="layer"] div[data-baseweb="menu"],
div[data-baseweb="layer"] ul[data-baseweb="menu"] {
  background: rgba(255, 255, 255, 0.98) !important;
}
div[data-baseweb="layer"] [role="option"],
div[data-baseweb="layer"] [role="menuitem"],
div[data-baseweb="layer"] li[role="option"] {
  color: #0b1220 !important;
  background: transparent !important;
}
div[data-baseweb="layer"] [role="option"]:hover,
div[data-baseweb="layer"] [role="menuitem"]:hover,
div[data-baseweb="layer"] li[role="option"]:hover {
  background: rgba(37, 99, 235, 0.08) !important;
}

/* Widget labels in main area (Streamlit renders these above inputs) */
section[data-testid="stMain"] [data-testid="stWidgetLabel"] * {
  color: rgba(15, 23, 42, 0.78) !important;
}
section[data-testid="stMain"] label,
section[data-testid="stMain"] label * {
  color: rgba(15, 23, 42, 0.78) !important;
}

/* Tabs (Groups page) */
div[data-testid="stTabs"] button {
  color: rgba(15, 23, 42, 0.70) !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: #0b1220 !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  background-color: rgba(37, 99, 235, 0.70) !important;
}

/* Global search: hard override (it was still picking up dark styles) */
div[class*="st-key-global_search"] div[data-baseweb="input"] > div {
  background: rgba(255, 255, 255, 0.92) !important;
  border-color: rgba(15, 23, 42, 0.14) !important;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06) !important;
}
div[class*="st-key-global_search"] div[data-baseweb="input"] input {
  color: #0b1220 !important;
}
div[class*="st-key-global_search"] div[data-baseweb="input"] input::placeholder {
  color: rgba(15, 23, 42, 0.45) !important;
}
div[class*="st-key-global_search_form"] div[data-testid="stFormSubmitButton"] button,
div[class*="st-key-global_search_form"] button[type="submit"] {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.92), rgba(219, 234, 254, 0.92)) !important;
  border: 1px solid rgba(37, 99, 235, 0.22) !important;
  color: #0b1220 !important;
}
/* Target the actual Search submit button deterministically (via its key wrapper). */
div[class*="st-key-global_search_submit"] button {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.92), rgba(219, 234, 254, 0.92)) !important;
  border: 1px solid rgba(37, 99, 235, 0.22) !important;
  color: #0b1220 !important;
}
div[class*="st-key-global_search_submit"] button p,
div[class*="st-key-global_search_submit"] button span {
  color: #0b1220 !important;
}
div[class*="st-key-global_search_form"] div[data-testid="stFormSubmitButton"] button p,
div[class*="st-key-global_search_form"] div[data-testid="stFormSubmitButton"] button span {
  color: #0b1220 !important;
}
div[class*="st-key-global_search_form"] div[data-testid="stFormSubmitButton"] button:hover {
  filter: brightness(0.98) !important;
}

/* Main buttons (avoid touching rating-star buttons) */
section[data-testid="stMain"] div[data-testid="stButton"] > button {
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
  background: rgba(255, 255, 255, 0.86) !important;
  color: #0b1220 !important;
}
section[data-testid="stMain"] div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.92), rgba(191, 219, 254, 0.72)) !important;
  border-color: rgba(37, 99, 235, 0.22) !important;
  color: #0b1220 !important;
}
section[data-testid="stMain"] div[data-testid="stButton"] > button[kind="secondary"] {
  background: rgba(255, 255, 255, 0.86) !important;
  border-color: rgba(15, 23, 42, 0.14) !important;
}

/* Sidebar nav buttons */
[data-testid="stSidebar"] div[data-testid="stButton"] > button {
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
  background: rgba(255, 255, 255, 0.80) !important;
  color: #0b1220 !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.92), rgba(219, 234, 254, 0.90)) !important;
  border-color: rgba(37, 99, 235, 0.22) !important;
  color: #0b1220 !important;
}

/* Cards */
.movie-card {
  border: 1px solid rgba(15, 23, 42, 0.10) !important;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(241, 245, 249, 0.98)) !important;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.10) !important;
}
.movie-card:hover { box-shadow: 0 14px 34px rgba(15, 23, 42, 0.14) !important; }
.movie-overview-hover { background: rgba(255, 255, 255, 0.96) !important; color: #0b1220 !important; }
.movie-rating { color: rgba(15, 23, 42, 0.62) !important; }
.movie-explanation { color: rgba(2, 132, 199, 0.95) !important; }

/* Rate Movies page: override custom dark surfaces */
.rate-row-shell + div[data-testid="stVerticalBlockBorderWrapper"],
.rated-panel-shell + div[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1px solid rgba(15, 23, 42, 0.10) !important;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(241, 245, 249, 0.96)) !important;
  box-shadow: 0 18px 38px rgba(15, 23, 42, 0.10) !important;
}
.rate-poster-card {
  border: 1px solid rgba(15, 23, 42, 0.12) !important;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(241, 245, 249, 0.94)) !important;
}
.rate-movie-title { color: #0b1220 !important; }
.rate-summary { color: rgba(15, 23, 42, 0.72) !important; }
.rating-stat-label { color: rgba(15, 23, 42, 0.62) !important; }
.rating-stat-value { color: #0b1220 !important; }
.rating-stat-sub { color: rgba(15, 23, 42, 0.58) !important; }
.star-rating-caption { color: rgba(15, 23, 42, 0.62) !important; }
.star-rating-value { color: #0b1220 !important; }
.star-rating-note { color: rgba(15, 23, 42, 0.55) !important; }

/* Rate Movies: stat cards should be light surfaces in light theme */
.rate-meta-block {
  border: 1px solid rgba(15, 23, 42, 0.10) !important;
  background: rgba(255, 255, 255, 0.92) !important;
  box-shadow: 0 12px 26px rgba(15, 23, 42, 0.08) !important;
}
.rate-detail-divider {
  background: rgba(15, 23, 42, 0.10) !important;
}

/* Rated list cards */
.rated-item-card {
  border: 1px solid rgba(15, 23, 42, 0.10) !important;
  background: rgba(255, 255, 255, 0.92) !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.24), 0 10px 22px rgba(15, 23, 42, 0.06) !important;
}
.rated-item-title { color: #0b1220 !important; }
.rated-item-sub { color: rgba(15, 23, 42, 0.55) !important; }
"""

DARK_THEME_CSS = """
body, .stApp { background-color: #0f172a !important; color: #f8fafc !important; }
[data-testid="stSidebar"] { border-right: 1px solid rgba(148, 163, 184, 0.12) !important; }
.sidebar-brand { color: #f8fafc !important; }
.hero-heading, .home-section-title, .search-section-title, .rate-page-title { color: #f8fafc !important; }
.hero-subheading { color: #bfd0ea !important; }
.rate-section-label { color: #dbeafe !important; }
[data-testid="stSidebar"] div[data-testid="stButton"] > button {
  border: 1px solid rgba(148, 163, 184, 0.16) !important;
  background: rgba(15, 23, 42, 0.72) !important;
  color: #f8fafc !important;
}
[data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"] {
  background: linear-gradient(135deg, #1d4ed8, #0f172a) !important;
  border-color: rgba(59, 130, 246, 0.45) !important;
}
.movie-card {
  border: 1px solid rgba(148, 163, 184, 0.18) !important;
  background: linear-gradient(180deg, rgba(30, 41, 59, 0.98), rgba(15, 23, 42, 0.98)) !important;
  box-shadow: 0 10px 24px rgba(2, 6, 23, 0.32) !important;
}
.movie-card:hover { box-shadow: 0 4px 8px rgba(0, 255, 0, 0.3) !important; }
.movie-overview-hover { background: rgba(2, 6, 23, 0.94) !important; color: #e2e8f0 !important; }
.movie-rating { color: #cbd5e1 !important; }
.movie-explanation { color: #93c5fd !important; }
"""

st.markdown(
    f"<style>{LIGHT_THEME_CSS if theme == 'light' else DARK_THEME_CSS}</style>",
    unsafe_allow_html=True,
)

# App logic
if 'user' not in st.session_state:
    # Hide sidebar on login page
    st.markdown('<style>[data-testid="stSidebar"] { display: none !important; }</style>', unsafe_allow_html=True)
    login_page()
else:
    user = st.session_state.user
    from database.db import SessionLocal
    from database.models import UserLikedMovie
    db = SessionLocal()
    liked = db.query(UserLikedMovie).filter(UserLikedMovie.user_id == user.user_id).all()
    db.close()

    if not liked:
        onboarding_page()
    else:
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Home"

        # Always show sidebar, no hide option
        st.markdown('<style>[data-testid="stSidebar"] { display: block !important; }</style>', unsafe_allow_html=True)
        with st.sidebar:
            st.markdown('<div class="sidebar-brand">Movie Night</div>', unsafe_allow_html=True)
            st.toggle("Light theme", key="theme_toggle")
            # Streamlit renders toggle label via nested spans; enforce contrast in light theme.
            if theme == "light":
                st.markdown(
                    "<style>"
                    "[data-testid='stSidebar'] div[data-testid='stToggle'] * { color: #0b1220 !important; }"
                    "</style>",
                    unsafe_allow_html=True,
                )

            for label in ["Home", "Recommendations", "Rate Movies", "Groups"]:
                if st.button(
                    label,
                    key=f"nav_{label}",
                    use_container_width=True,
                    type="primary" if st.session_state.current_page == label else "secondary",
                ):
                    st.session_state.current_page = label
                    st.rerun()

        page = st.session_state.current_page
        if page != "Rate Movies":
            search_bar()
        if page == "Home":
            home_page()
        elif page == "Recommendations":
            recommendations_page()
        elif page == "Rate Movies":
            rate_movies_page()
        elif page == "Groups":
            groups_page()

        if st.sidebar.button("Logout", key="logout"):
            del st.session_state.user
            st.rerun()
