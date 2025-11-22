PRAGMA foreign_keys = ON;

-- Kullanıcılar
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Antrenman seansları
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

-- Antrenmandaki hareketler
CREATE TABLE IF NOT EXISTS exercises (
    exercise_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id      INTEGER NOT NULL,
    exercise_name   TEXT NOT NULL,
    target_muscle   TEXT,
    sets            INTEGER,
    reps            INTEGER,
    weight_kg       REAL,
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id)
);

-- Workout Template (şablon)
CREATE TABLE IF NOT EXISTS workout_templates (
    template_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    template_name TEXT NOT NULL,
    workout_type TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Template içindeki hareketler
CREATE TABLE IF NOT EXISTS template_exercises (
    template_exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id INTEGER NOT NULL,
    exercise_name TEXT NOT NULL,
    target_muscle TEXT NOT NULL,
    default_sets INTEGER,
    default_reps INTEGER,
    default_weight REAL,
    FOREIGN KEY (template_id) REFERENCES workout_templates(template_id)
);
