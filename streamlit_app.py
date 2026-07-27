import base64
import os
from datetime import date
from html import escape
from pathlib import Path
from textwrap import dedent

import requests
import streamlit as st

def configured_api_url() -> str:
    try:
        value = st.secrets["API_URL"]
    except Exception:
        value = os.getenv("API_URL", "http://127.0.0.1:8000")
    return str(value).rstrip("/")


def configured_demo_mode() -> bool:
    try:
        value = st.secrets["DEMO_MODE"]
    except Exception:
        value = os.getenv("DEMO_MODE", "false")
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


API_URL = configured_api_url()
DEMO_MODE = configured_demo_mode()
DEMO_TOKEN = "demo-streamlit-token"
AUTH_HERO_IMAGE = Path(__file__).parent / "assets" / "auth-career-hero.png"
AUTH_HERO_IMAGE_DATA = base64.b64encode(AUTH_HERO_IMAGE.read_bytes()).decode("ascii")

STATUSES = [
    "Saved",
    "Applied",
    "Screening",
    "Interview",
    "Technical Round",
    "Offer",
    "Rejected",
    "Accepted",
]

STATUS_COLORS = {
    "Saved": "#64748b",
    "Applied": "#5b7caa",
    "Screening": "#d85d9d",
    "Interview": "#ff9442",
    "Technical Round": "#38c8b7",
    "Offer": "#2d8cff",
    "Rejected": "#ef4444",
    "Accepted": "#22a35a",
}

STATUS_LABELS = {
    "Saved": "Saved",
    "Applied": "Applied",
    "Screening": "Screening",
    "Interview": "Interview",
    "Technical Round": "Tests",
    "Offer": "Hiring",
    "Rejected": "Archived",
    "Accepted": "Accepted",
}

NAV_ITEMS = ["Dashboard", "Jobs", "Candidates", "Messages", "Company", "Settings"]

SAMPLE_CANDIDATES = [
    {
        "name": "Ayesha Khan",
        "role": "Junior Python Developer",
        "location": "Lahore, PK",
        "stage": "Screening",
        "experience": "1 year",
    },
    {
        "name": "Bilal Ahmed",
        "role": "FastAPI Backend Intern",
        "location": "Remote",
        "stage": "Interview",
        "experience": "6 months",
    },
    {
        "name": "Hira Malik",
        "role": "SQLAlchemy Trainee",
        "location": "Karachi, PK",
        "stage": "Applied",
        "experience": "Entry level",
    },
    {
        "name": "Omar Farooq",
        "role": "Full Stack Developer",
        "location": "Islamabad, PK",
        "stage": "Tests",
        "experience": "2 years",
    },
]

DEMO_APPLICATIONS = [
    {
        "id": 1,
        "company_name": "Nolyth",
        "job_title": "Lead AI Engineer",
        "status": "Applied",
        "location": "Lahore",
        "salary_range": "PKR 120k - 180k",
        "applied_date": date.today().isoformat(),
        "notes": "Prepare FastAPI and SQLAlchemy explanation.",
        "created_at": date.today().isoformat(),
    },
    {
        "id": 2,
        "company_name": "BluePeak",
        "job_title": "Entry Level Python Engineer",
        "status": "Screening",
        "location": "Remote",
        "salary_range": "Not shared",
        "applied_date": "2026-07-06",
        "notes": "First interview scheduled. Prepare JWT explanation.",
        "created_at": "2026-07-06",
    },
    {
        "id": 3,
        "company_name": "OrbitWorks",
        "job_title": "Junior Full Stack Developer",
        "status": "Accepted",
        "location": "Remote",
        "salary_range": "PKR 150k",
        "applied_date": "2026-07-05",
        "notes": "Accepted offer for demo data.",
        "created_at": "2026-07-05",
    },
]

