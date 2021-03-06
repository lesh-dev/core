--
-- PostgreSQL database dump
--

-- Dumped from database version 10.5 (Ubuntu 10.5-1.pgdg16.04+1)
-- Dumped by pg_dump version 10.5 (Ubuntu 10.5-1.pgdg16.04+1)

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;


SET default_tablespace = '';

SET default_with_oids = false;

SET TIME ZONE 'Europe/Moscow';

-- common tables
DROP TABLE IF EXISTS public.xversion;
DROP TABLE IF EXISTS public.pss;
DROP TABLE IF EXISTS public.notification;

DROP TABLE IF EXISTS public.contact;
DROP TABLE IF EXISTS public.solutions;
DROP TABLE IF EXISTS public.problems;
DROP TABLE IF EXISTS public.contestants;
DROP TABLE IF EXISTS public.submission;


CREATE TABLE public.contact (
    id serial primary key,
    person_id bigint NOT NULL,
    name text NOT NULL,
    value text NOT NULL
);
ALTER TABLE public.contact OWNER TO lesh;


CREATE TABLE public.contestants (
    contestants_id serial primary key,
    name text,
    mail text,
    phone text,
    parents text,
    address text,
    school text,
    level text,
    teacher_name text,
    work text,
    status text,
    contest_year text,
    fileexchange text
);
ALTER TABLE public.contestants OWNER TO lesh;


DROP TABLE IF EXISTS public.exam;
DROP TABLE IF EXISTS public.course_teachers;
DROP TABLE IF EXISTS public.course;
DROP TABLE IF EXISTS public.person_comment;
DROP TABLE IF EXISTS public.person_school;
DROP TABLE IF EXISTS public.person;
DROP TABLE IF EXISTS public.school;
DROP TABLE IF EXISTS public.department;



CREATE TABLE public.course (
    course_id serial primary key,
    course_title text,
    school_id bigint NOT NULL,
    course_cycle text,
    target_class text,
    course_desc text,
    course_comment text,
    course_created timestamp with time zone DEFAULT now(),
    course_modified timestamp with time zone DEFAULT now(),
    course_type text,
    course_area text,
    course_changedby text
);
ALTER TABLE public.course OWNER TO lesh;


CREATE TABLE public.course_teachers (
    course_teachers_id serial primary key,
    course_id bigint NOT NULL,
    course_teacher_id bigint NOT NULL,
    course_teachers_created timestamp with time zone DEFAULT now(),
    course_teachers_modified timestamp with time zone DEFAULT now(),
    course_teachers_changedby text
);
ALTER TABLE public.course_teachers OWNER TO lesh;


CREATE TABLE public.department (
    department_id serial primary key,
    department_title text,
    department_created timestamp with time zone DEFAULT now(),
    department_modified timestamp with time zone DEFAULT now(),
    department_changedby text
);
ALTER TABLE public.department OWNER TO lesh;


CREATE TABLE public.exam (
    exam_id serial primary key,
    student_person_id bigint NOT NULL,
    course_id bigint NOT NULL,
    exam_status text,
    deadline_date text,
    exam_comment text,
    exam_created timestamp with time zone DEFAULT now(),
    exam_modified timestamp with time zone DEFAULT now(),
    exam_changedby text
);
ALTER TABLE public.exam OWNER TO lesh;


CREATE TABLE public.notification (
    notification_id serial primary key,
    mail_group text,
    notification_text text,
    notification_html text
);
ALTER TABLE public.notification OWNER TO lesh;


CREATE TABLE public.person (
    person_id serial primary key,
    last_name text,
    first_name text,
    patronymic text,
    birth_date text,
    passport_data text,
    school text,
    school_city text,
    ank_class text,
    current_class text,
    phone text,
    cellular text,
    email text,
    skype text,
    social_profile text,
    is_teacher text,
    is_student text,
    favourites text,
    achievements text,
    hobby text,
    lesh_ref text,
    forest_1 text,
    forest_2 text,
    forest_3 text,
    tent_capacity text,
    tour_requisites text,
    anketa_status text,
    user_agent text,
    department_id bigint NOT NULL,
    person_created timestamp with time zone DEFAULT now(),
    person_modified timestamp with time zone DEFAULT now(),
    nick_name text,
    person_changedby text,
    teacher_fio text,
    parent_fio text,
    parent_phone text,
    parent_email text,
    school_period text,
    anketa_mode text
);
ALTER TABLE public.person OWNER TO lesh;


CREATE TABLE public.person_comment (
    person_comment_id serial primary key,
    comment_text text,
    blamed_person_id bigint NOT NULL,
    school_id bigint,
    owner_login text NOT NULL,
    record_acl text,
    person_comment_created timestamp with time zone DEFAULT now(),
    person_comment_modified timestamp with time zone DEFAULT now(),
    person_comment_deleted text,
    person_comment_changedby text
);
ALTER TABLE public.person_comment OWNER TO lesh;


CREATE TABLE public.person_school (
    person_school_id serial primary key,
    member_person_id bigint NOT NULL,
    member_department_id bigint NOT NULL,
    school_id bigint NOT NULL,
    is_student text,
    is_teacher text,
    curatorship text,
    current_class text,
    courses_needed varchar,
    person_school_created timestamp with time zone DEFAULT now(),
    person_school_modified timestamp with time zone DEFAULT now(),
    curator_group text,
    person_school_comment text,
    person_school_changedby text,
-- WTF???????????????????????????????
    frm text,
    tll text,
    school_coords text
);
ALTER TABLE public.person_school OWNER TO lesh;


