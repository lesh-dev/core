<?php
// Version: 1.1; PersonalMessage

$txt[143] = 'Личные сообщения';
$txt[148] = 'Отправить сообщение';
$txt[150] = 'Кому';
$txt[1502] = 'Копия';
$txt[316] = 'Входящие';
$txt[320] = 'Исходящие';
$txt[321] = 'Новое сообщение';
$txt[411] = 'Удалить сообщения';
// Don't translate "PMBOX" in this string.
$txt[412] = 'Удалить все личные сообщения';
$txt[413] = 'Вы уверены, что хотите удалить все сообщения?';
$txt[535] = 'Получатель';
// Don't translate the word "SUBJECT" here, as it is used to format the message - use numeric entities as well.
$txt[561] = 'Новое личное сообщение: SUBJECT';
// Don't translate SENDER or MESSAGE in this language string; they are replaced with the corresponding text - use numeric entities too.
$txt[562] = 'Только что Вы получили личное сообщение от SENDER на ' . $context['forum_name'] . '.' . "\n\n" . 'Обратите внимание это всего лишь уведомление. Пожалуйста не отвечайте на этот email.' . "\n\n" . 'Отправленное Вам сообщение:' . "\n\n" . 'MESSAGE';
$txt[748] = '(получатели: \'имя1, имя2\')';
// Use numeric entities in the below string.
$txt['instant_reply'] = 'Ответить на это личное сообщение здесь:';

$txt['smf249'] = 'Вы уверены, что хотите удалить все выделенные личные сообщения?';

$txt['sent_to'] = 'Получатель';
$txt['reply_to_all'] = 'Ответить Всем';

$txt['pm_capacity'] = 'Количество';
$txt['pm_currently_using'] = '%s сообщений, %s%% полон.';

$txt['pm_error_user_not_found'] = 'Не могу найти пользователя \'%s\'.';
$txt['pm_error_ignored_by_user'] = 'Пользователь \'%s\' заблокировал Выше личное сообщение.';
$txt['pm_error_data_limit_reached'] = 'Сообщение не может быть отправлено \'%s\' ящик переполнен!';
$txt['pm_successfully_sent'] = 'Сообщение удачно отправлено \'%s\'.';
$txt['pm_too_many_recipients'] = 'Вы не можете отправлять личные сообщения более %d получателям одновременно.';
$txt['pm_too_many_per_hour'] = 'Вы превысили количество %d отсылаемых личных сообщений за один час.';
$txt['pm_send_report'] = 'Отправить отчет';
$txt['pm_save_outbox'] = 'Сохранять копию в исходящих';
$txt['pm_undisclosed_recipients'] = 'Скрытые получатели';

$txt['pm_read'] = 'Прочитать';
$txt['pm_replied'] = 'Ответить';

// Message Pruning.
$txt['pm_prune'] = 'Удалить сообщения';
$txt['pm_prune_desc1'] = 'Удалить все личные сообщения старее чем';
$txt['pm_prune_desc2'] = 'дней.';
$txt['pm_prune_warning'] = 'Вы уверены, что хотите очистить Ваши личные сообщения?';

// Actions Drop Down.
$txt['pm_actions_title'] = 'Дальнейшие действия';
$txt['pm_actions_delete_selected'] = 'Удалить выделенные';
$txt['pm_actions_filter_by_label'] = 'Фильтровать по ярлыкам';
$txt['pm_actions_go'] = 'Отправить';

// Manage Labels Screen.
$txt['pm_apply'] = 'Принять';
$txt['pm_manage_labels'] = 'Управление ярлыками';
$txt['pm_labels_delete'] = 'Вы уверены, что хотите удалить выделенные ярлыки?';
$txt['pm_labels_desc'] = 'Здесь Вы можете добавлять, редактировать и удалять ярлыки для ваших личных сообщений.';
$txt['pm_label_add_new'] = 'Добавить новый ярлык';
$txt['pm_label_name'] = 'Имя ярлыка';
$txt['pm_labels_no_exist'] = 'У Вас нет созданных ярлыков!';

