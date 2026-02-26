# SKN27 1차 프로젝트 | Park킹

---

> 본 문서는 프로젝트 진행에 따라 지속적으로 업데이트됩니다.

---

## 👥팀 소개

저렴한 공영주차장을 가장 간편하게 찾을 수 있는 주차왕 **<mark>Park킹</mark>**


## 👥멤버

<table align="center">
  <tr>
    <td align="center"><b>박창제</b></td>
    <td align="center"><b>김경호</b></td>
    <td align="center"><b>문재경</b></td>
    <td align="center"><b>박송원</b></td>
    <td align="center"><b>임희진</b></td>
  </tr>

  <tr>
    <td align="center"><a href="https://github.com/ChangJe-P"><img src="https://img.shields.io/badge/ChangJe--P-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/guard884"><img src="https://img.shields.io/badge/guard884-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/mesrwi-arch"><img src="https://img.shields.io/badge/mesrwi--arch-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/SongwonPark08"><img src="https://img.shields.io/badge/SongwonPark08-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>
    <td align="center"><a href="https://github.com/imhuijin"><img src="https://img.shields.io/badge/imhuijin-181717?style=for-the-badge&logo=github&logoColor=white"></a></td>

  </tr>
</table>

---

## 📌 프로젝트 주제


**<mark>전국 자동차 등록 현황 및 기업 FAQ 조회 시스템</mark> & <mark>전국 공영주차장의 차종별 요금 조회 시스템 구축</mark>**



## 📌 프로젝트 기간

2026/ 02/ 25 (수) ~ 2026/ 02/ 26 (목)

---

## 📌 프로젝트 배경



![alt text](/image/asd.jpg)
![alt text](/image/asd2.jpg)


### ✅: 전국 자동차 등록 현황과 더불어 <mark>국내 국산차 **점유율의 90%이상을 차지하고 있는 현대와 기아의 FAQ 조회** 시스템을 구축</mark>했습니다.


![alt text](/image/asd3.png)
![alt text](/image/asd4.png)
![alt text](/image/asd5.png)
![alt text](/image/asd6.png)



### ✅: **<mark>빠른 차량 증가 속도 + 주차 공간 확보 부족</mark>**


![alt text](/image/asd7.png)

### ➡️ <mark>국가 차원에서 공영 주차장 확충으로 주차 문제 해결을 시도했으나 **할인 기준 및 요금이 통일되지 않아** 운전자들이 혼란</mark>스러워하는 현황입니다.



### ➡️➡️  이러한 문제 해결에 기여하기 위해 <mark>**전국 공영주차장의 차종별 요금 조회** 시스템 추가</mark>를 시도했습니다.

---



## 📌 프로젝트 목표 및 소개

1️⃣ : <mark>**전국 자동차 등록 현황** 및 **현대와 기아의 FAQ를 조회**</mark>할 수 있는 웹사이트를 구축하고자 합니다.


2️⃣ : 전국 공영 주차장의 위치 및 요금 데이터를 기반으로 운전자들에게 목적지 근처의 <mark>**공영주차장의 정확한 할인 및 요금 정보를 제공**</mark>하고자 합니다.




---

## 📌 프로젝트 내용

1️⃣ <mark>**자동차 등록 현황</mark>**
: 전국 자동차 등록 현황과 주차장 수를 이용하여 주차장 비율 확인가능 페이지


2️⃣ <mark>**FAQ 페이지</mark>**
: 각 자동차 기업 별 FAQ를 필터링 및 검색해 조회 가능한 페이지
 
 
 -크롤링 화면
 
 - 데이터베이스 저장 화면
 
 - FAQ 조회 화면


3️⃣ <mark>**주차장 현황</mark>**
: 전국 공영 주차장 장소 확인 및 검색, 주차장 정보(요금 및 운영시간 등) 조회가 가능한 페이지


---




## 🛠️ 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

---

## 요구사항 명세서


| No | 요구사항             | 구현 여부 | 상세 요구 사항                                | 비고                                  |
|----|----------------------|-----------|-----------------------------------------------|----------------------------------------|
| 1  | 차량 등록 현황       | 0         | 전국 자동차 등록 현황 조회 가능        | -                                      |
| 2  | 인구별 차량 통계 확인     | X         | 차량 규모 별 인구 통계 확인 기능 구현       | 기간 내 구현 불가하여 추후 추가 예정                                      |
| 3  | 주차 요금 계산       | 0         | 예상 주차 시간 별 금액 조회 가능     | -                                      |
| 4  | 주차장 지도 조회     | X         | 검색된 주차장의 위치를 지도로 확인 가능 | 기간 내 구현 불가하여 추후 추가 예정 |
| 5  | FAQ 조회             | 0         | 기업 별 FAQ 조회                              | -                                      |
| 6  | 데이터 크롤링             | 0         | 크롤링을 통해 기업 별 FAQ 데이터를 수집                              | -                                      |
| 7  | 데이터 베이스 구현             | 0         | 크롤링한 데이터를 이용해 데이터 베이스를 구현                              | -                                      |

