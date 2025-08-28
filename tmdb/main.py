# main.py
import time
from typing import Optional
from tmdb_client import fetch_discover_movies, fetch_movie_details
from emotion import score_emotions
from db import ensure_database_and_schema, db_conn, upsert_movies_and_get_ids, upsert_movie_emotions

def normalize_movie(raw: dict, overview_override: Optional[str] = None) -> dict:
    """TMDB 결과를 DB 입력 dict로 정규화."""
    return {
        "tmdb_id": raw.get("id"),
        "title": (raw.get("title") or "").strip(),
        "original_title": raw.get("original_title"),
        "overview": overview_override if overview_override is not None else raw.get("overview"),
        "release_date": (raw.get("release_date") or None),
        "popularity": raw.get("popularity"),
        "vote_average": raw.get("vote_average"),
        "vote_count": raw.get("vote_count"),
        "original_language": raw.get("original_language"),
        "poster_path": raw.get("poster_path"),
    }

def ingest_discover(
    target_nonnull_overview=100,
    delay_sec=0.35,
    language="ko-KR",
    region="KR",
    require_poster=True,
    backfill_language="en-US",
):
    """
    discover/movie를 순회하며 overview 있는 영화 target_nonnull_overview편 수집.
    ko-KR 개요가 없으면 backfill_language(예: en-US)로 상세 재조회하여 보강.
    """
    ensure_database_and_schema()
    collected = 0
    page = 1

    conn = db_conn()
    try:
        while collected < target_nonnull_overview:
            data = fetch_discover_movies(page, language=language, region=region)
            results = data.get("results", [])
            if not results:
                break

            batch = []
            for r in results:
                if require_poster and not r.get("poster_path"):
                    continue

                overview = r.get("overview")
                if not overview or not str(overview).strip():
                    # 영어로 보강 시도
                    try:
                        detail = fetch_movie_details(r["id"], language=backfill_language)
                        overview = detail.get("overview")
                    except Exception:
                        overview = None

                if not overview or not str(overview).strip():
                    continue  # 최종적으로도 개요 없으면 스킵

                batch.append(normalize_movie(r, overview_override=overview))
                if len(batch) + collected >= target_nonnull_overview:
                    break

            id_map = upsert_movies_and_get_ids(conn, batch)
            for m in batch:
                emo = score_emotions(m.get("overview"))
                upsert_movie_emotions(conn, id_map[m["tmdb_id"]], emo)

            collected += len(batch)
            print(f"page {page} 저장(누적 {collected}편)")
            page += 1
            time.sleep(delay_sec)

        print(f"완료: overview 있는 영화 {collected}편 저장")
    finally:
        conn.close()

if __name__ == "__main__":
    # 필요에 따라 파라미터 조정 가능
    ingest_discover(
        target_nonnull_overview=100,
        delay_sec=0.35,
        language="ko-KR",
        region="KR",
        require_poster=True,      # 포스터 없는 작품도 허용하려면 False
        backfill_language="en-US" # 한글 개요 없을 때 영어로 보강
    )
