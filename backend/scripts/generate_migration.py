"""Write a dbmate migration with the SQL that turns the database into what the
models in app.models describe.

Alembic's autogenerate does the comparison. Only the SQL it renders is kept,
so every migration is a plain .sql file with an up and a down section.

Usage: python scripts/generate_migration.py <name>
"""

import io
import sys
from datetime import UTC, datetime
from pathlib import Path

from alembic.autogenerate import produce_migrations
from alembic.operations import Operations
from alembic.operations.ops import MigrateOperation, OpContainer
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

from app.config.settings import settings
from app.models import Base

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations"


def render_sql(operation: MigrateOperation) -> str:
    output = io.StringIO()
    context = MigrationContext.configure(
        dialect_name="postgresql",
        opts={"as_sql": True, "output_buffer": output, "literal_binds": True},
    )
    operations = Operations(context)

    def run(op: MigrateOperation) -> None:
        if isinstance(op, OpContainer):
            for child in op.ops:
                run(child)
            return
        operations.invoke(op)

    run(operation)
    # SQLAlchemy leaves a space after each comma in CREATE TABLE.
    lines = [line.rstrip() for line in output.getvalue().strip().splitlines()]
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: generate_migration.py <name>")
    name = sys.argv[1]

    engine = create_engine(settings.database_url)
    with engine.connect() as connection:
        context = MigrationContext.configure(
            connection,
            # dbmate's bookkeeping table is not a model. Don't drop it.
            opts={"include_name": lambda n, kind, _: n != "schema_migrations"},
        )
        migration = produce_migrations(context, Base.metadata)

    if migration.upgrade_ops is None or migration.upgrade_ops.is_empty():
        sys.exit("The models already match the database. No migration created.")
    assert migration.downgrade_ops is not None

    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    path = MIGRATIONS_DIR / f"{timestamp}_{name}.sql"
    path.write_text(
        f"-- migrate:up\n{render_sql(migration.upgrade_ops)}\n\n"
        f"-- migrate:down\n{render_sql(migration.downgrade_ops)}\n"
    )
    print(
        f"Created {path.relative_to(MIGRATIONS_DIR.parent)}. Review it before committing."
    )


if __name__ == "__main__":
    main()
