<?php
// Version: 1.1; Install

// These should be the same as those in index.language.php.
$txt['lang_character_set'] = 'UTF-8';
$txt['lang_rtl'] = false;

$txt['smf_installer'] = 'Установка форума SMF';
$txt['installer_language'] = 'Язык';
$txt['installer_language_set'] = 'Установить';
$txt['congratulations'] = 'Поздравляем, процесс установки завершен!';
$txt['congratulations_help'] = 'Если у Вас возникают проблемы с работой форума, не забывайте про <a href="http://www.simplemachines.org/community/index.php" target="_blank">сайт технической поддержки</a>.';
$txt['still_writable'] = 'Директория установки имеет права на запись. В целях безопасности рекомендуется сделать ее доступной только для чтения.';
$txt['delete_installer'] = 'Нажмите сюда, чтобы удалить install.php.';
$txt['delete_installer_maybe'] = '<i>(работает не на всех серверах.)</i>';
$txt['go_to_your_forum'] = 'Теперь Вы можете перейти на установленный <a href="%s">форум</a>. После входа, Вам будет доступен раздел администрирования.';
$txt['good_luck'] = 'Удачи!<br />SimpleMachines';

$txt['user_refresh_install'] = 'Обновление форума';
$txt['user_refresh_install_desc'] = 'Во время установки, инсталлятор обнаружил, что одна или несколько таблиц, которые должны быть созданы в базе данных, уже существуют.<br />Эти таблицы были заполнены данными по умолчанию, Ваши данные, содержащиеся в таблицах, сохранены.';

$txt['default_topic_subject'] = 'Добро пожаловать в SMF!';
$txt['default_topic_message'] = 'Добро пожаловать на форум SimpleMachines!<br /><br />Если у Вас возникают проблемы с форумом, пожалуйста, обращайтесь на [url=http://www.simplemachines.org/community/index.php]официальный сайт поддержки[/url].<br /><br />Большое спасибо!<br />SimpleMachines';
$txt['default_board_name'] = 'Общий раздел';
$txt['default_board_description'] = 'В этом разделе можно вести разговоры на любые темы.';
$txt['default_category_name'] = 'Главная категория';
$txt['default_time_format'] = '%d %B %Y, %H:%M:%S';
$txt['default_news'] = 'SMF форум только что установлен!';
$txt['default_karmaLabel'] = 'Карма:';
$txt['default_karmaSmiteLabel'] = '[отнять]';
$txt['default_karmaApplaudLabel'] = '[прибавить]';
$txt['default_reserved_names'] = 'Admin\\nWebmaster\\nGuest\\nroot';
$txt['default_smileyset_name'] = 'По умолчанию';
$txt['default_classic_smileyset_name'] = 'Classic';
$txt['default_theme_name'] = 'SMF Default Theme - Core';
$txt['default_classic_theme_name'] = 'Classic YaBB SE Theme';
$txt['default_babylon_theme_name'] = 'Babylon Theme';

$txt['default_administrator_group'] = 'Администратор';
$txt['default_global_moderator_group'] = 'Глобальный модератор';
$txt['default_moderator_group'] = 'Модератор';
$txt['default_newbie_group'] = 'Новичок';
$txt['default_junior_group'] = 'Пользователь';
$txt['default_full_group'] = 'Постоялец';
$txt['default_senior_group'] = 'Старожил';
$txt['default_hero_group'] = 'Ветеран';

$txt['default_smiley_smiley'] = 'Улыбка';
$txt['default_wink_smiley'] = 'Подмигивающий';
$txt['default_cheesy_smiley'] = 'Веселый';
$txt['default_grin_smiley'] = 'Смеющийся';
$txt['default_angry_smiley'] = 'Злой';
$txt['default_sad_smiley'] = 'Грустный';
$txt['default_shocked_smiley'] = 'Шокирован';
$txt['default_cool_smiley'] = 'Крутой';
$txt['default_huh_smiley'] = 'Непонимающий';
$txt['default_roll_eyes_smiley'] = 'Строит глазки';
$txt['default_tongue_smiley'] = 'Показывает язык';
$txt['default_embarrassed_smiley'] = 'Обеспокоенный';
$txt['default_lips_sealed_smiley'] = 'Рот на замке';
$txt['default_undecided_smiley'] = 'В замешательстве';
$txt['default_kiss_smiley'] = 'Целующий';
$txt['default_cry_smiley'] = 'Плачущий';
$txt['default_evil_smiley'] = 'Злой';
$txt['default_azn_smiley'] = 'Azn';
$txt['default_afro_smiley'] = 'Афро';

