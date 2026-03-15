from html import escape

import streamlit as st

from services.tmdb_api import POSTER_BASE_URL


def _truncate(text, max_chars=110):
    if not text:
        return "No summary available."
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def movie_card(
    movie,
    selected=False,
    key_suffix="",
    action_label=None,
    explanation=None,
    badge=None,
):
    poster_url = (
        f"{POSTER_BASE_URL}{movie.get('poster_path', '')}"
        if movie.get("poster_path")
        else "https://via.placeholder.com/300x450?text=No+Image"
    )
    title = movie.get("title", "Unknown")
    rating = float(movie.get("vote_average", 0) or 0)
    overview = movie.get("overview", "")
    summary = _truncate(overview)
    selected_class = " is-selected" if selected else ""
    safe_title = escape(title)
    safe_overview = escape(overview or "No summary available.")
    # Do NOT escape summary or explanation, as they are plain text, not HTML
    safe_summary = summary



    html = f'''
    <div class="movie-card{selected_class}">
        <div class="movie-poster-wrap">
            <img class="movie-poster" src="{poster_url}" alt="{safe_title} poster">
            <div class="movie-overview-hover">{safe_overview}</div>
        </div>
        <div class="movie-meta">
            <div class="movie-title">{safe_title}</div>
            <div class="movie-rating">TMDB Rating: {rating:.1f}/10</div>
            <div class="movie-summary" title="{safe_overview}">{safe_summary}</div>
        </div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)

    if not action_label:
        return False

    return st.button(
        action_label,
        key=f"card_action_{movie['id']}_{key_suffix}",
        width="stretch",
        type="primary" if selected else "secondary",
    )
