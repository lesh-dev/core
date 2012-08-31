<?php
// Version: 1.1; ManagePermissions

$txt['permissions_title'] = 'Управление правами доступа пользователей';
$txt['permissions_modify'] = 'Изменить';
$txt['permissions_access'] = 'Доступ';
$txt['permissions_allowed'] = 'Разрешить';
$txt['permissions_denied'] = 'Запретить';

$txt['permissions_switch'] = 'Переключить на';
$txt['permissions_global'] = 'Глобальный';
$txt['permissions_local'] = 'Локальный';

$txt['permissions_groups'] = 'Права доступа по группам';
$txt['permissions_all'] = 'все';
$txt['permissions_none'] = 'нет';
$txt['permissions_set_permissions'] = 'Установить';

$txt['permissions_with_selection'] = 'С выделенным';
$txt['permissions_apply_pre_defined'] = 'Применить предустановленный профиль прав доступа';
$txt['permissions_select_pre_defined'] = 'Выберите профиль';
$txt['permissions_copy_from_board'] = 'Копировать права доступа с этого раздела';
$txt['permissions_select_board'] = 'Выберите раздел';
$txt['permissions_like_group'] = 'Установить права доступа как у этой группы';
$txt['permissions_select_membergroup'] = 'Выбрать группу';
$txt['permissions_add'] = 'Разрешить';
$txt['permissions_remove'] = 'Сбросить права доступа';
$txt['permissions_deny'] = 'Запретить';
$txt['permissions_select_permission'] = 'Выберите права доступа';

// All of the following block of strings should not use entities, instead use \\" for &quot; etc.
$txt['permissions_only_one_option'] = 'Вы можете выбрать только одно действие при изменении прав доступа';
$txt['permissions_no_action'] = 'Действие не выбрано';
$txt['permissions_deny_dangerous'] = 'Вы собираетесь запретить одно или несколько действий.\\nЕще раз все проверьте, дабы Вы случайно не урезали кому-то права.\\n\\nВы действительно хотите продолжить?';

$txt['permissions_boards'] = 'Права доступа по разделам';

$txt['permissions_modify_group'] = 'Изменение прав пользователей';
$txt['permissions_general'] = 'Основные права';
$txt['permissions_board'] = 'Права для разделов с глобальными привилегиями';
$txt['permissions_commit'] = 'Сохранить';
$txt['permissions_modify_local'] = 'Изменить локальные права доступа';
$txt['permissions_on'] = 'в разделе';
$txt['permissions_local_for'] = 'Локальные права доступа для раздела';
$txt['permissions_option_on'] = '+';
$txt['permissions_option_off'] = '-';
$txt['permissions_option_deny'] = 'X';
$txt['permissions_option_desc'] = 'В качестве прав доступа Вы можете установить следующие права \'Разрешить\' (+), \'Отклонить\' (-), или <span style="color: red;">\'Запретить\' (X)</span>.<br /><br />Пользуйтесь запретом прав доступа с осторожностью.';

$txt['permissiongroup_general'] = 'Общие';
$txt['permissionname_view_stats'] = 'Просмотр статистики форума';
$txt['permissionhelp_view_stats'] = 'Статистика пользователей отображает общую информацию о форуме, такую как, общее количество пользователей, количество оставленных сообщений, созданных тем и т.д.';
$txt['permissionname_view_mlist'] = 'Просмотр списка пользователей';
$txt['permissionhelp_view_mlist'] = 'Список пользователей показывает всех пользователей, зарегистрированных на форуме. Список может быть отсортирован по Вашему желанию. Список пользователей доступен с главной страницы и со страницы со статистикой форума.';
$txt['permissionname_who_view'] = 'Просмотр Кто Online';
$txt['permissionhelp_who_view'] = 'Список Кто Online отображает пользователей, которые в данный момент находятся на форуме, а также их текущее действие или местоположение. Эти права доступа будут работать только если Вы включите их в \'Характеристиках и Настройках\'. Чтобы просмотреть этот список, нажмите на ссылку Кто Online, на главной странице. Если запретить, пользователи смогут просматривать список Кто Online, но не будут видеть, где находятся и что делают остальные пользователи.';
$txt['permissionname_search_posts'] = 'Поиск сообщений и тем';
$txt['permissionhelp_search_posts'] = 'Данные права позволяют пользователям использовать функцию поиска по форуму. Если разрешить эту функцию, на главной странице пользователи увидят кнопку ПОИСК.';
$txt['permissionname_karma_edit'] = 'Изменение кармы пользователей';
$txt['permissionhelp_karma_edit'] = 'Карма это дополнительная возможность форума, которая отображает популярность пользователя на форуме. Данные права доступа будут работать, только если Вы включили функцию Карма, в настройках Вашего форума. Для гостей, данные права доступа установить невозможно.';

