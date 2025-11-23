PRAGMA foreign_keys = ON;

INSERT INTO muscle_aliases (alias_text, muscle_id) VALUES
-- CHEST
('gogus',        (SELECT muscle_id FROM muscles WHERE code='CHEST_MID')),
('gögüs',        (SELECT muscle_id FROM muscles WHERE code='CHEST_MID')),
('gogus orta',   (SELECT muscle_id FROM muscles WHERE code='CHEST_MID')),
('orta gogus',   (SELECT muscle_id FROM muscles WHERE code='CHEST_MID')),
('ust gogus',    (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER')),
('üst göğüs',    (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER')),
('alt gogus',    (SELECT muscle_id FROM muscles WHERE code='CHEST_LOWER')),
('lower chest',  (SELECT muscle_id FROM muscles WHERE code='CHEST_LOWER')),
('upper chest',  (SELECT muscle_id FROM muscles WHERE code='CHEST_UPPER')),
('chest',        (SELECT muscle_id FROM muscles WHERE code='CHEST_MID')),

-- BACK / LATS
('sirt',        (SELECT muscle_id FROM muscles WHERE code='BACK_MID')),
('sırt',        (SELECT muscle_id FROM muscles WHERE code='BACK_MID')),
('ust sirt',    (SELECT muscle_id FROM muscles WHERE code='BACK_UPPER')),
('üst sırt',    (SELECT muscle_id FROM muscles WHERE code='BACK_UPPER')),
('alt sirt',    (SELECT muscle_id FROM muscles WHERE code='BACK_LOWER')),
('alt sırt',    (SELECT muscle_id FROM muscles WHERE code='BACK_LOWER')),
('kanat',       (SELECT muscle_id FROM muscles WHERE code='BACK_LATS')),
('lats',        (SELECT muscle_id FROM muscles WHERE code='BACK_LATS')),
('lat',         (SELECT muscle_id FROM muscles WHERE code='BACK_LATS')),

-- SHOULDERS
('omuz',        (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT')),
('on omuz',     (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT')),
('ön omuz',     (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT')),
('yan omuz',    (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_SIDE')),
('arka omuz',   (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_REAR')),
('delt',        (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT')),
('deltoid',     (SELECT muscle_id FROM muscles WHERE code='SHOULDERS_FRONT')),

-- ARMS
('biseps',      (SELECT muscle_id FROM muscles WHERE code='BICEPS')),
('biceps',      (SELECT muscle_id FROM muscles WHERE code='BICEPS')),
('triceps',     (SELECT muscle_id FROM muscles WHERE code='TRICEPS')),
('triseps',     (SELECT muscle_id FROM muscles WHERE code='TRICEPS')),
('on kol',      (SELECT muscle_id FROM muscles WHERE code='FOREARMS')),
('ön kol',      (SELECT muscle_id FROM muscles WHERE code='FOREARMS')),
('onkul',       (SELECT muscle_id FROM muscles WHERE code='FOREARMS')),
('forearm',     (SELECT muscle_id FROM muscles WHERE code='FOREARMS')),

-- LEGS
('bacak',        (SELECT muscle_id FROM muscles WHERE code='QUADS')),
('quadriceps',   (SELECT muscle_id FROM muscles WHERE code='QUADS')),
('quad',         (SELECT muscle_id FROM muscles WHERE code='QUADS')),
('hamstring',    (SELECT muscle_id FROM muscles WHERE code='HAMSTRINGS')),
('hamstringler', (SELECT muscle_id FROM muscles WHERE code='HAMSTRINGS')),
('kalca',        (SELECT muscle_id FROM muscles WHERE code='GLUTES')),
('kalça',        (SELECT muscle_id FROM muscles WHERE code='GLUTES')),
('glute',        (SELECT muscle_id FROM muscles WHERE code='GLUTES')),
('glutes',       (SELECT muscle_id FROM muscles WHERE code='GLUTES')),
('ic bacak',     (SELECT muscle_id FROM muscles WHERE code='ADDUCTORS')),
('iç bacak',     (SELECT muscle_id FROM muscles WHERE code='ADDUCTORS')),

-- CALVES
('baldir',        (SELECT muscle_id FROM muscles WHERE code='CALVES_GASTRO')),
('baldır',        (SELECT muscle_id FROM muscles WHERE code='CALVES_GASTRO')),
('baldur',        (SELECT muscle_id FROM muscles WHERE code='CALVES_GASTRO')),
('calf',          (SELECT muscle_id FROM muscles WHERE code='CALVES_GASTRO')),
('calves',        (SELECT muscle_id FROM muscles WHERE code='CALVES_GASTRO')),

-- ABS / CORE
('karin',          (SELECT muscle_id FROM muscles WHERE code='ABS_UPPER')),
('karın',          (SELECT muscle_id FROM muscles WHERE code='ABS_UPPER')),
('alt karin',      (SELECT muscle_id FROM muscles WHERE code='ABS_LOWER')),
('alt karın',      (SELECT muscle_id FROM muscles WHERE code='ABS_LOWER')),
('ust karin',      (SELECT muscle_id FROM muscles WHERE code='ABS_UPPER')),
('üst karın',      (SELECT muscle_id FROM muscles WHERE code='ABS_UPPER')),
('oblik',          (SELECT muscle_id FROM muscles WHERE code='OBLIQUES')),
('obliques',       (SELECT muscle_id FROM muscles WHERE code='OBLIQUES')),
('core',           (SELECT muscle_id FROM muscles WHERE code='CORE_TRANSVERSE'));
