---
paths:
  - "frontend/**"
---

# Frontend rules

React and TypeScript rules for `frontend/`, on top of the root `AGENTS.md`.

- Call the backend only through the generated client in `src/client`
  (`listNotes()` and friends). Do not hand-write `fetch` calls or response
  types for the API.
- Never edit `src/client` by hand. Change the backend, then run
  `mise run client:generate`.
- Use relative URLs (`/api/v1/...`). Vite forwards them locally and nginx does
  the same when deployed, so the app never needs a backend hostname.
- Import from `src` with the `@/` alias: `import { App } from "@/App"`.
- No `any`, no `as` casts to silence the compiler, no non-null `!`. Fix the
  type instead.
- One component per file, named after the component.
- Handle the loading and error states of every API call, not just success.
