# ✈️ AI Travel Planning System – Multi-Agent LangGraph Project

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.20-green.svg)](https://www.langchain.com/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)

## 📌 Overview

This is a **production-ready multi-agent AI system** that plans complete trips – flights, hotels, and daily itineraries – using LangGraph orchestration. Instead of manually searching multiple websites, you simply describe your travel needs, and four specialized AI agents work together to deliver a polished, budget‑aware travel plan.

---

## ✨ Features

- ✈️ **Flight Agent** – Searches flight options (mock data, ready for real APIs like AviationStack)
- 🏨 **Hotel Agent** – Real‑time hotel search via Tavily API
- 📅 **Itinerary Agent** – Creates day‑by‑day plans using Groq (Llama 3.3 70B)
- 🤖 **Final Agent** – Combines all data into a clean, human‑readable response
- 🧠 **Persistent Memory** – PostgreSQL stores conversation history (long‑term memory)
- 🌐 **Real‑time APIs** – Tavily (hotels/sights), AviationStack (flights – ready to plug in)
- 💻 **Web Interface** – Streamlit chat UI with agent status indicators

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Agent Orchestration | LangGraph, LangChain |
| LLM | Groq (Llama 3.3 70B) |
| Search API | Tavily |
| Flight API | AviationStack (integration ready) |
| Database | PostgreSQL (checkpoint & memory) |
| Frontend | Streamlit |
| Language | Python 3.10+ |

---

## 📦 Installation (Step by Step)

### 1. Create and activate virtual environment

```bash
python -m venv langgraph_env3

2. Install dependencies
bash
pip install langgraph langchain langchain-openai langchain-groq langchain-community langchain-tavily psycopg[binary] psycopg_pool python-dotenv tavily-python requests streamlit

pip install -U "psycopg[binary,pool]" langgraph-checkpoint-postgres

3. Install PostgreSQL
Windows: Download from postgresql.org – remember password and port (default 5432)

Mac: brew install postgresql && brew services start postgresql

Linux (Ubuntu): sudo apt update && sudo apt install postgresql postgresql-contrib && sudo systemctl start postgresql

4. Create database
Open pgAdmin4 or psql and run:

sql
CREATE DATABASE langgraph_memory_demo;

5. Set up .env file
Create .env in the project root:

env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/langgraph_memory_demo

Replace YOUR_PASSWORD with your actual PostgreSQL password (and port if different).

6. Get API keys
API	Link
Groq	console.groq.com
Tavily	tavily.com
AviationStack	aviationstack.com

🚀 Running the Application
Terminal (CLI)
bash
python main.py
Then enter a request, e.g., Plan a 7-day Japan trip under 2 lakhs

Web Interface (Streamlit)
bash
streamlit run frontend.py
Browser opens at http://localhost:8501 – you get a chat UI with agent status.

🔄 Project Workflow
Flight Agent – searches flights (mock data, ready for AviationStack API)

Hotel Agent – calls Tavily API for hotel recommendations

Itinerary Agent – uses Groq LLM to create day‑by‑day schedule

Final Agent – formats final response and checks budget

PostgreSQL – stores conversation under a thread_id for long‑term memory

All agents share a TravelState dictionary that flows through the graph.

💬 Example Prompts
Plan a complete 7 days Japan trip including flights, hotels and sightseeing under 2 lakhs.

5-day trip from New York to Orlando for a family of 4, need flights and kid-friendly hotels.

Weekend trip from Mumbai to Goa, flights and beach view hotels.

3-day business trip to Singapore, need flights and hotel near Marina Bay.