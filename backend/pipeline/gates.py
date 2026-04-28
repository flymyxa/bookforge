def gate_result(stage_name: str, passed: bool) -> dict[str, str | bool]:
    return {
        "stage": stage_name,
        "passed": passed,
        "action": "resume" if passed else "pause",
    }
