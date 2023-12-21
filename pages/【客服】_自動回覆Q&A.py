import streamlit as st

# 定義預設回覆的關鍵字與答案
default_responses = {
    "你好": "你好！有什麼我可以幫你的嗎？",
    "天氣": "目前天氣晴朗，氣溫攝氏25度。",
    "最新消息": "最新消息：XXX。",
}

# 對話段落顯示區
conversation_history = []

# Streamlit應用主要程式碼
def main():
    st.title("自動回覆機器人")

    # 顯示對話段落
    st.markdown("## 對話段落")
    for item in reversed(conversation_history):
        st.text(item)

    # 輸入框
    user_input = st.text_input("請輸入訊息：")

    if user_input:
        # 將使用者輸入的訊息加入對話歷史
        conversation_history.append(f"你：{user_input}")

        # 檢查預設回覆的關鍵字
        for keyword, response in default_responses.items():
            if keyword in user_input:
                # 加入機器人回覆到對話歷史
                conversation_history.append(f"機器人：{response}")

        # 清空輸入框
        st.text_input("")

# 啟動應用
if __name__ == "__main__":
    main()
