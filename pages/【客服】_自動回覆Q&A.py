# 引入相關套件
import streamlit as st

# 初始化對話列表
dialogue = []

# Streamlit UI 布局
st.title("自動回覆機器人")

# 顯示對話段落
for paragraph in reversed(dialogue):
    st.text(paragraph)

# Streamlit UI 布局
user_input = st.text_input("請輸入關鍵字：")

# 如果使用者有輸入文字
if user_input:
    # 推薦相關關鍵字
    st.text("推薦關鍵字：預設1, 預設2, 預設3")

    # 將使用者輸入的文字加入對話列表
    dialogue.append(f"使用者：{user_input}")

    # 根據不同的關鍵字給予預設答案
    if "預設1" in user_input:
        st.text("機器人：這是預設1的回覆。")
    elif "預設2" in user_input:
        st.text("機器人：這是預設2的回覆。")
    elif "預設3" in user_input:
        st.text("機器人：這是預設3的回覆。")
    else:
        st.text("機器人：抱歉，我不太了解您的問題。")

    # 清空輸入框
    st.text_input("")
