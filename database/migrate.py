from alembic import command, op
from alembic.config import Config
import os

def run_migrations():
    # Point to the alembic.ini file
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini'))
    command.revision(alembic_cfg, autogenerate=True, message="Auto-generated migration")
    command.upgrade(alembic_cfg, 'head')

if __name__ == '__main__':
    run_migrations()
