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

# Initialize database
create_tables()

# Load CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# App logic
if 'user' not in st.session_state:
    login_page()
else:
    user = st.session_state.user
    # Check if onboarding complete
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

        with st.sidebar:
            st.markdown('<div class="sidebar-brand">Movie Night</div>', unsafe_allow_html=True)
            for label in ["Home", "Recommendations", "Rate Movies", "Groups"]:
                if st.button(
                    label,
                    key=f"nav_{label}",
                    width="stretch",
                    type="primary" if st.session_state.current_page == label else "secondary",
                ):
                    st.session_state.current_page = label
                    st.rerun()

        page = st.session_state.current_page
        # Only show global search bar on pages except Rate Movies
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
