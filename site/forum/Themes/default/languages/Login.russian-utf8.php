<?php
// Version: 1.1.2; Login

$txt[37] = 'Вы не ввели имя пользователя.';
$txt[38] = 'Вы не ввели пароль.';
$txt[39] = 'Неверный пароль';
$txt[98] = 'Имя пользователя';
$txt[155] = 'Техническое обслуживание';
$txt[245] = 'Регистрация прошла успешно!';
$txt[431] = 'Поздравляем! Теперь Вы зарегистрированы на форуме.';
// Use numeric entities in the below string.
$txt[492] = 'и Ваш пароль';
$txt[500] = 'Пожалуйста, введите действительный email адрес, %s.';
$txt[517] = 'Необходимая информация';
$txt[520] = 'Используется только для идентификации форумом.';
$txt[585] = 'Я принимаю';
$txt[586] = 'Я не принимаю';
$txt[633] = 'Внимание!';
$txt[634] = 'Только зарегистрированные пользователи имеют доступ в этот раздел.';
$txt[635] = 'Пожалуйста, войдите или';
$txt[636] = 'зарегистрируйтесь';
$txt[637] = 'на ' . $context['forum_name'] . '.';
// Use numeric entities in the below two strings.
$txt[701] = 'Вы можете изменить это после того как войдете в настройки Вашего профиля, или посетите эту страницу после входа:';
$txt[719] = 'Имя пользователя: ';
$txt[730] = 'Этот email адрес (%s) используется другим зарегистрированным пользователем. Если Вы думаете, что это ошибка, перейдите на страницу входа и воспользуйтесь напоминанием пароля используя этот адрес.';

$txt['login_hash_error'] = 'Политика паролей была изменена. Пожалуйста, смените Ваш пароль.';

$txt['register_age_confirmation'] = 'Я старше %d лет';

// Use numeric entities in the below six strings.
$txt['register_subject'] = 'Добро пожаловать на ' . $context['forum_name'];

// For the below three messages, %1$s is the display name, %2$s is the username, %3$s is the password, %4$s is the activation code, and %5$s is the activation link (the last two are only for activation.)
$txt['register_immediate_message'] = 'Вы зарегистрировались на ' . $context['forum_name'] . ', %1$s!' . "\n\n" . 'Ваше имя пользователя %2$s и пароль %3$s.' . "\n\n" . 'Вы можете изменить пароль после того как войдете в настройках Вашего профиля, или перейдя по этой ссылке после входа:' . "\n\n" . $scripturl . '?action=profile' . "\n\n" . $txt[130];
$txt['register_activate_message'] = 'Вы зарегистрированы на ' . $context['forum_name'] . ', %1$s!' . "\n\n" . 'Ваше имя пользователя %2$s и пароль %3$s (который может быть изменен позже.)' . "\n\n" . 'Перед тем как войти, Вам нужно активировать Вашу учетную запись. Для того чтобы это сделать, пожалуйста, перейдите по ссылке:' . "\n\n" . '%5$s' . "\n\n" . 'Если у Вас возникли проблемы с активацией, пожалуйста, используйте этот код "%4$s".' . "\n\n" . $txt[130];
$txt['register_pending_message'] = 'Ваш запрос о регистрации на ' . $context['forum_name'] . ' был принят, %1$s.' . "\n\n" . 'Имя пользователя %2$s и пароль %3$s.' . "\n\n" . 'Перед тем как Вы сможете войти и начать использовать форум, Ваш запрос должен рассмотреть и подтвердить Администратор форума.  После этого, Вы получите другое письмо с этого адреса.' . "\n\n" . $txt[130];

// For the below two messages, %1$s is the user's display name, %2$s is their username, %3$s is the activation code, and %4$s is the activation link (the last two are only for activation.)
$txt['resend_activate_message'] = 'Вы зарегистрированы на ' . $context['forum_name'] . ', %1$s!' . "\n\n" . 'Ваше имя пользователя "%2$s".' . "\n\n" . 'Перед тем как Вы сможете войти, сначала нужно активировать учетную запись. Для того чтобы это сделать перейдите по этой ссылке:' . "\n\n" . '%4$s' . "\n\n" . 'Если у Вас возникли проблемы с активацией, пожалуйста, используйте это код "%3$s".' . "\n\n" . $txt[130];
$txt['resend_pending_message'] = 'Ваш запрос о регистрации на ' . $context['forum_name'] . ' был получен, %1$s.' . "\n\n" . 'Имя пользователя под которым Вы зарегистрировались %2$s.' . "\n\n" . 'Перед тем как Вы сможете войти и начать использовать форум, Ваш запрос должен рассмотреть и подтвердить Администратор форума.  После этого, Вы получите другое письмо с этого адреса.' . "\n\n" . $txt[130];

$txt['ban_register_prohibited'] = 'Извините, Вам запрещено регистрироваться на этом форуме.';
$txt['under_age_registration_prohibited'] = 'Извините, но пользователям, не достигшим %d лет не разрешено регистрироваться на этом форуме.';

