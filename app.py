import streamlit as st
import pandas as pd
import joblib
import requests
import os
import subprocess
import sys
import time
from urllib.parse import urlparse

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ContentPulse AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ================================
       GLOBAL
    ================================= */

    .stApp {
        background: #f5f7fb;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: #111827 !important;
    }

    p, li, label {
        color: #374151;
    }

    /* ================================
       SIDEBAR
    ================================= */

    [data-testid="stSidebar"] {
        background: #0f172a;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    .sidebar-brand {
        padding: 8px 5px 28px 5px;
        border-bottom: 1px solid rgba(255,255,255,0.10);
        margin-bottom: 24px;
    }

    .sidebar-brand-title {
        font-size: 24px;
        font-weight: 800;
        color: white;
        letter-spacing: -0.5px;
    }

    .sidebar-brand-subtitle {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 5px;
    }

    .sidebar-section {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #64748b;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .api-online {
        background: rgba(16,185,129,0.15);
        border: 1px solid rgba(16,185,129,0.25);
        padding: 12px 14px;
        border-radius: 12px;
        color: #6ee7b7;
        font-weight: 600;
        font-size: 13px;
    }

    .api-offline {
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.25);
        padding: 12px 14px;
        border-radius: 12px;
        color: #fca5a5;
        font-weight: 600;
        font-size: 13px;
    }

    /* ================================
       HERO
    ================================= */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 48px 50px;
        margin-bottom: 32px;
        border-radius: 26px;
        background:
            linear-gradient(
                135deg,
                #0f172a 0%,
                #172554 45%,
                #1d4ed8 100%
            );
        box-shadow:
            0 25px 60px rgba(15,23,42,0.20);
        border: 1px solid rgba(255,255,255,0.08);
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -100px;
        top: -120px;
        background: rgba(96,165,250,0.18);
        border-radius: 50%;
        filter: blur(5px);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        right: 180px;
        bottom: -120px;
        background: rgba(129,140,248,0.15);
        border-radius: 50%;
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    .hero-title {
        font-size: 52px;
        line-height: 1.1;
        font-weight: 850;
        color: #ffffff !important;
        letter-spacing: -2px;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 21px;
        line-height: 1.5;
        font-weight: 600;
        color: #dbeafe !important;
        margin-bottom: 16px;
    }

    .hero-description {
        max-width: 900px;
        font-size: 16px;
        line-height: 1.75;
        color: #cbd5e1 !important;
        margin-bottom: 25px;
    }

    .hero-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .hero-tag {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.09);
        border: 1px solid rgba(255,255,255,0.13);
        color: #f8fafc !important;
        font-size: 13px;
        font-weight: 600;
    }

    /* ================================
       SECTION HEADERS
    ================================= */

    .section-title {
        font-size: 30px;
        font-weight: 800;
        color: #111827 !important;
        margin-top: 12px;
        margin-bottom: 6px;
        letter-spacing: -0.7px;
    }

    .section-subtitle {
        color: #6b7280 !important;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 24px;
    }

    /* ================================
       FEATURE CARDS
    ================================= */

    .feature-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 24px;
        min-height: 180px;
        box-shadow: 0 8px 25px rgba(15,23,42,0.05);
    }

    .feature-icon {
        font-size: 28px;
        margin-bottom: 12px;
    }

    .feature-title {
        font-size: 17px;
        font-weight: 750;
        color: #111827 !important;
        margin-bottom: 7px;
    }

    .feature-text {
        font-size: 13px;
        line-height: 1.6;
        color: #6b7280 !important;
    }

    /* ================================
       METRIC CARDS
    ================================= */

    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 8px 25px rgba(15,23,42,0.05);
        min-height: 120px;
    }

    .metric-label {
        font-size: 13px;
        font-weight: 600;
        color: #64748b !important;
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 850;
        color: #111827 !important;
        letter-spacing: -1px;
    }

    .metric-small {
        font-size: 12px;
        color: #94a3b8 !important;
        margin-top: 5px;
    }

    /* ================================
       ANALYZER CARD
    ================================= */

    .analyzer-card {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f8fafc 100%
        );
        border: 1px solid #dbe3ef;
        border-radius: 22px;
        padding: 30px;
        margin: 25px 0;
        box-shadow: 0 15px 40px rgba(15,23,42,0.07);
    }

    .analyzer-title {
        font-size: 22px;
        font-weight: 800;
        color: #111827 !important;
        margin-bottom: 6px;
    }

    .analyzer-description {
        color: #64748b !important;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* ================================
       STATUS BADGES
    ================================= */

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 750;
    }

    .badge-high {
        background: #fee2e2;
        color: #b91c1c !important;
    }

    .badge-medium {
        background: #fef3c7;
        color: #92400e !important;
    }

    .badge-low {
        background: #dcfce7;
        color: #166534 !important;
    }

    /* ================================
       INFO BOX
    ================================= */

    .info-card {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 16px;
        padding: 18px 20px;
        color: #1e40af !important;
        font-size: 14px;
        line-height: 1.6;
        margin: 15px 0;
    }

    .warning-card {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 16px;
        padding: 18px 20px;
        color: #92400e !important;
        font-size: 14px;
        line-height: 1.6;
    }

    .success-card {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 18px 20px;
        color: #065f46 !important;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ================================
       FOOTER
    ================================= */

    .footer {
        margin-top: 50px;
        padding: 25px;
        text-align: center;
        border-top: 1px solid #e5e7eb;
        color: #64748b !important;
        font-size: 12px;
        line-height: 1.8;
    }

    .footer b {
        color: #334155 !important;
    }

    /* ================================
       STREAMLIT BUTTONS
    ================================= */

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        border: 1px solid #dbe3ef;
        min-height: 42px;
    }

    .stButton > button:hover {
        border-color: #2563eb;
        color: #2563eb;
    }

    /* ================================
       DATAFRAME
    ================================= */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ================================
       MOBILE
    ================================= */

    @media (max-width: 768px) {

        .hero {
            padding: 32px 25px;
        }

        .hero-title {
            font-size: 36px;
        }

        .hero-subtitle {
            font-size: 17px;
        }

        .section-title {
            font-size: 25px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CONSTANTS
# =========================================================

API_URL = "http://127.0.0.1:8000"

MODEL_PATH = "models/content_priority_model.pkl"
DATA_PATH = "data/content_data.csv"


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_number(value, default=0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def format_number(value):
    try:
        return f"{int(float(value)):,}"
    except Exception:
        return "0"


def format_score(value):
    value = safe_number(value)

    if value <= 1:
        value = value * 100

    return f"{value:.0f}%"


def priority_badge(priority):
    priority = str(priority).strip().lower()

    if priority == "high":
        return '<span class="badge badge-high">HIGH PRIORITY</span>'

    if priority == "medium":
        return '<span class="badge badge-medium">MEDIUM PRIORITY</span>'

    return '<span class="badge badge-low">LOW PRIORITY</span>'


def normalize_url(url):
    url = str(url).strip()

    if not url:
        return ""

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def get_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return url


def api_request(endpoint, payload, timeout=90):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=timeout
        )

        if response.status_code == 200:
            return response.json(), None

        try:
            error_data = response.json()
            return None, str(error_data)
        except Exception:
            return None, response.text

    except requests.exceptions.ConnectionError:
        return None, (
            "FastAPI server is not running. "
            "Start it with: python -m uvicorn api:app --reload"
        )

    except requests.exceptions.Timeout:
        return None, "API request timed out. Please try again."

    except Exception as e:
        return None, str(e)


@st.cache_data(ttl=5, show_spinner=False)
def check_api():
    try:
        response = requests.get(
            API_URL,
            timeout=1
        )

        return response.status_code == 200

    except Exception:
        return False


def start_api_server():
    process = st.session_state.get("api_process")

    if process is not None and process.poll() is None:
        return

    launch_options = {
        "cwd": os.path.dirname(os.path.abspath(__file__)),
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }

    if os.name == "nt":
        launch_options["creationflags"] = subprocess.CREATE_NO_WINDOW

    try:
        st.session_state.api_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "api:app",
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
            ],
            **launch_options
        )
    except Exception:
        st.session_state.api_process = None


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


