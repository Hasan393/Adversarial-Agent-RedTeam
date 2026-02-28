import os
import google.generativeai as genai
from dotenv import load_dotenv
from red_team.probe_generator import generate_probes
from red_team.exploit_agent import attempt_exploit
from red_team.report_generator import generate_report
from blue_team.defense_orchestrator import orchestrate_defense

def log_battle(message):
    print(message)
    with open("battle_log.txt", "a") as f:
        f.write(message + "\n")

def main():
    open("battle_log.txt", "w").close()
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash')

    with open("target_code.py", "r") as f:
        code = f.read()

    log_battle("=====================================")
    log_battle("   🔥 ROUND 1: RED TEAM ATTACK 🔥   ")
    log_battle("=====================================")
    log_battle(f"\n[TARGET CODE]\n{code}\n")

    probes = generate_probes(model, code)
    log_battle(f"[RED TEAM - PROBE GENERATOR] Created Payloads:\n{probes}\n")

    exploit_result = attempt_exploit(model, code, probes)
    log_battle(f"[RED TEAM - EXPLOIT AGENT] Execution Result:\n{exploit_result}\n")

    report = generate_report(exploit_result)
    log_battle(f"[RED TEAM - REPORT GENERATOR] Final Verdict:\n{report}\n")

    if "VULNERABILITY DETECTED" in report:
        log_battle("=====================================")
        log_battle("  🛡️ ROUND 2: BLUE TEAM DEFENSE 🛡️  ")
        log_battle("=====================================")

        patched_code, verification = orchestrate_defense(model, code, report)
        
        log_battle(f"\n[BLUE TEAM - PATCH GENERATOR] Proposed Fix:\n{patched_code}\n")
        log_battle(f"[BLUE TEAM - VERIFICATION AGENT] Status: {verification}\n")

        if "VERIFIED" in verification.upper():
            with open("target_code.py", "w") as f:
                f.write(patched_code)
            log_battle("[SYSTEM] Vulnerability neutralized. Target code successfully overwritten.")
        else:
            log_battle("[SYSTEM] Patch failed verification constraints. Manual review required.")
    else:
        log_battle("[SYSTEM] Target system resilient. No patching required.")

if __name__ == "__main__":
    main()