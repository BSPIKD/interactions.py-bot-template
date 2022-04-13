alter table config_cmds
add column is_allowed tinyint(1) default 1 comment 'Jestli je příkaz povolený k používání';