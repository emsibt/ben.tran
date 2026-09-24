# Reliability -- Observability, Clean State, and Benchmarking

## Structured Logging

### Overview

All services in the application emit structured JSON log entries. This enables runtime debugging, post-hoc analysis, and automated monitoring of application behavior.

### Log Format

Every log entry is a single-line JSON object (`need to update the data to match with the application`):

```json
{
  "timestamp": "2026-03-30T12:00:00.000Z",
  "level": "INFO",
  "service": "document-service",
  "message": "Document imported successfully",
  "data": {
    "documentId": "abc-123",
    "filename": "design-notes.md",
    "sizeBytes": 2048
  }
}
```

### Log Levels

| Level | When to Use | Example |
|-------|-------------|---------|
| DEBUG | Routine data access, file reads | "Retrieved chunks for document" |
| INFO | Significant events | "Document imported", "Batch indexing complete" |
| WARNING | Missing but non-critical data | "Content not found for document" |
| ERROR | Failures | "File not found during import" |

### Service Logging Points

**{{service_name}}**
- Logic 1
- Logic 2
- Logic 3

...

### Configuring Log Level

Set the `LOG_LEVEL` environment variable:
```bash
LOG_LEVEL=INFO python -m <>  # Only INFO, WARNING, ERROR
LOG_LEVEL=WARNING python -m <>  # Only WARNING and ERROR
LOG_LEVEL=ERROR python -m <> # Only ERROR
```

Default: `DEBUG` (all messages).

## Clean State Management

### Purpose

Clean state management ensures that testing and benmarking start from a know, empty state. This prevents accumulated data from affecting test results or causing unexpected behavior.

### Reset Machanism

The application provides a `RESET_DATA` IPC channel that:
1. Removes the entire data directory (`knowledge-base-data/`)
2. Recreates the directory structure
3. Returns a successs response
4. The renderer clears all React state and refreshes

### When to Use Clean State

- Before running benmarks
- After a debugging session
- Befor testing a new feature
- When the data directory becomes corrupted

### Clean State Verification

Use the `clean-state-checklist.md` to verify:
- Build passes without errors
- Architecture boundaries are respected
- Runtime behavior is correct
- Logging output is as expected
- Data integrity is maintained