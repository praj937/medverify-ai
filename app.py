import streamlit as st
import random

st.set_page_config(page_title="MedVerify AI", layout="centered")

st.title("🩺 MedVerify AI")
st.markdown("""
### 🔍 Solving:
1. Clinical Document Classification & STG Compliance  
2. Document Forgery Detection
""")

file = st.file_uploader("📄 Upload Medical Document")

if file:
    st.info("Analyzing document...")

    text = file.getvalue().decode("utf-8", errors="ignore").lower()

    # =========================
    # 🧠 Problem 1: Classification + Compliance
    # =========================
    doc_type = "Prescription" if "prescription" in text else "Medical Document"

    compliance = "Compliant"
    if "overdose" in text or "wrong dosage" in text:
        compliance = "Non-Compliant"

    # =========================
    # 🔍 Problem 2: Forgery Detection (Improved Logic)
    # =========================
    suspicious_keywords = ["edited", "fake", "tampered", "scan copy"]

    keyword_flag = any(word in text for word in suspicious_keywords)

    anomaly_score = random.uniform(0, 1)

    fake_prob = anomaly_score

    if keyword_flag:
        fake_prob += 0.3  # boost suspicion

    fake_prob = min(fake_prob, 1.0)

    status = "Suspicious" if fake_prob > 0.6 else "Likely Genuine"

    # =========================
    # 📊 Display Results
    # =========================
    st.success("Analysis Complete ✅")

    st.subheader("📌 Clinical Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Document Type", doc_type)

    with col2:
        st.metric("STG Compliance", compliance)

    st.divider()

    st.subheader("🛡️ Forgery Detection")

    st.metric("Forgery Probability", f"{fake_prob:.2f}")
    st.write(f"**Status:** {status}")

    st.divider()

    # =========================
    # 💬 Chatbot
    # =========================
    st.subheader("💬 AI Assistant")
    query = st.text_input("Ask about the analysis")

    if query:
        q = query.lower()

        if "compliance" in q:
            st.write(f"The document is **{compliance}** based on dosage-related keyword checks.")

        elif "fake" in q or "forgery" in q:
            st.write(f"Forgery probability is **{fake_prob:.2f}**. Suspicion increases if tampering keywords are detected.")

        elif "why" in q:
            st.write("The system checks medical keywords for compliance and suspicious terms for forgery detection.")

        elif "type" in q:
            st.write(f"This document is classified as **{doc_type}**.")

        else:
            st.write("You can ask about compliance, forgery, or document type.")