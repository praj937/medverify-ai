import random

def detect_forgery(text):
    text = text.lower()

    suspicion = 0
    reasons = []

    if "hospital" not in text:
        suspicion += 0.2
        reasons.append("Missing hospital info")

    if "doctor" not in text:
        suspicion += 0.2
        reasons.append("Missing doctor name")

    if text.count("doctor") > 5:
        suspicion += 0.2
        reasons.append("Unusual repetition")

    if any(word in text for word in ["fake", "edited", "tampered"]):
        suspicion += 0.4
        reasons.append("Suspicious keywords detected")

    suspicion += random.uniform(0, 0.3)

    score = min(suspicion, 1.0)
    status = "Suspicious" if score > 0.6 else "Likely Genuine"

    return score, status, reasons