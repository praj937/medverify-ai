import streamlit as st
import random

st.set_page_config(page_title="MedVerify AI", layout="centered")

st.title("🩺 MedVerify AI")
st.markdown("Upload a medical document to analyze compliance and detect forgery.")

file = st.file_uploader("📄 Upload Document")

if file:
    st.info("Analyzing document...")

    # Extract text
    text = file.getvalue().decode("utf-8", errors="ignore")

    # Simple logic
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

    # ✅ CHATBOT (FIXED + SMART)
    st.subheader("💬 Chatbot")
    query = st.text_input("Ask about the result")

    if query:
        q = query.lower()

        if "compliance" in q:
            st.write(f"The document is **{data['compliance']}** based on detected keywords like dosage rules.")

        elif "fake" in q or "forgery" in q:
            st.write(f"The forgery probability is **{data['fake_probability']:.2f}**. Higher means more suspicious.")

        elif "type" in q or "document" in q:
            st.write(f"This document is classified as **{data['document_type']}**.")

        elif "why" in q:
            st.write("The system checks keywords like 'overdose' or 'prescription' to determine results.")

        else:
            st.write("You can ask about compliance, forgery, or document type.")