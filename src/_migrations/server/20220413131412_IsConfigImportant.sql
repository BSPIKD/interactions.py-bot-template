alter table config
add column is_important tinyint(1) default 1 comment 'Jestli je potřeba aby to bylo nakonfigurováno';