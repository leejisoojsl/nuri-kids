import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 설정 및 디자인 ---
st.set_page_config(page_title="누리키즈 챌린지", layout="centered") # 모바일을 위해 centered 설정

st.markdown("""
    <style>
    /* 모바일에서 글자 크기 조정 */
    .stCheckbox { transform: scale(1.2); }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 누리키즈 챌린지")

# --- 구글 시트 연결 설정 ---
# 1. 시트의 공유 설정을 '링크가 있는 모든 사용자 - 편집자'로 반드시 변경하세요.
SHEET_ID = '1CQtgnJKueyfaJs3rUrbtPc8pOCGRtPq9a6BX1Nsok3Y' 
SHEET_NAME = '관리자'
CSV_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
EXPORT_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/externaldata/google-visualizaton?tqx=out:csv'

# --- 데이터 저장 함수 ---
def save_to_google(name, study_score, hangeul_score):
    # 실제 운영 환경에서는 'st.connection'이나 'gspread' 라이브러리가 필요하지만,
    # 기획자용 가장 쉬운 방법은 URL 파라미터를 이용하는 방식입니다.
    # 우선은 '성공 메시지'와 함께 관리자가 볼 수 있게 데이터 프레임을 구성합니다.
    st.session_state['last_save'] = {
        "날짜": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "이름": name,
        "학습체크": f"{study_score}/5",
        "한글완성": f"{hangeul_score}/5"
    }

# --- 사이드바 로그인 ---
user_name = st.sidebar.text_input("아이 이름", value="누리")
is_admin = st.sidebar.toggle("관리자 모드")

# --- 메인 챌린지 화면 ---
today = datetime.now()
monday = today - timedelta(days=today.weekday())
dates = [(monday + timedelta(days=i)).strftime("%m/%d") for i in range(5)]

st.info(f"📅 이번 주 챌린지 ({dates[0]} ~ {dates[4]})")

# 모바일 대응을 위해 탭(Tabs) 기능 활용 (강력 추천)
tab1, tab2 = st.tabs(["✅ 학습 체크", "✍️ 한글 완성"])

with tab1:
    cols = st.columns(5)
    checks_study = []
    for i in range(5):
        with cols[i]:
            st.write(f"{['월','화','수','목','금'][i]}")
            checks_study.append(st.checkbox(" ", key=f"s_{i}"))
    st.metric("학습 누적 점수", f"{sum(checks_study)} / 5")

with tab2:
    cols = st.columns(5)
    checks_hangeul = []
    for i in range(5):
        with cols[i]:
            st.write(f"{['월','화','수','목','금'][i]}")
            checks_hangeul.append(st.checkbox(" ", key=f"h_{i}"))
    st.metric("한글 누적 점수", f"{sum(checks_hangeul)} / 5")

st.divider()

if st.button("🎈 오늘의 학습 완료 도장 쾅!", use_container_width=True):
    save_to_google(user_name, sum(checks_study), sum(checks_hangeul))
    st.balloons()
    st.success(f"{user_name} 어린이, 저장이 완료되었습니다!")

# --- 관리자 모드 데이터 출력 ---
if is_admin:
    st.header("📊 관리자 실시간 데이터")
    # 구글 시트 읽어오기
    try:
        df = pd.read_csv(CSV_URL)
        st.write("현재 구글 시트에 저장된 데이터:")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.warning("구글 시트 ID를 확인해주세요. 또는 아직 데이터가 없습니다.")
    
    if 'last_save' in st.session_state:
        st.write("📍 방금 입력된 최신 기록 (아직 시트 전송 전):")
        st.json(st.session_state['last_save'])
