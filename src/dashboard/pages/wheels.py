import streamlit as st
import pandas as pd
from src.wheel.genetic_optimizer import GeneticWheelOptimizer
from src.monte_carlo.simulator import MonteCarloSimulator
from src.config import Config

def show():
    st.header("🎯 Wheel Optimization (Genetic Algorithm)")
    game = st.selectbox("Game", ["Lotto", "Lotto Plus 1", "Lotto Plus 2", "Powerball"], key="wheel_game")
    # For demo, use your numbers plus common ones
    top13 = Config.YOUR_NUMBERS + [1,5,8,12,22,28,35]
    top13 = list(set(top13))[:13]
    st.write(f"Number pool (Top 13): {top13}")
    target_coverage = st.slider("Target pair coverage", 0.7, 0.99, 0.95)
    ga = GeneticWheelOptimizer(top13, line_length=6, target_coverage=target_coverage,
                               population_size=50, generations=30)
    if st.button("Run GA Optimization"):
        with st.spinner("Evolving optimal wheel..."):
            wheel = ga.get_optimal_wheel()
        coverage = ga.calculate_pair_coverage(wheel)
        st.success(f"Found {len(wheel)} tickets with {coverage:.2%} pair coverage")
        st.dataframe(pd.DataFrame(wheel, columns=[f"Num{i+1}" for i in range(6)]))
        sim = MonteCarloSimulator(game)
        hit_prob = sim.hit_probability(wheel, n_simulations=50000)
        st.metric("Estimated hit probability (≥4 matches)", f"{hit_prob:.2%}")
