import streamlit as st
from modules.predictor import train_model, predict
from modules.dashboard import plot_top_scorers, plot_team_goals
from modules.transfers import load_transfers, plot_top_transfers, plot_by_league
from modules.fantasy import optimize_team

# Page config
st.set_page_config(
    page_title="⚽ Football Intelligence Platform",
    layout="wide"
)

# Cache the model so it only trains once
@st.cache_resource
def load_model():
    return train_model()

# Header
st.title("⚽ Football Intelligence Platform")
st.caption("Match Prediction • Player Stats • Transfer Analysis • Fantasy Optimization")
st.divider()

# Sidebar navigation
page = st.sidebar.selectbox("Choose a Module", [
    "🔮 Match Predictor",
    "📊 Player Dashboard",
    "💰 Transfer Analyzer",
    "🏆 Fantasy Optimizer"
])

# ---- MATCH PREDICTOR ----
if page == "🔮 Match Predictor":
    st.header("🔮 Match Outcome Predictor")
    st.write("Uses a Random Forest model trained on real Premier League data to predict match results.")
    st.divider()

    with st.spinner("Training model on Premier League data..."):
        model, classes = load_model()

    st.success("✅ Model trained and ready!")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Home Team")
        home_avg = st.slider("Average Goals Scored (last 5 games)", 0.0, 4.0, 1.5, step=0.1)
    with col2:
        st.subheader("Away Team")
        away_avg = st.slider("Average Goals Scored (last 5 games) ", 0.0, 4.0, 1.2, step=0.1)

    st.divider()

    if st.button("🔮 Predict Result", use_container_width=True):
        result, proba = predict(model, home_avg, away_avg)
        labels = {"H": "🏠 Home Win", "A": "✈️ Away Win", "D": "🤝 Draw"}

        st.subheader(f"Prediction: {labels[result]}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Home Win", f"{proba[list(classes).index('H')]:.1%}" if 'H' in classes else "N/A")
        col2.metric("Draw", f"{proba[list(classes).index('D')]:.1%}" if 'D' in classes else "N/A")
        col3.metric("Away Win", f"{proba[list(classes).index('A')]:.1%}" if 'A' in classes else "N/A")

        st.bar_chart(dict(zip(classes, proba)))

# ---- PLAYER DASHBOARD ----
elif page == "📊 Player Dashboard":
    st.header("📊 Player Performance Dashboard")
    st.write("Player stats and team goal data pulled directly from PostgreSQL.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_top_scorers(), use_container_width=True)
    with col2:
        st.plotly_chart(plot_team_goals(), use_container_width=True)

# ---- TRANSFER ANALYZER ----
elif page == "💰 Transfer Analyzer":
    st.header("💰 Transfer Market Analyzer")
    st.write("Breakdown of the most expensive transfers in football history.")
    st.divider()

    df = load_transfers()

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_top_transfers(df), use_container_width=True)
    with col2:
        st.plotly_chart(plot_by_league(df), use_container_width=True)

    st.divider()
    st.subheader("Raw Transfer Data")
    st.dataframe(df, use_container_width=True)

# ---- FANTASY OPTIMIZER ----
elif page == "🏆 Fantasy Optimizer":
    st.header("🏆 Fantasy Team Optimizer")
    st.write("Picks the best 11-player team within your budget using a value optimization algorithm.")
    st.divider()

    budget = st.slider("Your Budget (£M)", 80.0, 100.0, 83.0, step=0.5)

    if st.button("🏆 Build My Team", use_container_width=True):
        team, total = optimize_team(budget)

        col1, col2 = st.columns(2)
        col1.metric("Total Cost", f"£{total}M")
        col2.metric("Players Selected", len(team))

        st.divider()
        st.subheader("Your Optimized Team")
        st.dataframe(team, use_container_width=True)

        st.divider()
        st.subheader("Team by Position")
        for pos in ["GK", "DF", "MF", "FW"]:
            pos_players = team[team["position"] == pos]
            if len(pos_players) > 0:
                st.write(f"**{pos}**")
                st.dataframe(pos_players, use_container_width=True)