CREATE TABLE public.problems (
    problems_id serial primary key,
    problem_name text,
    problem_html text,
    people text,
    criteria text,
    contest_year text
);
ALTER TABLE public.problems OWNER TO lesh;


CREATE TABLE public.pss (
    pss_id text NOT NULL,
    pss_value text,
    pss_created timestamp with time zone DEFAULT now(),
    pss_modified timestamp with time zone DEFAULT now(),
    pss_changedby text
);
ALTER TABLE public.pss OWNER TO lesh;


CREATE TABLE public.school (
    school_id serial primary key,
    school_title text,
    school_type text,
    school_date_start text,
    school_date_end text,
    school_created timestamp with time zone DEFAULT now(),
    school_modified timestamp with time zone DEFAULT now(),
    school_location text,
    school_changedby text,
    school_coords text
);
ALTER TABLE public.school OWNER TO lesh;


CREATE TABLE public.solutions (
    solutions_id serial primary key,
    problem_id text,
    contestant_id bigint,
    resolution_text text,
    resolution_author text,
    resolution_mark text,
    contest_year text
);
ALTER TABLE public.solutions OWNER TO lesh;


CREATE TABLE public.submission (
    submission_id serial primary key,
    mail text,
    attachment text,
    fileexchange text,
    submission_timestamp text, -- TODO utc?
    sender text,
    contest_year text,
    replied text,
    processed text
);


ALTER TABLE public.submission OWNER TO lesh;


CREATE TABLE public.xversion (
    db_version text
);


ALTER TABLE public.xversion OWNER TO lesh;


ALTER TABLE ONLY public.school
    ADD CONSTRAINT idx_school_pkey PRIMARY KEY (school_id);


ALTER TABLE ONLY public.contestants
    ADD CONSTRAINT idx_contestants_pkey PRIMARY KEY (contestants_id);


ALTER TABLE ONLY public.problems
    ADD CONSTRAINT idx_problems_pkey PRIMARY KEY (problems_id);


ALTER TABLE ONLY public.solutions
    ADD CONSTRAINT idx_solutions_pkey PRIMARY KEY (solutions_id);


ALTER TABLE ONLY public.notification
    ADD CONSTRAINT idx_notification_pkey PRIMARY KEY (notification_id);


ALTER TABLE ONLY public.course
    ADD CONSTRAINT idx_course_pkey PRIMARY KEY (course_id);


ALTER TABLE ONLY public.course_teachers
    ADD CONSTRAINT idx_course_teachers_pkey PRIMARY KEY (course_teachers_id);


ALTER TABLE ONLY public.department
    ADD CONSTRAINT idx_department_pkey PRIMARY KEY (department_id);


ALTER TABLE ONLY public.person
    ADD CONSTRAINT idx_person_pkey PRIMARY KEY (person_id);


ALTER TABLE ONLY public.person_school
    ADD CONSTRAINT idx_person_school_pkey PRIMARY KEY (person_school_id);


ALTER TABLE ONLY public.exam
    ADD CONSTRAINT idx_exam_pkey PRIMARY KEY (exam_id);


ALTER TABLE ONLY public.submission
    ADD CONSTRAINT idx_submission_pkey PRIMARY KEY (submission_id);


ALTER TABLE ONLY public.person_comment
    ADD CONSTRAINT idx_person_comment_pkey PRIMARY KEY (person_comment_id);


ALTER TABLE ONLY public.pss
    ADD CONSTRAINT idx_pss PRIMARY KEY (pss_id);


ALTER TABLE ONLY public.contact
    ADD CONSTRAINT idx_contact_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.contact
    ADD CONSTRAINT contact_person_id_fkey FOREIGN KEY (person_id) REFERENCES public.person(person_id);


ALTER TABLE ONLY public.course_teachers
    ADD CONSTRAINT course_teachers_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(course_id);


ALTER TABLE ONLY public.course_teachers
    ADD CONSTRAINT course_teachers_course_teacher_id_fkey FOREIGN KEY (course_teacher_id) REFERENCES public.person(person_id);


ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(course_id);


ALTER TABLE ONLY public.exam
    ADD CONSTRAINT exam_student_person_id_fkey FOREIGN KEY (student_person_id) REFERENCES public.person(person_id);


ALTER TABLE ONLY public.person_comment
    ADD CONSTRAINT person_comment_blamed_person_id_fkey FOREIGN KEY (blamed_person_id) REFERENCES public.person(person_id);


ALTER TABLE ONLY public.person_comment
    ADD CONSTRAINT person_comment_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.school(school_id);


ALTER TABLE ONLY public.person
    ADD CONSTRAINT person_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(department_id);


ALTER TABLE ONLY public.person_school
    ADD CONSTRAINT person_school_member_department_id_fkey FOREIGN KEY (member_department_id) REFERENCES public.department(department_id);


ALTER TABLE ONLY public.person_school
    ADD CONSTRAINT person_school_member_person_id_fkey FOREIGN KEY (member_person_id) REFERENCES public.person(person_id);


ALTER TABLE ONLY public.person_school
    ADD CONSTRAINT person_school_school_id_fkey FOREIGN KEY (school_id) REFERENCES public.school(school_id);

-- Fix such "bigint" as '2+прак'
ALTER TABLE public.person_school ALTER COLUMN courses_needed TYPE varchar;
