import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import Database
from src.analysis.frequency import FrequencyAnalyzer
from src.analysis.pairs import PairAnalyzer

def show():
    st.header("📊 Draw Statistics")
    game = st.selectbox("Game", ["Lotto", "Lotto Plus 1", "Lotto Plus 2", "Powerball"], key="stat_game")
    db = Database()
    draws = db.get_historical_draws(game, 300)
    max_num = 58 if "Lotto" in game else 50
    freq = FrequencyAnalyzer.get_number_frequencies(draws, max_num)
    freq_df = pd.DataFrame(list(freq.items()), columns=["Number", "Frequency"]).sort_values("Number")
    fig = px.bar(freq_df, x="Number", y="Frequency", title=f"Number Frequencies – {game}")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Frequent Pairs")
    pairs = PairAnalyzer.get_frequent_pairs(draws, 20)
    st.dataframe(pd.DataFrame(pairs, columns=["Pair", "Count"]))
