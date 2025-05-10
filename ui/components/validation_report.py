import streamlit as st
import json
import os
import re

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def render_validation_report(path):
    if os.path.exists(path):
        with open(path) as f:
            validation = json.load(f)
            status = validation.get("status", "unknown")
            message = strip_ansi_codes(validation.get("message", ""))
            st.subheader("📋 Validation Report")
            if status == "success":
                st.success(message)
            else:
                st.error(message)
    else:
        st.info("No validation report found. Please run the Validation Agent.")
