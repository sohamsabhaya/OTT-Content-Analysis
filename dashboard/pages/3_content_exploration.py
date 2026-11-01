"""
Page 4: Ratings & Content Exploration
Audience certification patterns, cross-platform overlap lookup, and interactive catalog search.
Clean, human-crafted Data Science analytics system.
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
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
    plot_rating_category_bars,
    plot_platform_overlap_heatmap
)

st.set_page_config(
    page_title="Catalog Overlap & Explorer | OTT Analytics",
    layout="wide"
)

apply_custom_css()

render_page_header(
    title="Catalog Overlap & Content Explorer",
    description="Audience certification patterns, multi-platform licensing overlap, and searchable content database (22,998 titles)."
)

raw_df = get_data()

# Database summary banner
plat_counts = raw_df['platform'].value_counts()
summary_text = "  &bull;  ".join([f"{p}: <b>{c:,}</b>" for p, c in plat_counts.items()])
st.markdown(
    f"""<div class="summary-banner">
        Unified Catalog: <b>{len(raw_df):,} total titles</b> &nbsp;&bull;&nbsp; {summary_text}
    </div>""",
    unsafe_allow_html=True
)

filtered_df, filter_state = render_sidebar_filters(raw_df)

if filtered_df.empty:
    st.warning("No titles match your selected filter criteria. Please adjust your sidebar filters.")
    st.stop()

# ── 1. Audience Certification Breakdown ──────────────────────────────────────
st.subheader("Target Audience Certification by Platform")
fig_ratings = plot_rating_category_bars(filtered_df)
st.plotly_chart(fig_ratings, use_container_width=True)

st.divider()

# ── 2. Cross-Platform Catalog Overlap ────────────────────────────────────────
st.subheader("Cross-Platform Catalog Overlap & Exclusivity")

dups = filtered_df.groupby(['title', 'type'])['platform'].apply(
    lambda x: sorted(list(set(x)))
).reset_index()
dups['platform_count'] = dups['platform'].apply(len)
shared_df = dups[dups['platform_count'] > 1].copy()
shared_df['platforms_str'] = shared_df['platform'].apply(lambda x: ', '.join(x))

c_sh1, c_sh2, c_sh3, c_sh4 = st.columns(4)
c_sh1.metric("Multi-Platform Titles",   f"{len(shared_df):,}")
c_sh2.metric("Available on 2 Services", f"{(shared_df['platform_count'] == 2).sum():,}")
c_sh3.metric("Available on 3+ Services", f"{(shared_df['platform_count'] >= 3).sum():,}")
c_sh4.metric("Catalog Exclusivity Rate", f"{((len(filtered_df) - len(shared_df)) / len(filtered_df) * 100):.1f}%" if len(filtered_df) > 0 else "N/A")

col_heat, col_shared_table = st.columns([1.1, 1.3])

with col_heat:
    fig_overlap = plot_platform_overlap_heatmap(filtered_df)
    st.plotly_chart(fig_overlap, use_container_width=True)

with col_shared_table:
    st.markdown("##### Shared Catalog Matrix")

    filter_choice = st.selectbox(
        "Filter Shared Titles:",
        options=[
            "All Shared Titles (2+ Platforms)",
            "Triple Platform Titles (3+ Services)",
            "Amazon Prime & Netflix",
            "Amazon Prime & Hulu",
            "Hulu & Netflix",
            "Disney+ Shared Titles"
        ],
        index=0,
        key="shared_filter_choice"
    )

    shared_search = st.text_input(
        "Search in shared titles:",
        placeholder="Filter by title name...",
        key="shared_text_search"
    )

    shared_df['Netflix']     = shared_df['platform'].apply(lambda p: 'Netflix' in p)
    shared_df['Prime Video'] = shared_df['platform'].apply(lambda p: 'Amazon Prime' in p)
    shared_df['Disney+']     = shared_df['platform'].apply(lambda p: 'Disney+' in p)
    shared_df['Hulu']        = shared_df['platform'].apply(lambda p: 'Hulu' in p)

    display_shared = shared_df.copy()

    if filter_choice == "Triple Platform Titles (3+ Services)":
        display_shared = display_shared[display_shared['platform_count'] >= 3]
    elif filter_choice == "Amazon Prime & Netflix":
        display_shared = display_shared[display_shared['Prime Video'] & display_shared['Netflix']]
    elif filter_choice == "Amazon Prime & Hulu":
        display_shared = display_shared[display_shared['Prime Video'] & display_shared['Hulu']]
    elif filter_choice == "Hulu & Netflix":
        display_shared = display_shared[display_shared['Hulu'] & display_shared['Netflix']]
    elif filter_choice == "Disney+ Shared Titles":
        display_shared = display_shared[display_shared['Disney+']]

    if shared_search.strip():
        q_s = shared_search.strip().lower()
        display_shared = display_shared[
            display_shared['title'].str.lower().str.contains(q_s, na=False, regex=False)
        ]

    display_cols = ['title', 'type', 'Netflix', 'Prime Video', 'Disney+', 'Hulu', 'platform_count']
    sorted_shared = display_shared[display_cols].sort_values(
        by=['platform_count', 'title'], ascending=[False, True]
    )

    st.caption(f"Showing **{len(sorted_shared):,}** shared titles")
    st.dataframe(
        sorted_shared,
        column_config={
            "title":          st.column_config.TextColumn("Title",       width="medium"),
            "type":           st.column_config.TextColumn("Format",      width="small"),
            "Netflix":        st.column_config.CheckboxColumn("Netflix",     width="small"),
            "Prime Video":    st.column_config.CheckboxColumn("Prime Video", width="small"),
            "Disney+":        st.column_config.CheckboxColumn("Disney+",     width="small"),
            "Hulu":           st.column_config.CheckboxColumn("Hulu",        width="small"),
            "platform_count": st.column_config.NumberColumn("Platforms",     width="small"),
        },
        use_container_width=True,
        hide_index=True,
        height=320
    )

st.divider()

# ── 3. Searchable Catalog Browser ────────────────────────────────────────────
st.subheader("Search Across Streaming Catalogs")

col_search, col_plat_filter = st.columns([2.5, 1])

with col_search:
    direct_search = st.text_input(
        "Search by Title, Director, or Cast Member:",
        placeholder="e.g. Inception, Nolan, DiCaprio...",
        key="main_page_search"
    )

with col_plat_filter:
    plat_subset = st.multiselect(
        "Platform Subset:",
        options=sorted(raw_df['platform'].unique()),
        default=sorted(raw_df['platform'].unique()),
        key="page_plat_subset"
    )

display_df = filtered_df[filtered_df['platform'].isin(plat_subset)].copy()

if direct_search.strip():
    q = direct_search.strip().lower()
    search_mask = (
        display_df['title'].astype(str).str.lower().str.contains(q, na=False, regex=False) |
        display_df['cast'].astype(str).str.lower().str.contains(q, na=False, regex=False) |
        display_df['director'].astype(str).str.lower().str.contains(q, na=False, regex=False) |
        display_df['listed_in'].astype(str).str.lower().str.contains(q, na=False, regex=False)
    )
    display_df = display_df[search_mask]

st.caption(f"Found **{len(display_df):,}** titles matching criteria")

col_export, _ = st.columns([1.2, 3])
csv_data = display_df[[
    'title_id', 'platform', 'type', 'title', 'release_year',
    'rating', 'rating_category', 'duration', 'listed_in', 'country', 'director', 'cast', 'date_added'
]].to_csv(index=False).encode('utf-8')

with col_export:
    st.download_button(
        label="Download Filtered Results as CSV",
        data=csv_data,
        file_name="ott_catalog_filtered.csv",
        mime="text/csv"
    )

display_cols = [
    'platform', 'type', 'title', 'release_year',
    'rating_category', 'duration', 'primary_genre', 'director', 'country'
]

st.dataframe(
    display_df[display_cols],
    use_container_width=True,
    hide_index=True,
    height=380
)

st.divider()

# ── 4. Title Detail Inspector ─────────────────────────────────────────────────
st.subheader("Title Metadata Inspector")

if not display_df.empty:
    unique_titles_available = sorted(display_df['title'].unique().tolist())

    selected_title = st.selectbox(
        "Select title to inspect:",
        options=unique_titles_available,
        index=0
    )

    if selected_title:
        title_records = raw_df[raw_df['title'].astype(str).str.lower() == selected_title.lower()]
        if not title_records.empty:
            year = title_records['release_year'].iloc[0]
            content_type = title_records['type'].iloc[0]
            platforms_available = ", ".join(title_records['platform'].unique().tolist())

            st.markdown(
                f"""<div class="inspector-card">
                    <div class="inspector-title">
                        {selected_title} <span class="inspector-year">({year})</span>
                    </div>
                    <div class="inspector-meta">
                        Format: <b>{content_type}</b> &nbsp;&bull;&nbsp; Available on: <b>{platforms_available}</b>
                    </div>
                </div>""",
                unsafe_allow_html=True
            )

            for _, record in title_records.iterrows():
                with st.container():
                    st.markdown(f"**Platform Record: {record['platform']}**")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.markdown(f"**Runtime:** `{record['duration']}`")
                    m2.markdown(f"**Audience:** `{record['rating_category']}` (`{record['rating']}`)")
                    m3.markdown(f"**Origin:** `{record['country']}`")
                    m4.markdown(f"**Added Date:** `{record['date_added']}`")

                    st.markdown(f"**Genres:** {record['listed_in']}")
                    st.markdown(f"**Director:** {record['director']}")
                    st.markdown(f"**Cast:** {record['cast']}")
                    st.markdown(f"**Synopsis:** {record['description']}")
                    st.caption(f"Composite ID: `{record['title_id']}`")
                    st.write("---")
        else:
            st.info("Title details not found in database.")
else:
    st.info("No titles match your search criteria.")
