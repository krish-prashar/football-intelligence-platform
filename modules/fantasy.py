import pandas as pd
from modules.database import Player, SessionLocal


def load_players_from_db():
    db = SessionLocal()
    players = db.query(Player).all()
    db.close()

    return pd.DataFrame([{
        "player": p.name,
        "position": p.position,
        "cost": p.cost,
        "expected_points": p.expected_points
    } for p in players])


def optimize_team(budget=83.0):
    df = load_players_from_db()

    df["value"] = df["expected_points"] / df["cost"]
    df = df.sort_values("value", ascending=False)

    team = []
    total_cost = 0
    position_limits = {"GK": 1, "DF": 3, "MF": 3, "FW": 3}
    position_count = {"GK": 0, "DF": 0, "MF": 0, "FW": 0}

    for _, player in df.iterrows():
        pos = player["position"]
        if (total_cost + player["cost"] <= budget and
                len(team) < 11 and
                position_count[pos] < position_limits[pos]):
            team.append(player)
            total_cost += player["cost"]
            position_count[pos] += 1

    result = pd.DataFrame(team)[["player", "position", "cost", "expected_points"]]
    return result, round(total_cost, 1)