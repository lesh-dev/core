<?php
// Version: 1.1; Search

$txt[183] = 'Параметры Поиска';
$txt[189] = 'Выберите раздел, в котором будет производиться поиск, или искать везде';
$txt[343] = 'По фразе целиком';
$txt[344] = 'Любое из слов';
$txt[583] = 'От пользователя';

$txt['search_post_age'] = 'Возраст сообщения';
$txt['search_between'] = 'Между';
$txt['search_and'] = 'и';
$txt['search_options'] = 'Свойства';
$txt['search_show_complete_messages'] = 'Отображать результаты в виде сообщений';
$txt['search_subject_only'] = 'Только название темы';
$txt['search_relevance'] = 'Совпадение';
$txt['search_date_posted'] = 'Дата сообщения';
$txt['search_order'] = 'Порядок сортировки';
$txt['search_orderby_relevant_first'] = 'Наиболее подходящие результаты первыми';
$txt['search_orderby_large_first'] = 'Наибольшие темы первыми';
$txt['search_orderby_small_first'] = 'Наименьшие темы первыми';
$txt['search_orderby_recent_first'] = 'Последние темы первыми';
$txt['search_orderby_old_first'] = 'Старые темы первыми';

$txt['search_specific_topic'] = 'Искать сообщения только в теме';

$txt['mods_cat_search'] = 'Поиск';
$txt['groups_search_posts'] = 'Группы пользователей с доступом к функции поиска';
$txt['simpleSearch'] = 'Разрешить простой поиск';
$txt['search_results_per_page'] = 'Максимум результатов на страницу';
$txt['search_weight_frequency'] = 'Релевантность поиска по количеству сообщений в теме';
$txt['search_weight_age'] = 'Релевантность поиска по возрасту последних сообщений';
$txt['search_weight_length'] = 'Релевантность поиска по величине темы';
$txt['search_weight_subject'] = 'Релевантность поиска по названию темы сообщений';
$txt['search_weight_first_message'] = 'Релевантность поиска по содержащимся первым сообщениям';
$txt['search_weight_sticky'] = 'Релевантность поиска по прикрепленным темам';

$txt['search_settings_desc'] = 'Здесь Вы можете изменять обычные настройки поиска.';
$txt['search_settings_title'] = 'Настройка поиска';
$txt['search_settings_save'] = 'Сохранить';

$txt['search_weights'] = 'Параметры поиска';
$txt['search_weights_desc'] = 'Здесь Вы можете изменять индивидуальные компоненты оценки совпадения по поиску.';
$txt['search_weights_title'] = 'Релевантность поиска';
$txt['search_weights_total'] = 'Всего';
$txt['search_weights_save'] = 'Сохранить';

$txt['search_method'] = 'Индексирование';
$txt['search_method_desc'] = 'Здесь Вы можете установить параметры поиска.';
$txt['search_method_title'] = 'Метод поиска';
$txt['search_method_save'] = 'Сохранить';
$txt['search_method_messages_table_space'] = 'Размер сообщений в базе данных';
$txt['search_method_messages_index_space'] = 'Размер индексов в базе данных';
$txt['search_method_kilobytes'] = 'Кб';
$txt['search_method_fulltext_index'] = 'Полнотекстовое индексирование';
$txt['search_method_no_index_exists'] = 'не создан';
$txt['search_method_fulltext_create'] = 'создать';
$txt['search_method_fulltext_cannot_create'] = 'невозможно создать индексирование, максимальная длинна сообщения - 65,535, либо тип таблицы отличается от типа MyISAM';
$txt['search_method_index_already_exsits'] = 'создан';
$txt['search_method_fulltext_remove'] = 'удалить';
$txt['search_method_index_partial'] = 'уже создан';
$txt['search_index_custom_resume'] = 'продолжить';
// This string is used in a javascript confirmation popup; don't use entities.
$txt['search_method_fulltext_warning'] = 'Для использования полнотекстового поиска, Вы должны создать полнотекстовое индексирование!';

$txt['search_index'] = 'Поисковое индексирование';
$txt['search_index_none'] = 'Не использовать индексирование';
$txt['search_index_custom'] = 'Выборочное индексирование';
$txt['search_index_label'] = 'Индексирование';
$txt['search_index_size'] = 'Размер';
$txt['search_index_create_custom'] = 'создать';
$txt['search_index_custom_remove'] = 'удалить';
// This string is used in a javascript confirmation popup; don't use entities.
$txt['search_index_custom_warning'] = 'Для использования выборочного поиска, Вы должны создать выборочное индексирование!';

$txt['search_force_index'] = 'Использовать только поисковый индекс';
$txt['search_match_words'] = 'Только слова целиком';
$txt['search_max_results'] = 'Максимум результатов для отображения';
$txt['search_max_results_disable'] = '(0: без ограничений)';

$txt['search_create_index'] = 'Создание индексирования';
$txt['search_create_index_why'] = 'Для чего нужны поисковое индексирование?';
$txt['search_create_index_start'] = 'Создать';
$txt['search_predefined'] = 'Предустановленный профиль';
$txt['search_predefined_small'] = 'Малоразмерное индексирование';
$txt['search_predefined_moderate'] = 'Среднеразмерное индексирование';
$txt['search_predefined_large'] = 'Большеразмерное индексирование';
$txt['search_create_index_continue'] = 'Продолжить';
$txt['search_create_index_not_ready'] = 'SMF создает поисковое индексирование сообщений. Чтобы предотвратить большую загрузку сервера, процесс создания индексирования был приостановлен. Процесс автоматически продолжится через несколько секунд. В случае полной остановки, нажмите на кнопку ниже.';
$txt['search_create_index_progress'] = 'Выполнено';
$txt['search_create_index_done'] = 'Индексирование завершено!';
$txt['search_create_index_done_link'] = 'Продолжить';
$txt['search_double_index'] = 'Ваша таблица сообщений использует два индекса. Для улучшения производительности рекомендуется удалить один из них.';

$txt['search_error_indexed_chars'] = 'Неверное число символов индексации. Как минимум 3 символа необходимы для индексации.';
$txt['search_error_max_percentage'] = 'Неверный процент отсеивания слов. Используйте значение как минимум 5%.';

$txt['search_adjust_query'] = 'Уточните параметры поиска';
$txt['search_adjust_submit'] = 'Повторить поиск';
$txt['search_did_you_mean'] = 'Возможно Вы ищете';

$txt['search_example'] = '<i>Пример:</i> Дин КУНЦ "Холодный огонь" -книга';

?>