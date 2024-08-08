from modules.scrap import get_weather
from modules.give_comment import predict_weather

def Generate_text():
    weather_data = get_weather()
    wea_text = f"{weather_data['city']}, {weather_data['temp']}, {weather_data['time']}, {weather_data['sky']}"
    comment = f"\"{predict_weather(weather_data['temp'], weather_data['time'], weather_data['sky'],)}\""
    return wea_text,comment