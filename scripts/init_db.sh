#!/bin/bash

DB_PATH="db/fitanalytics.db"

echo ">>> Resetting database..."

# db klasörü yoksa oluştur
mkdir -p db

# eski db varsa sil
if [ -f "$DB_PATH" ]; then
    echo ">>> Removing existing database..."
    rm "$DB_PATH"
fi

echo ">>> Creating fresh database..."

# Schema
sqlite3 "$DB_PATH" < sql/schema.sql
if [ $? -ne 0 ]; then
    echo "!!! ERROR: schema.sql failed"
    exit 1
fi

# Muscles seed
sqlite3 "$DB_PATH" < sql/muscles_seed.sql
if [ $? -ne 0 ]; then
    echo "!!! ERROR: muscles_seed.sql failed"
    exit 1
fi

# Exercise library seed
sqlite3 "$DB_PATH" < sql/exercise_library.sql
if [ $? -ne 0 ]; then
    echo "!!! ERROR: exercise_library.sql failed"
    exit 1
fi

echo ">>> Database initialized successfully!"
