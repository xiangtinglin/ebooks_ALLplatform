import streamlit as st

# 預設的關鍵字和相應的回覆
default_responses = {
    "chatgpt": "您好，我是ChatGPT。有什麼我可以幫助您的?",
    "資訊": "您可以在這裡找到有關資訊的相關內容。",
    # 在此添加更多的預設關鍵字和回覆
}

def get_default_response(user_input):
    for keyword, response in default_responses.items():
        if keyword in user_input:
            return response
    return "抱歉，我無法理解您的輸入。"

# Streamlit應用程式的開始
st.title("簡易自動回覆機器人")

# 對話視窗
st.subheader("ChatGPT 聊天對話框")
conversation = st.text_area("對話:", height=200, max_chars=500)

# 使用者輸入
user_input = st.text_input("輸入您的訊息:")

# 處理使用者輸入並回覆
if st.button("發送"):
    if user_input:
        conversation += f"\n你: {user_input}"
        response = get_default_response(user_input)
        conversation += f"\nChatGPT: {response}"

# 顯示對話視窗
st.text_area("對話紀錄:", value=conversation, height=200, max_chars=500, key="output")
