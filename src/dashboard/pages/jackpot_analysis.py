import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import Database
from src.analysis.jackpot_analyzer import JackpotAnalyzer

def show():
    st.header("💰 Jackpot Analysis & Predictions")
    game = st.selectbox("Game", ["Lotto", "Lotto Plus 1", "Lotto Plus 2", "Powerball"], key="jackpot_game")
    db = Database()
    draws = db.get_historical_draws(game, 300)
    if len(draws) == 0:
        st.warning("No data available.")
        return
    ja = JackpotAnalyzer(game)
    series = ja.prepare_jackpot_series(draws)
    st.subheader("Historical Jackpot Trend")
    fig = px.line(x=draws['draw_date'], y=series, title=f"{game} – Jackpot Over Time")
    st.plotly_chart(fig, use_container_width=True)
    stats = ja.analyze_jackpot_history(draws)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average", f"R{stats['average']:,.0f}")
    col2.metric("Last", f"R{stats['last_jackpot']:,.0f}")
    col3.metric("Max", f"R{stats['maximum']:,.0f}")
    col4.metric("Rollovers", stats['rollover_count'])
    st.subheader("Top 6 Future Jackpot Predictions")
    with st.spinner("Training models..."):
        top6 = ja.get_top6_jackpot_predictions(series, future_steps=6)
    for i, val in enumerate(top6, 1):
        st.metric(f"Prediction {i}", f"R{val:,.0f}")
    is_anomaly = ja.detect_jackpot_anomaly(series.iloc[-1], series[:-1])
    if is_anomaly:
        st.error("🚨 Anomaly detected – high chance of payout soon!")
    else:
        st.info("Jackpot within normal range.")
    st.subheader("Full Forecast (Ensemble)")
    preds = ja.predict_future_jackpots(steps=10)
    forecast_df = pd.DataFrame({
        "Step": range(1,11),
        "Ensemble": preds["ensemble"],
        "Linear Reg": preds["linear_regression"],
        "Random Forest": preds["random_forest"]
    })
    st.dataframe(forecast_df)
