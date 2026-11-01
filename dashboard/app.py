"""
Movie & OTT Platform Content Analysis - Executive Overview
Main entrypoint for the Streamlit Multi-Page Dashboard.
Clean, human-crafted Data Science analytics system.
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import streamlit as st
import pandas as pd
from dashboard.utils import (
    get_data,
    apply_custom_css,
    render_sidebar_filters,
    render_page_header
)
from src.analysis import (
    get_overall_kpis,
    get_platform_distribution,
    plot_platform_content_bars,
    plot_release_trends
)

# ── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="OTT Content Analytics | Executive Overview",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Base Stylesheet ─────────────────────────────────────────────────────────
apply_custom_css()

# ── Header ──────────────────────────────────────────────────────────────────
render_page_header(
    title="Executive Overview",
    description="Comparative analysis of catalog composition, format strategy, and historical release trajectories across Netflix, Amazon Prime Video, Disney+, and Hulu (22,998 titles)."
)

# ── Load data & sidebar ──────────────────────────────────────────────────────
raw_df = get_data()
filtered_df, filter_state = render_sidebar_filters(raw_df)

if filtered_df.empty:
    st.warning("No titles match your selected filter criteria. Please adjust your sidebar filters.")
    st.stop()

# ── 1. Executive Summary Metrics ─────────────────────────────────────────────
kpis = get_overall_kpis(filtered_df)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(
        label="Total Titles",
        value=f"{kpis['total_titles']:,}",
        help="Total records matching active filters"
    )
with col2:
    st.metric(
        label="Movies",
        value=f"{kpis['total_movies']:,}",
        delta=f"{kpis['movie_pct']}% of catalog"
    )
with col3:
    st.metric(
        label="TV Shows",
        value=f"{kpis['total_tv_shows']:,}",
        delta=f"{kpis['tv_pct']}% of catalog",
        delta_color="inverse"
    )
with col4:
    st.metric(
        label="Active Platforms",
        value=f"{kpis['platforms_count']} Services",
        help="Number of platforms in active filter"
    )
with col5:
    st.metric(
        label="Unique Titles",
        value=f"{kpis['unique_titles']:,}",
        help="Distinct title names across catalogs"
    )

st.divider()

# ── 2. Catalog Architecture & Trajectory ─────────────────────────────────────
col_left, col_right = st.columns([1.1, 1.3])

with col_left:
    st.subheader("Catalog Size & Format Composition")
    fig_bars = plot_platform_content_bars(filtered_df)
    st.plotly_chart(fig_bars, use_container_width=True)

with col_right:
    st.subheader("Historical Release Trajectory")
    fig_trends = plot_release_trends(filtered_df, min_year=filter_state['years'][0])
    st.plotly_chart(fig_trends, use_container_width=True)

st.divider()

# ── 3. Platform Breakdown Matrix ─────────────────────────────────────────────
st.subheader("Platform Breakdown Matrix")

plat_summary = get_platform_distribution(filtered_df)
st.dataframe(
    plat_summary,
    use_container_width=True,
    hide_index=True,
    column_config={
        "platform": st.column_config.TextColumn("Platform", width="medium"),
        "Movie": st.column_config.NumberColumn("Movies", format="%d"),
        "TV Show": st.column_config.NumberColumn("TV Shows", format="%d"),
        "Total": st.column_config.NumberColumn("Total Titles", format="%d"),
        "Movie %": st.column_config.NumberColumn("Movie Share", format="%.1f%%"),
        "TV Show %": st.column_config.NumberColumn("TV Show Share", format="%.1f%%")
    }
)

st.caption("Use the sidebar navigation to examine genre distributions, geographic production hubs, and individual title records.")
