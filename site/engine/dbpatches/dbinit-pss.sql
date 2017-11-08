/*
    Персональное постоянное хранилище настроек
    Persistent Session Storage
*/
drop table if exists pss;

create table pss (
    pss_id text primary key,   -- ключ (составной)
    pss_value text,             -- данные

    pss_created text,
    pss_modified text,
    pss_changedby text
);
