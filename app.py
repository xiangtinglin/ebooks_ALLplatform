
import streamlit as st

st.set_page_config(page_title="書單分析系統", layout="wide")

st.title("📊 書單分析平台")

st.write("請從左側選擇功能頁面")

# 直接跳轉
if "redirected" not in st.session_state:
    st.session_state.redirected = True
    st.switch_page("pages/【權利金】歷年總表紀錄_分析圖表.py")
