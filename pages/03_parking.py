import os
import sys
# 현재 파일의 위치를 기준으로 프로젝트 루트(상위 폴더)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import streamlit as st

from common.sidemenu import display_sidebar

st.set_page_config(page_title="주차장 찾기", layout="wide")
display_sidebar() # 공통 사이드바 호출

# --- Streamlit UI ---
st.title("🚗 주차장 찾기")