
import streamlit as st
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os
# 현재 파일의 위치를 기준으로 프로젝트 루트(상위 폴더)를 파이썬 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from common.sidemenu import display_sidebar
#공통 사이드바 호출
st.set_page_config(page_title=" FAQ 수집기", page_icon="🚗", layout="wide") # 넓게 보기 옵션 추가
display_sidebar()

def run_hyundai_crawler():
    # 1. Selenium 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # UI 환경에서는 headless 권장
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.hyundai.com/kr/ko/e/customer/center/faq"
    faq_list = []

    # UI 영역 설정
    progress_bar = st.progress(0)
    status_text = st.empty()
    data_preview = st.empty()

    try:
        driver.get(url)
        time.sleep(2)
        
        # 메뉴 개수 파악 (최대 9개)
        menu_range = range(1, 10)
        total_menus = len(menu_range)

        for idx, i in enumerate(menu_range):
            # 진행률 계산 및 업데이트
            progress_val = (idx) / total_menus
            progress_bar.progress(progress_val)
            
            try:
                menu_xpath = f'//*[@id="app"]/div[3]/section/div[2]/div/div[2]/section/div/div[1]/div[1]/ul/li[{i}]/button/span'
                menu = driver.find_element(By.XPATH, menu_xpath)
                menu_text = menu.text.strip()
                
                status_text.info(f"🔍 현재 수집 중인 카테고리: **{menu_text}**")
                driver.execute_script("arguments[0].click();", menu)
                time.sleep(1)

                page_numbers = driver.find_elements(By.CLASS_NAME, 'number')
                for n in page_numbers:
                    driver.execute_script("arguments[0].click();", n)
                    time.sleep(1)

                    questions = driver.find_elements(By.CLASS_NAME, 'list-content')
                    for question in questions:
                        q_text = question.text.strip()
                        driver.execute_script("arguments[0].click();", question)
                        time.sleep(0.5)
                        
                        try:
                            answer = driver.find_element(By.CLASS_NAME, 'conts')
                            a_text = answer.text.replace('\n', ' ').strip()
                            faq_list.append([menu_text, q_text, a_text])
                            
                            # 실시간 수집 현황 미리보기 업데이트 (최근 5건)
                            current_df = pd.DataFrame(faq_list, columns=['Category', 'Question', 'Answer'])
                            data_preview.dataframe(current_df.tail(5), use_container_width=True)
                        except:
                            continue
            except Exception as e:
                print(f"항목 파싱 중 오류 발생: {e}")

        progress_bar.progress(1.0)
        status_text.success("✅ 모든 데이터 수집이 완료되었습니다!")

    finally:
        driver.quit()

    return pd.DataFrame(faq_list, columns=['Category', 'Question', 'Answer'])


