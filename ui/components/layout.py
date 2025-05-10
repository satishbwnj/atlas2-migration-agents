import streamlit as st
import json
import os
import subprocess
import re
from components.plan_summary import render_plan_summary
from components.resource_table import render_resource_table
from components.validation_report import render_validation_report
from components.deploy_agent import render_deploy_agent

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def load_main_area(paths):
    # Load discovery data
    discovery_data = {}
    if os.path.exists(paths["discovery"]):
        with open(paths["discovery"]) as f:
            discovery_data = json.load(f)
            st.success(f"Loaded discovery data from `{paths['discovery']}`")
    else:
        st.warning(f"Discovery file not found at `{paths['discovery']}`")
        if st.button("▶ Run Discovery Agent", key="run_discovery"):
            with st.spinner("Running discovery..."):
                try:
                    subprocess.run(["python3", "agents/discovery_agent.py"], check=True)
                    st.success("Discovery agent completed successfully.")
                    st.rerun()
                except subprocess.CalledProcessError:
                    st.error("Failed to run discovery agent. Check logs.")

    # Load plan data
    plan_data = {}
    if os.path.exists(paths["plan"]):
        with open(paths["plan"]) as f:
            plan_data = json.load(f)
            st.success(f"Loaded migration plan from `{paths['plan']}`")
    else:
        st.warning(f"Plan file not found at `{paths['plan']}`")
        if st.button("▶ Run Planning Agent", key="run_planning"):
            with st.spinner("Generating migration plan..."):
                try:
                    subprocess.run(["python3", "agents/planning_agent.py"], check=True)
                    st.success("Planning agent completed successfully.")
                    st.rerun()
                except subprocess.CalledProcessError:
                    st.error("Failed to run planning agent. Check logs.")

    # Display discovery resources
    if discovery_data.get("resources"):
        render_resource_table(discovery_data["resources"])

    # Display migration plan
    if plan_data.get("plan"):
        render_plan_summary(plan_data)

    # Execute Terraform generation
    st.subheader("⚙️ Generate Terraform from Plan")
    if st.button("▶ Run Execution Agent", key="run_execution"):
        with st.spinner("Generating Terraform files..."):
            try:
                subprocess.run(["python3", "agents/execution_agent.py"], check=True)
                st.success("Terraform files generated successfully.")
                st.rerun()
            except subprocess.CalledProcessError:
                st.error("Failed to generate Terraform files.")

    # Show generated Terraform
    main_tf_path = os.path.join(paths["execution"], "main.tf")
    if os.path.exists(main_tf_path):
        with st.expander("📄 Generated Terraform - main.tf"):
            with open(main_tf_path) as f:
                terraform_code = f.read()
                st.code(terraform_code, language="hcl")
                st.download_button(
                    label="📥 Download main.tf",
                    data=terraform_code,
                    file_name="main.tf",
                    mime="text/plain"
                )

    # Run and show validation report
    st.subheader("✅ Validate Terraform")
    if st.button("▶ Run Validation Agent", key="run_validation"):
        with st.spinner("Running terraform validate..."):
            try:
                subprocess.run(["python3", "agents/validation_agent.py"], check=True)
                st.success("Validation complete.")
                st.rerun()
            except subprocess.CalledProcessError:
                st.error("Validation agent failed. Check logs.")

    render_validation_report(paths["validation"])

    # Deploy infrastructure
    render_deploy_agent(paths["execution"])

