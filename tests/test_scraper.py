import unittest
from src.scraper.lotto_scraper import LottoScraper

class TestScraper(unittest.TestCase):
    def test_fetch(self):
        scraper = LottoScraper()
        data = scraper.fetch_results(draw_id=1)
        self.assertIsNotNone(data)

if __name__ == "__main__":
    unittest.main()
