# Working in this repo

Rules for anyone changing code here, human or agent. Before editing `backend/` or
`frontend/`, also read the matching file in `.agents/rules/`.

## Before you start

- Read `README.md` and the code you are about to change.
- Make the smallest change that does the job. No extra abstractions, dependencies or
  config the task does not need.
- Follow the patterns already in the repo before inventing new ones.

## Writing code

- Clear names over comments. Only comment what a reader would otherwise get wrong.
- Guard clauses and early returns instead of nested `if`s.
- Keep functions short and focused on one thing.
- Delete dead code and commented-out code. Git remembers it.
- Validate untrusted input once, with pydantic, where it enters the system. Trust it
  after that.
- In the frontend, write modern TypeScript: arrow functions, `type` instead of
  `interface`, no `enum` or `namespace`.

## The database

The SQLAlchemy models in `backend/src/app/models/` are the source of truth for every
table. Change the database only this way:

1. Edit a model, or add one and import it in `models/__init__.py`.
2. Run `mise run db:dev:migrate:generate <name>`. It compares the models with the
   database and writes the SQL to a new file in `backend/migrations/`.
3. Read the generated SQL, then run `mise run db:dev:migrate:up`.
4. `mise run db:dev:migrate:status` shows whether the database is missing migrations.

Never write schema SQL by hand and never edit a migration that is already on `main`.
The only SQL you add to a migration is seed data.

## Queries

Every query must read as SQL. Use SQLAlchemy's `select()`, `insert()`, `update()` and
`delete()`, or `text()` with bound parameters, and run them on the session:

```python
rows = await session.scalars(
    select(models.Message).where(models.Message.id == message_id)
)
```

- Never use the ORM's object style: `session.query()`, `session.get()`,
  `session.add()`, `session.delete()` or lazy-loaded relationships.
- Never build SQL strings with f-strings or `%`. Pass values as parameters.

## The API contract

The routes and pydantic schemas are the source of truth for the API.
`backend/openapi.json` is generated from them and committed.
`frontend/src/api/generated/` is generated from that file and gitignored. Never edit
either by hand. After changing a route, run `mise run contract` and commit
`backend/openapi.json`.

## Finishing

- Run `mise run check` and fix everything it reports.