def run_kia_crawler():
    """
    기아자동차 FAQ 페이지를 크롤링하여 DataFrame을 반환하는 함수
    """
    # 1. Selenium 설정
    chrome_options = Options()

    chrome_options.add_argument('--headless=new') # 최신 헤드리스 모드 사용 권장
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 우회
    
     # 1. 웹 드라이버 설정 (Mac/Linux/Windows 호환)
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.kia.com/kr/customer-service/center/faq"
    driver.get(url)
    
    # 초기 로드 대기
    time.sleep(5)
    
    # 결과 저장용 리스트 (Pandas concat보다 리스트 append가 성능상 유리함)
    faq_data = []
    wait = WebDriverWait(driver, 5)
    
    # UI 영역 설정
    progress_bar = st.progress(0)
    status_text = st.empty()
    data_preview = st.empty()

    try:
        # 메뉴 버튼 찾기
        menus = driver.find_elements(By.CLASS_NAME, 'tabs__btn')
      
        # 메뉴 개수 파악 (최대 9개)
        #menu_range = range(1, 10)
        #total_menus = len(menu_range)
        pidx = 0
        for menu in menus:
            # 진행률 계산 및 업데이트
            pidx += 1
            progress_val = pidx/len(menus)
            progress_bar.progress(progress_val)
            print(progress_val)
            menu_name = menu.text.strip()
            
            status_text.info(f"🔍 현재 수집 중인 카테고리: **{menu_name}**")
            # 메뉴 선택
            driver.execute_script("arguments[0].click();", menu)
            
            # 메뉴 로딩 대기
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'faqinner__wrap')))
            time.sleep(1)

            while True:
                # 현재 활성화된 페이지 번호 확인
                current_page_element = driver.find_element(By.CSS_SELECTOR, '.paging-list li.is-active a')
                current_page = int(current_page_element.text)

                # BeautifulSoup으로 본문 파싱
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                description_divs = soup.find_all('div', class_='faqinner__wrap')

                for idx, description_div in enumerate(description_divs):
                    try:
                        # 질문 추출 (data-link-label)
                        question_button = driver.find_element(By.ID, f'accordion-item-{idx}-button')
                        question=question_button.find_element(By.CSS_SELECTOR,'.cmp-accordion__title').text
                        
                        #question = question_button.get_attribute('data-link-label')
                        
                        # 답변 추출 (p 태그 결합)
                        #p_tags = description_div.find_all('p')
                        p_tags = description_div.select('p, li')
                        answer_text = " ".join([p.get_text(strip=True) for p in p_tags])
                        #print(question)
                        faq_data.append({
                            "Category": menu_name,
                            "Question": question,
                            "Answer": answer_text
                        })
                         # 실시간 수집 현황 미리보기 업데이트 (최근 5건)
                        current_df = pd.DataFrame(faq_data, columns=['Category', 'Question', 'Answer'])
                        data_preview.dataframe(current_df.tail(5), use_container_width=True)
                    except Exception as e:
                        print(f"항목 파싱 중 오류 발생: {e}")

                try:
                    # 다음 페이지 버튼 검색 및 클릭
                    next_page = driver.find_element(By.XPATH, f'//ul[@class="paging-list"]/li[a[text()="{current_page + 1}"]]/a')
                    driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(3)
                except:
                    print(f"카테고리 종료: {menu_name}")
                    break
    
    finally:
        driver.quit()

    return pd.DataFrame(faq_data)

