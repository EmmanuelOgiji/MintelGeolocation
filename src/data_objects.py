class Location:
    """Data object to hold required location details"""
    def __init__(self, location_dict):
        self.city = location_dict.get("city")
        self.country = location_dict.get("country")
        self.region = location_dict.get("regionName")
        self.latitude = location_dict.get("lat")
        self.longitude = location_dict.get("lon")


class WeatherInfo:
    def __init__(self, weather_dict):
        """Data object to hold required weather information"""
        self.temp = weather_dict['list'][0].get("main").get("temp")
        self.min_temp = weather_dict['list'][0].get("main").get("temp_min")
        self.max_temp = weather_dict['list'][0].get("main").get("temp_max")
        self.pressure = weather_dict['list'][0].get("main").get("pressure")
        self.humidity = weather_dict['list'][0].get("main").get("humidity")


class Constants:
    """Data object to hold constants"""
    LOCATION_API = "http://ip-api.com/json/"
    WEATHER_API = "https://api.openweathermap.org/data/2.5/find"
