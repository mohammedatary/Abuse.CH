import requests
import json
from datetime import datetime

url = "https://urlhaus.abuse.ch/downloads/json_online/"

def fetch(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return Filter_and_Parse(data)
    else:
        print("Failed to fetch data")
        return []

# Function to filter and restructure data
def Filter_and_Parse(data):
    today_date = datetime.utcnow().date()
    filtered_data = []
    for key, entries in data.items():
        for entry in entries:
            entry_date = datetime.strptime(entry["dateadded"], "%Y-%m-%d %H:%M:%S UTC").date()
            if entry_date == today_date:
                new_entry = {
                    "IOC": entry["url"],
                    "threat": entry["threat"],
                    "last_online": entry["last_online"],
                    "url_status":entry["url_status"],
                    "tags":entry["tags"]

                }
                filtered_data.append(new_entry)
    return filtered_data

filtered_data = fetch(url)

today_str = datetime.now().strftime("%Y-%m-%d")

filename = f'urlhaus{today_str}.json'

with open(filename, 'w') as file:
    json.dump(filtered_data, file, indent=4)

print(f"Filtered data has been saved to {filename}")
