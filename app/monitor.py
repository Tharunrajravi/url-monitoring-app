import time
import requests
import os
import logging
from database import get_connection

# ----------------------------
# Configuration
# ----------------------------
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------
# Check a single URL (used immediately on add)
# ----------------------------
def check_single_url(url):
    try:
        start = time.time()

        response = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True
        )

        elapsed = (time.time() - start) * 1000

        # ✅ Correct logic
        if response.status_code >= 200 and response.status_code < 500:
            status = "UP"
        else:
            status = "DOWN"

    except Exception as e:
        logging.warning(f"Error checking {url}: {e}")
        status = "DOWN"
        elapsed = 0

    return status, round(elapsed, 2)

# ----------------------------
# Background monitoring loop
# ----------------------------
def check_urls():
    logging.info("URL monitoring thread started")

    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, url FROM urls")
        urls = cur.fetchall()

        for url_id, url in urls:
            status, response_time = check_single_url(url)

            cur.execute(
                "UPDATE urls SET status=?, response_time=? WHERE id=?",
                (status, response_time, url_id)
            )

        conn.commit()
        conn.close()

        time.sleep(CHECK_INTERVAL)

