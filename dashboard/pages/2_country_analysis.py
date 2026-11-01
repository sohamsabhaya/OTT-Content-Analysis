"""
Page 3: Country & Release Trends
Explores geographic production hubs, international catalogs, and multi-decade release trajectories.
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
    get_top_countries,
    plot_top_countries_bar,
    plot_country_choropleth,
    plot_country_platform_comparison,
    plot_release_trends,
    plot_platform_release_trends
)

st.set_page_config(
    page_title="Geographic & Release Trends | OTT Analytics",
    layout="wide"
)

apply_custom_css()

render_page_header(
    title="Geographic Footprint & Release Trajectories",
    description="Mapping international production origins, global content concentration, and multi-decade release volume across streaming catalogs."
)

raw_df = get_data()
filtered_df, filter_state = render_sidebar_filters(raw_df)

if filtered_df.empty:
    st.warning("No titles match your selected filter criteria. Please adjust your sidebar filters.")
    st.stop()

# ── 1. Global Geographic Distribution ────────────────────────────────────────
st.subheader("Global Content Production Footprint")

fig_map = plot_country_choropleth(filtered_df)
st.plotly_chart(fig_map, use_container_width=True)

col_c1, col_c2 = st.columns([1, 1.2])

with col_c1:
    fig_top_c = plot_top_countries_bar(filtered_df, top_n=10)
    st.plotly_chart(fig_top_c, use_container_width=True)

with col_c2:
    fig_c_plat = plot_country_platform_comparison(filtered_df, top_n=8)
    st.plotly_chart(fig_c_plat, use_container_width=True)

st.divider()

# ── 2. Historical Release Velocity ───────────────────────────────────────────
st.subheader("Historical Release Trajectory Over Decades")

start_year = filter_state['years'][0]
col_trend1, col_trend2 = st.columns(2)

with col_trend1:
    fig_format_trends = plot_release_trends(filtered_df, min_year=start_year)
    st.plotly_chart(fig_format_trends, use_container_width=True)

with col_trend2:
    fig_plat_trends = plot_platform_release_trends(filtered_df, min_year=start_year)
    st.plotly_chart(fig_plat_trends, use_container_width=True)

st.caption(
    "Data Note: Country parsing isolates individual co-production countries from comma-separated records. "
    "Titles with unspecified origin ('Unknown') are omitted from regional aggregations to preserve geographic integrity."
)
