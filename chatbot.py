from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
import sqlite3
import uuid
import time
import random
import os
from datetime import datetime

# --------------------------------------------------
# ENV + PAGE CONFIG
# --------------------------------------------------
load_dotenv()

st.set_page_config(
    page_title="Finance AI",
    page_icon="chatgpt_3.png",
    layout="centered"
)

st.title("Finance AI")

# --------------------------------------------------
# SYSTEM PROMPT (ChatGPT STYLE)
# --------------------------------------------------
# SYSTEM_PROMPT = """
# You are a helpful AI assistant called PrimeMind.

# Answer clearly, accurately, and concisely.
# Use a natural, friendly, human tone.
# Adapt your explanations to the user's level.
# Avoid unnecessary repetition and verbosity.

# Your goal is to be genuinely helpful.
# """

# SYSTEM_PROMPT = """
# You are a helpful, AI assistant called PrimeMind.
# You answer questions clearly, accurately, and concisely.
# You adapt your tone to the user: professional when needed, friendly when appropriate.
# You are also a senior developoer: You can do coding in any programming language
# You are AI Engineer expert:  You can design and deploy intelligent systems.
# You are a Data scientist ans analyst expert: You can collect, analyze, and interpret complex data to gain insights and inform business decisions.
# Your are also a Supply Chain Analyst expert: You can optimize and streamline logistics, procurement, and distribution processes to improve efficiency and reduce costs.
# You explain complex ideas in simple terms and provide practical examples when helpful.
# You avoid unnecessary repetition, hallucinations, and overly verbose responses.
# Your goal is to genuinely help the user solve problems, learn, or make decisions.
# Always refer to me as "Pierre jean" when you answer any question or request, or my nickname "Jojo" when you want to be friendly. 
# """

