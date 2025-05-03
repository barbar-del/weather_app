A containerized Flask application that:

- Fetches a 7-day weather forecast for a specified location via the Visual Crossing Weather API
- Logs search history to a JSON file with timestamps and resolved locations
- Exposes Prometheus metrics for request latency, search counts by city, and external API latency

---

## Prerequisites

- **Docker** installed
- **Visual Crossing Weather API key**:
  1. Sign up or log in at https://www.visualcrossing.com/
  2. Copy your API key from your profile or API settings

---

## Build the Docker Image

```bash
docker build -t flask-weather-app .
```

---

## Run the Container

### 1. Using a Host Environment Variable (recommended)

```bash
docker run -d \
  --name weather-app \
  -p 5000:5000 \
  -e WEATHER_API_KEY="$WEATHER_API_KEY" \
  flask-weather-app
```

### 2. Hard‑coding the API Key (not recommended)

```bash
docker run -d \
  --name weather-app \
  -p 5000:5000 \
  -e WEATHER_API_KEY="YOUR_ACTUAL_API_KEY" \
  flask-weather-app
```

---

## Access the Application

- **Web UI:** http://localhost:5000/
- **Prometheus metrics:** http://localhost:5000/metrics

---

## Project Layout

```
root/
├── Dockerfile            # Builds the container (uses Python 3.10-slim, adds non-root user, installs deps)
├── README.md             # This documentation file
└── flask_weather_app/    # Application package
    ├── __init__.py       # Package marker
    ├── app.py            # Flask app entrypoint
    ├── history.py        # Search‐history logic
    ├── requirements.txt  # Python dependencies
    ├── static/
    │   └── css/style.css # Styling for forms and tables
    ├── templates/        # Jinja2 HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── results.html
    │   └── history.html
    └── search_history.json  # Auto-created at runtime