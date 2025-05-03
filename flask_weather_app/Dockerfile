FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=flask_weather_app/app.py

# Create a group and user to run the application
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# Create working directory and set permissions
WORKDIR /app
COPY flask_weather_app/ ./flask_weather_app/

# Install dependencies
RUN pip install --no-cache-dir -r flask_weather_app/requirements.txt && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port for application and metrics
EXPOSE 5000

# Use Gunicorn to run the app with 4 workers
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_weather_app.app:app"]