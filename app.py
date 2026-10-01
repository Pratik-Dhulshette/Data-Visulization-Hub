#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import base64
from html import escape
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Netflix.csv"
RED = "#e50914"
PALETTE = ["#e50914", "#f05d5e", "#ff9c74", "#f5c36a", "#72c7b5", "#8ea5ff", "#c18aff", "#d4d4d8"]
PLOT_LAYOUT = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "DM Sans, sans-serif", "color": "#e6e3e0", "size": 12},
    "margin": {"l": 12, "r": 12, "t": 20, "b": 12},
    "hoverlabel": {"bgcolor": "#191919", "bordercolor": "#393536", "font": {"color": "#f7f4f2"}},
}

st.set_page_config(
    page_title="Data Visualization Hub",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def find_image(keywords: tuple[str, ...], excluded: tuple[str, ...] = ()) -> Path | None:
    supported = {".png", ".jpg", ".jpeg", ".webp"}
    candidates = [path for path in BASE_DIR.rglob("*") if path.suffix.lower() in supported]
    candidates = [path for path in candidates if not any(word in path.name.lower() for word in excluded)]
    ranked = sorted(
        candidates,
        key=lambda path: (
            -sum(word in path.stem.lower() for word in keywords),
            len(path.parts),
            path.name.lower(),
        ),
    )
    return ranked[0] if ranked and any(word in ranked[0].stem.lower() for word in keywords) else None


def image_data_uri(path: Path | None) -> str:
    if path is None:
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/webp" if path.suffix.lower() == ".webp" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    data.columns = data.columns.str.strip()
    for column in (
        "Title", "Type", "Category", "Region", "Rating", "Watch_Date",
        "Monthly_Revenue", "Watch_Count", "Watch_Time_Minutes",
    ):
        if column not in data.columns:
            data[column] = pd.NA
    data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
    data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")
    data["Monthly_Revenue"] = pd.to_numeric(data["Monthly_Revenue"], errors="coerce").fillna(0)
    data["Watch_Count"] = pd.to_numeric(data["Watch_Count"], errors="coerce").fillna(0)
    data["Watch_Time_Minutes"] = pd.to_numeric(data["Watch_Time_Minutes"], errors="coerce").fillna(0)
    data["_WatchYear"] = data["Watch_Date"].dt.year
    data["_WatchMonth"] = data["Watch_Date"].dt.to_period("M").astype("string")
    return data


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    return normalize_data(pd.read_csv(path))


@st.cache_data(show_spinner=False)
def load_uploaded_data(contents: bytes) -> pd.DataFrame:
    return normalize_data(pd.read_csv(BytesIO(contents)))


def options_for(data: pd.DataFrame, column: str) -> list:
    return sorted(data[column].dropna().unique().tolist(), key=str) if column in data else []


def apply_filters(data: pd.DataFrame, selections: dict[str, list]) -> pd.DataFrame:
    filtered = data.copy()
    for column, values in selections.items():
        if values:
            filtered = filtered[filtered[column].isin(values)]
    return filtered


def style_figure(figure: go.Figure, height: int = 320) -> go.Figure:
    figure.update_layout(**PLOT_LAYOUT, height=height, colorway=PALETTE, transition_duration=350)
    figure.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(255,255,255,.08)")
    figure.update_yaxes(gridcolor="rgba(255,255,255,.07)", zeroline=False, linecolor="rgba(255,255,255,.08)")
    return figure


def metric_card(label: str, value: str, note: str, index: int) -> None:
    st.markdown(
        f'<div class="metric-card metric-{index}"><span class="metric-label">{label}</span>'
        f'<strong class="metric-value">{value}</strong><span class="metric-note">{note}</span></div>',
        unsafe_allow_html=True,
    )


def section_heading(kicker: str, title: str, description: str, anchor: str) -> None:
    st.markdown(
        f'<div class="section-heading" id="{anchor}"><span class="eyebrow">{kicker}</span>'
        f'<h2>{title}</h2><p>{description}</p></div>',
        unsafe_allow_html=True,
    )


if not DATA_PATH.exists():
    st.error(f"Could not find Netflix.csv beside this application: {DATA_PATH}")
    st.stop()

data = load_data(str(DATA_PATH))
logo_path = find_image(("logo", "brand"), excluded=("background", "wallpaper", "hero"))
background_path = find_image(("background", "wallpaper", "hero", "cover"), excluded=("logo", "brand"))
logo_uri = image_data_uri(logo_path)
background_uri = image_data_uri(background_path)
valid_dates = data["Watch_Date"].dropna()
hero_date_label = f"{valid_dates.min():%b %Y} – {valid_dates.max():%b %Y}" if not valid_dates.empty else "Date range unavailable"

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --red:#e50914; --ink:#090909; --panel:#141313; --line:rgba(255,255,255,.09); --muted:#a29c9a; --paper:#f3efed; }
    html { scroll-behavior:smooth; scroll-padding-top:82px; }
    [data-testid="stAppViewContainer"] { background:radial-gradient(ellipse at 78% 13%,rgba(89,18,20,.17),transparent 31%),#090909; color:var(--paper); font-family:'DM Sans',sans-serif; }
    [data-testid="stHeader"] { display:none!important; }
    [data-testid="stToolbar"],[data-testid="stDecoration"] { display:none!important; }
    [data-testid="stAppViewContainer"] { overflow-x:clip; }
    [data-testid="stMainBlockContainer"] { padding:0 0 4rem; max-width:100%; }
    [data-testid="stMainBlockContainer"] > div { max-width:1240px; width:90vw; margin-inline:auto; }
    .block-container { padding-top:0!important; }
    [data-testid="stSidebar"] { background:#121010; }
    .nav-shell { position:sticky; top:0; z-index:100; display:flex; align-items:center; justify-content:space-between; box-sizing:border-box; width:100vw; margin-left:calc(50% - 50vw); padding:14px max(5vw,24px); background:rgba(9,9,9,.84); border-bottom:1px solid rgba(255,255,255,.07); backdrop-filter:blur(18px); }
    .nav-shell .brand { display:flex; align-items:center; gap:12px; min-width:0; color:#fff!important; text-decoration:none!important; font:800 13px 'Manrope',sans-serif; letter-spacing:.04em; }
    .nav-shell .brand img { flex:none; width:52px; height:52px; box-sizing:border-box; padding:3px; object-fit:contain; object-position:center; background:#f8f7f2; border:1px solid rgba(255,255,255,.3); border-radius:50%; }
    .brand-mark { color:var(--red); font:800 31px 'Manrope',sans-serif; }
    .nav-links { display:flex; gap:30px; align-items:center; }
    .nav-links a { color:#bbb5b2; text-decoration:none; font-size:12px; font-weight:600; transition:color .2s ease; }
    .nav-links a:hover,.nav-links a.active { color:#fff; }
    .nav-links a.active:after { content:''; display:block; height:2px; margin-top:7px; background:var(--red); border-radius:2px; }
    .mobile-menu { display:none; position:relative; color:#fff; font-size:11px; }
    .mobile-menu summary { cursor:pointer; list-style:none; padding:9px 12px; border:1px solid var(--line); border-radius:4px; }
    .mobile-menu summary::-webkit-details-marker { display:none; }
    .mobile-links { position:absolute; top:42px; right:0; display:grid; min-width:155px; padding:8px; background:#171414; border:1px solid #393332; border-radius:5px; box-shadow:0 12px 28px rgba(0,0,0,.4); }
    .mobile-links a { padding:10px; color:#eee; text-decoration:none; }
    .nav-status { color:#b5aaa7; font-size:11px; letter-spacing:.04em; }
    .nav-status i { display:inline-block; width:7px; height:7px; margin-right:7px; border-radius:50%; background:#76c9a6; box-shadow:0 0 12px #76c9a6; }
    .upload-intro { margin:30px 0 8px; }
    .upload-intro strong { display:block; margin-bottom:5px; color:#f6f2f0; font:700 16px 'Manrope',sans-serif; }
    .upload-intro span { color:#aaa3a0; font-size:12px; line-height:1.6; }
    [data-testid="stFileUploader"] { padding:14px 16px; background:rgba(20,18,18,.85); border:1px dashed rgba(255,255,255,.22); border-radius:7px; }
    [data-testid="stFileUploader"] section { background:transparent!important; }
    [data-testid="stFileUploader"] button { color:#f4efed!important; background:#1b1818!important; border:1px solid #3b3534!important; }
    .upload-status { margin:8px 0 20px; color:#8f8986; font-size:11px; }
    .hero-shell { position:relative; display:flex; align-items:flex-end; box-sizing:border-box; width:100vw; min-height:min(78vh,760px); margin-left:calc(50% - 50vw); padding:0 max(8vw,34px) 76px; overflow:hidden; background-color:#21090a; background-image:linear-gradient(90deg,rgba(7,6,6,.92) 0%,rgba(7,6,6,.66) 43%,rgba(7,6,6,.1) 100%),linear-gradient(0deg,#090909 0%,rgba(9,9,9,.02) 45%,rgba(9,9,9,.14) 100%),var(--hero-image); background-position:center,center,center 45%; background-size:cover; animation:hero-in .9s ease both; }
    .hero-shell:after { content:''; position:absolute; inset:auto 0 0; height:1px; background:linear-gradient(90deg,transparent,rgba(229,9,20,.8),transparent); }
    .hero-content { position:relative; z-index:1; max-width:690px; animation:rise-in .8s .12s ease both; }
    .hero-kicker,.eyebrow { color:#fa5c62; font:700 10px 'Manrope',sans-serif; letter-spacing:.16em; text-transform:uppercase; }
    .hero-shell .hero-title { margin:18px 0 15px; color:#fff!important; font:800 clamp(48px,7vw,88px)/.98 'Manrope',sans-serif; letter-spacing:-.035em; }
    .hero-shell .hero-title span { color:var(--red)!important; }
    .hero-copy { max-width:520px; margin:0; color:#c6c0bd; font-size:15px; line-height:1.75; }
    .hero-meta { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:24px 0 30px; color:#d7d0cd; font-size:11px; }
    .hero-meta b { color:#fff; font-size:12px; }
    .hero-shell .hero-cta { display:inline-flex; align-items:center; gap:12px; padding:14px 21px; color:white!important; text-decoration:none!important; background:var(--red); border-radius:3px; font-size:12px; font-weight:700; box-shadow:0 8px 24px rgba(229,9,20,.24); transition:transform .2s ease,background .2s ease,box-shadow .2s ease; }
    .hero-cta:hover { transform:translateY(-2px); background:#ff1723; box-shadow:0 12px 28px rgba(229,9,20,.35); }
    .section-heading { padding:60px 0 24px; scroll-margin-top:76px; }
    .section-heading h2 { margin:8px 0 7px; color:#f6f2f0; font:700 26px 'Manrope',sans-serif; letter-spacing:-.025em; }
    .section-heading p { margin:0; max-width:680px; color:#aaa3a0; font-size:12px; line-height:1.7; }
    .metric-grid { display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:12px; }
    .metric-card { position:relative; display:flex; flex-direction:column; min-height:130px; box-sizing:border-box; padding:20px 17px 17px; overflow:hidden; background:linear-gradient(145deg,rgba(31,28,28,.96),rgba(17,16,16,.95)); border:1px solid var(--line); border-radius:7px; box-shadow:0 12px 30px rgba(0,0,0,.18); transition:transform .25s ease,border-color .25s ease,background .25s ease; animation:rise-in .55s ease both; }
    .metric-card:after { content:''; position:absolute; top:0; left:0; width:34px; height:2px; background:var(--red); transition:width .25s ease; }
    .metric-card:hover { transform:translateY(-4px); border-color:rgba(229,9,20,.38); background:#1a1717; }
    .metric-card:hover:after { width:100%; }
    .metric-label { color:#aaa3a0; font-size:10px; font-weight:600; letter-spacing:.06em; text-transform:uppercase; }
    .metric-value { margin:17px 0 7px; color:#faf8f7; font:700 29px 'Manrope',sans-serif; }
    .metric-note { color:#827b78; font-size:10px; }
    .filter-wrap { padding:18px; background:rgba(20,18,18,.85); border:1px solid var(--line); border-radius:7px; }
    .filter-label { margin:0 0 13px; color:#eae4e1; font:700 11px 'Manrope',sans-serif; }
    [data-testid="stSelectbox"] label,[data-testid="stMultiSelect"] label,[data-testid="stTextInput"] label,[data-testid="stNumberInput"] label { color:#aaa3a0!important; font-size:10px!important; }
    [data-testid="stMultiSelect"] [data-baseweb="select"]>div,[data-testid="stTextInput"] input { background:#181616!important; border-color:#383332!important; color:#f5f1ef!important; border-radius:4px!important; }
    [data-testid="stMultiSelect"] [data-baseweb="tag"] { background:#472023!important; }
    [data-testid="stMultiSelect"] [data-baseweb="tag"] span { color:#fff!important; }
    [data-testid="stPlotlyChart"] { padding:10px 8px 2px; background:linear-gradient(150deg,rgba(27,24,24,.88),rgba(17,16,16,.78)); border:1px solid var(--line); border-radius:7px; transition:border-color .2s ease; }
    [data-testid="stPlotlyChart"]:hover { border-color:rgba(255,255,255,.17); }
    .chart-title { margin:18px 0 2px; color:#f0ebea; font:600 13px 'Manrope',sans-serif; }
    .chart-subtitle { margin:0 0 8px; color:#89817e; font-size:10px; }
    .insight-grid { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; }
    .insight-card { min-height:105px; padding:16px; background:#151313; border:1px solid var(--line); border-radius:6px; }
    .insight-card span { display:block; margin-bottom:13px; color:#948c89; font-size:10px; }
    .insight-card strong { color:#f4efed; font:600 14px 'Manrope',sans-serif; }
    .insight-card em { display:block; margin-top:5px; color:#8d8582; font-size:10px; font-style:normal; }
    .data-note { margin:22px 0 0; padding:14px 16px; color:#b5adaa; background:rgba(229,9,20,.07); border-left:2px solid var(--red); font-size:11px; line-height:1.6; }
    .table-note { margin:0 0 12px; color:#928a87; font-size:10px; }
    [data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:6px; overflow:hidden; }
    [data-testid="stButton"] button { color:#f4efed; background:#1b1818; border:1px solid #3b3534; border-radius:4px; transition:all .2s ease; }
    [data-testid="stButton"] button:hover { color:white; border-color:var(--red); background:#2b1618; }
    .pagination-label { padding-top:7px; color:#aaa3a0; font-size:11px; text-align:center; }
    .footer { display:flex; justify-content:space-between; gap:20px; margin:72px auto 0; padding:24px 0 0; border-top:1px solid var(--line); color:#88807d; font-size:10px; }
    .footer strong { color:#e4ddda; font-weight:600; }
    .footer a { margin-left:15px; color:#b9b1ae; text-decoration:none; }
    @keyframes rise-in { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
    @keyframes hero-in { from { filter:brightness(.55); } to { filter:brightness(1); } }
    @media (max-width:1000px) { .metric-grid { grid-template-columns:repeat(3,minmax(0,1fr)); } .insight-grid { grid-template-columns:repeat(3,minmax(0,1fr)); } .hero-shell { min-height:66vh; } }
    @media (max-width:640px) { .nav-shell { padding:10px 14px; gap:10px; } .nav-shell .brand { gap:8px; font-size:11px; line-height:1.25; } .nav-shell .brand img { width:44px; height:44px; } .nav-status,.nav-links { display:none; } .mobile-menu { display:block; flex:none; } .hero-shell { min-height:68vh; padding:0 22px 48px; background-position:center,center,58% center; } .hero-shell .hero-title { font-size:clamp(40px,12vw,52px); line-height:1.02; } .hero-copy { font-size:13px; } .hero-meta { gap:7px; line-height:1.7; } .section-heading { padding-top:42px; } .section-heading h2 { font-size:23px; } .metric-grid { grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; } .metric-card { min-height:116px; padding:15px 13px; } .metric-value { font-size:25px; } .insight-grid { grid-template-columns:repeat(2,minmax(0,1fr)); } .filter-wrap { padding:13px; } .upload-intro { margin-top:24px; } .footer { display:block; line-height:2.2; } .footer div+div { margin-top:10px; } [data-testid="stHorizontalBlock"] { flex-wrap:wrap!important; gap:10px!important; } [data-testid="stHorizontalBlock"] > [data-testid="column"] { min-width:0!important; flex:1 1 calc(50% - 10px)!important; } [data-testid="stDataFrame"] { max-width:100%; } }
    @media (prefers-reduced-motion:reduce) { *,*:before,*:after { scroll-behavior:auto!important; animation-duration:.01ms!important; transition-duration:.01ms!important; } }
    </style>
    """,
    unsafe_allow_html=True,
)

brand_image = f'<img src="{logo_uri}" alt="Data Visualization Hub logo">' if logo_uri else '<b class="brand-mark">D</b>'
hero_style = f"--hero-image:url('{background_uri}')" if background_uri else "--hero-image:linear-gradient(120deg,#381014,#100d0d 70%)"
st.markdown(
    f'<nav class="nav-shell"><a class="brand" href="#top">{brand_image}<span>Data Visualization Hub</span></a>'
    '<div class="nav-links"><a href="#dashboard">Dashboard</a><a href="#analytics">Analytics</a>'
    '<a href="#insights">Insights</a><a href="#data-explorer">Data Explorer</a></div>'
    '<details class="mobile-menu"><summary aria-label="Open navigation menu">Menu</summary><div class="mobile-links">'
    '<a href="#dashboard">Dashboard</a><a href="#analytics">Analytics</a><a href="#insights">Insights</a>'
    '<a href="#data-explorer">Data Explorer</a></div></details>'
    '<div class="nav-status"><i></i>DATA READY</div></nav>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="upload-intro"><strong>Bring your data</strong>'
    '<span>Upload a CSV file to explore it with the dashboard. Leave this empty to use the included sample.</span></div>',
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="CSV files work best when they include columns such as Title, Type, Region, Category, Rating, and Watch_Date.",
    key="dataset_upload",
)
dataset_label = DATA_PATH.name
if uploaded_file is not None:
    try:
        data = load_uploaded_data(uploaded_file.getvalue())
        dataset_label = uploaded_file.name
    except Exception as error:
        st.error(f"Could not read {uploaded_file.name}: {error}. The included sample dataset is still selected.")
st.markdown(f'<div class="upload-status">Active dataset: {escape(dataset_label)}</div>', unsafe_allow_html=True)

valid_dates = data["Watch_Date"].dropna()
hero_date_label = f"{valid_dates.min():%b %Y} – {valid_dates.max():%b %Y}" if not valid_dates.empty else "Date range unavailable"
st.markdown(
    f'<div id="top" class="hero-shell" style="{hero_style}"><div class="hero-content">'
    '<div class="hero-kicker">A clearer view of your data</div>'
    '<h1 class="hero-title" style="color:#fff!important">Data Visualization<br><span style="color:#e50914!important">Hub</span></h1>'
    '<p class="hero-copy">Explore viewing patterns, audience activity, and the signals behind the numbers in your selected dataset.</p>'
    f'<div class="hero-meta"><b>{len(data):,}</b> viewing records <span>·</span> '
    f'<b>{data["Title"].nunique():,}</b> distinct titles <span>·</span> {hero_date_label}</div>'
    '<a class="hero-cta" href="#analytics">Explore analytics <span aria-hidden="true">↘</span></a>'
    '</div></div>',
    unsafe_allow_html=True,
)

section_heading("AT A GLANCE", "The viewing landscape", "A live snapshot of the selected viewing records. Use the filters below to explore a specific slice.", "dashboard")
st.markdown('<div class="filter-wrap"><p class="filter-label">REFINE THE VIEW</p>', unsafe_allow_html=True)
filter_columns = st.columns(5, gap="small")
filter_specs = [("Type", "Content type"), ("Region", "Region"), ("Rating", "Rating"), ("_WatchYear", "Watch year"), ("Category", "Category")]
selections: dict[str, list] = {}
for column, (field, label) in zip(filter_columns, filter_specs):
    with column:
        selections[field] = st.multiselect(label, options_for(data, field), placeholder="All", key=f"filter_{field}")
st.markdown('</div>', unsafe_allow_html=True)

filtered = apply_filters(data, selections)
titles = filtered.dropna(subset=["Title"])
movie_titles = titles.loc[titles["Type"].eq("Movie"), "Title"].nunique()
show_titles = titles.loc[titles["Type"].eq("TV Show"), "Title"].nunique()
watch_date_range = "No dates" if filtered.empty else (
    f'{filtered["Watch_Date"].min():%b %Y} – {filtered["Watch_Date"].max():%b %Y}'
    if filtered["Watch_Date"].notna().any() else "Dates unavailable"
)
metric_data = [
    ("Total titles", f'{titles["Title"].nunique():,}', "Distinct titles in view"),
    ("Movies", f"{movie_titles:,}", "Distinct movie titles"),
    ("TV shows", f"{show_titles:,}", "Distinct series titles"),
    ("Regions", f'{filtered["Region"].nunique():,}', "Viewing regions represented"),
    ("Customers", f'{filtered["Customer_ID"].nunique():,}' if "Customer_ID" in filtered else "—", "Unique customer records"),
    ("Categories", f'{filtered["Category"].nunique():,}', "Distinct content categories"),
]
st.markdown('<div class="metric-grid">', unsafe_allow_html=True)
metric_columns = st.columns(6, gap="small")
for index, (column, item) in enumerate(zip(metric_columns, metric_data)):
    with column:
        metric_card(*item, index)
st.markdown('</div>', unsafe_allow_html=True)

section_heading("EXPLORE", "Analytics", f"{len(filtered):,} records · viewing activity from {watch_date_range}", "analytics")
if filtered.empty:
    st.info("No records match these filters. Clear one or more filters to continue.")
else:
    chart_left, chart_right = st.columns(2, gap="large")
    with chart_left:
        st.markdown('<p class="chart-title">Movies vs TV shows</p><p class="chart-subtitle">Share of viewing records by content type</p>', unsafe_allow_html=True)
        type_counts = filtered["Type"].fillna("Unspecified").value_counts().rename_axis("Type").reset_index(name="Records")
        type_fig = px.pie(type_counts, names="Type", values="Records", hole=.68, color_discrete_sequence=PALETTE)
        type_fig.update_traces(textposition="outside", textinfo="label+percent", hovertemplate="%{label}<br>%{value} records · %{percent}<extra></extra>")
        type_fig.update_layout(showlegend=False)
        st.plotly_chart(style_figure(type_fig, 330), width="stretch", config={"displayModeBar": False})
    with chart_right:
        st.markdown('<p class="chart-title">Viewing activity by month</p><p class="chart-subtitle">Watch records grouped by viewing month</p>', unsafe_allow_html=True)
        monthly = filtered.dropna(subset=["Watch_Date"]).groupby("_WatchMonth", as_index=False).agg(Records=("Title", "size"), Revenue=("Monthly_Revenue", "sum"))
        if monthly.empty:
            st.info("No valid watch dates in this selection.")
        else:
            month_fig = px.area(monthly, x="_WatchMonth", y="Records", markers=True, color_discrete_sequence=[RED], custom_data=["Revenue"])
            month_fig.update_traces(fillcolor="rgba(229,9,20,.16)", line={"width": 3}, hovertemplate="%{x}<br>%{y} viewing records<br>Revenue: ₹%{customdata[0]:,.0f}<extra></extra>")
            month_fig.update_layout(xaxis_title="Watch month", yaxis_title="Records")
            st.plotly_chart(style_figure(month_fig), width="stretch", config={"displayModeBar": False})

    chart_left, chart_right = st.columns(2, gap="large")
    with chart_left:
        st.markdown('<p class="chart-title">Top regions</p><p class="chart-subtitle">Viewing records by region, ranked</p>', unsafe_allow_html=True)
        region_counts = filtered["Region"].fillna("Unspecified").value_counts().head(10).sort_values().rename_axis("Region").reset_index(name="Records")
        region_fig = px.bar(region_counts, x="Records", y="Region", orientation="h", text="Records", color="Records", color_continuous_scale=[[0, "#5a171c"], [1, RED]])
        region_fig.update_traces(textposition="outside", hovertemplate="%{y}<br>%{x} records<extra></extra>")
        region_fig.update_layout(coloraxis_showscale=False, xaxis_title="Viewing records", yaxis_title="")
        st.plotly_chart(style_figure(region_fig), width="stretch", config={"displayModeBar": False})
    with chart_right:
        st.markdown('<p class="chart-title">Content rating distribution</p><p class="chart-subtitle">Audience ratings captured in the dataset</p>', unsafe_allow_html=True)
        rating_values = filtered.dropna(subset=["Rating"])
        if rating_values.empty:
            st.info("No ratings available in this selection.")
        else:
            rating_fig = px.histogram(rating_values, x="Rating", nbins=min(10, max(1, rating_values["Rating"].nunique())), color_discrete_sequence=["#f05d5e"])
            rating_fig.update_traces(marker_line_color="#2a1718", marker_line_width=1, hovertemplate="Rating %{x}<br>%{y} records<extra></extra>")
            rating_fig.update_layout(xaxis_title="Rating", yaxis_title="Viewing records", bargap=.16)
            st.plotly_chart(style_figure(rating_fig), width="stretch", config={"displayModeBar": False})

    chart_left, chart_right = st.columns(2, gap="large")
    with chart_left:
        st.markdown('<p class="chart-title">Popular categories</p><p class="chart-subtitle">Most-watched content categories</p>', unsafe_allow_html=True)
        category_counts = filtered["Category"].fillna("Unspecified").value_counts().head(10).sort_values().rename_axis("Category").reset_index(name="Records")
        category_fig = px.bar(category_counts, x="Records", y="Category", orientation="h", color="Category", color_discrete_sequence=PALETTE)
        category_fig.update_layout(showlegend=False, xaxis_title="Viewing records", yaxis_title="")
        category_fig.update_traces(hovertemplate="%{y}<br>%{x} records<extra></extra>")
        st.plotly_chart(style_figure(category_fig), width="stretch", config={"displayModeBar": False})
    with chart_right:
        st.markdown('<p class="chart-title">Movie vs TV activity by month</p><p class="chart-subtitle">Viewing records split by format over time</p>', unsafe_allow_html=True)
        by_month_type = filtered.dropna(subset=["Watch_Date"]).groupby(["_WatchMonth", "Type"], as_index=False).size().rename(columns={"size": "Records"})
        if by_month_type.empty:
            st.info("No valid watch dates in this selection.")
        else:
            activity_fig = px.bar(by_month_type, x="_WatchMonth", y="Records", color="Type", barmode="stack", color_discrete_sequence=PALETTE)
            activity_fig.update_layout(xaxis_title="Watch month", yaxis_title="Viewing records", legend_title_text="")
            activity_fig.update_traces(hovertemplate="%{x}<br>%{fullData.name}: %{y} records<extra></extra>")
            st.plotly_chart(style_figure(activity_fig), width="stretch", config={"displayModeBar": False})

    chart_left, chart_right = st.columns(2, gap="large")
    with chart_left:
        st.markdown('<p class="chart-title">Revenue by region</p><p class="chart-subtitle">Monthly revenue attributed to each viewing region</p>', unsafe_allow_html=True)
        revenue = filtered.groupby("Region", dropna=False, as_index=False)["Monthly_Revenue"].sum().sort_values("Monthly_Revenue")
        revenue["Region"] = revenue["Region"].fillna("Unspecified")
        revenue_fig = px.bar(revenue, x="Monthly_Revenue", y="Region", orientation="h", color_discrete_sequence=[RED], text_auto=".2s")
        revenue_fig.update_layout(xaxis_title="Monthly revenue", yaxis_title="", xaxis_tickprefix="₹")
        st.plotly_chart(style_figure(revenue_fig), width="stretch", config={"displayModeBar": False})
    with chart_right:
        st.markdown('<p class="chart-title">Average rating by subscription</p><p class="chart-subtitle">Rating patterns across plan tiers</p>', unsafe_allow_html=True)
        plan_rating = filtered.groupby("Subscription_Plan", as_index=False)["Rating"].mean().dropna() if "Subscription_Plan" in filtered else pd.DataFrame(columns=["Subscription_Plan", "Rating"])
        if plan_rating.empty:
            st.info("No subscription ratings available in this selection.")
        else:
            plan_fig = px.bar(plan_rating, x="Subscription_Plan", y="Rating", color="Subscription_Plan", color_discrete_sequence=PALETTE, text_auto=".2f")
            plan_fig.update_layout(showlegend=False, xaxis_title="Subscription plan", yaxis_title="Average rating")
            st.plotly_chart(style_figure(plan_fig), width="stretch", config={"displayModeBar": False})

section_heading("SIGNALS", "Insights from this selection", "Every callout is computed from the filtered rows currently in view.", "insights")


def leading_value(series: pd.Series) -> tuple[str, str]:
    counts = series.dropna().value_counts()
    return (str(counts.index[0]), f"{int(counts.iloc[0]):,} records") if not counts.empty else ("No data", "")


content_leader, content_count = leading_value(filtered["Type"])
region_leader, region_count = leading_value(filtered["Region"])
rating_leader, rating_count = leading_value(filtered["Rating"])
category_leader, category_count = leading_value(filtered["Category"])
year_counts = filtered["_WatchYear"].dropna().value_counts()
year_leader = str(int(year_counts.index[0])) if not year_counts.empty else "No data"
year_count = f"{int(year_counts.iloc[0]):,} viewing records" if not year_counts.empty else ""
insights = [
    ("Most common format", content_leader, content_count),
    ("Busiest watch year", year_leader, year_count),
    ("Top region", region_leader, region_count),
    ("Most common rating", rating_leader, rating_count),
    ("Popular category", category_leader, category_count),
]
st.markdown('<div class="insight-grid">' + "".join(
    f'<div class="insight-card"><span>{escape(label)}</span><strong>{escape(value)}</strong><em>{escape(note)}</em></div>'
    for label, value, note in insights
) + '</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="data-note"><strong>Data scope:</strong> charts use the columns available in the active file. '
    'Time-based views use valid values in <code>Watch_Date</code>; region and category views use their matching columns when present.</div>',
    unsafe_allow_html=True,
)

section_heading("CATALOG", "Data Explorer", "Search and inspect the selected records. The table is sortable by column and paginated for quick scanning.", "data-explorer")
title_query = st.text_input("Search titles", placeholder="Search by title, category, region, or type", key="title_search")
searchable = filtered.copy()
if title_query.strip():
    search_columns = [column for column in ["Title", "Category", "Region", "Type"] if column in searchable]
    matches = searchable[search_columns].astype("string").apply(
        lambda column: column.str.contains(title_query.strip(), case=False, na=False, regex=False)
    ).any(axis=1)
    searchable = searchable[matches]
preferred_columns = ["Title", "Category", "Type", "Rating", "Region", "Subscription_Plan", "Watch_Date", "Watch_Count", "Watch_Time_Minutes", "Language", "Device", "Monthly_Revenue"]
display_columns = [column for column in preferred_columns if column in searchable.columns]
display_columns.extend(column for column in searchable.columns if column not in display_columns and not column.startswith("_"))
page_size = 10
page_count = max(1, (len(searchable) + page_size - 1) // page_size)
if "table_page" not in st.session_state:
    st.session_state.table_page = 1
st.session_state.table_page = min(st.session_state.table_page, page_count)
page_left, page_center, page_right = st.columns([1, 2, 1])
with page_left:
    if st.button("← Previous", disabled=st.session_state.table_page <= 1, width="stretch"):
        st.session_state.table_page -= 1
        st.rerun()
with page_center:
    st.markdown(f'<div class="pagination-label">Page {st.session_state.table_page} of {page_count} · {len(searchable):,} matching records</div>', unsafe_allow_html=True)
with page_right:
    if st.button("Next →", disabled=st.session_state.table_page >= page_count, width="stretch"):
        st.session_state.table_page += 1
        st.rerun()
start = (st.session_state.table_page - 1) * page_size
table_page = searchable.iloc[start:start + page_size][display_columns].copy()
if "Watch_Date" in table_page:
    table_page["Watch_Date"] = table_page["Watch_Date"].dt.strftime("%b %d, %Y")
if "Monthly_Revenue" in table_page:
    table_page["Monthly_Revenue"] = table_page["Monthly_Revenue"].map(lambda value: f"₹{value:,.0f}")
st.markdown('<p class="table-note">Select a column header to sort. Customer names and identifiers are intentionally omitted from this portfolio view.</p>', unsafe_allow_html=True)
st.dataframe(table_page, width="stretch", hide_index=True, height=430)

section_heading("PROJECT", "About this dashboard", "A focused exploration of viewing behavior and subscription signals in the active dataset.", "about")
st.markdown(
    f'<footer class="footer"><div><strong>Data Visualization Hub</strong><br>Active dataset: {escape(dataset_label)}</div>'
    '<div>Built with Streamlit · pandas · Plotly<br><a href="https://github.com/" target="_blank">GitHub</a>'
    '<a href="https://www.linkedin.com/" target="_blank">LinkedIn</a></div></footer>',
    unsafe_allow_html=True,
)