import requests


def get_weather_data(city):
	URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=30bbb19aad4badf2852e44ab8517fc0d"
	r = requests.get(URL).json()
	return r
