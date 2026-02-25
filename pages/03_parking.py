import os
import sys
import re
import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

# 1. 경로 설정 및 공통 사이드바 호출
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.sidemenu import display_sidebar

st.set_page_config(page_title="주차장 찾기", layout="wide")
display_sidebar()

# 2. 데이터 로드 및 정제 함수
@st.cache_data
def load_parking_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "전국주차장정보표준데이터.csv")
    
    if not os.path.exists(csv_path):
        return None

    df = pd.read_csv(csv_path, encoding='cp949')
    
    # [지역명 정규화]
    def normalize_region(addr):
        if pd.isna(addr): return addr

        addr = str(addr)

        # 오염 데이터 제거 (특수문자 포함)
        if re.search(r'[?!@#]', addr):
            return None

        mapping = { # 긴것부터 value 값을 넣어야됨
                '서울특별시':    ['서울특별시', '서울시', '서울'],
                '경기도':       ['경기도동두천시평화로', '경기도오산시', '경기도', '경기'],
                '인천광역시':    ['인천광역시', '인천시', '인천'],
                '부산광역시':    ['부산광역시', '부산시', '부산'],
                '대구광역시':    ['대구광역시', '대구시', '대구'],
                '대전광역시':    ['대전광역시', '대전시', '대전'],
                '광주광역시':    ['광주광역시', '광주시', '광주'],
                '울산광역시':    ['울산광역시', '울산시', '울산'],
                '세종특별자치시': ['세종특별자치시', '세종시', '세종'],
                '제주특별자치도': ['제주특별자치도', '제주도', '제주'],
                '경상남도':     ['경상남도', '경상남동'],
                '경상북도':     ['경상북도', '경북'],
                '전라북도':     ['전북특별자치도', '전라북도', '전북'],
                '전라남도':     ['전라남도', '전남'],
                '충청남도':     ['충청남도', '충남'],
                '충청북도':     ['충청북도', '충북'],
                '강원특별자치도': ['강원특별자치도강릉시', '강원특별자치도', '강원도', '강원'],
            }


        for 정식명칭, 약식목록 in mapping.items():
            for 약식 in 약식목록:
                if addr.startswith(약식):
                    return 정식명칭 + ' ' + addr[len(약식):].strip()

        return None  # ← return addr 에서 None 으로 변경

    # [시군구 정제] 숫자 포함 데이터 제거
    def extract_clean_sigungu(addr):
        if pd.isna(addr): return None
        parts = str(addr).split()
        if len(parts) > 1:
            sigungu = parts[1]
            if re.search(r'\d', sigungu) or len(sigungu) < 2:
                return None
            return sigungu
        return None

    shorten = {
            '서울특별시': '서울',
            '인천광역시': '인천',
            '부산광역시': '부산',
            '대구광역시': '대구',
            '대전광역시': '대전',
            '광주광역시': '광주',
            '울산광역시': '울산',
            '세종특별자치시': '세종',
            '제주특별자치도': '제주',
            '강원특별자치도': '강원',
            '전라북도': '전북',
            '전라남도': '전남',
            '충청남도': '충남',
            '충청북도': '충북',
            '경상남도': '경남',
            '경상북도': '경북',
        }

    df['주소'] = df['소재지도로명주소'].fillna(df['소재지지번주소']).apply(normalize_region)
    df['시도'] = df['주소'].str.split().str[0].map(lambda x: shorten.get(x, x))
    df['시군구'] = df['주소'].apply(extract_clean_sigungu)

    # [금액 계산 및 포맷팅] .0 제거 및 콤마 추가
    def calc_hourly(row):
        try:
            base_time = float(row.get('주차기본시간', 0))
            base_fee = float(row.get('주차기본요금', 0))
            if base_time > 0:
                val = int((60 / base_time) * base_fee)
                return f"{val:,}원"
            return "무료"
        except:
            return "무료"

    df['기본 금액'] = df.apply(calc_hourly, axis=1)
    df['운영시간'] = df['평일운영시작시각'].fillna('') + " ~ " + df['평일운영종료시각'].fillna('')
    df['토요일운영시간'] = df['토요일운영시작시각'].fillna('') + " ~ " + df['토요일운영종료시각'].fillna('')
    df['공휴일운영시간'] = df['공휴일운영시작시각'].fillna('') + " ~ " + df['공휴일운영종료시각'].fillna('')
    
    # [수정] 주차장구분이 '공영'인 데이터만 추출
    df = df[df['주차장구분'] == '공영']

    return df

