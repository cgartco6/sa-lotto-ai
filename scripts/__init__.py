from src.database import Database

if __name__ == "__main__":
    db = Database()
    print(f"Database initialized at {db.db_path}")
