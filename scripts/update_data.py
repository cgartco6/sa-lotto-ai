from src.scraper.run_scraper import scrape_all

def update_data():
    print("Updating historical data...")
    scrape_all(["Lotto", "Lotto Plus 1", "Lotto Plus 2", "Powerball"])
    print("Data update complete.")

if __name__ == "__main__":
    update_data()
