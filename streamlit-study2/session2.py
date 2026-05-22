import streamlit as st

# 위젯의 매개변수로 key를 지정할 경우
# session_state의 key로 자동 저장한다
#초기화 가드 대신
# 최초 실행시 value 값을 초기값으로 사용.
# 데이터 변경시 -> return -> 마지막 session state 값으로 불러옴.
age_range = st.slider("나이 범위", 0, 80, (0, 80), key = 'age_range')

# 읽기
st.write("현재 선태 값: ", st.session_state['age_range'])
