Процедура переноса данных.

../fizlesh.sqlite3 -- исходная база.

1. Чистим битые ссылки, кривые целые числа и таймстемпы:

    `sqlite3 ../fizlesh.sqlite3 < remove_broken.sql`
2. Запускаем `./migrate.sh ../fizlesh.sqlite3`.
