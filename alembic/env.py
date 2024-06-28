from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from db.database_definition import SQL_ALCHEMY_DATABASE_URL

# To enable auto-detect schemas
from db.models import Base  # noqa

# Retrieve the Alembic Config object and set the SQLAlchemy URL.
config = context.config
config.set_main_option("sqlalchemy.url", SQL_ALCHEMY_DATABASE_URL)

# Setup loggers if config file name is provided.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Set the metadata for 'autogenerate' support.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    In this scenario we need to create an Engine and associate
    a connection with the context.
    """
    configuration = config.get_section(config.config_ini_section)
    if configuration is None:
        raise ValueError("Configuration section is missing.")

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine if we are running in offline or online mode,
# and run the appropriate migration function.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
