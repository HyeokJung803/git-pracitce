# overview.py
import streamlit as st
import pandas as pd

# 데이터 로드 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    df = pd.read_csv("data\clothing_data.csv")
    df['주문일자'] = pd.to_datetime(df['주문일자'])
    return df

df = load_data()

# ----------------------------------------------------
# 1. 사이드바 필터 구성 및 세션 상태(session_state) 동기화
# ----------------------------------------------------
st.sidebar.header("📊 전역 필터 설정")

# 카테고리 필터 세션 관리
categories = ["전체"] + sorted(df['카테고리'].unique().tolist())
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "전체"
idx_cat = categories.index(st.session_state.selected_category)
selected_cat = st.sidebar.selectbox("카테고리 선택", categories, index=idx_cat)
st.session_state.selected_category = selected_cat

# 브랜드 필터 세션 관리
brands = ["전체"] + sorted(df['브랜드'].unique().tolist())
if 'selected_brand' not in st.session_state:
    st.session_state.selected_brand = "전체"
idx_brand = brands.index(st.session_state.selected_brand)
selected_brand = st.sidebar.selectbox("브랜드 선택", brands, index=idx_brand)
st.session_state.selected_brand = selected_brand

# ----------------------------------------------------
# 2. 데이터 필터링
# ----------------------------------------------------
filtered_df = df.copy()
if st.session_state.selected_category != "전체":
    filtered_df = filtered_df[filtered_df['카테고리'] == st.session_state.selected_category]
if st.session_state.selected_brand != "전체":
    filtered_df = filtered_df[filtered_df['브랜드'] == st.session_state.selected_brand]

# ----------------------------------------------------
# 3. UI 렌더링 (깔끔한 요약 대시보드)
# ----------------------------------------------------
st.title("📊 판매 실적 요약 대시보드")
st.caption(f"현재 적용된 필터: 카테고리 **[{st.session_state.selected_category}]** | 브랜드 **[{st.session_state.selected_brand}]**")
st.markdown("---")

# 핵심 지표 (KPI) 카드
total_sales = filtered_df['총판매액'].sum()
total_qty = filtered_df['판매수량'].sum()
avg_rating = filtered_df['리뷰평점'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💡 총 판매액", f"{total_sales:,} 원")
col2.metric("📦 총 판매수량", f"{total_qty:,} 개")
col3.metric("⭐ 평균 리뷰 평점", f"{avg_rating:.2f} / 5.0" if not pd.isna(avg_rating) else "N/A")

st.markdown("---")

# 요약 차트: 일별 매출 트렌드
st.subheader("📈 매출 추이 요약")
if not filtered_df.empty:
    trend_df = filtered_df.set_index('주문일자').resample('D')['총판매액'].sum().reset_index()
    st.line_chart(data=trend_df, x='주문일자', y='총판매액')
else:
    st.warning("선택하신 필터 조건에 해당하는 매출 데이터가 없습니다.")