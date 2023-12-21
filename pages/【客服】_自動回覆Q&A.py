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

# 主程式
st.title("自動回覆機器人")

# 【輸入框】
user_input = st.text_input("輸入框:")
input_paragraph = f"使用者: {user_input}"

# 推薦相似的預設關鍵字
recommended_keywords = [key for key in default_responses.keys() if key in user_input]
if recommended_keywords:
    st.write(f"推薦關鍵字：{', '.join(recommended_keywords)}")

# 【顯示區】
st.sidebar.markdown("## 對話段落")
for para in reversed(conversation):
    st.sidebar.text(para)

# 判斷是否有預設回覆
response = None
for key in default_responses:
    if key in user_input:
        response = default_responses[key]
        break

# 更新對話段落
if user_input:
    conversation.append(input_paragraph)
    if response:
        response_paragraph = f"機器人: {response}"
        conversation.append(response_paragraph)

        # 模擬等待0.05秒，逐字顯示
        for char in response_paragraph:
            st.text(char)
            time.sleep(0.05)

# 清空輸入框
st.text_input("", key="dummy_key", value="")

# 模擬等待0.05秒
time.sleep(0.05)
