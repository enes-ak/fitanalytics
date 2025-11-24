"""Static list of ready-to-use workout templates.

Each template references concrete exercise_library IDs so we can
duplicate them straight into the user's template_exercises table.
"""

POPULAR_TEMPLATES = [
    {
        "slug": "push_classic",
        "name": "Push Günü (Klasik)",
        "workout_type": "push",
        "description": "Göğüs, omuz ve triceps odaklı temel güç kombinasyonu.",
        "tags": ["Göğüs", "Omuz", "Triceps"],
        "exercises": [
            {"exercise_lib_id": 1, "name": "Barbell Bench Press", "sets": 4, "reps": 8, "weight": 60},
            {"exercise_lib_id": 5, "name": "Dumbbell Incline Press", "sets": 4, "reps": 10, "weight": 20},
            {"exercise_lib_id": 39, "name": "Barbell Overhead Press", "sets": 3, "reps": 8, "weight": 40},
            {"exercise_lib_id": 43, "name": "Dumbbell Yana Açış", "sets": 3, "reps": 15, "weight": 8},
            {"exercise_lib_id": 60, "name": "Kablo Triceps Pushdown", "sets": 3, "reps": 12, "weight": 25},
        ],
    },
    {
        "slug": "pull_strength",
        "name": "Pull Günü (Sırt + Kol)",
        "workout_type": "pull",
        "description": "Sırt kalınlığı ve biceps vurgulu çekiş rutini.",
        "tags": ["Sırt", "Biceps"],
        "exercises": [
            {"exercise_lib_id": 24, "name": "Barbell Bent-Over Row", "sets": 4, "reps": 8, "weight": 60},
            {"exercise_lib_id": 22, "name": "Lat Pulldown (Geniş)", "sets": 4, "reps": 10, "weight": 45},
            {"exercise_lib_id": 28, "name": "Tek Kol Dumbbell Row", "sets": 3, "reps": 12, "weight": 24},
            {"exercise_lib_id": 33, "name": "Face Pull", "sets": 3, "reps": 15, "weight": 20},
            {"exercise_lib_id": 50, "name": "Barbell Curl", "sets": 3, "reps": 10, "weight": 30},
            {"exercise_lib_id": 54, "name": "Hammer Curl", "sets": 3, "reps": 12, "weight": 14},
        ],
    },
    {
        "slug": "legs_hypertrophy",
        "name": "Legs Günü (Hipertrofi)",
        "workout_type": "legs",
        "description": "Quadriceps, hamstring ve baldırları dengeli çalıştırır.",
        "tags": ["Quadriceps", "Hamstring", "Calf"],
        "exercises": [
            {"exercise_lib_id": 65, "name": "Back Squat", "sets": 4, "reps": 6, "weight": 80},
            {"exercise_lib_id": 68, "name": "Leg Press", "sets": 4, "reps": 12, "weight": 120},
            {"exercise_lib_id": 72, "name": "Romanian Deadlift", "sets": 3, "reps": 10, "weight": 70},
            {"exercise_lib_id": 69, "name": "Walking Lunge", "sets": 3, "reps": 12, "weight": 20},
            {"exercise_lib_id": 74, "name": "Seated Leg Curl", "sets": 3, "reps": 15, "weight": 35},
            {"exercise_lib_id": 81, "name": "Standing Calf Raise", "sets": 4, "reps": 15, "weight": 40},
        ],
    },

    {
        "slug": "upper_power",
        "name": "Upper Body (Güç Odaklı)",
        "workout_type": "upper",
        "description": "Üst vücut için göğüs, sırt, omuz ve kol kaslarını sinerjik şekilde çalıştıran güç protokolü.",
        "tags": ["Göğüs", "Sırt", "Omuz", "Biceps", "Triceps"],
        "exercises": [
            {"exercise_lib_id": 1, "name": "Barbell Bench Press", "sets": 4, "reps": 6, "weight": 70},
            {"exercise_lib_id": 24, "name": "Barbell Bent-Over Row", "sets": 4, "reps": 8, "weight": 60},
            {"exercise_lib_id": 39, "name": "Barbell Overhead Press", "sets": 3, "reps": 6, "weight": 45},
            {"exercise_lib_id": 22, "name": "Lat Pulldown", "sets": 3, "reps": 10, "weight": 45},
            {"exercise_lib_id": 50, "name": "Barbell Curl", "sets": 3, "reps": 10, "weight": 30},
            {"exercise_lib_id": 60, "name": "Cable Triceps Pushdown", "sets": 3, "reps": 12, "weight": 25},
        ],
    },
    {
        "slug": "lower_strength",
        "name": "Lower Body (Strength)",
        "workout_type": "lower",
        "description": "Alt vücut için squat–hinge–lunge üçlemesiyle maksimum verimlilik getiren konsantre güç çalışması.",
        "tags": ["Quadriceps", "Hamstring", "Glute", "Calf"],
        "exercises": [
            {"exercise_lib_id": 65, "name": "Back Squat", "sets": 4, "reps": 5, "weight": 85},
            {"exercise_lib_id": 72, "name": "Romanian Deadlift", "sets": 4, "reps": 8, "weight": 75},
            {"exercise_lib_id": 69, "name": "Walking Lunge", "sets": 3, "reps": 12, "weight": 22},
            {"exercise_lib_id": 74, "name": "Seated Leg Curl", "sets": 3, "reps": 12, "weight": 40},
            {"exercise_lib_id": 81, "name": "Standing Calf Raise", "sets": 4, "reps": 15, "weight": 45},
        ],
    },
    {
        "slug": "fullbody_compact",
        "name": "Full Body (Kompakt Program)",
        "workout_type": "full",
        "description": "Tüm vücut kas gruplarını tek seansta optimize eden zaman-verimlilik odaklı bir yaklaşım.",
        "tags": ["Full Body", "Güç", "Hipertrofi"],
        "exercises": [
            {"exercise_lib_id": 1, "name": "Barbell Bench Press", "sets": 3, "reps": 8, "weight": 60},
            {"exercise_lib_id": 65, "name": "Back Squat", "sets": 3, "reps": 6, "weight": 80},
            {"exercise_lib_id": 24, "name": "Bent-Over Row", "sets": 3, "reps": 10, "weight": 55},
            {"exercise_lib_id": 39, "name": "Overhead Press", "sets": 3, "reps": 8, "weight": 40},
            {"exercise_lib_id": 69, "name": "Walking Lunge", "sets": 2, "reps": 12, "weight": 20},
            {"exercise_lib_id": 33, "name": "Face Pull", "sets": 2, "reps": 15, "weight": 20},
        ],
    },
]
