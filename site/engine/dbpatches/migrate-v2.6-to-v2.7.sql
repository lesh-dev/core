/* Отделение */
create table department (
    department_id integer primary key autoincrement,
    department_title text,
    department_created text, -- utc timestamp
    department_modified text -- utc timestamp
);

alter table `school` add column `school_location` text;
