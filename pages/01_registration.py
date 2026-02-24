import os
import sys
# 현재 파일의 위치를 기준으로 프로젝트 루트(상위 폴더)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import date
from common.sidemenu import display_sidebar

st.set_page_config(page_title=" 자동차등록현황", page_icon="🚗", layout="wide") # 넓게 보기 옵션 추가
display_sidebar() # 공통 사이드바 호출


# # 1. 데이터 로드 (캐싱을 통해 속도 향상)
# @st.cache_data
# def load_data():
#     df = pd.read_csv('stat_region.csv')
#     # 연월 순서대로 정렬 (데이터가 뒤섞여 있을 경우 대비)
#     df['date_dt'] = pd.to_datetime(df['연월']).dt.date
#     return df

# df = load_data()

# # --- 상단 레이아웃: 필터 ---
# st.title("🚗 자동차 등록현황 분석 대시보드")
# st.markdown("---")

# col1, col2 = st.columns([1, 2])

# with col1:
#     st.subheader("🔍 데이터 필터링")
#     regions = st.multiselect(
#         "지역 선택",
#         options=sorted(df['시도별'].unique()),
#         default=['합계', '서울', '경기']
#     )
#     types = st.multiselect(
#         "차종 선택",
#         options=['승용', '승합', '화물', '특수'],
#         default=['승용']
#     )
#     uses = st.multiselect(
#         "용도 선택",
#         options=['관용', '자가용', '영업용'],
#         default=['자가용']
#     )

# with col2:
#     st.subheader("📅 기간 및 지표 설정")
#     # 슬라이더 설정
#     start_date = date(2016, 1, 1)
#     end_date = date(2026, 1, 1)
#     selected_range = st.slider(
#         "조회 기간",
#         min_value=start_date,
#         max_value=end_date,
#         value=(date(2016, 1, 1), date(2018, 12, 1)),
#         format="YYYY/MM"
#     )
    
#     # [추가] 분석 지표 선택 (누적 vs 증감)
#     metric_type = st.radio(
#         "분석 지표 선택",
#         ["누적 등록 대수 (Total)", "전월 대비 증감량 (Delta)"],
#         horizontal=True,
#         help="증감량은 이번 달 등록 대수에서 지난달 대수를 뺀 수치입니다."
#     )

# # 2. 데이터 필터링
# mask = (
#     (df['date_dt'] >= selected_range[0]) & 
#     (df['date_dt'] <= selected_range[1]) & 
#     (df['시도별'].isin(regions)) &
#     (df['차종'].isin(types)) &
#     (df['용도'].isin(uses))
# )
# filtered_df = df.loc[mask]

# # --- 메인 시각화 섹션 ---
# if not regions or not types or not uses:
#     st.warning("⚠️ 왼쪽 필터에서 지역, 차종, 용도를 최소 하나 이상 선택해주세요.")
# else:
#     # 3. 차트용 데이터 재구성 (피벗 테이블)
#     # 선택된 지역별로 추이를 보기 위해 피벗
#     chart_data = filtered_df.groupby(['연월', '시도별'])['count'].sum().reset_index()
#     chart_pivot = chart_data.pivot(index='연월', columns='시도별', values='count')

#     # 4. 지표 계산 (증감량 선택 시)
#     if "증감량" in metric_type:
#         plot_df = chart_pivot.diff().fillna(0)
#         chart_title = "📉 지역별 전월 대비 증감 추이"
#     else:
#         plot_df = chart_pivot
#         chart_title = "📈 지역별 누적 등록 대수 추이"

#     # 5. 시각화 출력
#     st.subheader(chart_title)
#     st.line_chart(plot_df)

#     # 6. 통계 요약 및 상세 데이터
#     col_a, col_b = st.columns(2)
    
#     with col_a:
#         st.write("### 📊 지표 요약")
#         if "증감량" in metric_type:
#             max_val = plot_df.max().max()
#             st.success(f"선택 기간 중 가장 큰 월간 증가는 **{max_val:,.0f}대** 입니다.")
#         else:
#             total_sum = filtered_df['count'].sum()
#             st.info(f"선택 기간/조건의 총 등록 합계: **{total_sum:,.0f}대**")

#     with col_b:
#         with st.expander("📝 원본 데이터 확인 (Pivoted)"):
#             st.dataframe(plot_df, use_container_width=True)

# # 푸터 (공통 사이드바 호출 위치 등은 유지)
# # display_sidebar()


