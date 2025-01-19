import json
import requests

# Path to the JSON file
json_file_path = r"C:\Users\nishi\store-analytics\yolov8\output.json"

# Endpoint URL
ENDPOINT_URL = "http://localhost:3000/api/store_data"  # 🔹 Change this to your actual endpoint URL

# Read the JSON file
with open(json_file_path, 'r') as f:
    data = json.load(f)

# Send the data to the endpoint
response = requests.post(ENDPOINT_URL, json=data)
print(f"Response from server: {response.status_code}, {response.text}")