# ============================================================
# 🚀 FASTAPI BACKEND — AI Research Agent (DEPLOYABLE VERSION)
# ============================================================

from fastapi import FastAPI
from agent import run_research_agent

# Create FastAPI app
app = FastAPI()

# ------------------------------------------------------------
# Root endpoint (health check)
# ------------------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "✅ AI Research Agent is running",
        "usage": "Use /research?query=your_topic"
    }

# ------------------------------------------------------------
# Research endpoint
# ------------------------------------------------------------
@app.get("/research")
def research(query: str):
    try:
        result = run_research_agent(query)
        return {
            "status": "success",
            "query": query,
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }