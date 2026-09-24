## Startup Rules

Before writing any code, complete these steps in order:

1. **Read this file completely.** It defines the boundaries and conventions for this project.
2. **Read `docs/ARCHITECTURE.md`** to understand the {{application_name}} layer structure.
3. **Read `docs/PRODUCT.md`** to understand the feature requirements.
4. **Read `docs/RELIABILITY.md`** to understand logging, observability, and clean state requirements.
5. **Run `bash init.sh`** to verify the project builds cleanly. If it fails, fix build errors before proceeding.
6. **Read `feature_list.json`** to see the current state of the features.

## Docs Hierarchy

the `docs/` directory is organized for agent readability:

```
docs/
    ARCHITECTURE.md -- {{application_name}} layer, data flow, full pipeline
    PRODUCT.md      -- Feature requirements and user facing behavior
    RELIABILITY     -- Logging, observability, clean state, benmarking
```

When adding new features, update the relevant doc before writing code.

## Electron Layer Boundaries (example)
This project has four strict layers. Code must respect these boundaries.

### Main Process (`src/main/`)
- Owns the `BrowserWindow` lifecycle and IPC registration.
- Imports services but never renderer code.
- All filesystem access happens here via services.

### Preload (`src/preload/`)
- The ONLY bridge between main and renderer.
- Uses `contextBridge.exposeInMainWorld` to expose typed APIs.
- Never imports React or renderer code.

### Renderer (`src/renderer/`)
- React + TypeScript UI layer.
- Communicates with main process exclusively through `window.knowledgeBase` API.
- Never imports Node.js modules (`fs`, `path`, `electron`).
- Uses the type declarations in `types.d.ts`.

### Services (`src/services/`)
- Pure TypeScript business logic running in the main process.
- Services may import from `src/shared/` but never from `src/renderer/`.
- Each service receives `PersistenceService` via constructor injection.

## Conventions:
- Type hints everywhere; `mypy` must pass. No `Any` without a comment explaining why.
- Logging via module-level loggers: `logger = logging.getLogger(__name__)`.
- INFO for significant event(user registered, order shipped).
- WARNING for missing but non-critical data (option config absent, fallback value used).
- ERROR for failures. Inside `except` blocks, use `logger.exception(...)` so the traceback is captured.
- Logging is configured once in `src/main.py` - never call `basicConfig` in domain modules.

## Definition of Done
A feature is "done" when all of the following are true:

1. Python comples without errors.
2. The app lauches and the window is visible
3. The feature appears in `feature_ list.json` with status `"pass"` and evidence
4. The code respects {{application_name}} boundaries defined above
5. No console erros during normal operation
6. Structured loggng covers all service operations
7. `docs/ARCHITECTURE.md` and/or `docs/PRODUCT.md` are updated
8. `clean-state-checklist.md` passes all checks.

## Working with the Feature List
The `feature_list.json` file is the source of truth for project progress:
- Each feature has a `status`: `"pass"`, `"fail"`, `"not-started"`.
- When implementing a feature, update its status to `"pass"` with evidence
- If a feature is blocked, set status to `"fail"` with a reason
- Never delete features from the list.

## Session Handoff
When resuming work, read `session-handoff.md` for context from a previous session. When finishing a session, update it with:

- What was accomplished
- What remains
- Any blockers or decisions made
- File that were modified
- Benchmark results if applicable

## Clean state
Before each major testing cycle:

1. Run `bash scripts/cleanup-scanner.sh` to check for stale artifacts
2. Verify `clean-state-checklist.md` passes
3. RUn `bash scripts/benchmark.sh` to measure performance