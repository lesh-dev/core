alter table `person` add column `nick_name` text;

create table xversion (
    db_version text
);

insert into xversion values('0.0.0');
update `xversion` set db_version = '2.13.1';
