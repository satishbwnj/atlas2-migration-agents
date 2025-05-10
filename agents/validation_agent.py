import os
import subprocess
import json
from pathlib import Path

def run_terraform_validate(directory):
    try:
        subprocess.run(["terraform", "init", "-input=false"], cwd=directory, check=True, capture_output=True, text=True)
        result = subprocess.run(
            ["terraform", "validate"],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "status": "success",
            "message": result.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": e.stderr.strip() or e.stdout.strip()
        }

def save_report(report, output_path):
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"✔ Validation report written to {output_path}")

def main():
    tf_dir = os.getenv("EXECUTION_OUTPUT_DIR", "data/generated_code")
    report_path = os.getenv("VALIDATION_REPORT_PATH", "data/validation_report.json")

    Path(tf_dir).mkdir(parents=True, exist_ok=True)

    report = run_terraform_validate(tf_dir)
    save_report(report, report_path)

if __name__ == "__main__":
    main()

