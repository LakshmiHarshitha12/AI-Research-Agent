<<<<<<< HEAD
# 🔬 AI Research Agent

> An autonomous AI agent that researches any topic — searches the web, reasons about results, and synthesizes a full report. Built with Groq (Llama 4), Tavily Search, and Streamlit.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-Llama%204-orange)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎥 Demo

![Agent Demo](https://via.placeholder.com/800x400?text=Add+a+screenshot+or+GIF+here)
=======
# 🤖 AI Research Agent

An AI-powered research agent that autonomously analyzes topics, extracts key insights, and generates structured reports using LLMs.

---

## 🚀 Features
- Multi-step AI agent (Plan → Research → Output)
- Structured research reports
- FastAPI-based API
- LLM-powered reasoning (Groq API)
>>>>>>> fd882f0b1f39eabba55c2034a4acaee38e0e76b6

---

## 🧠 How It Works
<<<<<<< HEAD

```
User Input → Agent Plans → Searches Web (2-3x) → Synthesizes → Report
                ↑                                      |
                └──────── Agentic Loop (ReAct) ────────┘
```

The agent uses the **ReAct pattern** (Reason + Act):
1. **Reason** — Claude/Llama thinks about what to do next
2. **Act** — Calls a tool (web search)
3. **Observe** — Reads the result
4. **Repeat** — Until research is complete

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ai-research-agent.git
cd ai-research-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up API keys
```bash
# Rename .env.example to .env
# Add your keys inside
```

Get your **free** API keys:
- **Groq**: [console.groq.com](https://console.groq.com) — no credit card!
- **Tavily**: [tavily.com](https://tavily.com) — optional, mock data works without it

### 4. Run the web UI
```bash
streamlit run app.py
```

Or run from terminal:
```bash
python agent.py
```

---

## 📁 Project Structure

```
ai-research-agent/
├── agent.py          # Core agent logic — agentic loop, tool use
├── app.py            # Streamlit web UI
├── requirements.txt  # Python dependencies
├── .env.example      # API key template
├── .gitignore        # Keeps secrets safe
└── README.md         # This file
```

---

## 🎯 Key AI Engineering Concepts

| Concept | Where in Code |
|---------|--------------|
| **Agentic Loop** | `while` loop in `run_research_agent()` |
| **Tool Use / Function Calling** | `TOOLS` list + `execute_tool()` |
| **ReAct Pattern** | Think → Act → Observe loop |
| **Prompt Engineering** | `system_prompt` in agent.py |
| **Context Window** | `messages` list sent every iteration |
| **Callback Pattern** | `on_update` function for live UI |

---

## 🛠️ Tech Stack

- **[Groq](https://groq.com)** — Ultra-fast free LLM inference (Llama 4)
- **[Tavily](https://tavily.com)** — AI-optimized web search API
- **[Streamlit](https://streamlit.io)** — Python web app framework

---

## 🔧 How to Extend

- Add **memory** with ChromaDB to remember past research
- Add **multi-agent** support — one agent per research angle
- Add **PDF export** of research reports
- Deploy to **Streamlit Cloud** for free hosting

---

## 👤 Author

**Your Name**
[LinkedIn](https://linkedin.com/in/yourprofile) • [GitHub](https://github.com/yourusername)
=======
1. Breaks topic into key research areas  
2. Generates detailed insights  
3. Formats output into a structured report  

---

## ⚙️ Tech Stack
- Python
- FastAPI
- Groq API (LLMs)
- Prompt Engineering

---

## 📦 Installation

```bash
git clone https://github.com/LakshmiHarshitha12/AI-Research-Agent.git
cd AI-Research-Agent
pip install -r requirements.txt
>>>>>>> fd882f0b1f39eabba55c2034a4acaee38e0e76b6
