-- Migration: create exercise and history tables with unique constraint on checksum/checksum_algorithm
CREATE TABLE IF NOT EXISTS exercise (
  id INTEGER PRIMARY KEY,
  checksum TEXT NOT NULL,
  checksum_algorithm TEXT NOT NULL DEFAULT 'sha256',
  file_path TEXT NOT NULL,
  parent_exercise_id INTEGER,
  tags_json TEXT,
  metadata_json TEXT,
  created_at TEXT,
  updated_at TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_exercise_checksum_algorithm ON exercise(checksum, checksum_algorithm);

CREATE TABLE IF NOT EXISTS exercise_checksum_history (
  id INTEGER PRIMARY KEY,
  exercise_id INTEGER NOT NULL,
  checksum TEXT NOT NULL,
  file_path TEXT NOT NULL,
  recorded_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_exercise_checksum_history_exercise_id ON exercise_checksum_history(exercise_id);
