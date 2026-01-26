# 📊 Screener Agent – Intelligent Stock Screening & Portfolio Engine

An **end-to-end automated stock screening system** built on top of **Screener.in**, designed for **quant-style strategy execution, scoring, ranking, portfolio construction**, and **API / MCP consumption**.

This project:
- Automates Screener.in queries using Playwright
- Extracts & normalizes stock fundamentals
- Calculates **composite scores** and **decayed scores**
- Ranks stocks per strategy
- Builds **Top-N portfolios**
- Persists everything in **SQLite**
- Exposes results via **FastAPI + MCP-compatible APIs**

---

## 🚀 Key Features

- ✅ Multiple predefined **high-quality screening strategies**
- ✅ Robust **Playwright automation** (pagination-safe)
- ✅ SQLite database for persistence
- ✅ Composite scoring (quality + valuation + trend + size)
- ✅ Score decay using historical scores
- ✅ Strategy-wise ranking
- ✅ Portfolio construction (Top N)
- ✅ REST APIs for consumption
- ✅ MCP-compatible interface for agentic systems
- ✅ Cron-friendly `/run-all` pipeline

---

## 📁 Project Structure

```text
screener/
├── app/
│   ├── api/                 # FastAPI route handlers
│   ├── tools/               # Screener browser & extractor
│   ├── services/            # Column mapping & normalization
│   ├── db/                  # SQLite DB logic (insert, score, rank, portfolio)
│   ├── strategy/            # Strategy registry
│   ├── mcp/                 # MCP server & client
│   ├── main.py              # FastAPI entrypoint
│
├── data/
│   └── screener.db          # SQLite database
│
├── run_screener.py          # CLI runner (optional)
├── README.md
└── .env

## Supported Screening Strategies
| # | Strategy                  | Description                   |
| - | ------------------------- | ----------------------------- |
| 1 | Quality Golden Cross      | ROCE + Trend confirmation     |
| 2 | High Quality Compounders  | Strong ROCE + growth          |
| 3 | Quality Value             | Low PE + High ROCE            |
| 4 | Largecap Quality Leaders  | Stable large caps             |
| 5 | Midcap Quality Growth     | Growth + quality midcaps      |
| 6 | Debt-Free Cash Generators | Zero/low debt companies       |
| 7 | Consistent Earnings       | Low volatility earnings       |
| 8 | RARP                      | High ROCE at reasonable price |


Setup Instructions
1️⃣ Clone & create virtualenv
git clone <repo-url>
cd screener
python -m venv .venv
source .venv/bin/activate

2️⃣ Install dependencies
pip install -r requirements.txt
playwright install chromium

3️⃣ Configure environment variables

Create .env file:

SCREENER_EMAIL=your_email@example.com
SCREENER_PASSWORD=your_password

4️⃣ Initialize Database
python app/db/init_db.py

5️⃣ Start API server
uvicorn app.main:app --reload


API will be available at:

http://127.0.0.1:8000

🔌 API Endpoints
🔹 Health Check
GET /health

🔹 List Available Strategies
GET /strategies

🔹 Run One Strategy (Heavy Operation)
POST /run
Content-Type: application/json

{
  "strategy_number": 5
}


Runs:

Screener query

Extraction

Scoring

Decay

Ranking

Score history snapshot

⚠️ Use sparingly

🔹 Run All Strategies (Scheduled Use)
POST /run-all


Used by:

Cron jobs

Nightly batch runs

🔹 Build Portfolio (Top-N)
POST /portfolio/build
Content-Type: application/json

{
  "strategy_number": 5,
  "top_n": 10
}


Writes portfolio to DB.

🔹 Fetch Latest Portfolio (FAST, SAFE)
GET /portfolio/latest?strategy_number=5


Recommended for:

Dashboards

AI agents

Analysis pipelines

🧮 Scoring System (High Level)

Each stock gets:

Composite Score

ROCE

PE (penalized if expensive)

Trend (DMA50 > DMA200)

Market Cap (penalizes nano/micro caps)

Decayed Score

Uses historical scores

Penalizes inconsistency

Strategy Rank

Based on decayed score

🗄️ Database Tables (Key)

stocks – raw fundamentals

stock_scores – current scores

stock_score_history – historical snapshots

portfolios – Top-N strategy portfolios

⏰ Scheduling (Recommended)
Daily Cron Job
crontab -e

0 2 * * * /usr/bin/curl -X POST http://127.0.0.1:8000/run-all >> ~/screener.log 2>&1


Runs all strategies nightly.

🤖 MCP Integration (Agentic AI)

APIs are OpenAPI compliant

Can be exposed via MCP server

Other AI systems can:

Discover tools

Call /portfolio/latest

Avoid heavy operations

🧠 Recommended Usage Pattern
Cron → /run-all → DB
AI Agent → /portfolio/latest → Analysis

⚠️ Notes & Warnings

Screener.in is a third-party site – avoid excessive frequency

/run and /run-all are heavy operations

Prefer /portfolio/latest for consumption

Use headless=False for Playwright debugging

🛣️ Roadmap (Optional Enhancements)

API key protection

Email / Slack alerts

Postgres migration

Vector DB for qualitative notes

Portfolio backtesting

Web UI dashboard

👨‍💻 Author Notes

This system is designed like a professional quant research backend:

Deterministic

Auditable

Agent-friendly

Extendable