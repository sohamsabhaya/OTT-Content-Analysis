"""
Page 2: Genre & Content Analysis
Explores genre prevalence, statistical runtime distributions, and TV season dynamics.
Clean, human-crafted Data Science analytics system.
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import streamlit as st
from dashboard.utils import (
    get_data,
    apply_custom_css,
    render_sidebar_filters,
    render_page_header
)
from src.analysis import (
    get_top_genres,
    plot_top_genres_bar,
    plot_genre_by_platform_stacked,
    get_movie_duration_stats,
    plot_movie_duration_histogram,
    plot_movie_duration_boxplot,
    get_tv_season_stats,
    plot_tv_season_distribution
)

st.set_page_config(
    page_title="Genre & Runtime Dynamics | OTT Analytics",
    layout="wide"
)

apply_custom_css()

render_page_header(
    title="Genre & Runtime Dynamics",
    description="Evaluating categorical genre concentration, statistical dispersion of movie durations, and television renewal structures across platforms."
)

raw_df = get_data()
filtered_df, filter_state = render_sidebar_filters(raw_df)

if filtered_df.empty:
    st.warning("No titles match your selected filter criteria. Please adjust your sidebar filters.")
    st.stop()

# ── 1. Genre Prevalence & Platform Comparison ────────────────────────────────
st.subheader("Genre Prevalence & Platform Specialization")

col_slider, _ = st.columns([1.2, 3])
with col_slider:
    top_n_genres = st.slider("Number of Top Genres to Display:", min_value=5, max_value=20, value=10)

col_g1, col_g2 = st.columns([1, 1.3])
with col_g1:
    fig_genre_bar = plot_top_genres_bar(filtered_df, top_n=top_n_genres)
    st.plotly_chart(fig_genre_bar, use_container_width=True)

with col_g2:
    fig_genre_stack = plot_genre_by_platform_stacked(filtered_df, top_n=top_n_genres)
    st.plotly_chart(fig_genre_stack, use_container_width=True)

st.divider()

# ── 2. Movie Duration Analysis (Central Tendency & Dispersion) ────────────────
st.subheader("Movie Duration Analysis: Central Tendency & Dispersion")

movie_stats = get_movie_duration_stats(filtered_df)

if movie_stats['count'] > 0:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Sample Size",       f"{movie_stats['count']:,} Movies")
    c2.metric("Mean Runtime",      f"{movie_stats['mean']} min")
    c3.metric("Median Runtime",    f"{movie_stats['median']} min")
    c4.metric("Std Deviation",     f"{movie_stats['std']} min")
    c5.metric("Interquartile Range", f"{movie_stats['iqr']} min")
    c6.metric("Min – Max",         f"{movie_stats['min']} – {movie_stats['max']} min")

    col_dur1, col_dur2 = st.columns(2)
    with col_dur1:
        fig_box = plot_movie_duration_boxplot(filtered_df)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_dur2:
        fig_hist = plot_movie_duration_histogram(filtered_df)
        st.plotly_chart(fig_hist, use_container_width=True)
else:
    st.info("No Movies currently in active filter selection. Enable 'Movie' in the sidebar filters to inspect duration distributions.")

st.divider()

# ── 3. TV Show Season Distribution ───────────────────────────────────────────
st.subheader("TV Show Season Longevity & Structure")

tv_stats = get_tv_season_stats(filtered_df)

if tv_stats['total_shows'] > 0:
    tc1, tc2, tc3, tc4, tc5 = st.columns(5)
    tc1.metric("Sample Size",     f"{tv_stats['total_shows']:,} Shows")
    tc2.metric("Single Season",   f"{tv_stats['single_season']:,}", f"{tv_stats['single_pct']}% of series")
    tc3.metric("Multi-Season",    f"{tv_stats['multi_season']:,}",  f"{tv_stats['multi_pct']}% renewed")
    tc4.metric("Mean Seasons",    f"{tv_stats['mean_seasons']}")
    tc5.metric("Longest Series",  f"{tv_stats['max_seasons']} Seasons")

    fig_tv_dist = plot_tv_season_distribution(filtered_df)
    st.plotly_chart(fig_tv_dist, use_container_width=True)
else:
    st.info("No TV Shows currently in active filter selection. Enable 'TV Show' in the sidebar filters to inspect season dynamics.")
