# Python 3.10 slim 이미지 기반
FROM python:3.10-slim

# 작업 디렉토리
WORKDIR /app

# 시스템 패키지 (folium, geopy, pillow 등 의존성)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 코드 & 데이터 복사
COPY . .

# Streamlit 포트 열기
EXPOSE 8501

# Streamlit 실행
CMD ["streamlit", "run", "Project2_Docker.py", "--server.port=8501", "--server.address=0.0.0.0"]

