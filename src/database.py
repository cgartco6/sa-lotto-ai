import sqlite3
import pandas as pd
from typing import Dict, List
from src.config import Config
import os

class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_tables()
    
    def _init_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS draws (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game TEXT NOT NULL,
                    draw_id INTEGER,
                    draw_date TEXT,
                    numbers TEXT,
                    bonus_ball INTEGER,
                    jackpot_amount REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(game, draw_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game TEXT,
                    prediction_date TEXT,
                    top13 TEXT,
                    top6 TEXT,
                    model_version TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wheel_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game TEXT,
                    wheel_tickets TEXT,
                    monte_carlo_hit_prob REAL,
                    actual_matches INTEGER,
                    draw_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def insert_draw(self, game: str, draw_data: Dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO draws (game, draw_id, draw_date, numbers, bonus_ball, jackpot_amount)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (game, draw_data['draw_id'], draw_data['draw_date'],
                  ','.join(map(str, draw_data['numbers'])), draw_data.get('bonus_ball'),
                  draw_data.get('jackpot_amount', 0)))
    
    def get_historical_draws(self, game: str, limit: int = 200) -> pd.DataFrame:
        query = "SELECT draw_date, numbers, bonus_ball, jackpot_amount FROM draws WHERE game = ? ORDER BY draw_date DESC LIMIT ?"
        df = pd.read_sql_query(query, sqlite3.connect(self.db_path), params=(game, limit))
        df['numbers'] = df['numbers'].apply(lambda x: [int(n) for n in x.split(',')])
        return df
    
    def save_prediction(self, game: str, top13: List[int], top6: List[int], model_version: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO predictions (game, prediction_date, top13, top6, model_version)
                VALUES (?, date('now'), ?, ?, ?)
            """, (game, ','.join(map(str, top13)), ','.join(map(str, top6)), model_version))