$txt['permissiongroup_pm'] = 'Личные сообщения';
$txt['permissionname_pm_read'] = 'Чтение личных сообщений';
$txt['permissionhelp_pm_read'] = 'Данные права доступа дают пользователям доступ в раздел личных сообщений. Без этих прав, пользователи не смогут читать личные сообщения.';
$txt['permissionname_pm_send'] = 'Отправка личных сообщений';
$txt['permissionhelp_pm_send'] = 'Данные права доступа дают пользователям возможность отправлять личные сообщения. Необходимы права для чтения личных сообщений.';

$txt['permissiongroup_calendar'] = 'Календарь';
$txt['permissionname_calendar_view'] = 'Просмотр календаря';
$txt['permissionhelp_calendar_view'] = 'Календарь отображает дни рождения, праздники или события в каждом месяце года. Эти права доступа дают возможность просматривать календарь. После того как Вы добавите эти права, пользователи увидят кнопку КАЛЕНДАРЬ в строке кнопок форума. Не забудьте включить функцию календаря в настройках форума.';
$txt['permissionname_calendar_post'] = 'Создание событий в календаре';
$txt['permissionhelp_calendar_post'] = 'Событие это созданная тема, которая привязана к определенному дню календаря. Событие может быть создано, если пользователь имеет права создания новых тем на форуме.';
$txt['permissionname_calendar_edit'] = 'Редактирование событий в календаре';
$txt['permissionhelp_calendar_edit'] = 'Событие может быть отредактировано, нажатием на красную звездочку (*). Для возможности редактирования событий, пользователь должен иметь право редактировать первое сообщение в теме.';
$txt['permissionname_calendar_edit_own'] = 'Собственные события';
$txt['permissionname_calendar_edit_any'] = 'Любые события';

$txt['permissiongroup_maintenance'] = 'Администрирование форума';
$txt['permissionname_admin_forum'] = 'Администрирование форума и базы данных';
$txt['permissionhelp_admin_forum'] = 'Это право позволяет пользователю:<ul><li>изменять настройки форума, базы данных и тем оформления </li><li>управлять пакетами модификаций</li><li> использовать функцию обслуживания форума</li><li> просматривать ошибки форума и лог модераторских действий</li></ul> Используйте эти права доступа с осторожностью. Оно дает очень большие привилегии на форуме.';
$txt['permissionname_manage_boards'] = 'Управление разделами и категориями';
$txt['permissionhelp_manage_boards'] = 'Эти права доступа позволяют пользователям создавать, редактировать и удалять разделы и категории на форуме.';
$txt['permissionname_manage_attachments'] = 'Управление вложениями и аватарами';
$txt['permissionhelp_manage_attachments'] = 'Эти права доступа позволяют пользователям управлять вложениями и аватарами на форуме.';
$txt['permissionname_manage_smileys'] = 'Управление смайлами';
$txt['permissionhelp_manage_smileys'] = 'Эти права доступа позволяют пользователям управлять смайлами форума. Удалять, добавлять, редактировать, а так же создавать новые наборы смайлов';
$txt['permissionname_edit_news'] = 'Редактирование новостей';
$txt['permissionhelp_edit_news'] = 'Это право позволяет пользователям управлять новостями форума. Функция новостей должна быть включена в настройках форума.';

