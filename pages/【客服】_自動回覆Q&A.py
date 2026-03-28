import streamlit as st

st.set_page_config(page_title="圖書經銷客服機器人", page_icon="📚")

# -------------------------------
# 1. 初始化 session state
# -------------------------------
if "dialogue" not in st.session_state:
    st.session_state.dialogue = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""


# -------------------------------
# 2. 回覆規則函式
# -------------------------------
def get_bot_reply(user_input: str) -> str:
    text = user_input.strip().lower()

    # 上架相關
    if any(keyword in text for keyword in ["上架", "平台上架", "通路上架", "書上架"]):
        return (
            "機器人：若您想確認書籍是否可上架，請先提供書名、ISBN 或合約編號。"
            "我們會協助確認該書是否已有授權、是否符合平台格式規範，以及目前上架進度。"
        )

    # 權利金相關
    elif any(keyword in text for keyword in ["權利金", "版稅", "分潤", "收入"]):
        return (
            "機器人：若您要查詢權利金，請提供書名、ISBN、合約編號，或指定查詢年度 / 月份。"
            "一般可協助確認：銷售期間、平台銷量、應計權利金、已支付 / 未支付狀態。"
        )

    # 版權 / 授權相關
    elif any(keyword in text for keyword in ["版權", "授權", "合約", "權利", "是否有授權"]):
        return (
            "機器人：版權 / 授權查詢通常需確認合約狀態。"
            "若您提供合約編號、書名或 ISBN，我們可協助初步判斷："
            "是否仍在授權期間內、是否可上架電子書平台、是否有版權衝突。"
        )

    # ISBN / 書名查詢
    elif any(keyword in text for keyword in ["isbn", "書名", "合約編號", "編號"]):
        return (
            "機器人：您可以直接輸入 ISBN、完整或部分書名、合約編號進行查詢。"
            "系統會依據資料比對對應書籍的上架、版權與權利金資訊。"
        )

    # 下架 / 無法提報
    elif any(keyword in text for keyword in ["下架", "無法提報", "不能上架", "提報失敗"]):
        return (
            "機器人：若書籍顯示無法提報或需下架，常見原因包括："
            "1. 電子書授權已失效；"
            "2. 不符平台格式規範；"
            "3. 與其他版本重複上架造成版權衝突；"
            "4. 書目資料異常或待補件。"
        )

    # 銷售 / 經銷
    elif any(keyword in text for keyword in ["經銷", "銷售", "通路", "平台"]):
        return (
            "機器人：若您想了解圖書經銷狀況，可提供書名或平台名稱。"
            "常見查詢包含：已上架平台、各平台銷售表現、提報狀態與後續經銷安排。"
        )

    # 問候
    elif any(keyword in text for keyword in ["你好", "您好", "hi", "hello"]):
        return (
            "機器人：您好，這裡是圖書經銷與版權查詢助手。"
            "您可以詢問上架進度、權利金、版權授權、下架原因，或直接輸入書名 / ISBN / 合約編號。"
        )

    # fallback
    else:
        return (
            "機器人：抱歉，我目前無法直接判斷您的問題。"
            "您可以改用以下方式提問：\n"
            "1. 查某本書是否已上架\n"
            "2. 查某本書的權利金 / 版稅\n"
            "3. 查授權或版權狀態\n"
            "4. 查下架或無法提報原因\n"
            "5. 直接輸入書名、ISBN 或合約編號"
        )


# -------------------------------
# 3. 處理送出
# -------------------------------
def submit_message():
    user_input = st.session_state.user_input.strip()
    if not user_input:
        return

    st.session_state.dialogue.append(f"使用者：{user_input}")
    bot_reply = get_bot_reply(user_input)
    st.session_state.dialogue.append(bot_reply)

    # 清空輸入框
    st.session_state.user_input = ""


# -------------------------------
# 4. UI
# -------------------------------
st.title("📚 圖書經銷／上架／權利金／版權 助手")

st.write("可詢問：上架進度、權利金、版權授權、下架原因，或直接輸入書名 / ISBN / 合約編號。")

# 顯示對話紀錄
for paragraph in st.session_state.dialogue:
    st.write(paragraph)

# 輸入區
st.text_input("請輸入訊息：", key="user_input", on_change=submit_message)

# 範例問題
with st.expander("💡 可參考的提問方式"):
    st.write("• 這本書可以上架嗎？")
    st.write("• 我要查某本書的權利金")
    st.write("• 這本書為什麼被下架？")
    st.write("• 幫我確認這本書是否還有電子書授權")
    st.write("• ISBN 978XXXXXXXXX")
