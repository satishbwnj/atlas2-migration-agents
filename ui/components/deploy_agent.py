import streamlit as st
import os
import subprocess
import json

def render_deploy_agent(tf_dir):
    st.subheader("🚀 Deploy Infrastructure")

    tf_main = os.path.join(tf_dir, "main.tf")
    if not os.path.exists(tf_main):
        st.warning("No Terraform code found. Please run the Execution Agent first.")
        return

    with st.expander("📄 Preview main.tf"):
        with open(tf_main) as f:
            st.code(f.read(), language="hcl")

    if st.button("🔄 Initialize Terraform", key="deploy_init"):
        with st.spinner("Running terraform init..."):
            result = subprocess.run(["terraform", "init"], cwd=tf_dir, capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Terraform initialized successfully.")
                st.code(result.stdout)
            else:
                st.error("Terraform init failed.")
                st.code(result.stderr)

    if st.button("🔁 Terraform Plan", key="deploy_plan"):
        with st.spinner("Running terraform plan..."):
            result = subprocess.run(["terraform", "plan", "-out=tfplan"], cwd=tf_dir, capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Terraform plan created.")
                st.code(result.stdout)
            else:
                st.error("Terraform plan failed.")
                st.code(result.stderr)

    if st.button("✅ Apply Infrastructure", key="deploy_apply"):
        with st.spinner("Applying Terraform plan..."):
            result = subprocess.run(["terraform", "apply", "-auto-approve"], cwd=tf_dir, capture_output=True, text=True)
            if result.returncode == 0:
                st.success("Infrastructure deployed successfully.")
                st.code(result.stdout)
            else:
                st.error("Terraform apply failed.")
                st.code(result.stderr)
