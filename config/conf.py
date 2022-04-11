from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
MASTER_MIGRATION = Path.joinpath(ROOT_DIR, 'src', '_migrations', 'master')
SERVER_MIGRATION = Path.joinpath(ROOT_DIR, 'src', '_migrations', 'server')

super_user = 'super-user'

role_owner = 'owner-role'
role_main_admin = 'main-admin-role'
role_admin = 'admin-role'
role_ateam = 'ateam-role'
