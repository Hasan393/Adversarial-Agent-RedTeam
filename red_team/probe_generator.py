def generate_probes(model, code):
    prompt = f"Analyze this code and generate 3 malicious attack payloads. Return ONLY a Python list of strings.\n{code}"
    response = model.generate_content(prompt)
    try:
        return eval(response.text.strip().replace("```python", "").replace("```", ""))
    except:
        return [response.text.strip()]