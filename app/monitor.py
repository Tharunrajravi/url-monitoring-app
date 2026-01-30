import time
import requests
import os
from database import get_connection

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))

def check_urls():
    while True:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, url FROM urls")
        urls = cur.fetchall()

        for url_id, url in urls:
            try:
                start = time.time()
                response = requests.get(url, timeout=5)
                elapsed = (time.time() - start) * 1000
                status = "UP" if response.status_code == 200 else "DOWN"
            except Exception:
                status = "DOWN"
                elapsed = 0

            cur.execute(
                "UPDATE urls SET status=?, response_time=? WHERE id=?",
                (status, round(elapsed, 2), url_id)
            )

        conn.commit()
        conn.close()
        time.sleep(CHECK_INTERVAL)

