import plotly.express as px
import pandas as pd
from modules.database import Player, Match, SessionLocal


def plot_top_scorers():
    """Bar chart of top 10 scorers from the players table"""
    db = SessionLocal()
    players = db.query(Player).order_by(Player.goals.desc()).limit(10).all()
    db.close()

    df = pd.DataFrame([{
        "player": p.name,
        "goals": p.goals,
        "team": p.team
    } for p in players])

    fig = px.bar(df, x="player", y="goals", color="team",
                 title="Top 10 Scorers")
    return fig


def plot_team_goals():
    """Bar chart of which teams score the most at home"""
    db = SessionLocal()
    matches = db.query(Match).all()
    db.close()

    df = pd.DataFrame([{
        "team": m.home_team,
        "goals": m.home_score
    } for m in matches])

    grouped = df.groupby("team")["goals"].sum().reset_index()

    fig = px.bar(
        grouped.nlargest(10, "goals"),
        x="team", y="goals",
        title="Top 10 Teams by Home Goals"
    )
    return fig