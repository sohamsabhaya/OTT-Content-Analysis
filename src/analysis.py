"""
Analytical Engine for Movie & OTT Platform Content Analysis
Statistical calculations, aggregations, and high-clarity Plotly visualizations.
Focused strictly on rigorous data science operations without decorative vanity charts.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Tuple, List, Optional, Any


# ── Clean, purposeful platform brand colors ──────────────────────────────────
PLATFORM_COLORS = {
    'Netflix': '#E50914',
    'Amazon Prime': '#00A8E1',
    'Disney+': '#113CCF',
    'Hulu': '#10B981'
}

TYPE_COLORS = {
    'Movie': '#3B82F6',     # Slate Blue
    'TV Show': '#1E293B'    # Deep Charcoal Slate
}

AUDIENCE_COLORS = {
    'Kids': '#10B981',      # Green
    'Teens': '#3B82F6',     # Blue
    'Adults': '#EF4444',    # Crimson
    'Unrated': '#9CA3AF'    # Gray
}


def get_current_theme_mode() -> str:
    """Safely retrieves current theme mode ('light' or 'dark') from Streamlit session state."""
    try:
        import streamlit as st
        if hasattr(st, 'session_state') and 'theme_mode' in st.session_state:
            return st.session_state['theme_mode']
    except Exception:
        pass
    return 'light'


def get_type_colors(theme_mode: Optional[str] = None) -> Dict[str, str]:
    """Returns format colors adjusted for active theme (avoids black-on-black in dark mode)."""
    if theme_mode is None:
        theme_mode = get_current_theme_mode()
    if theme_mode == 'dark':
        return {
            'Movie': '#38BDF8',   # Bright Sky Blue
            'TV Show': '#F1F5F9'  # Crisp Off-White / Silver
        }
    return {
        'Movie': '#3B82F6',       # Slate Blue
        'TV Show': '#1E293B'      # Dark Charcoal
    }


def apply_clean_chart_theme(
    fig: go.Figure,
    title: Optional[str] = None,
    height: Optional[int] = None,
    theme_mode: Optional[str] = None
) -> go.Figure:
    """
    Applies an understated, human-designed data publication theme using Nunito typography.
    Dynamically shifts between publication Light and Dark palettes.
    """
    if theme_mode is None:
        theme_mode = get_current_theme_mode()

    is_dark = (theme_mode == 'dark')

    font_color = '#F9FAFB' if is_dark else '#111827'
    subtext_color = '#94A3B8' if is_dark else '#4B5563'
    grid_color = '#262F40' if is_dark else '#F0F2F5'
    zeroline_color = '#334155' if is_dark else '#E5E7EB'
    tick_color = '#94A3B8' if is_dark else '#6B7280'

    layout_update: Dict[str, Any] = dict(
        font=dict(family="Nunito, -apple-system, sans-serif", size=12, color=font_color),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=45 if title else 20, b=35, l=45, r=20),
        legend=dict(
            font=dict(family="Nunito, -apple-system, sans-serif", size=11, color=subtext_color),
            bgcolor='rgba(0,0,0,0)',
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    if height:
        layout_update['height'] = height
    if title:
        layout_update['title'] = dict(
            text=f"<b>{title}</b>",
            font=dict(family="Nunito, -apple-system, sans-serif", size=14, color=font_color),
            x=0.01,
            xanchor='left'
        )
    fig.update_layout(**layout_update)

    axis_style = dict(
        gridcolor=grid_color,
        zerolinecolor=zeroline_color,
        tickfont=dict(family="Nunito, -apple-system, sans-serif", size=11, color=tick_color),
        title_font=dict(family="Nunito, -apple-system, sans-serif", size=12, color=subtext_color)
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    return fig


def load_processed_data(file_path: str = 'data/processed/unified_ott_dataset.csv') -> pd.DataFrame:
    """Loads preprocessed unified OTT dataset."""
    df = pd.read_csv(file_path)
    df['date_added_clean'] = pd.to_datetime(df['date_added_clean'], errors='coerce')
    return df


# ==============================================================================
# Module 1: Catalog Composition & Platform Strategy
# ==============================================================================

def get_overall_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculates summary KPIs across active filter selections."""
    total_titles = len(df)
    total_movies = int((df['type'] == 'Movie').sum())
    total_tv_shows = int((df['type'] == 'TV Show').sum())
    platforms_count = int(df['platform'].nunique())

    movie_pct = (total_movies / total_titles * 100) if total_titles > 0 else 0
    tv_pct = (total_tv_shows / total_titles * 100) if total_titles > 0 else 0

    unique_titles = int(df['title'].str.lower().nunique())
    cross_platform_count = int(df.duplicated(subset=['title', 'type'], keep=False).sum())

    return {
        'total_titles': total_titles,
        'unique_titles': unique_titles,
        'total_movies': total_movies,
        'total_tv_shows': total_tv_shows,
        'movie_pct': round(movie_pct, 1),
        'tv_pct': round(tv_pct, 1),
        'platforms_count': platforms_count,
        'cross_platform_records': cross_platform_count
    }


