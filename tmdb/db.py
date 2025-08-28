# MySQL 연결/스키마/Upsert 함수


import mysql.connector
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD

def server_conn():
    return mysql.connector.connect(
        host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD
    )

def db_conn():
    return mysql.connector.connect(
        host=MYSQL_HOST, port=MYSQL_PORT,
        user=MYSQL_USER, password=MYSQL_PASSWORD,
        database=MYSQL_DB, charset="utf8mb4", use_unicode=True
    )

DDL_CREATE_DB = f"""
CREATE DATABASE IF NOT EXISTS {MYSQL_DB}
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
"""

DDL_MOVIES = """
CREATE TABLE IF NOT EXISTS movies (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  tmdb_id INT NOT NULL,
  title VARCHAR(255) NOT NULL,
  original_title VARCHAR(255) NULL,
  overview TEXT NULL,
  release_date DATE NULL,
  popularity DECIMAL(10,3) NULL,
  vote_average DECIMAL(4,2) NULL,
  vote_count INT NULL,
  original_language VARCHAR(10) NULL,
  poster_path VARCHAR(300) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_tmdb_id (tmdb_id),
  KEY idx_release_date (release_date),
  KEY idx_popularity (popularity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_EMOTIONS = """
CREATE TABLE IF NOT EXISTS emotions (
  id TINYINT UNSIGNED NOT NULL,
  name VARCHAR(20) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_emotion_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

DDL_MOVIE_EMOTIONS = """
CREATE TABLE IF NOT EXISTS movie_emotions (
  movie_id BIGINT UNSIGNED NOT NULL,
  emotion_id TINYINT UNSIGNED NOT NULL,
  score DECIMAL(5,4) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (movie_id, emotion_id),
  CONSTRAINT fk_me_movie  FOREIGN KEY (movie_id)  REFERENCES movies(id)   ON DELETE CASCADE,
  CONSTRAINT fk_me_emotion FOREIGN KEY (emotion_id) REFERENCES emotions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

EMOTION_SEED = [(1,'기쁨'),(2,'분노'),(3,'슬픔'),(4,'상처'),(5,'당황'),(6,'불안')]

UPSERT_MOVIE = """
INSERT INTO movies (
  tmdb_id, title, original_title, overview, release_date,
  popularity, vote_average, vote_count, original_language, poster_path
) VALUES (
  %(tmdb_id)s, %(title)s, %(original_title)s, %(overview)s, %(release_date)s,
  %(popularity)s, %(vote_average)s, %(vote_count)s, %(original_language)s, %(poster_path)s
)
ON DUPLICATE KEY UPDATE
  title=VALUES(title),
  original_title=VALUES(original_title),
  overview=VALUES(overview),
  release_date=VALUES(release_date),
  popularity=VALUES(popularity),
  vote_average=VALUES(vote_average),
  vote_count=VALUES(vote_count),
  original_language=VALUES(original_language),
  poster_path=VALUES(poster_path);
"""

UPSERT_MOVIE_EMOTION = """
INSERT INTO movie_emotions (movie_id, emotion_id, score)
VALUES (%s, %s, %s)
ON DUPLICATE KEY UPDATE score=VALUES(score);
"""

def ensure_database_and_schema():
    conn = server_conn()
    try:
        cur = conn.cursor()
        cur.execute(DDL_CREATE_DB)
        conn.commit()
    finally:
        conn.close()

    conn = db_conn()
    try:
        cur = conn.cursor()
        cur.execute(DDL_MOVIES)
        cur.execute(DDL_EMOTIONS)
        cur.execute(DDL_MOVIE_EMOTIONS)
        cur.executemany("INSERT IGNORE INTO emotions (id, name) VALUES (%s,%s)", EMOTION_SEED)
        conn.commit()
    finally:
        conn.close()

def upsert_movies_and_get_ids(conn, movies):
    """
    movies: normalize된 dict 리스트
    return: {tmdb_id: movies.id}
    """
    ids = {}
    cur = conn.cursor()
    try:
        for m in movies:
            cur.execute(UPSERT_MOVIE, m)
            cur.execute("SELECT id FROM movies WHERE tmdb_id=%s", (m["tmdb_id"],))
            ids[m["tmdb_id"]] = cur.fetchone()[0]
        conn.commit()
        return ids
    finally:
        cur.close()

def upsert_movie_emotions(conn, movie_id: int, emotion_scores: dict):
    rows = [(movie_id, eid, float(score)) for eid, score in emotion_scores.items()]
    cur = conn.cursor()
    try:
        cur.executemany(UPSERT_MOVIE_EMOTION, rows)
        conn.commit()
    finally:
        cur.close()
