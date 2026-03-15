import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import requests
from styles import load_css

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Web Search",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(load_css(), unsafe_allow_html=True)

st.markdown('<div class="main-title">AI Web Search</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask the internet anything</div>', unsafe_allow_html=True)
st.divider()

query = st.text_input("Query", placeholder="Ask a question…", label_visibility="collapsed")

if st.button("Ask"):
    if not query.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Thinking…"):
            try:
                response = requests.post(
                    f"{API_URL}/query", json={"query": query}, timeout=60
                )

                if response.status_code == 503:
                    st.warning("Search provider is rate-limited. Wait a moment and try again.")
                    st.stop()

                response.raise_for_status()
                data = response.json()

                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])

                st.markdown(f"""
                <div class="card">
                    <div class="card-label">Answer</div>
                    <div class="card-body">{answer}</div>
                </div>
                """, unsafe_allow_html=True)

                if sources:
                    links_html = "".join(
                        f'<a class="source-link" href="{s}" target="_blank" rel="noopener">{s}</a>'
                        for s in sources
                    )
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-label">Sources</div>
                        {links_html}
                    </div>
                    """, unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("Cannot reach the backend. Make sure the API server is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
