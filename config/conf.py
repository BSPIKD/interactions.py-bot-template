from pathlib import Path

# 0.0.1.1
# 0.0.1-rc.1
# core.major.minor.patch-rc
__version__ = '0.0.0.1'
__author__ = "Dom-kun#5353"
__name__ = 'Template'
__contact__ = 'mandinec53@gmail.com'

ROOT_DIR = Path(__file__).parent.parent
MASTER_MIGRATION = Path.joinpath(ROOT_DIR, 'src', '_migrations', 'master')
SERVER_MIGRATION = Path.joinpath(ROOT_DIR, 'src', '_migrations', 'server')

super_user = 'super-user'

role_owner = 'owner-role'
role_main_admin = 'main-admin-role'
role_admin = 'admin-role'
role_ateam = 'ateam-role'

err_msg_no_rights = 'Nemáte dostatečná práva pro tento příkaz!'
