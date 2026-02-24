import sys
import os
import streamlit as st
# 현재 파일의 위치를 기준으로 프로젝트 루트(상위 폴더)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.sidemenu import display_sidebar
st.set_page_config(page_title="FAQ 검색", layout="wide")
#공통 사이드바 호출
display_sidebar()
# --- Streamlit UI ---
st.title("🚗 FAQ 검색")