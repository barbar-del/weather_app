# Use a minimal Python runtime
FROM python:3.10-slim

# Don’t buffer logs, set FLASK entrypoint
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=flask_weather_app/app.py \
    # Point Python at your package so `import history` works
    PYTHONPATH=/app/flask_weather_app

# Create an unprivileged user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Set your working directory
WORKDIR /app

# Install only what your app needs
COPY flask_weather_app/requirements.txt ./flask_weather_app/requirements.txt
RUN pip install --no-cache-dir -r flask_weather_app/requirements.txt

# Bring in your application code
COPY flask_weather_app/ ./flask_weather_app/

# Fix permissions so appuser can write the history file
RUN chown -R appuser:appgroup /app && \
    touch flask_weather_app/search_history.json && \
    chown appuser:appgroup flask_weather_app/search_history.json

# Drop root privileges
USER appuser

# Expose Flask’s port
EXPOSE 5000

# Optional: make Docker check that your app is alive
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:5000/ || exit 1

# Launch under Gunicorn; no host‐side vars needed beyond WEATHER_API_KEY
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_weather_app.app:app"]
