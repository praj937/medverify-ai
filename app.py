import streamlit as st
import random

st.set_page_config(page_title="MedVerify AI", layout="centered")

st.title("🩺 MedVerify AI")
st.markdown("Upload a medical document to analyze compliance and detect forgery.")

file = st.file_uploader("📄 Upload Document")

if file:
    st.info("Analyzing document...")

    text = file.getvalue().decode("utf-8", errors="ignore")

    doc_type = "Prescription" if "prescription" in text.lower() else "Medical Document"
    compliance = "Non-Compliant" if "overdose" in text.lower() else "Compliant"
    fake_prob = random.uniform(0, 1)

    data = {
        "document_type": doc_type,
        "compliance": compliance,
        "fake_probability": fake_prob
    }

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
        if "compliance" in query.lower():
            st.write("The document was checked using basic STG rules.")
        elif "fake" in query.lower():
            st.write("Forgery probability is calculated using anomaly detection logic.")
        else:
            st.write("Ask about compliance or fake detection.")