def get_platform_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Returns content breakdown (Total, Movies, TV Shows, Percentages) per platform."""
    platform_summary = df.groupby(['platform', 'type']).size().unstack(fill_value=0)
    for col in ['Movie', 'TV Show']:
        if col not in platform_summary.columns:
            platform_summary[col] = 0

    platform_summary['Total'] = platform_summary['Movie'] + platform_summary['TV Show']
    platform_summary['Movie %'] = (platform_summary['Movie'] / platform_summary['Total'] * 100).round(1)
    platform_summary['TV Show %'] = (platform_summary['TV Show'] / platform_summary['Total'] * 100).round(1)
    platform_summary = platform_summary.sort_values(by='Total', ascending=False).reset_index()
    return platform_summary


def plot_platform_content_bars(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart comparing Movies vs TV Shows per platform."""
    theme_mode = get_current_theme_mode()
    type_colors = get_type_colors(theme_mode)
    platform_summary = df.groupby(['platform', 'type']).size().reset_index(name='Count')

    fig = px.bar(
        platform_summary,
        x='platform',
        y='Count',
        color='type',
        barmode='group',
        color_discrete_map=type_colors,
        labels={'platform': 'Platform', 'Count': 'Total Titles', 'type': 'Format'},
        text='Count'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        yaxis_title='Number of Titles',
        xaxis_title=''
    )
    return apply_clean_chart_theme(fig, title='Catalog Size & Breakdown by Platform', theme_mode=theme_mode)


# ==============================================================================
# Module 2: Statistical Runtime & Season Analysis
# ==============================================================================

def get_movie_duration_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculates measures of central tendency and dispersion for movie runtimes."""
    movies_dur = df[(df['type'] == 'Movie') & (df['duration_minutes'].notna())]['duration_minutes']

    if len(movies_dur) == 0:
        return {'count': 0, 'mean': 0, 'median': 0, 'min': 0, 'max': 0, 'std': 0, 'iqr': 0}

    q75, q25 = np.percentile(movies_dur, [75, 25])

    return {
        'count': int(len(movies_dur)),
        'mean': round(float(movies_dur.mean()), 1),
        'median': round(float(movies_dur.median()), 1),
        'min': int(movies_dur.min()),
        'max': int(movies_dur.max()),
        'std': round(float(movies_dur.std()), 1),
        'iqr': round(float(q75 - q25), 1)
    }


def plot_movie_duration_boxplot(df: pd.DataFrame) -> go.Figure:
    """Boxplot showing distribution quartiles, median, and outliers across platforms."""
    movies_dur = df[(df['type'] == 'Movie') & (df['duration_minutes'].notna())]

    fig = px.box(
        movies_dur,
        x='platform',
        y='duration_minutes',
        color='platform',
        color_discrete_map=PLATFORM_COLORS,
        labels={'platform': 'Platform', 'duration_minutes': 'Runtime (Minutes)'},
        points='outliers'
    )
    fig.update_layout(showlegend=False)
    return apply_clean_chart_theme(fig, title='Movie Duration Distribution (Quartiles & Outliers)')


def plot_movie_duration_histogram(df: pd.DataFrame) -> go.Figure:
    """Frequency histogram of movie runtimes across catalogs."""
    theme_mode = get_current_theme_mode()
    bar_color = '#60A5FA' if theme_mode == 'dark' else '#3B82F6'
    movies_dur = df[(df['type'] == 'Movie') & (df['duration_minutes'].notna())]

    fig = px.histogram(
        movies_dur,
        x='duration_minutes',
        nbins=50,
        labels={'duration_minutes': 'Duration (Minutes)'},
        color_discrete_sequence=[bar_color]
    )
    fig.update_layout(
        bargap=0.05,
        xaxis_title='Duration (Minutes)',
        yaxis_title='Frequency (Titles)'
    )
    return apply_clean_chart_theme(fig, title='Movie Runtime Frequency Distribution', theme_mode=theme_mode)


def get_tv_season_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculates statistics for TV show season counts."""
    tv_shows = df[(df['type'] == 'TV Show') & (df['duration_seasons'].notna())]['duration_seasons']

    if len(tv_shows) == 0:
        return {'total_shows': 0, 'single_season': 0, 'multi_season': 0, 'single_pct': 0, 'max_seasons': 0, 'mean_seasons': 0}

    single = int((tv_shows == 1).sum())
    multi = int((tv_shows > 1).sum())
    total = int(len(tv_shows))

    return {
        'total_shows': total,
        'single_season': single,
        'multi_season': multi,
        'single_pct': round((single / total * 100), 1) if total > 0 else 0,
        'multi_pct': round((multi / total * 100), 1) if total > 0 else 0,
        'max_seasons': int(tv_shows.max()),
        'mean_seasons': round(float(tv_shows.mean()), 1),
        'median_seasons': round(float(tv_shows.median()), 1)
    }


