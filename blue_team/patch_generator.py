def generate_patch(model, code, report):
    prompt = f"Fix this code based on the vulnerability report. Use modern security practices (e.g., parameterized queries).\nCode:\n{code}\nReport:\n{report}\nReturn ONLY valid, raw Python code."
    response = model.generate_content(prompt)
    return response.text.strip().replace("```python", "").replace("```", "").strip()