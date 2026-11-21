# SWE-RL-Harness 🛠️⚡

> **Reproducible Reinforcement Learning Environments & Deterministic Verification Engine for Evaluating Frontier Coding LLMs & SWE Agents.**

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)
[![Docker](https://img.shields.io/badge/Docker-Hermetic%20Sandboxes-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Verification](https://img.shields.io/badge/Verifiers-Deterministic%20AST-brightgreen.svg)]()

---

## Overview

`SWE-RL-Harness` is a production-grade benchmark and evaluation harness designed to test autonomous AI software engineering agents and RL-trained models on real-world engineering tasks extracted from production repositories.

Unlike synthetic toy benchmarks, `SWE-RL-Harness` focuses on **non-trivial engineering challenges**:
1. **Subtle Multi-File Bugs:** Race conditions, off-by-one pointer arithmetic, memory leaks, cache incoherency.
2. **Feature Implementation:** Non-trivial features requiring adherence to established API contracts and architectural patterns.
3. **Legacy Codebase Refactoring:** Modernizing synchronous blockers to async I/O and non-blocking queues.
4. **Performance Optimization:** Critical path algorithmic improvements and memory footprint reduction.

```
+---------------------------------------------------------------------------------------+
|                                    SWE-RL-Harness                                    |
+---------------------------------------------------------------------------------------+
|  [Agent / Frontier LLM]                                                               |
|        |                                                                              |
|        v  (Git Patch / Solution Diff)                                                 |
|  +---------------------------------------------------------------------------------+  |
|  | 1. AST Anti-Cheat Scanner                                                       |  |
|  |    - AST mutation analysis & hardcoded-constant detection                       |  |
|  |    - Monkey-patching and mock-injection rejection                               |  |
|  +---------------------------------------------------------------------------------+  |
|        | Pass                                                                         |
|        v                                                                              |
|  +---------------------------------------------------------------------------------+  |
|  | 2. Hermetic Sandbox Orchestration (Docker / Linux cgroups)                       |  |
|  |    - Sub-2s ephemeral container provisioning                                     |  |
|  |    - Hermetic network isolation & pinned dependency baseline                     |  |
|  +---------------------------------------------------------------------------------+  |
|        | Execute                                                                      |
|        v                                                                              |
|  +---------------------------------------------------------------------------------+  |
|  | 3. Deterministic Verifier Engine                                                |  |
|  |    - Clean build & compilation verification (Python, Rust, Java, TypeScript, C++)|  |
|  |    - Fails-Without-Patch & Passes-With-Patch matrix verification                 |  |
|  |    - Property-based testing & stress benchmarks                                  |  |
|  +---------------------------------------------------------------------------------+  |
|        |                                                                              |
|        v                                                                              |
|  [Deterministic Reward Metric: Binary Success, Latency Delta, Flakiness Score]       |
+---------------------------------------------------------------------------------------+
```

---

## Key Features

- **Hermetic Sandbox Isolation:** Sub-2 second spin-up of containerized runtime environments with isolated filesystems and resource bounds (CPU, memory, wall-clock timeout) using Docker and Linux cgroups.
- **Deterministic Verifiers:** Dual-phase verifiers ensuring:
  1. Fail-to-Pass (F2P): Tests fail on base repository without the patch.
  2. Pass-to-Pass (P2P): Non-target regression tests remain green.
- **Anti-Cheat & AST Inspection:** Automatically inspects candidate ASTs to prevent shortcut hacks, such as hardcoded returns, pytest fixture overrides, or test assertion modifications.
- **Polyglot Repositories:** Full support for Python3, Java, Rust, TypeScript, and C++.
- **Ambiguity & Flakiness Guardrails:** Runs tests across multiple randomized seeds and resource constraints to flag unstable tasks before ingestion into the RL pipeline.

---

## Directory Structure

```
SWE-RL-Harness/
├── harness/
│   ├── __init__.py
│   ├── environment.py       # Ephemeral container lifecycle & cgroup management
│   ├── verifier.py          # Deterministic test runner & patch validator
│   ├── anti_cheat.py        # AST inspection for cheating heuristics
│   └── runner.py            # CLI entrypoint for batch evaluation runs
├── tasks/                   # Production-grade task definitions
│   ├── task_001_fastapi_race_condition.json
│   └── task_002_rust_channel_deadlock.json
├── tests/
│   └── test_verifier.py     # Self-eval unit tests
├── Dockerfile               # Multi-stage hermetic verification base image
├── pyproject.toml
└── requirements.txt
```

---

## Quickstart

### 1. Installation
```bash
git clone https://github.com/Rushild25/SWE-RL-Harness.git
cd SWE-RL-Harness
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Verify a Solution Patch
```bash
python -m harness.runner \
    --task-id task_001_fastapi_race_condition \
    --patch-file sample_patch.diff \
    --timeout 60
```

### 3. Output Schema
```json
{
  "task_id": "task_001_fastapi_race_condition",
  "status": "RESOLVED",
  "ast_checks": {
    "cheating_detected": false,
    "mutations_verified": true
  },
  "verification": {
    "fail_to_pass_passed": 4,
    "pass_to_pass_passed": 42,
    "regressions": 0
  },
  "metrics": {
    "execution_time_sec": 4.12,
    "memory_peak_mb": 118.4
  }
}
```

---

## License

This project is licensed under the [MIT License](LICENSE).
