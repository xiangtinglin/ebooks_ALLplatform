import streamlit as st

# 初始化對話列表
conversation = []

# 初始化預設的關鍵字和回覆
default_responses = {
    "你好": "你好！有什麼我可以幫忙的嗎？",
    "天氣": "請問你想查詢哪個城市的天氣？",
    "感謝": "不客氣，有其他問題歡迎隨時問我！"
}

# Streamlit 界面
st.title("簡易自動回覆機器人")

# 第一區-對話段落文字顯示區
st.sidebar.title("對話段落")
for c in conversation:
    st.sidebar.text(c)

# 第二區-輸入框
user_input = st.text_input("輸入框")

# 如果使用者輸入非空字串
if user_input:
    # 將使用者輸入添加到對話列表
    conversation.append(f"使用者: {user_input}")

    # 檢查預設的關鍵字
    for keyword, response in default_responses.items():
        if keyword in user_input:
            # 將回覆添加到對話列表
            conversation.append(f"機器人: {response}")

    # 清空輸入框
    st.text_input("")

# 顯示對話段落文字
st.sidebar.title("對話段落")
for c in reversed(conversation):
    st.sidebar.text(c)
