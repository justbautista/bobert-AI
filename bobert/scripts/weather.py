import datetime as dt
import requests
import geocoder
import json

API_KEY = "1dc13fdb9f3d234d72e7694cb84b7502"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct?"

loc = geocoder.ip("me").latlng
url = f"{BASE_URL}lat={loc[0]}&lon={loc[1]}&appid={API_KEY}"

response = requests.get(url).json()

city = response[""]