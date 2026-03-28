import re
from typing import Dict, List, Optional, Tuple

import streamlit as st

# =========================================================
# Page config
# =========================================================
st.set_page_config(
    page_title="圖書經銷客服助手",
    page_icon="📚",
    layout="wide",
)

# =========================================================
# 可調整的 FAQ / 制度文字
# 這裡先用「安全版」說法，避免沒有真實制度時答太死
# 你之後可以直接把內容改成你們公司的正式版本
# =========================================================
FAQ_ZH = {
    "cooperation": (
        "您好，若您希望與我們合作圖書經銷或電子書上架，歡迎先提供您的身份別"
        "（作者／出版社／版權代理／內容提供方）以及基本書目資訊。\n\n"
        "一般合作流程包含：合作洽談、授權確認、書目與檔案格式檢查、平台提報與後續銷售管理。\n\n"
        "若您願意，也可直接提供書名、ISBN、授權狀態與聯絡方式，以便後續評估合作方式。"
    ),
    "royalty": (
        "您好，權利金的結算時間與抽成比例通常會依合作合約、平台規則與合作模式而有所不同。\n\n"
        "常見情況下，會依月結、季結、半年結或其他約定週期進行結算；抽成比例也可能因平台、產品型態與授權條件不同而有所差異。\n\n"
        "若您已有合作合約，建議以合約條款為準；若您正在洽談合作，歡迎提供合作類型與書籍資訊，我們可協助說明一般流程與確認方向。"
    ),
    "materials": (
        "為了協助評估合作或查詢書籍狀態，建議提供以下資訊：\n"
        "1. 書名\n"
        "2. ISBN\n"
        "3. 作者 / 出版社名稱\n"
        "4. 合約編號（若有）\n"
        "5. 授權狀態\n"
        "6. 欲上架平台\n"
        "7. 聯絡方式\n\n"
        "資料越完整，越有助於加快確認流程。"
    ),
    "listing_time": (
        "上架所需時間通常取決於：\n"
        "1. 授權確認是否完成\n"
        "2. 書目資料是否完整\n"
        "3. 檔案格式是否符合平台規範\n"
        "4. 各平台的審核流程\n\n"
        "若資料齊備且無異常，流程通常會較快；若有版權、格式或資料缺漏，則可能延長處理時間。"
    ),
    "cannot_list": (
        "常見無法提報或無法上架的原因包括：\n"
        "1. 電子書授權已失效\n"
        "2. 不符平台格式規範\n"
        "3. 書目資料待補件\n"
        "4. 與既有版本重複上架而產生版權衝突\n\n"
        "若您提供書名、ISBN 或合約編號，我可以進一步協助整理查詢方向。"
    ),
    "contact": (
        "若您希望進一步洽談合作，建議先提供您的身份（作者 / 出版社 / 版權代理）"
        "與書籍基本資訊。我也可以先幫您整理需要準備的資料清單。"
    ),
}

FAQ_EN = {
    "cooperation": (
        "Hello. If you are interested in working with us on book distribution or e-book listing, "
        "please provide your role first, such as author, publisher, rights agent, or content provider, "
        "along with the basic title information.\n\n"
        "The usual process includes initial discussion, rights confirmation, metadata and file review, "
        "platform submission, and follow-up sales management."
    ),
    "royalty": (
        "Hello. The royalty settlement period and revenue-sharing ratio usually depend on the cooperation "
        "agreement, platform rules, and business model.\n\n"
        "In practice, settlements may be arranged monthly, quarterly, semi-annually, or according to other "
        "agreed terms. The revenue-sharing ratio may also vary depending on the platform, product type, "
        "and licensing conditions.\n\n"
        "If you already have a contract, please refer to the contract terms."
    ),
    "materials": (
        "To evaluate cooperation or check a title status, it is helpful to provide:\n"
        "1. Title name\n"
        "2. ISBN\n"
        "3. Author / publisher name\n"
        "4. Contract number (if any)\n"
        "5. License status\n"
        "6. Target platforms\n"
        "7. Contact information"
    ),
    "listing_time": (
        "The listing timeline usually depends on rights confirmation, metadata completeness, "
        "file-format compliance, and each platform's review process."
    ),
    "cannot_list": (
        "Common reasons a title cannot be submitted or listed include expired e-book rights, "
        "platform format issues, incomplete metadata, or copyright conflicts caused by duplicate listings."
    ),
    "contact": (
        "If you would like to discuss cooperation further, please provide your role "
        "(author / publisher / rights agent) and the basic title information first."
    ),
}

