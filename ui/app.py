import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Web Search Agent", layout="centered")

st.title("AI Web Search Agent")
st.markdown("Minimal interface for the AI Web Search Agent.")

query = st.text_input("User Question Input", placeholder="What are the latest MacBook specs?")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Searching the web..."):
            try:
                response = requests.post(f"{API_URL}/query", json={"query": query})
                response.raise_for_status()
                data = response.json()
                
                st.subheader("Answer")
                st.write(data.get("answer", ""))
                
                st.subheader("Sources")
                sources = data.get("sources", [])
                if sources:
                    for source in sources:
                        st.markdown(f"- {source}")
                else:
                    st.write("No sources found.")
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to backend: {e}")
