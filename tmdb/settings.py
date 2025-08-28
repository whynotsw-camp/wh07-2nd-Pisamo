# load_dotenv() 환경 변수 관리

import os
from dotenv import load_dotenv

load_dotenv()

# TMDB
TMDB_V4_TOKEN = os.getenv("TMDB_V4_TOKEN")
if not TMDB_V4_TOKEN:
    raise RuntimeError("TMDB_V4_TOKEN이 .env에 없습니다.")

# MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB   = os.getenv("MYSQL_DB", "churo_me")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# 기타
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
