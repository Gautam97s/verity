import requests
import json

url = "http://127.0.0.1:8000/business/create"
payload = {
    "name": "My Test Business",
    "owner_name": "Gautam",
    "industry": "Tech"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Create Response: {response.status_code}")
    print(response.json())

    url_list = "http://127.0.0.1:8000/business/list"
    response_list = requests.get(url_list)
    print(f"List Response: {response_list.status_code}")
    print(response_list.json())
except Exception as e:
    print(f"Error: {e}")
