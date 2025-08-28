# TMDB API 호출 전용 함수들

import requests
from settings import TMDB_V4_TOKEN, REQUEST_TIMEOUT

TMDB_BASE = "https://api.themoviedb.org/3"
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_V4_TOKEN}",
}

def fetch_discover_movies(page=1, sort_by="popularity.desc", language="ko-KR", region=None):
    params = {"sort_by": sort_by, "page": page, "language": language}
    if region:
        params["region"] = region
    resp = requests.get(f"{TMDB_BASE}/discover/movie", headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def fetch_movie_details(movie_id: int, language: str = "ko-KR") -> dict:
    params = {"language": language}
    resp = requests.get(f"{TMDB_BASE}/movie/{movie_id}", headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()
