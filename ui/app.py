import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import requests
from ui.styles import load_css


def _format_domain(url: str) -> str:
    try:
        host = urlparse(url).netloc
        return host.replace("www.", "")
    except Exception:
        return url[:40]

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Web Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(load_css(), unsafe_allow_html=True)

st.markdown('<div class="search-agent-header">🔍 Ask the Web</div>', unsafe_allow_html=True)
st.markdown('<div class="search-agent-subtitle">Real-time answers powered by AI search</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("💬 Chat Controls")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Ask a question about anything (Press Enter to send)..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Searching the web..."):
            try:
                # Send plain-text history for conversational context
                import re
                clean_history = []
                for m in st.session_state.messages[:-1]:
                    text = re.sub(r"<[^>]+>", "", m["content"]).strip()
                    if text:
                        clean_history.append({"role": m["role"], "content": text[:300]})

                payload = {"query": prompt, "history": clean_history or None}
                response = requests.post(f"{API_URL}/query", json=payload, timeout=60)


                if response.status_code == 503:
                    error_msg = "Search provider is rate-limited. Wait a moment and try again."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.stop()

                response.raise_for_status()
                data = response.json()

                answer = data.get("answer", "No answer returned.")
                sources = data.get("sources", [])

                full_response = f"<div style='line-height:1.8'>{answer}</div>"

                if sources:
                    pills = ""
                    for i, s in enumerate(sources, 1):
                        label = _format_domain(s)
                        pills += f'<a href="{s}" class="source-tag" target="_blank">{i}. {label}</a> '
                    full_response += (
                        '<hr style="border:none;border-top:1px solid #334155;margin:12px 0">'
                        f'<div style="margin-top:8px">{pills}</div>'
                    )

                st.markdown(full_response, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except requests.exceptions.ConnectionError:
                error_msg = "Cannot reach the backend. Make sure the API server is running on port 8000."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.Timeout:
                error_msg = "Request timed out. Try again."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except requests.exceptions.RequestException as e:
                error_msg = f"Request failed: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
