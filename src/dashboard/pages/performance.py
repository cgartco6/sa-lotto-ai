import streamlit as st
import pandas as pd
from src.database import Database
from src.monte_carlo.simulator import MonteCarloSimulator
from src.config import Config

def show():
    st.header("📈 Performance Tracking")
    db = Database()
    st.subheader("Monte Carlo Sensitivity Analysis")
    game = st.selectbox("Game", ["Lotto", "Powerball"], key="perf_game")
    tickets = st.number_input("Number of tickets per draw", 1, 100, 10)
    sim = MonteCarloSimulator(game)
    if st.button("Run Sensitivity"):
        import numpy as np
        max_num = 58 if "Lotto" in game else 50
        count = 6 if "Lotto" in game else 5
        dummy_wheel = [tuple(np.random.choice(range(1,max_num+1), count, replace=False)) for _ in range(tickets)]
        prob = sim.hit_probability(dummy_wheel, n_simulations=20000)
        st.metric(f"Hit probability (≥{Config.WHEEL_GUARANTEE} matches)", f"{prob:.2%}")
