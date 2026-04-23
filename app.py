import streamlit as st
from utils.stg_rules import check_compliance
from utils.forgery_rules import detect_forgery
import base64
import time

# =========================
# 🎨 BACKGROUND + GLASS UI
# =========================
def set_bg():
    with open("background.png", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            background: rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(12px);
            padding: 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.3);
        }}

        h1, h2, h3 {{
            color: #0b3c5d;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# =========================
# ⚙️ PAGE CONFIG
# =========================
st.set_page_config(page_title="MedVerify AI", layout="centered")

set_bg()

# =========================
# 🏥 HEADER
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
    # ⏳ Animated loading
    with st.spinner("Analyzing document..."):
        time.sleep(1.5)

        text = file.getvalue().decode("utf-8", errors="ignore")

        # =========================
        # 🧠 DOCUMENT CLASSIFICATION
        # =========================
        if "prescription" in text.lower():
            doc_type = "Prescription"
        elif "discharge" in text.lower():
            doc_type = "Discharge Summary"
        else:
            doc_type = "Medical Document"

        # =========================
        # 🧠 STG COMPLIANCE
        # =========================
        compliance, reason = check_compliance(text)

        # =========================
        # 🔍 FORGERY DETECTION
        # =========================
        fake_prob, status, reasons = detect_forgery(text)

    st.success("Analysis Complete ✅")

    # =========================
    # 📊 CLINICAL SECTION
    # =========================
    st.subheader("📌 Clinical Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Document Type", doc_type)

    with col2:
        if compliance == "Compliant":
            st.success("STG Compliance: ✅ Compliant")
        else:
            st.error("STG Compliance: ❌ Non-Compliant")

    st.caption(f"Reason: {reason}")

    st.markdown("---")

    # =========================
    # 🛡️ FORGERY SECTION
    # =========================
    st.subheader("🛡️ Forgery Detection")

    st.metric("Forgery Probability", f"{fake_prob:.2f}")
    st.write(f"**Status:** {status}")

    # 📊 Progress bar
    st.progress(int(fake_prob * 100))

    if reasons:
        st.write("### 🔍 Detected Issues:")
        for r in reasons:
            st.write(f"- {r}")
    else:
        st.write("No major issues detected")

    st.markdown("---")

    # =========================
    # 💬 CHATBOT
    # =========================
    st.subheader("💬 AI Assistant")
    query = st.text_input("Ask about the analysis")

    if query:
        q = query.lower()

        if "compliance" in q:
            st.write(f"The document is **{compliance}** because {reason}.")

        elif "fake" in q or "forgery" in q:
            st.write(f"Forgery probability is **{fake_prob:.2f}**. Status: {status}.")

        elif "why" in q:
            st.write("The system checks dosage rules, missing fields, repetition patterns, and suspicious keywords.")

        elif "type" in q:
            st.write(f"This document is classified as **{doc_type}**.")

        else:
            st.write("You can ask about compliance, forgery detection, or document type.")

# =========================
# 🏁 FOOTER
# =========================
st.markdown("---")
st.caption("Built for Healthcare AI Hackathon 🚀")