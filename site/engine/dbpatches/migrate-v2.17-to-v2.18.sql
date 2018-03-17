/*
@@ -53,6 +53,8 @@ create table person (
     achievements text,   -- достижения
     hobby text,          -- хобби

+    school_period text,     -- ориентировочные даты пребывания на школе
+
     lesh_ref text,       -- откуда узнали о школе (2.1+)

     forest_1 text,       -- 1-й выход в лес (2.3a+)
@@ -66,6 +66,7 @@ create table person (

     anketa_status text, -- former activity_status
         -- enum:(new, processed, declined, taken, duplicated, spam)
+    anketa_mode text,     -- источник анкеты

     user_agent text,    -- идентификатор браузера, с которого была подана анкета
*/

alter table `person` add column `school_period` text;
alter table `person` add column `anketa_mode` text;

update `xversion` set db_version = '2.18.1';
