import streamlit as st

# 儲存聊天紀錄的全域變數
chat_history = []

# 預設的關鍵字和回答
default_responses = {
    "你好": "哈囉！有什麼我可以幫助你的嗎？",
    "天氣": "請問你想查詢哪個城市的天氣？",
    # 在這裡添加更多的預設關鍵字和回答
}

# Streamlit App
st.title("自動回覆機器人")

# 第一區-輸入框
user_input = st.text_input("請輸入你的問題：")
selected_keyword = st.selectbox("選擇相關的預設關鍵字：", list(default_responses.keys()))

# 如果使用者輸入了問題
if user_input:
    # 將使用者的問題和回答加入聊天紀錄
    chat_history.append({"user": user_input, "bot": default_responses.get(selected_keyword, "抱歉，我不太理解你的問題。")})

# 第二區-顯示框
st.subheader("聊天紀錄")

# 顯示過去的提問和回答
for chat in chat_history:
    st.text(f"你: {chat['user']}")
    st.text(f"機器人: {chat['bot']}")
    st.text("------")

# 顯示最新的回答
if user_input:
    st.text(f"你: {user_input}")
    st.text(f"機器人: {default_responses.get(selected_keyword, '抱歉，我不太理解你的問題。')}")
    st.text("------")
