import streamlit as st

home      = st.Page("home.py",      title="홈",      icon="🏠")
dashboard = st.Page("dashboard.py", title="대시보드", icon="📊")
overview = st.Page("overview.py", title="요약",     icon="📊")
detail   = st.Page("detail.py",   title="상세 분석", icon="🔍")
pg = st.navigation([home, dashboard, overview, detail])
pg.run()   # 빠뜨리면 페이지 전환이 안 됨