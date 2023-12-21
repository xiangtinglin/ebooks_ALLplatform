import streamlit as st
import time

# 初始化對話段落
conversation = []

# 定義預設關鍵字及相應的回覆
default_responses = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "再見": "再見！歡迎隨時回來。",
    "感謝": "不客氣，有其他問題可以問我哦。"
}

# 輸入框
user_input = st.text_input("輸入框:")

# 推薦相關的預設關鍵字
recommended_keywords = [key for key in default_responses.keys() if key in user_input]
if recommended_keywords:
    st.write(f"推薦關鍵字：{', '.join(recommended_keywords)}")

# 判斷是否有預設回覆
response = None
for key in default_responses:
    if key in user_input:
        response = default_responses[key]
        break

# 更新對話段落
if user_input:
    conversation.append(f"使用者: {user_input}")
    if response:
        st.write(f"機器人: ", end="")
        for char in response:
            st.write(char, end="", key=None)
            time.sleep(0.05)
        st.write("")  # 換行

# 顯示區
st.sidebar.markdown("## 對話段落")
for para in reversed(conversation):
    st.sidebar.text(para)
