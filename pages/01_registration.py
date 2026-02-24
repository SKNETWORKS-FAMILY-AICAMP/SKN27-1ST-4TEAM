
import streamlit as st

import sys
import os
# 현재 파일의 위치를 기준으로 프로젝트 루트(상위 폴더)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.sidemenu import display_sidebar
#공통 사이드바 호출
st.set_page_config(page_title=" 자동차등록현황", page_icon="🚗", layout="wide") # 넓게 보기 옵션 추가
display_sidebar()
# --- Streamlit UI 구성 ---
st.title("🚗 자동차등록현황")