QUESTION_TEMPLATES_ZH = [
    "我是出版社，想合作上架電子書，流程是什麼？",
    "我是作者，可以直接跟你們合作嗎？",
    "請問銷售後多久會結算權利金？",
    "權利金抽成比例怎麼算？",
    "這本書為什麼無法提報？",
    "請幫我查 ISBN 9789571234567 的上架方向",
    "請問電子書授權是否仍有效？",
]

QUESTION_TEMPLATES_EN = [
    "I am a publisher. How can I work with you?",
    "I am an author. Can I cooperate with your company directly?",
    "When are royalties settled after sales?",
    "What is the revenue-sharing ratio?",
    "Why can't this title be listed?",
    "Please check the listing direction for ISBN 9789571234567.",
    "Is the e-book license still valid?",
]

# =========================================================
# 初始化 session state
# Session State 會在同一個使用者 session 的 rerun 之間保留資料
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "您好，我是圖書經銷／上架／權利金／版權助手 📚\n\n"
                "您可以直接問我：\n"
                "- 如何合作\n"
                "- 上架流程\n"
                "- 權利金 / 抽成 / 結算\n"
                "- 授權 / 版權\n"
                "- 無法提報 / 下架原因\n\n"
                "也可以直接輸入書名、ISBN 或合約編號，我會盡量接續前文理解。"
            ),
        }
    ]

if "context" not in st.session_state:
    st.session_state.context = {
        "language": "zh",              # zh / en
        "isbn": None,
        "contract_number": None,
        "book_name": None,
        "publisher": None,
        "role_hint": None,             # 作者 / 出版社 / rights agent / ...
        "topic": None,                 # cooperation / royalty / listing / copyright / cannot_list / ...
    }

# =========================================================
# 工具函式
# =========================================================
def detect_language(text: str) -> str:
    """很簡單的語言偵測：若英文字母比例高，視為英文；否則視為中文。"""
    if not text:
        return "zh"

    english_words = re.findall(r"[A-Za-z]+", text)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)

    if len(" ".join(english_words)) > max(3, len(chinese_chars) * 1.2):
        return "en"
    return "zh"


def extract_isbn(text: str) -> Optional[str]:
    """
    抓 10 或 13 碼 ISBN，允許有破折號。
    """
    candidates = re.findall(r"[\d\-]{10,17}", text)
    for item in candidates:
        pure = item.replace("-", "")
        if pure.isdigit() and len(pure) in (10, 13):
            return pure
    return None


def extract_contract_number(text: str) -> Optional[str]:
    """
    非常保守的合約編號抓法。
    你若有固定格式，可改成更準確的 regex。
    """
    text_up = text.upper()

    # 若明確寫出「合約編號」
    m = re.search(r"(合約編號|contract\s*number|contract)\s*[:：]?\s*([A-Z0-9\-_]{4,20})", text_up)
    if m:
        return m.group(2)

    # 一般英數混合編號
    candidates = re.findall(r"\b[A-Z][A-Z0-9\-_]{3,19}\b", text_up)
    if candidates:
        return candidates[0]
    return None


def extract_role_hint(text: str, lang: str) -> Optional[str]:
    text_lower = text.lower()
    if lang == "zh":
        if "作者" in text:
            return "作者"
        if "出版社" in text:
            return "出版社"
        if "版權代理" in text:
            return "版權代理"
        if "總經銷" in text or "經銷" in text:
            return "經銷夥伴"
    else:
        if "author" in text_lower:
            return "author"
        if "publisher" in text_lower:
            return "publisher"
        if "rights agent" in text_lower or "agent" in text_lower:
            return "rights agent"
        if "distributor" in text_lower or "distribution partner" in text_lower:
            return "distribution partner"
    return None


def extract_book_name(text: str, lang: str) -> Optional[str]:
    """
    簡單抓法：
    中文：書名是XXX / 書名：XXX
    英文：title is XXX / title: XXX
    """
    if lang == "zh":
        m = re.search(r"書名\s*[是為:：]?\s*(.+)", text)
    else:
        m = re.search(r"title\s*(is|:)?\s*(.+)", text, re.IGNORECASE)

    if not m:
        return None

    val = m.groups()[-1].strip()
    if len(val) > 1:
        return val
    return None


