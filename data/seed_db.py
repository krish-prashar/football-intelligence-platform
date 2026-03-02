import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from modules.database import Match, Player, SessionLocal, create_tables
from dotenv import load_dotenv

load_dotenv()


def seed_matches():
    API_KEY = os.getenv("API_KEY")
    headers = {"X-Auth-Token": API_KEY}
    url = "https://api.football-data.org/v4/competitions/PL/matches"

    print("Fetching matches from API...")
    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)

    data = response.json()
    db = SessionLocal()

    count = 0
    for match in data["matches"]:
        score = match["score"]["fullTime"]
        if score["home"] is not None:
            m = Match(
                home_team=match["homeTeam"]["name"],
                away_team=match["awayTeam"]["name"],
                home_score=score["home"],
                away_score=score["away"],
                date=match["utcDate"][:10]
            )
            db.add(m)
            count += 1

    db.commit()
    db.close()
    print(f"Saved {count} matches!")


def seed_players():
    db = SessionLocal()

    players = [
        Player(name="Salah", team="Liverpool", position="FW",
               goals=18, assists=6, cost=13.0, expected_points=9.5),
        Player(name="De Bruyne", team="Man City", position="MF",
               goals=8, assists=12, cost=10.5, expected_points=8.2),
        Player(name="Haaland", team="Man City", position="FW",
               goals=25, assists=3, cost=14.0, expected_points=10.2),
        Player(name="Saka", team="Arsenal", position="MF",
               goals=12, assists=9, cost=8.5, expected_points=7.8),
        Player(name="Alisson", team="Liverpool", position="GK",
               goals=0, assists=0, cost=5.5, expected_points=6.1),
        Player(name="Trippier", team="Newcastle", position="DF",
               goals=2, assists=7, cost=6.5, expected_points=7.0),
        Player(name="Raya", team="Arsenal", position="GK",
               goals=0, assists=0, cost=5.0, expected_points=5.8),
        Player(name="Alexander-Arnold", team="Liverpool", position="DF",
               goals=3, assists=8, cost=7.5, expected_points=7.2),
        Player(name="Watkins", team="Aston Villa", position="FW",
               goals=14, assists=6, cost=8.0, expected_points=7.5),
        Player(name="Rashford", team="Man United", position="FW",
               goals=7, assists=4, cost=9.0, expected_points=6.5),
    ]

    db.add_all(players)
    db.commit()
    db.close()
    print(f"Saved {len(players)} players!")


if __name__ == "__main__":
    print("Creating tables...")
    create_tables()
    print("Tables created!")
    seed_matches()
    seed_players()
    print("Done! Database is ready.")