import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_titanic():
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
    return pd.read_csv(url)

df = load_titanic().copy()
df['Age'] = df['Age'].fillna(df['Age'].median())

# 사이드바
with st.sidebar:
    st.header("필터")
    st.divider()

    pclass_options = st.multiselect(
        "객실 등급",
        [1, 2, 3],
        default=[1, 2, 3]
    )

    gender = st.selectbox("성별", ["전체", "male", "female"])
    age_range = st.slider("나이 범위", 0, 80, (0, 80))
    survived_only = st.checkbox("생존자만 보기")

# 필터링
filtered = df[df['Pclass'].isin(pclass_options)]
filtered = filtered[(filtered['Age'] >= age_range[0]) & (filtered['Age'] <= age_range[1])]

if gender != "전체":
    filtered = filtered[filtered['Sex'] == gender]

if survived_only:
    filtered = filtered[filtered['Survived'] == 1]

# 탭
tab1, tab2, tab3 = st.tabs(
    ["📊 나이 분포", "📊 등급별 생존", "📋 데이터"]
)

with tab1:
    fig = px.histogram(filtered, x='Age', nbins=20, title='나이 분포')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("👉 나이가 어릴수록 생존 경향이 있는지 확인")

with tab2:
    surv = filtered.groupby('Pclass')['Survived'].mean().reset_index()
    fig2 = px.bar(
        surv,
        x='Pclass',
        y='Survived',
        title='등급별 생존율',
        template='simple_white'
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("👉 1등급 생존율이 가장 높음")

with tab3:
    st.dataframe(
        filtered[['Name','Survived','Pclass','Sex','Age','Fare']],
        hide_index=True
    )