import requests
from requests.auth import HTTPBasicAuth

url = "https://iskm.egov.uz:9444/oauth2/token"

data = {
    "grant_type": "password",
    "username": "your_username",
    "password": "your_password"
}
consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret"

response = requests.post(url, data=data, auth=HTTPBasicAuth(consumer_key, consumer_secret))

if response.status_code == 200:
    access_token = response.json().get("access_token")
    print("Access Token:", access_token)
else:
    print("Failed to get access token:", response.status_code, response.text)
