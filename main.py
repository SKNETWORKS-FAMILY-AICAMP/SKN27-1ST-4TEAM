from common.sidemenu import display_sidebar  # 공통 모듈 임포트
import streamlit as st
import sys
import os



sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 사이드바 메뉴 표시
display_sidebar()


# 스타일 설정
# 버튼, 카드 크기, 폰트 등 전체적인 디자인
st.markdown("""
<style>
    /* 전체 배경색 */
    .main { background-color: #f8f9fa; }

    /* 카드 제목 스타일 */
    .card-title {
        font-size: 18px;
        font-weight: 700;
        color: #212529;
        margin-bottom: 8px;
    }
    /* 버튼 스타일 (높이, 글자 크기, 모서리 둥글기) */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
        height: 60px;
        font-size: 16px;
    }
    /* 페이지 제목 스타일 */
    h1 {
        color: #212529;
        font-weight: 800;
        margin-bottom: 32px;
    }
     /* 카드 너비 설정 (숫자가 클수록 카드가 넓어짐) */
    .block-container {
        max-width: 950px;     
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ---- UI ----
st.title("홈페이지")

import streamlit as st
import streamlit.components.v1 as components
import json

# ---- 체크박스로 동물 선택 ----
col_a, col_b = st.columns([3, 6])
with col_a:
    with st.expander("SKN27-1st-4team"):
        inner_col1, inner_col2 = st.columns(2)  # ← 변수명 변경
        with inner_col1:
            use_cat = st.checkbox("🐱 고양이", value=False)
        with inner_col2:
            use_dog = st.checkbox("🐶 강아지", value=False)

# 선택 모드 결정
if use_cat and use_dog:
    mode = 'both'
elif use_dog:
    mode = 'dog'
elif use_cat:
    mode = 'cat'
else:
    mode = 'none'  # 둘 다 미선택

cat_messages = ['야옹~ 주차완료!', '냥냥 주차~', '여기다 세우면 되겠다냥!']
dog_messages = ['멍멍~ 주차완료!', '왈왈 주차~', '여기다 세우면 되겠다멍!']
both_messages = ['둘이 같이 주차완료!', '🐱🐶 베프 주차~', '냥멍 주차 성공!']

if mode != 'none':
    components.html(f"""
    <style>
    body {{ margin: 0; overflow: hidden; background: transparent; height: 140px; }}

    #parking-area {{
        position: absolute;
        bottom: 10px; right: 20px;
        width: 90px; height: {'90px' if mode == 'both' else '60px'};
        border: 3px solid #ffcc00;
        border-radius: 4px;
        background: rgba(255, 204, 0, 0.08);
        transform: perspective(300px) rotateX(40deg);
    }}
    #parking-area::after {{
        content: '';
        position: absolute; top: 50%; left: 10%;
        width: 80%; height: 2px;
        background: rgba(255, 204, 0, 0.4);
        transform: translateY(-50%);
    }}
    #parking-label {{
        position: absolute;
        bottom: 10px; right: 20px;
        width: 90px; height: {'90px' if mode == 'both' else '60px'};
        display: flex; align-items: center; justify-content: center;
        transform: perspective(300px) rotateX(40deg);
        z-index: 10; pointer-events: none;
    }}
    #parking-label span {{
        font-size: 9px; font-weight: bold;
        color: #ffcc00; letter-spacing: 1px;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        white-space: nowrap; font-family: sans-serif;
    }}
    #parking-sign {{
        position: absolute; bottom: 98px; right: 42px;
        background: #1a73e8; color: white; font-weight: bold;
        border-radius: 50%; width: 26px; height: 26px;
        display: flex; align-items: center; justify-content: center;
        font-family: Arial; font-size: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }}
    #bubble {{
        position: absolute; bottom: 100px; right: 120px;
        background: white; border: 2px solid #333;
        border-radius: 12px; padding: 6px 10px;
        font-size: 13px; opacity: 0; transition: opacity 0.3s;
        white-space: nowrap; font-family: sans-serif;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }}
    #bubble::after {{
        content: ''; position: absolute;
        bottom: -10px; right: 16px;
        border: 5px solid transparent;
        border-top-color: #333;
    }}

    /* 고양이 차 */
    #car1 {{
        position: absolute; bottom: 15px; left: -80px;
        font-size: 40px; line-height: 1;
        transform: scaleX(-1) perspective(300px) rotateX(30deg);
        filter: drop-shadow(0px 4px 3px rgba(0,0,0,0.3));
    }}
    #animal1 {{
        position: absolute; bottom: 40px; left: -60px;
        font-size: 18px; line-height: 1;
        transform: perspective(300px) rotateX(30deg);
    }}
    #shadow1 {{
        position: absolute; bottom: 8px; left: -70px;
        width: 50px; height: 12px;
        background: rgba(0,0,0,0.15);
        border-radius: 50%; filter: blur(4px);
    }}

    /* 강아지 차 (both 모드에서만 표시) */
    #car2 {{
        position: absolute; bottom: 65px; left: -80px;
        font-size: 40px; line-height: 1;
        transform: scaleX(-1) perspective(300px) rotateX(30deg);
        filter: drop-shadow(0px 4px 3px rgba(0,0,0,0.3));
        display: {'block' if mode == 'both' else 'none'};
    }}
    #animal2 {{
        position: absolute; bottom: 90px; left: -60px;
        font-size: 18px; line-height: 1;
        transform: perspective(300px) rotateX(30deg);
        display: {'block' if mode == 'both' else 'none'};
    }}
    #shadow2 {{
        position: absolute; bottom: 58px; left: -70px;
        width: 50px; height: 12px;
        background: rgba(0,0,0,0.15);
        border-radius: 50%; filter: blur(4px);
        display: {'block' if mode == 'both' else 'none'};
    }}

    .particle {{
        position: absolute; font-size: 16px; pointer-events: none;
        animation: pop 1s ease-out forwards;
    }}
    @keyframes pop {{
        0%   {{ opacity: 1; transform: translateY(0) scale(1); }}
        100% {{ opacity: 0; transform: translateY(-40px) scale(0.5); }}
    }}
    </style>

    <div id="parking-sign">P</div>
    <div id="parking-area"></div>
    <div id="parking-label"><span>공영주차장</span></div>
    <div id="bubble"></div>

    <!-- 첫번째 (고양이 or 강아지) -->
    <div id="shadow1"></div>
    <div id="car1">🚗</div>
    <div id="animal1">{'🐱' if mode != 'dog' else '🐶'}</div>

    <!-- 두번째 (both 모드에서만) -->
    <div id="shadow2"></div>
    <div id="car2">🚗</div>
    <div id="animal2">🐶</div>

    <script>
    var mode = '{mode}';

    var car1    = document.getElementById('car1');
    var animal1 = document.getElementById('animal1');
    var shadow1 = document.getElementById('shadow1');
    var car2    = document.getElementById('car2');
    var animal2 = document.getElementById('animal2');
    var shadow2 = document.getElementById('shadow2');
    var bubble  = document.getElementById('bubble');

    var x = -80;
    var speed = 4;
    var phase = 'run';
    var screenW = window.innerWidth;
    var parkingX = screenW - 130;

    var catMsg  = {json.dumps(cat_messages)};
    var dogMsg  = {json.dumps(dog_messages)};
    var bothMsg = {json.dumps(both_messages)};

    function getMessages() {{
        if (mode === 'both') return bothMsg;
        if (mode === 'dog')  return dogMsg;
        return catMsg;
    }}

    function showBubble(msg) {{
        bubble.textContent = msg;
        bubble.style.opacity = '1';
        setTimeout(function() {{ bubble.style.opacity = '0'; }}, 2000);
    }}

    function spawnParticles() {{
        var emojis = ['✨','⭐','💛','🐾','❤️'];
        for (var i = 0; i < 5; i++) {{
            (function(i) {{
                setTimeout(function() {{
                    var p = document.createElement('div');
                    p.className = 'particle';
                    p.textContent = emojis[i % emojis.length];
                    p.style.right = (20 + Math.random() * 80) + 'px';
                    p.style.bottom = (20 + Math.random() * 60) + 'px';
                    document.body.appendChild(p);
                    setTimeout(function() {{ p.remove(); }}, 1000);
                }}, i * 150);
            }})(i);
        }}
    }}

    function resetAll() {{
        x = -80;
        [car1, animal1, shadow1, car2, animal2, shadow2].forEach(function(el) {{
            el.style.transition = '';
            el.style.opacity = '1';
        }});
        car1.style.left    = x + 'px';
        animal1.style.left = (x + 20) + 'px';
        shadow1.style.left = (x + 10) + 'px';
        animal1.style.bottom = '40px';

        car2.style.left    = x + 'px';
        animal2.style.left = (x + 20) + 'px';
        shadow2.style.left = (x + 10) + 'px';
        animal2.style.bottom = '90px';

        phase = 'run';
    }}

    function animate() {{
        if (phase === 'run') {{
            x += speed;

            /* 첫번째 차 이동 */
            car1.style.left    = x + 'px';
            animal1.style.left = (x + 20) + 'px';
            shadow1.style.left = (x + 10) + 'px';

            /* 두번째 차 이동 (both 모드) */
            if (mode === 'both') {{
                car2.style.left    = x + 'px';
                animal2.style.left = (x + 20) + 'px';
                shadow2.style.left = (x + 10) + 'px';
            }}

            if (x >= parkingX) {{
                phase = 'arrive';

                /* 동물들 내리기 */
                animal1.style.transition = 'bottom 0.5s ease, left 0.4s ease';
                setTimeout(function() {{
                    animal1.style.bottom = '12px';
                    animal1.style.left = (x - 10) + 'px';
                }}, 50);

                if (mode === 'both') {{
                    animal2.style.transition = 'bottom 0.5s ease, left 0.4s ease';
                    setTimeout(function() {{
                        animal2.style.bottom = '62px';
                        animal2.style.left = (x - 10) + 'px';
                    }}, 50);
                }}

                spawnParticles();
                var msgs = getMessages();
                showBubble(msgs[Math.floor(Math.random() * msgs.length)]);

                setTimeout(function() {{
                    [car1, animal1, shadow1, car2, animal2, shadow2].forEach(function(el) {{
                        el.style.transition = 'opacity 0.8s';
                        el.style.opacity = '0';
                    }});
                    phase = 'hide';
                    setTimeout(function() {{ resetAll(); }}, 1000);
                }}, 2000);
            }}
        }}
        requestAnimationFrame(animate);
    }}

    animate();
    </script>
    """, height=140)


# ---- 상단 카드 2개 (자동차 등록 현황 / 기업별 FAQ) ----
# col1, col2 로 화면을 좌우 2칸으로 나눔
col1, col2 = st.columns(2, gap="medium")

with col1:
    with st.container(border=True):
        st.markdown("#### 🚗 자동차 등록 현황")
        st.caption("자동차 등록 현황 그래프")
        if st.button("자동차 등록 현황 보기 →", use_container_width=True, key="btn_reg"):
            st.switch_page("pages/01_registration.py")

with col2:
    with st.container(border=True):
        st.markdown("#### 기업별 FAQ 조회")
        st.caption("기업별 FAQ 크롤링 및 조회")
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("🔍 크롤링", use_container_width=True, key="btn_crawl"):
                st.switch_page("pages/02_faq_crawling.py")
        with btn_col2:
            if st.button("💾 DB 저장", use_container_width=True, key="btn_db"):
                st.switch_page("pages/02_faq_db_insert.py")
        with btn_col3:
            if st.button("🔎 FAQ 검색", use_container_width=True, key="btn_faq"):
                st.switch_page("pages/02_faq_search.py")

st.markdown("<br>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("#### 🅿️ 지역별 공영 주차장")
    st.caption("지역별 맞춤 주차장 정보 제공")
    if st.button("공영 주차장 조회 →", use_container_width=True, key="btn_park"):
        st.switch_page("pages/03_parking.py")

