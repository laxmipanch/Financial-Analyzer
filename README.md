# Financial-Analyzer

# 🧠 MCP Agentic Workflow Demo — Financial Analyzer

This project is a hands-on exploration of **agentic AI workflows** using the [MCP Agent](https://github.com/lastmile-ai/mcp-agent).

> ⚠️ Not a finance project — the goal is to experiment with **multi-agent coordination**, **LLM evaluation loops**, and **autonomous workflows** via MCP.

---

## 🧩 What It Does

A multi-agent system that:
1. Uses a **Google Search agent** to collect real-time financial data.
2. Passes that data through an **EvaluatorOptimizerLLM**, ensuring only high-quality results proceed.
3. Feeds the research into a **financial analyst agent** for interpretation.
4. Generates a final stock report via a **report writer agent**.
5. Displays everything — logs and output — in a **Streamlit UI**.

---

## 🛠 Tech Stack

- **Python + asyncio**
- **[MCP Protocol](https://modelcontextprotocol.io/)** 
- **OpenAIAugmentedLLM** for GPT-4o integration
- **EvaluatorOptimizerLLM** for auto-improvement loops
- **Streamlit** for UI

---

## 📦 Setup

### 1. Clone & Install

```bash
git clone https://github.com/laxmipanch/Financial-Analyzer.git
```
```bash
pip install -r requirements.txt
```

## Demo
[Watch the demo video](https://drive.google.com/file/d/165NrAk9vmVE96c5RJzUHC9yRa-sBIyGv/view)
