# common.py
import streamlit as st

def display_sidebar():
    # 1. 페이지 설정 (가장 처음에 와야 함)

    st.set_page_config(
        page_title="4조 프로젝트",
        layout="wide",
        initial_sidebar_state="expanded", # 사이드바 초기 상태
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )
    # 2. 사이드바의 자동 네비게이션을 숨기는 CSS
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:    
        st.title("📂 메뉴")
        st.page_link("main.py", label="홈페이지", icon="🏠")
        st.page_link("pages/01_registration.py", label="자동차등록현황", icon="🏎️")
        
        with st.expander("📂 FAQ 페이지", expanded=True):
            # 파일 경로가 실제 파일 위치와 일치하는지 꼭 확인하세요!
            st.page_link("pages/02_faq1.py", label="현대자동차", icon="🏎️")
            st.page_link("pages/02_faq2.py", label="기아자동차", icon="🚙")
            st.page_link("pages/02_faq3.py", label="제네시스", icon="🚗")
            
        with st.expander("📊 주차장 현황"):
            st.button("주간 리포트 보기1", key="btn1")
            st.button("주간 리포트 보기2", key="btn2")
            st.button("주간 리포트 보기3", key="btn3")
            
        st.divider()
        st.caption("4조 프로젝트 화이팅! 🔥")   