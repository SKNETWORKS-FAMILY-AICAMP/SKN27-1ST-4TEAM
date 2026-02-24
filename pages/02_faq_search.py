import pandas as pd
from sqlalchemy import create_engine, text
from st_keyup import st_keyup
import sys
import os
import streamlit as st

# 프로젝트 루트 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.sidemenu import display_sidebar


# DB 설정 (필요시 환경 변수로 관리 권장)
DB_CONFIG = "mysql+pymysql://root:root1234@localhost:3306/faqdb"
engine = create_engine(DB_CONFIG)
####################################################################
def run_query(query, params=None):
    """SQL 쿼리를 실행하고 결과를 데이터프레임으로 반환"""
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)

# def get_categories():
#     """카테고리 목록을 중복 없이 가져옴"""
#     query = "SELECT DISTINCT category FROM FAQ"
#     df = run_query(query)
#     return ["전체"] + df['category'].tolist()
def get_categories(brand="전체"):
    """브랜드별 카테고리 목록을 중복 없이 가져옴"""
    if brand == "전체":
        query = "SELECT DISTINCT category FROM FAQ"
        params = {}
    else:
        query = "SELECT DISTINCT category FROM FAQ WHERE brand_code = :brand"
        params = {"brand": brand}
        
    df = run_query(query, params)
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



####################################################################
def display_search_filters():
    """브랜드 선택 시 해당 브랜드의 카테고리만 로드하도록 구성"""
    st.header("🔍 검색 및 필터 설정")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. 브랜드 선택 (이 값이 아래 category_list에 영향을 줍니다)
        brand = st.selectbox("브랜드 선택", ["전체", "HYUNDAI", "KIA", "GENESIS"])
    
    with col2:
        # 2. 선택된 브랜드를 인자로 전달하여 카테고리 목록을 가져옴
        # db_handler 모듈 사용 시 db.get_categories(brand)
        category_list = get_categories(brand) 
        
        # 3. 가져온 리스트로 셀렉트박스 생성
        category = st.selectbox("카테고리 선택", category_list)
    
    # keyword = st.text_input("검색어 입력 (질문/답변)")
    # st.text_input 대신 st_keyup 사용 (글자 입력 시 즉시 값 반환)
    keyword = st_keyup("검색어 실시간 입력", key="search_input")
    sort_option = st.radio("정렬 기준", ["최신순", "오래된순", "제목순"], horizontal=True)
    
    return brand, category, keyword, sort_option
def display_results(df):
    """실시간 검색에 최적화된 리스트형 UI"""
    st.subheader(f"📌 검색 결과 ({len(df)}건)")
    
    if df.empty:
        st.info("검색 결과가 없습니다.")
        return

    # 행 높이가 고민이라면, 테이블 대신 Expander 리스트를 활용해보세요.
    for _, row in df.iterrows():
        # 질문을 클릭하면 답변이 펼쳐지는 구조 (행 높이 문제를 근본적으로 해결)
        with st.expander(f"[{row['brand_code']}] {row['question']}"):
            st.markdown(f"**카테고리:** `{row['category']}`")
            st.info(row['answer'])
            st.caption(f"최종 수정: {row['updated_at']}")
# def display_results(df):
#     """데이터프레임 결과 출력 UI"""
#     st.subheader(f"📌 검색 결과 ({len(df)}건)")
    
#     if df.empty:
#         st.info("조건에 맞는 데이터가 없습니다.")
#         return

#     st.dataframe(
#         df,
#         use_container_width=True,
#         column_config={
#             "faq_id": "🆔 ID",
#             "brand_code": "브랜드",
#             "category": "카테고리",
#             # width를 "large" 또는 "max"로 설정하여 행 높이가 확보되도록 유도
#             "question": st.column_config.TextColumn("질문 내용", width="large"),
#             "answer": st.column_config.TextColumn("답변 내용", width="max"),
#             "updated_at": st.column_config.DatetimeColumn("마지막 수정일", format="YYYY-MM-DD HH:mm")
#         },
#         hide_index=True
#     )


def main():
    st.set_page_config(page_title="FAQ 데이터베이스 통합 검색 시스템 ",page_icon="🚗", layout="wide")
    display_sidebar()
    st.title("🚗FAQ 데이터베이스 통합 검색 시스템")

    # 1. 필터 UI 구성 (여기서 brand, category, keyword가 바뀔 때마다 스크립트 재실행)
    brand, category, keyword, sort_opt = display_search_filters()

    # 2. 결과 출력 공간 확보
    # result_area를 만들어두면 쿼리 실행 중에 화면이 깜빡이는 것을 최소화할 수 있습니다.
    result_area = st.container()

    try:
        # 사용자가 입력한 keyword 등을 기반으로 실시간 쿼리
        results = fetch_faq_data(brand, category, keyword, sort_opt)
        
        with result_area:
            display_results(results)
            
    except Exception as e:
        st.error(f"데이터 조회 중 오류 발생: {e}")

if __name__ == "__main__":
    main()