def detect_topic(text: str, lang: str) -> Optional[str]:
    t = text.lower()

    # 雙語 topic 偵測
    topic_keywords = {
        "cooperation": [
            "合作", "配合", "如何合作", "怎麼合作", "洽談",
            "cooperate", "cooperation", "work with you", "partnership"
        ],
        "royalty": [
            "權利金", "版稅", "分潤", "抽成", "收入", "結算",
            "royalty", "royalties", "revenue share", "revenue-sharing", "settlement", "settle"
        ],
        "listing": [
            "上架", "提報", "平台上架", "通路上架", "可上架", "能上架", "上平台",
            "list", "listing", "submit", "submission", "platform listing", "publish on platform"
        ],
        "copyright": [
            "版權", "授權", "合約", "權利", "授權期間", "電子書授權",
            "copyright", "license", "licence", "rights", "contract", "licensing"
        ],
        "cannot_list": [
            "下架", "無法提報", "不能上架", "提報失敗", "為什麼不能", "為何不能",
            "removed", "take down", "cannot list", "can't list", "failed submission", "rejected"
        ],
        "materials": [
            "要準備什麼", "需要什麼資料", "提供什麼資料", "要附什麼",
            "what information", "what materials", "what should i provide", "what documents"
        ],
        "contact": [
            "聯絡", "窗口", "怎麼聯繫", "如何聯絡",
            "contact", "reach you", "how to contact"
        ],
        "listing_time": [
            "多久上架", "上架多久", "需要多久", "時程", "多久會上",
            "how long", "timeline", "how much time", "listing time"
        ],
    }

    for topic, keywords in topic_keywords.items():
        if any(k in t or k in text for k in keywords):
            return topic
    return None


def contains_followup_reference(text: str, lang: str) -> bool:
    if lang == "zh":
        words = ["這本", "那本", "它", "這個", "那個", "剛剛那本", "前面那本"]
    else:
        words = ["it", "this title", "that title", "this book", "that book", "the previous one"]
    low = text.lower()
    return any(w in text or w in low for w in words)


def update_context(user_input: str) -> None:
    lang = detect_language(user_input)
    st.session_state.context["language"] = lang

    isbn = extract_isbn(user_input)
    if isbn:
        st.session_state.context["isbn"] = isbn

    contract_number = extract_contract_number(user_input)
    # 避免 ISBN 被同時判成 contract number
    if contract_number and contract_number != isbn:
        st.session_state.context["contract_number"] = contract_number

    role_hint = extract_role_hint(user_input, lang)
    if role_hint:
        st.session_state.context["role_hint"] = role_hint

    book_name = extract_book_name(user_input, lang)
    if book_name:
        st.session_state.context["book_name"] = book_name

    topic = detect_topic(user_input, lang)
    if topic:
        st.session_state.context["topic"] = topic


def format_target(ctx: Dict) -> str:
    return ctx.get("book_name") or ctx.get("isbn") or ctx.get("contract_number") or "目前這本書"


def reply_cooperation(ctx: Dict, lang: str) -> str:
    role_hint = ctx.get("role_hint")
    if lang == "en":
        base = FAQ_EN["cooperation"]
        if role_hint:
            return f"I understand that you are likely a {role_hint}.\n\n{base}"
        return base

    base = FAQ_ZH["cooperation"]
    if role_hint:
        return f"我理解您目前的身份可能是「{role_hint}」。\n\n{base}"
    return base


def reply_royalty(ctx: Dict, lang: str) -> str:
    target = format_target(ctx)
    if lang == "en":
        if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
            return (
                f"If you are asking about royalties for \"{target}\", I can continue with that title.\n\n"
                f"{FAQ_EN['royalty']}"
            )
        return FAQ_EN["royalty"]

    if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
        return (
            f"若您是要詢問「{target}」的權利金，我可以接續以這本書為查詢對象。\n\n"
            f"{FAQ_ZH['royalty']}"
        )
    return FAQ_ZH["royalty"]


def reply_listing(ctx: Dict, lang: str) -> str:
    target = format_target(ctx)
    if lang == "en":
        if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
            return (
                f"If you want to check the listing direction for \"{target}\", I can help review:\n"
                "1. Whether e-book rights are available\n"
                "2. Whether the file and metadata meet platform requirements\n"
                "3. Whether the title has already been submitted or listed\n"
                "4. Whether there may be duplicate-listing or copyright conflicts"
            )
        return (
            "Please provide the title name, ISBN, or contract number first. "
            "Then I can help you review whether the title may be listed and what to check next."
        )

    if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
        return (
            f"若您想查詢「{target}」的上架方向，我可以協助確認：\n"
            "1. 是否具有電子書授權\n"
            "2. 書目與檔案格式是否符合平台規範\n"
            "3. 是否已提報 / 已上架 / 待處理\n"
            "4. 是否可能有重複上架或版權衝突"
        )
    return "請先提供書名、ISBN 或合約編號，我才能幫您進一步判斷這本書的上架方向。"


