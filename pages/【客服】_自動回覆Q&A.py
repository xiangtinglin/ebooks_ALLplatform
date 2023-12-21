# 定義預設的關鍵字和對應的答案
default_responses = {
    "問候": "你好！有什麼我可以幫助你的嗎？",
    "天氣": "目前天氣晴，溫度22度。",
    # 添加更多的預設關鍵字和答案
}

def get_default_response(user_input):
    for keyword, response in default_responses.items():
        if keyword in user_input:
            return response
    return "抱歉，我不太明白你的問題。"

def main():
    st.title("簡易自動回覆機器人")

    user_input = st.text_input("輸入你的問題：")

    if user_input:
        default_response = get_default_response(user_input)
        st.text("機器人回覆：{}".format(default_response))

if __name__ == "__main__":
    main()
