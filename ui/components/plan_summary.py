import streamlit as st
import json

def render_plan_summary(plan_data):
    st.subheader("🧠 Suggested Migration Plan")
    for p in plan_data.get("plan", []):
        with st.expander(f"{p['resource_type']} → {p['strategy']}"):
            st.json(p)