def plot_tv_season_distribution(df: pd.DataFrame) -> go.Figure:
    """Bar chart of TV Show season lengths."""
    theme_mode = get_current_theme_mode()
    bar_color = '#60A5FA' if theme_mode == 'dark' else '#1E293B'

    tv_shows = df[(df['type'] == 'TV Show') & (df['duration_seasons'].notna())].copy()

    tv_shows['season_group'] = tv_shows['duration_seasons'].apply(
        lambda s: f"{int(s)} Season" if s == 1 else (f"{int(s)} Seasons" if s < 10 else "10+ Seasons")
    )
    season_order = ["1 Season"] + [f"{i} Seasons" for i in range(2, 10)] + ["10+ Seasons"]
    counts = tv_shows['season_group'].value_counts().reindex(season_order).fillna(0).reset_index()
    counts.columns = ['Seasons', 'Count']

    fig = px.bar(
        counts,
        x='Seasons',
        y='Count',
        labels={'Seasons': 'Seasons', 'Count': 'TV Shows'},
        text='Count',
        color_discrete_sequence=[bar_color]
    )
    fig.update_traces(textposition='outside')
    return apply_clean_chart_theme(fig, title='TV Show Season Longevity Distribution', theme_mode=theme_mode)


# ==============================================================================
# Module 3: Genre Analysis
# ==============================================================================

def explode_genres(df: pd.DataFrame) -> pd.DataFrame:
    """Splits comma-separated genres in 'listed_in' into individual rows."""
    exploded = df.assign(genre=df['listed_in'].astype(str).str.split(','))\
                 .explode('genre')
    exploded['genre'] = exploded['genre'].str.strip()
    exploded = exploded[~exploded['genre'].isin(['nan', '', 'Unknown'])]
    return exploded


