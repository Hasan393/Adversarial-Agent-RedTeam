def verify_patch(model, patched_code, report):
    prompt = f"Does this code perfectly resolve the issue in the report while maintaining the original function signatures?\nCode:\n{patched_code}\nReport:\n{report}\nReturn exactly 'VERIFIED' or 'FAILED'."
    response = model.generate_content(prompt)
    return response.text.strip()