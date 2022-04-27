create table `logs`
(
    date_cts timestamp default current_timestamp(),
    date_uts int(11)   default unix_timestamp(),
    class    varchar(255)  not null,
    method   varchar(255)  not null,
    line     int,
    type     varchar(50)   not null,
    message  varchar(2000) not null
);