create table config
(
    `key`       varchar(255) not null,
    `value`     varchar(255),
    description varchar(2000),
    primary key (`key`)
) comment 'Výchozí práva';

insert into config (`key`, description)
values ('default-admin-cmd-channel',
        'Výchozí channel, kde se dají admin příkazy používat (Pokud je hodnota null, může se používat všude)');

insert into config (`key`, description)
values ('default-owner-cmd-channel',
        'Výchozí channel, kde se dají owner příkazy používat (Pokud je hodnota null, může se používat všude)');

insert into config (`key`, description)
values ('default-user-cmd-channel',
        'Výchozí channel, kde se dají user příkazy používat (Pokud je hodnota null, může se používat všude)');

create table config_admin_roles_users
(
    role_id   bigint       not null,
    name      varchar(100) not null,
    type      varchar(100) not null default 'role' comment 'Typ role/uživatel',
    positions varchar(100) not null default 'ateam' comment 'ateam/owner',
    primary key (role_id)
) comment 'Tabulka pro seznam AT rolí/uživatelů';

create table config_cmds
(
    id     int          not null auto_increment,
    name   varchar(300) not null comment 'Název celého příkazu',
    rights varchar(2)   not null default 'U' comment 'Práva příkazu (U - uživatelský, A - kdokoliv z AT, AA - Admin + Hlavní admin + majitel, S - Hlavní admin + Majitel, SS - Majitel)',
    primary key (id)
) comment 'Nastavení práv příkazů';

# create table config_cmd_rights
# (
#     cmd_id int not null,
#
#     primary key (cmd_id),
#     foreign key (cmd_id) references config_cmds (id)
# ) comment 'Dodatečná práva příkazů';
