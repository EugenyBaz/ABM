import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, make_url
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.database.database import Base
from app.models import tasks  # noqa: F401


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = settings.DATABASE_URL

url = make_url(DATABASE_URL)
if url.drivername.endswith("+asyncpg"):
    url = url.set(drivername="postgresql+psycopg2")

config.set_main_option("sqlalchemy.url", str(url))


def run_migrations_offline():
    context.configure(
        url=str(url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online_async():
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    asyncio.run(run_migrations_online_async())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
