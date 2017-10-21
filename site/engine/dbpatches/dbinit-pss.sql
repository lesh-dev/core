/*
    Персональное постоянное хранилище настроек
    Persistent Session Storage
*/
create table pss (
    pss_key text primary key,  -- ключ (составной)
    pss_value text             -- данные
);
