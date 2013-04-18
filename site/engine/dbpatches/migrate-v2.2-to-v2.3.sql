/* Почтовые нотификации (сериализуемые в одно письмо для компактности) */
create table notification (
    notification_id integer primary key autoincrement,
    mail_group text,        -- почтовая группа
    notification_text text  -- тело нотификации в формате HTML
);
