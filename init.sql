create table users
(
    user_id   serial
        primary key,
    login     varchar(80) not null,
    password  varchar(200) not null,
    user_type varchar(80) not null,
    email     varchar(80) not null,
    phone_nr  integer     not null,
    photo     varchar(80),
    logged_in boolean
);

alter table users
    owner to panda;

create table students
(
    student_id     integer     not null
        primary key
        references users,
    name           varchar(80) not null,
    surname        varchar(80) not null,
    gradebook_nr   integer     not null,
    class_name     varchar(80) not null,
    date_of_birth  date        not null,
    place_of_birth varchar(80) not null,
    address        varchar(80) not null
);

alter table students
    owner to panda;

create table teachers
(
    teacher_id   integer     not null
        primary key
        references users,
    name         varchar(80) not null,
    surname      varchar(80) not null,
    classroom_nr integer     not null,
    description  varchar(80) not null
);

alter table teachers
    owner to panda;

create table parents
(
    parent_id  integer     not null
        primary key
        references users,
    name       varchar(80) not null,
    surname    varchar(80) not null,
    student_id integer
        references students
);

alter table parents
    owner to panda;

create table announcements
(
    announcement_id serial
        primary key,
    description     varchar(1000),
    add_date        timestamp with time zone,
    in_archive      boolean,
    teacher_id      integer
        references teachers
);

alter table announcements
    owner to panda;

create table subjects
(
    subject_id   serial
        primary key,
    subject_name varchar(80) not null,
    class_name   varchar(80) not null,
    teacher_id   integer     not null
        references teachers
);

alter table subjects
    owner to panda;

create table classes
(
    class_name          varchar(10) not null
        primary key,
    homeroom_teacher_id integer
        references teachers,
    class_profile       varchar(50) not null
);

alter table classes
    owner to panda;

create table grades
(
    grade_id    serial
        primary key,
    subject_id  integer     not null
        references subjects,
    type        integer     not null,
    weight      integer     not null,
    student_id  integer     not null
        references students,
    description varchar(80) not null,
    add_date    timestamp with time zone,
    is_final    boolean     not null
);

alter table grades
    owner to panda;

create table lessons
(
    lesson_id   serial
        primary key,
    subject_id  integer                  not null
        references subjects,
    day_of_week varchar(15)              not null,
    start_time  timestamp with time zone not null,
    end_time    timestamp with time zone not null,
    building    varchar(20),
    test        varchar(80)
);

alter table lessons
    owner to panda;


-- USERS
INSERT INTO users (login, password, user_type, email, phone_nr, photo, logged_in) VALUES
('student1', 'scrypt:32768:8:1$yzF6rN6sjF2a9FFu$fcdbe0d9c54cbb00f486e5f8eabb9cabbf554bd1946aa8b9941d69d2987459bfae03c8cc7119b63a195b3ba6f6e6cd534698d3efd2c68b6c615503a650084ec1', 'student', 'student1@szkola.pl', 123456789, NULL, false),
('teacher1', 'scrypt:32768:8:1$yzF6rN6sjF2a9FFu$fcdbe0d9c54cbb00f486e5f8eabb9cabbf554bd1946aa8b9941d69d2987459bfae03c8cc7119b63a195b3ba6f6e6cd534698d3efd2c68b6c615503a650084ec1', 'teacher', 'teacher1@szkola.pl', 987654321, NULL, false),
('parent1', 'scrypt:32768:8:1$yzF6rN6sjF2a9FFu$fcdbe0d9c54cbb00f486e5f8eabb9cabbf554bd1946aa8b9941d69d2987459bfae03c8cc7119b63a195b3ba6f6e6cd534698d3efd2c68b6c615503a650084ec1', 'parent', 'parent1@szkola.pl', 456123789, NULL, false);

-- STUDENTS
INSERT INTO students (student_id, name, surname, gradebook_nr, class_name, date_of_birth, place_of_birth, address) VALUES
(1, 'Jan', 'Kowalski', 101, '3A', '2007-04-10', 'Warszawa', 'ul. Szkolna 1');

-- TEACHERS
INSERT INTO teachers (teacher_id, name, surname, classroom_nr, description) VALUES
(2, 'Anna', 'Nowak', 12, 'Matematyka');

-- PARENTS
INSERT INTO parents (parent_id, name, surname, student_id) VALUES
(3, 'Marek', 'Kowalski', 1);

-- ANNOUNCEMENTS
INSERT INTO announcements (description, add_date, in_archive, teacher_id) VALUES
('Drodzy uczniowie. Proszę przygotować się na sprawdzian z funkcji kwadratowej.', NOW() - INTERVAL '15 days', false, 2),
('Zebranie z rodzicami odbędzie się w przyszły wtorek o godzinie 17:00.', NOW() - INTERVAL '40 days', false, 2);

-- SUBJECTS
INSERT INTO subjects (subject_name, class_name, teacher_id) VALUES
('Matematyka', '3A', 2);

-- CLASSES
INSERT INTO classes (class_name, homeroom_teacher_id, class_profile) VALUES
('3A', 2, 'Matematyczno-fizyczny');

-- GRADES
INSERT INTO grades (subject_id, type, weight, student_id, description, add_date, is_final) VALUES
(1, 1, 2, 1, 'Sprawdzian – funkcje', NOW() - INTERVAL '10 days', false),
(1, 2, 1, 1, 'Kartkówka – pierwiastki', NOW() - INTERVAL '5 days', false);

-- LESSONS
INSERT INTO lessons (subject_id, day_of_week, start_time, end_time, building, test) VALUES
(1, 'Monday', NOW() + INTERVAL '1 hour', NOW() + INTERVAL '2 hours', 'Budynek A', 'Sprawdzian z równań'),
(1, 'Wednesday', NOW() + INTERVAL '3 hours', NOW() + INTERVAL '4 hours', 'Budynek A', NULL);
