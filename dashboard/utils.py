"""
Shared utility and filter module for Streamlit Multi-Page Dashboard.
Clean, human-designed Data Science publication theme using Nunito typography.
"""

import os
from typing import Tuple, Dict, Any
import streamlit as st
import pandas as pd
import numpy as np
from src.analysis import (
    load_processed_data,
    explode_genres,
    explode_countries,
    PLATFORM_COLORS,
    TYPE_COLORS,
    AUDIENCE_COLORS
)


@st.cache_data(show_spinner="Loading OTT catalog data...")
def get_data() -> pd.DataFrame:
    """Loads unified dataset with caching."""
    candidate_paths = [
        'data/processed/unified_ott_dataset.csv',
        '../data/processed/unified_ott_dataset.csv',
        '../../data/processed/unified_ott_dataset.csv'
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            return load_processed_data(p)
    raise FileNotFoundError("Could not find unified_ott_dataset.csv in data/processed/")


def apply_custom_css():
    """
    Injects clean, authentic typography and dynamic Light/Dark mode styling.
    Strictly eliminates white-on-white text issues in light mode and ensures proper rich dark mode.
    """
    if 'theme_mode' not in st.session_state:
        st.session_state['theme_mode'] = 'light'

    is_dark = (st.session_state['theme_mode'] == 'dark')

    if is_dark:
        bg_main = '#0B0F19'
        card_bg = '#151B28'
        border_color = '#262F40'
        text_primary = '#F9FAFB'
        text_secondary = '#94A3B8'
        text_muted = '#64748B'
        metric_label = '#CBD5E1'
        metric_label_hover = '#F8FAFC'
        sidebar_bg = '#0B0F19'
        sidebar_border = '#262F40'
        sidebar_text = '#F9FAFB'
        input_bg = '#151B28'
        input_border = '#262F40'
        input_text = '#F9FAFB'
        popover_bg = '#151B28'
        popover_text = '#F9FAFB'
        popover_hover = '#262F40'
        table_bg = '#151B28'
        table_border = '#262F40'
        hr_color = '#262F40'
        btn_bg = '#1E293B'
        btn_border = '#475569'
        btn_text = '#F8FAFC'
        btn_hover_bg = '#262F40'
        btn_hover_color = '#60A5FA'
        nav_hover = 'rgba(255, 255, 255, 0.08)'
        nav_active_bg = 'rgba(59, 130, 246, 0.20)'
        nav_active_text = '#60A5FA'
        tag_bg = '#1E293B'
        tag_border = '#3B4861'
        tag_text = '#93C5FD'
    else:
        bg_main = '#F8F9FB'
        card_bg = '#FFFFFF'
        border_color = '#E5E7EB'
        text_primary = '#111827'
        text_secondary = '#475569'
        text_muted = '#64748B'
        metric_label = '#374151'
        metric_label_hover = '#111827'
        sidebar_bg = '#1F2430'
        sidebar_border = 'rgba(255, 255, 255, 0.08)'
        sidebar_text = '#E5E7EB'
        input_bg = '#FFFFFF'
        input_border = '#D1D5DB'
        input_text = '#111827'
        popover_bg = '#FFFFFF'
        popover_text = '#111827'
        popover_hover = '#F3F4F6'
        table_bg = '#FFFFFF'
        table_border = '#E5E7EB'
        hr_color = '#E5E7EB'
        btn_bg = '#FFFFFF'
        btn_border = '#CBD5E1'
        btn_text = '#111827'
        btn_hover_bg = '#F1F5F9'
        btn_hover_color = '#1D4ED8'
        nav_hover = 'rgba(255, 255, 255, 0.06)'
        nav_active_bg = 'rgba(59, 130, 246, 0.15)'
        nav_active_text = '#60A5FA'
        tag_bg = '#EFF6FF'
        tag_border = '#BFDBFE'
        tag_text = '#1E40AF'

    css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800&display=swap');

        /* ── Typography & Base Canvas ────────────────────────────────────── */
        html, body, [class*="css"], .stApp, button, input, select, textarea {{
            font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }}

        .stApp {{
            background-color: {bg_main} !important;
            color: {text_primary} !important;
        }}

        /* ── Main Content Container ──────────────────────────────────────── */
        .main .block-container {{
            background-color: {bg_main} !important;
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            max-width: 1360px !important;
        }}

        /* ── Page Header ─────────────────────────────────────────────────── */
        .page-header {{
            margin-bottom: 1.25rem;
            padding-bottom: 0.60rem;
            border-bottom: 1px solid {border_color};
        }}
        .page-title {{
            font-size: 1.65rem;
            font-weight: 800;
            color: {text_primary};
            margin: 0 0 0.25rem 0;
            letter-spacing: -0.01em;
        }}
        .page-description {{
            font-size: 0.90rem;
            color: {text_secondary};
            margin: 0;
            line-height: 1.45;
        }}

        /* ── Metric Cards (Equal sizes, high-contrast crisp labels) ──────── */
        div[data-testid="stMetric"] {{
            background: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
            padding: 14px 16px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
            min-height: 120px !important;
            height: 120px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: flex-start !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
            transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        }}
        div[data-testid="stMetric"]:hover {{
            border-color: {'#3B82F6' if is_dark else '#93C5FD'} !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, {'0.25' if is_dark else '0.06'}) !important;
        }}

        /* Metric Label: High contrast, uppercase, clean letter spacing */
        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] *,
        div[data-testid="stMetricLabel"] label,
        div[data-testid="stMetricLabel"] p,
        div[data-testid="stMetricLabel"] span,
        div[data-testid="stMetricLabel"] div,
        label[data-testid="stMetricLabel"],
        label[data-testid="stMetricLabel"] *,
        label[data-testid="stMetricLabel"] p,
        label[data-testid="stMetricLabel"] span {{
            color: {metric_label} !important;
            font-size: 0.74rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            opacity: 1 !important;
            line-height: 1.3 !important;
        }}

        /* Tooltip help icon inside metric label */
        div[data-testid="stMetricLabel"] svg,
        div[data-testid="stMetricLabel"] svg *,
        label[data-testid="stMetricLabel"] svg,
        label[data-testid="stMetricLabel"] svg *,
        div[data-testid="stMetricLabel"] [data-testid="stTooltipIcon"] svg,
        div[data-testid="stMetricLabel"] .stTooltipIcon svg {{
            color: {metric_label} !important;
            fill: {metric_label} !important;
            stroke: {metric_label} !important;
            opacity: 0.80 !important;
        }}
        div[data-testid="stMetricLabel"] svg:hover,
        label[data-testid="stMetricLabel"] svg:hover {{
            color: {metric_label_hover} !important;
            fill: {metric_label_hover} !important;
            stroke: {metric_label_hover} !important;
            opacity: 1.0 !important;
        }}

        /* Metric Value */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] *,
        div[data-testid="stMetricValue"] > div {{
            font-size: 1.55rem !important;
            font-weight: 800 !important;
            color: {text_primary} !important;
            letter-spacing: -0.01em !important;
            line-height: 1.25 !important;
            margin-top: 2px !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }}

        /* Metric Delta */
        div[data-testid="stMetricDelta"] {{
            margin-top: 4px !important;
        }}
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] *,
        div[data-testid="stMetricDelta"] > div {{
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            white-space: nowrap !important;
        }}

        /* ── Plotly Visualizations Cards ─────────────────────────────────── */
        .element-container:has(div[data-testid="stPlotlyChart"]) {{
            background: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
            padding: 14px 16px 8px 16px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
            margin-bottom: 1rem !important;
        }}

        /* ── Headings ─────────────────────────────────────────────────────── */
        h1, h2, h3, h4 {{
            color: {text_primary} !important;
            font-family: 'Nunito', sans-serif !important;
        }}
        h2 {{
            font-size: 1.20rem !important;
            font-weight: 700 !important;
            margin-top: 1rem !important;
            margin-bottom: 0.5rem !important;
        }}
        h3 {{
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            margin-top: 0.75rem !important;
        }}

        /* ── Main Page Form Inputs (High contrast - NO white on white!) ───── */
        .main label {{
            color: {text_primary} !important;
            font-weight: 600 !important;
        }}
        .main .stTextInput input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border: 1px solid {input_border} !important;
            border-radius: 6px !important;
        }}
        .main .stSelectbox [data-baseweb="select"] > div,
        .main .stMultiSelect [data-baseweb="select"] > div {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border: 1px solid {input_border} !important;
            border-radius: 6px !important;
        }}
        .main .stSelectbox span,
        .main .stMultiSelect span {{
            color: {input_text} !important;
        }}
        .main [data-testid="stMultiSelect"] [data-baseweb="tag"] {{
            background: {tag_bg} !important;
            border: 1px solid {tag_border} !important;
            border-radius: 4px !important;
        }}
        .main [data-testid="stMultiSelect"] [data-baseweb="tag"] span {{
            color: {tag_text} !important;
            font-weight: 600 !important;
        }}

        /* ── Dropdown Popovers / Menus (Global) ───────────────────────────── */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        ul[role="listbox"] {{
            background-color: {popover_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 6px !important;
        }}
        [data-baseweb="popover"] li,
        [data-baseweb="menu"] li,
        ul[role="listbox"] li {{
            background-color: {popover_bg} !important;
            color: {popover_text} !important;
        }}
        [data-baseweb="popover"] li span,
        [data-baseweb="menu"] li span,
        ul[role="listbox"] li span {{
            color: {popover_text} !important;
            font-weight: 500 !important;
        }}
        [data-baseweb="popover"] li:hover,
        [data-baseweb="menu"] li:hover,
        ul[role="listbox"] li[aria-selected="true"] {{
            background-color: {popover_hover} !important;
            color: {popover_text} !important;
        }}

        /* ── Sidebar ─────────────────────────────────────────────────────── */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg} !important;
            border-right: 1px solid {sidebar_border} !important;
        }}
        section[data-testid="stSidebar"] label {{
            color: {sidebar_text} !important;
            font-size: 0.80rem !important;
            font-weight: 600 !important;
        }}
        section[data-testid="stSidebar"] > div:first-child {{
            padding-top: 1rem !important;
        }}

        /* Sidebar Brand */
        .sidebar-brand-block {{
            padding: 4px 6px 14px 6px;
            margin-bottom: 12px;
            border-bottom: 1px solid {sidebar_border};
        }}
        .sidebar-brand-title {{
            font-size: 1.05rem;
            font-weight: 800;
            color: #FFFFFF !important;
            margin: 0;
            letter-spacing: -0.01em;
        }}
        .sidebar-brand-subtitle {{
            font-size: 0.75rem;
            color: #CBD5E1 !important;
            margin: 2px 0 0 0;
        }}

        /* Sidebar Section Labels */
        .sidebar-heading {{
            font-size: 0.70rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #CBD5E1 !important;
            margin: 14px 0 6px 2px;
        }}

        /* ── Native Multipage Navigation (Sidebar Navbar) ────────────────── */
        [data-testid="stSidebarNav"] {{
            padding: 0.25rem 0 !important;
            margin-bottom: 0.75rem !important;
            border-bottom: 1px solid {sidebar_border} !important;
        }}
        [data-testid="stSidebarNav"] a,
        [data-testid="stSidebarNav"] a *,
        [data-testid="stSidebarNav"] a span,
        [data-testid="stSidebarNav"] a p,
        [data-testid="stSidebarNav"] a div,
        a[data-testid="stSidebarNavLink"],
        a[data-testid="stSidebarNavLink"] *,
        a[data-testid="stSidebarNavLink"] span {{
            color: #E2E8F0 !important;
            font-family: 'Nunito', sans-serif !important;
            font-size: 0.90rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.01em !important;
            text-transform: capitalize !important;
            opacity: 1 !important;
        }}
        [data-testid="stSidebarNav"] a,
        a[data-testid="stSidebarNavLink"] {{
            border-radius: 6px !important;
            padding: 7px 12px !important;
            margin-bottom: 3px !important;
            transition: all 0.15s ease !important;
        }}
        [data-testid="stSidebarNav"] a:hover,
        a[data-testid="stSidebarNavLink"]:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
        }}
        [data-testid="stSidebarNav"] a:hover *,
        [data-testid="stSidebarNav"] a:hover span,
        [data-testid="stSidebarNav"] a:hover p,
        a[data-testid="stSidebarNavLink"]:hover *,
        a[data-testid="stSidebarNavLink"]:hover span {{
            color: #FFFFFF !important;
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"],
        a[data-testid="stSidebarNavLink"][aria-current="page"] {{
            background: rgba(59, 130, 246, 0.22) !important;
            border-left: 3.5px solid #3B82F6 !important;
        }}
        [data-testid="stSidebarNav"] a[aria-current="page"] *,
        [data-testid="stSidebarNav"] a[aria-current="page"] span,
        [data-testid="stSidebarNav"] a[aria-current="page"] p,
        a[data-testid="stSidebarNavLink"][aria-current="page"] *,
        a[data-testid="stSidebarNavLink"][aria-current="page"] span {{
            color: #60A5FA !important;
            font-weight: 700 !important;
        }}

        /* Sidebar Widgets */
        section[data-testid="stSidebar"] .stMultiSelect > div,
        section[data-testid="stSidebar"] .stSelectbox > div > div,
        section[data-testid="stSidebar"] .stTextInput > div > div {{
            background-color: {'#151B28' if is_dark else '#161A22'} !important;
            border: 1px solid {'#262F40' if is_dark else '#374151'} !important;
            border-radius: 6px !important;
            color: #FFFFFF !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] {{
            background: {'#262F40' if is_dark else '#2D333F'} !important;
            border: 1px solid {'#3B4861' if is_dark else '#4B5563'} !important;
            border-radius: 4px !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] span {{
            color: #F3F4F6 !important;
            font-weight: 600 !important;
        }}
        section[data-testid="stSidebar"] .stSlider [data-testid="stSliderThumb"] {{
            background: #3B82F6 !important;
            border-color: #3B82F6 !important;
        }}
        section[data-testid="stSidebar"] .stCaption {{
            color: #CBD5E1 !important;
            font-size: 0.76rem !important;
        }}

        /* ── Captions (High contrast, clearly visible) ──────────────────── */
        .main .stCaption,
        div[data-testid="stCaptionContainer"],
        div[data-testid="stCaptionContainer"] p {{
            color: {text_secondary} !important;
            font-size: 0.84rem !important;
            line-height: 1.45 !important;
            opacity: 1 !important;
        }}

        /* ── Tables & DataFrames ─────────────────────────────────────────── */
        div[data-testid="stDataFrame"] {{
            background: {table_bg} !important;
            border: 1px solid {table_border} !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }}

        /* ── All General Buttons (Strict high-contrast text) ─────────────── */
        div[data-testid="stButton"] > button,
        div[data-testid="stButton"] > button:focus,
        div[data-testid="stButton"] > button:active,
        button[data-testid="baseButton-secondary"],
        button[kind="secondary"] {{
            background-color: {btn_bg} !important;
            background: {btn_bg} !important;
            border: 1.5px solid {btn_border} !important;
            border-radius: 8px !important;
            padding: 7px 16px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.15s ease !important;
        }}
        div[data-testid="stButton"] > button *,
        div[data-testid="stButton"] > button p,
        div[data-testid="stButton"] > button span,
        div[data-testid="stButton"] > button div,
        button[data-testid="baseButton-secondary"] *,
        button[data-testid="baseButton-secondary"] p,
        button[kind="secondary"] *,
        button[kind="secondary"] p {{
            color: {btn_text} !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            font-family: 'Nunito', sans-serif !important;
            opacity: 1 !important;
        }}
        div[data-testid="stButton"] > button:hover,
        button[data-testid="baseButton-secondary"]:hover,
        button[kind="secondary"]:hover {{
            background-color: {btn_hover_bg} !important;
            background: {btn_hover_bg} !important;
            border-color: #3B82F6 !important;
        }}
        div[data-testid="stButton"] > button:hover *,
        div[data-testid="stButton"] > button:hover p,
        div[data-testid="stButton"] > button:hover span,
        div[data-testid="stButton"] > button:hover div,
        button[data-testid="baseButton-secondary"]:hover *,
        button[data-testid="baseButton-secondary"]:hover p,
        button[kind="secondary"]:hover *,
        button[kind="secondary"]:hover p {{
            color: {btn_hover_color} !important;
        }}

        div[data-testid="stDownloadButton"] > button,
        button[data-testid="baseButton-primary"] {{
            background-color: #10B981 !important;
            background: #10B981 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 7px 18px !important;
        }}
        div[data-testid="stDownloadButton"] > button *,
        div[data-testid="stDownloadButton"] > button p,
        button[data-testid="baseButton-primary"] *,
        button[data-testid="baseButton-primary"] p {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            opacity: 1 !important;
        }}
        div[data-testid="stDownloadButton"] > button:hover,
        button[data-testid="baseButton-primary"]:hover {{
            background-color: #059669 !important;
            background: #059669 !important;
        }}

        /* ── Dedicated Theme Toggle Button Wrapper ───────────────────────── */
        .theme-toggle-wrapper div[data-testid="stButton"] > button,
        .theme-toggle-wrapper button {{
            background-color: {btn_bg} !important;
            background: {btn_bg} !important;
            border: 1.5px solid {btn_border} !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }}
        .theme-toggle-wrapper div[data-testid="stButton"] > button *,
        .theme-toggle-wrapper div[data-testid="stButton"] > button p,
        .theme-toggle-wrapper div[data-testid="stButton"] > button span,
        .theme-toggle-wrapper button *,
        .theme-toggle-wrapper button p,
        .theme-toggle-wrapper button span {{
            color: {btn_text} !important;
            font-size: 0.90rem !important;
            font-weight: 700 !important;
            font-family: 'Nunito', sans-serif !important;
            letter-spacing: 0.01em !important;
            opacity: 1 !important;
        }}
        .theme-toggle-wrapper div[data-testid="stButton"] > button:hover,
        .theme-toggle-wrapper button:hover {{
            background-color: {btn_hover_bg} !important;
            background: {btn_hover_bg} !important;
            border-color: #3B82F6 !important;
        }}
        .theme-toggle-wrapper div[data-testid="stButton"] > button:hover *,
        .theme-toggle-wrapper div[data-testid="stButton"] > button:hover p,
        .theme-toggle-wrapper div[data-testid="stButton"] > button:hover span,
        .theme-toggle-wrapper button:hover *,
        .theme-toggle-wrapper button:hover p,
        .theme-toggle-wrapper button:hover span {{
            color: {btn_hover_color} !important;
        }}

        /* ── Custom Cards ────────────────────────────────────────────────── */
        .summary-banner {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 6px;
            padding: 10px 16px;
            margin-bottom: 16px;
            font-size: 0.88rem;
            color: {text_primary};
        }}
        .inspector-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 14px;
        }}
        .inspector-title {{
            font-size: 1.25rem;
            font-weight: 800;
            color: {text_primary};
        }}
        .inspector-year {{
            font-size: 0.95rem;
            font-weight: 500;
            color: {text_muted};
        }}
        .inspector-meta {{
            font-size: 0.85rem;
            color: {text_secondary};
            margin-top: 4px;
        }}

        /* ── Dividers ────────────────────────────────────────────────────── */
        hr {{
            border: none !important;
            border-top: 1px solid {hr_color} !important;
            margin: 1.25rem 0 !important;
        }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_page_header(title: str, description: str):
    """
    Renders page title and description with an elegant theme toggle button on the right.
    """
    if 'theme_mode' not in st.session_state:
        st.session_state['theme_mode'] = 'light'

    is_dark = (st.session_state['theme_mode'] == 'dark')

    col_title, col_toggle = st.columns([5.5, 1.3])
    with col_title:
        st.markdown(
            f"""
            <div class="page-header">
                <h1 class="page-title">{title}</h1>
                <p class="page-description">{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_toggle:
        st.markdown('<div class="theme-toggle-wrapper">', unsafe_allow_html=True)
        st.markdown('<div style="height: 6px;"></div>', unsafe_allow_html=True)
        btn_label = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
        safe_key = "theme_btn_" + "".join(c if c.isalnum() else "_" for c in title.lower())
        if st.button(btn_label, key=safe_key, help="Toggle between Light and Dark mode", use_container_width=True):
            st.session_state['theme_mode'] = 'light' if is_dark else 'dark'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# Backward-compatible alias
render_page_hero = render_page_header


def render_sidebar_nav():
    """Renders branded sidebar header and navigation section."""
    st.sidebar.markdown(
        """
        <div class="sidebar-brand-block">
            <h2 class="sidebar-brand-title">OTT Content Analytics</h2>
            <p class="sidebar-brand-subtitle">Cross-Platform Intelligence System</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown('<div class="sidebar-heading">Filters</div>', unsafe_allow_html=True)


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Renders global interactive sidebar filters and returns the filtered DataFrame.
    """
    render_sidebar_nav()

    # Platform Filter
    all_platforms = sorted(df['platform'].unique().tolist())
    selected_platforms = st.sidebar.multiselect(
        "Platforms",
        options=all_platforms,
        default=all_platforms,
        help="Select one or more streaming services to analyze."
    )
    if not selected_platforms:
        selected_platforms = all_platforms

    # Content Type (Format)
    all_types = sorted(df['type'].unique().tolist())
    selected_types = st.sidebar.multiselect(
        "Content Format",
        options=all_types,
        default=all_types,
        help="Filter by Movie or TV Show."
    )
    if not selected_types:
        selected_types = all_types

    # Release Year Slider
    min_year = int(df['release_year'].min())
    max_year = int(df['release_year'].max())
    selected_years = st.sidebar.slider(
        "Release Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    # Audience Rating
    all_ratings = ['Kids', 'Teens', 'Adults', 'Unrated']
    selected_ratings = st.sidebar.multiselect(
        "Target Audience Certification",
        options=all_ratings,
        default=all_ratings
    )
    if not selected_ratings:
        selected_ratings = all_ratings

    # Apply base filters
    mask = (
        df['platform'].isin(selected_platforms) &
        df['type'].isin(selected_types) &
        df['release_year'].between(selected_years[0], selected_years[1]) &
        df['rating_category'].isin(selected_ratings)
    )
    filtered_df = df[mask].copy()

    filter_state = {
        'platforms': selected_platforms,
        'types': selected_types,
        'years': selected_years,
        'ratings': selected_ratings,
        'genre': 'All Genres',
        'country': 'All Countries',
        'search': ''
    }

    return filtered_df, filter_state
