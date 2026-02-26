import os
import sys
# 현재 파일의 위치를 기준으로 프로젝트 루트(상위 폴더)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common.sidemenu import display_sidebar

st.set_page_config(page_title=" 자동차등록현황", page_icon="🚗", layout="wide") # 넓게 보기 옵션 추가
display_sidebar() # 공통 사이드바 호출

st.title("지역별 자동차 등록 현황")

# # 1. 데이터 로드 (캐싱을 통해 속도 향상)
@st.cache_data
def load_car_data():
    car_df = pd.read_csv('./car.csv')
    return car_df

# 1. 데이터 로드
df = load_car_data()

# '합계' 행(자동차 등록수)과 '주차구획수' 행 추출
total_cars = df[df['차종'] == '합계'].iloc[0, 1:-1].astype(float)
parking_slots = df[df['차종'] == '주차구획수'].iloc[0, 1:-1].astype(float)

# 2. Rate(주차 수급률) 계산 (주차면수 / 등록대수)
# 같은 눈금에 보이기 위해 %로 변환하거나 가공이 필요할 수 있습니다.
rate = (parking_slots / total_cars) * 100 

# 그래프용 데이터프레임 생성
plot_df = pd.DataFrame({
    '지역': total_cars.index,
    '등록대수': total_cars.values,
    '수급률': rate.values
})

# 3. 그래프 생성 (이중 축 사용 권장 버전)
# 같은 눈금을 원하시면 secondary_y를 제거하면 되지만, 수급률이 보이게 하려면 이중축이 좋습니다.
fig = make_subplots(specs=[[{"secondary_y": True}]])

# (1) 막대 그래프 추가 (자동차 등록 대수)
fig.add_trace(
    go.Bar(x=plot_df['지역'], y=plot_df['등록대수'], name="자동차 등록수", marker_color='skyblue'),
    secondary_y=False,
)

# (2) 꺾은선 그래프 오버레이 (주차 수급률)
fig.add_trace(
    go.Scatter(x=plot_df['지역'], y=plot_df['수급률'], name="주차 수급률(%)", 
               mode='lines+markers', line=dict(color='red', width=3)),
    secondary_y=True, # 같은 눈금을 원하시면 이 줄을 False로 바꾸세요.
)

# 4. 레이아웃 설정
fig.update_layout(
    title_text="지역별 자동차 등록수 및 주차 수급률 (2026.01 기준, 자가용 대상)",
    xaxis_title="지역",
    legend=dict(x=0, y=1.1, orientation="h")
)

# 축 이름 설정
fig.update_yaxes(title_text="자동차 등록수 (대)", secondary_y=False)
fig.update_yaxes(title_text="주차 수급률 (%)", secondary_y=True)

# Streamlit에 출력
st.plotly_chart(fig, use_container_width=True)

with st.expander('상세 데이터 보기'):
    st.dataframe(plot_df)