import json
import os


def load_discovery_output(path):
    with open(path, 'r') as f:
        return json.load(f)

def generate_migration_plan(resources):
    plan = []
    for res in resources:
        strategy = "analyze"
        if res['type'] == "aws_instance":
            strategy = "migrate to ECS or Fargate"
        elif res['type'] == "aws_db_instance":
            strategy = "migrate to Aurora or RDS Proxy"
        elif res['type'] == "aws_security_group":
            strategy = "review ingress/egress rules"

        plan.append({
            "resource_id": res.get("id"),
            "resource_type": res["type"],
            "strategy": strategy,
            "public": res.get("public", None),
            "details": res
        })
    return plan

def save_migration_plan(plan, output_path):
    with open(output_path, 'w') as f:
        json.dump({"plan": plan}, f, indent=2)
    print(f"✔ Migration plan saved to {output_path}")

def main():
    discovery_path = os.getenv("DISCOVERY_PATH", "data/discovery_output.json")
    plan_output_path = os.getenv("PLAN_OUTPUT_PATH", "data/migration_plan.json")

    discovery = load_discovery_output(discovery_path)
    resources = discovery.get("resources", [])
    plan = generate_migration_plan(resources)
    save_migration_plan(plan, plan_output_path)

if __name__ == "__main__":
    main()
