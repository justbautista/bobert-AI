from datetime import date, timedelta
import requests
import geocoder

API_KEY = "1dc13fdb9f3d234d72e7694cb84b7502"
DAY_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
CURRENT_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "imperial"

loc = geocoder.ip("me").latlng

def createUrl(baseUrl):
    url = f"{baseUrl}lat={loc[0]}&lon={loc[1]}&units={UNITS}&appid={API_KEY}"
    return url

def findDayWeather(day):
    url = createUrl(DAY_BASE_URL)
    response = requests.get(url).json()

    if day == "today":
        theDay = str(date.today())
    else:
        theDay = str(date.today() + timedelta(days=1))

    hi = -300
    lo = 300
    hiWind = -10000
    loWind = 10000
    descriptions = set()
    theDayFound = False
    output = ""
    city = response["city"]["name"]
    country = response["city"]["country"]

    for i in range(response["cnt"]):
        dateFormatted = response["list"][i]["dt_txt"].split()[0]
        hiTemp = response["list"][i]["main"]["temp_max"]
        loTemp = response["list"][i]["main"]["temp_min"]
        description = response["list"][i]["weather"][0]["description"]
        windSpeed = response["list"][i]["wind"]["speed"]

        if dateFormatted == theDay:
            hi = max(hiTemp, hi)
            lo = min(loTemp, lo)
            hiWind = max(windSpeed, hiWind)
            loWind = min(windSpeed, loWind)
            descriptions.add(description)
            theDayFound = True

    if theDayFound:
        if day == "today":
            output = f"\n\n\tRest of Day\n"
        else:
            output = f"\nWeather Summary For Tomorrow in {city}, {country}:\n\n"

        output += f"\tTemperature Range(Fahrenheit): {lo} - {hi}\n"
        output += f"\tWind Speed Range(mph): {loWind} - {hiWind}\n"
        output += "\tDescription: "

        for i, desc in enumerate(descriptions):
            if (i == len(descriptions) - 1):
                output += desc
                break

            output += f"{desc}, "

    output += "\n"
    return output

def findCurrentWeather():
    url = createUrl(CURRENT_BASE_URL)
    response = requests.get(url).json()

    city = response["name"]
    country = response["sys"]["country"]
    temperature = response["main"]["temp"]
    wind = response["wind"]["speed"]
    description = response["weather"][0]["description"]

    output = f"\nWeather Summary For Today in {city}, {country}:\n\n"
    output += "\tCurrent\n"
    output += f"\tTemperature(Fahrenheit): {temperature}\n"
    output += f"\tWind Speed(mph): {wind}\n"
    output += f"\tDescription: {description}"

    return output

def findWeatherToday():
    return findCurrentWeather() + findDayWeather("today")


print(findWeatherToday())
print(findDayWeather("tomorrow"))