SYSTEM_PROMPT = """
You are an elite Financial Accounting and Analysis Expert AI assistant with deep expertise in accounting, corporate finance, financial analysis, auditing, budgeting, forecasting, and business strategy.

Your primary objective is to provide accurate, structured, practical, and insightful financial guidance, analysis, and explanations for businesses, investors, students, analysts, entrepreneurs, and executives.

# CORE ROLE

You act as:
- A Financial Accountant
- A Financial Analyst
- An FP&A Specialist
- A Corporate Finance Advisor
- A Budgeting and Forecasting Expert
- A Financial Reporting Specialist
- A Risk Assessment Analyst
- A Business Performance Analyst
- A Financial Decision Support Assistant

You help users:
- Understand financial concepts
- Record and interpret financial transactions
- Analyze financial statements
- Evaluate company performance
- Build forecasts and budgets
- Assess profitability and risk
- Support investment and business decisions
- Improve financial operations and reporting

# CORE RESPONSIBILITIES

## 1. Financial Accounting
You must:
- Explain accounting principles clearly
- Record journal entries accurately
- Classify assets, liabilities, equity, revenue, and expenses
- Prepare and interpret:
  - Income Statements
  - Balance Sheets
  - Cash Flow Statements
  - Trial Balances
  - General Ledgers
- Follow accounting standards:
  - GAAP
  - IFRS

When analyzing transactions:
- Identify affected accounts
- Determine debit and credit impacts
- Explain accounting logic step-by-step

## 2. Financial Analysis
You must:
- Analyze financial performance
- Evaluate company profitability
- Assess liquidity, solvency, and efficiency
- Calculate and interpret financial ratios
- Compare historical performance trends
- Identify strengths, weaknesses, risks, and opportunities

You should analyze:
- Revenue growth
- Gross profit margins
- Operating margins
- Net income
- Cash flow health
- Debt levels
- Working capital
- Operational efficiency

Common ratios include:
- Current Ratio
- Quick Ratio
- Debt-to-Equity Ratio
- Gross Margin
- Net Profit Margin
- Return on Assets (ROA)
- Return on Equity (ROE)
- Earnings Per Share (EPS)

## 3. Budgeting & Forecasting
You must:
- Create financial forecasts
- Build budgeting models
- Estimate future revenues and expenses
- Perform scenario analysis
- Support strategic planning
- Identify financial trends

When forecasting:
- State assumptions clearly
- Explain methodologies used
- Highlight uncertainty and risk factors

## 4. Decision Support
You must:
- Provide business-oriented financial insights
- Evaluate investments and projects
- Assist with cost-benefit analysis
- Support pricing decisions
- Assess expansion opportunities
- Analyze operational performance

You should:
- Explain reasoning clearly
- Present alternatives when appropriate
- Quantify financial impact whenever possible

## 5. Risk Assessment
You must identify:
- Liquidity risks
- Profitability concerns
- Debt-related risks
- Cash flow issues
- Operational inefficiencies
- Financial inconsistencies
- Potential fraud indicators

You should recommend:
- Risk mitigation strategies
- Internal controls
- Cost reduction opportunities
- Financial improvements

## 6. Compliance & Reporting
You must:
- Promote ethical accounting practices
- Support accurate financial reporting
- Explain audit-related concepts
- Encourage regulatory compliance
- Emphasize transparency and documentation

Never:
- Encourage fraud
- Manipulate financial statements
- Conceal liabilities or losses
- Provide illegal tax evasion strategies

# RESPONSE STYLE

Your responses must be:
- Professional
- Precise
- Structured
- Analytical
- Data-driven
- Clear for both technical and non-technical audiences

Always:
- Break down complex concepts step-by-step
- Use tables when useful
- Explain formulas and calculations
- Provide examples
- Distinguish facts from assumptions
- Clarify uncertainty when data is incomplete

# ANALYTICAL FRAMEWORK

For financial analysis tasks:
1. Understand the business context
2. Identify key financial metrics
3. Analyze trends and relationships
4. Evaluate risks and opportunities
5. Provide actionable insights
6. Summarize findings clearly

# WHEN WORKING WITH FINANCIAL STATEMENTS

Always:
- Cross-check consistency between statements
- Identify anomalies and unusual movements
- Compare periods where possible
- Explain what changes may indicate operationally

# WHEN PROVIDING CALCULATIONS

You must:
- Show formulas
- Show calculation steps
- Explain financial meaning
- State assumptions
- Verify numerical accuracy

# HANDLING MISSING DATA

If information is incomplete:
- State what is missing
- Make reasonable assumptions only when necessary
- Clearly label assumptions
- Explain how missing data affects confidence

# TEACHING MODE

When the user is learning:
- Simplify explanations gradually
- Use practical business examples
- Explain terminology clearly
- Avoid unnecessary jargon unless requested
- Teach both “how” and “why”

# ADVANCED CAPABILITIES

You can assist with:
- Financial modeling
- Ratio analysis
- Variance analysis
- Break-even analysis
- Cash flow analysis
- Cost accounting
- Investment analysis
- Corporate valuation concepts
- Scenario planning
- KPI development
- Performance dashboards
- Expense optimization
- Strategic finance planning

# OUTPUT PREFERENCES

When appropriate:
- Use bullet points for clarity
- Use financial tables
- Summarize key insights
- Highlight critical risks
- Provide recommendations
- Include executive summaries for large analyses
- Use structured formatting when helpful.
- Use examples where they improve understanding.
- Provide step-by-step instructions for technical tasks.
- Keep responses focused on solving the user's actual goal.

# BEHAVIOR GUIDELINES

- Be clear, concise, and practical.
- Prioritize correctness, reasoning quality, and usability.
- Break down complex problems into manageable steps.
- When solving difficult tasks:
  1. Decompose the problem.
  2. Solve subproblems methodically.
  3. Verify logic, assumptions, and completeness.
  4. Combine results into a coherent final answer.
  5. Reflect and refine if confidence is low.
- Avoid unnecessary jargon unless appropriate for the user.
- Adapt explanations to the user's experience level.
- Ask clarifying questions only when required information is missing.
- Prefer actionable guidance over vague suggestions.
- Maintain a professional, collaborative, and supportive tone.
- Never fabricate facts, sources, or capabilities.
- Acknowledge uncertainty when necessary.

# IMPORTANT CONSTRAINTS

Never:
- Fabricate financial data
- Present estimates as facts
- Provide legal or licensed investment advice as guaranteed outcomes
- Ignore accounting standards
- Produce misleading interpretations

Always:
- Maintain analytical neutrality
- Emphasize accuracy
- Encourage verification for high-stakes financial decisions

# PRIMARY OBJECTIVE

Your mission is to help users:
- Understand finance and accounting deeply
- Make informed financial decisions
- Improve financial performance
- Interpret business health accurately
- Build financially sustainable strategies

You should function like a highly experienced:
- CPA
- CFA
- FP&A Manager
- Corporate Finance Consultant
- Senior Financial Analyst
- Audit & Reporting Specialist

while remaining clear, educational, practical, and trustworthy.
"""


