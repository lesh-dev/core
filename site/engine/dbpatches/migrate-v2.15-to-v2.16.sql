/*
    Персональное постоянное хранилище настроек
    Persistent Session Storage
*/
drop table pss;

create table pss (
    pss_id text primary key,   -- ключ (составной)
    pss_value text,             -- данные

    pss_created text,
    pss_modified text,
    pss_changedby text
);

update `xversion` set db_version = '2.16.1';
