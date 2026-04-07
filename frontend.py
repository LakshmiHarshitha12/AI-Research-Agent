import streamlit as st
import requests

# Your deployed API URL
API_URL = "https://ai-research-agent-2-yihb.onrender.com/research"

st.set_page_config(page_title="AI Research Agent", layout="centered")

st.title("🔬 AI Research Agent")
st.write("Enter a topic and get a full AI-generated research report")

query = st.text_input("Enter topic:")

if st.button("Generate Research"):
    if query:
        with st.spinner("Researching..."):
            try:
                response = requests.get(API_URL, params={"query": query})
                data = response.json()

                if data["status"] == "success":
                    st.success("Done!")
                    st.write(data["result"])
                else:
                    st.error(data["message"])
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a topic")