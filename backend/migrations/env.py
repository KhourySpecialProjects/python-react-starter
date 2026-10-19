import asyncio
from logging.config import fileConfig

from alembic import context
from alembic.operations.ops import MigrationScript
from alembic.runtime.migration import MigrationContext
from sqlalchemy import Connection

from app.core.db import engine
from app.models import Base

if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)


def skip_empty_revision(
    _context: MigrationContext, _revision: object, directives: list[MigrationScript]
) -> None:
    """Migrations come from model changes. With no changes, write nothing."""
    upgrade_ops = directives[0].upgrade_ops
    if upgrade_ops is not None and upgrade_ops.is_empty():
        directives.clear()
        print("No model changes found, so no migration was created.")


def run_migrations(connection: Connection) -> None:
    # Autogenerate compares the database against every model on this metadata.
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        process_revision_directives=skip_empty_revision,
    )
    with context.begin_transaction():
        context.run_migrations()


async def main() -> None:
    async with engine.connect() as connection:
        await connection.run_sync(run_migrations)
    await engine.dispose()


asyncio.run(main())
