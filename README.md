# Dynamo — Fix the Broken Terminal-Bench Task

## Overview

This repository contains a **repaired Terminal-Bench 2 (Harbor)** task called `log-report`. The original task was intentionally broken across multiple axes. All defects have been identified and fixed to comply with Harbor's strict authoring standards.

The underlying task is simple: **parse an Apache-style access log and produce a JSON summary report**.

---

## Defects Found & Fixed

### 1. Format (`task.toml`)
| Before | After |
|--------|-------|
| `artifacts = "/app/out.json"` (string, wrong path) | `artifacts = ["/app/report.json"]` (array, correct path) |

### 2. Environment (`Dockerfile`)
| Before | After |
|--------|-------|
| `FROM python:latest` (unpinned) | `FROM python:3.12-slim@sha256:...` (pinned by digest) |
| `COPY solution_hint.py` (leaked solution) | Removed — no solution in agent image |

### 3. Instruction (`instruction.md`)
| Before | After |
|--------|-------|
| Vague, conversational prompt | Clear instructions with 5 numbered success criteria matching the verifier |

### 4. Verifier (`tests/test_outputs.py` & `tests/test.sh`)
| Before | After |
|--------|-------|
| Only checked file exists + non-empty (gameable) | Validates JSON structure and exact values (`total_requests=6`, `unique_ips=3`, `top_path=/index.html`) |
| Reward written to `/app/reward.txt` | Reward written to `/logs/verifier/reward.txt` |
| No CTRF output | Generates `/logs/verifier/ctrf.json` via `--ctrf` flag |
| Broken exit-code logic with `set -euo pipefail` | Proper exit-code capture with `&& result=0 \|\| result=$?` |

---

## Task Structure

```
log-report/
├── task.toml                 # Task configuration (Harbor TOML)
├── instruction.md            # Agent instructions with numbered success criteria
├── environment/
│   ├── Dockerfile            # Reproducible agent environment (pinned image)
│   ├── access.log            # Input data (6 Apache-style log entries)
│   └── solution_hint.py      # (present in context but NOT copied to image)
├── solution/
│   ├── solve.py              # Reference oracle solution
│   └── solve.sh              # Shell wrapper
└── tests/
    ├── test.sh               # Verifier entry point
    └── test_outputs.py       # 5 pytest tests (1:1 with instruction criteria)
```

---

## Expected Results

### Oracle Run (`harbor run -p log-report -a oracle`)
- **reward.txt**: `1`
- **ctrf.json**: 5 passed, 0 failed

### No-Op Run (`harbor run -p log-report --agent nop`)
- **reward.txt**: `0`
- **ctrf.json**: 0 passed, 5 failed

---

## Correct Output (`/app/report.json`)

```json
{
  "total_requests": 6,
  "unique_ips": 3,
  "top_path": "/index.html"
}
```

---

> **Note**: Please make this repo private after passing the assessment.
