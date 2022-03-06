from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
MASTER_MIGRATION = Path.joinpath(ROOT_DIR, 'src', '_migrations', 'master')
SERVER_MIGRATION = Path.joinpath(ROOT_DIR, 'src', '_migrations', 'server')
