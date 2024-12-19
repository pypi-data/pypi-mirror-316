from owm_key import owm_api_key
import requests
import json


# TODO 1
def get_weather_data(place, api_key=None):
    URL = f'https://api.openweathermap.org/data/2.5/weather?q={place}&appid={api_key}'
    response = requests.get(URL)

    if response.status_code == 200:
        res_obj = json.loads(response.text)
        data = json.dumps({"name": res_obj["name"], "coord": res_obj["coord"], "country": res_obj["sys"]["country"],
                           "feels_like (C)": round(res_obj["main"]["feels_like"] - 273.15, 2),
                           "timezone": res_obj["timezone"] / 3600}, separators=(',', ':'))
        print(data)
        return data
    else:
        print(f"Failed to fetch weather data for {place}. Status code: {response.status_code}")
        return None


if __name__ == '__main__':
    get_weather_data('Saint Petersburg', api_key=owm_api_key)
    get_weather_data('Dakka', api_key=owm_api_key)
    get_weather_data('Chicago', api_key=owm_api_key)