$txt['permissiongroup_member_admin'] = 'Администрирование пользователей';
$txt['permissionname_moderate_forum'] = 'Управление пользователями форума';
$txt['permissionhelp_moderate_forum'] = 'Эти права доступа включают все важные функции модерирования, такие как:<ul><li>доступ к настройке регистрации</li><li>просмотр и удаление пользователей</li><li>просмотр информации пользователей, включающей проверку IP адреса</li><li>активация учетной записи</li><li>получение уведомление об одобрении учетной записи и возможность одобрить учетную запись</li><li>отправка личных сообщений пользователям, которые отказались от получения личных сообщений</li><li>другие функции</li></ul>';
$txt['permissionname_manage_membergroups'] = 'Управление группами пользователей';
$txt['permissionhelp_manage_membergroups'] = 'Позволяет пользователям редактировать группы пользователей, а так же включать пользователей в эти группы.';
$txt['permissionname_manage_permissions'] = 'Управление правами доступа';
$txt['permissionhelp_manage_permissions'] = 'Это право позволяет пользователям менять права доступа у групп пользователей.';
$txt['permissionname_manage_bans'] = 'Редактирование бан листа';
$txt['permissionhelp_manage_bans'] = 'Это право позволяет пользователям редактировать бан лист. Есть возможность очищать лог попыток обращения к форуму от забаненных пользователей.';
$txt['permissionname_send_mail'] = 'Отправка email пользователям';
$txt['permissionhelp_send_mail'] = 'Это право позволяет делать массовую рассылку сообщений пользователям, либо некоторым группам пользователей. Можно отправлять email или личные сообщения.';

$txt['permissiongroup_profile'] = 'Профили пользователей';
$txt['permissionname_profile_view'] = 'Просмотр профилей пользователей';
$txt['permissionhelp_profile_view'] = 'Это право позволяет просматривать профили зарегистрированных на форуме пользователей. Смотреть общую информацию, статистику и все сообщения пользователя.';
$txt['permissionname_profile_view_own'] = 'Собственный профиль';
$txt['permissionname_profile_view_any'] = 'Любой профиль';
$txt['permissionname_profile_identity'] = 'Изменение настроек учетной записи';
$txt['permissionhelp_profile_identity'] = 'Настройки учетной записи включают в себя основные настройки, такие как изменение пароля, email адреса, языка и т.д.';
$txt['permissionname_profile_identity_own'] = 'Собственный профиль';
$txt['permissionname_profile_identity_any'] = 'Любой профиль';
$txt['permissionname_profile_extra'] = 'Редактирование дополнительных настроек профиля';
$txt['permissionhelp_profile_extra'] = 'Дополнительные настройки учетной записи включают в себя настройку аватара, тем оформления, уведомлений и личных сообщений.';
$txt['permissionname_profile_extra_own'] = 'Собственный профиль';
$txt['permissionname_profile_extra_any'] = 'Любой профиль';
$txt['permissionname_profile_title'] = 'Установка подписи над аватаром';
$txt['permissionhelp_profile_title'] = 'Данная подпись отображается в каждой теме, над профилем каждого пользователя, естественно, если это поле не было оставлено пустым.';
$txt['permissionname_profile_title_own'] = 'Собственный профиль';
$txt['permissionname_profile_title_any'] = 'Любой профиль';
$txt['permissionname_profile_remove'] = 'Удаление учетной записи';
$txt['permissionhelp_profile_remove'] = 'Это право позволяет пользователям удалять их собственные учетные записи с форума.';
$txt['permissionname_profile_remove_own'] = 'Собственный';
$txt['permissionname_profile_remove_any'] = 'Любой';
$txt['permissionname_profile_server_avatar'] = 'Использование аватаров форума';
$txt['permissionhelp_profile_server_avatar'] = 'Это право позволяет пользователям использовать аватары, которые установлены на Вашем форуме.';
$txt['permissionname_profile_upload_avatar'] = 'Загрузка аватаров на сервер';
$txt['permissionhelp_profile_upload_avatar'] = 'Это право позволит пользователям загружать свои собственные аватары на сервер.';
$txt['permissionname_profile_remote_avatar'] = 'Установка удаленных аватар';
$txt['permissionhelp_profile_remote_avatar'] = 'Это право позволит пользователям указывать ссылки на аватары, расположенные на другом сервере. В целях безопасности, не стоит разрешать использовать данную функцию непроверенным пользователям.';

$txt['permissiongroup_general_board'] = 'Общие';
$txt['permissionname_moderate_board'] = 'Модерирование раздела';
$txt['permissionhelp_moderate_board'] = 'Это право добавляет некоторые небольшие функции модерирования в разделах. Например, ответ в закрытую тему, изменение времени окончания голосования и просмотр результатов голосования.';

