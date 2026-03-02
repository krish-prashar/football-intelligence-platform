from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from modules.database import get_db, Match, Player
from modules.predictor import train_model, predict
from modules.fantasy import optimize_team

app = FastAPI(
    title="Football Intelligence API",
    description="Match predictions, player stats, and fantasy optimization",
    version="1.0.0"
)

print("Training model...")
model, classes = train_model()
print("Model ready!")


@app.get("/")
def root():
    return {"message": "Football Intelligence API is running!"}


@app.get("/matches")
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(Match).limit(20).all()
    return [
        {
            "home_team": m.home_team,
            "away_team": m.away_team,
            "score": f"{m.home_score} - {m.away_score}",
            "date": m.date
        }
        for m in matches
    ]


@app.get("/players")
def get_players(db: Session = Depends(get_db)):
    players = db.query(Player).all()
    return [
        {
            "name": p.name,
            "team": p.team,
            "position": p.position,
            "goals": p.goals,
            "cost": p.cost
        }
        for p in players
    ]


@app.get("/predict")
def predict_match(home_avg: float = 1.5, away_avg: float = 1.2):
    result, proba = predict(model, home_avg, away_avg)
    return {
        "prediction": result,
        "meaning": {"H": "Home Win", "A": "Away Win", "D": "Draw"}[result],
        "probabilities": dict(zip(classes, [round(p, 3) for p in proba]))
    }


@app.get("/fantasy")
def get_fantasy_team(budget: float = 83.0):
    team, total = optimize_team(budget)
    return {
        "budget": budget,
        "total_cost": total,
        "team": team.to_dict(orient="records")
    }