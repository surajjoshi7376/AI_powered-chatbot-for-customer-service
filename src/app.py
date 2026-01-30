import streamlit as st
from chatbot import pipeline

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="SupportMate — Your Customer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Custom CSS for Better Look
# -------------------------------
st.markdown("""
<style>
/* Import clean professional font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Chat container width */
.chat-container {
    max-width: 760px;
    margin: auto;
}

/* Base chat bubble */
.chat-bubble {
    display: inline-block;
    padding: 10px 14px;
    border-radius: 14px;
    margin-bottom: 8px;
    max-width: 75%;
    line-height: 1.45;
    font-size: 15px;
    word-wrap: break-word;
}

/* User message */
.user-bubble {
    background-color: #DCF8C6;
    color: #1f2933;   /* Dark readable text */
    border-top-right-radius: 4px;
    align-self: flex-end;
}

/* Bot message */
.bot-bubble {
    background-color: #F1F3F5;
    color: #111827;   /* Darker text */
    border-top-left-radius: 4px;
}

/* Align bubbles properly */
.user-container {
    display: flex;
    justify-content: flex-end;
}

.bot-container {
    display: flex;
    justify-content: flex-start;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

/* Input box polish */
.stChatInput textarea {
    font-size: 15px !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.markdown("## 🤖 SupportMate")
    st.markdown(
        """
        **What I can help with:**
        - 📦 Order tracking  
        - 🚚 Shipping info  
        - 🔄 Returns & refunds  
        - 📜 Store policies  
        """
    )

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    show_sources = st.checkbox("🔍 Show retrieved context", value=False)

    st.divider()
    st.markdown(
        "<small>Powered by RAG + FAISS + Qwen</small>",
        unsafe_allow_html=True
    )

# -------------------------------
# Header
# -------------------------------
st.markdown(
    "<h1 style='text-align:center;'>🤖 SupportMate </h1>"
    "<h5 style= 'text-align:center;'> Your Customer Support Assistant</h5>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color: gray;'>Ask about orders, shipping, returns, or refunds</p>",
    unsafe_allow_html=True
)
st.divider()

# -------------------------------
# Chat State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Render Messages
# -------------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        st.markdown(
            f"""
            <div class="user-container">
                <div class="chat-bubble user-bubble">
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="bot-container">
                <div class="chat-bubble bot-bubble">
                    {content}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

            # Optional: show retrieved KB context
        if show_sources and "retrieved" in msg:
                with st.expander("📚 Retrieved Context"):
                    for i, r in enumerate(msg["retrieved"], start=1):
                        st.markdown(
                            f"**{i}. Source:** `{r['source']}`  \n"
                            f"**Score:** {round(r['score'], 3)}  \n"
                            f"**Chunk:** {r['chunk'][:400]}..."
                        )

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# Input Box
# -------------------------------
user_input = st.chat_input("Type your question here...")

if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    st.markdown(
    f"""
    <div class="user-container">
        <div class="chat-bubble user-bubble">
            {user_input}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    # Run pipeline
    with st.chat_message("assistant"):
        with st.spinner("🔎 Searching knowledge base..."):
            result = pipeline(user_input)
            reply = result["final_answer"]

            st.markdown(
    f"""
    <div class="bot-container">
        <div class="chat-bubble bot-bubble">
            {reply}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

            # Save bot response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply,
                    "retrieved": result.get("retrieved", [])
                }
            )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    "<center><small>© 2026 SupportMate — Your Customer Support Assistant</small></center>",
    unsafe_allow_html=True
)