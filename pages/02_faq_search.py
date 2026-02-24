import pandas as pd
from sqlalchemy import create_engine, text
# DB 설정 (필요시 환경 변수로 관리 권장)
DB_CONFIG = "mysql+pymysql://root:root1234@localhost:3306/faqdb"
engine = create_engine(DB_CONFIG)
####################################################################
def run_query(query, params=None):
    """SQL 쿼리를 실행하고 결과를 데이터프레임으로 반환"""
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)

def get_categories():
    """카테고리 목록을 중복 없이 가져옴"""
    query = "SELECT DISTINCT category FROM FAQ"
    df = run_query(query)
    return ["전체"] + df['category'].tolist()

def fetch_faq_data(brand="전체", category="전체", keyword="", sort_option="최신순"):
    """필터 조건에 따른 FAQ 데이터를 조회"""
    base_query = "SELECT * FROM FAQ WHERE 1=1"
    params = {}

    if brand != "전체":
        base_query += " AND brand_code = :brand"
        params['brand'] = brand

    if category != "전체":
        base_query += " AND category = :category"
        params['category'] = category

    if keyword:
        base_query += " AND (question LIKE :keyword OR answer LIKE :keyword)"
        params['keyword'] = f"%{keyword}%"

    # 정렬 로직
    sort_dict = {
        "최신순": "ORDER BY created_at DESC",
        "오래된순": "ORDER BY created_at ASC",
        "제목순": "ORDER BY question ASC"
    }
    base_query += f" {sort_dict.get(sort_option, 'ORDER BY created_at DESC')}"
    
    return run_query(base_query, params)


import sys
import os

# 프로젝트 루트 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.sidemenu import display_sidebar
####################################################################
def display_search_filters():
    """사이드바 검색 필터 UI 구성"""
    st.header("🔍 검색 및 필터 설정")
    
    brand = st.selectbox("브랜드 선택", ["전체", "HYUNDAI", "KIA", "GENESIS"])
    
    # DB에서 카테고리 실시간 호출
    category_list = get_categories()
    category = st.selectbox("카테고리 선택", category_list)
    
    keyword = st.text_input("검색어 입력 (질문/답변)")
    sort_option = st.radio("정렬 기준", ["최신순", "오래된순", "제목순"])
    
    return brand, category, keyword, sort_option

def display_results(df):
    """데이터프레임 결과 출력 UI"""
    st.subheader(f"📌 검색 결과 ({len(df)}건)")
    
    if df.empty:
        st.info("조건에 맞는 데이터가 없습니다.")
        return

    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "faq_id": "🆔 ID",
            "brand_code": "브랜드",
            "category": "카테고리",
            "question": "질문 내용",
            "answer": "답변 내용",
            "updated_at": st.column_config.DatetimeColumn("마지막 수정일", format="YYYY-MM-DD HH:mm")
        },
        hide_index=True
    )    
import streamlit as st
import sys
import os

def main():
    st.set_page_config(page_title="FAQ DB Explorer", layout="wide")
    display_sidebar()
    st.title("🗂️ FAQ 데이터베이스 통합 검색 시스템")

    # 1. 필터 UI 렌더링 및 값 수집
    brand, category, keyword, sort_opt = display_search_filters()

    # 2. 데이터 조회 및 출력
    try:
        results = fetch_faq_data(brand, category, keyword, sort_opt)
        display_results(results)
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()