import streamlit as st
import time

# 初始化對話段落
conversation = []

# 輸入框
user_input = st.text_input("輸入框:")

# 推薦相關的預設關鍵字
recommended_keywords = ["你好", "再見", "感謝"]  # 這裡可以替換成實際的相似關鍵字
for keyword in recommended_keywords:
    if keyword in user_input:
        st.write(f"推薦關鍵字：{keyword}")

# 模擬等待0.05秒
time.sleep(0.05)

# 顯示區
st.sidebar.markdown("## 對話段落")
for para in reversed(conversation):
    st.sidebar.text(para)

# 定義預設關鍵字及相應的回覆
default_responses = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "再見": "再見！歡迎隨時回來。",
    "感謝": "不客氣，有其他問題可以問我哦。"
}

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
        conversation.append(f"機器人: {response}")

        # 顯示每個字間隔0.05秒出現，不換行
        for char in f"機器人: {response}":
            st.write(char, end='', key='char')
            time.sleep(0.05)
    st.write("")  # 換行

# 模擬等待0.05秒
time.sleep(0.05)
