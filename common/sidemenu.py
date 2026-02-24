# common.py
import os
import streamlit as st


def display_sidebar():
    # 1. 페이지 설정 (가장 처음에 와야 함)

    # st.set_page_config(
    #     page_title="4조 프로젝트",
    #     layout="wide",
    #     initial_sidebar_state="expanded", # 사이드바 초기 상태
    #     menu_items={
    #         'Get Help': None,
    #         'Report a bug': None,
    #         'About': None
    #     }
    # )
    # 2. 사이드바의 자동 네비게이션을 숨기는 CSS
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:  

        # 현재 파일명 확인
        current_file = os.path.basename(st.active_script_hash if hasattr(st, "active_script_hash") else "")

        st.title("📂 메뉴")
        
        st.page_link("main.py", label="홈페이지", icon="🏠",disabled=("main.py" in st.session_state.get('current_page', '')))
        st.page_link("pages/01_registration.py", label="자동차등록현황", icon="🏎️",disabled=("pages/01_registration.py" in st.session_state.get('current_page', '')))
        
        
        with st.expander("📂 FAQ 페이지", expanded=True):
            # 파일 경로가 실제 파일 위치와 일치하는지 꼭 확인하세요!
            st.page_link("pages/02_faq_crawling.py", label="크롤링", icon="🏎️",disabled=("pages/02_faq_crawling.py" in st.session_state.get('current_page', '')))
            st.page_link("pages/02_faq_db_insert.py", label="데이타베이스저장", icon="💾",disabled=("pages/02_faq_db_insert.py" in st.session_state.get('current_page', '')))
            st.page_link("pages/02_faq_search.py", label="FAQ 검색", icon="🚗",disabled=("pages/02_faq_search.py" in st.session_state.get('current_page', '')))
            
        st.page_link("pages/03_parking.py", label="주차장현황", icon="🅿️",disabled=("pages/03_parking.py" in st.session_state.get('current_page', '')))
            
        st.divider()

        st.caption("4조 프로젝트 화이팅! 🔥")   