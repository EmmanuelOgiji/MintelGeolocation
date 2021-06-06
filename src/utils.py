import logging
import os

import pandas
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from urllib3 import Retry
from requests.adapters import HTTPAdapter

try:
    from data_objects import Location, Constants, WeatherInfo
except (ModuleNotFoundError, ImportError):
    from .data_objects import Location, Constants, WeatherInfo

logger = logging.getLogger()
logging.basicConfig(level="INFO")
logger.setLevel("INFO")


def get_request_session_with_retries(backoff_factor):
    """

    :param backoff_factor: backoff factor use in implementing
    exponential back off in retries
    :return: request session with retry strategy in place
    """
    logger.info("Setting up request session")
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=backoff_factor
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    return http


def get_location(ip_address):
    """

    :param ip_address: ip address to get location info on
    :return: Object with details on location of IP address
    """
    logger.info(f"Getting location from ip address:{ip_address}")
    http = get_request_session_with_retries(60)

    location_response = http.get(
        url=f"{Constants.LOCATION_API}/{ip_address}"
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
    http = get_request_session_with_retries(1)

    weather_response = http.get(
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
        Country=location.country,
        Region=location.region,
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


def build_weather_data_from_locations(ip_address_path):
    """
    Gets location and corresponding weather info from IP addresses
    and writes them into csv file
    :param ip_address_path: path to text file with list of ip addresses
    """
    ips = get_ips_from_file(ip_address_path)
    for ip in ips:
        index = ips.index(ip)
        location = get_location(ip)
        weather_info = get_weather_info(
            longitude=location.longitude,
            latitude=location.latitude
        )
        output = build_output_dict(location, weather_info, ip)
        df = pandas.DataFrame(output, index=[index])
        logger.debug(f"Output: \n {df}")
        if index == 0:
            df.to_csv('output.csv')
        else:
            df.to_csv('output.csv', mode='a', header=False)


def use_data():
    """
    Uses data produced from API on weather and locations to give groups,
    aggregates and visualizations
    """
    data = pandas.read_csv('output.csv')
    # Group by
    city_group = data.groupby(by=["City"])
    country_group = data.groupby(by=["Country"])
    region_group = data.groupby(by=["Region"])

    logger.info("Grouping Demonstration")

    logger.info("Grouping Example: Details on IPs from Quebec")
    logger.info(region_group.get_group("Quebec"))

    logger.info("Grouping Example: Details on IPs from the US")
    logger.info(country_group.get_group("United States"))

    logger.info("Grouping Example: Details on IPs from Seattle")
    logger.info(city_group.get_group("Seattle"))

    # Aggregation
    logger.info("Aggregation Demonstration")

    logger.info("Aggregation example: Average Temperature in Countries")
    continent_average_temp = country_group.aggregate({"Temperature": "mean"})
    logger.info(continent_average_temp)

    logger.info("Aggregation example: Mean Max/Min Temperature in Countries")
    continent_average_temp_min_and_max = country_group.aggregate(
        {
            "MaxTemperature": "mean",
            "MinTemperature": "mean"
        }
    )
    logger.info(continent_average_temp_min_and_max)

    # Visualizations
    logger.info("Visualization Demonstration")

    logger.info("Figure 1: Average Temperature in Countries")
    res = continent_average_temp.reset_index()
    res_wide = res.melt(id_vars="Continent")
    plt.figure(figsize=(10, 8))
    sns.barplot(x="Continent", y="value", data=res_wide, hue="variable")
    logger.info("Figure 2: Mean Max/Min Temperature in Countries")
    continent_average_temp_min_and_max.plot.bar(figsize=(18, 6))
    plt.show()