def reply_copyright(ctx: Dict, lang: str) -> str:
    target = format_target(ctx)
    if lang == "en":
        if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
            return (
                f"If you are asking about rights for \"{target}\", I can help organize the review direction:\n"
                "1. Whether the license may still be valid\n"
                "2. Whether the title may be listed on a given platform\n"
                "3. Whether there may be rights conflicts or duplicate authorization issues"
            )
        return (
            "Please provide the title, ISBN, or contract number first. "
            "Then I can help you organize the rights/licensing review direction."
        )

    if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
        return (
            f"若您是在問「{target}」的版權 / 授權狀態，我可以協助整理確認方向：\n"
            "1. 是否仍在授權期間內\n"
            "2. 是否可上架指定平台\n"
            "3. 是否可能有版權衝突或重複授權問題"
        )
    return "請提供書名、ISBN 或合約編號，我才能協助您整理版權 / 授權的確認方向。"


def reply_cannot_list(ctx: Dict, lang: str) -> str:
    target = format_target(ctx)
    if lang == "en":
        if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
            return (
                f"If \"{target}\" cannot be listed or submitted, common reasons include:\n"
                "1. Expired e-book rights\n"
                "2. Platform format issues\n"
                "3. Incomplete metadata or missing materials\n"
                "4. Duplicate listing or copyright conflict"
            )
        return FAQ_EN["cannot_list"]

    if ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number"):
        return (
            f"若「{target}」無法提報或無法上架，常見原因包括：\n"
            "1. 電子書授權已失效\n"
            "2. 不符平台格式規範\n"
            "3. 書目資料待補件\n"
            "4. 重複上架或版權衝突"
        )
    return FAQ_ZH["cannot_list"]


def reply_materials(ctx: Dict, lang: str) -> str:
    return FAQ_EN["materials"] if lang == "en" else FAQ_ZH["materials"]


def reply_listing_time(ctx: Dict, lang: str) -> str:
    return FAQ_EN["listing_time"] if lang == "en" else FAQ_ZH["listing_time"]


def reply_contact(ctx: Dict, lang: str) -> str:
    return FAQ_EN["contact"] if lang == "en" else FAQ_ZH["contact"]


def reply_identifier_only(ctx: Dict, lang: str, user_input: str) -> Optional[str]:
    stripped = user_input.strip()
    isbn = extract_isbn(stripped)
    contract_number = extract_contract_number(stripped)

    # 若使用者幾乎只輸入一個 ISBN / 合約編號，回覆接續提示
    if isbn and len(stripped.replace("-", "")) <= 20:
        if lang == "en":
            return (
                f"Got it. I will keep ISBN {isbn} as the current title in context.\n\n"
                "You can now continue by asking about listing, royalties, licensing, "
                "or reasons why it cannot be submitted."
            )
        return (
            f"收到，我已將 ISBN {isbn} 記為目前查詢對象。\n\n"
            "接下來您可以直接繼續問：上架、權利金、授權、版權或無法提報原因。"
        )

    if contract_number and len(stripped) <= 24:
        if lang == "en":
            return (
                f"Got it. I will keep contract number {contract_number} as the current context.\n\n"
                "You can continue by asking about royalties, listing, or licensing."
            )
        return (
            f"收到，我已將合約編號 {contract_number} 記為目前查詢上下文。\n\n"
            "接下來您可以直接問：權利金、上架、授權或版權相關問題。"
        )
    return None


def reply_followup_without_topic(ctx: Dict, lang: str) -> Optional[str]:
    if not (ctx.get("isbn") or ctx.get("book_name") or ctx.get("contract_number")):
        return None

    target = format_target(ctx)
    if lang == "en":
        return (
            f"I will continue using \"{target}\" as the current title.\n\n"
            "You can ask follow-up questions such as:\n"
            "- Can it be listed?\n"
            "- What about royalties?\n"
            "- Is the license still valid?\n"
            "- Why can't it be submitted?"
        )

    return (
        f"我會先接續以「{target}」作為目前查詢對象。\n\n"
        "您可以繼續問：\n"
        "- 這本可以上架嗎？\n"
        "- 權利金怎麼結算？\n"
        "- 授權還有效嗎？\n"
        "- 為什麼不能提報？"
    )


def get_suggested_questions(lang: str) -> List[str]:
    return QUESTION_TEMPLATES_EN if lang == "en" else QUESTION_TEMPLATES_ZH