# 2. 데이터 로드 (실제 파일명에 맞춰주세요)
@st.cache_data
def load_region_data():
    df = pd.read_csv('stat_region.csv')
    df['date_dt'] = pd.to_datetime(df['연월']).dt.date
    return df

# 성별/연령별 데이터는 별도의 파일(예: stat_demographics.csv)이 있다고 가정
# 만약 파일이 없다면 구조만 참고하세요.
@st.cache_data
def load_demo_data():
    # 예시용 더미 데이터 생성 (실제 파일이 있다면 pd.read_csv 사용)
    data = {
        '연월': ['2023-01']*4,
        '시도별': ['서울', '서울', '경기', '경기'],
        '성별': ['남', '여', '남', '여'],
        '연령대': ['30대', '30대', '40대', '40대'],
        'count': [1500, 1300, 2000, 1800]
    }
    return pd.DataFrame(data)

df_region = load_region_data()

# --- [상단] 분석 지표 선택 (라디오 버튼) ---
st.title("🚗 자동차 등록 데이터 분석")
analysis_mode = st.radio(
    "분석 지표를 선택하세요",
    ["지역/차종별 등록 추이", "성별/연령별 점유율 (특정 시점)"],
    horizontal=True
)

st.markdown("---")

# --- [중간] 분석 모드에 따른 동적 필터 구성 ---
if analysis_mode == "지역/차종별 등록 추이":
    # --- 모드 A: 추이 분석 필터 ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 가로로 배치하기 위해 또 내부 컬럼 사용 가능
        sub_c1, sub_c2, sub_c3 = st.columns(3)
        regions = sub_c1.multiselect("지역", sorted(df_region['시도별'].unique()), default=['서울', '경기'])
        types = sub_c2.multiselect("차종", ['승용', '승합', '화물', '특수'], default=['승용'])
        uses = sub_c3.multiselect("용도", ['관용', '자가용', '영업용'], default=['자가용'])
        
    with col2:
        selected_range = st.slider(
            "조회 기간",
            min_value=date(2016, 1, 1),
            max_value=date(2026, 1, 1),
            value=(date(2016, 1, 1), date(2018, 12, 1)),
            format="YYYY/MM"
        )

    # 데이터 필터링 및 시각화
    mask = (df_region['date_dt'] >= selected_range[0]) & \
           (df_region['date_dt'] <= selected_range[1]) & \
           (df_region['시도별'].isin(regions)) & \
           (df_region['차종'].isin(types)) & \
           (df_region['용도'].isin(uses))
    
    filtered_df = df_region.loc[mask]
    
    if not filtered_df.empty:
        st.subheader("📊 지역별 등록 추이 비교")
        chart_pivot = filtered_df.groupby(['연월', '시도별'])['count'].sum().unstack().fillna(0)
        st.line_chart(chart_pivot)
    else:
        st.warning("선택한 조건에 데이터가 없습니다.")

else:
    # --- 모드 B: 점유율 분석 필터 ---
    # 여기서는 '차종', '용도' 필터를 아예 노출하지 않음
    df_demo = load_demo_data()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # demo_regions = st.multiselect("지역 선택", sorted(df_region['시도별'].unique()), default=['서울'])
        selected_regions = st.multiselect("조회 지역", sorted(df_demo['시도별'].unique()), default=['서울'])
        # 기간이 아닌 '특정 시점' 선택 (selectbox 혹은 single value slider)
        available_months = sorted(df_demo['연월'].unique(), reverse=True)
        selected_month = st.selectbox("조회 연월 선택", available_months)
    
    with col2:
        st.info("💡 성별/연령별 데이터는 차종 및 용도 구분이 포함되어 있지 않습니다.")

    # 필터링
    demo_mask = (df_demo['연월'] == selected_month) & (df_demo['시도별'].isin(selected_regions))
    filtered_demo = df_demo.loc[demo_mask]
    
    # 시각화 (Pie Chart)
    if not filtered_demo.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"### 🚻 성별 점유율 ({selected_month})")
            fig_sex = px.pie(filtered_demo, values='count', names='성별', hole=0.3)
            st.plotly_chart(fig_sex, use_container_width=True)
        
        with c2:
            st.write(f"### 🎂 연령별 점유율 ({selected_month})")
            fig_age = px.pie(filtered_demo, values='count', names='연령대')
            st.plotly_chart(fig_age, use_container_width=True)
    else:
        st.warning("선택한 조건에 해당하는 데이터가 없습니다.")