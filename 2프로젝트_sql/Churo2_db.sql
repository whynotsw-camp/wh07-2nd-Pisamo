-- 데이터베이스 생성
CREATE DATABASE Churo2_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE Churo2_db;

-- 회원 테이블
CREATE TABLE Member (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    login_id       VARCHAR(50) UNIQUE NOT NULL,
    name           VARCHAR(50),
    gender         VARCHAR(10),
    age            INT,
    address        VARCHAR(255),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password       VARCHAR(255) NOT NULL,
    ip_address     VARCHAR(50),
	latitude       DECIMAL(10,7), -- 추가: 위도
    longitude      DECIMAL(10,7), -- 추가: 경도
    role           VARCHAR(20) -- ex: user, admin
);

-- 비회원 테이블
CREATE TABLE Guest (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address     VARCHAR(50)
);

-- 병원 테이블
CREATE TABLE Hospital (
    hospital_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    latitude      DECIMAL(10,7),   -- 위도
    longitude     DECIMAL(10,7),   -- 경도
    phone         VARCHAR(50),
    website_url   VARCHAR(255)
);

CREATE TABLE Movie (
    movie_id      INT AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(100) NOT NULL,
    description   TEXT,
    poster_url    VARCHAR(255),
    emotion_genre VARCHAR(20),   -- 추가: 감정 장르 (불안, 우울, 기쁨 등)
    rating        DECIMAL(3,1)
);

CREATE TABLE Music (
    music_id      INT AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(100) NOT NULL,
    artist        VARCHAR(100),
    album_cover   VARCHAR(255),
    emotion_genre VARCHAR(20)    -- 추가
);

CREATE TABLE Drama (
    drama_id      INT AUTO_INCREMENT PRIMARY KEY,
    title         VARCHAR(100) NOT NULL,
    description   TEXT,
    poster_url    VARCHAR(255),
    emotion_genre VARCHAR(20),   -- 추가
    rating        DECIMAL(3,1)
);

-- 사용자 세션 정보 테이블
CREATE TABLE UserSession (
    session_id     INT AUTO_INCREMENT PRIMARY KEY,  -- 개별 세션 식별자
    user_id        INT NOT NULL,                    -- 회원 식별자
    login_id       VARCHAR(50) NOT NULL,            -- 로그인 아이디
    login_date     DATE NOT NULL,                   -- 로그인 날짜
    login_time     DATETIME DEFAULT CURRENT_TIMESTAMP, -- 로그인 시간
    logout_time    DATETIME NULL,                   -- 로그아웃 시간
    FOREIGN KEY (user_id) REFERENCES Member(user_id),
    FOREIGN KEY (login_id) REFERENCES Member(login_id)
);

-- 사용자 채팅 로그
CREATE TABLE UserChat (
    chat_id        INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT NOT NULL,
    chat_date      DATE NOT NULL,
    chat_time      TIME NOT NULL,
    question       TEXT,
    answer         TEXT,
    FOREIGN KEY (user_id) REFERENCES Member(user_id)
);
ALTER TABLE UserChat
ADD UNIQUE KEY uniq_chat_datetime (user_id, chat_date, chat_time);


-- 사용자 감정 로그
CREATE TABLE EmotionLog (
    emotion_id     INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT NOT NULL,
    chat_date      DATE NOT NULL,
    chat_time      TIME NOT NULL,
    joy_score      DECIMAL(4,3),
    sadness_score  DECIMAL(4,3),
    anger_score    DECIMAL(4,3),
    hurt_score     DECIMAL(4,3),
    embarrassed_score DECIMAL(4,3),
    anxiety_score  DECIMAL(4,3),
    dominant_emotion VARCHAR(20),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id, chat_date, chat_time) REFERENCES UserChat(user_id, chat_date, chat_time)
);

ALTER TABLE EmotionLog
ADD COLUMN chat_id INT,
ADD CONSTRAINT fk_emotion_chat
FOREIGN KEY (chat_id) REFERENCES UserChat(chat_id);

-- 상담 리포트 요약
CREATE TABLE CounselingSummary (
    summary_id     INT AUTO_INCREMENT PRIMARY KEY,
    user_id        INT NOT NULL,
    chat_id        INT NOT NULL,
    summary_text   TEXT,
    music_rec_id   INT,
    drama_rec_id   INT,
    action_plan    TEXT,
    FOREIGN KEY (user_id) REFERENCES Member(user_id),
    FOREIGN KEY (chat_id) REFERENCES UserChat(chat_id)
);

-- 사용자 북마크 테이블
CREATE TABLE UserBookmark (
    bookmark_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL,
    movie_id      INT,
    music_id      INT,
    drama_id      INT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Member(user_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (music_id) REFERENCES Music(music_id),
    FOREIGN KEY (drama_id) REFERENCES Drama(drama_id)
);