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

st.sidebar.header("🔍 상세 분석 필터")

current_cat = st.session_state.get('selected_category', '전체')
current_brand = st.session_state.get('selected_brand', '전체')

categories = ["전체"] + sorted(df['카테고리'].unique().tolist())
idx_cat = categories.index(current_cat) if current_cat in categories else 0
selected_cat = st.sidebar.selectbox("카테고리 변경", categories, index=idx_cat)
st.session_state.selected_category = selected_cat

brands = ["전체"] + sorted(df['브랜드'].unique().tolist())
idx_brand = brands.index(current_brand) if current_brand in brands else 0
selected_brand = st.sidebar.selectbox("브랜드 변경", brands, index=idx_brand)
st.session_state.selected_brand = selected_brand

filtered_df = df.copy()
if st.session_state.selected_category != "전체":
    filtered_df = filtered_df[filtered_df['카테고리'] == st.session_state.selected_category]
if st.session_state.selected_brand != "전체":
    filtered_df = filtered_df[filtered_df['브랜드'] == st.session_state.selected_brand]

st.title("🔍 카테고리 및 브랜드 상세 분석")
st.info(f"💡 **현재 분석 타겟:** 카테고리 **[{st.session_state.selected_category}]** | 브랜드 **[{st.session_state.selected_brand}]**")

st.markdown("### 📋 데이터 로우 내역 조회")

keyword = st.text_input("키워드 검색 (입력 후 엔터 시 테이블에 즉시 반영)", key="search_input_field")

display_df = filtered_df.copy()

if keyword:
    k = keyword.strip().lower()
    search_targets = ['주문번호', '카테고리', '상품명', '브랜드', '색상', '사이즈']
    available_targets = [col for col in search_targets if col in display_df.columns]
    
    if available_targets:
        mask = display_df[available_targets].fillna('').astype(str).apply(lambda x: x.str.lower().str.contains(k)).any(axis=1)
        display_df = display_df[mask]

if display_df.empty:
    st.warning("선택하신 필터 및 검색 조건에 일치하는 데이터가 없습니다. 다시 입력해 주세요.")
else:
    if keyword:
        st.caption(f"🎯 키워드 **'{keyword}'** 필터링 적용 중 ({len(display_df):,}행 찾음)")

    st.dataframe(
        display_df.sort_values(by='주문일자', ascending=False),
        use_container_width=True
    )

    st.markdown("---")

    st.markdown("### 📦 세부 상품별 판매 현황 (TOP 10)")
    product_stats = display_df.groupby('상품명').agg(
        매출액합계=('총판매액', 'sum'),
        판매수량합계=('판매수량', 'sum')
    ).sort_values(by='매출액합계', ascending=False).head(10)
    
    # 그래프 시인성을 위해 금액 단위를 백만 단위(M) 혹은 억 단위로 나누어 가공
    product_stats['매출액(억 원)'] = product_stats['매출액합계'] / 100000000
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**상품별 총 매출액 (단위: 억 원)**")
        st.bar_chart(product_stats['매출액(억 원)'])
    with col2:
        st.write("**상품별 총 판매수량 (개)**")
        st.bar_chart(product_stats['판매수량합계'])

    st.markdown("---")

    st.markdown("### 🎨 상품 옵션 선호도 분석")
    
    # 브랜드 점유율 금액도 억 단위 변환
    brand_share = (display_df.groupby('브랜드')['총판매액'].sum() / 100000000).sort_values(ascending=False)
    color_share = display_df.groupby('색상')['판매수량'].sum().sort_values(ascending=False).head(7)
    size_share = display_df.groupby('사이즈')['판매수량'].sum().sort_values(ascending=False)
    
    col3, col4, col5 = st.columns(3)
    with col3:
        st.write("**브랜드별 점유율 (단위: 억 원)**")
        st.bar_chart(brand_share)
    with col4:
        st.write("**인기 색상 순위 (판매량)**")
        st.bar_chart(color_share)
    with col5:
        st.write("**사이즈 수요 분포 (판매량)**")
        st.bar_chart(size_share)

    st.markdown("---")

    st.markdown("### 👥 구매 고객층 세부 쪼개기")
    col6, col7 = st.columns(2)
    with col6:
        st.write("**성별 판매 비율**")
        gender_data = display_df.groupby('성별')['판매수량'].sum()
        st.bar_chart(gender_data)
    with col7:
        st.write("**고객 연령대 분포 상세**")
        age_dist = display_df['고객연령'].value_counts().sort_index()
        st.bar_chart(age_dist)