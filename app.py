import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="누리키즈 챌린지", page_icon="🎨", layout="wide")

# 귀여운 스타일 적용
st.markdown("""
    <style>
    .main { background-color: #FFF9E1; }
    .stButton>button { background-color: #FF6B6B; color: white; border-radius: 20px; }
    h1 { color: #4A4A4A; font-family: 'Nanum Gothic', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 누리키즈 챌린지")

# 2. 구글 시트 연결 (간편 방식)
# 아래 'YOUR_SHEET_ID' 부분에 1단계에서 복사한 시트 ID를 넣으세요.
SHEET_ID = '1CQtgnJKueyfaJs3rUrbtPc8pOCGRtPq9a6BX1Nsok3Y'
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=Sheet1'

# 3. 사이드바 - 로그인 및 정보
st.sidebar.header("🏠 입장하기")
user_name = st.sidebar.text_input("아이 이름을 입력하세요", value="누리")
is_admin = st.sidebar.checkbox("관리자 모드")

# 4. 메인 화면 - 이번 주 날짜 계산
today = datetime.now()
monday = today - timedelta(days=today.weekday())
week_days = ["월", "화", "수", "목", "금"]
dates = [(monday + timedelta(days=i)).strftime("%m/%d") for i in range(5)]

st.subheader(f"📅 {today.strftime('%m월 %d일')} 오늘의 학습")

# 5. 챌린지 표 (이미지 구현)
# 헤더
cols = st.columns([1.5, 1, 1, 1, 1, 1, 1.2])
cols[0].write("**구분**")
for i, day in enumerate(week_days):
    cols[i+1].write(f"**{day}({dates[i]})**")
cols[6].write("**누적**")

st.divider()

# 학습 체크 행
row1 = st.columns([1.5, 1, 1, 1, 1, 1, 1.2])
row1[0].write("✅ **학습 체크**")
c1 = [row1[i+1].checkbox(" ", key=f"study_{i}") for i in range(5)]
row1[6].write(f"**{sum(c1)} / 5**")

# 한글 완성 행
row2 = st.columns([1.5, 1, 1, 1, 1, 1, 1.2])
row2[0].write("✍️ **한글 완성**")
c2 = [row2[i+1].checkbox(" ", key=f"hangeul_{i}") for i in range(5)]
row2[6].write(f"**{sum(c2)} / 5**")

# 6. 저장 기능
if st.button("오늘의 학습 완료! 도장 쾅!"):
    # 실제 운영시에는 여기서 구글 시트로 데이터를 전송하는 코드가 작동합니다.
    st.balloons()
    st.success(f"🎉 {user_name} 어린이, 오늘 정말 잘했어요!")

# 7. 관리자 모드
if is_admin:
    st.divider()
    st.header("🔍 관리자 데이터 확인")
    try:
        df = pd.read_csv(SHEET_URL)
        st.dataframe(df)
    except:
        st.info("구글 시트에 데이터가 쌓이면 이곳에서 한눈에 볼 수 있습니다.")