/*
    Присланное: может содержать пачки работ,
    подлежит дальнейшей обработке и расклеиванию.
    v2.9
*/
create table submission(
    submission_id integer primary key autoincrement,
    mail text,
    attachment text,
    fileexchange text,
    submission_timestamp text,
    sender text,
    replied text,
    processed text,
    contest_year text
);

/*
    Участники олимпиады (заполняется де-факто вручную,
    т.к. работы грузятся пачками и их надо расклеивать).
*/
create table contestants(
    contestants_id integer primary key autoincrement,
    name text,
    mail text,
    phone text,
    parents text,
    address text,
    school text,
    level text,
    teacher_name text,
    work text,
    fileexchange text,
    status text,
    contest_year text
);

/*
    Задачи олипиады
*/
create table problems(
    problems_id integer primary key autoincrement,
    contest_year text,
    problem_name text,
    problem_html text,
    people text,
    criteria text
);

/*
    Проверка олимпиады
*/
create table solutions(
    solutions_id integer primary key autoincrement,
    problem_id, -- TODO: FK
    contest_year text,
    contestant_id integer,
    resolution_text text,
    resolution_author text,
    resolution_mark text
);
