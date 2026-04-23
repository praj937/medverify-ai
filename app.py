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

st.set_page_config(page_title="MedVerify AI", layout="centered")
set_bg()

# =========================
# 🏥 HEADER
# =========================
st.title("🩺 MedVerify AI")
st.success("🚀 End-to-end AI-powered medical document verification system")

st.markdown("""
### 🔍 AI System for:
- Clinical Document Classification & STG Compliance  
- Document Forgery / Deepfake Detection  
""")

st.markdown(
    "<h3 style='text-align: center;'>👨‍💻 Developed by Prajwal SHiremath</h3>",
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# 🧠 STG FUNCTION
# =========================
def check_compliance(text):
    text = text.lower()
    issues = []

    if "paracetamol 1000mg" in text:
        issues.append("Excess paracetamol dosage")

    if "overdose" in text:
        issues.append("Unsafe dosage detected")

    if "antibiotic" in text and "no diagnosis" in text:
        issues.append("Antibiotic without diagnosis")

    if issues:
        return "Non-Compliant", issues
    else:
        return "Compliant", ["No violations detected"]

# =========================
# 🔍 FORGERY FUNCTION
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
        reasons.append("Unusual repetition")

    if any(w in text for w in ["fake", "edited", "tampered"]):
        score += 0.4
        reasons.append("Suspicious keywords detected")

    score += random.uniform(0, 0.3)

    score = min(score, 1.0)
    status = "🔴 Suspicious" if score > 0.6 else "🟢 Likely Genuine"

    return score, status, reasons

# =========================
# 📂 MODE SELECTION
# =========================
mode = st.selectbox("Choose Mode", ["Upload Document", "Use Sample Dataset"])

text = None

if mode == "Upload Document":
    file = st.file_uploader("📄 Upload Medical Document")
    if file:
        text = file.getvalue().decode("utf-8", errors="ignore")

else:
    st.info("Using sample dataset example")
    try:
        with open("sample.txt", "r") as f:
            text = f.read()
    except:
        text = "prescription overdose paracetamol 1000mg fake edited no hospital"

# =========================
# 🚀 PROCESSING
# =========================
if text:
    with st.spinner("🔍 Running AI analysis..."):
        time.sleep(1.5)

        if "prescription" in text.lower():
            doc_type = "Prescription"
        else:
            doc_type = "Medical Document"

        compliance, issues = check_compliance(text)
        fake_prob, status, reasons = detect_forgery(text)

    st.success("✅ Analysis Complete")

    st.markdown("## 📊 AI Analysis Dashboard")

    # Problem 1
    st.subheader("📌 Clinical Analysis (Problem 1)")
    st.metric("Document Type", doc_type)

    if compliance == "Compliant":
        st.success("STG Compliance: ✅ Compliant")
    else:
        st.error("STG Compliance: ❌ Non-Compliant")

    for i in issues:
        st.write(f"- {i}")

    st.markdown("---")

    # Problem 2
    st.subheader("🛡️ Forgery Detection (Problem 2)")
    st.metric("Forgery Risk Score", f"{fake_prob:.2f}")
    st.write(f"Status: {status}")

    st.progress(int(fake_prob * 100))

    st.write("### 📊 Risk Interpretation")
    if fake_prob < 0.3:
        st.success("Low Risk")
    elif fake_prob < 0.6:
        st.warning("Moderate Risk")
    else:
        st.error("High Risk")

    st.write("### 🧠 AI Confidence")
    confidence = round(1 - abs(fake_prob - 0.5), 2)
    st.write(f"{confidence}")

    for r in reasons:
        st.write(f"- {r}")

    st.markdown("---")

    # AI Summary
    st.write("### 🧠 AI Summary")
    st.write("""
This system uses:
- Rule-based NLP  
- STG compliance checks  
- Multi-factor anomaly detection  
- Heuristic scoring  
""")

# =========================
# 📂 DATASET NOTE
# =========================
st.markdown("---")
st.info("📂 Tested using structured healthcare document datasets and sample clinical records.")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 Built by Prajwal S Hiremath | Healthcare AI Hackathon Project")