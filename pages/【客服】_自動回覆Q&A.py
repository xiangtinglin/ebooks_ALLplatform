import streamlit as st

# 定義預設的關鍵字和對應的答案
default_responses = {
    "問候": "你好！歡迎使用自動回覆機器人。",
    "工作": "我是一個自動回覆機器人，可以回答與特定關鍵字相關的問題。",
    "天氣": "很抱歉，我目前無法提供天氣資訊。",
    # 可以繼續添加更多的預設關鍵字和對應的答案
}

def get_default_response(user_input):
    for keyword, response in default_responses.items():
        if keyword in user_input:
            return response
    return "抱歉，我不明白你的問題。"

# Streamlit應用程式的開始
st.title("自動回覆機器人")

# 對話框
user_input = st.text_input("你想問什麼？")

# 顯示使用者輸入的對話
st.write("你說：", user_input)

# 獲取並顯示回覆
bot_response = get_default_response(user_input)
st.write("機器人回答：", bot_response)
