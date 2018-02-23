/*
@@ -53,6 +53,8 @@ create table person (
     achievements text,   -- достижения
     hobby text,          -- хобби

+    school_period text,     -- ориентировочные даты пребывания на школе
+
     lesh_ref text,       -- откуда узнали о школе (2.1+)

     forest_1 text,       -- 1-й выход в лес (2.3a+)
*/

alter table `person` add column `school_period` text;

update `xversion` set db_version = '2.18.1';
