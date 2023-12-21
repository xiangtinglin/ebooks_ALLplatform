import streamlit as st
import time

# 設定預設回覆的關鍵字與答案
default_responses = {
    "你好": "你好！有什麼我可以幫忙的嗎？",
    "再見": "再見，歡迎隨時回來！",
    "感謝": "不客氣，有其他問題歡迎問我。",
}

# 初始化對話紀錄
conversation_history = []

# Streamlit UI
st.title("簡易自動回覆機器人")

# 第一區 - 顯示框
st.markdown("### 第一區 - 顯示框")

for interaction in conversation_history:
    st.text(f"{interaction['user']}: {interaction['question']}")
    st.text(f"機器人: {interaction['response']}")
    st.markdown("---")

# 第二區 - 輸入框
st.markdown("### 第二區 - 輸入框")

# 讓使用者輸入關鍵字
user_input = st.text_input("輸入您的問題：")

# 檢查預設回覆的關鍵字
for keyword, response in default_responses.items():
    if keyword in user_input:
        st.text("機器人正在思考中...")
        time.sleep(1)  # 模擬思考時間

        # 逐字打印回覆
        for char in response:
            st.text("機器人: " + char)
            time.sleep(0.05)

        # 將對話紀錄添加到歷史
        conversation_history.append({"user": "使用者", "question": user_input, "response": response})
        break

# 如果使用者沒有輸入，則顯示提示訊息
if not user_input:
    st.text("請輸入問題。")

# 顯示最新的對話紀錄
st.markdown("### 最新對話紀錄")
if conversation_history:
    latest_interaction = conversation_history[-1]
    st.text(f"{latest_interaction['user']}: {latest_interaction['question']}")
    st.text(f"機器人: {latest_interaction['response']}")
else:
    st.text("尚無對話紀錄。")
