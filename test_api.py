import requests
from datetime import date


date = date.today().strftime('%Y-%m-%d')
flight_num = input("Please enter the flight number: ")

url = f"https://aerodatabox.p.rapidapi.com/flights/number/{flight_num}/{date}"

headers = {
	"X-RapidAPI-Key": "17f75df5efmsh9b4ae3bc52aebc4p120b7cjsn63e5ff22f6da",
	"X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.json())