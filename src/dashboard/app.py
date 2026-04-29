import streamlit as st
from src.config import Config
import src.dashboard.pages.predictions as predictions
import src.dashboard.pages.statistics as statistics
import src.dashboard.pages.wheels as wheels
import src.dashboard.pages.performance as performance
import src.dashboard.pages.jackpot_analysis as jackpot_analysis

st.set_page_config(page_title="SA Lotto AI Ultimate", layout="wide")
st.title("🎰 South African Lotto AI – Ultimate System")
st.markdown(f"Your fixed numbers: {Config.YOUR_NUMBERS}")

if 'game' not in st.session_state:
    st.session_state['game'] = 'Lotto'

page = st.sidebar.selectbox("Navigation", ["Predictions", "Statistics", "Wheels", "Performance", "Jackpot Analysis"])

if page == "Predictions":
    predictions.show()
elif page == "Statistics":
    statistics.show()
elif page == "Wheels":
    wheels.show()
elif page == "Performance":
    performance.show()
elif page == "Jackpot Analysis":
    jackpot_analysis.show()
