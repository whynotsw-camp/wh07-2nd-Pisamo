# CSV로 내보내기

import os, csv, sys
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST","127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT","3306")),
        user=os.getenv("MYSQL_USER","root"),
        password=os.getenv("MYSQL_PASSWORD",""),
        database=os.getenv("MYSQL_DB","churo_me"),
        charset="utf8mb4",
        use_unicode=True
    )

def main():
    print("[INFO] CWD:", os.getcwd())  # 현재 작업 폴더 확인

    try:
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM v_movie_top_emotion;")
        rows = cur.fetchall()
    except mysql.connector.Error as e:
        print("[ERROR] MySQL 오류:", e)
        sys.exit(1)
    finally:
        try:
            cur.close(); conn.close()
        except:
            pass

    if not rows:
        print("[WARN] v_movie_top_emotion 조회 결과가 0건입니다.")
        print(" - 뷰가 존재하는지/데이터가 들어있는지 확인해주세요:")
        print("   USE churo_me; SELECT COUNT(*) FROM v_movie_top_emotion;")
        sys.exit(0)

    # 저장 경로(./exports/movies.csv)
    out_dir = os.path.join(os.getcwd(), "exports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "movies.csv")

    # 필드명은 rows[0].keys()로 안전하게
    fieldnames = list(rows[0].keys())

    try:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        print(f"[OK] CSV 저장 완료: {out_path}")
    except Exception as e:
        print("[ERROR] 파일 저장 실패:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
