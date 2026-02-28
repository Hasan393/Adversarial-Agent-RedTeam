def generate_report(exploit_result):
    if "EXPLOITED" in exploit_result.upper():
        return f"VULNERABILITY DETECTED\nDetails: {exploit_result}"
    return "NO VULNERABILITIES FOUND"