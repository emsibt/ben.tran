# Clean State Checklist

Run this checklist before commiting and at the end of the session.

## Build

- [ ] `pip install -e .` completes successfully
- [ ] `pytest tests/` passes with no errors
- [ ] `ruff check .` to makes sure no warnings about unused variables or imports

## Architecture

- [ ]
- [ ]

## Runtime

- [ ] Application starts without errors (`python -m <> / uvicorn app.main:app --reload`)
- [ ] Structured JSON log output appears in console at startup
- [ ] ...

## Logging

- [ ] All log entries are valid JSON (parseable)
- [ ] Log entries include timestamp, level, service and message
- [ ] ...

## Data Integrity

- [ ] Clean state reset removes all data files
- [ ] ...

## Performance

- [ ] `bash scripts/benchmark.sh` runs without errors

## Repository

- [ ] No unintended files in git status
- [ ] No sensitive data (.env, credentials) staged
- [ ] `claude-progress.md` updated with current state
- [ ] `feature_list.json` reflects actual feature status
- [ ] `session-handoff.md` updated if session is ending

## Scripts

- [ ] `bash scripts/cleanup-scanner.sh` reports no stale artifacts
- [ ] `bash scripts/benchmark.sh` completes the full task suite
- [ ] `bash init.sh` passes all verification steps

