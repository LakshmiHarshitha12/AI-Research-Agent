# ============================================================
# 🖥️ STREAMLIT UI — Web Interface for the Research Agent
#
# Streamlit turns Python scripts into web apps instantly!
# No HTML, no CSS, no JavaScript needed.
#
# Run with: streamlit run app.py
# ============================================================

import streamlit as st
import time
from agent import run_research_agent

# -------------------------------------------------------
# PAGE CONFIGURATION
# Must be the FIRST streamlit command in the file
# -------------------------------------------------------
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔬",
    layout="wide",                    # Use full screen width
    initial_sidebar_state="expanded"  # Show sidebar by default
)

# -------------------------------------------------------
# CUSTOM STYLES
# st.markdown with unsafe_allow_html lets us add CSS
# -------------------------------------------------------
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    /* Status message box */
    .status-box {
        background: #1e1e2e;
        border-left: 3px solid #6366f1;
        padding: 8px 14px;
        border-radius: 4px;
        margin: 4px 0;
        font-family: monospace;
        font-size: 0.85rem;
        color: #cdd6f4;
    }
    /* Report output box */
    .report-box {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------
# SIDEBAR — Settings and Info
# st.sidebar puts things in the left panel
# -------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/robot.png", width=80)
    st.title("⚙️ Settings")
    st.divider()

    # Model info
    st.markdown("**🤖 Model**")
    st.info("Llama 4 Scout via Groq\n(Free & Fast!)")

    st.divider()

    # How it works section
    st.markdown("**🧠 How It Works**")
    st.markdown("""
    1. You enter a research topic
    2. Agent **plans** search queries
    3. Agent **searches** the web (2-3x)
    4. Agent **synthesizes** findings
    5. You get a full report!
    """)

    st.divider()

    # Key concepts for interview prep
    st.markdown("**🎯 AI Concepts Used**")
    st.markdown("""
    - `Agentic Loop` (ReAct pattern)
    - `Tool Use / Function Calling`
    - `Prompt Engineering`
    - `Context Window Management`
    """)

    st.divider()
    st.caption("Built with Groq + Tavily + Streamlit")
    st.caption("🔗 [View on GitHub](https://github.com)")


# -------------------------------------------------------
# MAIN PAGE
# -------------------------------------------------------
st.markdown('<p class="main-title">🔬 AI Research Agent</p>', unsafe_allow_html=True)
st.markdown("**Autonomous research powered by Llama 4 + Groq**  \nEnter any topic and watch the agent search, think, and synthesize a full report.")

st.divider()

# -------------------------------------------------------
# INPUT SECTION
# -------------------------------------------------------
col1, col2 = st.columns([3, 1])   # 3:1 ratio columns

with col1:
    # Text input for research topic
    topic = st.text_input(
        label="Research Topic",
        placeholder="e.g. Latest advancements in AI agents 2024",
        label_visibility="collapsed"
    )

with col2:
    # Big research button
    start_button = st.button("🚀 Research", use_container_width=True, type="primary")

# Example topics as quick-click buttons
st.markdown("**Try an example:**")
ex1, ex2, ex3 = st.columns(3)

with ex1:
    if st.button("🤖 AI Agent trends", use_container_width=True):
        topic = "Latest advancements in AI agents 2024"
        start_button = True

with ex2:
    if st.button("🧠 Prompt Engineering", use_container_width=True):
        topic = "Best practices for prompt engineering with LLMs"
        start_button = True

with ex3:
    if st.button("📚 RAG explained", use_container_width=True):
        topic = "How does Retrieval Augmented Generation RAG work"
        start_button = True


# -------------------------------------------------------
# RESEARCH EXECUTION
# -------------------------------------------------------
if start_button and topic:

    st.divider()

    # Two columns: live log on left, report on right
    log_col, report_col = st.columns([1, 2])

    with log_col:
        st.markdown("#### 📡 Live Agent Log")
        log_container = st.container()     # We'll add messages here live

    with report_col:
        st.markdown("#### 📄 Research Report")
        report_placeholder = st.empty()    # Will show report when done
        report_placeholder.info("⏳ Waiting for agent to complete research...")

    # -------------------------------------------------------
    # CALLBACK FUNCTION
    # This is called by agent.py every time something happens
    # It updates the UI in real time!
    #
    # 🎯 INTERVIEW CONCEPT: Callbacks decouple the agent logic
    #    from the UI — agent.py doesn't need to know about Streamlit
    # -------------------------------------------------------
    log_messages = []   # Store all messages

    def on_update(update_type: str, message: str):
        """Called by agent on every step — updates the UI live"""
        log_messages.append((update_type, message))

        # Choose icon based on update type
        icons = {
            "thinking": "🧠",
            "tool_call": "🔧",
            "tool_result": "✅",
            "done": "🎉",
            "error": "❌"
        }
        icon = icons.get(update_type, "•")

        # Rebuild the log display with all messages so far
        with log_container:
            for t, msg in log_messages:
                ico = icons.get(t, "•")
                # Remove markdown bold for display in code block
                clean_msg = msg.replace("**", "")
                st.markdown(
                    f'<div class="status-box">{ico} {clean_msg}</div>',
                    unsafe_allow_html=True
                )

    # -------------------------------------------------------
    # RUN THE AGENT
    # st.spinner shows a loading spinner while code runs
    # -------------------------------------------------------
    with st.spinner("Agent is researching..."):
        result = run_research_agent(
            research_topic=topic,
            max_iterations=10,
            on_update=on_update      # Pass our UI callback!
        )

    # -------------------------------------------------------
    # SHOW FINAL REPORT
    # st.markdown renders markdown formatting nicely
    # -------------------------------------------------------
    with report_col:
        report_placeholder.empty()   # Clear the "waiting" message

        if result.startswith("❌") or result.startswith("⚠️"):
            st.error(result)
        else:
            st.markdown(result)

            # Download button — lets user save the report!
            st.download_button(
                label="⬇️ Download Report",
                data=result,
                file_name=f"research_{topic[:30].replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )

    # Success message at the bottom
    st.success("✅ Research complete! Scroll up to read the report.")

elif start_button and not topic:
    st.warning("⚠️ Please enter a research topic first!")


# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.divider()
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.8rem'>"
    "Built with ❤️ using Groq API + Tavily + Streamlit | "
    "AI Research Agent — Portfolio Project"
    "</div>",
    unsafe_allow_html=True
)