$txt['activate_account'] = 'Активация учетной записи';
$txt['activate_success'] = 'Ваша учетная запись активирована. Вы можете войти на форум.';
$txt['activate_not_completed1'] = 'Ваш email-адрес должен быть проверен, прежде чем Вы сможете войти.';
$txt['activate_not_completed2'] = 'Отправить повторно письмо для активации?';
$txt['activate_after_registration'] = 'Спасибо за регистрацию. Через несколько минут Вы получите письмо с ссылкой для активации Вашей учетной записи.';
$txt['invalid_userid'] = 'Пользователь не существует';
$txt['invalid_activation_code'] = 'Неправильный код активации';
$txt['invalid_activation_username'] = 'Имя пользователя или email';
$txt['invalid_activation_new'] = 'Если Вы зарегистрировались и указали неправильный email адрес, напишите новый и укажите Ваш пароль.';
$txt['invalid_activation_new_email'] = 'Новый email адрес';
$txt['invalid_activation_password'] = 'Старый пароль';
$txt['invalid_activation_resend'] = 'Отправить повторно код активации';
$txt['invalid_activation_known'] = 'Если Вы знаете Ваш код активации, пожалуйста, наберите его здесь.';
$txt['invalid_activation_retry'] = 'Код активации';
$txt['invalid_activation_submit'] = 'Активировать';

$txt['coppa_not_completed1'] = 'Администратор еще не получил согласия на Вашу регистрацию от родителей/опекуна.';
$txt['coppa_not_completed2'] = 'Нужны подробности?';

$txt['awaiting_delete_account'] = 'Ваша учетная запись была отмечена на удаление!<br />Если Вы хотите восстановить Вашу учетную запись, пожалуйста, реактивируйте Вашу учетную запись отметив &quot;Активировать мою учетную запись&quot; и войдите снова.';
$txt['undelete_account'] = 'Активировать мою учетную запись';

$txt['change_email_success'] = 'Ваш email адрес был изменен. Вам отправлено письмо для активации.';
$txt['resend_email_success'] = 'Новое письмо активации было удачно отправлено.';
// Use numeric entities in the below three strings.
$txt['change_password'] = 'Информация о новом пароле';
$txt['change_password_1'] = 'Информация для входа на';
$txt['change_password_2'] = 'был изменен и пароль сброшен. Ниже приведена информация для входа.';

$txt['maintenance3'] = 'Форум находится на Техническом Обслуживании.';

// These two are used as a javascript alert; please use international characters directly, not as entities.
$txt['register_agree'] = 'Пожалуйста, прочитайте соглашение прежде, чем Вы зарегистрируетесь.';
$txt['register_passwords_differ_js'] = 'Пароли не совпадают!';

$txt['approval_after_registration'] = 'Спасибо за регистрацию. Администратор должен подтвердить Вашу регистрацию, прежде чем Вы сможете использовать Вашу учетную запись. После подтверждения Вы получите письмо от Администратора.';

$txt['admin_settings_desc'] = 'Здесь Вы можете изменить настройки, связанные с регистрацией новых пользователей.';

$txt['admin_setting_registration_method'] = 'Способ регистрации новых пользователей';
$txt['admin_setting_registration_disabled'] = 'Регистрация запрещена';
$txt['admin_setting_registration_standard'] = 'Мгновенная регистрация';
$txt['admin_setting_registration_activate'] = 'Активация пользователя';
$txt['admin_setting_registration_approval'] = 'Одобрение пользователя';
$txt['admin_setting_notify_new_registration'] = 'Уведомлять Администратора при регистрации новых пользователей';
$txt['admin_setting_send_welcomeEmail'] = 'Отправлять приветствие новым пользователям';

$txt['admin_setting_password_strength'] = 'Требования к длине пароля пользователей';
$txt['admin_setting_password_strength_low'] = 'Низкое - минимум 4 символа';
$txt['admin_setting_password_strength_medium'] = 'Среднее - не может совпадать с именем пользователя';
$txt['admin_setting_password_strength_high'] = 'Высокое - сочетание различных символов';

$txt['admin_setting_image_verification_type'] = 'Сложность изображения визуальной проверки';
$txt['admin_setting_image_verification_type_desc'] = 'Более сложное изображение тяжелее обходить ботам';
$txt['admin_setting_image_verification_off'] = 'Запретить';
$txt['admin_setting_image_verification_vsimple'] = 'Очень простое - Обычный текст на изображении';
$txt['admin_setting_image_verification_simple'] = 'Простое - Накладывать цвет на символы, без шума';
$txt['admin_setting_image_verification_medium'] = 'Среднее - Накладывать цвет на символы, с шумами';
$txt['admin_setting_image_verification_high'] = 'Высокое - Наклонные символы, с значительными шумами';
$txt['admin_setting_image_verification_sample'] = 'Пример';
$txt['admin_setting_image_verification_nogd'] = '<b>Обратите внимание:</b> так как на данном сервере не установлена GD библиотека настройки сложности работать не будут.';

