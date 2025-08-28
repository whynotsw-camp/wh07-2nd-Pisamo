CREATE DATABASE Churo_me
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE Churo_me;

CREATE TABLE emotion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE   -- 예: 슬픔, 기쁨, 분노
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_info (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- 사용자 고유 ID
    name VARCHAR(50) NOT NULL,             -- 이름
    gender ENUM('M', 'F', 'Other'),        -- 성별 (남/여/기타)
    age INT CHECK (age >= 0),              -- 나이
    residence VARCHAR(100),                -- 거주지
    session_info TEXT                      -- 세션 정보 (로그인 기록 등)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_post (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- 게시글 고유 ID
    user_id INT NOT NULL,                  -- 작성자 (FK)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 등록일자
    content TEXT NOT NULL,                 -- 게시글 내용
    review VARCHAR(255),                   -- 리뷰 요약/한줄평
    FOREIGN KEY (user_id) REFERENCES user_info(id) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE user_emotion_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    emotion_id INT NOT NULL,
    score DECIMAL(3,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE,
    FOREIGN KEY (emotion_id) REFERENCES emotion(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE user_session (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    device VARCHAR(100),
    ip_address VARCHAR(45),
    FOREIGN KEY (user_id) REFERENCES user_info(id)
);
-- 영화 데이터 테이블 생성
CREATE TABLE movie (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- 고유 식별자
    name VARCHAR(100) NOT NULL,              -- 영화 제목
    description TEXT,                        -- 줄거리 설명
    poster_image VARCHAR(255),               -- 포스터 이미지 URL
    emotion_id INT, 
    FOREIGN KEY (emotion_id) REFERENCES emotion(id)
        ON DELETE SET NULL,                       -- 장르
    rating DECIMAL(2,1)                      -- 평점
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 드라마 데이터 테이블 생성
CREATE TABLE drama (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- 고유 식별자
    name VARCHAR(100) NOT NULL,              -- 드라마 이름
    description TEXT,                        -- 줄거리 설명
    poster_image VARCHAR(255),               -- 포스터 이미지 URL
    emotion_id INT, 
    FOREIGN KEY (emotion_id) REFERENCES emotion(id)
        ON DELETE SET NULL,                       -- 장르 (예: 로맨스, 스릴러)
    rating DECIMAL(2,1)                      -- 평점 (예: 8.5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 음악 데이터 테이블 생성
CREATE TABLE music (
    id INT AUTO_INCREMENT PRIMARY KEY,       -- 고유 식별자
    name VARCHAR(100) NOT NULL,              -- 노래 제목
    artist VARCHAR(100) NOT NULL,            -- 가수명
    album_cover_url VARCHAR(255),            -- 앨범 커버 이미지(URL)
    emotion_id INT, 
    FOREIGN KEY (emotion_id) REFERENCES emotion(id)
        ON DELETE SET NULL            -- 감정 분류 (예: 슬픔, 기쁨 등)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 병원 데이터 테이블 생성
CREATE TABLE hospital_info (
    id INT AUTO_INCREMENT PRIMARY KEY,        
    name VARCHAR(100) NOT NULL,               
    longitude DECIMAL(10,7) NOT NULL,         
    latitude DECIMAL(10,7) NOT NULL,          
    phone VARCHAR(20),                        
    website_url VARCHAR(255)                  
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE location (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,        -- 예: 서울 강남구
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7)
);

ALTER TABLE user_info
ADD COLUMN location_id INT,
ADD FOREIGN KEY (location_id) REFERENCES location(id);

ALTER TABLE hospital_info
ADD COLUMN location_id INT,
ADD FOREIGN KEY (location_id) REFERENCES location(id);


