import streamlit as st
import pandas as pd
from src.database import Database
from src.analysis.hybrid_predictor import HybridPredictor
from src.config import Config

def show():
    st.header("🔮 AI Predictions (Hybrid Ensemble)")
    game = st.session_state.get('game', 'Lotto')
    db = Database()
    draws = db.get_historical_draws(game, 200)
    max_num = Config.GAME_PARAMS[game]["main_max"]
    predictor = HybridPredictor(game, max_num)
    if st.button("Run Full Hybrid Analysis", key="pred_btn"):
        with st.spinner("Running LSTM, XGBoost, Bayesian, Prophet, RL..."):
            results = predictor.analyze_all(draws)
        col1, col2 = st.columns(2)
        col1.metric("Top 13 Numbers", ", ".join(map(str, results['top13'][:13])))
        col2.metric("Top 6 Recommended", ", ".join(map(str, results['top6'])))
        st.subheader("Jackpot Forecast")
        st.line_chart(pd.Series(results['jackpot_forecast']))
        if results['jackpot_anomaly']:
            st.error("🚨 JACKPOT ANOMALY DETECTED!")
        st.info(f"🤖 RL Bet Advice: {results['bet_advice']['advice']}")
        st.write("**Frequent Pairs:**", results['frequent_pairs'][:5])
        st.write("**Jackpot Top6 Predictions:**", results['jackpot_top6'])
