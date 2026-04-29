# SA Lotto AI – Ultimate System

Fully automated AI-powered prediction & optimization for South African Lotto, Lotto Plus 1/2, Powerball.

## Features
- Automated scraping of real historical results (2+ years)
- Multiple AI models: LSTM, XGBoost, Prophet, Bayesian MCMC
- Ensemble predictions combining all models
- Advanced wheel optimization: Genetic Algorithm, Monte Carlo coverage
- Jackpot time-series forecasting (SARIMA/GARCH, Holt-Winters)
- Reinforcement learning for optimal betting strategy
- Interactive Streamlit dashboard
- Telegram alerts for jackpot build-ups and predictions
- Performance tracking & hit probability estimation

## Quick Start
```bash
pip install -r requirements.txt
cp .env.example .env  # add your Telegram token
python scripts/init_db.py
python src/scraper/run_scraper.py
python scripts/train_models.py
streamlit run src/dashboard/app.py
python scripts/run_scheduler.py   # for alerts
