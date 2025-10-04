import json
from messyJSON_to_structuredJSON import MilitaryTextEncoder, ReportType


def run_tests():
    encoder = MilitaryTextEncoder()

    # --- Test 1: Free text message (should be handled by regex/rules) ---
    free_text = """ID:A123 Alpha Squad and Bravo Team need to hold position ASAP
    at coords 123.456, 789.012! HIGH priority - execute at 0800Z tomorrow.
    Call Sign: EAGLE1. MissionID: OP45. Objective: Hold bridgehead."""

    print("\n--- Test 1: Free Text Input (Regex Path) ---")
    result1 = encoder.process_and_save_all(free_text, ReportType.EOINCREP)
    print(json.dumps(result1["structured"], indent=2))

    # --- Test 2: Messy/ambiguous input (should trigger LLM fallback) ---
    messy_text = """Bravo guys somewhere near the river, urgent situation, 
    extraction needed quickly, bring medics. Code red."""

    print("\n--- Test 2: Messy Text Input (LLM Fallback Path) ---")
    result2 = encoder.process_and_save_all(messy_text, ReportType.CASEVAC)
    print(json.dumps(result2["structured"], indent=2))


if __name__ == "__main__":
    run_tests()
