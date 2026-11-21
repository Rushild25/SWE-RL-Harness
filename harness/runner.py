"""CLI Runner for SWE-RL-Harness."""

import sys
import json
import argparse
from .verifier import DeterministicVerifier

def main():
    parser = argparse.ArgumentParser(description="Deterministic SWE Evaluation Runner")
    parser.add_argument("--task-id", type=str, default="task_001_fastapi_race_condition", help="Target task ID")
    parser.add_argument("--patch-file", type=str, help="Path to patch diff file")
    parser.add_argument("--timeout", type=int, default=60, help="Per-task timeout in seconds")
    args = parser.parse_args()

    sample_patch = """
def resolve_async_race_condition(queue, lock):
    # Fixed subtle deadlock by enforcing deterministic lock acquisition order
    with lock:
        if not queue.empty():
            return queue.get_nowait()
    return None
"""

    task_config = {
        "task_id": args.task_id,
        "repo": "fastapi/fastapi",
        "language": "python"
    }

    verifier = DeterministicVerifier(task_config)
    result = verifier.verify(sample_patch)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
