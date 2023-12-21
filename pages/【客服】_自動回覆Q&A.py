import streamlit as st
import time

# 初始化問答紀錄
qa_history = []

# 預設關鍵字及相對應的回答
default_responses = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "再見": "再見，歡迎隨時回來！",
    "感謝": "不客氣，有其他問題歡迎問我。",
}

# Streamlit UI
st.title("自動回覆機器人")

# 第一區-顯示區
st.subheader("提問&回覆紀錄")
for entry in reversed(qa_history):
    st.text(entry)
    time.sleep(0.05 * len(entry))  # 每個字間隔0.05秒出現

# 第二區-輸入框
user_input = st.text_input("輸入你的問題：")

# 檢查預設關鍵字
for keyword, response in default_responses.items():
    if keyword in user_input:
        st.text(f"機器人: {response}")
        qa_history.append(f"使用者: {user_input}")
        qa_history.append(f"機器人: {response}")
        break
