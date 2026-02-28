# Adversarial-Agent-RedTeam

## Overview

This repository demonstrates an **adversarial red‑team / blue‑team workflow** using the
Google Gemini generative AI SDK. The goal is to simulate a semi‑automated
security assessment on a target Python codebase, detect vulnerabilities and
enforce automated patching. It is intended for educational and proof‑of‑concept
purposes and should not be used in production without significant modifications.


## Project Structure

```
adversarial_agent_redteam/
├── .env                 # environment variables (ignored by git)
├── requirements.txt     # Python dependencies
├── target_code.py       # sample vulnerable code under test
├── main.py              # orchestration script
├── red_team/            # components used to attack the target
│   ├── __init__.py
│   ├── probe_generator.py
│   ├── exploit_agent.py
│   └── report_generator.py
└── blue_team/           # components used to defend and patch
    ├── __init__.py
    ├── defense_orchestrator.py
    ├── patch_generator.py
    └── verification_agent.py
```


## Components

### Red Team

* `probe_generator.generate_probes` – asks the AI model to craft malicious
  payloads based on the provided source code.
* `exploit_agent.attempt_exploit` – simulates applying payloads to the code and
  reports whether any of them would cause a failure or breach (e.g., SQL
  injection).
* `report_generator.generate_report` – translates exploit results into a human‑
  readable vulnerability report.

### Blue Team

* `patch_generator.generate_patch` – instructs the AI model to rewrite the
  vulnerable code using secure practices (parameterized queries, input
  validation, etc.) based on the vulnerability report.
* `verification_agent.verify_patch` – asks the model to confirm whether the
  proposed patch resolves the issue while preserving function signatures.
* `defense_orchestrator.orchestrate_defense` – ties patch generation and
  verification together in a simple workflow.

### Target Code

`target_code.py` contains an intentionally insecure `authenticate_user`
function that builds SQL queries by concatenating user input. It serves as the
example application under test.


## Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hasan393/Adversarial-Agent-RedTeam.git
   cd Adversarial-Agent-RedTeam
   ```

2. **Install dependencies** (preferably in a virtual environment):
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   * Copy `.env.example` to `.env` and set your Gemini API key:
     ```
     cp .env.example .env
     # edit .env and replace the placeholder
     ```
   * Ensure `.gitignore` contains `.env` so keys are not committed.

4. **Run the simulation**:
   ```bash
   python main.py
   ```
   This will execute the red‑team attack, log each step to `battle_log.txt`, and
   if a vulnerability is found, run the blue‑team defense and optionally write
   the patched code back to `target_code.py`.


## Logging & Output

* `battle_log.txt` – generated on each run; contains a chronological record of
  probe generation, exploit attempts, reports, and defense actions.
* Standard output mirrors log entries for interactive visibility.


## Extending the Project

* Replace `target_code.py` with your own Python functions or modules to test
  different patterns.
* Improve red‑team logic by adding more sophisticated exploitation or static
  analysis techniques.
* Augment blue‑team modules to apply multiple patches, run unit tests, or
  integrate with CI pipelines.
* Swap out the underlying generative model by changing the `model =
  genai.GenerativeModel(...)` line in `main.py`.


## Security Considerations

> **Important:** the current proofs-of-concept rely on untrusted AI model
> outputs and perform unsafe operations (e.g. `eval()`) purely for expediency.
> Do **not** deploy this code in any environment handling sensitive or production
> data. The example code intentionally contains vulnerabilities and insecure
> patterns; treat it as educational only.


## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to fork and experiment – and always keep the blue team sharp!