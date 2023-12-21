# 安裝 streamlit：pip install streamlit

import streamlit as st
import time

# 預設的關鍵字和回答
default_responses = {
    "你好": "你好！有什麼我可以幫忙的嗎？",
    "再見": "再見，歡迎下次再來！",
    "感謝": "不客氣，有其他問題就問吧！",
}

# 初始化對話歷史
conversation_history = []

# Streamlit 介面
st.title("簡易自動回覆機器人")

# 第一區 - 顯示框
st.subheader("對話歷史")
for entry in conversation_history:
    st.text(entry)

# 第二區 - 輸入框
st.subheader("輸入框")

# 讓使用者輸入關鍵字
user_input = st.text_input("請輸入您的問題：")

# 根據關鍵字給予預設答案
for keyword, response in default_responses.items():
    if keyword in user_input:
        # 顯示推薦關鍵字
        st.text(f"建議關鍵字：{', '.join(default_responses.keys())}")

        # 模擬回覆的打字效果
        st.text("機器人正在思考中...")
        with st.spinner("輸入中..."):
            time.sleep(1)
        
        # 將對話加入歷史
        conversation_history.append(f"使用者：{user_input}")
        conversation_history.append(f"機器人：{response}")

        # 顯示回覆
        for char in response:
            st.text(f"機器人：{char}")
            time.sleep(0.05)

        # 將回覆加入歷史
        conversation_history.append(f"機器人：{response}")

# 更新對話歷史
st.text("更新對話歷史...")
time.sleep(1)
st.text("對話歷史已更新！")