$txt['error_message_click'] = 'Нажмите сюда';
$txt['error_message_try_again'] = 'чтобы повторить действие.';
$txt['error_message_bad_try_again'] = 'продолжить установку не смотря ни на что (Не рекомендуется).';

$txt['install_settings'] = 'Основные настройки';
$txt['install_settings_info'] = 'Некоторые детали, необходимые для установки :).';
$txt['install_settings_name'] = 'Название форума';
$txt['install_settings_name_info'] = 'Здесь указывается полное название Вашего форума, например: &quot;Тестовый форум&quot;.';
$txt['install_settings_name_default'] = 'Название Вашего форума';
$txt['install_settings_url'] = 'Адрес(URL) форума';
$txt['install_settings_url_info'] = 'Адрес(URL) форума указывается <b>без \'/\'</b> в конце.<br />Программа установки автоматически определила адрес. При желании Вы можете его изменить.';
$txt['install_settings_compress'] = 'Gzip сжатие';
$txt['install_settings_compress_title'] = 'Сжимать исходящие данные для экономии трафика.';
// In this string, you can translate the word "PASS" to change what it says when the test passes.
$txt['install_settings_compress_info'] = 'Эта функция работает не на всех серверах.<br />Нажмите <a href="install.php?obgz=1&amp;pass_string=PASS" onclick="return reqWin(this.href, 200, 60);" target="_blank">сюда</a> для проверки Вашего сервера. (Если сжатие поддерживается сервером, Вы увидите слово "PASS".)';
$txt['install_settings_dbsession'] = 'Сессии в Базе Данных';
$txt['install_settings_dbsession_title'] = 'Хранить сессии в Базе Данных';
$txt['install_settings_dbsession_info1'] = 'Эта функция повышает производительность форума из-за быстрого доступа к сессиям пользователей.';
$txt['install_settings_dbsession_info2'] = 'Хорошая идея хранить сессии в базе данных, но на Вашем сервере она может не работать.';
$txt['install_settings_utf8'] = 'Использовать кодировку UTF-8';
$txt['install_settings_utf8_title'] = 'Использовать кодировку UTF-8 по умолчанию';
$txt['install_settings_utf8_info'] = 'Эта особенность позволяет в базе данных и форуме использовать международную кодировку, UTF-8. Это удобно при использовании мультиязычности при использовании различных кодировок.';
$txt['install_settings_stats'] = 'Позволить собирать статистику';
$txt['install_settings_stats_title'] = 'Разрешить Simple Machines собирать ежемесячную статистику';
$txt['install_settings_stats_info'] = 'Если разрешить, то это позволит Machines посещать Ваш сайт раз в месяц для сбора обычной статистики. Это поможет нам принять решение по оптимизации программного обеспечения. Для получения подробной информации посетите <a href="http://www.simplemachines.org/about/stats.php">информационную страницу</a>.';
$txt['install_settings_proceed'] = 'Продолжить';

