/*
@@ -34,6 +34,7 @@ create table person (
     school_city text,   -- город, в котором находится школа
     ank_class text,     -- класс подачи заявки
     current_class text, -- текущий класс
+    teacher_fio text,      -- ФИО учителя ключевого предмета

     phone text,         -- телефон (городской)
     cellular text,      -- мобильный телефон
@@ -41,6 +42,10 @@ create table person (
     skype text,         -- skype
     social_profile text,  -- профиль ВКонтакте и т.п. (используемый!)

+    parent_fio text,       -- ФИО Законного Представителя (ЗП)
+    parent_phone text,     -- мобильный телефон ЗП
+    parent_email text,     -- контактный email ЗП
+
     is_teacher text, -- типично препод
     is_student text, -- типично школьник

*/

alter table `person` add column `teacher_fio` text;
alter table `person` add column `parent_fio` text;
alter table `person` add column `parent_phone` text;
alter table `person` add column `parent_email` text;

update `xversion` set db_version = '2.17.1';
