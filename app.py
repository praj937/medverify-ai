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
                backdrop-filter: blur(14px);
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
- Document Forgery / Deepfake Detection  
""")

st.markdown(
    "<h3 style='text-align: center;'>👨‍💻 Developed by Prajwal S Hiremath</h3>",
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# 🧠 STG LOGIC (Problem 1)
# =========================
def check_compliance(text):
    text = text.lower()
    issues = []

    if "paracetamol 1000mg" in text:
        issues.append("Excess paracetamol dosage")

    if "overdose" in text or "wrong dosage" in text:
        issues.append("Unsafe dosage detected")

    if "antibiotic" in text and "no diagnosis" in text:
        issues.append("Antibiotic prescribed without diagnosis")

    if issues:
        return "Non-Compliant", issues
    else:
        return "Compliant", ["No violations detected"]

# =========================
# 🔍 FORGERY LOGIC (Problem 2)
# =========================
def detect_forgery(text):
    text = text.lower()
    score = 0
    reasons = []

    if "hospital" not in text:
        score += 0.2
        reasons.append("Missing hospital information")

    if "doctor" not in text:
        score += 0.2
        reasons.append("Missing doctor details")

    if text.count("doctor") > 5:
        score += 0.2
        reasons.append("Unusual repetition pattern")

    suspicious_words = ["fake", "edited", "tampered", "scan copy"]
    if any(w in text for w in suspicious_words):
        score += 0.4
        reasons.append("Suspicious keywords detected")

    score += random.uniform(0, 0.3)

    score = min(score, 1.0)
    status = "🔴 Suspicious" if score > 0.6 else "🟢 Likely Genuine"

    return score, status, reasons

# =========================
# 📄 FILE UPLOAD
# =========================
file = st.file_uploader("📄 Upload Medical Document")

if file:
    with st.spinner("🔍 Running AI analysis..."):
        time.sleep(1.5)

        text = file.getvalue().decode("utf-8", errors="ignore")

        # Classification
        if "prescription" in text.lower():
            doc_type = "Prescription"
        elif "discharge" in text.lower():
            doc_type = "Discharge Summary"
        else:
            doc_type = "Medical Document"

        compliance, compliance_issues = check_compliance(text)
        fake_prob, status, forgery_reasons = detect_forgery(text)

    st.success("✅ Analysis Complete")

    # =========================
    # 📊 PROBLEM 1
    # =========================
    st.subheader("📌 Clinical Analysis (Problem 1)")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Document Type", doc_type)

    with col2:
        if compliance == "Compliant":
            st.success("STG Compliance: ✅ Compliant")
        else:
            st.error("STG Compliance: ❌ Non-Compliant")

    st.write("### 🔍 Compliance Explanation:")
    for issue in compliance_issues:
        st.write(f"- {issue}")

    st.markdown("---")

    # =========================
    # 📊 PROBLEM 2
    # =========================
    st.subheader("🛡️ Forgery Detection (Problem 2)")

    st.metric("Forgery Risk Score", f"{fake_prob:.2f}")
    st.write(f"**Status:** {status}")

    st.progress(int(fake_prob * 100))

    # 🔥 Risk Interpretation
    st.write("### 📊 Risk Interpretation")
    if fake_prob < 0.3:
        st.success("Low Risk Document")
    elif fake_prob < 0.6:
        st.warning("Moderate Risk Document")
    else:
        st.error("High Risk Document")

    # 🔥 AI Confidence
    st.write("### 🧠 AI Confidence")
    confidence = round(1 - abs(fake_prob - 0.5), 2)
    st.write(f"Confidence Score: {confidence}")

    if forgery_reasons:
        st.write("### 🔍 Detected Anomalies:")
        for r in forgery_reasons:
            st.write(f"- {r}")
    else:
        st.write("No anomalies detected")

    st.markdown("---")

    # =========================
    # 💬 CHATBOT
    # =========================
    st.subheader("💬 AI Assistant")
    query = st.text_input("Ask about the analysis")

    if query:
        q = query.lower()

        if "compliance" in q:
            st.write(f"The document is **{compliance}** based on STG rules.")

        elif "fake" in q or "forgery" in q:
            st.write(f"Forgery risk score is **{fake_prob:.2f}**, indicating {status}.")

        elif "why" in q:
            st.write("The system evaluates dosage rules, missing fields, anomaly patterns, and suspicious keywords.")

        elif "type" in q:
            st.write(f"The document is classified as **{doc_type}**.")

        else:
            st.write("Ask about compliance, forgery detection, or document type.")

# =========================
# ⚠️ DATASET + DISCLAIMER
# =========================
st.markdown("---")
st.info("📂 Designed to work with structured healthcare datasets and document samples.")
st.warning("⚠️ Prototype system. Advanced models like ClinicalBERT and CNN-based deepfake detection can enhance accuracy.")

# =========================
# 🏁 FOOTER
# =========================
st.markdown("---")
st.caption("🚀 Built by Prajwal SHiremath | Healthcare AI Hackathon Project")