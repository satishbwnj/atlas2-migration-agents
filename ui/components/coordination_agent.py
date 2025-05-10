import streamlit as st
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def render_coordination_agent(discovery_path, plan_path, api_key):
    client = OpenAI(api_key=api_key)

    # Custom CSS
    st.markdown("""
        <style>
        .chat-container {
            display: flex;
            flex-direction: column-reverse;
            height: 400px;
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

    st.subheader("🤖 Coordination Agent (LLM-powered)")

    # UI Controls
    model = st.selectbox("Select OpenAI Model", ["gpt-3.5-turbo", "gpt-4"], index=1)

    # Load discovery and plan data
    discovery_data, plan_data = {}, {}
    if os.path.exists(discovery_path):
        with open(discovery_path) as f:
            discovery_data = json.load(f)
    if os.path.exists(plan_path):
        with open(plan_path) as f:
            plan_data = json.load(f)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm your coordination agent. Ask me anything about your cloud migration."}
        ]

    # Show chat history (in reverse so latest is at bottom)
    chat_html = '<div class="chat-container">'
    for msg in reversed(st.session_state.messages):
        role_class = "user" if msg["role"] == "user" else "assistant"
        chat_html += f'<div class="message {role_class}">{msg["content"]}</div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Type your coordination request..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.experimental_rerun()

    # Generate response if user message is last
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        if not (discovery_data and plan_data):
            st.warning("Please run discovery and planning agents first.")
        else:
            with st.spinner("Coordinating across agents..."):
                full_context = f"""

Discovery Data:
{json.dumps(discovery_data, indent=2)}

Migration Plan:
{json.dumps(plan_data, indent=2)}

Conversation History:
{[m for m in st.session_state.messages]}
"""

                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are a cloud infrastructure coordination agent that orchestrates AWS migrations using insights from discovery, planning, execution, and validation phases."},
                            {"role": "user", "content": full_context}
                        ]
                    )
                    reply = response.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"OpenAI call failed: {e}")
