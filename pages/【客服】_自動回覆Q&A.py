import streamlit as st
import time

# 定義預設的關鍵字和相對應的答案
default_responses = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "天氣": "請問你想查詢哪個城市的天氣？",
    "感謝": "不客氣，有其他問題歡迎隨時問我！",
}

# 初始化對話歷史
conversation_history = []

# Streamlit UI設計
st.title("簡易自動回覆機器人")

# 顯示對話段落文字
st.markdown("## 對話段落文字")
for paragraph in reversed(conversation_history):
    st.text(paragraph)

# 輸入框
user_input = st.text_input("輸入您的訊息：")

# 根據用戶輸入處理回覆
if user_input:
    conversation_history.append(f"使用者: {user_input}")
    st.text("機器人: ", end="")
    
    # 逐字顯示最新回覆
    for char in default_responses.get(user_input, "抱歉，我不太理解你的問題。"):
        st.text(char)
        time.sleep(0.05)
    
    # 增加機器人回覆到對話歷史
    conversation_history.append(f"機器人: {default_responses.get(user_input, '抱歉，我不太理解你的問題。')}")

# 顯示輸入相關的預設關鍵字
if user_input:
    suggested_keywords = [keyword for keyword in default_responses.keys() if keyword in user_input]
    if suggested_keywords:
        st.text(f"相關關鍵字推薦: {', '.join(suggested_keywords)}")

# 將對話歷史限制在10個段落以內
conversation_history = conversation_history[-10:]
