INSERT INTO users (name) VALUES ('Enes');

-- Workout 1
INSERT INTO workouts (user_id, workout_date, workout_type, duration_min, notes)
VALUES
(1, '2025-01-10', 'push', 75, 'Göğüs + Omuz + Arka kol');

INSERT INTO exercises (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
VALUES
(1, 'Bench Press', 'Chest', 4, 10, 60),
(1, 'Incline Dumbbell Press', 'Chest', 3, 12, 32.5),
(1, 'Lateral Raise', 'Shoulders', 4, 15, 12),
(1, 'Triceps Pushdown', 'Triceps', 3, 12, 35);

-- Workout 2
INSERT INTO workouts (user_id, workout_date, workout_type, duration_min, notes)
VALUES
(1, '2025-01-12', 'pull', 70, 'Sırt + Arka kol');

INSERT INTO exercises (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
VALUES
(2, 'Barbell Row', 'Back', 4, 10, 70),
(2, 'Lat Pulldown', 'Back', 3, 12, 55),
(2, 'Face Pull', 'Rear Delts', 3, 15, 25);

-- Workout 3
INSERT INTO workouts (user_id, workout_date, workout_type, duration_min, notes)
VALUES
(1, '2025-01-14', 'legs', 80, 'Bacak günü');

INSERT INTO exercises (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
VALUES
(3, 'Squat', 'Legs', 5, 8, 90),
(3, 'Leg Press', 'Legs', 4, 10, 150),
(3, 'Leg Curl', 'Hamstrings', 3, 12, 40);
