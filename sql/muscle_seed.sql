PRAGMA foreign_keys = ON;

INSERT INTO muscles (code, primary_region, sub_region, name_en, name_tr) VALUES
-- CHEST
('CHEST_UPPER','CHEST','UPPER','Upper Chest','Üst Göğüs'),
('CHEST_MID','CHEST','MID','Mid Chest','Orta Göğüs'),
('CHEST_LOWER','CHEST','LOWER','Lower Chest','Alt Göğüs'),

-- BACK
('BACK_LATS','BACK','LATS','Lats','Kanat'),
('BACK_UPPER','BACK','UPPER','Upper Back','Üst Sırt'),
('BACK_MID','BACK','MID','Mid Back','Orta Sırt'),
('BACK_LOWER','BACK','LOWER','Lower Back','Alt Sırt'),

-- TRAPS
('TRAPS_UPPER','TRAPS','UPPER','Upper Traps','Üst Trapez'),
('TRAPS_MID','TRAPS','MID','Mid Traps','Orta Trapez'),
('TRAPS_LOWER','TRAPS','LOWER','Lower Traps','Alt Trapez'),

-- SHOULDERS
('SHOULDERS_FRONT','SHOULDERS','FRONT','Front Delts','Ön Omuz'),
('SHOULDERS_SIDE','SHOULDERS','SIDE','Side Delts','Yan Omuz'),
('SHOULDERS_REAR','SHOULDERS','REAR','Rear Delts','Arka Omuz'),

-- ARMS
('BICEPS','ARMS','BICEPS','Biceps','Biseps'),
('TRICEPS','ARMS','TRICEPS','Triceps','Triseps'),
('FOREARMS','ARMS','FOREARMS','Forearms','Ön Kol'),

-- CORE / ABS
('ABS_UPPER','CORE','UPPER','Upper Abs','Üst Karın'),
('ABS_LOWER','CORE','LOWER','Lower Abs','Alt Karın'),
('OBLIQUES','CORE','OBLIQUES','Obliques','Oblik'),
('CORE_TRANSVERSE','CORE','DEEP','Transverse Abdominis','Derin Core'),

-- LEGS
('QUADS','LEGS','QUADS','Quads','Ön Bacak'),
('HAMSTRINGS','LEGS','HAMSTRINGS','Hamstrings','Arka Bacak'),
('GLUTES','LEGS','GLUTES','Glutes','Kalça'),
('ADDUCTORS','LEGS','ADDUCTORS','Adductors','İç Bacak'),

-- CALVES
('CALVES_GASTRO','LEGS','CALVES','Gastrocnemius','Baldır (Gastro)'),
('CALVES_SOLEUS','LEGS','SOLEUS','Soleus','Baldır (Soleus)'),

-- FULL BODY
('FULL_BODY','FULL_BODY','GENERAL','Full Body','Tüm Vücut');
