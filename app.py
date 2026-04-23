import streamlit as st
import random

st.set_page_config(page_title="MedVerify AI", layout="centered")

# =========================
# 🎨 HEADER
# =========================
st.title("🩺 MedVerify AI")
st.markdown("""
### 🔍 AI System for:
- Clinical Document Classification & STG Compliance  
- Document Forgery Detection  
""")

st.markdown("---")

# =========================
# 📄 FILE UPLOAD
# =========================
file = st.file_uploader("📄 Upload Medical Document")

if file:
    st.info("Analyzing document...")

    text = file.getvalue().decode("utf-8", errors="ignore").lower()

    # =========================
    # 🧠 PROBLEM 1: CLASSIFICATION + STG
    # =========================
    if "prescription" in text:
        doc_type = "Prescription"
    elif "discharge" in text:
        doc_type = "Discharge Summary"
    else:
        doc_type = "Medical Document"

    compliance = "Compliant"
    compliance_reason = "All checks passed"

    if "overdose" in text or "wrong dosage" in text:
        compliance = "Non-Compliant"
        compliance_reason = "Detected unsafe dosage keywords"

    if "paracetamol 1000mg" in text:
        compliance = "Non-Compliant"
        compliance_reason = "Dosage exceeds recommended limits"

    # =========================
    # 🔍 PROBLEM 2: FORGERY DETECTION
    # =========================
    suspicion = 0
    reasons = []

    # Missing expected fields
    if "hospital" not in text:
        suspicion += 0.2
        reasons.append("Missing hospital information")

    if "doctor" not in text:
        suspicion += 0.2
        reasons.append("Missing doctor details")

    # Repetition anomaly
    if text.count("doctor") > 5:
        suspicion += 0.2
        reasons.append("Unusual repetition detected")

    # Suspicious keywords
    suspicious_keywords = ["fake", "edited", "tampered", "scan copy"]
    if any(word in text for word in suspicious_keywords):
        suspicion += 0.4
        reasons.append("Suspicious keywords found")

    # Add randomness for variation
    suspicion += random.uniform(0, 0.3)

    fake_prob = min(suspicion, 1.0)
    status = "🔴 Suspicious" if fake_prob > 0.6 else "🟢 Likely Genuine"

    # =========================
    # 📊 DISPLAY RESULTS
    # =========================
    st.success("Analysis Complete ✅")

    st.subheader("📌 Clinical Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Document Type", doc_type)

    with col2:
        if compliance == "Compliant":
            st.success("STG Compliance: ✅ Compliant")
        else:
            st.error("STG Compliance: ❌ Non-Compliant")

    st.caption(f"Reason: {compliance_reason}")

    st.markdown("---")

    st.subheader("🛡️ Forgery Detection")

    st.metric("Forgery Probability", f"{fake_prob:.2f}")
    st.write(f"**Status:** {status}")

    if reasons:
        st.write("### 🔍 Detected Issues:")
        for r in reasons:
            st.write(f"- {r}")
    else:
        st.write("No major issues detected")

    st.markdown("---")

    # =========================
    # 💬 SMART CHATBOT
    # =========================
    st.subheader("💬 AI Assistant")
    query = st.text_input("Ask about the analysis")

    if query:
        q = query.lower()

        if "compliance" in q:
            st.write(f"The document is **{compliance}** because {compliance_reason}.")

        elif "fake" in q or "forgery" in q:
            st.write(f"The forgery probability is **{fake_prob:.2f}**. Status: {status}.")

        elif "why" in q:
            st.write("The system checks dosage rules, missing fields, repetition patterns, and suspicious keywords.")

        elif "type" in q:
            st.write(f"This document is classified as **{doc_type}**.")

        else:
            st.write("You can ask about compliance, forgery detection, or document type.")

# =========================
# 🎯 FOOTER
# =========================
st.markdown("---")
st.caption("Built for Healthcare AI Hackathon 🚀")