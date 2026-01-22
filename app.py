import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 설정 및 모바일 최적화 CSS
st.set_page_config(page_title="누리키즈 챌린지", page_icon="🎨", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #FFF9E1; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 10px; padding: 10px; }
    .stCheckbox { transform: scale(1.5); margin-top: 10px; }
    div[data-testid="stMetricValue"] { font-size: 1.5rem; color: #FF6B6B; }
    </style>
    """, unsafe_allow_html=True)

# 2. 구글 시트 연결 설정
# 시트 주소 예시: https://docs.google.com/spreadsheets/d/시트ID/edit
SHEET_URL = https://docs.google.com/spreadsheets/d/1CQtgnJKueyfaJs3rUrbtPc8pOCGRtPq9a6BX1Nsok3Y/edit
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 사이드바 구성 (로그인 및 관리자)
st.sidebar.title("🏠 누리키즈")
user_name = st.sidebar.text_input("아이 이름을 입력하세요", value="누리")
is_admin = st.sidebar.toggle("관리자 모드 접속")

# 4. 메인 화면 - 날짜 계산
st.title("🎨 누리키즈 챌린지")
today = datetime.now()
monday = today - timedelta(days=today.weekday())
dates = [(monday + timedelta(days=i)).strftime("%m/%d") for i in range(5)]
week_days = ["월", "화", "수", "목", "금"]

st.info(f"📅 이번 주: {dates[0]} ~ {dates[4]}")

# 5. 모바일 최적화 챌린지 입력 (탭 방식)
tab1, tab2 = st.tabs(["✅ 학습 체크", "✍️ 한글 완성"])

with tab1:
    cols = st.columns(5)
    checks_study = []
    for i in range(5):
        with cols[i]:
            st.write(f"**{week_days[i]}**")
            st.caption(dates[i])
            checks_study.append(st.checkbox(" ", key=f"s_{i}"))
    st.metric("학습 누적 점수", f"{sum(checks_study)} / 5")

with tab2:
    cols = st.columns(5)
    checks_hangeul = []
    for i in range(5):
        with cols[i]:
            st.write(f"**{week_days[i]}**")
            st.caption(dates[i])
            checks_hangeul.append(st.checkbox(" ", key=f"h_{i}"))
    st.metric("한글 누적 점수", f"{sum(checks_hangeul)} / 5")

st.divider()

# 6. 데이터 저장 로직 (구글 시트 쓰기)
if st.button("🎈 오늘의 학습 완료 도장 쾅!", use_container_width=True):
    try:
        # 기존 데이터 불러오기
        existing_data = conn.read(spreadsheet=SHEET_URL)
        
        # 새 데이터 생성
        new_row = pd.DataFrame([{
            "날짜": today.strftime("%Y-%m-%d"),
            "이름": user_name,
            "학습체크": sum(checks_study),
            "한글완성": sum(checks_hangeul)
        }])
        
        # 데이터 합치기
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # 구글 시트 업데이트
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        
        st.balloons()
        st.success(f"🎉 {user_name} 어린이, 오늘 기록이 저장되었습니다!")
    except Exception as e:
        st.error("저장 중 오류가 발생했습니다. 'Secrets' 설정을 확인해주세요.")

# 7. 관리자 모드
if is_admin:
    st.header("📊 관리자 전체 데이터 확인")
    admin_df = conn.read(spreadsheet=SHEET_URL)
    st.dataframe(admin_df, use_container_width=True)

