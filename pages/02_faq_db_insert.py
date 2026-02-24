
import streamlit as st
import pandas as pd
from sqlalchemy import text

import sys
import os
# 현재 파일의 위치를 기준으로 프로젝트 루트(상위 폴더)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.sidemenu import display_sidebar
#공통 사이드바 호출
display_sidebar()
brand_code=""

@st.cache_resource
def get_connector():
    # st.connection을 통해 DB 연결 (secrets.toml 설정 필요)
    return st.connection("faqdb", type='sql', autocommit=True)

def insert_faq_data(file):
    """
    FAQ CSV 데이터를 읽어 FAQ 테이블에 insert 함
    """
    conn = get_connector()
    
    # 1. CSV 데이터 읽기
    try:
        # 헤더가 없는 경우 names를 지정, 있다면 상황에 맞춰 수정 가능
        df = pd.read_csv(file, header=0, names=['category', 'question', 'answer'])
        #df = pd.read_csv(file, header=0)
        #df.columns = ['category', 'question', 'answer'] # 이름 표준화
    
        # 2. 화면에 미리보기
        st.subheader("업로드된 데이터 미리보기")
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
        return

    # 2. SQL 구문 정의 (제공된 테이블 구조 기준)
    query = text("""
        INSERT INTO FAQ (brand_code, category, question, answer)
        VALUES (:brand_code, :category, :question, :answer)
    """)

    success_count = 0
    fail_list = []
    brand_code = file.name.split('_')[0]
    # 3. 데이터 반복 삽입
    for _, row in df.iterrows():
        try:
            with conn.session as session:
                session.execute(query, {
                    "brand_code": brand_code, 
                    "category": row['category'],
                    "question": row['question'],
                    "answer": row['answer']
                })
                session.commit()
            success_count += 1
        except Exception as e:
            fail_list.append({"question": row['question'], "error": str(e)})

    return success_count, fail_list

# --- Streamlit UI ---
st.title("🚗 자동차 FAQ 데이터 데이타베이스저장")

uploaded_file = st.file_uploader("자동차 FAQ CSV 파일을 업로드하세요", type=['csv'])

if uploaded_file:
    if st.button("데이터베이스에 저장"):
        with st.spinner("데이터 저장 중..."):
            success, fails = insert_faq_data(uploaded_file)
            
            st.success(f"성공적으로 {success}건의 데이터를 저장했습니다.")
            
            if fails:
                st.error(f"{len(fails)}건의 데이터 저장에 실패했습니다.")
                with st.expander("실패 목록 확인"):
                    st.write(fails)

# --- 저장된 데이터 확인 ---
if st.checkbox("저장된 데이터 미리보기"):
    conn = get_connector()
    print(conn)
    # 1. 데이터 가져오기
    existing_data = conn.query("SELECT * FROM FAQ ORDER BY created_at DESC LIMIT 10")
    
    # 2. 데이터가 있는지, 비어있지 않은지 확인
    if existing_data is not None and not existing_data.empty:
        st.write(f"최근 데이터 {len(existing_data)}건을 불러왔습니다.")
        st.table(existing_data) # 혹은 더 예쁜 st.dataframe(existing_data) 사용 추천
    else:
        st.warning("조회된 데이터가 없습니다.")