$txt['mysql_settings'] = 'Настройки MySQL';
$txt['mysql_settings_info'] = 'Настройки Вашего MySQL сервера. Если Вам не известны эти данные, обратитесь к Вашему хостеру.';
$txt['mysql_settings_server'] = 'Сервер MySQL';
$txt['mysql_settings_server_info'] = 'Чаще всего используется localhost - если Вы не знаете имя сервера, попробуйте localhost.';
$txt['mysql_settings_username'] = 'Пользователь MySQL';
$txt['mysql_settings_username_info'] = 'Введите имя пользователя, для подключения к Базе Данных MySQL.<br />Если Вы не знаете имя пользователя, попробуйте ввести учетную запись FTP пользователя. Чаще всего эти данные совпадают.';
$txt['mysql_settings_password'] = 'Пароль MySQL';
$txt['mysql_settings_password_info'] = 'Введите пароль для доступа к Базе Данных MySQL.<br />Если не знаете пароль, попробуйте ввести пароль от учетный записи FTP пользователя.';
$txt['mysql_settings_database'] = 'база данных MySQL';
$txt['mysql_settings_database_info'] = 'Введите название базы данных, которое Вы хотите использовать.<br />Если База отсутствует, инсталлятор попытается создать ее.';
$txt['mysql_settings_prefix'] = 'Префикс таблиц MySQL';
$txt['mysql_settings_prefix_info'] = 'Префикс для каждой таблицы в Базе Данных.  <b>Не устанавливайте два форума с одним и тем же префиксом!</b>.';

$txt['user_settings'] = 'Создание Вашей учетной записи';
$txt['user_settings_info'] = 'Программа установки создаст для Вас учетную запись администратора.';
$txt['user_settings_username'] = 'Имя пользователя';
$txt['user_settings_username_info'] = 'Выберите имя, которое Вы хотите использовать.<br />Внимание! Это имя в дальнейшем изменить нельзя! Вы сможете изменить только отображаемое имя.';
$txt['user_settings_password'] = 'Пароль';
$txt['user_settings_password_info'] = 'Введите пароль!';
$txt['user_settings_again'] = 'Подтвердите пароль';
$txt['user_settings_again_info'] = '(подтверждение пароля.)';
$txt['user_settings_email'] = 'Email адрес';
$txt['user_settings_email_info'] = 'Введите Ваш email адрес.  <b>Он должен быть действительным.</b>';
$txt['user_settings_database'] = 'Пароль к Базе Данных MySQL';
$txt['user_settings_database_info'] = 'В целях безопасности, для создания учетной записи администратора, требуется ввести пароль к Базе Данных MySQL.';
$txt['user_settings_proceed'] = 'Продолжить';

$txt['ftp_setup'] = 'Настройки FTP сервера';
$txt['ftp_setup_info'] = 'Программа установки может подключиться к серверу по протоколу FTP, чтобы изменить атрибуты файлов(папок), если необходимо изменить права на запись или наоборот.  Если инсталлятор, по каким-то причинам, не смог этого сделать, рекомендуется вручную зайти на форум через FTP и изменить атрибуты требуемых файлов на нужные. Пожалуйста, не забывайте, что до полной установки форума, SSL не поддерживается.';
$txt['ftp_server'] = 'FTP сервер';
$txt['ftp_server_info'] = 'Укажите название FTP сервера и порт.';
$txt['ftp_port'] = 'Порт';
$txt['ftp_username'] = 'Имя пользователя';
$txt['ftp_username_info'] = 'Имя пользователя для доступа к FTP. <i>В дальнейшем нигде не используется и не сохраняется.</i>';
$txt['ftp_password'] = 'Пароль';
$txt['ftp_password_info'] = 'Пароль для доступа к FTP. <i>В дальнейшем нигде не используется и не сохраняется.</i>';
$txt['ftp_path'] = 'Путь установки';
$txt['ftp_path_info'] = 'Это путь FTP сервера.';
$txt['ftp_path_found_info'] = 'Найденный путь.';
$txt['ftp_connect'] = 'Подключиться';
$txt['ftp_setup_why'] = 'Для чего это нужно?';
$txt['ftp_setup_why_info'] = 'Следующие файлы должны иметь права на запись. Программа установки может попытаться сделать их таковыми, если по каким-то причинам этого не произошло, пожалуйста, проставьте права на запись для этих файлов вручную. CHMOD 777 (на некоторых серверах 755):';
$txt['ftp_setup_again'] = 'Проверить права на запись.';