$txt['admin_setting_coppaAge'] = 'Минимальный возраст пользователя для успешной регистрации';
$txt['admin_setting_coppaAge_desc'] = '(0- без ограничения)';
$txt['admin_setting_coppaType'] = 'Действия, выполняемые при регистрации пользователя моложе указанного возраста';
$txt['admin_setting_coppaType_reject'] = 'Отменить регистрацию';
$txt['admin_setting_coppaType_approval'] = 'Запросить подтверждение у родителей/опекуна';
$txt['admin_setting_coppaPost'] = 'Email адрес, на который должно быть прислано одобрение о разрешении регистрации';
$txt['admin_setting_coppaPost_desc'] = 'Только предупредить, если пользователь моложе установленного возраста';
$txt['admin_setting_coppaFax'] = 'Номер факса, на который должно быть прислано одобрение о разрешении регистрации';
$txt['admin_setting_coppaPhone'] = 'Ваш контактный номер для связи с родителями';
$txt['admin_setting_coppa_require_contact'] = 'Вы также должны ввести почтовый адрес или номер телефона для контактов с родителями/опекунами, чтобы получить одобрение.';

$txt['admin_register'] = 'Регистрация нового пользователя';
$txt['admin_register_desc'] = 'Здесь Вы можете зарегистрировать новых пользователей. Рекомендуется отправить детали пользователей на их email.';
$txt['admin_register_username'] = 'Имя пользователя';
$txt['admin_register_email'] = 'email адрес';
$txt['admin_register_password'] = 'Пароль';
$txt['admin_register_username_desc'] = 'Имя нового пользователя';
$txt['admin_register_email_desc'] = 'Email адрес пользователя';
$txt['admin_register_password_desc'] = 'Пароль нового пользователя';
$txt['admin_register_email_detail'] = 'Отправить новый пароль пользователю';
$txt['admin_register_email_detail_desc'] = 'Требуется верный email адрес';
$txt['admin_register_email_activate'] = 'Требовать активации учетной записи';
$txt['admin_register_group'] = 'Основная группа пользователя';
$txt['admin_register_group_desc'] = 'Основная группа, к которой будет принадлежать новый пользователь';
$txt['admin_register_group_none'] = '(нет основной группы)';
$txt['admin_register_done'] = 'Пользователь %s удачно зарегистрирован!';

$txt['admin_browse_register_new'] = 'Зарегистрировать нового пользователя';

// Use numeric entities in the below three strings.
$txt['admin_notify_subject'] = 'Зарегистрирован новый пользователь';
$txt['admin_notify_profile'] = 'На Вашем форуме зарегистрирован новый пользователь, %s. Нажмите на ссылку, чтобы просмотреть его профиль.';
$txt['admin_notify_approval'] = 'Прежде чем пользователь сможет отправлять сообщения, учетная запись должна быть одобрена. Нажмите на ссылку чтобы одобрить пользователя.';

$txt['coppa_title'] = 'Форум с ограничением по возрасту';
$txt['coppa_after_registration'] = 'Спасибо за регистрацию на форуме ' . $context['forum_name'] . '.<br /><br />Поскольку Вы младше  {MINIMUM_AGE} лет, мы должны получить от Вашего родителя или опекуна разрешение, прежде чем Вы сможете использовать Вашу учетную запись. Чтобы активировать учетную запись, пожалуйста, распечатайте эту форму:';
$txt['coppa_form_link_popup'] = 'Открыть форму в новом окне';
$txt['coppa_form_link_download'] = 'Загрузить форму как текстовый файл';
$txt['coppa_send_to_one_option'] = 'Попросите родителей/опекунов заполнить форму:';
$txt['coppa_send_to_two_options'] = 'Попросите родителей/опекунов отправить заполненную форму на email или факс, указанные ниже:';
$txt['coppa_send_by_post'] = 'Отправить по следующему адресу:';
$txt['coppa_send_by_fax'] = 'Отправить факс по следующему номеру:';
$txt['coppa_send_by_phone'] = 'Альтернатива, пускай родители позвонят Администратору форума по телефону {PHONE_NUMBER}.';

$txt['coppa_form_title'] = 'Форма одобрения для регистрации на ' . $context['forum_name'];
$txt['coppa_form_address'] = 'Адрес';
$txt['coppa_form_date'] = 'Дата';
$txt['coppa_form_body'] = 'Я {PARENT_NAME},<br /><br /> разрешаю  {CHILD_NAME} (имя ребенка) зарегистрироваться на форуме: ' . $context['forum_name'] . ', с именем пользователя: {USER_NAME}.<br /><br />Я понимаю, что введенная личная информация {USER_NAME} может быть показана другим пользователям форума.<br /><br />Подпись:<br />{PARENT_NAME} (Родитель/Опекун).';

$txt['visual_verification_label'] = 'Визуальная проверка';
$txt['visual_verification_description'] = 'Наберите символы отображаемые на изображении';
$txt['visual_verification_sound'] = 'Прослушать';
$txt['visual_verification_sound_again'] = 'Проиграть снова';
$txt['visual_verification_sound_close'] = 'Закрыть окно';
$txt['visual_verification_request_new'] = 'Запросить другое изображение';
$txt['visual_verification_sound_direct'] = 'Проблемы с прослушиванием? Попробуйте прямую ссылку для прослушивания';

?>