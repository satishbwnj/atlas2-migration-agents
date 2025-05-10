import streamlit as st
import json

def render_resource_table(resources):
    st.subheader("🔍 Discovered Resources")
    for r in resources:
        with st.expander(f"{r['type']} - {r.get('id', r.get('name', 'unknown'))}"):
            st.json(r)
