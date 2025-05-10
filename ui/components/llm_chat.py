import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def render_llm_chat(discovery_path=None, plan_path=None):
    # Custom CSS styling
    st.markdown("""
        <style>
        .chat-container {
            display: flex;
            flex-direction: column-reverse;
            height: 600px;
            overflow-y: auto;
            padding: 1rem;
            background-color: #f1f3f5;
            border-radius: 12px;
            border: 1px solid #dee2e6;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        .message {
            margin-bottom: 1rem;
            padding: 0.75rem 1rem;
            border-radius: 12px;
            max-width: 75%;
            line-height: 1.4;
            font-size: 0.95rem;
        }
        .user {
            background-color: #d0ebff;
            align-self: flex-end;
            text-align: right;
        }
        .assistant {
            background-color: #ffffff;
            align-self: flex-start;
        }
        .stChatInput input {
            border-radius: 24px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### 🤖 Cloud Migration Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm here to help you with your AWS migration. What would you like to know?"}
        ]

    # Scrollable chat box, in reverse order so newest messages show at bottom
    chat_html = '<div class="chat-container">'
    for msg in reversed(st.session_state.messages):
        role_class = "user" if msg["role"] == "user" else "assistant"
        chat_html += f'<div class="message {role_class}">{msg["content"]}</div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Chat input at the bottom
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message immediately
        st.experimental_rerun()

    # Automatically respond if last message is from user
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.experimental_rerun()
