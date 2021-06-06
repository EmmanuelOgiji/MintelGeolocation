import logging
import os

import pandas
import requests
import matplotlib.pyplot as plt
import seaborn as sns

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
        Country=location.country,
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
            df.to_csv('output.csv', mode='a')
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
    continent_group = data.groupby(by=["Continent"])

    logger.info("Grouping Demonstration")

    logger.info("Grouping Example: Details on IPs from Europe")
    logger.info(continent_group.get_group("Europe"))

    logger.info("Grouping Example: Details on IPs from the US")
    logger.info(country_group.get_group("United States"))

    logger.info("Grouping Example: Details on IPs from Seattle")
    logger.info(city_group.get_group("Seattle"))

    # Aggregation
    logger.info("Aggregation Demonstration")

    logger.info("Aggregation example: Average Temperature in Continents")
    continent_average_temp = continent_group.aggregate({"Temperature": "mean"})
    logger.info(continent_average_temp)

    logger.info("Aggregation example: Mean Max/Min Temperature in Continents")
    continent_average_temp_min_and_max = continent_group.aggregate(
        {
            "MaxTemperature": "mean",
            "MinTemperature": "mean"
        }
    )
    logger.info(continent_average_temp_min_and_max)

    # Visualizations
    logger.info("Visualization Demonstration")

    logger.info("Figure 1: Average Temperature in Continents")
    res = continent_average_temp.reset_index()
    res_wide = res.melt(id_vars="Continent")
    plt.figure(figsize=(10, 8))
    sns.barplot(x="Continent", y="value", data=res_wide, hue="variable")
    logger.info("Figure 2: Mean Max/Min Temperature in Continents")
    continent_average_temp_min_and_max.plot.bar(figsize=(18, 6))
    plt.show()
