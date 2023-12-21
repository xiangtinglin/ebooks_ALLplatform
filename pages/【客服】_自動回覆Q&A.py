import streamlit as st

# 定義預設的關鍵字和對應的回答
default_responses = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "天氣": "天氣晴朗，適合出門活動。",
    "新聞": "最新的新聞是......",
    # 添加更多的預設關鍵字和回答
}

# 初始化對話紀錄
conversation_history = []

# Streamlit應用程式的標題
st.title("簡易自動回覆機器人")

# 第一區-輸入框
user_input = st.text_input("請輸入你的問題或關鍵字：")

# 檢查是否有預設的關鍵字
matched_keyword = None
for keyword in default_responses.keys():
    if keyword in user_input:
        matched_keyword = keyword
        break

# 推薦相關的預設關鍵字
if matched_keyword:
    st.markdown(f"建議的關鍵字：{', '.join(default_responses.keys())}")

# 根據不同關鍵字給予預設的答案
if matched_keyword:
    response = default_responses[matched_keyword]
    conversation_history.append({"user": user_input, "bot": response})
else:
    response = "我還不太懂你的問題，請再詳細說明一下。"
    conversation_history.append({"user": user_input, "bot": response})

# 第二區-顯示框
st.subheader("對話紀錄")
for entry in conversation_history:
    st.text(f"你: {entry['user']}")
    st.text(f"機器人: {entry['bot']}")

# 顯示最新的回答
st.subheader("機器人的回答")
st.text(response)
