import schedule
import time
import logging
import asyncio
from pathlib import Path
from src.scraper import TelegramScraper
from src.database import Database

def run_job():
    try:
        db = Database()
        scraper = TelegramScraper()

        # Process groups asynchronously
        asyncio.run(scraper.process_groups())

    except Exception as e:
        logging.error(f"Error in job: {e}")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Schedule job every 5 minutes
    schedule.every(5).minutes.do(run_job)

    # Run immediately first time
    run_job()

    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()