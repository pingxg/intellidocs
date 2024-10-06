from alembic import command
from alembic.config import Config
import os

def run_migrations():
    # Point to the alembic.ini file
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini'))
    command.upgrade(alembic_cfg, 'head')  # Apply all migrations up to the latest revision (head)

if __name__ == '__main__':
    run_migrations()
