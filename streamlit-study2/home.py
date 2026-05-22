# home.py
import streamlit as st
name = st.text_input("이름을 입력하세요", key='user_name')
if st.session_state.get('user_name'):
    st.info("대시보드 페이지로 이동해보세요.")