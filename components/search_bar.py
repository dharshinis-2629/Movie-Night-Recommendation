import streamlit as st

from components.movie_card import movie_card
from services.tmdb_api import search_movies


def search_bar():
    st.markdown('<div class="global-search-shell">', unsafe_allow_html=True)
    query = st.text_input(
        "Search movies",
        key="global_search",
        placeholder="Try: space adventure, time travel movies, funny romance...",
        label_visibility="collapsed",
    ).strip()

    if not query:
        st.markdown("</div>", unsafe_allow_html=True)
        return

    results = search_movies(query)
    st.markdown('<div class="search-section-title">Search Results</div>', unsafe_allow_html=True)

    if not results:
        st.info("No matching movies were found.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    cols = st.columns(4)
    for index, movie in enumerate(results[:8]):
        with cols[index % 4]:
            movie_card(
                movie,
                key_suffix=f"search_{index}"
            )

    st.markdown("</div>", unsafe_allow_html=True)
