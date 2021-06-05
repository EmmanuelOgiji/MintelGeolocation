class Location:
    """Data object to hold required location details"""
    def __init__(self, location_dict):
        self.city = location_dict.get("city")
        self.province = location_dict.get("state_prov")
        self.country = location_dict.get("country_name")
        self.continent = location_dict.get("continent_name")
        self.latitude = location_dict.get("latitude")
        self.longitude = location_dict.get("longitude")


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
    LOCATION_API = "https://api.ipgeolocation.io/ipgeo"
    WEATHER_API = "https://api.openweathermap.org/data/2.5/find"