df_raw = load_parking_data()

if df_raw is None:
    st.error("⚠️ CSV 파일을 찾을 수 없습니다.")
    st.stop()

# --- Streamlit UI ---
st.title("🚗 공영 주차장 찾기")

col1, col2, col3 = st.columns(3)
with col1:          # 첫번째 칸
    sido_options = ["선택"] + sorted(df_raw['시도'].dropna().unique().tolist())
    selected_sido = st.selectbox("지역 선택", sido_options)
with col2:          # 두번째 칸
    if selected_sido != "선택":
        sigungu_list = ["선택"] + sorted(df_raw[df_raw['시도'] == selected_sido]['시군구'].dropna().unique().tolist())
    else:
        sigungu_list = ["지역을 먼저 선택해 주세요"]
    selected_sigungu = st.selectbox("시/군/구/동 선택", sigungu_list)
with col3:
    # 안내 문구를 (주차장명)에서 (동네명, 도로명 등)으로 변경
    keyword = st.text_input("상세 검색 (동네명, 도로명 등)", "")

# 필터링
filtered_df = df_raw.copy()
if selected_sido != "선택":
    filtered_df = filtered_df[filtered_df['시도'] == selected_sido]
if selected_sigungu != "선택" and selected_sigungu != "지역을 먼저 선택하세요":
    filtered_df = filtered_df[filtered_df['시군구'] == selected_sigungu]
# 3. 상세 검색 (주차장명 -> 주소 기준으로 변경)
if keyword:
    # 주소 컬럼에 사용자가 입력한 키워드가 포함되어 있는지 확인
    filtered_df = filtered_df[filtered_df['주소'].str.contains(keyword, na=False)]

# 메인 리스트
# 주차구획수를 가져와서 정수형으로 변환 (데이터가 없을 경우 0)
display_df = filtered_df[['주차장명', '주소', '운영시간', '기본 금액', '주차구획수']].copy()
display_df['주차구획수'] = display_df['주차구획수'].fillna(0).astype(int)
display_df.rename(columns={'주차구획수': '주차 수'}, inplace=True)
st.subheader(f"📍 검색 결과 ({len(display_df)}건)")
selected = st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row"
)

# 계산 함수
def calculate_parking_fee(duration_hours, data, car_type, additional_discount):
    try:
        # 시간 단위(시)를 분 단위로 변환
        total_minutes = int(duration_hours * 60)
        
        base_time = int(data.get('주차기본시간', 0))
        base_fee = int(data.get('주차기본요금', 0))
        add_time = int(data.get('추가단위시간', 0))
        add_fee = int(data.get('추가단위요금', 0))
        day_fee = data.get('1일주차권요금')
        
        # 기본 요금 계산
        if total_minutes <= base_time:
            total_fee = base_fee
        else:
            # 추가 요금 계산 (올림 방식)
            extra_time = total_minutes - base_time
            import math
            extra_units = math.ceil(extra_time / add_time) if add_time > 0 else 0
            total_fee = base_fee + (extra_units * add_fee)
            
        # 1일 최대 요금 적용 (한도가 설정되어 있는 경우)
        if pd.notna(day_fee) and day_fee > 0:
            total_fee = min(total_fee, int(day_fee))
            
        # 할인율 적용
        discount_rate = 1.0
        # 차량 타입별 할인 (경차, 친환경차 보통 50%)
        if car_type in ["경차", "친환경차"]:
            discount_rate *= 0.5
        
        # 추가 할인 (장애인, 국가유공자 보통 80%, 다자녀 50% 등 - 여기서는 일반적인 기준 적용)
        if additional_discount == "장애인" or additional_discount == "국가유공자":
            discount_rate *= 0.2 # 80% 할인
        elif additional_discount == "다자녀":
            discount_rate *= 0.5 # 50% 할인
            
        return int(total_fee * discount_rate)
    except:
        return 0

