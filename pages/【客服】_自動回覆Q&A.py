import streamlit as st
import time

# 初始化對話列表
conversation = []

# 預設回覆字典
default_responses = {
    "你好": "你好！有什麼我可以幫助你的嗎？",
    "再見": "再見，歡迎下次再來！",
    "感謝": "不客氣，有其他問題歡迎問我喔！"
}

# 預設的關鍵字
default_keywords = list(default_responses.keys())

# Streamlit 介面配置
st.title("自動回覆機器人")

# 第一區 - 顯示框
st.text_area("對話區域", value="\n".join(conversation), height=300, max_chars=None, key="conversation")

# 第二區 - 輸入框
user_input = st.text_input("請輸入您的問題：")

# 推薦相關關鍵字
recommended_keywords = [keyword for keyword in default_keywords if keyword in user_input]
if recommended_keywords:
    st.text("推薦關鍵字：" + ", ".join(recommended_keywords))

# 模擬自動回覆
for char in "正在思考中...":
    st.text(char)
    time.sleep(0.05)

# 根據關鍵字給予預設答案
for keyword, response in default_responses.items():
    if keyword in user_input:
        reply = response
        break
else:
    reply = "抱歉，我不太理解您的問題。"

# 更新對話列表
conversation.append(f"使用者：{user_input}")
conversation.append(f"機器人：{reply}")

# 顯示回覆
st.text(reply)

# 更新對話區域
st.text_area("對話區域", value="\n".join(conversation), height=300, max_chars=None, key="conversation")
