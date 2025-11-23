PRAGMA foreign_keys = ON;

---------------------------------------------------------------
-- USERS
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT NOT NULL,
    email          TEXT UNIQUE NOT NULL,
    password_hash  TEXT NOT NULL
);

---------------------------------------------------------------
-- WORKOUTS
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS workouts (
    workout_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    workout_date    DATE NOT NULL,
    workout_type    TEXT NOT NULL CHECK (
                        workout_type IN ('push', 'pull', 'legs', 'upper', 'lower', 'full', 'other')
                    ),
    notes           TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

---------------------------------------------------------------
-- EXERCISES (User logs)
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercises (
    exercise_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id       INTEGER NOT NULL,
    exercise_name    TEXT NOT NULL,           -- ham text
    muscle_id        INTEGER NOT NULL,        -- canonical muscle
    exercise_lib_id  INTEGER,                 -- link to library (optional)
    sets             INTEGER,
    reps             INTEGER,
    weight_kg        REAL,
    volume           REAL,                    -- sets * reps * weight
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id),
    FOREIGN KEY (muscle_id) REFERENCES muscles(muscle_id),
    FOREIGN KEY (exercise_lib_id) REFERENCES exercise_library(exercise_lib_id)
);

---------------------------------------------------------------
-- WORKOUT TEMPLATES
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS workout_templates (
    template_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER NOT NULL,
    template_name  TEXT NOT NULL,
    workout_type   TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

---------------------------------------------------------------
-- TEMPLATE EXERCISES
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS template_exercises (
    template_exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id          INTEGER NOT NULL,
    exercise_lib_id      INTEGER NOT NULL,
    exercise_name        TEXT NOT NULL,
    muscle_id            INTEGER NOT NULL,
    default_sets         INTEGER,
    default_reps         INTEGER,
    default_weight       REAL,
    FOREIGN KEY (template_id) REFERENCES workout_templates(template_id),
    FOREIGN KEY (exercise_lib_id) REFERENCES exercise_library(exercise_lib_id),
    FOREIGN KEY (muscle_id) REFERENCES muscles(muscle_id)
);
---------------------------------------------------------------
-- CANONICAL MUSCLES
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS muscles (
    muscle_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    code            TEXT UNIQUE NOT NULL,     -- CHEST_UPPER, BACK_LATS...
    primary_region  TEXT NOT NULL,            -- CHEST, BACK, ARMS, LEGS, CORE...
    sub_region      TEXT,                     -- UPPER, LOWER, LATS, OBLIQUES...
    name_en         TEXT NOT NULL,
    name_tr         TEXT NOT NULL
);

---------------------------------------------------------------
-- EXERCISE LIBRARY (Curated list)
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercise_library (
    exercise_lib_id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug            TEXT UNIQUE NOT NULL,
    name_en         TEXT NOT NULL,
    name_tr         TEXT NOT NULL,
    muscle_id       INTEGER NOT NULL,
    is_compound     INTEGER DEFAULT 1,
    equipment       TEXT,
    difficulty      TEXT,
    FOREIGN KEY (muscle_id) REFERENCES muscles(muscle_id)
);

---------------------------------------------------------------
-- EXERCISE ALIASES (different names → same library item)
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercise_aliases (
    alias_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_lib_id INTEGER NOT NULL,
    alias_text      TEXT NOT NULL,
    FOREIGN KEY (exercise_lib_id) REFERENCES exercise_library(exercise_lib_id)
);

---------------------------------------------------------------
-- EXERCISE MEDIA (optional GIFs, images)
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercise_media (
    media_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_lib_id INTEGER NOT NULL,
    media_type      TEXT NOT NULL,
    file_name       TEXT NOT NULL,
    FOREIGN KEY (exercise_lib_id) REFERENCES exercise_library(exercise_lib_id)
);

---------------------------------------------------------------
-- MUSCLE ALIASES (Göğüs, chest, gogus → CHEST_MID)
---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS muscle_aliases (
    alias_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    alias_text   TEXT UNIQUE NOT NULL,
    muscle_id    INTEGER NOT NULL,
    FOREIGN KEY (muscle_id) REFERENCES muscles(muscle_id)
);
