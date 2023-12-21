import streamlit as st

# 定義預設的關鍵字和相應的回答
default_responses = {
    "供檔": "所需內容：",
    "天氣": "目前天氣晴朗。",
    "時間": "現在是下午3點。",
    # 添加更多關鍵字和回答
}

def get_default_response(user_input):
    # 遍歷所有預設關鍵字，如果找到匹配的就返回相應的回答
    for keyword, response in default_responses.items():
        if keyword in user_input:
            return response
    # 如果沒有匹配的關鍵字，返回默認回答
    return "抱歉，我不太明白你說的是什麼。"

# Streamlit 應用程式
def main():
    st.title("簡易自動回覆機器人")

    # 用於記錄對話的列表
    conversation_history = []

    # 獲取使用者輸入
    user_input = st.text_input("輸入你的訊息:")

    if st.button("發送"):
        # 記錄使用者輸入到對話歷史
        conversation_history.append(f"你: {user_input}")

        # 獲取預設回覆
        default_response = get_default_response(user_input)

        # 記錄機器人回覆到對話歷史
        conversation_history.append(f"機器人: {default_response}")

    # 顯示對話歷史
    st.text_area("對話歷史", value="\n".join(conversation_history), height=200)

if __name__ == "__main__":
    main()
