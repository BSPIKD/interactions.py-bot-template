create table guilds
(
    id           bigint                                 not null primary key,
    name         varchar(255)                           not null,
    registration timestamp  default current_timestamp() not null,
    is_active    tinyint(1) default 1                   not null,
    db_name      varchar(255)                           not null
);
