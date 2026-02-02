from flask import Flask, render_template, request, redirect
import threading
import logging

from database import init_db, get_connection
from monitor import check_urls, check_single_url

# ----------------------------
# Logging configuration
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ----------------------------
# Flask app initialization
# ----------------------------
app = Flask(__name__)

# Initialize database
init_db()

# ----------------------------
# Start background monitoring thread
# ----------------------------
logging.info("Starting background URL monitoring thread")
monitor_thread = threading.Thread(target=check_urls, daemon=True)
monitor_thread.start()

# ----------------------------
# Main dashboard route
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":
        url = request.form["url"].strip()
        logging.info(f"Adding URL: {url}")

        # 🔥 Immediate check (NO 30s wait)
        status, response_time = check_single_url(url)

        cur.execute(
            "INSERT INTO urls (url, status, response_time) VALUES (?, ?, ?)",
            (url, status, response_time)
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cur.execute("SELECT * FROM urls")
    urls = cur.fetchall()
    conn.close()

    return render_template("index.html", urls=urls)

# ----------------------------
# Health check endpoint
# ----------------------------
@app.route("/health")
def health():
    return {"status": "ok"}

# ----------------------------
# App entry point
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