model = load_model()


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_dataset():

    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()

    try:
        return pd.read_csv(DATA_PATH)
    except Exception:
        return pd.DataFrame()


df = load_dataset()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">
                📊 ContentPulse AI
            </div>
            <div class="sidebar-brand-subtitle">
                Website Content Intelligence Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">Navigation</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Select Module",
        [
            "🏠 Overview",
            "📊 Dataset Dashboard",
            "🌐 Live Website Analyzer"
        ],
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="sidebar-section">System</div>',
        unsafe_allow_html=True
    )

    api_online = check_api()

    if not api_online:
        start_api_server()
        time.sleep(0.5)
        check_api.clear()
        api_online = check_api()

    if api_online:

        st.markdown(
            """
            <div class="api-online">
                🟢 API Online<br>
                <span style="font-size:11px;">
                FastAPI backend connected
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="api-offline">
                🔴 API Offline<br>
                <span style="font-size:11px;">
                FastAPI is starting. Refresh shortly.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div style="
            margin-top:30px;
            padding-top:20px;
            border-top:1px solid rgba(255,255,255,0.10);
            color:#94a3b8;
            font-size:11px;
            line-height:1.7;
        ">
        ContentPulse AI analyzes publicly accessible
        website content and HTML signals.
        <br><br>
        Private Google Analytics, Search Console,
        backlink and conversion data are not accessed
        without authorized integrations.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HERO
# =========================================================

st.html(
    """
    <div class="hero">
        <div class="hero-content">

            <div class="hero-title">
                📊 ContentPulse AI
            </div>

            <div class="hero-subtitle">
                AI-Powered Website Content Analyzer & Refresh Recommendation
            </div>

            <div class="hero-description">
                Analyze website content, identify content quality issues,
                evaluate refresh opportunities, and prioritize pages using
                machine-learning assisted decision support.
            </div>

            <div class="hero-tags">
                <span class="hero-tag">🤖 Machine Learning</span>
                <span class="hero-tag">🌐 Live Website Analysis</span>
                <span class="hero-tag">📈 Content Intelligence</span>
                <span class="hero-tag">🔎 SEO Signals</span>
                <span class="hero-tag">⚡ FastAPI</span>
            </div>

        </div>
    </div>
    """,
)


# =========================================================
# OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">🚀 Project Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            ContentPulse AI is an AI-assisted website content intelligence
            platform designed to analyze content quality, identify refresh
            opportunities, and help prioritize pages that may need attention.
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # Feature Cards
    # -----------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">
                    Live Website Analysis
                </div>
                <div class="feature-text">
                    Analyze publicly accessible website pages directly
                    using the FastAPI backend.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <div class="feature-title">
                    ML-Assisted Scoring
                </div>
                <div class="feature-text">
                    Use machine-learning predictions to support
                    content refresh prioritization.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔎</div>
                <div class="feature-title">
                    Content & SEO Signals
                </div>
                <div class="feature-text">
                    Inspect titles, headings, links, images, content
                    length, quality and other public signals.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">
                    Actionable Recommendations
                </div>
                <div class="feature-text">
                    Get practical suggestions for improving content
                    structure and refresh readiness.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------
    # Dataset Stats
    # -----------------------------------------

    if not df.empty:

        total_pages = len(df)

        high_count = 0
        medium_count = 0
        low_count = 0

        if "priority" in df.columns:

            priority_series = (
                df["priority"]
                .astype(str)
                .str.lower()
            )

            high_count = int(
                (priority_series == "high").sum()
            )

            medium_count = int(
                (priority_series == "medium").sum()
            )

            low_count = int(
                (priority_series == "low").sum()
            )

        st.markdown(
            '<div class="section-title">📊 Current Dataset</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">Local content dataset summary</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">DATASET PAGES</div>
                    <div class="metric-value">{format_number(total_pages)}</div>
                    <div class="metric-small">Analyzed records</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">HIGH PRIORITY</div>
                    <div class="metric-value">{format_number(high_count)}</div>
                    <div class="metric-small">Needs attention first</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">MEDIUM PRIORITY</div>
                    <div class="metric-value">{format_number(medium_count)}</div>
                    <div class="metric-small">Potential opportunity</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">LOW PRIORITY</div>
                    <div class="metric-value">{format_number(low_count)}</div>
                    <div class="metric-small">Lower urgency</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------
    # How it works
    # -----------------------------------------

    st.markdown(
        '<div class="section-title">⚙️ How ContentPulse AI Works</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            A simple workflow from website URL to actionable content insights.
        </div>
        """,
        unsafe_allow_html=True
    )

    w1, w2, w3, w4 = st.columns(4)

    steps = [
        (
            w1,
            "01",
            "Enter Website",
            "Provide a public website or page URL."
        ),
        (
            w2,
            "02",
            "Collect Signals",
            "Extract publicly accessible HTML and content signals."
        ),
        (
            w3,
            "03",
            "Analyze",
            "Evaluate content quality, structure and refresh signals."
        ),
        (
            w4,
            "04",
            "Prioritize",
            "Generate refresh priority and recommendations."
        )
    ]

    for col, number, title, description in steps:

        with col:

            st.html(
                f"""
                <div class="feature-card">
                    <div style="
                        font-size:12px;
                        font-weight:800;
                        color:#2563eb;
                        margin-bottom:12px;
                    ">
                        STEP {number}
                    </div>

                    <div class="feature-title">
                        {title}
                    </div>

                    <div class="feature-text">
                        {description}
                    </div>
                </div>
                """,
            )

    st.markdown(
        """
        <div class="info-card">
            💡 <b>Important:</b>
            Public website analysis does not automatically provide
            private traffic, Google Search Console, Google Analytics,
            backlink or conversion data. Those require authorized
            integrations.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DATASET DASHBOARD
# =========================================================

elif page == "📊 Dataset Dashboard":

    st.markdown(
        '<div class="section-title">📊 Dataset Intelligence Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Explore content priorities, refresh scores, traffic signals
            and ML-assisted recommendations from the local dataset.
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:

        st.error(
            "Dataset not found. Make sure "
            "`data/content_data.csv` exists."
        )

    else:

        # -----------------------------------------
        # Dataset overview metrics
        # -----------------------------------------

        total_pages = len(df)

        high_count = 0
        medium_count = 0
        low_count = 0

        if "priority" in df.columns:

            priorities = (
                df["priority"]
                .astype(str)
                .str.lower()
            )

            high_count = int(
                (priorities == "high").sum()
            )

            medium_count = int(
                (priorities == "medium").sum()
            )

            low_count = int(
                (priorities == "low").sum()
            )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">TOTAL PAGES</div>
                    <div class="metric-value">{format_number(total_pages)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">HIGH PRIORITY</div>
                    <div class="metric-value">{format_number(high_count)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">MEDIUM PRIORITY</div>
                    <div class="metric-value">{format_number(medium_count)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">LOW PRIORITY</div>
                    <div class="metric-value">{format_number(low_count)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # -----------------------------------------
        # Filters
        # -----------------------------------------

        st.markdown(
            '<div class="section-title">🎛️ Dataset Filters</div>',
            unsafe_allow_html=True
        )

        f1, f2 = st.columns(2)

        filtered_df = df.copy()

        with f1:

            if "priority" in df.columns:

                available_priorities = [
                    "All",
                    "High",
                    "Medium",
                    "Low"
                ]

                selected_priority = st.selectbox(
                    "Priority",
                    available_priorities
                )

                if selected_priority != "All":

                    filtered_df = filtered_df[
                        filtered_df["priority"]
                        .astype(str)
                        .str.lower()
                        ==
                        selected_priority.lower()
                    ]

        with f2:

            if "refresh_score" in df.columns:

                min_score = st.slider(
                    "Minimum Refresh Score",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.05
                )

                filtered_df = filtered_df[
                    pd.to_numeric(
                        filtered_df["refresh_score"],
                        errors="coerce"
                    ).fillna(0)
                    >= min_score
                ]

        st.markdown(
            f"""
            <div class="info-card">
                Showing <b>{len(filtered_df):,}</b> pages after filtering.
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------------------
        # Charts
        # -----------------------------------------

        chart1, chart2 = st.columns(2)

        with chart1:

            st.markdown("### 📌 Priority Distribution")

            if "priority" in df.columns:

                priority_counts = (
                    df["priority"]
                    .astype(str)
                    .str.title()
                    .value_counts()
                )

                st.bar_chart(priority_counts)

        with chart2:

            st.markdown("### 📈 Refresh Score Distribution")

            if "refresh_score" in df.columns:

                score_data = pd.to_numeric(
                    df["refresh_score"],
                    errors="coerce"
                ).dropna()

                if not score_data.empty:

                    score_bins = pd.cut(
                        score_data,
                        bins=[0, .2, .4, .6, .8, 1.0],
                        labels=[
                            "0-20%",
                            "20-40%",
                            "40-60%",
                            "60-80%",
                            "80-100%"
                        ],
                        include_lowest=True
                    )

                    distribution = score_bins.value_counts(
                        sort=False
                    )

                    st.bar_chart(distribution)

        st.markdown("<br>", unsafe_allow_html=True)

        # -----------------------------------------
        # Filtered data
        # -----------------------------------------

        st.markdown(
            '<div class="section-title">📋 Content Pages</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Filtered CSV",
            data=filtered_df.to_csv(index=False).encode("utf-8"),
            file_name="contentpulse_filtered_pages.csv",
            mime="text/csv",
            use_container_width=True
        )

        # -----------------------------------------
        # High priority
        # -----------------------------------------

        if "priority" in df.columns:

            high_priority_df = df[
                df["priority"]
                .astype(str)
                .str.lower()
                == "high"
            ].copy()

            if not high_priority_df.empty:

                st.markdown(
                    '<div class="section-title">🔥 High Priority Pages</div>',
                    unsafe_allow_html=True
                )

                display_columns = [
                    col for col in [
                        "url",
                        "title",
                        "refresh_score",
                        "priority",
                        "traffic",
                        "monthly_traffic"
                    ]
                    if col in high_priority_df.columns
                ]

                if display_columns:

                    st.dataframe(
                        high_priority_df[
                            display_columns
                        ].head(20),
                        use_container_width=True,
                        hide_index=True
                    )

        # -----------------------------------------
        # Individual page analysis
        # -----------------------------------------

        st.markdown(
            '<div class="section-title">🔍 Individual Page Analysis</div>',
            unsafe_allow_html=True
        )

        if len(filtered_df) > 0:

            selected_index = st.selectbox(
                "Select a page",
                filtered_df.index,
                format_func=lambda x: str(
                    filtered_df.loc[x].get(
                        "url",
                        filtered_df.loc[x].get(
                            "title",
                            f"Page {x}"
                        )
                    )
                )
            )

            selected_data = filtered_df.loc[
                selected_index
            ]

            refresh_score = safe_number(
                selected_data.get(
                    "refresh_score",
                    0
                )
            )

            priority = str(
                selected_data.get(
                    "priority",
                    "Unknown"
                )
            )

            traffic = safe_number(
                selected_data.get(
                    "monthly_traffic",
                    selected_data.get(
                        "traffic",
                        0
                    )
                )
            )

            d1, d2, d3 = st.columns(3)

            with d1:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">REFRESH SCORE</div>
                        <div class="metric-value">
                            {format_score(refresh_score)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with d2:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">PRIORITY</div>
                        <div style="margin-top:14px;">
                            {priority_badge(priority)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with d3:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">MONTHLY TRAFFIC</div>
                        <div class="metric-value">
                            {format_number(traffic)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("<br>", unsafe_allow_html=True)

            # -----------------------------------------
            # ML Prediction
            # -----------------------------------------

            st.markdown("### 🤖 ML Model Prediction")

            if model is not None:

                feature_columns = [
                    "word_count",
                    "content_age_days",
                    "days_since_update",
                    "monthly_traffic",
                    "search_volume",
                    "avg_position",
                    "ctr",
                    "engagement_rate",
                    "bounce_rate",
                    "backlinks",
                    "content_quality"
                ]

                available_features = []

                for feature in feature_columns:

                    if feature in selected_data.index:
                        available_features.append(feature)

                if len(available_features) == len(feature_columns):

                    try:

                        input_data = pd.DataFrame(
                            [[
                                safe_number(
                                    selected_data[col]
                                )
                                for col in feature_columns
                            ]],
                            columns=feature_columns
                        )

                        prediction = model.predict(
                            input_data
                        )[0]

                        st.success(
                            f"ML Prediction: {prediction}"
                        )

                        if hasattr(model, "predict_proba"):
                            confidence = max(
                                model.predict_proba(input_data)[0]
                            )
                            st.caption(
                                f"Prediction confidence: {confidence:.1%}"
                            )

                    except Exception as e:

                        st.warning(
                            f"ML prediction could not be generated: {e}"
                        )

                else:

                    st.info(
                        "Required ML feature columns are not available "
                        "for this dataset row."
                    )

            else:

                st.warning(
                    "ML model file not found. "
                    "Make sure models/content_priority_model.pkl exists."
                )

            # -----------------------------------------
            # Recommendation
            # -----------------------------------------

            if refresh_score >= 0.65:

                st.markdown(
                    """
                    <div class="warning-card">
                        🔥 <b>Recommended Action:</b><br>
                        This page appears to have a strong refresh opportunity.
                        Review content freshness, structure, relevance,
                        search intent and overall quality.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif refresh_score >= 0.40:

                st.markdown(
                    """
                    <div class="info-card">
                        🟡 <b>Recommended Action:</b><br>
                        Consider reviewing this page for moderate
                        content improvements and freshness updates.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="success-card">
                        🟢 <b>Recommended Action:</b><br>
                        This page currently has a lower refresh priority.
                        Continue monitoring its performance.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# LIVE WEBSITE ANALYZER
# =========================================================

elif page == "🌐 Live Website Analyzer":

    st.markdown(
        '<div class="section-title">🌐 Live Website Analyzer</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-subtitle">
            Analyze a public webpage or crawl multiple pages from a website
            using the ContentPulse AI FastAPI backend.
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------
    # Analyzer mode
    # -----------------------------------------

    mode = st.radio(
        "Analysis Mode",
        [
            "📄 Single Page",
            "🕷️ Full Website"
        ],
        horizontal=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # SINGLE PAGE
    # =====================================================

    if mode == "📄 Single Page":

        st.html(
            """
            <div class="analyzer-card">
                <div class="analyzer-title">
                    🔎 Analyze One Web Page
                </div>

                <div class="analyzer-description">
                    Enter a public URL to inspect content, structure,
                    links, images, quality and refresh signals.
                </div>
            </div>
            """,
        )

        website_url = st.text_input(
            "Website URL",
            placeholder="https://example.com/blog/article",
            key="single_page_url"
        )

        analyze_button = st.button(
            "🚀 Analyze Page",
            use_container_width=True
        )

        if analyze_button:

            website_url = normalize_url(
                website_url
            )

            if not website_url:

                st.error(
                    "Please enter a website URL."
                )

            else:

                with st.spinner(
                    "Analyzing webpage..."
                ):

                    result, error = api_request(
                        "/analyze-url",
                        {
                            "url": website_url
                        },
                        timeout=90
                    )

                if error:

                    st.error(
                        f"Analysis failed: {error}"
                    )

                elif result:

                    # -------------------------------------
                    # Basic information
                    # -------------------------------------

                    page_url = result.get(
                        "url",
                        website_url
                    )

                    title = result.get(
                        "title",
                        "Not available"
                    )

                    meta_description = result.get(
                        "meta_description",
                        result.get(
                            "description",
                            "Not available"
                        )
                    )

                    st.markdown(
                        f"""
                        <div class="success-card">
                            ✅ <b>Analysis completed</b><br>
                            Domain: <b>{get_domain(page_url)}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        "### 📄 Page Information"
                    )

                    st.markdown(
                        f"""
                        <div class="feature-card">

                            <div class="feature-title">
                                {title}
                            </div>

                            <div class="feature-text">
                                <b>URL:</b> {page_url}
                                <br><br>
                                <b>Meta Description:</b>
                                {meta_description}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # -------------------------------------
                    # Extract metrics
                    # -------------------------------------

                    word_count = safe_number(
                        result.get(
                            "word_count",
                            0
                        )
                    )

                    headings = safe_number(
                        result.get(
                            "headings",
                            result.get(
                                "heading_count",
                                0
                            )
                        )
                    )

                    internal_links = safe_number(
                        result.get(
                            "internal_links",
                            0
                        )
                    )

                    external_links = safe_number(
                        result.get(
                            "external_links",
                            0
                        )
                    )

                    images = safe_number(
                        result.get(
                            "images",
                            result.get(
                                "image_count",
                                0
                            )
                        )
                    )

                    images_without_alt = safe_number(
                        result.get(
                            "images_without_alt",
                            result.get(
                                "missing_alt",
                                0
                            )
                        )
                    )

                    quality_score = safe_number(
                        result.get(
                            "content_quality",
                            result.get(
                                "quality_score",
                                0
                            )
                        )
                    )

                    refresh_score = safe_number(
                        result.get(
                            "refresh_score",
                            0
                        )
                    )

                    priority = result.get(
                        "priority",
                        "Unknown"
                    )

                    # -------------------------------------
                    # Main metrics
                    # -------------------------------------

                    st.markdown(
                        "### 📊 Content Health"
                    )

                    m1, m2, m3, m4 = st.columns(4)

                    with m1:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    WORD COUNT
                                </div>
                                <div class="metric-value">
                                    {format_number(word_count)}
                                </div>
                                <div class="metric-small">
                                    Page content
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with m2:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    CONTENT QUALITY
                                </div>
                                <div class="metric-value">
                                    {format_score(quality_score)}
                                </div>
                                <div class="metric-small">
                                    Quality signal
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with m3:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    REFRESH SCORE
                                </div>
                                <div class="metric-value">
                                    {format_score(refresh_score)}
                                </div>
                                <div class="metric-small">
                                    Refresh opportunity
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with m4:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    PRIORITY
                                </div>
                                <div style="margin-top:15px;">
                                    {priority_badge(priority)}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # -------------------------------------
                    # Structure metrics
                    # -------------------------------------

                    st.markdown(
                        "### 🧱 Content Structure"
                    )

                    s1, s2, s3, s4 = st.columns(4)

                    structure = [
                        (
                            s1,
                            "HEADINGS",
                            headings
                        ),
                        (
                            s2,
                            "INTERNAL LINKS",
                            internal_links
                        ),
                        (
                            s3,
                            "EXTERNAL LINKS",
                            external_links
                        ),
                        (
                            s4,
                            "IMAGES",
                            images
                        )
                    ]

                    for col, label, value in structure:

                        with col:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-label">
                                        {label}
                                    </div>
                                    <div class="metric-value">
                                        {format_number(value)}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # -------------------------------------
                    # SEO / Media
                    # -------------------------------------

                    st.markdown(
                        "### 🔎 SEO & Media Signals"
                    )

                    seo1, seo2, seo3 = st.columns(3)

                    with seo1:

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    IMAGES WITHOUT ALT
                                </div>
                                <div class="metric-value">
                                    {format_number(images_without_alt)}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with seo2:

                        title_length = len(
                            str(title)
                        )

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    TITLE LENGTH
                                </div>
                                <div class="metric-value">
                                    {title_length}
                                </div>
                                <div class="metric-small">
                                    characters
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    with seo3:

                        meta_length = len(
                            str(meta_description)
                        )

                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">
                                    META LENGTH
                                </div>
                                <div class="metric-value">
                                    {meta_length}
                                </div>
                                <div class="metric-small">
                                    characters
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # -------------------------------------
                    # Scores
                    # -------------------------------------

                    st.markdown(
                        "### 📈 Score Overview"
                    )

                    score_col1, score_col2 = st.columns(2)

                    with score_col1:

                        st.markdown(
                            "**Refresh Opportunity**"
                        )

                        st.progress(
                            min(
                                max(refresh_score, 0),
                                1
                            )
                        )

                        st.caption(
                            f"Score: {format_score(refresh_score)}"
                        )

                    with score_col2:

                        st.markdown(
                            "**Content Quality**"
                        )

                        st.progress(
                            min(
                                max(quality_score, 0),
                                1
                            )
                        )

                        st.caption(
                            f"Score: {format_score(quality_score)}"
                        )

                    # -------------------------------------
                    # Recommendation
                    # -------------------------------------

                    st.markdown(
                        "### 💡 Recommendation"
                    )

                    if str(priority).lower() == "high":

                        st.markdown(
                            """
                            <div class="warning-card">
                                🔥 <b>High Refresh Opportunity</b><br>
                                This page should be reviewed first.
                                Focus on content freshness, search intent,
                                content depth, structure, internal linking
                                and media optimization.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    elif str(priority).lower() == "medium":

                        st.markdown(
                            """
                            <div class="info-card">
                                🟡 <b>Moderate Refresh Opportunity</b><br>
                                This page may benefit from targeted
                                improvements and periodic content review.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            """
                            <div class="success-card">
                                🟢 <b>Lower Refresh Priority</b><br>
                                The page currently shows fewer signals
                                indicating an immediate refresh need.
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # -------------------------------------
                    # Automated checks
                    # -------------------------------------

                    st.markdown(
                        "### 🧠 Automated Content Checks"
                    )

                    checks = []

                    if word_count < 500:
                        checks.append(
                            "⚠️ Low content depth: page contains fewer than 500 words."
                        )
                    else:
                        checks.append(
                            "✅ Content length is above the basic 500-word threshold."
                        )

                    if title_length < 30:
                        checks.append(
                            "⚠️ Page title may be too short."
                        )
                    elif title_length > 65:
                        checks.append(
                            "⚠️ Page title may be too long."
                        )
                    else:
                        checks.append(
                            "✅ Title length is within a reasonable range."
                        )

                    if meta_length == 0:
                        checks.append(
                            "⚠️ Meta description appears to be missing."
                        )
                    elif meta_length < 70:
                        checks.append(
                            "⚠️ Meta description may be too short."
                        )
                    elif meta_length > 170:
                        checks.append(
                            "⚠️ Meta description may be too long."
                        )
                    else:
                        checks.append(
                            "✅ Meta description length looks reasonable."
                        )

                    if headings == 0:
                        checks.append(
                            "⚠️ No headings were detected."
                        )
                    else:
                        checks.append(
                            "✅ Headings detected."
                        )

                    if images > 0 and images_without_alt > 0:
                        checks.append(
                            "⚠️ Some images appear to be missing ALT text."
                        )
                    elif images > 0:
                        checks.append(
                            "✅ Image ALT coverage looks good."
                        )

                    if internal_links == 0:
                        checks.append(
                            "⚠️ No internal links detected."
                        )
                    else:
                        checks.append(
                            "✅ Internal links detected."
                        )

                    for check in checks:

                        st.markdown(
                            f"- {check}"
                        )

                    # -------------------------------------
                    # Suggestions
                    # -------------------------------------

                    st.markdown(
                        "### 🛠️ Improvement Suggestions"
                    )

                    suggestions = []

                    if word_count < 500:
                        suggestions.append(
                            "Increase useful content depth where appropriate."
                        )

                    if title_length < 30 or title_length > 65:
                        suggestions.append(
                            "Review the page title for clarity and appropriate length."
                        )

                    if meta_length < 70 or meta_length > 170:
                        suggestions.append(
                            "Improve the meta description for better search-result messaging."
                        )

                    if headings < 2:
                        suggestions.append(
                            "Improve content structure with meaningful headings."
                        )

                    if images_without_alt > 0:
                        suggestions.append(
                            "Add descriptive ALT text to images where relevant."
                        )

                    if internal_links == 0:
                        suggestions.append(
                            "Consider adding relevant internal links."
                        )

                    if not suggestions:
                        suggestions.append(
                            "No major basic content issues were detected."
                        )

                    for suggestion in suggestions:

                        st.markdown(
                            f"- {suggestion}"
                        )

                    # -------------------------------------
                    # Detailed result
                    # -------------------------------------

                    with st.expander(
                        "📋 View Detailed Analysis"
                    ):

                        result_df = pd.DataFrame(
                            [
                                {
                                    "Metric": key,
                                    "Value": value
                                }
                                for key, value in result.items()
                                if not isinstance(
                                    value,
                                    (dict, list)
                                )
                            ]
                        )

                        st.dataframe(
                            result_df,
                            use_container_width=True,
                            hide_index=True
                        )

                    # -------------------------------------
                    # Raw API response
                    # -------------------------------------

                    with st.expander(
                        "🧩 View Raw API Response"
                    ):

                        st.json(result)

    # =====================================================
    # FULL WEBSITE
    # =====================================================

    else:

        st.html(
            """
            <div class="analyzer-card">
                <div class="analyzer-title">
                    🕷️ Full Website Analyzer
                </div>

                <div class="analyzer-description">
                    Crawl multiple public pages from the same website
                    and identify pages with higher refresh opportunities.
                </div>
            </div>
            """,
        )

        website_url = st.text_input(
            "Website URL",
            placeholder="https://example.com",
            key="full_website_url"
        )

        max_pages = st.slider(
            "Maximum Pages to Analyze",
            min_value=1,
            max_value=25,
            value=10,
            step=1
        )

        analyze_website_button = st.button(
            "🕷️ Analyze Website",
            use_container_width=True
        )

        if analyze_website_button:

            website_url = normalize_url(
                website_url
            )

            if not website_url:

                st.error(
                    "Please enter a website URL."
                )

            else:

                with st.spinner(
                    f"Crawling website and analyzing up to {max_pages} pages..."
                ):

                    result, error = api_request(
                        "/analyze-website",
                        {
                            "url": website_url,
                            "max_pages": max_pages
                        },
                        timeout=180
                    )

                if error:

                    st.error(
                        f"Website analysis failed: {error}"
                    )

                elif result:

                    # -------------------------------------
                    # Get pages
                    # -------------------------------------

                    pages = result.get(
                        "pages",
                        result.get(
                            "results",
                            []
                        )
                    )

                    if isinstance(
                        pages,
                        dict
                    ):

                        pages = list(
                            pages.values()
                        )

                    pages_df = pd.DataFrame(
                        pages
                    )

                    # -------------------------------------
                    # Summary
                    # -------------------------------------

                    summary = result.get(
                        "summary",
                        {}
                    )

                    analyzed_count = result.get(
                        "pages_analyzed",
                        summary.get(
                            "pages_analyzed",
                            len(pages_df)
                        )
                    )

                    high_count = result.get(
                        "high_priority",
                        summary.get(
                            "high",
                            0
                        )
                    )

                    medium_count = result.get(
                        "medium_priority",
                        summary.get(
                            "medium",
                            0
                        )
                    )

                    low_count = result.get(
                        "low_priority",
                        summary.get(
                            "low",
                            0
                        )
                    )

                    st.markdown(
                        """
                        <div class="success-card">
                            ✅ <b>Website analysis completed.</b>
                            Review the priority distribution and top
                            refresh opportunities below.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        "### 📊 Website Summary"
                    )

                    w1, w2, w3, w4 = st.columns(4)

                    metrics = [
                        (
                            w1,
                            "PAGES ANALYZED",
                            analyzed_count
                        ),
                        (
                            w2,
                            "HIGH PRIORITY",
                            high_count
                        ),
                        (
                            w3,
                            "MEDIUM PRIORITY",
                            medium_count
                        ),
                        (
                            w4,
                            "LOW PRIORITY",
                            low_count
                        )
                    ]

                    for col, label, value in metrics:

                        with col:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-label">
                                        {label}
                                    </div>
                                    <div class="metric-value">
                                        {format_number(value)}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # -------------------------------------
                    # Website chart
                    # -------------------------------------

                    if any([
                        high_count,
                        medium_count,
                        low_count
                    ]):

                        st.markdown(
                            "### 📈 Priority Distribution"
                        )

                        chart_data = pd.Series(
                            {
                                "High": high_count,
                                "Medium": medium_count,
                                "Low": low_count
                            }
                        )

                        st.bar_chart(
                            chart_data
                        )

                    # -------------------------------------
                    # Normalize common column names
                    # -------------------------------------

                    if not pages_df.empty:

                        st.markdown(
                            "### 🔥 Top Refresh Opportunities"
                        )

                        if "refresh_score" in pages_df.columns:

                            pages_df["refresh_score_numeric"] = (
                                pd.to_numeric(
                                    pages_df["refresh_score"],
                                    errors="coerce"
                                )
                                .fillna(0)
                            )

                            top_pages = (
                                pages_df
                                .sort_values(
                                    "refresh_score_numeric",
                                    ascending=False
                                )
                                .head(10)
                                .drop(
                                    columns=[
                                        "refresh_score_numeric"
                                    ],
                                    errors="ignore"
                                )
                            )

                            st.dataframe(
                                top_pages,
                                use_container_width=True,
                                hide_index=True
                            )

                        # -------------------------------------
                        # Filters
                        # -------------------------------------

                        st.markdown(
                            "### 🎛️ Website Results"
                        )

                        result_filter = st.selectbox(
                            "Filter by Priority",
                            [
                                "All",
                                "High",
                                "Medium",
                                "Low"
                            ],
                            key="website_priority_filter"
                        )

                        display_df = pages_df.copy()

                        if (
                            result_filter != "All"
                            and "priority"
                            in display_df.columns
                        ):

                            display_df = display_df[
                                display_df["priority"]
                                .astype(str)
                                .str.lower()
                                ==
                                result_filter.lower()
                            ]

                        display_df = display_df.drop(
                            columns=[
                                "refresh_score_numeric"
                            ],
                            errors="ignore"
                        )

                        st.dataframe(
                            display_df,
                            use_container_width=True,
                            hide_index=True
                        )

                        # -------------------------------------
                        # Website-level statistics
                        # -------------------------------------

                        st.markdown(
                            "### 📌 Website Content Statistics"
                        )

                        avg_word_count = 0
                        avg_quality = 0
                        missing_alt_total = 0

                        if "word_count" in pages_df.columns:

                            avg_word_count = pd.to_numeric(
                                pages_df["word_count"],
                                errors="coerce"
                            ).mean()

                        if "content_quality" in pages_df.columns:

                            avg_quality = pd.to_numeric(
                                pages_df["content_quality"],
                                errors="coerce"
                            ).mean()

                        elif "quality_score" in pages_df.columns:

                            avg_quality = pd.to_numeric(
                                pages_df["quality_score"],
                                errors="coerce"
                            ).mean()

                        if "images_without_alt" in pages_df.columns:

                            missing_alt_total = pd.to_numeric(
                                pages_df["images_without_alt"],
                                errors="coerce"
                            ).fillna(0).sum()

                        stats1, stats2, stats3 = st.columns(3)

                        with stats1:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-label">
                                        AVG WORD COUNT
                                    </div>
                                    <div class="metric-value">
                                        {format_number(
                                            avg_word_count
                                        )}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with stats2:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-label">
                                        AVG CONTENT QUALITY
                                    </div>
                                    <div class="metric-value">
                                        {format_score(
                                            avg_quality
                                        )}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        with stats3:

                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-label">
                                        MISSING ALT TEXT
                                    </div>
                                    <div class="metric-value">
                                        {format_number(
                                            missing_alt_total
                                        )}
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        # -------------------------------------
                        # CSV download
                        # -------------------------------------

                        st.markdown(
                            "### 📥 Export Results"
                        )

                        csv_data = display_df.to_csv(
                            index=False
                        ).encode(
                            "utf-8"
                        )

                        st.download_button(
                            label="⬇️ Download Analysis CSV",
                            data=csv_data,
                            file_name="contentpulse_website_analysis.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

                    else:

                        st.warning(
                            "No pages were returned by the API."
                        )

                    # -------------------------------------
                    # Raw response
                    # -------------------------------------

                    with st.expander(
                        "🧩 View Raw Website API Response"
                    ):

                        st.json(result)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        <b>ContentPulse AI</b> · AI-Assisted Website
        Content Analysis & Refresh Recommendation
        <br>
        Public website analysis is based on publicly accessible
        HTML and content signals.
        <br>
        Private analytics, Search Console, backlink and conversion
        data are not accessed without an authorized integration.
    </div>
    """,
    unsafe_allow_html=True
)