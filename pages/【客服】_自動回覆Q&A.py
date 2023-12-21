import streamlit as st
import time

# 儲存對話歷史的列表
conversation_history = []

# 預設的回覆字典，關鍵字對應回覆
default_responses = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "再見": "再見，歡迎下次再來！",
    "感謝": "不客氣，有其他問題也可以問我哦！",
}

# Streamlit 界面配置
st.title("自動回覆機器人")

# 第一區 - 顯示框
st.markdown("### 對話歷史")
for entry in conversation_history:
    st.text(entry)

# 第二區 - 輸入框
user_input = st.text_input("輸入你的訊息：")

# 判斷是否有相對應的預設回覆
matched_response = None
for keyword, response in default_responses.items():
    if keyword in user_input:
        matched_response = response
        break

# 如果有預設回覆，顯示回覆
if matched_response:
    st.text("機器人回覆：")
    for char in matched_response:
        st.text(char)
        time.sleep(0.05)

    # 將對話加入歷史紀錄
    conversation_history.append(f"使用者：{user_input}")
    conversation_history.append(f"機器人：{matched_response}")

# 如果沒有預設回覆，不顯示回覆
elif user_input:
    # 將對話加入歷史紀錄
    conversation_history.append(f"使用者：{user_input}")

# 顯示清空按鈕
if st.button("清空對話歷史"):
    conversation_history = []

# 更新 Streamlit 介面
st.text("")
