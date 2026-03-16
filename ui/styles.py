def load_css() -> str:
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@400;600;700&display=swap');

        .stApp {
            font-family: 'Inter', sans-serif;
        }

        .search-agent-header {
            background: linear-gradient(90deg, #6C63FF 0%, #3F3CBB 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
            text-align: center;
            font-family: 'Outfit', sans-serif;
        }

        .search-agent-subtitle {
            color: #6B7280;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 2rem;
            font-weight: 500;
        }

        .source-tag {
            display: inline-block;
            background-color: rgba(99,102,241,0.12);
            color: #818CF8 !important;
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 600;
            text-decoration: none !important;
            margin: 4px 6px 4px 0;
            border: 1px solid rgba(99,102,241,0.25);
            transition: all 0.2s ease;
            max-width: 260px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .source-tag:hover {
            background-color: rgba(99,102,241,0.22);
            border-color: #818CF8;
            transform: translateY(-1px);
        }

        [data-testid="chatAvatarIcon-assistant"] {
            background-color: #6C63FF !important;
            color: white !important;
        }

        [data-testid="chatAvatarIcon-user"] {
            background-color: #1F2937 !important;
            color: white !important;
        }
    </style>
    """
