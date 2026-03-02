# ⚽ Football Intelligence Platform

A full-stack data science platform that combines match outcome prediction, player performance dashboards, transfer market analysis, and fantasy team optimization — all built with Python.

**Live Demo:** (https://football-intelligence-platform-vm28pebeczzbmdmq7tlzsa.streamlit.app/)  
**Built by:** Krish Prashar — 2nd Year CS Student at Wilfrid Laurier University

---

## What It Does

**🔮 Match Predictor** — Uses a Random Forest machine learning model trained on real Premier League match data to predict whether the home team wins, loses, or draws.

**📊 Player Dashboard** — Visualizes top scorers and team goal stats pulled directly from a PostgreSQL database.

**💰 Transfer Analyzer** — Analyzes the most expensive transfers in football history, broken down by position and league.

**🏆 Fantasy Optimizer** — Picks the best 11-player fantasy team within a given budget using a value optimization algorithm (expected points per £).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Machine Learning | scikit-learn (Random Forest) |
| Data Processing | pandas, NumPy |
| Visualizations | Plotly |
| REST API | FastAPI |
| Database | PostgreSQL (via SQLAlchemy ORM) |
| Frontend | Streamlit |
| Containerization | Docker |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Deployment | Streamlit Cloud + Supabase |

---

## Project Structure
```
football-intelligence-platform/
│
├── modules/
│   ├── database.py       # PostgreSQL models and connection
│   ├── predictor.py      # Match outcome ML model
│   ├── dashboard.py      # Player and team visualizations
│   ├── transfers.py      # Transfer market analysis
│   └── fantasy.py        # Fantasy team optimizer
│
├── data/
│   └── seed_db.py        # Fetches real data from API and seeds DB
│
├── tests/
│   ├── test_predictor.py # Unit tests for ML module
│   └── test_fantasy.py   # Unit tests for fantasy optimizer
│
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI/CD pipeline
│
├── api.py                # FastAPI backend with 4 endpoints
├── app.py                # Streamlit frontend
└── requirements.txt
```

---

## How To Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/krish-prashar/football-intelligence-platform.git
cd football-intelligence-platform
```

**2. Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root folder:
```
DATABASE_URL=postgresql://admin:password@localhost:5432/football
API_KEY=your_football_data_org_api_key
```

**5. Start PostgreSQL with Docker**
```bash
docker start football-db
```

**6. Seed the database**
```bash
python3 data/seed_db.py
```

**7. Run the Streamlit app**
```bash
streamlit run app.py
```

**8. Or run the FastAPI backend**
```bash
uvicorn api:app --reload
```
Then visit **localhost:8000/docs** for the interactive API docs.

---

## Running Tests
```bash
pytest tests/ -v
```

All tests run automatically on every push via GitHub Actions.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/matches` | Returns 20 most recent matches |
| GET | `/players` | Returns all players |
| GET | `/predict?home_avg=1.5&away_avg=1.2` | Predicts match outcome |
| GET | `/fantasy?budget=83.0` | Returns optimized fantasy team |

---

## Data Sources

- **football-data.org** — Real Premier League match results (free API)
- **StatsBomb Open Data** — Detailed player statistics

---

## Author

**Krish Prashar**  
2nd Year Computer Science @ Wilfrid Laurier University  
AWS Certified Cloud Practitioner  
[GitHub](https://github.com/krish-prashar) | [LinkedIn](https://www.linkedin.com/in/krish-prashar-67fr/)
