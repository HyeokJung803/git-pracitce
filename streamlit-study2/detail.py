# detail.py
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("data\clothing_data.csv")
    df['주문일자'] = pd.to_datetime(df['주문일자'])
    return df

df = load_data()

# ----------------------------------------------------
# 1. 세션 상태(session_state)로부터 전역 필터 값 안전하게 참조
# ----------------------------------------------------
current_cat = st.session_state.get('selected_category', '전체')
current_brand = st.session_state.get('selected_brand', '전체')

# ----------------------------------------------------
# 2. 데이터 필터링
# ----------------------------------------------------
filtered_df = df.copy()
if current_cat != "전체":
    filtered_df = filtered_df[filtered_df['카테고리'] == current_cat]
if current_brand != "전체":
    filtered_df = filtered_df[filtered_df['브랜드'] == current_brand]

# ----------------------------------------------------
# 3. UI 렌더링 (카테고리/브랜드별 세부 딥다이브)
# ----------------------------------------------------
st.title("🔍 카테고리 및 브랜드 상세 분석")
st.info(f"💡 **분석 타겟 링킹:** 카테고리 **[{current_cat}]** | 브랜드 **[{current_brand}]**")

if filtered_df.empty:
    st.warning("분석할 데이터가 없습니다. 요약 페이지에서 필터를 조절해 주세요.")
else:
    # ----------------------------------------------------
    # 세부 지표 1: 카테고리 내 상품별 성과 분석
    # ----------------------------------------------------
    st.markdown("### 📦 세부 상품별 판매 현황 (TOP 10)")
    
    # 상품명 기준으로 매출 및 수량 집계
    product_stats = filtered_df.groupby('상품명').agg(
        매출액합계=('총판매액', 'sum'),
        판매수량합계=('판매수량', 'sum')
    ).sort_values(by='매출액합계', ascending=False).head(10)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**상품별 총 매출액 (원)**")
        st.bar_chart(product_stats['매출액합계'])
    with col2:
        st.write("**상품별 총 판매수량 (개)**")
        st.bar_chart(product_stats['판매수량합계'])

    st.markdown("---")

    # ----------------------------------------------------
    # 세부 지표 2: 상품 옵션별(색상/사이즈) 쪼개기 분석
    # ----------------------------------------------------
    st.markdown("### 🎨 상품 옵션 선호도 분석")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.write("**브랜드별 점유율 (매출액)**")
        brand_share = filtered_df.groupby('브랜드')['총판매액'].sum().sort_values(ascending=False)
        st.bar_chart(brand_share)
        
    with col4:
        st.write("**인기 색상 순위 (판매량)**")
        color_share = filtered_df.groupby('색상')['판매수량'].sum().sort_values(ascending=False).head(7)
        st.bar_chart(color_share)
        
    with col5:
        st.write("**사이즈 수요 분포 (판매량)**")
        size_share = filtered_df.groupby('사이즈')['판매수량'].sum().sort_values(ascending=False)
        st.bar_chart(size_share)

    st.markdown("---")

    # ----------------------------------------------------
    # 세부 지표 3: 고객 데모그래픽 타겟 분석
    # ----------------------------------------------------
    st.markdown("### 👥 구매 고객층 세부 쪼개기")
    col6, col7 = st.columns(2)
    
    with col6:
        st.write("**성별 판매 비율**")
        gender_data = filtered_df.groupby('성별')['판매수량'].sum()
        st.bar_chart(gender_data)
        
    with col7:
        st.write("**고객 연령대 분포 상세**")
        age_dist = filtered_df['고객연령'].value_counts().sort_index()
        st.bar_chart(age_dist)

    st.markdown("---")

    # ----------------------------------------------------
    # 세부 지표 4: 마이크로 데이터 내역 테이블
    # ----------------------------------------------------
    st.markdown("### 📋 필터링된 데이터 로우 내역")
    st.dataframe(
        filtered_df.sort_values(by='주문일자', ascending=False),
        use_container_width=True
    )