def run_genesis_crawler():
    """제네시스 FAQ 데이터 수집"""
    faq_data = []
    
    # Selenium 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") # 백그라운드 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 감지 우회
    
    # 1. 웹 드라이버 설정 (Mac/Linux/Windows 호환)
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.genesis.com/kr/ko/customer-service/faq"
    driver.get(url)
    
    # 초기 로드 대기
    time.sleep(5)
    
    # 결과 저장용 리스트 (Pandas concat보다 리스트 append가 성능상 유리함)
    faq_data = []
    wait = WebDriverWait(driver, 5)
    
    # UI 영역 설정
    progress_bar = st.progress(0)
    status_text = st.empty()
    data_preview = st.empty()

    try:
        # 메뉴 버튼 찾기
        menus = driver.find_elements(By.CLASS_NAME, 'tabs__btn')
      
        # 메뉴 개수 파악 (최대 9개)
        #menu_range = range(1, 10)
        #total_menus = len(menu_range)
        pidx = 0
        for menu in menus:
            # 진행률 계산 및 업데이트
            pidx += 1
            progress_val = pidx/len(menus)
            progress_bar.progress(progress_val)
            print(progress_val)
            menu_name = menu.text.strip()
            
            status_text.info(f"🔍 현재 수집 중인 카테고리: **{menu_name}**")
            # 메뉴 선택
            driver.execute_script("arguments[0].click();", menu)
            
            # 메뉴 로딩 대기
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'faqinner__wrap')))
            time.sleep(1)

            while True:
                # 현재 활성화된 페이지 번호 확인
                current_page_element = driver.find_element(By.CSS_SELECTOR, '.paging-list li.is-active a')
                current_page = int(current_page_element.text)

                # BeautifulSoup으로 본문 파싱
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                description_divs = soup.find_all('div', class_='faqinner__wrap')

                for idx, description_div in enumerate(description_divs):
                    try:
                        # 질문 추출 (data-link-label)
                        question_button = driver.find_element(By.ID, f'accordion-item-{idx}-button')
                        question=question_button.find_element(By.CSS_SELECTOR,'.cmp-accordion__title').text
                        
                        #question = question_button.get_attribute('data-link-label')
                        
                        # 답변 추출 (p 태그 결합)
                        #p_tags = description_div.find_all('p')
                        p_tags = description_div.select('p, li')
                        answer_text = " ".join([p.get_text(strip=True) for p in p_tags])
                        #print(question)
                        faq_data.append({
                            "Category": menu_name,
                            "Question": question,
                            "Answer": answer_text
                        })
                         # 실시간 수집 현황 미리보기 업데이트 (최근 5건)
                        current_df = pd.DataFrame(faq_data, columns=['Category', 'Question', 'Answer'])
                        data_preview.dataframe(current_df.tail(5), use_container_width=True)
                    except Exception as e:
                        print(f"항목 파싱 중 오류 발생: {e}")

                try:
                    # 다음 페이지 버튼 검색 및 클릭
                    next_page = driver.find_element(By.XPATH, f'//ul[@class="paging-list"]/li[a[text()="{current_page + 1}"]]/a')
                    driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(3)
                except:
                    print(f"카테고리 종료: {menu_name}")
                    break
    
    finally:
        driver.quit()

    return pd.DataFrame(faq_data)
    


# --- Streamlit UI 구성 ---




st.title("🚗 FAQ 크롤러")
st.markdown("버튼을 누르면 고객센터의 FAQ 데이터를 실시간으로 수집합니다.")

# 1. 컬럼 생성 (2개로 분할)
col1, col2 ,col3,col4= st.columns([1,1,1,2])

# 각 변수에 버튼 상태를 저장하여 클릭 후에도 결과가 유지되도록 합니다.
with col1:
    hyundai_clicked = st.button("🚀 현대자동차 FAQ 크롤링 시작", use_container_width=True)

with col2:
    kia_clicked = st.button("🚀 기아자동차 FAQ 크롤링 시작", use_container_width=True)

with col3:
    genesis_clicked = st.button("🚀  제네시스 FAQ 크롤링 시작", use_container_width=True)
    
# --- 결과 출력 영역 ---
#반복되는 출력 로직을 함수로 만들면 코드가 깔끔해집니다.
def display_results(df, filename):
    st.divider()
    st.subheader(f"📊 수집 결과 요약 ({filename})")
    st.write(f"총 **{len(df)}** 건의 데이터를 수집했습니다.")
    
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 CSV 파일 다운로드",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )
    st.dataframe(df, use_container_width=True)


# 버튼이 눌렸을 때 각각의 로직 실행
if hyundai_clicked:
    with st.spinner("현대차 데이터를 수집 중입니다..."):
        result_df = run_hyundai_crawler()
        if not result_df.empty:
            now = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"hyundai_faq_{now}.csv"
            display_results(result_df, filename)

if kia_clicked:
    with st.spinner("기아차 데이터를 수집 중입니다..."):
        result_df = run_kia_crawler()
        if not result_df.empty:
            now = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"kia_faq_{now}.csv"
            display_results(result_df, filename)

if genesis_clicked:
    with st.spinner("제네시스 데이터를 수집 중입니다..."):
        result_df = run_genesis_crawler()
        if not result_df.empty:
            now = datetime.now().strftime("%Y%m%d_%H%M")
            filename = f"genesis_faq_{now}.csv"
            display_results(result_df, filename)

#