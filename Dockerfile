FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app

# --- System deps required by Playwright Chromium ---
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libxshmfence1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libdrm2 \
    libglib2.0-0 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libxcb1 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxss1 \
    libxcursor1 \
    libxi6 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# --- Python deps ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🔥 THIS IS THE CRITICAL LINE 🔥
RUN playwright install --with-deps

# --- App code ---
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
