import streamlit as st

home      = st.Page("home.py",      title="홈",      icon="🏠")
dashboard = st.Page("dashboard.py", title="대시보드", icon="📊")


pg = st.navigation([home, dashboard])
pg.run()   # 빠뜨리면 페이지 전환이 안 됨