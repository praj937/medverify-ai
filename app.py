import streamlit as st
import requests

st.set_page_config(page_title="MedVerify AI", layout="centered")

st.title("🩺 MedVerify AI")
st.markdown("Upload a medical document to analyze compliance and detect forgery.")

file = st.file_uploader("📄 Upload Document")

if file:
    st.info("Analyzing document...")

    files = {"file": file.getvalue()}
    res = requests.post("http://127.0.0.1:8000/analyze/", files=files)

    if res.status_code == 200:
        data = res.json()

        st.success("Analysis Complete ✅")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Document Type", data["document_type"])

        with col2:
            st.metric("Compliance", data["compliance"])

        st.metric("Fake Probability", f"{data['fake_probability']:.2f}")

        st.divider()

        st.subheader("💬 Chatbot")
        query = st.text_input("Ask about the result")

        if query:
            chat = requests.post(
                "http://127.0.0.1:8000/chat/",
                params={"query": query}
            )
            st.write(chat.json()["response"])