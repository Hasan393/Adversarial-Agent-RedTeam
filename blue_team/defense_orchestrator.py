from .patch_generator import generate_patch
from .verification_agent import verify_patch

def orchestrate_defense(model, code, report):
    patched_code = generate_patch(model, code, report)
    verification = verify_patch(model, patched_code, report)
    return patched_code, verification