import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_imdb():
    df = pd.read_csv('imdb_top_1000.csv')
    df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
    return df

imdb = load_imdb().copy()

st.title("IMDB 대시보드")

with st.sidebar:
    min_rating = st.slider("최소 평점", 7.0, 9.5, 7.6, step=0.1)
    year_range = st.slider("개봉 연도", 1920, 2020, (2000, 2020))

filtered = imdb[
    (imdb['IMDB_Rating'] >= min_rating) &
    (imdb['Released_Year'] >= year_range[0]) &
    (imdb['Released_Year'] <= year_range[1])
]

st.metric("영화 개수", len(filtered))
st.dataframe(filtered)

filtered1 = imdb[
    (imdb['IMDB_Rating'] >= 9.0) &
    (imdb['Released_Year'] >= 2000)
]

st.metric("2000년 이후 평점 9점 이상 영화", len(filtered1))
st.dataframe(filtered1)

fig = px.histogram(
    filtered,
    x="IMDB_Rating",
    nbins=20,
    title="평점 분포"
)

st.plotly_chart(fig, use_container_width=True)

fig1 = px.scatter(
    filtered,
    x="Released_Year",
    y="IMDB_Rating",
    hover_name="Series_Title",
    hover_data=["Genre", "Runtime"],
    title="연도 vs 평점"
)

st.plotly_chart(fig1, use_container_width=True)