st.set_page_config(page_title="Career Pipeline", page_icon=":briefcase:", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --blue: #2563eb;
        --blue-soft: #eff6ff;
        --ink: #111827;
        --muted: #7c8798;
        --line: #e5eaf2;
        --panel: #ffffff;
        --page: #f3f6fb;
        --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    }

    .stApp {
        background: linear-gradient(135deg, #f8fbff 0%, #eef4fb 48%, #e5edf7 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1560px;
        padding: 1.35rem 1.45rem 2rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
        height: 0;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        display: none;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }

    .side-rail {
        background: #ffffff;
        border: 1px solid rgba(226, 232, 240, 0.95);
        border-radius: 18px;
        box-shadow: 0 20px 55px rgba(15, 23, 42, 0.07);
        min-height: auto;
        padding: 1.15rem 1.05rem 0.85rem;
    }

    .brand {
        align-items: center;
        color: #0f172a;
        display: flex;
        font-size: 1.75rem;
        font-weight: 900;
        justify-content: space-between;
        letter-spacing: 0;
        padding: 0 0 1.05rem;
    }

    .brand span:first-child::first-letter {
        color: var(--blue);
    }

    .collapse-pill {
        align-items: center;
        border: 1px solid #e3ebf5;
        border-radius: 999px;
        color: #8b94a5;
        display: inline-flex;
        font-size: 0.82rem;
        height: 1.8rem;
        justify-content: center;
        width: 1.8rem;
    }

    .sidebar-search {
        align-items: center;
        background: #f8fafc;
        border: 1px solid #e1e8f2;
        border-radius: 12px;
        color: #8b94a5;
        display: flex;
        font-size: 0.9rem;
        justify-content: space-between;
        margin: 0.35rem 0 1.05rem;
        min-height: 2.55rem;
        padding: 0 0.85rem;
    }

    .workspace {
        align-items: center;
        color: #303948;
        display: flex;
        font-size: 0.95rem;
        font-weight: 700;
        gap: 0.6rem;
        padding: 0 0 0.95rem;
    }

    .workspace-icon {
        align-items: center;
        background: linear-gradient(145deg, #2563eb, #3b82f6);
        border-radius: 12px;
        color: #ffffff;
        display: inline-flex;
        height: 2.1rem;
        justify-content: center;
        width: 2.1rem;
    }

    .control-spacer {
        height: 1.35rem;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button {
        border: 0;
        border-radius: 12px;
        box-shadow: none;
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 750;
        justify-content: flex-start;
        margin: 0.2rem 0;
        min-height: 2.65rem;
        padding: 0 0.95rem;
        width: 100%;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button:hover {
        background: #eff6ff;
        color: var(--blue);
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button[kind="primary"] {
        background: #eff6ff;
        border-left: 4px solid var(--blue);
        color: var(--blue);
    }

    .sidebar-footer-spacer {
        height: 1.85rem;
    }

    .job-header,
    .tabs-line,
    .toolbar-line,
    .dashboard-stat-strip,
    .pipeline-board {
        border-left: 0;
    }

    .dashboard-archive-spacer {
        height: 1.35rem;
    }

    .top-icon-row {
        align-items: center;
        display: flex;
        gap: 0.7rem;
        height: 3rem;
        justify-content: flex-end;
    }

    .profile-avatar {
        align-items: center;
        background: linear-gradient(145deg, #e0f2fe, #bfdbfe);
        border: 2px solid #ffffff;
        border-radius: 12px;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.13);
        color: #1d4ed8;
        display: inline-flex;
        font-weight: 900;
        height: 2.75rem;
        justify-content: center;
        width: 2.75rem;
    }

    .user-pill {
        color: #303948;
        display: block;
        line-height: 1.15;
        white-space: nowrap;
    }

    .user-name {
        color: #0f172a;
        font-size: 0.98rem;
        font-weight: 850;
    }

    .user-email {
        color: #8b94a5;
        font-size: 0.78rem;
        margin-top: 0.18rem;
    }

    .job-header {
        background: #ffffff;
        border: 1px solid var(--line);
        border-bottom: 0;
        border-radius: 16px 16px 0 0;
        margin-top: 0.4rem;
        padding: 1.05rem 1.15rem 0.45rem;
    }

    .job-title {
        color: #252d3a;
        font-size: 1.18rem;
        font-weight: 850;
        line-height: 1.2;
    }

    .job-meta {
        color: #9aa3af;
        font-size: 0.82rem;
        margin-top: 0.28rem;
    }

    .tabs-line {
        align-items: end;
        background: #ffffff;
        border-bottom: 1px solid var(--line);
        color: #9aa3af;
        display: flex;
        gap: 2.25rem;
        padding: 0.85rem 1.15rem 0;
        white-space: nowrap;
    }

    .tab {
        font-size: 0.9rem;
        padding-bottom: 0.9rem;
    }

    .tab.active {
        border-bottom: 2px solid var(--blue);
        color: #4f5866;
        font-weight: 800;
    }

    .tiny-badge {
        background: #eef1f5;
        border-radius: 999px;
        color: #9aa3af;
        font-size: 0.72rem;
        margin-left: 0.35rem;
        padding: 0.05rem 0.38rem;
    }

    .toolbar-line {
        align-items: center;
        background: #ffffff;
        display: flex;
        justify-content: space-between;
        padding: 0.9rem 1.15rem 0.75rem;
    }

    .segmented {
        border: 1px solid #d8e1ee;
        border-radius: 10px;
        display: inline-flex;
        overflow: hidden;
    }

    .segmented span {
        color: #303948;
        font-size: 0.86rem;
        font-weight: 750;
        padding: 0.64rem 1.45rem;
    }

    .segmented span:first-child {
        background: #eff6ff;
        border-bottom: 2px solid var(--blue);
        color: var(--blue);
    }

    .select-mode {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 10px;
        color: #303948;
        font-size: 0.86rem;
        font-weight: 750;
        padding: 0.62rem 0.85rem;
    }

    .pipeline-board {
        background: #f8fafc;
        border: 1px solid var(--line);
        border-radius: 0 0 16px 16px;
        display: grid;
        gap: 0.8rem;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        overflow: visible;
        padding: 1rem;
    }

    .pipeline-column {
        background: #f8fafc;
        border-radius: 12px;
        min-width: 0;
    }

    .column-head {
        align-items: center;
        color: #515d6d;
        display: flex;
        font-size: 0.88rem;
        font-weight: 800;
        gap: 0.5rem;
        justify-content: space-between;
        margin-bottom: 0.7rem;
        min-height: 1.8rem;
    }

    .column-title {
        align-items: center;
        display: inline-flex;
        gap: 0.48rem;
    }

    .status-square {
        border-radius: 3px;
        display: inline-block;
        height: 0.68rem;
        width: 0.68rem;
    }

    .count-pill {
        background: #eef1f5;
        border-radius: 999px;
        color: #a1a9b4;
        font-size: 0.75rem;
        padding: 0.05rem 0.45rem;
    }

    .dots {
        color: #aab1bb;
        letter-spacing: 0.1rem;
    }

    .candidate-card {
        background: #ffffff;
        border: 1px solid #e1e8f2;
        border-radius: 12px;
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.045);
        margin-bottom: 0.68rem;
        padding: 0.82rem 0.78rem;
        transition: border-color 120ms ease, box-shadow 120ms ease, transform 120ms ease;
    }

    .candidate-card-link {
        display: block;
        text-decoration: none !important;
    }

    .candidate-card:hover {
        border-color: #bfdbfe;
        box-shadow: 0 14px 28px rgba(37, 99, 235, 0.08);
        transform: translateY(-1px);
    }

    .candidate-card-link:focus .candidate-card {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
    }

    .card-main {
        align-items: center;
        display: flex;
        gap: 0.65rem;
        min-width: 0;
    }

    .card-main > div {
        min-width: 0;
    }

    .card-avatar {
        align-items: center;
        background: #dbeafe;
        border-radius: 14px;
        color: #1d4ed8;
        display: inline-flex;
        flex: 0 0 2.05rem;
        font-size: 0.78rem;
        font-weight: 900;
        height: 2.05rem;
        justify-content: center;
        width: 2.05rem;
    }

    .candidate-name {
        color: #263142;
        font-size: 0.88rem;
        font-weight: 850;
        line-height: 1.12;
        overflow-wrap: anywhere;
    }

    .profile-link {
        color: var(--blue);
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 0.18rem;
        overflow: hidden;
        overflow-wrap: anywhere;
        white-space: normal;
    }

    .card-age {
        color: #a0a8b3;
        font-size: 0.72rem;
        margin-top: 0.75rem;
        overflow: hidden;
        overflow-wrap: anywhere;
        white-space: normal;
    }

    .auth-shell {
        align-items: stretch;
        display: grid;
        grid-template-columns: 0.78fr 1.22fr;
        margin: 1.2rem auto 0;
        max-width: 1080px;
        min-height: 540px;
    }

    .auth-visual {
        background:
            linear-gradient(180deg, rgba(7, 24, 55, 0.04), rgba(7, 24, 55, 0.32));
        background-position: center;
        background-size: cover;
        border: 0;
        border-radius: 14px 0 0 14px;
        box-shadow: none;
        min-height: min(760px, calc(100vh - 4.5rem));
        overflow: hidden;
        padding: 1.7rem;
        position: relative;
    }

    .auth-visual-brand {
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 900;
        position: relative;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.28);
    }

    .auth-chip {
        align-items: center;
        backdrop-filter: blur(12px);
        background: rgba(9, 44, 96, 0.56);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 999px;
        color: #ffffff;
        display: flex;
        font-size: 0.78rem;
        font-weight: 800;
        gap: 0.55rem;
        min-width: 11rem;
        padding: 0.85rem 1rem;
        position: absolute;
    }

    .auth-chip.one {
        right: 1.6rem;
        top: 10.5rem;
    }

    .auth-chip.two {
        left: 1.9rem;
        top: 15.7rem;
    }

    .auth-chip.three {
        right: 2.2rem;
        top: 21.2rem;
    }

    .auth-chip-dot {
        background: #ffffff;
        border-radius: 50%;
        color: var(--blue);
        display: inline-flex;
        flex: 0 0 1.8rem;
        font-size: 0.72rem;
        height: 1.8rem;
        justify-content: center;
        place-items: center;
        width: 1.8rem;
    }

    .auth-visual-copy {
        bottom: 4.3rem;
        color: #ffffff;
        font-size: 1.55rem;
        font-weight: 850;
        left: 1.6rem;
        line-height: 1.12;
        max-width: 360px;
        padding: 0;
        position: absolute;
        text-align: left;
        text-shadow: 0 3px 16px rgba(0, 0, 0, 0.38);
    }

    .auth-visual-person {
        bottom: 2rem;
        color: rgba(255, 255, 255, 0.88);
        font-size: 0.78rem;
        left: 1.7rem;
        line-height: 1.45;
        position: absolute;
        text-shadow: 0 2px 12px rgba(0, 0, 0, 0.35);
    }

    .auth-form-shell {
        background: #ffffff;
        border: 2px solid #111827;
        border-left: 0;
        min-height: 540px;
        padding: 4.1rem 5.2rem;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) {
        background: #ffffff;
        border: 1px solid #dce6f2;
        border-radius: 14px;
        box-shadow: 0 24px 52px rgba(33, 46, 63, 0.13);
        overflow: hidden;
        max-width: 1480px;
        margin: 0 auto;
    }

    .dashboard-stat-strip {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 16px;
        display: grid;
        gap: 0.82rem;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        margin: 0.85rem 0;
        padding: 0.95rem;
    }

    .dashboard-stat {
        background: #f8fbff;
        border: 1px solid #e0e8f2;
        border-radius: 12px;
        padding: 0.8rem 0.95rem;
    }

    .dashboard-stat-label {
        color: #748195;
        font-size: 0.72rem;
        font-weight: 850;
        text-transform: uppercase;
    }

    .dashboard-stat-value {
        color: #1d2634;
        font-size: 1.45rem;
        font-weight: 900;
        margin-top: 0.12rem;
    }

    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 16px;
        box-shadow: 0 14px 35px rgba(15, 23, 42, 0.055);
        min-height: auto;
        padding: 1.05rem 1.1rem;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 0;
        border-radius: 0 14px 14px 0;
        box-shadow: none;
        min-height: min(760px, calc(100vh - 4.5rem));
        padding: clamp(3.2rem, 8vh, 5.6rem) clamp(3rem, 5.5vw, 5.4rem) 2.6rem;
    }

    div[data-testid="stForm"] h3 {
        color: #1d2634;
        font-size: 1.2rem;
        font-weight: 850;
        margin-bottom: 0.85rem;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] h3 {
        color: #1d2634;
        font-size: 1.65rem;
        font-weight: 850;
        margin-bottom: 0.25rem;
        text-align: center;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] .stTextInput,
    div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] .stButton {
        width: 100%;
    }

    .stTextInput label,
    .stTextArea label,
    .stDateInput label,
    .stSelectbox label,
    .stMultiSelect label {
        color: #5d6878;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 0.22rem;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #ffffff;
        border: 0;
        border-radius: 0;
        color: #1d2634;
        min-height: 2.25rem;
    }

    .stTextInput input[type="password"] {
        padding-right: 2.8rem;
    }

    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {
        background-color: #ffffff;
        border: 1px solid #d7dfeb;
        border-radius: 10px;
        color: #1d2634;
        min-height: 2.55rem;
        overflow: hidden;
        width: 100%;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        color: #1d2634;
        caret-color: var(--blue);
    }

    .stTextInput div[data-baseweb="input"] > div:empty,
    .stTextInput div[data-baseweb="input"] > div:not(:has(input)):not(:has(button)):not(:has(svg)) {
        display: none !important;
        flex: 0 0 0 !important;
        min-width: 0 !important;
        width: 0 !important;
    }

    .stTextInput div[data-baseweb="input"] svg {
        fill: #7a8798 !important;
        height: 1rem !important;
        width: 1rem !important;
    }

    .stTextInput div[data-baseweb="input"] button:hover svg,
    .stTextInput div[data-baseweb="input"] [role="button"]:hover svg {
        fill: var(--blue) !important;
    }

    div[data-baseweb="input"] button[aria-label*="password"],
    div[data-baseweb="input"] button[title*="password"],
    div[data-baseweb="input"] button[aria-label*="Password"],
    div[data-baseweb="input"] button[title*="Password"] {
        align-items: center !important;
        background: transparent !important;
        border: 0 !important;
        border-left: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        color: #68758a !important;
        display: inline-flex !important;
        height: 2.7rem !important;
        justify-content: center !important;
        margin: 0 !important;
        min-height: 2.7rem !important;
        width: 2.8rem !important;
    }

    div[data-baseweb="input"] button[aria-label*="password"] svg,
    div[data-baseweb="input"] button[title*="password"] svg,
    div[data-baseweb="input"] button[aria-label*="Password"] svg,
    div[data-baseweb="input"] button[title*="Password"] svg {
        fill: currentColor !important;
        height: 1.05rem !important;
        width: 1.05rem !important;
    }

    div[data-baseweb="input"] button[aria-label*="password"]:hover,
    div[data-baseweb="input"] button[title*="password"]:hover,
    div[data-baseweb="input"] button[aria-label*="Password"]:hover,
    div[data-baseweb="input"] button[title*="Password"]:hover {
        background: #eef7ff !important;
        color: var(--blue) !important;
    }

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: var(--blue);
        box-shadow: 0 0 0 3px rgba(35, 135, 237, 0.14);
    }

    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 750;
        min-height: 2.55rem;
    }

    .stFormSubmitButton > button {
        background: var(--blue);
        border: 1px solid var(--blue);
        color: #ffffff;
    }

    .stFormSubmitButton > button:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
        color: #ffffff;
    }

    div[data-testid="stButton"] button {
        border: 1px solid var(--blue);
        border-radius: 10px;
        box-shadow: none;
        font-size: 0.95rem;
        min-height: 2.45rem;
        padding: 0 1.15rem;
    }

    div[data-testid="stButton"] button[kind="secondary"] {
        background: #ffffff;
        color: var(--blue);
        min-height: 2.25rem;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        background: var(--blue);
        border-color: var(--blue);
        color: #ffffff;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #1676d9;
        color: var(--blue);
    }

    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background: #eff6ff;
        color: var(--blue);
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #1d4ed8;
        color: #ffffff;
    }

    .stTextInput div[data-baseweb="input"] button,
    .stTextInput div[data-baseweb="input"] button:hover,
    .stTextInput div[data-baseweb="input"] button:focus,
    .stTextInput div[data-baseweb="input"] button:active,
    .stTextInput div[data-baseweb="input"] [role="button"],
    .stTextInput div[data-baseweb="input"] [role="button"]:hover,
    .stTextInput div[data-baseweb="input"] [role="button"]:focus,
    .stTextInput div[data-baseweb="input"] [role="button"]:active {
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        color: #7a8798 !important;
        outline: 0 !important;
    }

    .stTextInput div[data-baseweb="input"] button svg,
    .stTextInput div[data-baseweb="input"] [role="button"] svg {
        fill: currentColor !important;
    }

    .stTextInput div[data-baseweb="input"] button:hover,
    .stTextInput div[data-baseweb="input"] [role="button"]:hover {
        color: var(--blue) !important;
    }

    .stTextInput div[data-baseweb="input"] > div:last-child,
    .stTextInput div[data-baseweb="input"] > div:last-child *,
    .stTextInput div[data-baseweb="input"] button,
    .stTextInput div[data-baseweb="input"] button * {
        background: transparent !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    .auth-note {
        color: #7a8798;
        font-size: 0.82rem;
        margin: 1.05rem 0 0.45rem;
        text-align: center;
    }

    .auth-subtitle {
        color: #7a8798;
        font-size: 0.86rem;
        line-height: 1.45;
        margin: 0 0 1.45rem;
        text-align: center;
    }

    .auth-link {
        color: #7357f6;
        font-size: 0.82rem;
        font-weight: 850;
        margin: 0.35rem 0 0.8rem;
    }

    .auth-error-banner {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 14px;
        color: #b91c1c;
        font-size: 0.9rem;
        font-weight: 750;
        margin: 0.85rem 0 0.25rem;
        padding: 0.9rem 1rem;
    }

    .page-summary {
        align-items: center;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 22px;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.045);
        display: flex;
        justify-content: space-between;
        margin-top: 0.65rem;
        padding: 1.25rem 1.35rem;
    }

    .page-summary-title {
        color: #0f172a;
        font-size: 1.45rem;
        font-weight: 900;
        line-height: 1.15;
    }

    .page-summary-copy {
        color: #667085;
        font-size: 0.9rem;
        margin-top: 0.32rem;
    }

    .page-summary-badge {
        background: #eef2ff;
        border: 1px solid #e0e7ff;
        border-radius: 999px;
        color: #4f46e5;
        font-size: 0.82rem;
        font-weight: 850;
        padding: 0.45rem 0.75rem;
        white-space: nowrap;
    }

    .placeholder-card {
        align-items: center;
        background: #ffffff;
        border: 1px dashed #cbd5e1;
        border-radius: 22px;
        box-shadow: 0 14px 34px rgba(15, 23, 42, 0.04);
        display: flex;
        gap: 0.9rem;
        margin-top: 1rem;
        padding: 1.25rem;
    }

    .placeholder-icon {
        align-items: center;
        background: #eef2ff;
        border-radius: 16px;
        color: #4f46e5;
        display: inline-flex;
        flex: 0 0 2.8rem;
        font-size: 1.15rem;
        height: 2.8rem;
        justify-content: center;
        width: 2.8rem;
    }

    .placeholder-title {
        color: #172033;
        font-size: 1rem;
        font-weight: 850;
    }

    .placeholder-copy {
        color: #667085;
        font-size: 0.86rem;
        margin-top: 0.2rem;
    }

    .delete-warning {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 16px;
        color: #9a3412;
        font-size: 0.86rem;
        margin: 0.8rem 0;
        padding: 0.8rem 0.9rem;
    }

    .delete-confirm-row {
        align-items: center;
        display: flex;
        gap: 0.65rem;
        margin: 0.35rem 0 0.85rem;
    }

    .delete-confirm-text {
        color: #344054;
        font-size: 0.9rem;
        font-weight: 800;
    }

    .delete-box-spacer {
        height: 0.1rem;
    }

    .stCheckbox label {
        align-items: center !important;
        color: #475467 !important;
        display: flex !important;
        gap: 0.55rem !important;
        min-height: 1.8rem !important;
    }

    .stCheckbox label p {
        color: #475467 !important;
        font-size: 0.88rem !important;
        font-weight: 650 !important;
        margin: 0 !important;
    }

    .stCheckbox span[data-baseweb="checkbox"] {
        background: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        height: 1.05rem !important;
        width: 1.05rem !important;
    }

    .stCheckbox div[data-baseweb="checkbox"],
    .stCheckbox [role="checkbox"],
    .stCheckbox span[data-baseweb="checkbox"] > div,
    .stCheckbox div[data-baseweb="checkbox"] > div {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 6px !important;
        box-shadow: none !important;
        color: #ffffff !important;
        height: 1.05rem !important;
        min-height: 1.05rem !important;
        min-width: 1.05rem !important;
        width: 1.05rem !important;
    }

    .stCheckbox span[data-baseweb="checkbox"][aria-checked="true"] {
        background: #ffffff !important;
        border-color: #2563eb !important;
    }

    .stCheckbox div[data-baseweb="checkbox"][aria-checked="true"],
    .stCheckbox [role="checkbox"][aria-checked="true"],
    .stCheckbox span[data-baseweb="checkbox"][aria-checked="true"] > div,
    .stCheckbox div[data-baseweb="checkbox"][aria-checked="true"] > div {
        background: #2563eb !important;
        background-color: #2563eb !important;
        border-color: #2563eb !important;
    }

    .stCheckbox span[data-baseweb="checkbox"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }

    .stCheckbox [role="checkbox"][aria-checked="false"],
    .stCheckbox div[data-baseweb="checkbox"][aria-checked="false"],
    .stCheckbox span[data-baseweb="checkbox"][aria-checked="false"],
    .stCheckbox [role="checkbox"][aria-checked="false"] > div,
    .stCheckbox div[data-baseweb="checkbox"][aria-checked="false"] > div,
    .stCheckbox span[data-baseweb="checkbox"][aria-checked="false"] > div {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border-color: #cbd5e1 !important;
        color: #ffffff !important;
    }

    .stToggle label {
        color: #344054 !important;
        font-size: 0.88rem !important;
        font-weight: 750 !important;
    }

    .stToggle [role="switch"] {
        background: #ffffff !important;
        border: 1.5px solid #111827 !important;
        box-shadow: none !important;
    }

    .stToggle [role="switch"][aria-checked="true"] {
        background: #2563eb !important;
        border-color: #1d4ed8 !important;
    }

    .stToggle [role="switch"] > div {
        background: #111827 !important;
        box-shadow: none !important;
    }

    .stToggle [role="switch"][aria-checked="true"] > div {
        background: #ffffff !important;
    }

    .stRadio [role="radiogroup"] {
        background: #ffffff;
        border: 1px solid #d0d5dd;
        border-radius: 14px;
        display: inline-flex;
        gap: 0.35rem;
        padding: 0.35rem;
    }

    .stRadio label {
        align-items: center !important;
        border-radius: 10px;
        color: #344054 !important;
        font-size: 0.86rem !important;
        font-weight: 750 !important;
        padding: 0.35rem 0.55rem !important;
    }

    .stRadio label:hover {
        background: #f8fafc;
    }

    .stRadio label p {
        color: inherit !important;
        font-size: 0.86rem !important;
        font-weight: 750 !important;
    }

    div[data-testid="stButton"] button:has(span:only-child) {
        overflow: hidden;
    }

    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stHorizontalBlock"]) {
        row-gap: 0.75rem;
    }

    /* Final SaaS UI revamp overrides. Kept at the end so Streamlit wrappers cannot wash it out. */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 28rem),
            linear-gradient(135deg, #f8fafc 0%, #eef4fb 45%, #e7eff8 100%) !important;
    }

    .block-container {
        max-width: 1680px !important;
        padding: 1.2rem 1.5rem 2.25rem !important;
    }

    .side-rail {
        background: rgba(255, 255, 255, 0.96) !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 22px !important;
        box-shadow: 0 24px 70px rgba(15, 23, 42, 0.08) !important;
        padding: 1.25rem 1.05rem 1rem !important;
    }

    .brand {
        border-bottom: 1px solid #eef2f7;
        color: #0f172a !important;
        margin-bottom: 0.9rem;
        padding-bottom: 1rem !important;
    }

    .brand span:first-child {
        color: #2563eb;
    }

    .collapse-pill {
        background: #f8fafc;
    }

    .sidebar-search {
        background: #f8fafc !important;
        border-color: #e2e8f0 !important;
        border-radius: 14px !important;
    }

    .workspace {
        background: #f8fafc;
        border: 1px solid #edf2f7;
        border-radius: 16px;
        margin-bottom: 0.7rem;
        padding: 0.7rem !important;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button {
        border: 0 !important;
        border-radius: 14px !important;
        color: #64748b !important;
        font-size: 0.94rem !important;
        font-weight: 800 !important;
        min-height: 2.9rem !important;
        padding-left: 1rem !important;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button[kind="primary"] {
        background: #2563eb !important;
        border-left: 0 !important;
        color: #ffffff !important;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.18) !important;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button:hover {
        background: #eff6ff !important;
        color: #2563eb !important;
    }

    .top-icon-row {
        align-items: center !important;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 999px;
        box-shadow: 0 14px 34px rgba(15, 23, 42, 0.05);
        display: inline-flex !important;
        gap: 0.65rem !important;
        height: 3.05rem !important;
        justify-content: flex-start !important;
        max-width: 100%;
        min-width: 0;
        padding: 0.32rem 0.85rem 0.32rem 0.36rem;
    }

    .profile-avatar {
        box-shadow: none !important;
        flex: 0 0 2.25rem !important;
        border-radius: 50% !important;
        height: 2.25rem !important;
        width: 2.25rem !important;
    }

    .user-pill {
        display: flex !important;
        flex: 1 1 auto;
        gap: 0.4rem;
        line-height: 1 !important;
        min-width: 0;
        white-space: nowrap;
    }

    .user-name {
        display: inline-flex;
        align-items: center;
        color: #0f172a !important;
        font-size: 0.92rem !important;
        font-weight: 900 !important;
        gap: 0.28rem;
        min-width: 0;
    }

    .user-arrow {
        color: #0f172a;
        font-size: 0.78rem;
        line-height: 1;
    }

    .user-email {
        align-self: center;
        color: #8b94a5 !important;
        font-size: 0.78rem !important;
        line-height: 1 !important;
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .job-header,
    .tabs-line,
    .toolbar-line,
    .dashboard-stat-strip,
    .pipeline-board,
    div[data-testid="stForm"],
    .candidate-card {
        box-sizing: border-box;
    }

    .job-header {
        display: none !important;
    }

    .job-title {
        color: #0f172a !important;
        font-size: 1.35rem !important;
        font-weight: 900 !important;
    }

    .tabs-line,
    .toolbar-line {
        display: none !important;
    }

    .dashboard-stat-strip {
        border-radius: 20px !important;
        box-shadow: 0 16px 42px rgba(15, 23, 42, 0.045);
        margin: 1rem 0 !important;
    }

    .dashboard-stat {
        background: linear-gradient(180deg, #ffffff, #f8fbff) !important;
        border-radius: 16px !important;
        min-height: 5.1rem;
    }

    .pipeline-board {
        border: 1px solid #e2e8f0 !important;
        border-radius: 22px !important;
        box-shadow: 0 18px 48px rgba(15, 23, 42, 0.055);
        gap: 1rem !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        padding: 1rem !important;
    }

    .pipeline-column {
        background: #f8fafc !important;
        border: 1px solid #edf2f7;
        border-radius: 18px !important;
        padding: 0.8rem;
    }

    .candidate-card {
        border-radius: 16px !important;
        box-shadow: 0 12px 26px rgba(15, 23, 42, 0.06) !important;
    }

    .candidate-name,
    .profile-link,
    .card-age {
        overflow-wrap: anywhere !important;
        white-space: normal !important;
    }

    div[data-testid="stForm"] {
        border-radius: 22px !important;
        box-shadow: 0 18px 48px rgba(15, 23, 42, 0.07) !important;
        padding: 1.25rem !important;
    }

    div[data-testid="stForm"] h3 {
        font-size: 1.35rem !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {
        border-radius: 14px !important;
        min-height: 2.8rem !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 14px !important;
        min-height: 2.75rem !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) {
        border-radius: 24px !important;
        box-shadow: 0 30px 80px rgba(15, 23, 42, 0.12) !important;
        max-width: 1500px !important;
    }

    .auth-visual {
        border-radius: 24px 0 0 24px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 0 24px 24px 0 !important;
    }

    @media (max-width: 1200px) {
        .pipeline-board {
            grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        }
    }

    @media (max-width: 900px) {
        .block-container {
            padding: 1rem;
        }

        .side-rail {
            min-height: auto;
        }

        .side-rail {
            border-bottom: 1px solid var(--line);
            border-right: 0;
        }

        .tabs-line {
            overflow-x: auto;
        }

        .dashboard-stat-strip {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .pipeline-column {
            min-width: 0;
        }

        .pipeline-board {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .auth-visual {
            border-radius: 12px 12px 0 0;
            border-right: 1px solid #cbd9eb;
            min-height: 320px;
        }

        div[data-testid="stForm"],
        div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] {
            border-left: 1px solid #dce6f2;
            border-radius: 0 0 12px 12px;
            min-height: auto;
            padding: 2rem 1.25rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "token" not in st.session_state:
    st.session_state.token = None
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"
if "auth_error" not in st.session_state:
    st.session_state.auth_error = None
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Dashboard"
if "demo_username" not in st.session_state:
    st.session_state.demo_username = "usman"
if "demo_applications" not in st.session_state:
    st.session_state.demo_applications = [item.copy() for item in DEMO_APPLICATIONS]


def selected_job_id() -> int | None:
    selected = st.query_params.get("selected_job")
    if isinstance(selected, list):
        selected = selected[0] if selected else None
    try:
        return int(selected) if selected else None
    except (TypeError, ValueError):
        return None


def is_demo_session() -> bool:
    return DEMO_MODE or st.session_state.token == DEMO_TOKEN


def auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {st.session_state.token}"}


def api_error_message(response: requests.Response, fallback: str) -> str:
    try:
        return response.json().get("detail", fallback)
    except ValueError:
        return fallback


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def format_date(value: str | None) -> str:
    parsed = parse_date(value)
    if parsed is None:
        return "No date"
    return parsed.strftime("%d %b %Y")


def initials(*parts: str | None) -> str:
    letters = [part.strip()[0] for part in parts if part and part.strip()]
    return "".join(letters[:2]).upper() or "CP"


def relative_label(application: dict) -> str:
    raw_date = application.get("applied_date") or application.get("created_at", "")[:10]
    parsed = parse_date(raw_date)
    if parsed is None:
        return "Recently"
    days = (date.today() - parsed).days
    if days <= 0:
        return "Today"
    if days == 1:
        return "1 day ago"
    if days < 14:
        return f"{days} days ago"
    weeks = max(days // 7, 2)
    return f"{weeks} weeks ago"


def fetch_applications() -> list[dict]:
    if is_demo_session():
        return st.session_state.demo_applications

    try:
        response = requests.get(
            f"{API_URL}/applications",
            headers=auth_headers(),
            timeout=10,
        )
    except requests.RequestException:
        st.error("Could not connect to the backend API.")
        return []
    if response.ok:
        return response.json()
    st.error(api_error_message(response, "Could not load applications"))
    return []


def fetch_current_user() -> dict:
    if is_demo_session():
        return {"username": st.session_state.demo_username}

    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers=auth_headers(),
            timeout=10,
        )
    except requests.RequestException:
        st.error("Could not connect to the backend API.")
        return {"username": "User"}
    if response.ok:
        return response.json()
    st.error(api_error_message(response, "Could not load profile"))
    return {"username": "User"}


def render_nav() -> None:
    st.markdown(
        """
        <div class="side-rail">
            <div class="brand"><span>join</span><span class="collapse-pill">&lsaquo;</span></div>
            <div class="sidebar-search"><span>Search</span><span>&#128269;</span></div>
            <div class="workspace"><span class="workspace-icon">CP</span> Career</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for item, icon in zip(NAV_ITEMS, ["⌂", "▦", "◎", "✉", "□", "⚙"]):
        active = st.session_state.active_nav == item
        label = f"{icon}   {item}"
        if st.button(
            label,
            key=f"nav_{item.lower()}",
            type="primary" if active else "secondary",
            use_container_width=True,
        ):
            st.session_state.active_nav = item
            st.rerun()

    st.markdown("<div class='sidebar-footer-spacer'></div>", unsafe_allow_html=True)
    if st.button("↪   Logout", key="sidebar_logout", use_container_width=True):
        st.session_state.token = None
        st.rerun()


def render_dashboard_filters(current_user: dict) -> tuple[str, list[str], bool]:
    username = escape(current_user.get("username", "User"))
    avatar = initials(username)
    email = f"{username.lower()}@career.local"
    control_cols = st.columns([1.45, 0.82, 0.24, 0.5], gap="small")
    with control_cols[0]:
        search_text = st.text_input(
            "Search",
            placeholder="Search anything",
            key="dashboard_search",
        )
    with control_cols[1]:
        selected_statuses = st.multiselect(
            "Filter by status",
            STATUSES,
            default=[],
            key="dashboard_status_filter",
        )
    with control_cols[2]:
        st.markdown("<div class='dashboard-archive-spacer'></div>", unsafe_allow_html=True)
        show_closed = st.checkbox(
            "Archived",
            value=True,
            key="dashboard_show_archived",
            label_visibility="collapsed",
        )
    with control_cols[3]:
        st.markdown("<div class='control-spacer'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="top-icon-row">
                <span class="profile-avatar">{avatar}</span>
                <span class="user-pill">
                    <span class="user-name">{username}<span class="user-arrow">⌄</span></span>
                    <span class="user-email">{email}</span>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    return search_text, selected_statuses, show_closed


def render_header(total_count: int, title: str = "Career Pipeline", subtitle: str | None = None) -> None:
    safe_title = escape(title)
    safe_subtitle = escape(
        subtitle or "Track applications, interviews, and offers in one focused workspace."
    )
    st.markdown(
        f"""
        <div class="page-summary">
            <div>
                <div class="page-summary-title">{safe_title}</div>
                <div class="page-summary-copy">{safe_subtitle}</div>
            </div>
            <div class="page-summary-badge">{total_count} jobs</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_candidate_card(application: dict) -> str:
    company = escape(application["company_name"])
    title = escape(application["job_title"])
    location = escape(application.get("location") or "View profile")
    card_initials = initials(application["job_title"], application["company_name"])
    application_id = application["id"]
    return dedent(f"""
    <a class="candidate-card-link" href="?selected_job={application_id}">
    <div class="candidate-card">
        <div class="card-main">
            <span class="card-avatar">{card_initials}</span>
            <div>
                <div class="candidate-name">{company}</div>
                <div class="profile-link">{title}</div>
            </div>
        </div>
        <div class="card-age">{relative_label(application)} - {location}</div>
    </div>
    </a>
    """).strip()


def render_pipeline(applications: list[dict]) -> None:
    columns_html = []
    for status in STATUSES:
        items = [item for item in applications if item["status"] == status]
        color = STATUS_COLORS[status]
        cards = "".join(render_candidate_card(item) for item in items)
        if not cards:
            cards = dedent("""
            <div class="candidate-card">
                <div class="candidate-name">No roles yet</div>
                <div class="profile-link">Add one from the form below</div>
                <div class="card-age">Ready when you are</div>
            </div>
            """).strip()
        columns_html.append(
            dedent(f"""
            <div class="pipeline-column">
                <div class="column-head">
                    <span class="column-title">
                        <span class="status-square" style="background:{color};"></span>
                        {STATUS_LABELS[status]}
                        <span class="count-pill">{len(items)}</span>
                    </span>
                    <span class="dots">...</span>
                </div>
                {cards}
            </div>
            """).strip()
        )

    st.markdown(
        f"<div class='pipeline-board'>{''.join(columns_html)}</div>",
        unsafe_allow_html=True,
    )


def render_selected_application_details(applications: list[dict]) -> None:
    application_id = selected_job_id()
    if application_id is None:
        return

    application = next((item for item in applications if item["id"] == application_id), None)
    if application is None:
        return

    company = escape(application["company_name"])
    title = escape(application["job_title"])
    status = escape(STATUS_LABELS.get(application["status"], application["status"]))
    location = escape(application.get("location") or "Not added")
    salary = escape(application.get("salary_range") or "Not added")
    applied_date = escape(format_date(application.get("applied_date")))
    notes = escape(application.get("notes") or "No notes added.")

    st.markdown(
        dedent(f"""
        <div class="placeholder-card">
            <span class="placeholder-icon">{initials(application["job_title"], application["company_name"])}</span>
            <div>
                <div class="placeholder-title">{company} - {title}</div>
                <div class="placeholder-copy">
                    Status: {status} &nbsp; | &nbsp; Location: {location} &nbsp; | &nbsp; Salary: {salary}
                </div>
                <div class="placeholder-copy">Applied date: {applied_date}</div>
                <div class="placeholder-copy">Notes: {notes}</div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )


def render_dashboard_stats(
    total_count: int,
    active_count: int,
    interview_count: int,
    offer_count: int,
) -> None:
    stats = [
        ("Visible jobs", total_count),
        ("Active", active_count),
        ("Interviews", interview_count),
        ("Offers", offer_count),
    ]
    cards = "".join(
        dedent(f"""
        <div class="dashboard-stat">
            <div class="dashboard-stat-label">{label}</div>
            <div class="dashboard-stat-value">{value}</div>
        </div>
        """).strip()
        for label, value in stats
    )
    st.markdown(
        f"<div class='dashboard-stat-strip'>{cards}</div>",
        unsafe_allow_html=True,
    )


def render_placeholder_view(title: str) -> None:
    icon = {
        "Candidates": "◎",
        "Messages": "✉",
        "Company": "□",
        "Settings": "⚙",
    }.get(title, "▦")
    st.markdown(
        dedent(f"""
        <div class="placeholder-card">
            <span class="placeholder-icon">{icon}</span>
            <div>
                <div class="placeholder-title">{escape(title)} is reserved for a future phase</div>
                <div class="placeholder-copy">This section is not connected to backend features yet, so no fake data is shown.</div>
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True,
    )


def render_candidates_view() -> None:
    cards = []
    for candidate in SAMPLE_CANDIDATES:
        name = escape(candidate["name"])
        role = escape(candidate["role"])
        location = escape(candidate["location"])
        stage = escape(candidate["stage"])
        experience = escape(candidate["experience"])
        avatar = initials(candidate["name"])
        cards.append(
            dedent(f"""
            <div class="candidate-card">
                <div class="card-main">
                    <span class="card-avatar">{avatar}</span>
                    <div>
                        <div class="candidate-name">{name}</div>
                        <div class="profile-link">{role}</div>
                    </div>
                </div>
                <div class="card-age">{location} - {experience} - {stage}</div>
            </div>
            """).strip()
        )

    st.markdown(
        f"<div class='pipeline-board'>{''.join(cards)}</div>",
        unsafe_allow_html=True,
    )


def application_matches(
    application: dict,
    search_value: str,
    selected_statuses: list[str],
    show_closed: bool,
) -> bool:
    haystack = (
        f"{application['company_name']} {application['job_title']} "
        f"{application.get('location') or ''} {application.get('notes') or ''}"
    ).lower()
    matches_search = not search_value or search_value in haystack
    matches_status = not selected_statuses or application["status"] in selected_statuses
    matches_closed = show_closed or application["status"] not in {"Accepted", "Rejected"}
    return matches_search and matches_status and matches_closed


def handle_create_application() -> None:
    with st.form("create_application_form", clear_on_submit=True):
        st.subheader("Add New Job")
        st.caption("Save a role you want to track in your career pipeline.")
        form_cols = st.columns(2, gap="small")
        with form_cols[0]:
            company_name = st.text_input("Company name")
            status = st.selectbox("Status", STATUSES, index=1)
            salary_range = st.text_input("Salary range")
        with form_cols[1]:
            job_title = st.text_input("Job title")
            location = st.text_input("Location")
            use_applied_date = st.checkbox("Add applied date", value=True)

        applied_date = None
        if use_applied_date:
            applied_date = st.date_input("Applied date", value=date.today())

        notes = st.text_area("Notes", height=90)
        create_submit = st.form_submit_button("Create Job", use_container_width=True)

    if create_submit:
        payload = {
            "company_name": company_name,
            "job_title": job_title,
            "status": status,
            "location": location or None,
            "salary_range": salary_range or None,
            "applied_date": applied_date.isoformat() if applied_date else None,
            "notes": notes or None,
        }
        if is_demo_session():
            next_id = max((item["id"] for item in st.session_state.demo_applications), default=0) + 1
            st.session_state.demo_applications.append(
                {
                    "id": next_id,
                    "created_at": date.today().isoformat(),
                    **payload,
                }
            )
            st.success("Application added.")
            st.rerun()

        try:
            response = requests.post(
                f"{API_URL}/applications",
                json=payload,
                headers=auth_headers(),
                timeout=10,
            )
        except requests.RequestException:
            st.error("Could not connect to the backend API.")
            return
        if response.ok:
            st.success("Application added.")
            st.rerun()
        else:
            st.error(api_error_message(response, "Could not add application"))


def render_editors(applications: list[dict]) -> None:
    if not applications:
        return

    st.subheader("Manage Jobs")
    for application in applications:
        label = f"{application['company_name']} - {application['job_title']} - {application['status']}"
        with st.expander(label):
            with st.form(f"edit_form_{application['id']}"):
                st.caption("Edit this job without changing the backend payload.")
                edit_top = st.columns(2)
                with edit_top[0]:
                    edit_company = st.text_input(
                        "Company name",
                        value=application["company_name"],
                        key=f"edit_company_{application['id']}",
                    )
                    edit_status = st.selectbox(
                        "Status",
                        STATUSES,
                        index=STATUSES.index(application["status"]),
                        key=f"edit_status_{application['id']}",
                    )
                    edit_salary = st.text_input(
                        "Salary range",
                        value=application["salary_range"] or "",
                        key=f"edit_salary_{application['id']}",
                    )
                with edit_top[1]:
                    edit_title = st.text_input(
                        "Job title",
                        value=application["job_title"],
                        key=f"edit_title_{application['id']}",
                    )
                    edit_location = st.text_input(
                        "Location",
                        value=application["location"] or "",
                        key=f"edit_location_{application['id']}",
                    )
                    existing_date = parse_date(application.get("applied_date"))
                    keep_date = st.checkbox(
                        "Keep applied date",
                        value=existing_date is not None,
                        key=f"edit_keep_date_{application['id']}",
                    )

                edit_applied_date = None
                if keep_date:
                    edit_applied_date = st.date_input(
                        "Applied date",
                        value=existing_date or date.today(),
                        key=f"edit_applied_date_{application['id']}",
                    )

                edit_notes = st.text_area(
                    "Notes",
                    value=application["notes"] or "",
                    height=100,
                    key=f"edit_notes_{application['id']}",
                )

                save_submit = st.form_submit_button("Save changes", use_container_width=True)

            confirm_key = f"delete_confirmed_{application['id']}"
            if confirm_key not in st.session_state:
                st.session_state[confirm_key] = False

            st.markdown(
                "<div class='delete-warning'>Deleting is permanent. Tick the confirmation box before using Delete Job.</div>",
                unsafe_allow_html=True,
            )
            confirm_delete = st.checkbox(
                "I understand and want to delete this job",
                key=confirm_key,
            )

            delete_submit = st.button(
                "Delete job",
                key=f"delete_job_{application['id']}",
                use_container_width=True,
            )
            confirm_delete = st.session_state[confirm_key]

            if save_submit:
                payload = {
                    "company_name": edit_company,
                    "job_title": edit_title,
                    "status": edit_status,
                    "location": edit_location or None,
                    "salary_range": edit_salary or None,
                    "applied_date": edit_applied_date.isoformat() if edit_applied_date else None,
                    "notes": edit_notes or None,
                }
                if is_demo_session():
                    st.session_state.demo_applications = [
                        {**item, **payload} if item["id"] == application["id"] else item
                        for item in st.session_state.demo_applications
                    ]
                    st.success("Application updated.")
                    st.rerun()

                try:
                    update_response = requests.put(
                        f"{API_URL}/applications/{application['id']}",
                        json=payload,
                        headers=auth_headers(),
                        timeout=10,
                    )
                except requests.RequestException:
                    st.error("Could not connect to the backend API.")
                    return
                if update_response.ok:
                    st.success("Application updated.")
                    st.rerun()
                else:
                    st.error(api_error_message(update_response, "Update failed"))

            if delete_submit:
                if not confirm_delete:
                    st.warning("Please confirm before deleting this job.")
                else:
                    if is_demo_session():
                        st.session_state.demo_applications = [
                            item
                            for item in st.session_state.demo_applications
                            if item["id"] != application["id"]
                        ]
                        st.success("Application deleted.")
                        st.rerun()

                    try:
                        delete_response = requests.delete(
                            f"{API_URL}/applications/{application['id']}",
                            headers=auth_headers(),
                            timeout=10,
                        )
                    except requests.RequestException:
                        st.error("Could not connect to the backend API.")
                        return
                    if delete_response.ok:
                        st.success("Application deleted.")
                        st.rerun()
                    else:
                        st.error(api_error_message(delete_response, "Delete failed"))


def render_auth_screen() -> None:
    left_col, right_col = st.columns([0.82, 1.18], gap="small")

    with left_col:
        st.markdown(
            f"""
            <div
                class="auth-visual"
                style='background-image:
                    linear-gradient(90deg, rgba(7, 24, 55, 0.72), rgba(7, 24, 55, 0.08) 58%),
                    url("data:image/png;base64,{AUTH_HERO_IMAGE_DATA}");'
            >
                <div class="auth-visual-brand">Career Pipeline</div>
                <div class="auth-visual-copy">"Simply all the tools<br>for every job search."</div>
                <div class="auth-visual-person">Usman Ahmad<br>Career Pipeline Sprint Project</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        with st.container(border=True):
            if st.session_state.auth_mode == "Login":
                st.subheader("Welcome back to Career Pipeline")
                st.markdown(
                    "<div class='auth-subtitle'>Track applications, interviews, and offers from one clean dashboard.</div>",
                    unsafe_allow_html=True,
                )
                login_username = st.text_input("Username")
                login_password = st.text_input("Password", type="password")
                st.markdown("<div class='auth-link'>Forgot password?</div>", unsafe_allow_html=True)
                login_submit = st.button(
                    "Log in",
                    key="login_submit",
                    type="primary",
                    use_container_width=True,
                )

                if login_submit:
                    if DEMO_MODE:
                        if login_username == "usman" and login_password == "12345678":
                            st.session_state.auth_error = None
                            st.session_state.demo_username = login_username
                            st.session_state.token = DEMO_TOKEN
                            st.toast("Logged in successfully.")
                            st.rerun()
                        else:
                            st.session_state.auth_error = "Invalid username or password."
                    else:
                        try:
                            response = requests.post(
                                f"{API_URL}/auth/token",
                                data={"username": login_username, "password": login_password},
                                timeout=10,
                            )
                        except requests.RequestException:
                            st.session_state.auth_error = "Could not connect to the backend API."
                            response = None
                    if DEMO_MODE:
                        pass
                    elif response and response.ok:
                        st.session_state.auth_error = None
                        st.session_state.token = response.json()["access_token"]
                        st.toast("Logged in successfully.")
                        st.rerun()
                    elif response is not None:
                        st.session_state.auth_error = api_error_message(
                            response,
                            "Invalid username or password.",
                        )

                if st.session_state.auth_error:
                    st.markdown(
                        f"<div class='auth-error-banner'>{escape(st.session_state.auth_error)}</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    "<div class='auth-note'>Do not have an account?</div>",
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Create account",
                    key="switch_to_register",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state.auth_error = None
                    st.session_state.auth_mode = "Register"
                    st.rerun()
            else:
                st.subheader("Create your account")
                st.markdown(
                    "<div class='auth-subtitle'>Start organizing your job applications with a secure account.</div>",
                    unsafe_allow_html=True,
                )
                register_username = st.text_input("Username")
                register_password = st.text_input("Password", type="password")
                register_submit = st.button(
                    "Create account",
                    key="register_submit",
                    type="primary",
                    use_container_width=True,
                )

                if register_submit:
                    if DEMO_MODE:
                        st.session_state.auth_error = None
                        st.session_state.demo_username = register_username or "demo"
                        st.session_state.token = DEMO_TOKEN
                        st.toast("Account created.")
                        st.rerun()
                    else:
                        try:
                            response = requests.post(
                                f"{API_URL}/auth/register",
                                json={"username": register_username, "password": register_password},
                                timeout=10,
                            )
                        except requests.RequestException:
                            st.session_state.auth_error = "Could not connect to the backend API."
                            response = None
                        if response and response.ok:
                            st.session_state.auth_error = None
                            st.toast("Account created. You can log in now.")
                            st.session_state.auth_mode = "Login"
                            st.rerun()
                        elif response is not None:
                            st.session_state.auth_error = api_error_message(response, "Registration failed")

                if st.session_state.auth_error:
                    st.markdown(
                        f"<div class='auth-error-banner'>{escape(st.session_state.auth_error)}</div>",
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    "<div class='auth-note'>Already have an account?</div>",
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Log in",
                    key="switch_to_login",
                    type="secondary",
                    use_container_width=True,
                ):
                    st.session_state.auth_error = None
                    st.session_state.auth_mode = "Login"
                    st.rerun()


def render_dashboard() -> None:
    current_user = fetch_current_user()
    applications = fetch_applications()

    rail_col, main_col = st.columns([0.16, 0.84], gap="small")
    with rail_col:
        render_nav()

    with main_col:
        search_text, selected_statuses, show_closed = render_dashboard_filters(current_user)
        active_nav = st.session_state.active_nav
        shows_pipeline_view = active_nav in {"Dashboard", "Jobs"}

        search_value = search_text.strip().lower()
        filtered_applications = [
            application
            for application in applications
            if application_matches(application, search_value, selected_statuses, show_closed)
        ]

        total_count = len(filtered_applications)
        active_count = sum(
            1 for item in filtered_applications if item["status"] not in {"Rejected", "Accepted"}
        )
        interview_count = sum(
            1 for item in filtered_applications if item["status"] in {"Interview", "Technical Round"}
        )
        offer_count = sum(1 for item in filtered_applications if item["status"] == "Offer")

        username = current_user.get("username", "there")
        if active_nav == "Dashboard":
            title = f"Good to see you, {username}"
            subtitle = "Here is a clean overview of your job search progress."
        elif active_nav == "Jobs":
            title = "Jobs"
            subtitle = "Create, update, and organize every job application."
        else:
            title = active_nav
            subtitle = "This area is planned for a future project phase."

        render_header(total_count if shows_pipeline_view else 0, title, subtitle)
        render_dashboard_stats(total_count, active_count, interview_count, offer_count)

        if active_nav == "Dashboard":
            render_pipeline(filtered_applications)
            render_selected_application_details(filtered_applications)
        elif active_nav == "Jobs":
            pipeline_col, form_col = st.columns([1.25, 0.75], gap="small")
            with pipeline_col:
                render_pipeline(filtered_applications)
                render_selected_application_details(filtered_applications)
            with form_col:
                handle_create_application()
                render_editors(filtered_applications)
        elif active_nav == "Candidates":
            render_candidates_view()
        else:
            render_placeholder_view(active_nav)


if not st.session_state.token:
    render_auth_screen()
else:
    render_dashboard()
