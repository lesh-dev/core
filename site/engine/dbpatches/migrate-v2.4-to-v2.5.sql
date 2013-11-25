alter table `contestants` add column `contest_year` text;
alter table `problems` add column `contest_year` text;
alter table `solutions` add column `contest_year` text;
drop table `sol_discussion`;