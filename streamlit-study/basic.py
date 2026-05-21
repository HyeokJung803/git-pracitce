import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_titanic():
    url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
    return pd.read_csv(url)

df = load_titanic().copy()
df['Age'] = df['Age'].fillna(df['Age'].median())

st.title("타이타닉 대시보드")

with st.sidebar:
    st.header("필터")

    pclass_options = st.multiselect("객실 등급", [1, 2, 3], default=[1, 2, 3])
    gender = st.selectbox("성별", ["전체", "male", "female"])
    age_range = st.slider("나이 범위", 0, 80, (0, 80))
    survived_only = st.checkbox("생존자만 보기")

    chart_type = st.selectbox("차트 종류", ["히스토그램", "막대그래프", "파이차트"])

filtered = df[df['Pclass'].isin(pclass_options)]
filtered = filtered[(filtered['Age'] >= age_range[0]) & (filtered['Age'] <= age_range[1])]

if gender != "전체":
    filtered = filtered[filtered['Sex'] == gender]

if survived_only:
    filtered = filtered[filtered['Survived'] == 1]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("선택된 승객", len(filtered))

with col2:
    st.metric("생존자", filtered['Survived'].sum())

with col3:
    rate = f"{filtered['Survived'].mean()*100:.1f}%" if len(filtered) > 0 else "N/A"
    st.metric("생존율", rate)

tab1, tab2 = st.tabs(["📊 차트", "📋 데이터"])

with tab1:
    if len(filtered) == 0:
        st.warning("조건에 맞는 데이터가 없습니다.")
    else:
        if chart_type == "히스토그램":
            fig = px.histogram(filtered, x='Age', nbins=20, title='나이 분포')

        elif chart_type == "막대그래프":
            fig = px.bar(filtered, x='Sex', color='Survived', title='성별 생존 비교')

        elif chart_type == "파이차트":
            survival_counts = filtered['Survived'].value_counts()
            fig = px.pie(values=survival_counts.values, names=['사망', '생존'], title='생존 비율')

        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.dataframe(filtered[['Name', 'Survived', 'Pclass', 'Sex', 'Age', 'Fare']], hide_index=True)