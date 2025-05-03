import json
from datetime import datetime


# Log the search location and timestamp to a JSON file  to the end of the file 
def log_search(raw_location, filename, resolved_location=None):
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'location': raw_location
    }
    if resolved_location:
        entry['resolved'] = resolved_location
    try:
        with open(filename, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(filename, 'w') as f:
            json.dump([entry], f, indent=2)

# Get the search history from the JSON file
def get_history(filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

