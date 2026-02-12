import re

def check_legal_metrology(data):
    """
    Layer 1: Legal Metrology Compliance (Primary Check)
    Checks for mandatory government requirements.
    """
    mandatory_fields = [
        "net_quantity", 
        "mrp", 
        "manufacturer_details", 
        "batch_number", 
        "expiry_date", 
        "consumer_care_contact"
    ]
    
    missing_fields = [field for field in mandatory_fields if not data.get(field)]
    
    if missing_fields:
        return {"status": "Non-compliant", "missing": missing_fields, "score": 0}
    return {"status": "Compliant", "missing": [], "score": 50}

def check_claims(claims_text):
    """
    Layer 2: Claim Verification (Secondary Check)
    Detects Hard Rules (Illegal) and Soft Flags (Warnings).
    """
    issues = []
    score_deduction = 0
    
    # Hard Rules (Illegal -> Direct Fail)
    hard_rules = {
        r"FDA Approved": "False claim: FDA does not approve cosmetics.",
        r"100% Natural": "Misleading claim: '100%' is scientifically unverifiable.",
        r"Chemical-Free": "Misleading claim: Nothing is chemical-free.",
        r"Ayurvedic": "Ayurvedic/Herbal claims require AYUSH license." # Simplified check
    }

    # Soft Flags (Need Proof)
    soft_flags = {
        r"Vegan Certified": "Warning: Requires certificate proof.",
        r"Dermatologically Tested": "Warning: Requires lab report.",
        r"Clinically Proven": "Warning: Requires clinical trial data."
    }

    # Check Hard Rules
    for pattern, message in hard_rules.items():
        if re.search(pattern, claims_text, re.IGNORECASE):
            issues.append({"type": "HARD_FAIL", "message": message})
            score_deduction += 50

    # Check Soft Flags
    for pattern, message in soft_flags.items():
        if re.search(pattern, claims_text, re.IGNORECASE):
            issues.append({"type": "SOFT_WARNING", "message": message})
            score_deduction += 10

    return issues, score_deduction

def calculate_trust_score(data):
    """Generates the final Trust Score."""
    metrology_result = check_legal_metrology(data)
    
    # Base score comes from metrology
    score = metrology_result["score"]
    
    # Layer 2 Check
    claims_text = data.get("claims", "")
    claim_issues, deduction = check_claims(claims_text)
    
    # Final Calculation
    final_score = max(0, score + (50 - deduction)) # Max 100
    
    status = "VERIFIED"
    if final_score < 40:
        status = "FAIL"
    elif final_score < 80:
        status = "PARTIAL"

    return {
        "final_score": final_score,
        "status": status,
        "metrology_check": metrology_result,
        "claim_issues": claim_issues
    }