def generate_reply(user_input: str) -> str:
    update_context(user_input)

    ctx = st.session_state.context
    lang = ctx["language"]

    # 問候
    if lang == "en":
        if any(w in user_input.lower() for w in ["hello", "hi", "hey"]):
            return (
                "Hello. I am your book distribution, listing, royalty, and licensing assistant.\n\n"
                "You can ask me about cooperation, listing workflow, royalties, licensing, or why a title cannot be listed."
            )
    else:
        if any(w in user_input for w in ["你好", "您好", "哈囉", "嗨"]):
            return (
                "您好，我是圖書經銷／上架／權利金／版權助手。\n\n"
                "您可以直接問我：合作方式、上架流程、權利金、授權、版權，或無法提報的原因。"
            )

    # 若只是輸入 ISBN / 合約編號
    identifier_reply = reply_identifier_only(ctx, lang, user_input)
    if identifier_reply:
        return identifier_reply

    # 若為接續指代
    if contains_followup_reference(user_input, lang) and not detect_topic(user_input, lang):
        followup = reply_followup_without_topic(ctx, lang)
        if followup:
            return followup

    topic = detect_topic(user_input, lang) or ctx.get("topic")

    if topic == "cooperation":
        return reply_cooperation(ctx, lang)
    if topic == "royalty":
        return reply_royalty(ctx, lang)
    if topic == "listing":
        return reply_listing(ctx, lang)
    if topic == "copyright":
        return reply_copyright(ctx, lang)
    if topic == "cannot_list":
        return reply_cannot_list(ctx, lang)
    if topic == "materials":
        return reply_materials(ctx, lang)
    if topic == "listing_time":
        return reply_listing_time(ctx, lang)
    if topic == "contact":
        return reply_contact(ctx, lang)

    # fallback
    suggestions = get_suggested_questions(lang)
    if lang == "en":
        return (
            "I am not fully sure which topic you want to ask about yet.\n\n"
            "You can try one of these examples:\n- "
            + "\n- ".join(suggestions[:5])
        )

    return (
        "我目前還不太確定您想詢問哪一類問題。\n\n"
        "您可以參考這些問法：\n- "
        + "\n- ".join(suggestions[:5])
    )


def clear_chat() -> None:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "您好，我是圖書經銷／上架／權利金／版權助手 📚\n\n"
                "您可以直接問我：合作、上架、權利金、授權、版權、無法提報等問題。"
            ),
        }
    ]
    st.session_state.context = {
        "language": "zh",
        "isbn": None,
        "contract_number": None,
        "book_name": None,
        "publisher": None,
        "role_hint": None,
        "topic": None,
    }


# =========================================================
# Sidebar
# =========================================================
with st.sidebar:
    st.header("⚙️ 功能")
    st.button("清空對話", use_container_width=True, on_click=clear_chat)

    st.markdown("---")
    st.subheader("💡 問題模板（中文）")
    for q in QUESTION_TEMPLATES_ZH:
        st.caption(f"• {q}")

    st.subheader("💡 Question templates (English)")
    for q in QUESTION_TEMPLATES_EN:
        st.caption(f"• {q}")

    st.markdown("---")
    st.subheader("🧠 目前上下文")
    st.json(st.session_state.context)

# =========================================================
# Main UI
# =========================================================
st.title("📚 圖書經銷客服助手")
st.caption(
    "支援：圖書經銷、平台上架、權利金、版權 / 授權、無法提報原因、合作洽詢、基本中英雙語問答。"
)

# 聊天紀錄
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 快速問題按鈕
st.markdown("### 快速提問")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("如何跟你們合作？", use_container_width=True):
        quick_prompt = "如何跟你們合作？"
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        st.session_state.messages.append({"role": "assistant", "content": generate_reply(quick_prompt)})
        st.rerun()
with col2:
    if st.button("權利金多久結算？", use_container_width=True):
        quick_prompt = "我是出版社，請問銷售後多久可以結算權利金？"
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        st.session_state.messages.append({"role": "assistant", "content": generate_reply(quick_prompt)})
        st.rerun()
with col3:
    if st.button("這本書為什麼不能上架？", use_container_width=True):
        quick_prompt = "這本書為什麼不能上架？"
        st.session_state.messages.append({"role": "user", "content": quick_prompt})
        st.session_state.messages.append({"role": "assistant", "content": generate_reply(quick_prompt)})
        st.rerun()

# Chat input
prompt = st.chat_input("請輸入訊息，例如：我是出版社，想合作上架電子書，流程是什麼？ / I am a publisher. How can I work with you?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    reply = generate_reply(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(reply)
