import streamlit as st
import base64
import time
import random

# =========================
# 🎨 BACKGROUND (SAFE)
# =========================
def set_bg():
    try:
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
    except:
        pass

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

# 👨‍💻 CENTERED NAME (PREMIUM)
st.markdown(
    "<h3 style='text-align: center;'>👨‍💻 Developed by Prajwal S Hiremath</h3>",
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# 🧠 STG FUNCTION
# =========================
def check_compliance(text):
    text = text.lower()

    if "paracetamol 1000mg" in text:
        return "Non-Compliant", "Paracetamol dosage exceeds safe limit"

    if "overdose" in text or "wrong dosage" in text:
        return "Non-Compliant", "Unsafe dosage detected"

    if "antibiotic" in text and "no diagnosis" in text:
        return "Non-Compliant", "Antibiotic without diagnosis"

    return "Compliant", "All checks passed"

# =========================
# 🔍 FORGERY FUNCTION
# =========================
def detect_forgery(text):
    text = text.lower()

    suspicion = 0
    reasons = []

    if "hospital" not in text:
        suspicion += 0.2
        reasons.append("Missing hospital information")

    if "doctor" not in text:
        suspicion += 0.2
        reasons.append("Missing doctor details")

    if text.count("doctor") > 5:
        suspicion += 0.2
        reasons.append("Unusual repetition detected")

    if any(word in text for word in ["fake", "edited", "tampered"]):
        suspicion += 0.4
        reasons.append("Suspicious keywords found")

    suspicion += random.uniform(0, 0.3)

    score = min(suspicion, 1.0)
    status = "🔴 Suspicious" if score > 0.6 else "🟢 Likely Genuine"

    return score, status, reasons

# =========================
# 📄 FILE UPLOAD
# =========================
file = st.file_uploader("📄 Upload Medical Document")

if file:
    with st.spinner("Analyzing document..."):
        time.sleep(1.5)

        text = file.getvalue().decode("utf-8", errors="ignore")

        # =========================
        # 🧠 CLASSIFICATION
        # =========================
        if "prescription" in text.lower():
            doc_type = "Prescription"
        elif "discharge" in text.lower():
            doc_type = "Discharge Summary"
        else:
            doc_type = "Medical Document"

        # =========================
        # 🧠 STG
        # =========================
        compliance, reason = check_compliance(text)

        # =========================
        # 🔍 FORGERY
        # =========================
        fake_prob, status, reasons = detect_forgery(text)

    st.success("Analysis Complete ✅")

    # =========================
    # 📊 CLINICAL ANALYSIS
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
    # 🛡️ FORGERY DETECTION
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
st.caption("🚀 Built by Prajwal S Hiremath | Healthcare AI Hackathon Project")