import streamlit as st
import json
import os
from openai import OpenAI

def render_coordination_agent(discovery_path, plan_path, api_key):
    client = OpenAI(api_key=api_key)

    st.subheader("🤖 Coordination Agent (LLM-powered)")
    model = st.selectbox("Select OpenAI Model", ["gpt-3.5-turbo", "gpt-4"], index=1)
    prompt = st.text_area("Ask a migration-related question or request a summary:")

    if st.button("💬 Ask OpenAI"):
        if not api_key:
            st.warning("Missing OpenAI API key in environment.")
            return

        discovery_data = {}
        plan_data = {}
        if os.path.exists(discovery_path):
            with open(discovery_path) as f:
                discovery_data = json.load(f)
        if os.path.exists(plan_path):
            with open(plan_path) as f:
                plan_data = json.load(f)

        if not (discovery_data and plan_data):
            st.warning("Please run discovery and planning agents first.")
            return

        full_context = f"""
Discovery Data:
{json.dumps(discovery_data, indent=2)}

Migration Plan:
{json.dumps(plan_data, indent=2)}

User Prompt: {prompt.strip()}
"""

        with st.spinner("Thinking with OpenAI..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a cloud infrastructure migration assistant for AWS."},
                        {"role": "user", "content": full_context}
                    ]
                )
                st.success("Response from OpenAI:")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"OpenAI call failed: {e}")
