# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- System deps ----------
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  && rm -rf /var/lib/apt/lists/*

# ---------- Working directory ----------
WORKDIR /app

# ---------- Install Python deps ----------
COPY pyproject.toml .
COPY . .
RUN pip install --no-cache-dir .

# ---------- Copy application code ----------
COPY . .

# ---------- Expose service port ----------
EXPOSE 8000

# ---------- Healthcheck (optional but recommended) ----------
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
  CMD curl -f http://localhost:8000/health || exit 1

# ---------- Run ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
