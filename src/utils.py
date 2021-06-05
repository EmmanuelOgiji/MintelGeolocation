import logging
import os

import requests

from data_objects import Location, Constants, WeatherInfo

logger = logging.getLogger()
logging.basicConfig(level="DEBUG")
logger.setLevel("DEBUG")


def get_location(ip_address):
    """

    :param ip_address: ip address to get location info on
    :return: Object with details on location of IP address
    """
    logger.info(f"Getting location from ip address:{ip_address}")
    location_response = requests.get(
        url=Constants.LOCATION_API,
        headers={
            "Content-Type": "application/json"
        },
        params={
            "apiKey": os.getenv("LOCATION_API_KEY"),
            "ip": ip_address
        }
    ).json()
    logger.debug(f"Full API response: {location_response}")
    location = Location(location_response)
    logger.info(f"Location details: {location.__dict__}")
    return location


def get_weather_info(latitude, longitude):
    """

    :param latitude: the coordinate latitude
    :param longitude: the coordinate longitude
    :return: Object containing weather info for location
    represented by coordinates longitude and latitude
    """
    logger.info(
        f"Getting weather info for coordinates: lon:{longitude}, lat:{latitude}"
    )
    weather_response = requests.get(
        url=Constants.WEATHER_API,
        headers={
            "Content-Type": "application/json"
        },
        params={
            "appid": os.getenv("WEATHER_API_KEY"),
            "lat": latitude,
            "lon": longitude,
            "units": "metric",
            "cnt": "1"
        }
    ).json()
    logger.debug(f"Full API response: {weather_response}")
    weather_info = WeatherInfo(weather_response)
    logger.info(f"Weather Info: {weather_info.__dict__}")
    return weather_info


def build_output_dict(location, weather_info, ip):
    """

    :param location: Object with details on location of IP address
    :param weather_info: Object containing weather info for location
    represented by coordinates longitude and latitude
    :param ip: ip address to get location and weather info on
    :return: a dict with the details obtained from one run
    """
    output = dict(
        IPAddress=ip,
        City=location.city,
        Longitude=location.longitude,
        Latitude=location.latitude,
        Province=location.province,
        Country=location.province,
        Continent=location.continent,
        Temperature=weather_info.temp,
        MinTemperature=weather_info.min_temp,
        MaxTemperature=weather_info.max_temp,
        Humidity=weather_info.humidity,
        Pressure=weather_info.pressure
    )
    logger.info(f"Output: {output}")
    return output


def get_ips_from_file(ip_address_path):
    """

    :param ip_address_path: Path to text file with ip addresses
    :return: list with the ip addresses from the file
    """
    logger.info(
        f"Getting ip addresses from txt file: {ip_address_path}"
    )
    with open(ip_address_path) as f:
        lines = f.read().splitlines()
    logger.debug(lines)
    return lines
