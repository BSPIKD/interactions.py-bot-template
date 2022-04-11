create table users
(
    id        bigint       not null,
    username  varchar(255) not null,
    date_reg  timestamp             default current_timestamp() comment 'Datum registrace',
    is_active tinyint(1)   not null default 1 comment 'Jestli je uživatel na serveru',
    primary key (id)
);