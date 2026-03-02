import plotly.express as px
import pandas as pd


def load_transfers():
    data = {
        "player": ["Mbappe", "Neymar", "Coutinho", "Griezmann", "Lukaku",
                   "Pogba", "Dembele", "Hazard", "De Ligt", "Felix"],
        "fee_millions": [180, 222, 142, 120, 115, 105, 105, 100, 85, 126],
        "position": ["FW", "FW", "MF", "FW", "FW", "MF", "FW", "MF", "DF", "FW"],
        "league": ["Ligue 1", "Ligue 1", "La Liga", "La Liga", "Serie A",
                   "Premier League", "La Liga", "La Liga", "Serie A", "La Liga"]
    }
    return pd.DataFrame(data)


def plot_top_transfers(df):
    fig = px.bar(
        df.nlargest(10, "fee_millions"),
        x="player",
        y="fee_millions",
        color="position",
        title="Most Expensive Transfers Ever"
    )
    return fig


def plot_by_league(df):
    grouped = df.groupby("league")["fee_millions"].sum().reset_index()
    fig = px.pie(
        grouped,
        values="fee_millions",
        names="league",
        title="Transfer Spending by League"
    )
    return fig