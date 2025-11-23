PRAGMA foreign_keys = ON;

-- ========== CHEST (GÖĞÜS) ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('barbell_flat_bench_press', 'Barbell Flat Bench Press', 'Barbell Düz Bench Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 1, 'barbell', 'intermediate'),
('barbell_incline_bench_press', 'Barbell Incline Bench Press', 'Barbell İncline Bench Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER'), 1, 'barbell', 'intermediate'),
('barbell_decline_bench_press', 'Barbell Decline Bench Press', 'Barbell Decline Bench Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_LOWER'), 1, 'barbell', 'intermediate'),
('dumbbell_flat_bench_press', 'Dumbbell Flat Bench Press', 'Dumbbell Düz Bench Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 1, 'dumbbell', 'intermediate'),
('dumbbell_incline_press', 'Dumbbell Incline Press', 'Dumbbell İncline Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER'), 1, 'dumbbell', 'intermediate'),
('dumbbell_decline_press', 'Dumbbell Decline Press', 'Dumbbell Decline Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_LOWER'), 1, 'dumbbell', 'intermediate'),
('machine_chest_press', 'Machine Chest Press', 'Makine Chest Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 1, 'machine', 'beginner'),
('smith_flat_bench_press', 'Smith Machine Bench Press', 'Smith Bench Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 1, 'smith', 'beginner'),
('smith_incline_press', 'Smith Incline Press', 'Smith İncline Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER'), 1, 'smith', 'beginner'),
('push_up', 'Push-Up', 'Şınav',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 1, 'bodyweight', 'beginner'),
('incline_push_up', 'Incline Push-Up', 'İncline Şınav',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER'), 1, 'bodyweight', 'beginner'),
('decline_push_up', 'Decline Push-Up', 'Decline Şınav',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_LOWER'), 1, 'bodyweight', 'intermediate'),
('dumbbell_fly_flat', 'Dumbbell Fly (Flat)', 'Dumbbell Fly (Düz)',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 0, 'dumbbell', 'intermediate'),
('dumbbell_fly_incline', 'Dumbbell Fly (Incline)', 'Dumbbell Fly (İncline)',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER'), 0, 'dumbbell', 'intermediate'),
('cable_crossover_high_to_low', 'Cable Crossover High to Low', 'Kablo Crossover (Yukarıdan Aşağı)',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_LOWER'), 0, 'cable', 'intermediate'),
('cable_crossover_low_to_high', 'Cable Crossover Low to High', 'Kablo Crossover (Aşağıdan Yukarı)',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER'), 0, 'cable', 'intermediate'),
('pec_deck_fly', 'Pec Deck Fly', 'Pec Deck Fly',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 0, 'machine', 'beginner'),
('single_arm_cable_chest_press', 'Single Arm Cable Chest Press', 'Tek Kol Kablo Chest Press',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_MID'), 1, 'cable', 'intermediate'),
('dip_chest_lean', 'Chest Dips (Forward Lean)', 'Göğüs Dips (Öne Eğilerek)',
 (SELECT muscle_id FROM muscles WHERE code='CHEST_LOWER'), 1, 'bodyweight', 'advanced');


-- ========== BACK / LATS / TRAPS ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('pull_up', 'Pull-Up', 'Barfiks',
 (SELECT muscle_id FROM muscles WHERE code='BACK_LATS'), 1, 'bodyweight', 'intermediate'),
('chin_up', 'Chin-Up', 'Chin-Up',
 (SELECT muscle_id FROM muscles WHERE code='BACK_LATS'), 1, 'bodyweight', 'intermediate'),
('lat_pulldown_wide', 'Lat Pulldown (Wide Grip)', 'Lat Pulldown (Geniş Tutuş)',
 (SELECT muscle_id FROM muscles WHERE code='BACK_LATS'), 1, 'machine', 'beginner'),
('lat_pulldown_close', 'Lat Pulldown (Close Grip)', 'Lat Pulldown (Dar Tutuş)',
 (SELECT muscle_id FROM muscles WHERE code='BACK_LATS'), 1, 'machine', 'beginner'),
('barbell_bent_over_row', 'Barbell Bent-Over Row', 'Barbell Bent-Over Row',
 (SELECT muscle_id FROM muscles WHERE code='BACK_MID'), 1, 'barbell', 'intermediate'),
('pendlay_row', 'Pendlay Row', 'Pendlay Row',
 (SELECT muscle_id FROM muscles WHERE code='BACK_MID'), 1, 'barbell', 'advanced'),
('t_bar_row', 'T-Bar Row', 'T-Bar Row',
 (SELECT muscle_id FROM muscles WHERE code='BACK_MID'), 1, 'machine', 'intermediate'),
('seated_cable_row', 'Seated Cable Row', 'Oturur Kablo Row',
 (SELECT muscle_id FROM muscles WHERE code='BACK_MID'), 1, 'cable', 'beginner'),
('one_arm_dumbbell_row', 'One-Arm Dumbbell Row', 'Tek Kol Dumbbell Row',
 (SELECT muscle_id FROM muscles WHERE code='BACK_MID'), 1, 'dumbbell', 'beginner'),
('machine_row', 'Machine Row', 'Makine Row',
 (SELECT muscle_id FROM muscles WHERE code='BACK_MID'), 1, 'machine', 'beginner'),
('deadlift_conventional', 'Conventional Deadlift', 'Conventional Deadlift',
 (SELECT muscle_id FROM muscles WHERE code='BACK_LOWER'), 1, 'barbell', 'advanced'),
('rack_pull', 'Rack Pull', 'Rack Pull',
 (SELECT muscle_id FROM muscles WHERE code='BACK_LOWER'), 1, 'barbell', 'advanced'),
('good_morning', 'Barbell Good Morning', 'Barbell Good Morning',
 (SELECT muscle_id FROM muscles WHERE code='BACK_LOWER'), 1, 'barbell', 'advanced'),
('face_pull', 'Face Pull', 'Face Pull',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_REAR'), 0, 'cable', 'beginner'),
('dumbbell_shrug', 'Dumbbell Shrug', 'Dumbbell Shrug',
 (SELECT muscle_id FROM muscles WHERE code='TRAPS_UPPER'), 0, 'dumbbell', 'beginner'),
('barbell_shrug', 'Barbell Shrug', 'Barbell Shrug',
 (SELECT muscle_id FROM muscles WHERE code='TRAPS_UPPER'), 0, 'barbell', 'intermediate'),
('upright_row_barbell', 'Barbell Upright Row', 'Barbell Upright Row',
 (SELECT muscle_id FROM muscles WHERE code='TRAPS_UPPER'), 0, 'barbell', 'intermediate'),
('reverse_fly_dumbbell', 'Dumbbell Reverse Fly', 'Dumbbell Reverse Fly',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_REAR'), 0, 'dumbbell', 'beginner'),
('reverse_fly_machine', 'Reverse Fly Machine', 'Reverse Fly Makinesi',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_REAR'), 0, 'machine', 'beginner');


-- ========== SHOULDERS ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('overhead_press_barbell', 'Barbell Overhead Press', 'Barbell Overhead Press',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT'), 1, 'barbell', 'intermediate'),
('overhead_press_dumbbell', 'Dumbbell Shoulder Press', 'Dumbbell Omuz Press',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT'), 1, 'dumbbell', 'beginner'),
('arnold_press', 'Arnold Press', 'Arnold Press',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT'), 1, 'dumbbell', 'intermediate'),
('machine_shoulder_press', 'Machine Shoulder Press', 'Makine Omuz Press',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT'), 1, 'machine', 'beginner'),
('lateral_raise_dumbbell', 'Dumbbell Lateral Raise', 'Dumbbell Yana Açış',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_SIDE'), 0, 'dumbbell', 'beginner'),
('lateral_raise_cable', 'Cable Lateral Raise', 'Kablo Yana Açış',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_SIDE'), 0, 'cable', 'intermediate'),
('front_raise_dumbbell', 'Dumbbell Front Raise', 'Dumbbell Öne Kaldırış',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT'), 0, 'dumbbell', 'beginner'),
('front_raise_plate', 'Plate Front Raise', 'Plaka Öne Kaldırış',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT'), 0, 'other', 'beginner'),
('rear_delt_fly_dumbbell', 'Rear Delt Fly (Dumbbell)', 'Dumbbell Arka Omuz Fly',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_REAR'), 0, 'dumbbell', 'beginner'),
('rear_delt_fly_cable', 'Rear Delt Cable Fly', 'Kablo Arka Omuz Fly',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_REAR'), 0, 'cable', 'intermediate'),
('reverse_pec_deck', 'Reverse Pec Deck', 'Reverse Pec Deck',
 (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_REAR'), 0, 'machine', 'beginner');


-- ========== BICEPS ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('barbell_curl', 'Barbell Curl', 'Barbell Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'barbell', 'beginner'),
('ez_bar_curl', 'EZ Bar Curl', 'EZ Bar Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'barbell', 'beginner'),
('dumbbell_bicep_curl', 'Dumbbell Bicep Curl', 'Dumbbell Biceps Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'dumbbell', 'beginner'),
('incline_dumbbell_curl', 'Incline Dumbbell Curl', 'İncline Dumbbell Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'dumbbell', 'intermediate'),
('hammer_curl', 'Hammer Curl', 'Hammer Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'dumbbell', 'beginner'),
('concentration_curl', 'Concentration Curl', 'Konsantrasyon Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'dumbbell', 'beginner'),
('preacher_curl', 'Preacher Curl', 'Preacher Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'machine', 'intermediate'),
('cable_curl', 'Cable Curl', 'Kablo Curl',
 (SELECT muscle_id FROM muscles WHERE code='BICEPS'), 0, 'cable', 'intermediate');


-- ========== TRICEPS ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('close_grip_bench_press', 'Close-Grip Bench Press', 'Dar Tutuş Bench Press',
 (SELECT muscle_id FROM muscles WHERE code='TRICEPS'), 1, 'barbell', 'intermediate'),
('triceps_dip', 'Triceps Dips', 'Triceps Dips',
 (SELECT muscle_id FROM muscles WHERE code='TRICEPS'), 1, 'bodyweight', 'intermediate'),
('cable_triceps_pushdown', 'Cable Triceps Pushdown', 'Kablo Triceps Pushdown',
 (SELECT muscle_id FROM muscles WHERE code='TRICEPS'), 0, 'cable', 'beginner'),
('overhead_triceps_extension_dumbbell', 'Overhead Triceps Extension (Dumbbell)', 'Dumbbell Overhead Triceps',
 (SELECT muscle_id FROM muscles WHERE code='TRICEPS'), 0, 'dumbbell', 'beginner'),
('skullcrusher_ezbar', 'EZ Bar Skullcrusher', 'EZ Bar Skullcrusher',
 (SELECT muscle_id FROM muscles WHERE code='TRICEPS'), 0, 'barbell', 'intermediate'),
('rope_overhead_triceps', 'Rope Overhead Triceps Extension', 'Halat Overhead Triceps',
 (SELECT muscle_id FROM muscles WHERE code='TRICEPS'), 0, 'cable', 'intermediate'),
('bench_dip', 'Bench Dip', 'Bench Dip',
 (SELECT muscle_id FROM muscles WHERE code='TRICEPS'), 1, 'bodyweight', 'beginner');


-- ========== LEGS ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('back_squat', 'Back Squat', 'Back Squat',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 1, 'barbell', 'intermediate'),
('front_squat', 'Front Squat', 'Front Squat',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 1, 'barbell', 'advanced'),
('hack_squat_machine', 'Hack Squat Machine', 'Hack Squat Makinesi',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 1, 'machine', 'intermediate'),
('leg_press', 'Leg Press', 'Leg Press',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 1, 'machine', 'beginner'),
('walking_lunge_dumbbell', 'Walking Lunge (Dumbbell)', 'Dumbbell Yürüyüş Lunge',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 1, 'dumbbell', 'intermediate'),
('bulgarian_split_squat', 'Bulgarian Split Squat', 'Bulgarian Split Squat',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 1, 'dumbbell', 'intermediate'),
('leg_extension', 'Leg Extension', 'Leg Extension',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 0, 'machine', 'beginner'),
('romanian_deadlift_barbell', 'Romanian Deadlift', 'Romanian Deadlift',
 (SELECT muscle_id FROM muscles WHERE code='HAMSTRINGS'), 1, 'barbell', 'intermediate'),
('lying_leg_curl', 'Lying Leg Curl', 'Yatarak Leg Curl',
 (SELECT muscle_id FROM muscles WHERE code='HAMSTRINGS'), 0, 'machine', 'beginner'),
('seated_leg_curl', 'Seated Leg Curl', 'Oturur Leg Curl',
 (SELECT muscle_id FROM muscles WHERE code='HAMSTRINGS'), 0, 'machine', 'beginner'),
('glute_bridge_barbell', 'Barbell Glute Bridge', 'Barbell Glute Bridge',
 (SELECT muscle_id FROM muscles WHERE code='GLUTES'), 1, 'barbell', 'beginner'),
('hip_thrust_barbell', 'Barbell Hip Thrust', 'Barbell Hip Thrust',
 (SELECT muscle_id FROM muscles WHERE code='GLUTES'), 1, 'barbell', 'intermediate'),
('cable_pull_through', 'Cable Pull-Through', 'Kablo Pull-Through',
 (SELECT muscle_id FROM muscles WHERE code='GLUTES'), 1, 'cable', 'intermediate'),
('sumo_deadlift', 'Sumo Deadlift', 'Sumo Deadlift',
 (SELECT muscle_id FROM muscles WHERE code='GLUTES'), 1, 'barbell', 'advanced'),
('adductor_machine', 'Adductor Machine', 'Adduktor Makinesi',
 (SELECT muscle_id FROM muscles WHERE code='ADDUCTORS'), 0, 'machine', 'beginner'),
('cable_adduction', 'Cable Hip Adduction', 'Kablo İç Bacak',
 (SELECT muscle_id FROM muscles WHERE code='ADDUCTORS'), 0, 'cable', 'intermediate'),
('standing_calf_raise', 'Standing Calf Raise', 'Standing Calf Raise',
 (SELECT muscle_id FROM muscles WHERE code='CALVES_GASTRO'), 0, 'machine', 'beginner'),
('seated_calf_raise', 'Seated Calf Raise', 'Seated Calf Raise',
 (SELECT muscle_id FROM muscles WHERE code='CALVES_SOLEUS'), 0, 'machine', 'beginner'),
('donkey_calf_raise', 'Donkey Calf Raise', 'Donkey Calf Raise',
 (SELECT muscle_id FROM muscles WHERE code='CALVES_GASTRO'), 0, 'machine', 'intermediate'),
('bodyweight_squat', 'Bodyweight Squat', 'Vücut Ağırlığı Squat',
 (SELECT muscle_id FROM muscles WHERE code='QUADS'), 1, 'bodyweight', 'beginner');


-- ========== CORE / ABS / OBLIQUES ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('crunch', 'Crunch', 'Crunch',
 (SELECT muscle_id FROM muscles WHERE code='ABS_UPPER'), 0, 'bodyweight', 'beginner'),
('reverse_crunch', 'Reverse Crunch', 'Reverse Crunch',
 (SELECT muscle_id FROM muscles WHERE code='ABS_LOWER'), 0, 'bodyweight', 'beginner'),
('hanging_leg_raise', 'Hanging Leg Raise', 'Barfiks Bacağını Kaldırma',
 (SELECT muscle_id FROM muscles WHERE code='ABS_LOWER'), 0, 'bodyweight', 'intermediate'),
('lying_leg_raise', 'Lying Leg Raise', 'Yatarak Bacak Kaldırma',
 (SELECT muscle_id FROM muscles WHERE code='ABS_LOWER'), 0, 'bodyweight', 'beginner'),
('plank', 'Plank', 'Plank',
 (SELECT muscle_id FROM muscles WHERE code='CORE_TRANSVERSE'), 0, 'bodyweight', 'beginner'),
('side_plank', 'Side Plank', 'Yan Plank',
 (SELECT muscle_id FROM muscles WHERE code='OBLIQUES'), 0, 'bodyweight', 'beginner'),
('russian_twist', 'Russian Twist', 'Russian Twist',
 (SELECT muscle_id FROM muscles WHERE code='OBLIQUES'), 0, 'other', 'intermediate'),
('cable_woodchop', 'Cable Woodchop', 'Kablo Woodchop',
 (SELECT muscle_id FROM muscles WHERE code='OBLIQUES'), 0, 'cable', 'intermediate'),
('ab_wheel_rollout', 'Ab Wheel Rollout', 'Ab Wheel Rollout',
 (SELECT muscle_id FROM muscles WHERE code='CORE_TRANSVERSE'), 0, 'other', 'advanced'),
('sit_up_decline', 'Decline Sit-Up', 'Decline Mekik',
 (SELECT muscle_id FROM muscles WHERE code='ABS_UPPER'), 0, 'bodyweight', 'intermediate');


-- ========== FULL BODY / COMPOUND ==========
INSERT INTO exercise_library (slug, name_en, name_tr, muscle_id, is_compound, equipment, difficulty)
VALUES
('clean_and_press', 'Clean and Press', 'Clean and Press',
 (SELECT muscle_id FROM muscles WHERE code='FULL_BODY'), 1, 'barbell', 'advanced'),
('snatch', 'Snatch', 'Snatch',
 (SELECT muscle_id FROM muscles WHERE code='FULL_BODY'), 1, 'barbell', 'advanced'),
('kettlebell_swing', 'Kettlebell Swing', 'Kettlebell Swing',
 (SELECT muscle_id FROM muscles WHERE code='FULL_BODY'), 1, 'kettlebell', 'intermediate'),
('burpee', 'Burpee', 'Burpee',
 (SELECT muscle_id FROM muscles WHERE code='FULL_BODY'), 1, 'bodyweight', 'intermediate'),
('thruster_barbell', 'Barbell Thruster', 'Barbell Thruster',
 (SELECT muscle_id FROM muscles WHERE code='FULL_BODY'), 1, 'barbell', 'advanced');
