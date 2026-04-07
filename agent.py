# ============================================================
# 🤖 AI RESEARCH AGENT — Core Logic
# Powered by Groq (FREE!) + Tavily Search
# ============================================================

import os
import json
from datetime import datetime
from typing import List, Dict, Callable, Optional
from groq import Groq
import requests
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------
# 🧰 TOOL DEFINITIONS
# 🎯 INTERVIEW TIP: This format is the industry standard for
#    tool use / function calling across all major LLM APIs
# -------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for current information on a topic. "
                "Use this when you need up-to-date facts, recent news, "
                "or information you don't already know."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the web"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return (default 5)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_findings",
            "description": (
                "Summarize and synthesize all research findings into a "
                "clear structured report. Call this ONLY after gathering "
                "enough information from web searches."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The main research topic"
                    },
                    "findings": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of key findings from searches"
                    },
                    "report_format": {
                        "type": "string",
                        "enum": ["brief", "detailed", "bullet_points"],
                        "description": "How to format the final report"
                    }
                },
                "required": ["topic", "findings"]
            }
        }
    }
]


# -------------------------------------------------------
# 🔍 TOOL IMPLEMENTATIONS
# -------------------------------------------------------

def web_search(query: str, num_results: int = 5) -> Dict:
    """
    Searches the web using Tavily API.
    Falls back to mock data if no API key is set.

    🎯 INTERVIEW CONCEPT: Tool execution layer —
    the bridge between AI decisions and real-world actions.
    """
    api_key = os.getenv("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")

    if not api_key:
        return {
            "query": query,
            "results": [
                {
                    "title": f"Result about {query}",
                    "url": "https://example.com",
                    "content": (
                        f"Simulated content about {query}. "
                        f"Add TAVILY_API_KEY to .env for real web results. "
                        f"This topic has seen many recent developments."
                    )
                }
            ],
            "note": "Mock data — add TAVILY_API_KEY to .env for real searches"
        }

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": num_results,
        "search_depth": "advanced",
        "include_answer": True
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "query": query,
            "quick_answer": data.get("answer", ""),
            "results": [
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:500]
                }
                for r in data.get("results", [])
            ]
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "query": query}


def summarize_findings(topic: str, findings: List[str], report_format: str = "detailed") -> Dict:
    """
    Organizes findings into a structured research report.

    🎯 INTERVIEW CONCEPT: Structured output — converting raw
    AI findings into a clean, usable format.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {
        "topic": topic,
        "generated_at": now,
        "format": report_format,
        "total_findings": len(findings),
        "findings": findings,
        "summary": f"Research on '{topic}' completed with {len(findings)} key findings."
    }


# -------------------------------------------------------
# ⚙️ TOOL ROUTER
# -------------------------------------------------------

def execute_tool(tool_name: str, tool_args: Dict) -> str:
    """Routes AI tool calls to the correct Python function."""
    if tool_name == "web_search":
        result = web_search(
            query=tool_args["query"],
            num_results=tool_args.get("num_results", 5)
        )
    elif tool_name == "summarize_findings":
        result = summarize_findings(
            topic=tool_args["topic"],
            findings=tool_args["findings"],
            report_format=tool_args.get("report_format", "detailed")
        )
    else:
        result = {"error": f"Unknown tool: {tool_name}"}

    return json.dumps(result, indent=2)


# -------------------------------------------------------
# 🧠 THE AGENT LOOP
# 🎯 INTERVIEW CONCEPT: ReAct pattern (Reason + Act)
#    Used in LangChain, AutoGen, CrewAI and all agent frameworks
#
# NEW: on_update callback — lets Streamlit UI show live progress!
# This is called every time something happens in the agent loop.
# -------------------------------------------------------

def run_research_agent(
    research_topic: str,
    max_iterations: int = 10,
    on_update: Optional[Callable] = None   # 🆕 Callback for live UI updates
) -> str:
    """
    Runs the AI Research Agent for a given topic.

    Args:
        research_topic: What to research
        max_iterations: Safety limit for the agentic loop
        on_update: Optional callback function called with status updates
                   Signature: on_update(type, message)
                   Types: "thinking", "tool_call", "tool_result", "done", "error"

    Returns:
        Final research report as a string
    """

    def update(type: str, message: str):
        """Helper to send updates to UI or print to console"""
        if on_update:
            on_update(type, message)
        else:
            print(f"[{type.upper()}] {message}")

    # Initialize Groq client
    groq_key = os.getenv("GROK_API_KEY")
    

    client = Groq(api_key=groq_key)


    update("thinking", f"🔬 Starting research on: **{research_topic}**")

    system_prompt = """You are an expert AI Research Agent. Your job is to:

1. PLAN: Break down the research topic into key sub-questions
2. SEARCH: Use web_search tool multiple times to gather information
   - Search for different angles (overview, recent news, expert opinions)
   - Always do at least 2-3 searches before summarizing
3. SYNTHESIZE: Use summarize_findings tool to compile your report

RULES:
- Always search before summarizing — never make up information
- Be thorough: search for multiple aspects of the topic
- If a search gives poor results, try a different query

FORMAT your final answer as a clean, well-structured markdown report."""

    # 🎯 INTERVIEW CONCEPT: Message history = how agents remember context
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please research this topic thoroughly: {research_topic}"}
    ]

    iteration = 0

    # -------------------------------------------------------
    # THE MAIN AGENTIC LOOP
    # -------------------------------------------------------
    while iteration < max_iterations:
        iteration += 1
        update("thinking", f"🧠 Thinking... (step {iteration}/{max_iterations})")

        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                parallel_tool_calls=False,
                max_tokens=4096
            )
        except Exception as e:
            update("error", f"❌ API error: {str(e)}")
            return f"Error: {str(e)}"

        response_message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason
        messages.append(response_message)

        # Case A: Done — return final answer
        if finish_reason == "stop":
            update("done", "✅ Research complete!")
            return response_message.content

        # Case B: Tool calls requested
        elif finish_reason == "tool_calls":
            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Show what the agent is doing in the UI
                if tool_name == "web_search":
                    update("tool_call", f"🔍 Searching: **{tool_args.get('query', '')}**")
                elif tool_name == "summarize_findings":
                    update("tool_call", f"📝 Summarizing {len(tool_args.get('findings', []))} findings...")

                result_str = execute_tool(tool_name, tool_args)
                update("tool_result", f"✓ Got results for: {tool_name}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": result_str
                })

        else:
            update("error", f"⚠️ Unexpected finish reason: {finish_reason}")
            break

    return "⚠️ Agent reached maximum iterations. Research may be incomplete."


# -------------------------------------------------------
# Run directly from terminal: python agent.py
# -------------------------------------------------------
if __name__ == "__main__":
    result = run_research_agent(
        "Latest advancements in AI agents and LLM tool use in 2024"
    )
    print("\n" + "="*60)
    print("📄 FINAL RESEARCH REPORT")
    print("="*60)
    print(result)
