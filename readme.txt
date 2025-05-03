A simple Flask web application that retrieves and displays a 7-day weather forecast for a given location using the Visual Crossing Weather API, with search history tracking and Prometheus metrics.

## Features
- Landing page with search bar and buttons for searching and viewing history.
- Search results displayed in a responsive table showing date, max/min temperature, and humidity.
- Search history is logged to a JSON file and can be viewed or downloaded.
- Prometheus metrics endpoint (`/metrics`) exposes:
  - Request latency histogram
  - Search counter by location
  - External API call latency histogram

## Getting Started

### Prerequisites
- Docker installed on your host.
- A Visual Crossing Weather account and API key:
  1. Go to https://www.visualcrossing.com/  
  2. Sign up for a free or paid account.  
  3. Navigate to your profile or API settings to obtain your Weather API key.

### Setup & Build


1. (Optional) Export your API key as an environment variable on the host:
   ```bash
   export WEATHER_API_KEY="your_actual_api_key_here"
   ```
2. Build the Docker image:
   ```bash
   docker build -t flask-weather-app .
   ```

### Running the Container

#### 1. Using a host environment variable (recommended)
```bash
docker run -d \
  -p 5000:5000 \
  --name weather-app \
  -e WEATHER_API_KEY="$WEATHER_API_KEY" \
  flask-weather-app
```

#### 2. Hard-coding your API key inline
```bash
docker run -d \
  -p 5000:5000 \
  --name weather-app \
  -e WEATHER_API_KEY="your_actual_api_key_here" \
  flask-weather-app
```

Once running:
- Visit `http://localhost:5000` in your browser for the app UI.
- Scrape metrics via `http://localhost:5000/metrics` for Prometheus ingestion.

## Project Structure
```
root/
├── Dockerfile
├── README.md
└── flask_weather_app/
    ├── app.py
    ├── history.py
    ├── requirements.txt
    ├── static/css/style.css
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   ├── results.html
    │   └── history.html
    └── search_history.json