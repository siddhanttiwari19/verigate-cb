FROM python:3.12-slim

WORKDIR /app

# Install deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Non-root user — don't run production containers as root.
# Must chown /app before switching, since WORKDIR/COPY above ran as root
# and the appuser otherwise has no write permission to generate data here.
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Generate the demo dataset at build time so the container is runnable
# out of the box; in real deployment, mount a volume with real data
# instead and skip this step.
RUN python app/data_gen.py

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]