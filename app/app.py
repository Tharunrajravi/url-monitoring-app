from flask import Flask, render_template, request, redirect
import threading
import logging
from database import init_db, get_connection
from monitor import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)
init_db()

logging.info("Starting background monitor thread")
monitor_thread = threading.Thread(target=check_urls, daemon=True)
monitor_thread.start()

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        url = request.form["url"]
        logging.info(f"Adding URL: {url}")
        cur.execute(
            "INSERT INTO urls (url, status, response_time) VALUES (?, ?, ?)",
            (url, "PENDING", 0)
        )
        conn.commit()
        return redirect("/")

    cur.execute("SELECT * FROM urls")
    urls = cur.fetchall()
    conn.close()
    return render_template("index.html", urls=urls)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

