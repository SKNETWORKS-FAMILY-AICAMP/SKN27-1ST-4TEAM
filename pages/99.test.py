import streamlit as st
import pandas as pd

# 1. 샘플 데이터
df = pd.DataFrame({
    "장소": ["서울역", "강남역", "홍대입구역"],
    "lat": [37.5546, 37.4979, 37.5575],
    "lon": [126.9706, 127.0276, 126.9245]
})

# 2. 팝업창 함수 정의 (@st.dialog 사용)
@st.dialog("위치 확인")
def show_map_popup(row_data):
    st.write(f"### 📍 {row_data['장소'].values[0]}")
    # 지도 출력
    st.map(row_data, latitude="lat", longitude="lon", zoom=15)
    
    if st.button("닫기"):
        st.rerun()

st.title("🚩 행 클릭 시 팝업 지도")

# 3. 데이터프레임 출력
selected = st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row"
)

# 4. 선택 이벤트 감지 및 팝업 호출
if len(selected.selection.rows) > 0:
    selected_index = selected.selection.rows[0]
    selected_data = df.iloc[[selected_index]]
    
    # 팝업 함수 실행
    show_map_popup(selected_data)