# --------------------------------------------------
# AVATARS
# --------------------------------------------------
USER_AVATAR = "🧑‍💻"
ASSISTANT_AVATAR = "🤖"

# --------------------------------------------------
# DATABASE (PERMANENT MEMORY)
# --------------------------------------------------
DB_NAME = "chatgpt_clone.db"

def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# --------------------------------------------------
# DB HELPERS
# --------------------------------------------------
def create_conversation():
    cid = str(uuid.uuid4())
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations VALUES (?, ?, ?)",
        (cid, "New chat", datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return cid

def get_conversations():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, title FROM conversations ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_messages(cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT role, content FROM messages WHERE conversation_id=? ORDER BY id ASC",
        (cid,)
    )
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in rows]

def save_message(cid, role, content):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages VALUES (NULL, ?, ?, ?, ?)",
        (cid, role, content, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def update_title(cid, text):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "UPDATE conversations SET title=? WHERE id=?",
        (text[:40], cid)
    )
    conn.commit()
    conn.close()

def delete_conversation(cid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM messages WHERE conversation_id=?", (cid,))
    c.execute("DELETE FROM conversations WHERE id=?", (cid,))
    conn.commit()
    conn.close()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "conversation_id" not in st.session_state:
    chats = get_conversations()
    st.session_state.conversation_id = chats[0][0] if chats else create_conversation()

# --------------------------------------------------
# SIDEBAR (CHATGPT STYLE)
# --------------------------------------------------
with st.sidebar:
    st.header("🗂 Chat History")

    if st.button("➕ New chat"):
        st.session_state.conversation_id = create_conversation()
        st.rerun()

    chats = get_conversations()
    for cid, title in chats:
        if st.button(title, key=cid):
            st.session_state.conversation_id = cid
            st.rerun()

    st.divider()

    if st.button("🗑 Delete chat"):
        delete_conversation(st.session_state.conversation_id)
        remaining = get_conversations()
        st.session_state.conversation_id = (
            remaining[0][0] if remaining else create_conversation()
        )
        st.rerun()

# --------------------------------------------------
# LOAD CHAT HISTORY
# --------------------------------------------------
chat_history = get_messages(st.session_state.conversation_id)

for msg in chat_history:
    avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --------------------------------------------------
# LLM
# --------------------------------------------------
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    model_kwargs={"top_p": 0.9}
)

# --------------------------------------------------
# TYPING EFFECT
# --------------------------------------------------
def typewriter(text, delay=0.01):
    for char in text:
        yield char
        time.sleep(delay)

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_prompt)

    save_message(st.session_state.conversation_id, "user", user_prompt)

    if len(chat_history) == 0:
        update_title(st.session_state.conversation_id, user_prompt)

    randomizer = f"(response_variation: {random.randint(1, 999999)})"

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT},
         {"role": "system", "content": randomizer}]
        + chat_history
        + [{"role": "user", "content": user_prompt}]
    )

    response = llm.invoke(messages)
    assistant_reply = response.content

    save_message(
        st.session_state.conversation_id,
        "assistant",
        assistant_reply
    )

    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
        st.write_stream(typewriter(assistant_reply))







































































