# 상세 정보
if len(selected.selection.rows) > 0:
    idx = selected.selection.rows[0]
    data = filtered_df.iloc[idx]
    if data['주차장구분'] == '공영':
        st.markdown("---")
        # 제목 옆에 주차 가능 대수 표시
        parking_count = int(data['주차구획수']) if pd.notna(data['주차구획수']) else 0
        st.subheader(f"🔍 {data['주차장명']} 상세 정보 (총 {parking_count}면)")
        
        # 금액 포맷 함수
        def format_money(val):
            try:
                if pd.isna(val) or val == 0: return "무료💲🤑💰"
                return f"{int(float(val)):,}원"
            except: return "정보없음"

        dataF = pd.DataFrame({
            "구분": ["평일", "토요일", "공휴일"],
            "운영 시간": [data['운영시간'], data['토요일운영시간'], data['공휴일운영시간']]
        })

        # 주차추가단위시간 제외하고 기본/시간당/추가요금만 구성
        base_fee_text = f"{int(data['주차기본시간'])}분 / {format_money(data['주차기본요금'])}" if data['주차기본시간'] > 0 else "무료💲🤑💰"
        add_fee_text = format_money(data.get('추가단위요금', 0)) # 추가단위시간 없이 금액만 표시
        #add_time = f"{int(data['추가단위시간'])}" 
        # 값이 있으면 숫자로 바꾸고, 없으면 '-' 표시
        add_time = int(data['추가단위시간']) if pd.notna(data.get('추가단위시간')) else "-"

        if (data['요금정보'] == "무료") or (data['요금정보'] == "유료" and str(data['주차기본요금']).strip() == "nan"):
            base_fee_text = "무료💲🤑💰"
            m1, m2 = st.columns(2)
            with m1:
                st.metric("**기본 금액**", "무료💲🤑💰" if data['요금정보'] == "무료" else base_fee_text)
            with m2:
                st.write("📅 **상세 운영 시간**")
                st.dataframe(dataF, hide_index=True, use_container_width=True)
        else:    
            m1, m2, m3, m4 = st.columns([1.5, 1, 1, 1])
            with m1:
                st.metric("**기본 금액**", "무료💲🤑💰" if data['요금정보'] == "무료" else base_fee_text)
            with m2:
                if data['요금정보'] != "무료":
                    st.metric(f"**추가 요금({add_time}분**)", add_fee_text)
                else:
                    st.metric("**추가 요금**", "무료")
            with m3:
                # 1일 최대 요금 로직 적용
                daily_val = data.get('1일주차권요금')
                if pd.isna(daily_val) or daily_val == 0:
                    st.metric("1일 최대(입장) 요금", "한도 없음")
                else:
                    st.metric("1일 최대(입장) 요금", f"{int(float(daily_val)):,}원")
            with m4:
                st.write("📅 **상세 운영 시간**")
                st.dataframe(dataF, hide_index=True, use_container_width=True)

        st.markdown("#### 🎁 할인 및 혜택 정보")
        
        # 1. 특기사항 가져오기
        sale_text = data.get('특기사항', "")
        
        # 2. '실질적 유료' 여부 판단 (요금정보가 유료 AND 주차기본요금이 NaN이 아님)
        is_actually_paid = (data['요금정보'] == "유료") and pd.notna(data.get('주차기본요금'))
        
        # 3. 로직 적용
        if is_actually_paid:
            # 실질적 유료인데 특기사항이 없거나 너무 짧으면 기본 할인 문구 출력
            if pd.isna(sale_text) or len(str(sale_text).strip()) < 5:
                sale_text = "• 장애인/국가유공자: 80% 할인\n• 경차/저공해차: 50% 할인\n• 다자녀 가구: 30~50% 할인"
            else:
                sale_text = str(sale_text)
        else:
            # 무료 주차장이거나 기본요금이 없는 경우
            sale_text = "-"
            
        st.info(sale_text)

        # ... [기존 상세 정보 코드 이후] ...

        if data['요금정보'] == "유료" and pd.notna(data.get('주차기본요금')):
            st.markdown("---")
            st.subheader(f"💰 {data['주차장명']} 요금 계산기")
            
            # 입력 영역
            c1, c2, c3 = st.columns([1, 1, 1])
            with c1:
                use_hours = st.selectbox("예상 주차 시간 (시간)",[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
            with c2:
                car_type = st.selectbox("차량 종류", ["승용차", "경차", "친환경차"])
            with c3:
                add_discount = st.selectbox("추가 할인 혜택", ["없음", "장애인", "국가유공자", "다자녀"])
            
            # 계산 실행
            final_fee = calculate_parking_fee(use_hours, data, car_type, add_discount)
            
            # 결과 표시
            st.info(f"⏱️ **{use_hours}시간** 이용 시 예상 주차 요금은 **{final_fee:,}원** 입니다.")
            st.caption("※ 실제 요금은 현장 상황 및 주차장의 운영 규정에 따라 다를 수 있습니다.")
else:
    st.info("💡 목록에서 주차장을 클릭하면 상세 정보를 확인할 수 있습니다.")


