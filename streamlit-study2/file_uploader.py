import streamlit as st
import pandas as pd

uploaded = st.file_uploader("CSV 파일을 선택하세요", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success(f"로드 완료: {uploaded.name}  ({len(df):,}행)")
    st.dataframe(df.head())
else:
    st.info("CSV 파일을 업로드하면 미리보기가 표시됩니다.")