---

## 🧩 데이터베이스 설계문서: ERD

![alt text](/image/ERD1.png)

---

## 🧩 수집 데이터: 어떤 데이터를 어떻게 수집하였는지

**전국 공영주차장 정보**

[![주차장 데이터](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN27-1ST-4TEAM/blob/feature-README/%EC%A3%BC%EC%B0%A8%EC%9E%A5%20%EB%8D%B0%EC%9D%B4%ED%84%B0.png)](https://www.data.go.kr/data/15012896/standard.do)


**전국 자동차 등록 정보**

[![자동차 등록](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN27-1ST-4TEAM/blob/feature-README/%EC%9E%90%EB%8F%99%EC%B0%A8%20%EB%93%B1%EB%A1%9D.png)](https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58&hFormId=5498&hSelectId=5498&hPoint=00&hAppr=1&hDivEng=&oFileName=&rFileName=&midpath=&sFormId=5498&sStart=202601&sEnd=202601&sStyleNum=2&settingRadio=xlsx)

**FAQ 데이터**

[![현대](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN27-1ST-4TEAM/blob/feature-README/%EC%9E%90%EB%8F%99%EC%B0%A8%20%EB%93%B1%EB%A1%9D.png)](https://www.hyundai.com/kr/ko/e/customer/center/faq)

[![기아](https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN27-1ST-4TEAM/blob/feature-README/%EC%9E%90%EB%8F%99%EC%B0%A8%20%EB%93%B1%EB%A1%9D.png)](https://www.kia.com/kr/customer-service/center/faq)


---

## 🧩 데이터 조회 프로그램: 화면 설계서

![alt text](/image/image.png)


---

## ⚡ 주요 시스템 기능 구현 : 실제 구현된 화면과 기능


## <mark>**홈페이지**</mark>
각 세션의 버튼을 통해 해당 페이지로 이동할 수 있습니다.



   > 😸🐶 고양이와 강아지 공영주차장에 운전 및 주차


## <mark>**자동차등록현황**</mark>



## <mark>**FAQ**</mark>
세부적으로 나누면 **크롤링, 데이터베이스 저장 ,faq조회** 총 3가지로 나눌 수 있습니다.
 
###   **크롤링 화면**

   👉
   
   버튼을 통해 원하는 기업의 FAQ 크롤링 작업 수행 가능

  
   👉
   
   크롤링 진행 정도와 크롤링 결과를 실시간으로 보여줌

  
   👉
   
   완료되면, 결과를 요약해서 보여주고 CSV 파일로 다운로드할 수 있음
   
 	
###   **데이터베이스 저장 화면**(먼저 도커가 실행 중인지 확인)
    
   👉
   
   데이터베이스 & 테이블 생성 버튼 -> 크롤링 결과를 저장할 테이블 생성
 
 
   👉
   
   크롤링 결과 파일(csv) 업로드 > 데이터베이스에 저장(버튼)
    
 	
###   **FAQ 조회 화면**
   
   👉
   
   저장한 데이터베이스 상에서 FAQ 정보를 보여줌
   
   
   👉
   
   원하는 브랜드 선택할 수 있고, 그에 따라 카테고리도 변경됨

## <mark>**주차장**</mark>
세부적으로 나누면 **위치 선택 및 검색**, **주차장 정보 조회**


### **위치 선택 및 검색**
   👉
   
   대분류(지역선택)->소분류(시/군/구/동)->상세주소(지역명)
   
   
   👉
   
   검색 후 원하는 주차장 선택

### **주차장 상세 정보 조회**

   👉
   
   검색 결과에 있는 데이터 클릭 시 해당 주차장의 상세 정보 확인 가능
   
   > 무료 주차장과 유료 주차장의 상세 정보를 달리함
   
   👉 
   
   무료 주차장 선택 시 주차 요금(무료), 운영 시간 조회 가능
   
   👉
   
   유료 주차장 선택 시 요금 정보, 추가 시간 별 요금 정보, 운영 시간 조회 가능
   예상 주차 시간에 따른 요금 계산 기능 구현
   (예상 주차 시간, 차량 종류, 할인 혜택 선택 후 예상 금액 조회 가능) 
   
   최대 이용 요금이 정해져있는 경우, 최대 이용 요금 초과된 시간으로 요금 조회하면 최대 이용 요금으로 조회
   
   이용 요금이 입장료인 경우, 입장료 자체를 최대 이용 요금으로 설정
   

---