$txt['permissiongroup_topic'] = 'Темы';
$txt['permissionname_post_new'] = 'Создание новых тем';
$txt['permissionhelp_post_new'] = 'Это право позволяет пользователям создавать новые темы. По умолчанию, оно не позволяет отвечать в темы. То есть если у пользователя нет прав отвечать в теме, он сможет только ее создать.';
$txt['permissionname_merge_any'] = 'Объединение тем';
$txt['permissionhelp_merge_any'] = 'Это право позволяет пользователям объединять две темы в одну. Главной темой получится та, у которой первое сообщение создано раньше по времени.';
$txt['permissionname_split_any'] = 'Разделение тем';
$txt['permissionhelp_split_any'] = 'Это право позволяет пользователям разделять темы';
$txt['permissionname_send_topic'] = 'Отправка тем друзьям';
$txt['permissionhelp_send_topic'] = 'Это право позволяет пользователям отправлять ссылку на тему своим друзьям.';
$txt['permissionname_make_sticky'] = 'Прикрепление тем';
$txt['permissionhelp_make_sticky'] = 'Это право позволяет пользователям прикреплять темы.';
$txt['permissionname_move'] = 'Перемещение тем';
$txt['permissionhelp_move'] = 'Это право позволяет перемещать тему из одного раздела в другой.';
$txt['permissionname_move_own'] = 'Собственная тема';
$txt['permissionname_move_any'] = 'Любая тема';
$txt['permissionname_lock'] = 'Закрытие тем';
$txt['permissionhelp_lock'] = 'Это право позволяет пользователям закрывать темы. После этого в нее может написать только Модератор или Администратор.';
$txt['permissionname_lock_own'] = 'Собственная тема';
$txt['permissionname_lock_any'] = 'Любая тема';
$txt['permissionname_remove'] = 'Удаление тем';
$txt['permissionhelp_remove'] = 'Это право позволяет пользователям удалять темы.';
$txt['permissionname_remove_own'] = 'Собственная тема';
$txt['permissionname_remove_any'] = 'Любая тема';
$txt['permissionname_post_reply'] = 'Отправка сообщений в тему';
$txt['permissionhelp_post_reply'] = 'Это право позволяет пользователям отвечать в темы';
$txt['permissionname_post_reply_own'] = 'Собственная тема';
$txt['permissionname_post_reply_any'] = 'Любая тема';
$txt['permissionname_modify_replies'] = 'Редактирование любых ответов в собственной теме';
$txt['permissionhelp_modify_replies'] = 'Это право позволяет автору темы изменять ответы в собственной теме.';
$txt['permissionname_delete_replies'] = 'Удаление любых ответов в собственной теме';
$txt['permissionhelp_delete_replies'] = 'Это право позволяет автору темы удалять ответы в собственной теме.';
$txt['permissionname_announce_topic'] = 'Объявление пользователей о теме';
$txt['permissionhelp_announce_topic'] = 'Это право позволяет отправлять уведомления о теме по email зарегистрированным пользователям или только выбранным группам пользователей.';

$txt['permissiongroup_post'] = 'Сообщения';
$txt['permissionname_delete'] = 'Удаление сообщений';
$txt['permissionhelp_delete'] = 'Это право позволяет пользователям удалять сообщение в темах, кроме самого первого сообщения.';
$txt['permissionname_delete_own'] = 'Собственное сообщение';
$txt['permissionname_delete_any'] = 'Любое сообщение';
$txt['permissionname_modify'] = 'Редактирование сообщений';
$txt['permissionhelp_modify'] = 'Редактирование сообщений';
$txt['permissionname_modify_own'] = 'Собственное сообщение';
$txt['permissionname_modify_any'] = 'Любое сообщение';
$txt['permissionname_report_any'] = 'Оповещение Модераторов';
$txt['permissionhelp_report_any'] = 'Это право помещает в каждом ответе ссылку для оповещения Модераторов. После оповещения, все Модераторы раздела получать уведомление на email со ссылкой и комментарием.';

