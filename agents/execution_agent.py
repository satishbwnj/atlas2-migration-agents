import json
import os
from pathlib import Path

TERRAFORM_TEMPLATE = """
resource "{type}" "{name}" {{
{body}
}}
"""

UNCONFIGURABLE_ATTRS = {
    "arn", "id", "address", "endpoint", "hosted_zone_id", "resource_id",
    "status", "instance_state", "primary_network_interface_id",
    "public_dns", "public_ip", "private_dns", "engine_version_actual", "owner_id"
}

CPU_DEPRECATED_KEYS = {"cpu_core_count", "cpu_threads_per_core"}

CPU_REPLACEMENT_TEMPLATE = """
  cpu_options {{
    core_count       = {core_count}
    threads_per_core = {threads_per_core}
  }}
"""

def sanitize(value):
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return None
    else:
        return value

def generate_terraform_block(resource):
    tf_type = resource.get("resource_type", resource.get("type"))
    name = (
        resource.get("details", {}).get("name") or
        resource.get("name") or
        resource.get("resource_id") or
        resource.get("id") or
        "resource"
    )
    name = name.replace('-', '_')

    attributes = resource.get("details", {}).get("attributes", {})
    lines = []
    cpu_attrs = {}

    for k, v in attributes.items():
        if k in UNCONFIGURABLE_ATTRS:
            continue
        if k in CPU_DEPRECATED_KEYS:
            cpu_attrs[k] = v
            continue

        val = sanitize(v)
        if isinstance(val, (list, dict)) or val is None or val == "\"\"":
            continue  # skip complex, null, or empty values
        lines.append(f"  {k} = {val}")

    if cpu_attrs:
        core = cpu_attrs.get("cpu_core_count", 1)
        threads = cpu_attrs.get("cpu_threads_per_core", 1)
        lines.append(CPU_REPLACEMENT_TEMPLATE.format(core_count=core, threads_per_core=threads))

    return TERRAFORM_TEMPLATE.format(type=tf_type, name=name, body="\n".join(lines))

def generate_files(plan, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(output_dir, "main.tf"), "w") as f:
        for resource in plan:
            tf = generate_terraform_block(resource)
            f.write(tf + "\n")
    print(f"✔ Terraform files written to {output_dir}/main.tf")

def main():
    plan_path = os.getenv("PLAN_OUTPUT_PATH", "data/migration_plan.json")
    output_dir = os.getenv("EXECUTION_OUTPUT_DIR", "data/generated_code")

    with open(plan_path) as f:
        plan_data = json.load(f)
        plan = plan_data.get("plan", [])

    generate_files(plan, output_dir)

if __name__ == "__main__":
    main()