// Labeling Drop Down.
$txt['pm_current_label'] = 'Ярлык';
$txt['pm_msg_label_title'] = 'Изменить ярлыки';
$txt['pm_msg_label_apply'] = 'Добавить ярлык';
$txt['pm_msg_label_remove'] = 'Удалить ярлык';
$txt['pm_msg_label_inbox'] = 'Входящие';
$txt['pm_sel_label_title'] = 'Ярлыки для выделенных';
$txt['labels_too_many'] = 'Извините, %s сообщения имеют максимально разрешенное количество ярлыков!';

// Sidebar Headings.
$txt['pm_labels'] = 'Ярлыки';
$txt['pm_messages'] = 'Сообщений';
$txt['pm_preferences'] = 'Предпочтения';

$txt['pm_is_replied_to'] = 'Вы ответили на это сообщение.';

// Reporting messages.
$txt['pm_report_to_admin'] = 'Сообщить Администратору';
$txt['pm_report_title'] = 'Сообщить о личном сообщении';
$txt['pm_report_desc'] = 'С этой страницы Вы можете сообщить о полученном Вами личном сообщении Администрации форума.';
$txt['pm_report_admins'] = 'Отправить Администратору';
$txt['pm_report_all_admins'] = 'Отправить всем Администраторам форума';
$txt['pm_report_reason'] = 'Причина';
$txt['pm_report_message'] = 'Отправить';

// Important - The following strings should use numeric entities.
$txt['pm_report_pm_subject'] = '[Отчет] ';
// In the below string, do not translate "{REPORTER}" or "{SENDER}".
$txt['pm_report_pm_user_sent'] = '{REPORTER} отправил отчет о личном сообщении, отправленном {SENDER}, по следующим причинам:';
$txt['pm_report_pm_other_recipients'] = 'Другие получатели сообщения:';
$txt['pm_report_pm_hidden'] = '%d скрытые получатель(и)';
$txt['pm_report_pm_unedited_below'] = 'Ниже содержание личного сообщения о котором посылали отчет:';
$txt['pm_report_pm_sent'] = 'Отправители:';

$txt['pm_report_done'] = 'Спасибо за отправленный отчет. Скоро Вы получите сообщение от Администрации';
$txt['pm_report_return'] = 'Вернутся во входящие';

$txt['pm_search_title'] = 'Поиск личных сообщений';
$txt['pm_search_bar_title'] = 'Поиск сообщений';
$txt['pm_search_text'] = 'Поиск';
$txt['pm_search_go'] = 'Поиск';
$txt['pm_search_advanced'] = 'Расширенный поиск';
$txt['pm_search_user'] = 'по пользователю';
$txt['pm_search_match_all'] = 'Содержащее все слова';
$txt['pm_search_match_any'] = 'Содержащее любые слова';
$txt['pm_search_options'] = 'Свойства';
$txt['pm_search_post_age'] = 'По возрасту';
$txt['pm_search_show_complete'] = 'Показывать в результатах сообщения целиком.';
$txt['pm_search_subject_only'] = 'Поиск только по теме и автору.';
$txt['pm_search_between'] = 'Между';
$txt['pm_search_between_and'] = 'и';
$txt['pm_search_between_days'] = 'дней';
$txt['pm_search_order'] = 'Результаты поиска';
$txt['pm_search_choose_label'] = 'Выберите параметры поиска или поиск всего';

$txt['pm_search_results'] = 'Результаты поиска';
$txt['pm_search_none_found'] = 'Сообщений не найдено';

$txt['pm_search_orderby_relevant_first'] = 'Уместные первым';
$txt['pm_search_orderby_recent_first'] = 'Последние первыми';
$txt['pm_search_orderby_old_first'] = 'Старые первыми';

$txt['pm_visual_verification_label'] = 'Визуальная проверка';
$txt['pm_visual_verification_desc'] = 'Пожалуйста введите код на изображении прежде чем отправите личное сообщение.';
$txt['pm_visual_verification_listen'] = 'Прослушать';

?>