import re
import streamlit as st

st.set_page_config(page_title="圖書經銷助手", page_icon="📚", layout="centered")

# -------------------------
# 初始化狀態
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "您好，這裡是圖書經銷／上架／權利金／版權助手。\n您可以直接問我：上架進度、權利金、版權授權、下架原因，或輸入書名 / ISBN / 合約編號。"
        }
    ]

if "context" not in st.session_state:
    st.session_state.context = {
        "isbn": None,
        "contract_number": None,
        "book_name": None,
        "topic": None
    }

# -------------------------
# 工具函式
# -------------------------
def extract_isbn(text: str):
    # 抓 10~13 碼，允許有 -，再去掉 -
    candidates = re.findall(r'[\d\-]{10,17}', text)
    for c in candidates:
        pure = c.replace("-", "")
        if pure.isdigit() and len(pure) in [10, 13]:
            return pure
    return None

def extract_contract_number(text: str):
    # 範例：4~10 位英數混合，可依你的實際格式再調整
    match = re.search(r'\b[A-Z0-9]{4,10}\b', text.upper())
    if match:
        return match.group(0)
    return None

def detect_topic(text: str):
    text_lower = text.lower()

    if any(k in text for k in ["上架", "提報", "平台", "通路上架", "可上架", "能上架"]):
        return "上架"
    if any(k in text for k in ["權利金", "版稅", "分潤", "收入", "結算"]):
        return "權利金"
    if any(k in text for k in ["版權", "授權", "合約", "權利", "授權期間"]):
        return "版權"
    if any(k in text for k in ["下架", "無法提報", "不能上架", "提報失敗"]):
        return "下架"
    if any(k in text for k in ["經銷", "銷售", "平台", "通路"]):
        return "經銷"
    return None

def maybe_extract_book_name(text: str):
    # 簡單示意：如果句子有「書名是XXX」
    match = re.search(r'書名[是為:]?\s*(.+)', text)
    if match:
        return match.group(1).strip()
    return None

def update_context(user_input: str):
    isbn = extract_isbn(user_input)
    contract_number = extract_contract_number(user_input)
    topic = detect_topic(user_input)
    book_name = maybe_extract_book_name(user_input)

    # 更新上下文
    if isbn:
        st.session_state.context["isbn"] = isbn
    if contract_number and not isbn:
        # 避免 ISBN 也被當成 contract number
        st.session_state.context["contract_number"] = contract_number
    if book_name:
        st.session_state.context["book_name"] = book_name
    if topic:
        st.session_state.context["topic"] = topic

def generate_reply(user_input: str) -> str:
    ctx = st.session_state.context
    text = user_input.strip()

    # 先更新上下文
    update_context(text)

    isbn = ctx["isbn"]
    contract_number = ctx["contract_number"]
    book_name = ctx["book_name"]
    topic = detect_topic(text) or ctx["topic"]

    # 問候
    if any(k in text.lower() for k in ["你好", "您好", "hi", "hello"]):
        return "您好，我可以協助您查詢圖書上架進度、權利金、版權授權、下架原因，也可以依書名、ISBN 或合約編號接續查詢。"

    # 如果使用者只丟 ISBN
    if extract_isbn(text) and len(text.replace("-", "").strip()) <= 20:
        return f"收到，我已記住您目前查詢的 ISBN 是 {ctx['isbn']}。接下來您可以繼續問我這本書的上架、權利金、版權或下架問題。"

    # 如果問上架
    if topic == "上架":
        if isbn or contract_number or book_name:
            target = book_name or isbn or contract_number
            return (
                f"若是查詢「{target}」的上架狀態，我可以協助確認：\n"
                "1. 是否有電子書授權\n"
                "2. 是否符合平台提報規格\n"
                "3. 是否已提報 / 準備提報 / 已上架\n"
                "4. 是否有重複上架或版權衝突"
            )
        return "可以，請提供書名、ISBN 或合約編號，我才能進一步判斷是否可上架以及目前提報進度。"

    # 如果問權利金
    if topic == "權利金":
        if isbn or contract_number or book_name:
            target = book_name or isbn or contract_number
            return (
                f"若是查詢「{target}」的權利金，我可以接續這本書來看。\n"
                "一般會確認：查詢期間、銷售平台、銷量、應計權利金、已支付 / 未支付狀態。"
            )
        return "可以，請告訴我您要查哪一本書的權利金，提供書名、ISBN 或合約編號都可以。"

    # 如果問版權 / 授權
    if topic == "版權":
        if isbn or contract_number or book_name:
            target = book_name or isbn or contract_number
            return (
                f"若是查詢「{target}」的版權 / 授權狀態，我可以協助確認方向包括：\n"
                "1. 是否仍在授權期間內\n"
                "2. 是否可上架指定平台\n"
                "3. 是否存在版權衝突或重複授權問題"
            )
        return "可以，請提供書名、ISBN 或合約編號，我才能協助確認版權與授權狀態。"

    # 如果問下架
    if topic == "下架":
        if isbn or contract_number or book_name:
            target = book_name or isbn or contract_number
            return (
                f"若是查詢「{target}」被下架或無法提報的原因，常見情況包括：\n"
                "1. 電子書授權已失效\n"
                "2. 不符平台規格\n"
                "3. 重複上架導致版權衝突\n"
                "4. 書目資料異常或待補件"
            )
        return "可以，請提供是哪一本書，我才能接續幫您判斷下架或無法提報的可能原因。"

    # 如果使用者問「那這本呢」「那它呢」這種接續問題
    if any(k in text for k in ["這本", "那本", "它", "這個", "那個"]):
        if isbn or contract_number or book_name:
            target = book_name or isbn or contract_number
            return f"目前我會接續以「{target}」作為查詢對象。您可以直接問我它的上架、權利金、版權或下架問題。"
        return "我可以接續上一個查詢對象，但目前還沒有辨識到書名、ISBN 或合約編號，請先提供其中一項。"

    # fallback
    return (
        "我有點不確定您的問題想查哪一類。\n"
        "您可以這樣問我：\n"
        "• 這本書可以上架嗎？\n"
        "• 幫我查 ISBN 9789571234567 的權利金\n"
        "• 這本書為什麼被下架？\n"
        "• 這本書還有電子書授權嗎？"
    )

# -------------------------
# 畫面
# -------------------------
st.title("📚 圖書經銷／上架／權利金／版權 助手")

with st.expander("目前記住的查詢上下文"):
    st.write(st.session_state.context)

# 顯示聊天紀錄
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 輸入框
if prompt := st.chat_input("請輸入問題，例如：這本書可以上架嗎？"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    reply = generate_reply(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
