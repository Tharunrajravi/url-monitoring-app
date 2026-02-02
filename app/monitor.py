import time
import requests
import os
from database import get_connection

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 30))

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

        if response.status_code > 200 and response.status_code < 500:
            status = "UP"
        else:
            status = "DOWN"

    except Exception:
        status = "DOWN"
        elapsed = 0

    return status, round(elapsed, 2)


def check_urls():
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