$txt['permissiongroup_poll'] = 'Голосования';
$txt['permissionname_poll_view'] = 'Просмотр голосований';
$txt['permissionhelp_poll_view'] = 'Это право позволяет пользователям просматривать голосования. Без этого права они увидят одну тему (без голосования).';
$txt['permissionname_poll_vote'] = 'Возможность голосовать';
$txt['permissionhelp_poll_vote'] = 'Это право позволяет зарегистрированным пользователям голосовать в голосованиях.';
$txt['permissionname_poll_post'] = 'Создание голосований';
$txt['permissionhelp_poll_post'] = 'Это право позволяет пользователям создавать голосования.';
$txt['permissionname_poll_add'] = 'Добавление голосований в тему';
$txt['permissionhelp_poll_add'] = 'Это право позволяет добавлять голосование в тему, которая уже была создана. Это право требует права редактирования первого сообщения в теме.';
$txt['permissionname_poll_add_own'] = 'Собственная тема';
$txt['permissionname_poll_add_any'] = 'Любая тема';
$txt['permissionname_poll_edit'] = 'Редактирование голосований';
$txt['permissionhelp_poll_edit'] = 'Это право позволяет редактировать варианты ответов в голосовании и сбрасывать счетчик голосов. Для задания опции количества максимальных сообщений и время голосования, пользователь должен иметь право  \'Модерирование раздела\'.';
$txt['permissionname_poll_edit_own'] = 'Собственное голосование';
$txt['permissionname_poll_edit_any'] = 'Любое голосование';
$txt['permissionname_poll_lock'] = 'Закрытие голосований';
$txt['permissionhelp_poll_lock'] = 'Это право позволяет пользователям закрывать голосования.';
$txt['permissionname_poll_lock_own'] = 'Собственное голосование';
$txt['permissionname_poll_lock_any'] = 'Любое голосование';
$txt['permissionname_poll_remove'] = 'Удаление голосований';
$txt['permissionhelp_poll_remove'] = 'Это право позволяет пользователям удалять голосования.';
$txt['permissionname_poll_remove_own'] = 'Собственное голосование';
$txt['permissionname_poll_remove_any'] = 'Любое голосование';

$txt['permissiongroup_notification'] = 'Уведомления';
$txt['permissionname_mark_any_notify'] = 'Получение уведомлений о новых ответах';
$txt['permissionhelp_mark_any_notify'] = 'Это право позволяет пользователям получать уведомления о новых сообщениях в теме.';
$txt['permissionname_mark_notify'] = 'Получение уведомлений о новых темах';
$txt['permissionhelp_mark_notify'] = 'Это право позволяет пользователям получать уведомления о новых темах.';

$txt['permissiongroup_attachment'] = 'Вложения';
$txt['permissionname_view_attachments'] = 'Просмотр вложений';
$txt['permissionhelp_view_attachments'] = 'Вложения - это файлы, которые пользователь прикрепил к своему сообщению. Это право позволяет просматривать вложения, сделанные пользователями.';
$txt['permissionname_post_attachment'] = 'Отправка вложений';
$txt['permissionhelp_post_attachment'] = 'Вложения - это файлы, которые пользователь прикрепил к своему сообщению. Это право позволят прикреплять вложения к сообщению. На одно сообщение может быть несколько вложений.';

$txt['permissionicon'] = '';

$txt['permission_settings_title'] = 'Настройка Прав Доступа';
$txt['groups_manage_permissions'] = 'Группа пользователей, имеющая право изменять права доступа';
$txt['permission_settings_submit'] = 'Сохранить';
$txt['permission_settings_enable_deny'] = 'Включить использование запрещающих прав для групп';
// Escape any single quotes in here twice.. 'it\'s' -> 'it\\\'s'.
$txt['permission_disable_deny_warning'] = 'Выключение этой функции сбросит все запрещающие права пользователей.';
$txt['permission_by_membergroup_desc'] = 'Здесь Вы можете установить глобальные права для каждой группы. Эти права будут действовать в любом разделе, кроме тех на которые распространяются локальные права доступа.';
$txt['permission_by_board_desc'] = 'Здесь Вы можете установить какие права будет использовать раздел, глобальные или локальные. Использование локальных разрешений подразумевает, что для групп пользователей в этом разделе действуют свои определенные права, возможно отличающиеся от глобальных.';
$txt['permission_settings_desc'] = 'Здесь Вы можете выбрать, кто имеет право изменять права в разделах.';
$txt['permission_settings_enable_postgroups'] = 'Включить использование прав для групп основанных на количестве сообщений';
// Escape any single quotes in here twice.. 'it\'s' -> 'it\\\'s'.
$txt['permission_disable_postgroups_warning'] = 'Выключение этой функции сбросит все выставленные права доступа для групп основанных на количестве сообщений.';
$txt['permission_settings_enable_by_board'] = 'Включить выставление отдельных прав доступа для каждого раздела';
// Escape any single quotes in here twice.. 'it\'s' -> 'it\\\'s'.
$txt['permission_disable_by_board_warning'] = 'Выключение этой опции сбросит все выставленные права доступа для раздела.';

?>