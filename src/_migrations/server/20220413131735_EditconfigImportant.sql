update config set is_important = 0
where `key` = 'default-admin-cmd-channel'
or `key` = 'default-owner-cmd-channel'
or `key` = 'default-user-cmd-channel';