
def load_css():
    return """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* ── Base ─────────────────────────────────────────────── */
    .stApp {
        background-color: #0b0f14;
        color: #e6edf3;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ── Container ────────────────────────────────────────── */
    .block-container {
        max-width: 820px !important;
        margin: 0 auto !important;
        padding-top: 70px !important;
        padding-bottom: 60px !important;
    }

    /* ── Title ─────────────────────────────────────────────── */
    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: 600;
        letter-spacing: -0.02em;
        color: #e6edf3;
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 15px;
        margin-bottom: 40px;
    }

    /* ── Card ──────────────────────────────────────────────── */
    .card {
        background: #11161c;
        border: 1px solid #1c232b;
        border-radius: 12px;
        padding: 22px 24px;
        margin-top: 18px;
    }

    .card-label {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #8b949e;
        margin-bottom: 12px;
    }

    .card-body {
        font-size: 15px;
        line-height: 1.7;
        color: #c9d1d9;
        white-space: pre-wrap;
    }

    /* ── Sources ───────────────────────────────────────────── */
    .source-link {
        display: block;
        font-size: 13.5px;
        color: #38bdf8;
        text-decoration: none;
        padding: 6px 0;
        word-break: break-all;
    }

    .source-link:hover {
        text-decoration: underline;
        color: #7dd3fc;
    }

    /* ── Input ─────────────────────────────────────────────── */
    .stTextInput > div > div > input {
        background: #0f141a !important;
        border: 1px solid #1f2730 !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        color: #e6edf3 !important;
        font-size: 15px !important;
        transition: border-color 0.15s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #38bdf8 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #484f58 !important;
    }

    .stTextInput label { display: none !important; }

    /* ── Button ────────────────────────────────────────────── */
    .stButton > button {
        background: #0f141a !important;
        border: 1px solid #1f2730 !important;
        border-radius: 10px !important;
        color: #e6edf3 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 10px 22px !important;
        width: 100% !important;
        transition: border-color 0.15s ease, color 0.15s ease !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
    }

    .stButton > button:active {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
    }

    /* ── Divider ───────────────────────────────────────────── */
    hr {
        border: none !important;
        border-top: 1px solid #1c232b !important;
        margin: 0 0 28px 0 !important;
    }

    /* ── Spinner / Alerts ──────────────────────────────────── */
    .stSpinner > div { border-top-color: #38bdf8 !important; }

    .stAlert {
        background: #11161c !important;
        border: 1px solid #1c232b !important;
        border-radius: 10px !important;
    }

    /* ── Scrollbar ─────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #1f2730; border-radius: 10px; }

    </style>
    """
