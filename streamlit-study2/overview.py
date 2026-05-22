import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "data", "clothing_data.csv")
    df = pd.read_csv(file_path)
    
    if '총판매액' in df.columns:
        if df['총판매액'].dtype == object:
            df['총판매액'] = df['총판매액'].astype(str).str.replace(r'[$,]', '', regex=True).astype(float)
        else:
            df['총판매액'] = df['총판매액'].astype(float)
            
    if '판매수량' in df.columns:
        if df['판매수량'].dtype == object:
            df['판매수량'] = df['판매수량'].astype(str).str.replace(r'[$,]', '', regex=True).astype(float)
        else:
            df['판매수량'] = df['판매수량'].astype(float)

    df['주문일자'] = pd.to_datetime(df['주문일자'])
    return df

df = load_data()

st.sidebar.header("📊 전역 필터 설정")

categories = ["전체"] + sorted(df['카테고리'].unique().tolist())
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "전체"
idx_cat = categories.index(st.session_state.selected_category)
st.session_state.selected_category = st.sidebar.selectbox("카테고리 선택", categories, index=idx_cat)

brands = ["전체"] + sorted(df['브랜드'].unique().tolist())
if 'selected_brand' not in st.session_state:
    st.session_state.selected_brand = "전체"
idx_brand = brands.index(st.session_state.selected_brand)
st.session_state.selected_brand = st.sidebar.selectbox("브랜드 선택", brands, index=idx_brand)

filtered_df = df.copy()
if st.session_state.selected_category != "전체":
    filtered_df = filtered_df[filtered_df['카테고리'] == st.session_state.selected_category]
if st.session_state.selected_brand != "전체":
    filtered_df = filtered_df[filtered_df['브랜드'] == st.session_state.selected_brand]

st.title("📊 판매 실적 요약 대시보드")
st.caption(f"현재 필터: 카테고리 [{st.session_state.selected_category}] | 브랜드 [{st.session_state.selected_brand}]")
st.markdown("---")

total_sales = filtered_df['총판매액'].sum() if '총판매액' in filtered_df.columns else 0
total_qty = filtered_df['판매수량'].sum() if '판매수량' in filtered_df.columns else 0
avg_rating = filtered_df['리뷰평점'].mean() if '리뷰평점' in filtered_df.columns else 0

# 금액 포맷팅 최적화 (억 단위 쪼개기 및 쉼표 추가)
if total_sales >= 100000000:
    sales_display = f"{total_sales / 100000000:,.2f} 억 원"
else:
    sales_display = f"{int(total_sales):,} 원"

col1, col2, col3 = st.columns(3)
col1.metric("💡 총 판매액", sales_display)
col2.metric("📦 총 판매수량", f"{int(total_qty):,} 개")
col3.metric("⭐ 평균 리뷰 평점", f"{avg_rating:.2f} / 5.0" if not pd.isna(avg_rating) else "N/A")

st.markdown("---")

st.subheader("📈 매출 추이 요약 (단위: 원)")
if not filtered_df.empty and '총판매액' in filtered_df.columns:
    trend_df = filtered_df.set_index('주문일자').resample('D')['총판매액'].sum().reset_index()
    st.line_chart(data=trend_df, x='주문일자', y='총판매액')
else:
    st.warning("데이터가 없습니다.")

st.divider()
uploaded = st.file_uploader("내 데이터 업로드 (CSV)", type=["csv"])
if uploaded is not None:
    user_df = pd.read_csv(uploaded)
    st.success(f"{uploaded.name} ({len(user_df):,}행)")
    st.dataframe(user_df.describe(), use_container_width=True)