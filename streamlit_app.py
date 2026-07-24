import base64
from datetime import date
from html import escape
from pathlib import Path
from textwrap import dedent

import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
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

st.set_page_config(page_title="Career Pipeline", page_icon=":briefcase:", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --blue: #2387ed;
        --ink: #1d2634;
        --muted: #8b94a5;
        --line: #e7ebf1;
        --panel: #ffffff;
        --page: #edf3f8;
    }

    .stApp {
        background:
            radial-gradient(circle at 9% 6%, rgba(255, 255, 255, 0.72), transparent 28%),
            linear-gradient(145deg, #e8eef4 0%, #f7fbff 46%, #dde8f3 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1500px;
        padding: 2.2rem 2.25rem 2.5rem;
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
        gap: 0.95rem;
    }

    .join-shell {
        background: var(--panel);
        border: 1px solid #dbe3ed;
        border-radius: 12px;
        box-shadow: 0 18px 42px rgba(34, 48, 68, 0.12);
        overflow: hidden;
        margin: 0 auto 1.15rem;
        min-height: min(760px, calc(100vh - 5rem));
        width: 100%;
    }

    .side-rail {
        border-right: 1px solid var(--line);
        background: #ffffff;
        border-radius: 10px 0 0 10px;
        min-height: auto;
        padding: 1.35rem 1rem 0.75rem;
    }

    .brand {
        align-items: center;
        color: #0f172a;
        display: flex;
        font-size: 1.95rem;
        font-weight: 900;
        justify-content: space-between;
        letter-spacing: 0;
        padding: 0 0 1rem;
    }

    .brand span:first-child::first-letter {
        color: var(--blue);
    }

    .collapse-pill {
        align-items: center;
        border: 1px solid #e6edf5;
        border-radius: 999px;
        color: #8b94a5;
        display: inline-flex;
        font-size: 0.9rem;
        height: 1.8rem;
        justify-content: center;
        width: 1.8rem;
    }

    .sidebar-search {
        align-items: center;
        border: 1px solid #e0e7f0;
        border-radius: 8px;
        color: #8b94a5;
        display: flex;
        font-size: 0.9rem;
        justify-content: space-between;
        margin: 0.5rem 0 1.2rem;
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
        background: var(--blue);
        border-radius: 50%;
        color: #ffffff;
        display: inline-flex;
        height: 2rem;
        justify-content: center;
        width: 2rem;
    }

    .nav-item {
        align-items: center;
        background: transparent;
        border: 0;
        color: #7f8a9b;
        cursor: pointer;
        display: flex;
        font-size: 0.93rem;
        font-weight: 650;
        gap: 0.7rem;
        line-height: 1;
        margin: 0.12rem 0.6rem;
        padding: 0.72rem 0.7rem;
        border-radius: 6px;
        text-align: left;
        width: calc(100% - 1.2rem);
    }

    .nav-item.active {
        background: #eef7ff;
        color: var(--blue);
        font-weight: 850;
    }

    .nav-item:hover {
        background: #f1f7fd;
        color: var(--blue);
    }

    .control-spacer {
        height: 1.35rem;
    }

    .nav-icon {
        align-items: center;
        color: inherit;
        display: inline-flex;
        font-size: 0.78rem;
        font-weight: 900;
        height: 1.25rem;
        justify-content: center;
        width: 1.35rem;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button {
        border: 0;
        border-radius: 8px;
        box-shadow: none;
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 750;
        justify-content: flex-start;
        margin: 0.18rem 0;
        min-height: 2.75rem;
        padding: 0 0.95rem;
        width: 100%;
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button:hover {
        background: #eef7ff;
        color: var(--blue);
    }

    div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]:has(.side-rail) ~ div[data-testid="stElementContainer"] div[data-testid="stButton"] button[kind="primary"] {
        background: #eef7ff;
        border-left: 4px solid var(--blue);
        color: var(--blue);
    }

    .main-pane {
        background: #ffffff;
        min-height: min(760px, calc(100vh - 5rem));
        overflow: hidden;
        padding: 0;
    }

    .topbar,
    .job-header,
    .tabs-line,
    .toolbar-line,
    .dashboard-stat-strip,
    .pipeline-board {
        border-left: 1px solid #eef2f7;
    }

    .topbar {
        align-items: center;
        border-bottom: 1px solid var(--line);
        display: flex;
        justify-content: flex-end;
        padding: 0.9rem 1.25rem;
    }

    .dashboard-user-inline {
        align-items: center;
        display: flex;
        height: 2.7rem;
        justify-content: flex-end;
    }

    .dashboard-archive-spacer {
        height: 1.35rem;
    }

    .top-icon-row {
        align-items: center;
        display: flex;
        gap: 0.55rem;
        height: 2.7rem;
        justify-content: flex-end;
    }

    .top-icon {
        align-items: center;
        background: #f8f7fb;
        border: 1px solid #eef1f6;
        border-radius: 50%;
        color: #64748b;
        display: inline-flex;
        font-size: 1rem;
        height: 2.45rem;
        justify-content: center;
        width: 2.45rem;
    }

    .profile-avatar {
        align-items: center;
        background: linear-gradient(145deg, #dbeafe, #93c5fd);
        border: 2px solid #ffffff;
        border-radius: 50%;
        box-shadow: 0 6px 14px rgba(35, 135, 237, 0.16);
        color: #0f4c81;
        display: inline-flex;
        font-weight: 900;
        height: 2.55rem;
        justify-content: center;
        width: 2.55rem;
    }

    .searchbox {
        align-items: center;
        background: #f8fbff;
        border: 1px solid #dde6f1;
        border-radius: 6px;
        box-shadow: 0 3px 12px rgba(33, 46, 63, 0.04);
        color: #9aa3af;
        display: flex;
        gap: 0.65rem;
        min-height: 2.6rem;
        padding: 0 0.8rem;
    }

    .primary-action {
        align-items: center;
        background: var(--blue);
        border-radius: 5px;
        box-shadow: 0 7px 14px rgba(35, 135, 237, 0.18);
        color: #ffffff;
        display: inline-flex;
        font-size: 0.94rem;
        font-weight: 750;
        gap: 0.55rem;
        min-height: 2.6rem;
        padding: 0 1.05rem;
    }

    .user-pill {
        align-items: center;
        color: #303948;
        display: flex;
        gap: 0.65rem;
        justify-content: end;
        white-space: nowrap;
    }

    .avatar {
        align-items: center;
        background: #e8edf5;
        border-radius: 50%;
        color: var(--blue);
        display: inline-flex;
        font-size: 0.82rem;
        font-weight: 900;
        height: 2.1rem;
        justify-content: center;
        width: 2.1rem;
    }

    .job-header {
        padding: 1.2rem 1.25rem 0.45rem;
    }

    .back-dot {
        align-items: center;
        background: #f2f5f9;
        border-radius: 50%;
        color: #9ca5b2;
        display: inline-flex;
        height: 1.65rem;
        justify-content: center;
        margin-right: 0.65rem;
        width: 1.65rem;
    }

    .job-title {
        color: #252d3a;
        font-size: 1.12rem;
        font-weight: 850;
        line-height: 1.2;
    }

    .job-meta {
        color: #9aa3af;
        font-size: 0.82rem;
        padding-left: 2.35rem;
    }

    .tabs-line {
        align-items: end;
        border-bottom: 1px solid var(--line);
        color: #9aa3af;
        display: flex;
        gap: 2.25rem;
        padding: 1rem 1.25rem 0;
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
        display: flex;
        justify-content: space-between;
        padding: 1rem 1.25rem 0.7rem;
    }

    .segmented {
        border: 1px solid #d8dde5;
        border-radius: 6px;
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
        background: #eef7ff;
        border-bottom: 2px solid var(--blue);
        color: var(--blue);
    }

    .select-mode {
        border: 1px solid var(--line);
        border-radius: 5px;
        color: #303948;
        font-size: 0.86rem;
        font-weight: 750;
        padding: 0.6rem 0.8rem;
    }

    .pipeline-board {
        background: #f8fafd;
        display: grid;
        gap: 0.7rem;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        overflow: visible;
        padding: 0.85rem 0.9rem 1rem;
    }

    .pipeline-column {
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
        margin-bottom: 0.8rem;
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
        border: 1px solid var(--line);
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(41, 54, 72, 0.055);
        margin-bottom: 0.62rem;
        padding: 0.78rem 0.72rem;
    }

    .candidate-card:hover {
        border-color: #c8d9ee;
        box-shadow: 0 8px 18px rgba(41, 54, 72, 0.09);
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
        background: #89c5ff;
        border-radius: 50%;
        color: #2a6fb5;
        display: inline-flex;
        flex: 0 0 1.9rem;
        font-size: 0.78rem;
        font-weight: 900;
        height: 1.9rem;
        justify-content: center;
        width: 1.9rem;
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
        min-height: calc(100vh - 5.2rem);
        overflow: hidden;
        padding: 1.45rem;
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
        bottom: 2.2rem;
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 850;
        left: 1.6rem;
        line-height: 1.12;
        max-width: 360px;
        padding: 0;
        position: absolute;
        text-align: left;
        text-shadow: 0 3px 16px rgba(0, 0, 0, 0.38);
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
    }

    .auth-hero {
        display: none;
    }

    .auth-title {
        color: #1d2634;
        font-size: 2.15rem;
        font-weight: 900;
        line-height: 1.12;
        margin: 0.7rem 0 0.75rem;
        max-width: 600px;
    }

    .auth-copy {
        color: #737f8f;
        font-size: 1rem;
        line-height: 1.65;
        max-width: 520px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: 0 8px 20px rgba(33, 46, 63, 0.05);
        padding: 1rem;
    }

    .dashboard-stat-strip {
        background: #ffffff;
        border-bottom: 1px solid var(--line);
        display: grid;
        gap: 0.75rem;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        padding: 0.95rem 1.25rem;
    }

    .dashboard-stat {
        background: #f8fbff;
        border: 1px solid #e0e8f2;
        border-radius: 8px;
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

    .dashboard-controls-title {
        color: #1d2634;
        font-size: 1.05rem;
        font-weight: 900;
        margin: 1.35rem 0 0.45rem;
    }

    .metric-label {
        color: #8b94a5;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
    }

    .metric-value {
        color: #1d2634;
        font-size: 1.7rem;
        font-weight: 900;
        margin-top: 0.1rem;
    }

    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 8px;
        box-shadow: none;
        min-height: auto;
        padding: 0.9rem 1rem;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 0;
        border-radius: 0 14px 14px 0;
        box-shadow: none;
        min-height: calc(100vh - 5.2rem);
        padding: clamp(3.2rem, 8vh, 6.4rem) clamp(3.8rem, 6vw, 6.6rem) 3.2rem;
    }

    div[data-testid="stForm"] h3 {
        color: #1d2634;
        font-size: 1.2rem;
        font-weight: 850;
        margin-bottom: 0.85rem;
    }

    div[data-testid="stHorizontalBlock"]:has(.auth-visual) div[data-testid="stVerticalBlockBorderWrapper"] h3 {
        color: #1d2634;
        font-size: 1.55rem;
        font-weight: 850;
        margin-bottom: 1.55rem;
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
        border-radius: 6px;
        color: #1d2634;
        min-height: 2.45rem;
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
        border-radius: 5px;
        font-weight: 750;
        min-height: 2.5rem;
    }

    .stFormSubmitButton > button {
        background: var(--blue);
        border: 1px solid var(--blue);
        color: #ffffff;
    }

    .stFormSubmitButton > button:hover {
        background: #1676d9;
        border-color: #1676d9;
        color: #ffffff;
    }

    div[data-testid="stButton"] button {
        border: 1px solid var(--blue);
        border-radius: 6px;
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
        background: #eef7ff;
        color: var(--blue);
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #1676d9;
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

    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stHorizontalBlock"]) {
        row-gap: 0.75rem;
    }

    @media (max-width: 900px) {
        .block-container {
            padding: 1rem;
        }

        .join-shell,
        .side-rail,
        .main-pane {
            min-height: auto;
        }

        .side-rail {
            border-bottom: 1px solid var(--line);
            border-right: 0;
        }

        .topbar {
            grid-template-columns: 1fr;
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
if "active_status_filter" not in st.session_state:
    st.session_state.active_status_filter = "All"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Jobs"


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
    response = requests.get(
        f"{API_URL}/applications",
        headers=auth_headers(),
        timeout=10,
    )
    if response.ok:
        return response.json()
    st.error(api_error_message(response, "Could not load applications"))
    return []


def fetch_current_user() -> dict:
    response = requests.get(
        f"{API_URL}/auth/me",
        headers=auth_headers(),
        timeout=10,
    )
    if response.ok:
        return response.json()
    st.error(api_error_message(response, "Could not load profile"))
    return {"username": "User"}


def render_nav() -> None:
    st.markdown(
        """
        <div class="side-rail">
            <div class="brand"><span>join</span><span class="collapse-pill">&laquo;</span></div>
            <div class="sidebar-search"><span>Search</span><span>&#128269;</span></div>
            <div class="workspace"><span class="workspace-icon">CP</span> Career</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for item, icon in zip(NAV_ITEMS, ["⌂", "▣", "◎", "✉", "□", "⚙"]):
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


def render_topbar(current_user: dict) -> None:
    username = escape(current_user.get("username", "User"))
    avatar = initials(username)
    st.markdown(
        f"""
        <div class="topbar">
            <div class="user-pill"><span class="avatar">{avatar}</span><span>{username}</span><span>v</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard_filters(current_user: dict) -> tuple[str, list[str], bool]:
    username = escape(current_user.get("username", "User"))
    avatar = initials(username)
    control_cols = st.columns([1.45, 0.82, 0.38, 0.32, 0.46], gap="small")
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
        if st.button("↪", use_container_width=True, key="dashboard_logout", help="Log out"):
            st.session_state.token = None
            st.rerun()
    with control_cols[4]:
        st.markdown("<div class='control-spacer'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="top-icon-row">
                <span class="top-icon">?</span>
                <span class="top-icon">&#128276;</span>
                <span class="profile-avatar">{avatar}</span>
                <span class="user-pill"><span>{username}</span><span>⌄</span></span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    return search_text, selected_statuses, show_closed


def render_header(total_count: int, title: str = "Career Pipeline") -> None:
    safe_title = escape(title)
    st.markdown(
        f"""
        <div class="job-header">
            <div class="job-title"><span class="back-dot">&lt;</span>{safe_title}</div>
            <div class="job-meta">#{total_count:06d} &nbsp;&nbsp; Remote and local job search</div>
        </div>
        <div class="tabs-line">
            <div class="tab">Candidates</div>
            <div class="tab active">Pipeline <span class="tiny-badge">{total_count}</span></div>
            <div class="tab">Free job boards</div>
            <div class="tab">Premium job boards</div>
            <div class="tab">Bookings</div>
            <div style="margin-left:auto;" class="tab">Share &nbsp;&nbsp; View &nbsp;&nbsp; Edit job ad</div>
        </div>
        <div class="toolbar-line">
            <div class="segmented"><span>Qualified</span><span>Disqualified</span></div>
            <div class="select-mode">Select mode</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_candidate_card(application: dict) -> str:
    company = escape(application["company_name"])
    title = escape(application["job_title"])
    location = escape(application.get("location") or "View profile")
    card_initials = initials(application["job_title"], application["company_name"])
    return dedent(f"""
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
    st.markdown(
        dedent(f"""
        <div class="candidate-card">
            <div class="candidate-name">{escape(title)}</div>
            <div class="card-age">This dashboard section is ready for the next step.</div>
        </div>
        """).strip(),
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
        st.subheader("Create new job")
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
        create_submit = st.form_submit_button("Save application", use_container_width=True)

    if create_submit:
        response = requests.post(
            f"{API_URL}/applications",
            json={
                "company_name": company_name,
                "job_title": job_title,
                "status": status,
                "location": location or None,
                "salary_range": salary_range or None,
                "applied_date": applied_date.isoformat() if applied_date else None,
                "notes": notes or None,
            },
            headers=auth_headers(),
            timeout=10,
        )
        if response.ok:
            st.success("Application added.")
            st.rerun()
        else:
            st.error(api_error_message(response, "Could not add application"))


def render_editors(applications: list[dict]) -> None:
    if not applications:
        return

    st.subheader("Job details")
    for application in applications:
        label = f"{application['company_name']} - {application['job_title']} - {application['status']}"
        with st.expander(label):
            with st.form(f"edit_form_{application['id']}"):
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

                action_cols = st.columns(2)
                with action_cols[0]:
                    save_submit = st.form_submit_button("Save changes", use_container_width=True)
                with action_cols[1]:
                    delete_submit = st.form_submit_button("Delete job", use_container_width=True)

            if save_submit:
                update_response = requests.put(
                    f"{API_URL}/applications/{application['id']}",
                    json={
                        "company_name": edit_company,
                        "job_title": edit_title,
                        "status": edit_status,
                        "location": edit_location or None,
                        "salary_range": edit_salary or None,
                        "applied_date": edit_applied_date.isoformat() if edit_applied_date else None,
                        "notes": edit_notes or None,
                    },
                    headers=auth_headers(),
                    timeout=10,
                )
                if update_response.ok:
                    st.success("Application updated.")
                    st.rerun()
                else:
                    st.error(api_error_message(update_response, "Update failed"))

            if delete_submit:
                delete_response = requests.delete(
                    f"{API_URL}/applications/{application['id']}",
                    headers=auth_headers(),
                    timeout=10,
                )
                if delete_response.ok:
                    st.success("Application deleted.")
                    st.rerun()
                else:
                    st.error(api_error_message(delete_response, "Delete failed"))


def render_auth_screen() -> None:
    left_col, right_col = st.columns([0.78, 1.22], gap="small")

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
                <div class="auth-visual-copy">Organize every role,<br>interview, and offer.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        with st.container(border=True):
            if st.session_state.auth_mode == "Login":
                st.subheader("Welcome back")
                login_username = st.text_input("Username")
                login_password = st.text_input("Password", type="password")
                login_submit = st.button(
                    "Log in",
                    key="login_submit",
                    type="primary",
                    use_container_width=True,
                )

                if login_submit:
                    response = requests.post(
                        f"{API_URL}/auth/token",
                        data={"username": login_username, "password": login_password},
                        timeout=10,
                    )
                    if response.ok:
                        st.session_state.token = response.json()["access_token"]
                        st.toast("Logged in successfully.")
                        st.rerun()
                    else:
                        error_message = api_error_message(
                            response,
                            "Invalid username or password.",
                        )
                        st.toast(error_message)

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
                    st.session_state.auth_mode = "Register"
                    st.rerun()
            else:
                st.subheader("Create account")
                register_username = st.text_input("Username")
                register_password = st.text_input("Password", type="password")
                register_submit = st.button(
                    "Create account",
                    key="register_submit",
                    type="primary",
                    use_container_width=True,
                )

                if register_submit:
                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={"username": register_username, "password": register_password},
                        timeout=10,
                    )
                    if response.ok:
                        st.toast("Account created. You can log in now.")
                        st.session_state.auth_mode = "Login"
                        st.rerun()
                    else:
                        error_message = api_error_message(response, "Registration failed")
                        st.toast(error_message)

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
        shows_jobs_view = active_nav == "Jobs"

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

        render_header(total_count if shows_jobs_view else 0, "Jobs" if shows_jobs_view else active_nav)
        render_dashboard_stats(total_count, active_count, interview_count, offer_count)

        if shows_jobs_view:
            pipeline_col, form_col = st.columns([1.25, 0.75], gap="small")
            with pipeline_col:
                render_pipeline(filtered_applications)
            with form_col:
                handle_create_application()
                render_editors(filtered_applications)
        else:
            render_placeholder_view(active_nav)


if not st.session_state.token:
    render_auth_screen()
else:
    render_dashboard()