$txt['error_php_too_low'] = 'Внимание! Для нормальной работы SMF форума требуется версия PHP выше, чем установлена у Вас. <br />Если Вы пользуетесь услугами хостинга, обратитесь к хостеру с просьбой обновить версию PHP. Установку форума можно продолжить, но могут возникнуть проблемы.<br /><b>Это не рекомендуется</b>.';
$txt['error_missing_files'] = 'Программе установки не хватает некоторых файлов!<br /><br />Пожалуйста, удостоверьтесь в том, что Вы загрузили на сервер все файлы.';
$txt['error_session_save_path'] = 'Пожалуйста, оповестите Вашего хостера о том, что <b>session.save_path указанный в php.ini</b> неверный!  Путь необходимо изменить на <b>существующую</b> директорию, которая <b>имеет права на запись</b>.<br />';
$txt['error_windows_chmod'] = 'Вы используете сервер на базе Windows, и некоторые файлы не имеют прав на запись. Пожалуйста, обратитесь к Вашему хостеру, с просьбой дать права на запись, пользователю, под которым работает PHP. Следующие файлы и папки должны иметь права на запись:';
$txt['error_ftp_no_connect'] = 'Невозможно подключиться к FTP серверу с указанными данными.';
$txt['error_mysql_connect'] = 'Невозможно подключиться к Базе Данных MySQL с указанными данными.<br /><br />Если Вы не знаете, какие данные необходимо ввести, пожалуйста, обратитесь к Вашему хостеру.';
$txt['error_mysql_too_low'] = 'Версия установленного MySQL сервера устарела. и не соответствует минимальным требования форума SMF.<br /><br />Пожалуйста, обратитесь к Вашему хостеру с просьбой обновить программное обеспечение.';
$txt['error_mysql_database'] = 'Программа установки не может получить доступ к &quot;<i>%s</i>&quot;. На некоторых серверах необходимо вручную создать базу данных.';
$txt['error_mysql_queries'] = 'Некоторые запросы были неправильно обработаны. Это могло произойти из-за неподдерживаемой или старой версии MySQL сервера.<br /><br />Информация о запросе:';
$txt['error_mysql_queries_line'] = 'Строка #';
$txt['error_mysql_missing'] = 'Программа установки не смогла определить поддержку MySQL. Пожалуйста, удостоверьтесь в том, что PHP установлено с поддержкой MySQL.';
$txt['error_session_missing'] = 'Программа установки не смогла определить поддержку сессий на Вашем сервере интерпретатором PHP.  Пожалуйста, удостоверьтесь в том, что PHP установлен с поддержкой сессий.';
$txt['error_user_settings_again_match'] = 'Пароли не совпадают!';
$txt['error_user_settings_taken'] = 'Извините, пользователь с таким именем уже зарегистрирован.<br /><br />Учетная запись не создана.';
$txt['error_user_settings_query'] = 'Во время создания учетной записи администратора возникла следующая ошибка:';
$txt['error_subs_missing'] = 'Отсутствует файл Sources/Subs.php. Пожалуйста, удостоверьтесь в том, что Вы загрузили на сервер все файлы.';
$txt['error_mysql_alter_priv'] = 'Учетная записать MySQL, которую Вы указали не имеет права ИЗМЕНЯТЬ, СОЗДАВАТЬ и УДАЛЯТЬ таблицы в базе данных, что необходимо для правильной работы форума SMF.';
$txt['error_versions_do_not_match'] = 'Программа установки обнаружила другую установленную версию SMF. Если Вы хотите обновить установленную версию, воспользуйтесь программой обновления(upgrade.php).<br /><br />';
$txt['error_mod_security'] = 'Программа установки обнаружила установленный модуль mod_security. Этот модуль будет блокировать передающиеся формой данные. SMF форум имеет встроенный сканер безопасности, который превосходит по возможностям этот модуль и работает намного эффективней.<br /><br /><a href="http://www.simplemachines.org/redirect/mod_security">Как отключить mod_security</a>';
$txt['error_utf8_mysql_version'] = 'Текущая версия базы данных не поддерживает кодировку UTF-8. Вы можете без проблем установить SMF, но без поддержки UTF-8. Если Вы хотите включить поддержку UTF-8 в будущем (обновите сначала MySQL сервер Вашего форума до версии >=4.1), Вы можете преобразовать форум в UTF-8 через панель Администрирования.';

?>