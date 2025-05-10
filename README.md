# 🧠 Atlas 2.0 Multi-Agent Migration Shell

This repository contains the **foundational shell** for a multi-agent based migration assistant, purpose-built to support the **JPMC Hackathon** project titled:

### 📌 *Leveraging Multiple Large Language Model (LLM) Agents and Workflow for Atlas 2.0 Migration*

---

## 🧭 Project Context

In the vast landscape of **JPMC’s AWS platform**, Atlas 1 currently hosts over a thousand production-grade applications. The firm’s migration to **Atlas 2.0**—a modern cloud-native framework—demands tools that support not only application migration but also **data center to cloud**, **compute transitions**, and **automated infrastructure transformations**.

This shell establishes a fully working prototype that simulates:
- **Discovery of legacy infrastructure**
- **Planning migration steps**
- **Execution via Terraform**
- **Validation and deployment**
- **Coordination using LLMs**

---

## ⚙️ What's Included

| Agent              | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **Discovery Agent**| Uses Terraform or Boto3 to detect legacy resources like EC2, RDS, SGs       |
| **Planning Agent** | Generates a high-level migration plan JSON                                  |
| **Execution Agent**| Creates Terraform HCL based on discovered resources                         |
| **Validation Agent**| Runs `terraform validate` to confirm integrity                             |
| **Deploy Agent**   | Applies Terraform to provision infrastructure                               |
| **Coordination Agent (LLM)** | Chat-based interface to ask questions, orchestrate flow, and auto-trigger agents |

The **Streamlit dashboard** allows users to run each agent step-by-step or interact with the coordination agent powered by **OpenAI GPT models**.

---

## 🧠 Vision for the Hackathon

This is **just the shell**.

### The full vision:
- LLMs will **coordinate and decide** which agents to run, in what order.
- The system will support **self-healing**, automatically adjusting plans or retries on failure.
- Engineers can chat with the LLM to gain insights or trigger custom flows.
- Future enhancements include **Agent Autonomy** (using CrewAI or LangChain), integration with **internal JPMC APIs**, and **multi-region validation**.

---

## 🚀 Local Setup

1. **Clone the repo:**
```bash
git clone https://github.com/satishbwnj/atlas2-migration-agents.git
cd atlas2-migration-agents
