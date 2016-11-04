alter table `department` add column `department_changedby` text;
alter table `person` add column `person_changedby` text;
alter table `course` add column `course_changedby` text;
alter table `course_teachers` add column `course_teachers_changedby` text;
alter table `exam` add column `exam_changedby` text;
alter table `school` add column `school_changedby` text;
alter table `person_school` add column `person_school_changedby` text;
alter table `person_comment` add column `person_comment_changedby` text;

update `xversion` set db_version = '2.14.1';
