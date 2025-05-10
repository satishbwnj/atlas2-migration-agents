import os
import subprocess
import json
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_PROFILE = os.getenv("AWS_PROFILE", "default")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def is_terraform_project(project_path):
    tf_files = [f for f in os.listdir(project_path) if f.endswith('.tf') or f.endswith('.tfstate')]
    return len(tf_files) > 0

def run_terraform_show(project_path):
    try:
        result = subprocess.run(
            ["terraform", "show", "-json"],
            cwd=project_path,
            check=True,
            capture_output=True,
            text=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError:
        return None

def discover_terraform_resources(terraform_json):
    resources = []
    values = terraform_json.get("values", {}).get("root_module", {}).get("resources", [])
    for res in values:
        resources.append({
            "type": res.get("type"),
            "name": res.get("name"),
            "attributes": res.get("values")
        })
    return resources

def discover_aws_resources():
    session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
    ec2 = session.client("ec2")
    rds = session.client("rds")

    resources = []

    for reservation in ec2.describe_instances()["Reservations"]:
        for instance in reservation["Instances"]:
            public = "PublicIpAddress" in instance
            resources.append({
                "type": "aws_instance",
                "id": instance["InstanceId"],
                "public": public,
                "ports_open": [],
            })

    for db in rds.describe_db_instances()["DBInstances"]:
        public = db.get("PubliclyAccessible", False)
        resources.append({
            "type": "aws_db_instance",
            "id": db["DBInstanceIdentifier"],
            "engine": db["Engine"],
            "public": public,
            "port": db["Endpoint"]["Port"]
        })

    for sg in ec2.describe_security_groups()["SecurityGroups"]:
        ports = [
            {
                "from_port": rule.get("FromPort"),
                "to_port": rule.get("ToPort"),
                "protocol": rule.get("IpProtocol"),
                "cidr_blocks": rule.get("IpRanges")
            }
            for rule in sg.get("IpPermissions", [])
        ]
        resources.append({
            "type": "aws_security_group",
            "id": sg["GroupId"],
            "name": sg["GroupName"],
            "description": sg["Description"],
            "ports_open": ports
        })

    return resources

def main(project_path):
    if is_terraform_project(project_path):
        print("✔ Terraform files detected. Using Terraform mode.")
        tf_json = run_terraform_show(project_path)
        if tf_json:
            resources = discover_terraform_resources(tf_json)
        else:
            print("⚠ Failed to parse Terraform output.")
            return
    else:
        print("ℹ No Terraform files found. Using AWS API discovery.")
        resources = discover_aws_resources()

    output = {"resources": resources}
    output_path = os.path.join(project_path, "discovery_output.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"✔ Discovery complete. Output written to {output_path}")

if __name__ == "__main__":
    main(os.getenv("PROJECT_PATH", "."))
