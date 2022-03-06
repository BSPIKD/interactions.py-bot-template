create table _migrations
(
    name        varchar(255) not null,
    `timestamp` timestamp default current_timestamp()
);