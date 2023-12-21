import streamlit as st

# 預設關鍵字&回覆。
default_responses = {
    "你好": "你好！有什么我可以帮助你的吗？",
    "天气": "目前天气晴朗。",
    "时间": "现在是下午3点。",
    # 添加更多关键字和回答
}

def get_default_response(user_input):
    # 遍历所有预设关键字，如果找到匹配的就返回相应的回答
    for keyword, response in default_responses.items():
        if keyword in user_input:
            return response
    # 如果没有匹配的关键字，返回默认回答
    return "抱歉，我不太明白你说的是什么。"

# Streamlit 应用程序
def main():
    st.title("简易自动回复机器人")

    # 用于记录对话的列表
    conversation_history = []

    # 获取用户输入
    user_input = st.text_input("输入你的消息:")

    if st.button("发送"):
        # 记录用户输入到对话历史
        conversation_history.append(f"你: {user_input}")

        # 获取默认回复
        default_response = get_default_response(user_input)

        # 记录机器人回复到对话历史
        conversation_history.append(f"机器人: {default_response}")

    # 显示对话历史
    st.text_area("对话历史", value="\n".join(conversation_history), height=200)

if __name__ == "__main__":
    main()
