# 1️⃣ Base image (small, stable)
FROM python:3.10-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy dependencies first (layer caching)
COPY requirements.txt .

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy application code
COPY app/ app/

# 6️⃣ Expose application port
EXPOSE 5000

# 7️⃣ Environment defaults (can be overridden)
ENV CHECK_INTERVAL=30
ENV DB_NAME=/app/urls.db

# 8️⃣ Start application
CMD ["python", "app/app.py"]
