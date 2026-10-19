# Working with agents

Rules for anyone writing code in this repo, human or AI agent. Coding agents
(Claude Code, Codex, Cursor, Copilot) read this file automatically.
`CLAUDE.md` is a symlink to it.

This is a starting point. Add a rule when you catch yourself correcting the
same mistake twice.

Before changing `backend/`, read `.agents/rules/backend.md`. Before changing
`frontend/`, read `.agents/rules/frontend.md`.

## Before you change anything

- Read the code you are about to change, and the code that calls it.
- Make the smallest change that solves the problem.
- Follow the patterns already in the repo. If one looks wrong, ask before
  replacing it.

## Adding code and dependencies

- Do not add a dependency for something the standard library or an existing
  dependency already does. Say why when you add one.
- Do not add abstractions, config options or files the task does not need.
- Two similar blocks of code are fine. Extract a shared function on the third.

## Writing code

- Names carry the meaning. If a variable needs a comment to explain what it
  holds, rename it.
- Comments explain why, not what. Delete comments that restate the code.
- Use guard clauses and early returns instead of nested `if`s.
- Validate input once, where it enters the system (request bodies, query
  params). Trust it after that.
- Do not swallow errors. If you cannot handle one, let it surface.
- Delete code nothing uses, including commented-out code.

## Finishing

- Run `mise run check` and fix what it reports. It runs the same checks as CI.
- If you changed a route or a response schema, run `mise run client:generate`
  and commit the regenerated files.
- Say what you ran and what you did not.
