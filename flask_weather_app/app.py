from flask import Flask, render_template, request, send_file, redirect, url_for, g, Response
import os
import requests
import time
from history import log_search, get_history
from prometheus_client import Histogram, Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')  # Ensure this env var is set
HISTORY_FILE = 'search_history.json'

# Prometheus metrics
REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'Flask request latency in seconds',
    ['method', 'endpoint']
)
SEARCH_COUNTER = Counter(
    'flask_search_requests_total',
    'Total number of search requests',
    ['location']
)
API_LATENCY = Histogram(
    'external_api_latency_seconds',
    'Latency of external weather API calls',
    ['location']
)

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def record_latency(response):
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        REQUEST_LATENCY.labels(request.method, request.path).observe(elapsed)
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            return redirect(url_for('results', loc=location))
    return render_template('index.html')

@app.route('/results')
def results():
    raw_loc = request.args.get('loc')
    SEARCH_COUNTER.labels(raw_loc).inc()
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{raw_loc}/next7days?unitGroup=metric&elements=datetime%2Ctempmax%2Ctempmin%2Chumidity&"
        f"include=days%2Cfcst&key={API_KEY}&options=stnslevel1%2Cnonulls&contentType=json"
    )
    try:
        with API_LATENCY.labels(raw_loc).time():
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        data = response.json()
        days = data.get('days', [])
        resolved = data.get('resolvedAddress', raw_loc)
        # Log both raw input and resolved city
        log_search(raw_loc, HISTORY_FILE, resolved)
        if not days:
            error = f"No weather data found for '{resolved}'."
            return render_template('results.html', days=[], location=resolved, error=error)
        return render_template('results.html', days=days, location=resolved)
    except requests.RequestException:
        error = f"Could not retrieve weather for '{raw_loc}'. Please check the location and try again."
        return render_template('results.html', days=[], location=raw_loc, error=error)

@app.route('/history')
def show_history():
    history = get_history(HISTORY_FILE)
    return render_template('history.html', history=history)

@app.route('/download-history')
def download_history():
    return send_file(HISTORY_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)