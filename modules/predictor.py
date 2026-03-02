import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from modules.database import Match, SessionLocal


def load_matches_from_db():
    """Load all matches from the database into a pandas DataFrame"""
    db = SessionLocal()
    matches = db.query(Match).all()
    db.close()

    return pd.DataFrame([{
        "home_score": m.home_score,
        "away_score": m.away_score,
    } for m in matches])


def prepare_data(df):
    """Add features and result labels the model needs to learn from"""
    df = df.dropna()

    df["home_goals_avg"] = df["home_score"].rolling(5, min_periods=1).mean()
    df["away_goals_avg"] = df["away_score"].rolling(5, min_periods=1).mean()

    def get_result(row):
        if row["home_score"] > row["away_score"]:
            return "H"
        elif row["home_score"] < row["away_score"]:
            return "A"
        else:
            return "D"

    df["result"] = df.apply(get_result, axis=1)
    return df.dropna()


def train_model():
    """Train a Random Forest model on historical match data"""
    df = load_matches_from_db()
    df = prepare_data(df)

    X = df[["home_goals_avg", "away_goals_avg"]]
    y = df["result"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model Accuracy: {acc:.2%}")

    return model, list(model.classes_)


def predict(model, home_avg, away_avg):
    """Use trained model to predict a single match"""
    result = model.predict([[home_avg, away_avg]])[0]
    proba = model.predict_proba([[home_avg, away_avg]])[0]
    return result, proba.tolist()