def get_top_genres(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Calculates top genres across entire dataset."""
    exploded = explode_genres(df)
    genre_counts = exploded.groupby('genre').size().reset_index(name='Count')
    genre_counts = genre_counts.sort_values(by='Count', ascending=False).head(top_n)
    return genre_counts


def plot_top_genres_bar(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal ranked bar chart of top N content genres."""
    theme_mode = get_current_theme_mode()
    bar_color = '#60A5FA' if theme_mode == 'dark' else '#3B82F6'
    top_df = get_top_genres(df, top_n=top_n).sort_values(by='Count', ascending=True)

    fig = px.bar(
        top_df,
        x='Count',
        y='genre',
        orientation='h',
        labels={'Count': 'Titles', 'genre': 'Genre'},
        text='Count',
        color_discrete_sequence=[bar_color]
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        margin=dict(t=45, b=30, l=140, r=40),
        yaxis_title='',
        xaxis_title='Number of Titles'
    )
    return apply_clean_chart_theme(fig, title=f'Top {top_n} Content Genres', theme_mode=theme_mode)


def plot_genre_by_platform_stacked(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Comparative stacked bar chart across top genres by platform."""
    exploded = explode_genres(df)
    top_genres = exploded['genre'].value_counts().head(top_n).index
    filtered = exploded[exploded['genre'].isin(top_genres)]

    summary = filtered.groupby(['genre', 'platform']).size().reset_index(name='Count')

    fig = px.bar(
        summary,
        x='genre',
        y='Count',
        color='platform',
        color_discrete_map=PLATFORM_COLORS,
        labels={'genre': 'Genre', 'Count': 'Titles', 'platform': 'Platform'},
        barmode='stack'
    )
    fig.update_layout(
        xaxis_tickangle=-30,
        xaxis_title='',
        yaxis_title='Number of Titles'
    )
    return apply_clean_chart_theme(fig, title=f'Platform Comparison across Top {top_n} Genres')


# ==============================================================================
# Module 4: Geographic Production Analysis
# ==============================================================================

def explode_countries(df: pd.DataFrame) -> pd.DataFrame:
    """Splits comma-separated countries into individual rows, excluding Unknown."""
    exploded = df.assign(country_clean=df['country'].astype(str).str.split(','))\
                 .explode('country_clean')
    exploded['country_clean'] = exploded['country_clean'].str.strip()
    exploded = exploded[~exploded['country_clean'].isin(['nan', '', 'Unknown', 'Not Specified'])]
    return exploded


def get_top_countries(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Returns top N content-producing countries."""
    exploded = explode_countries(df)
    country_counts = exploded.groupby('country_clean').size().reset_index(name='Count')
    country_counts = country_counts.sort_values(by='Count', ascending=False).head(top_n)
    return country_counts


def plot_top_countries_bar(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart for top N content-producing countries."""
    theme_mode = get_current_theme_mode()
    bar_color = '#34D399' if theme_mode == 'dark' else '#10B981'
    top_df = get_top_countries(df, top_n=top_n).sort_values(by='Count', ascending=True)

    fig = px.bar(
        top_df,
        x='Count',
        y='country_clean',
        orientation='h',
        labels={'Count': 'Total Titles', 'country_clean': 'Country'},
        text='Count',
        color_discrete_sequence=[bar_color]
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        margin=dict(t=45, b=30, l=130, r=40),
        yaxis_title='',
        xaxis_title='Total Titles Produced'
    )
    return apply_clean_chart_theme(fig, title=f'Top {top_n} Content-Producing Countries', theme_mode=theme_mode)


def plot_country_choropleth(df: pd.DataFrame) -> go.Figure:
    """Global choropleth map showing content production volume worldwide."""
    theme_mode = get_current_theme_mode()
    is_dark = (theme_mode == 'dark')

    exploded = explode_countries(df)
    counts = exploded.groupby('country_clean').size().reset_index(name='Titles')

    colorscale = [
        [0, '#151B28'],
        [0.2, '#1E3A8A'],
        [0.6, '#3B82F6'],
        [1, '#93C5FD']
    ] if is_dark else [
        [0, '#EFF6FF'],
        [0.2, '#BFDBFE'],
        [0.6, '#3B82F6'],
        [1, '#1E3A8A']
    ]

    fig = px.choropleth(
        counts,
        locations='country_clean',
        locationmode='country names',
        color='Titles',
        hover_name='country_clean',
        color_continuous_scale=colorscale
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular',
            bgcolor='rgba(0,0,0,0)',
            landcolor='#1E293B' if is_dark else '#F3F4F6',
            subunitcolor='#334155' if is_dark else '#E5E7EB'
        ),
        margin=dict(t=45, b=10, l=10, r=10),
        coloraxis_colorbar=dict(title="Titles")
    )
    return apply_clean_chart_theme(fig, title='Global Content Production Distribution', theme_mode=theme_mode)


def plot_country_platform_comparison(df: pd.DataFrame, top_n: int = 8) -> go.Figure:
    """Stacked bar chart comparing top countries by platform catalog."""
    exploded = explode_countries(df)
    top_countries = exploded['country_clean'].value_counts().head(top_n).index
    filtered = exploded[exploded['country_clean'].isin(top_countries)]

    summary = filtered.groupby(['country_clean', 'platform']).size().reset_index(name='Count')

    fig = px.bar(
        summary,
        x='country_clean',
        y='Count',
        color='platform',
        color_discrete_map=PLATFORM_COLORS,
        labels={'country_clean': 'Country', 'Count': 'Titles'},
        barmode='stack'
    )
    fig.update_layout(
        xaxis_tickangle=-30,
        xaxis_title='',
        yaxis_title='Number of Titles'
    )
    return apply_clean_chart_theme(fig, title=f'Platform Breakdown for Top {top_n} Producing Countries')


# ==============================================================================
# Module 5: Release Trends
# ==============================================================================

def get_yearly_trends(df: pd.DataFrame, min_year: int = 1990) -> pd.DataFrame:
    """Aggregates title counts by release year and format."""
    filtered = df[df['release_year'] >= min_year]
    yearly = filtered.groupby(['release_year', 'type']).size().unstack(fill_value=0).reset_index()
    for col in ['Movie', 'TV Show']:
        if col not in yearly.columns:
            yearly[col] = 0
    yearly['Total'] = yearly['Movie'] + yearly['TV Show']
    return yearly.sort_values(by='release_year')


def plot_release_trends(df: pd.DataFrame, min_year: int = 1990) -> go.Figure:
    """Line chart of content release velocity over years (Movies vs TV Shows)."""
    theme_mode = get_current_theme_mode()
    is_dark = (theme_mode == 'dark')
    type_colors = get_type_colors(theme_mode)

    yearly = get_yearly_trends(df, min_year=min_year)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly['release_year'], y=yearly['Movie'],
        mode='lines+markers', name='Movies',
        line=dict(color=type_colors['Movie'], width=2.5),
        marker=dict(size=5, color=type_colors['Movie'])
    ))
    fig.add_trace(go.Scatter(
        x=yearly['release_year'], y=yearly['TV Show'],
        mode='lines+markers', name='TV Shows',
        line=dict(color=type_colors['TV Show'], width=2.5),
        marker=dict(size=5, color=type_colors['TV Show'])
    ))
    fig.add_trace(go.Scatter(
        x=yearly['release_year'], y=yearly['Total'],
        mode='lines', name='Total',
        line=dict(color='#64748B' if is_dark else '#9CA3AF', width=1.5, dash='dot')
    ))

    fig.update_layout(
        xaxis_title='Release Year',
        yaxis_title='Releases per Year'
    )
    return apply_clean_chart_theme(fig, title=f'Content Release Velocity ({min_year} - Present)', theme_mode=theme_mode)


def plot_platform_release_trends(df: pd.DataFrame, min_year: int = 2000) -> go.Figure:
    """Multi-platform line chart comparing annual releases over time."""
    filtered = df[df['release_year'] >= min_year]
    plat_yearly = filtered.groupby(['release_year', 'platform']).size().reset_index(name='Count')

    fig = px.line(
        plat_yearly,
        x='release_year',
        y='Count',
        color='platform',
        color_discrete_map=PLATFORM_COLORS,
        labels={'release_year': 'Release Year', 'Count': 'Titles Released'}
    )
    fig.update_layout(
        xaxis_title='Release Year',
        yaxis_title='Titles Released'
    )
    return apply_clean_chart_theme(fig, title=f'Annual Release Volume by Platform ({min_year} - Present)')


# ==============================================================================
# Module 6: Ratings & Cross-Platform Overlap
# ==============================================================================

def get_rating_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates content counts by audience category and platform."""
    summary = df.groupby(['rating_category', 'platform']).size().unstack(fill_value=0).reset_index()
    return summary


def plot_rating_category_bars(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart showing audience rating distribution by platform."""
    summary = df.groupby(['platform', 'rating_category']).size().reset_index(name='Count')

    fig = px.bar(
        summary,
        x='platform',
        y='Count',
        color='rating_category',
        barmode='group',
        color_discrete_map=AUDIENCE_COLORS,
        labels={'platform': 'Platform', 'Count': 'Number of Titles', 'rating_category': 'Target Audience'},
        text='Count'
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Number of Titles'
    )
    return apply_clean_chart_theme(fig, title='Audience Classification by Platform')


def plot_platform_overlap_heatmap(df: pd.DataFrame) -> go.Figure:
    """Calculates and visualizes pairwise shared content overlap between platforms."""
    theme_mode = get_current_theme_mode()
    is_dark = (theme_mode == 'dark')

    dups = df.groupby(['title', 'type'])['platform'].apply(lambda x: sorted(list(set(x)))).reset_index()
    shared = dups[dups['platform'].apply(len) > 1]

    platforms = sorted(df['platform'].unique())
    matrix = pd.DataFrame(0, index=platforms, columns=platforms)

    for plats in shared['platform']:
        for p1 in plats:
            for p2 in plats:
                if p1 != p2:
                    matrix.loc[p1, p2] += 1

    colorscale = [
        [0, '#151B28'],
        [0.4, '#1D4ED8'],
        [1, '#60A5FA']
    ] if is_dark else [
        [0, '#F9FAFB'],
        [0.4, '#93C5FD'],
        [1, '#1E40AF']
    ]

    fig = px.imshow(
        matrix,
        text_auto=True,
        color_continuous_scale=colorscale,
        labels=dict(x="Platform", y="Platform", color="Shared Titles")
    )
    fig.update_layout(
        margin=dict(t=45, b=30, l=30, r=30)
    )
    return apply_clean_chart_theme(fig, title='Cross-Platform Catalog Overlap (Shared Titles)', theme_mode=theme_mode)
