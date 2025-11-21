-- === USER EKLE (login olabilmen için gerekli) ===
INSERT INTO users (name, email, password_hash)
VALUES (
    'sema',
    'sema@example.com',
    '$pbkdf2-sha256$29000$6g/O4IkYVEdhZDTxjUH/sA$eRSLu4S6mdtjVYcLowRRtQxq5m8LSZD1Jq7P3o9jGdc'
);

---------------------------------------------------
-- WORKOUT 1 — PUSH (Göğüs + Omuz + Triceps)
---------------------------------------------------
INSERT INTO workouts (user_id, workout_date, workout_type, duration_min, notes)
VALUES
(1, '2025-01-10', 'push', 70, 'Göğüs + Omuz + Arka kol');

INSERT INTO exercises (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
VALUES
(1, 'Bench Press', 'Chest', 4, 10, 20),
(1, 'Incline Dumbbell Press', 'Chest', 3, 12, 15),
(1, 'Cable Fly', 'Chest', 3, 15, 12),
(1, 'Shoulder Press', 'Shoulders', 4, 10, 12),
(1, 'Lateral Raise', 'Shoulders', 4, 12, 10),
(1, 'Triceps Rope Pushdown', 'Triceps', 4, 12, 20),
(1, 'Overhead Triceps Extension', 'Triceps', 3, 12, 18);

---------------------------------------------------
-- WORKOUT 2 — PULL (Sırt + Biceps + Rear Delts)
---------------------------------------------------
INSERT INTO workouts (user_id, workout_date, workout_type, duration_min, notes)
VALUES
(1, '2025-01-12', 'pull', 75, 'Sırt + Biceps + Arka omuz');

INSERT INTO exercises (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
VALUES
(2, 'Barbell Row', 'Back', 4, 10, 40),
(2, 'Lat Pulldown', 'Back', 3, 12, 35),
(2, 'Seated Row', 'Back', 3, 12, 40),
(2, 'Face Pull', 'Rear Delts', 3, 15, 12),
(2, 'Barbell Curl', 'Biceps', 4, 10, 20),
(2, 'Hammer Curl', 'Biceps', 3, 12, 18);

---------------------------------------------------
-- WORKOUT 3 — LEGS (Quadriceps + Hamstrings + Calves)
---------------------------------------------------
INSERT INTO workouts (user_id, workout_date, workout_type, duration_min, notes)
VALUES
(1, '2025-01-14', 'legs', 80, 'Bacak + Arka bacak');

INSERT INTO exercises (workout_id, exercise_name, target_muscle, sets, reps, weight_kg)
VALUES
(3, 'Squat', 'Legs', 5, 8, 90),
(3, 'Leg Press', 'Legs', 4, 12, 110),
(3, 'Leg Extension', 'Legs', 3, 15, 35),
(3, 'Romanian Deadlift', 'Hamstrings', 4, 10, 50),
(3, 'Leg Curl', 'Hamstrings', 3, 12, 35),
(3, 'Standing Calf Raise', 'Calves', 4, 15, 30);
