import streamlit as st
import json
import os
import subprocess
from pathlib import Path
import re
from openai import OpenAI
from dotenv import load_dotenv
from components.layout import load_main_area
from components.coordination_agent import render_coordination_agent

load_dotenv()

st.set_page_config(page_title="Atlas 2.0 Migration Dashboard", layout="wide")

st.title("🧭 Atlas 2.0 Migration Dashboard")

# Layout containers
left, right = st.columns([2, 1])

# Load data paths from env or defaults
discovery_path = os.getenv("DISCOVERY_PATH", "data/discovery_output.json")
plan_path = os.getenv("PLAN_OUTPUT_PATH", "data/migration_plan.json")
project_path = os.getenv("PROJECT_PATH", "./")
execution_output_dir = os.getenv("EXECUTION_OUTPUT_DIR", "data/generated_code")
validation_report_path = os.getenv("VALIDATION_REPORT_PATH", "data/validation_report.json")
openai_api_key = os.getenv("OPENAI_API_KEY")

paths = {
    "discovery": discovery_path,
    "plan": plan_path,
    "project": project_path,
    "execution": execution_output_dir,
    "validation": validation_report_path
}

with left:
    load_main_area(paths)

with right:
    render_coordination_agent(discovery_path, plan_path, api_key=openai_api_key)

# Footer
st.markdown("---")
st.caption("Built for Hackathon • Atlas 2.0 Migration Agents")
