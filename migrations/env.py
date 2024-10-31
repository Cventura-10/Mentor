import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context
from app import db  # Ensure this imports the SQLAlchemy instance
from app.models import User  # Import your models here to ensure they are recognized

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Set up logging configurations from the config file
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Set target_metadata for Alembic to detect model changes
target_metadata = db.metadata  # Use the main metadata for all models

def get_engine():
    try:
        # Retrieve the engine for different Flask-SQLAlchemy versions
        return current_app.extensions['migrate'].db.get_engine()
    except TypeError:
        return current_app.extensions['migrate'].db.engine

# Configure Alembic with the SQLAlchemy URL from the app’s config
config.set_main_option(
    'sqlalchemy.url', str(get_engine().url).replace('%', '%%')
)
target_db = current_app.extensions['migrate'].db

def get_metadata():
    # Fetch metadata; compatible with multiple metadata setups if used
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode, without a DBAPI."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode, connecting directly to the database."""
    
    # Callback to avoid migrations if no schema changes detected
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            context.run_migrations()

# Execute migrations depending on mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
