from src.scraper import LottoScraper, PowerballScraper
from src.database import Database
import time

def scrape_all(games: list):
    db = Database()
    scrapers = {
        "Lotto": LottoScraper(),
        "Lotto Plus 1": LottoScraper(),
        "Lotto Plus 2": LottoScraper(),
        "Powerball": PowerballScraper()
    }
    for game in games:
        print(f"Scraping {game}...")
        scraper = scrapers[game]
        for draw_id in range(1, 300):
            data = scraper.fetch_results(draw_id)
            if not data or 'drawId' not in data:
                break
            parsed = scraper.parse_draw_data(data)
            db.insert_draw(game, parsed)
            time.sleep(0.5)
    print("Scraping complete.")

if __name__ == "__main__":
    scrape_all(["Lotto", "Lotto Plus 1", "Lotto Plus 2", "Powerball"])
