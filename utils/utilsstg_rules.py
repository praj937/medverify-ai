def check_compliance(text):
    text = text.lower()

    if "paracetamol 1000mg" in text:
        return "Non-Compliant", "Paracetamol dosage exceeds safe limit"

    if "overdose" in text or "wrong dosage" in text:
        return "Non-Compliant", "Unsafe dosage detected"

    if "antibiotic" in text and "no diagnosis" in text:
        return "Non-Compliant", "Antibiotic prescribed without diagnosis"

    return "Compliant", "All checks passed"