

-- 1. faqdb가 존재하면 삭제
DROP DATABASE IF EXISTS faqdb;

-- 2. faqdb 새로 생성
CREATE DATABASE faqdb;

-- 3. 생성한 데이터베이스 사용
USE faqdb;

# faqdb 접속 

use faqdb;

DROP TABLE IF EXISTS FAQ;

CREATE TABLE FAQ (
    faq_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'FAQ 고유 번호',
    brand_code VARCHAR(20) NOT NULL COMMENT '브랜드 구분 (HYUNDAI, KIA, GENESIS 등)',
    category VARCHAR(50) NOT NULL COMMENT '질문 분류',
    question TEXT NOT NULL COMMENT '질문 내용',
    answer TEXT NOT NULL COMMENT '답변 내용',
   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시'
);

-- 검색 성능을 위한 인덱스 추가 (브랜드별 조회가 잦을 경우 필수)
CREATE INDEX idx_brand_code ON FAQ(brand_code);