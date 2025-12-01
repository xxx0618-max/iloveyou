import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="체력 데이터 상관관계 분석", layout="wide")

st.title("🏋️‍♂️ 체력 데이터 상관관계 분석 대시보드")

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_excel("fitness data.xlsx")

df = load_data()

st.subheader("📌 데이터 미리보기")
st.dataframe(df.head())

# 숫자형 컬럼만 추출
numeric_df = df.select_dtypes(include=["int64", "float64"])

st.subheader("📊 숫자형 컬럼 상관계수 히트맵")

corr = numeric_df.corr()

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(corr, cmap="coolwarm", annot=False)
st.pyplot(fig)

st.markdown("---")

# --- 상관관계 계산 ---
# 상관계수를 절대값 기준으로 정렬
corr_unstacked = corr.unstack()
corr_unstacked = corr_unstacked[corr_unstacked.index.get_level_values(0) != corr_unstacked.index.get_level_values(1)]

# 양의 상관관계 TOP 1
positive_corr = corr_unstacked.sort_values(ascending=False).head(1)

# 음의 상관관계 TOP 1
negative_corr = corr_unstacked.sort_values(ascending=True).head(1)

st.subheader("📌 가장 높은 양/음의 상관관계 찾기")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔼 양의 상관관계 가장 높은 변수 보기"):
        pair = positive_corr.index[0]
        value = positive_corr.iloc[0]
        st.success(f"**양의 상관관계 1위:** {pair[0]} ↔ {pair[1]} = {value:.4f}")

with col2:
    if st.button("🔽 음의 상관관계 가장 높은 변수 보기"):
        pair = negative_corr.index[0]
        value = negative_corr.iloc[0]
        st.error(f"**음의 상관관계 1위:** {pair[0]} ↔ {pair[1]} = {value:.4f}")

st.markdown("---")

# 상세 비교 그래프
st.subheader("📈 두 변수 간 관계 시각화")

var_x = st.selectbox("X축 변수 선택", numeric_df.columns)
var_y = st.selectbox("Y축 변수 선택", numeric_df.columns)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=numeric_df, x=var_x, y=var_y)
plt.title(f"{var_x} vs {var_y}")
st.pyplot(fig2)
