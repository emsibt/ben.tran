# Session Handoff

## 2026-09-17 (later) — document-chunking, metadata-extraction, indexing-status-ui, grounded-qa built and verified

### What was accomplished

All 11 features in `feature_list.json` now **pass**. The 4 new ones:

- **document-chunking** — already implemented (`IndexingService.chunkText`:
  blank-line split, merge toward 500 chars, oversized paragraph = own chunk) and
  tested; verified and evidenced, including an app-level run (scratch profile:
  3 sample documents → 14 chunks, restored from the persisted index on reboot).
- **metadata-extraction** — `lineCount` added to `DocumentMeta` and extracted at
  import (`countLines`: trailing newline does not open a new line).
  `DocumentDetail` shows words · lines · chars. Records written before the field
  existed recompute it in `toMeta` (legacy-profile test) — no migration needed.
- **indexing-status-ui** — new `src/renderer/components/StatusBar.tsx` along the
  bottom edge: status dot + label (`Indexing…` / `Indexed` / `No index`),
  document/chunk counts, build time, and a **Rebuild index** button wired to the
  previously UI-unused `indexing:rebuild` channel. App gained a `rebuilding`
  busy state; the old footer counts line was replaced.
- **grounded-qa** — retrieval/citations/confidence were already in place; the
  generic fallback answer now names the top-ranked chunk (per retrieval-plan.md
  "a generic response based on the most relevant citation") instead of a static
  sentence. Added a `[smoke] qa` probe: one real `qa:ask` round-trip at every
  smoke boot (log-only, does not affect exit code).

### Verification (all green, 2026-09-17)

- `npm run check` — strict tsc, main + renderer
- `npm test` — 21 tests passing (13 qa/indexing + 8 document service; new:
  lineCount assertions + legacy-record recompute test)
- `npm run smoke` — real profile: bridge OK, 1 doc/1 chunk, qa probe answered,
  0 console errors, exit 0
- Scratch-profile boot (`KB_DATA_DIR` + compiled-service seeder, deleted after):
  3 documents / 14 chunks, qa "How does chunking work?" → **confidence 0.85,
  2 citations** through the real IPC stack, 0 console errors

### Docs updated

- `feature_list.json` — 4 features → `pass` with evidence
- `docs/PRODUCT.md` — line counts in detail metadata; StatusBar replaces the
  footer counts; generic fallback names the top chunk
- `docs/ARCHITECTURE.md` — smoke now includes the qa round-trip; answering
  section describes the grounded generic fallback

### Decisions made

- Legacy records without `lineCount` are handled at read time (`lineCount ??
  countLines(content)`) rather than by rewriting stored JSON — the real profile
  keeps working untouched.
- The StatusBar sits at the very bottom (below the question bar, VS Code style);
  the redundant footer counts div and its `.stats` CSS rule were removed.
- Smoke's qa probe uses "How does chunking work?" and only logs the result: an
  empty/unaligned index legitimately answers 0.30/0 citations, which must not
  fail the smoke run.

### What remains

- All 11 listed features pass; no blockers.
- Next natural step (per repo pattern): a p02 project that swaps the mock Q&A
  for an LLM-backed service and compares against this baseline.

## 2026-09-17 — document-import, document-detail, basic-persistence built and verified

### What was accomplished

All three new features in `feature_list.json` now **pass**:

- **document-import** — extracted the sidebar import controls into
  `src/renderer/components/ImportPanel.tsx` (per the feature description). The
  dialog → import → index-rebuild pipeline was already in place and remains
  unchanged; evidence updated with the real end-to-end import found in the
  profile (~295 KB doc imported 2026-09-17 10:01 via the native dialog).
- **document-detail** — `DocumentViewer.tsx` replaced by
  `src/renderer/components/DocumentDetail.tsx`: full content over IPC
  (`documents:read`), full metadata line, and a **two-step delete button**
  (no blocking `window.confirm`). Delete is new end-to-end:
  `documents:delete` channel (shared/types) → IPC handler validates the id,
  calls `DocumentService.deleteDocument`, rebuilds the index (deleted chunks
  stop answering) and returns remaining docs + stats → preload
  `documents.delete(id)` → `App.handleDelete` updates list/stats and clears
  the selection when the open document is deleted.
- **basic-persistence** — storage was already correct (one JSON record per
  document under `<userData>/knowledge-base-data/documents/`, index at
  `index/chunks.json`, restored/rebuilt at startup). Added verification:
  - `src/services/documentService.test.ts` (7 tests): import metadata,
    extension/size rejection, list ordering, **cross-restart persistence**
    (fresh service instances over the same baseDir), delete → index
    consistency, invalid-id/double-delete errors. `npm test`: 20/20 green.
  - App-level restart proof via new `KB_DATA_DIR` env override in
    `main/index.ts`: seeded a scratch dir with one stored record, booted the
    app twice with `--smoke` — boot 1 exercised the rebuild path, boot 2 the
    index-restore path; both reported `1 document(s), 1 chunk(s)`,
    0 console errors, exit 0. Scratch dir deleted afterwards.

### Verification (all green, 2026-09-17)

- `npm run check` — strict tsc, main + renderer
- `npm test` — 20 tests passing (13 qa/indexing + 7 document service)
- `npm run smoke` — bridge OK, 0 renderer console errors, exit 0 (ran 3×)

### Docs updated

- `feature_list.json` — 3 features → `pass` with evidence
- `docs/PRODUCT.md` — detail/delete feature added; non-goals now "no editing"
- `docs/ARCHITECTURE.md` — documents namespace includes delete; `KB_DATA_DIR` documented

### Decisions made

- `tsconfig.json` migrated from deprecated `moduleResolution: "Node"` (node10,
  flagged as an error by newer TypeScript — removed in TS 7) to
  `module`/`moduleResolution: "NodeNext"` with explicit `.js` extensions on
  relative imports across main/preload/services. Emitted output stays
  CommonJS (package.json has no `"type"` field), so Electron behavior is
  unchanged; renderer keeps `moduleResolution: "Bundler"` with extensionless
  imports.
- Delete uses a two-step in-UI confirm instead of `window.confirm` (blocking
  sync dialog; poor fit in Electron).
- After a delete the whole index is rebuilt from stored records (simple,
  correct; baseline corpus is tiny). No incremental chunk removal.
- The content endpoint keeps the channel name `documents:read` (consistent
  with `documents:list`/`documents:import`); it fulfils the "getContent IPC"
  requirement. Component names match the feature descriptions exactly
  (`ImportPanel`, `DocumentDetail`).

### What remains / ideas for the next project

- All 7 listed features pass; no blockers.
- Next natural step (per repo pattern): a p02 project that swaps the mock Q&A
  for an LLM-backed service and compares against this baseline.
