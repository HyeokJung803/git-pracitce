import streamlit as st
import plotly.express as px
import pandas as pd

# 텍스트 입력
name = st.text_input("이름", placeholder="홍길동")

# 드롭다운
gender = st.selectbox("성별", ["전체", "male", "female"])

# 범위 슬라이더
age_min, age_max = st.slider("나이 범위", 0, 100, (20, 60))

# 버튼
if st.button("확인"):
    st.write("버튼이 눌렸습니다!")

# 체크박스
show = st.checkbox("원본 데이터 보기")

# 다중 선택
opts = st.multiselect("등급", [1, 2, 3], default=[1, 2, 3])

# with 블록 안 = 사이드바
with st.sidebar:
    st.header("필터")
    pclass = st.selectbox("객실 등급", [1, 2, 3])
    survived_only = st.checkbox("생존자만")

# 메인 화면
st.title("타이타닉 대시보드")
st.write(f"선택된 등급: {pclass}")

@st.cache_data
def load_titanic():
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
    return pd.read_csv(url)

titanic = load_titanic().copy()

# ── 위젯 ──────────────────────────────────────────────────────────────────────
pclass = st.selectbox("객실 등급", [1, 2, 3])
survived_only = st.checkbox("생존자만 보기")

# ── 필터 적용 ─────────────────────────────────────────────────────────────────
filtered = titanic[titanic['Pclass'] == pclass]
if survived_only:
    filtered = filtered[filtered['Survived'] == 1]

st.write(f"결과: {len(filtered)}명")
st.dataframe(filtered.head(3), hide_index = True, width = 'stretch')

st.metric(label="생존율", value="38.4%", delta="+2.1%")

# delta_color
st.metric("비용", "1,500원", "-100원",
          delta_color="inverse")   # 낮을수록 좋을 때

@st.cache_data
def load_titanic():
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
    return pd.read_csv(url)

titanic = load_titanic()

fig = px.scatter(
    titanic, x='Age', y='Fare',
    color='Survived',
    hover_name='Name',
    title='나이 vs 요금',
    template='simple_white'
)

# ✅ width='stretch': 전체 너비 (최신 API)
st.plotly_chart(fig, width='stretch')