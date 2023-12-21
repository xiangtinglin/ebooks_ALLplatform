# 匯入所需的套件
import streamlit as st

# 預設的關鍵字與答案對應表
default_responses = {
    "聊天": "您想聊什麼呢？",
    "問候": "哈囉！您好！",
    "機器人": "我是您的助手，有什麼我可以幫您的嗎？",
    "感謝": "不客氣，有其他問題歡迎問我喔！"
}

# Streamlit應用程式的開始
def main():
    st.title("自動回覆機器人")

    # 輸入框
    user_input = st.text_input("chatgpt 聊天對話框")

    # 如果使用者有輸入文字
    if user_input:
        st.text("上一句：{}".format(user_input))

        # 判斷輸入的文字是否包含任何預設的關鍵字
        matched_responses = [response for keyword, response in default_responses.items() if keyword in user_input]

        # 如果有匹配到預設的關鍵字，顯示對應的答案
        if matched_responses:
            st.text("機器人：{}".format(matched_responses[0]))
        else:
            st.text("機器人：抱歉，我不確定如何回覆這個。")

# 執行Streamlit應用程式
if __name__ == "__main__":
    main()
