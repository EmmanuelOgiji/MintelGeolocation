import argparse
import logging

from .utils import (
    build_weather_data_from_locations,
    use_data
)

logger = logging.getLogger()
logging.basicConfig(level="DEBUG")
logger.setLevel("DEBUG")


def main(ip_address_path):
    """
    Main function which gets location and weather info from IP addresses
    and produces, groups, aggregates and plots
    :param ip_address_path: path to text file with list of ip addresses
    """
    build_weather_data_from_locations(ip_address_path)
    use_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ips', dest='ips', default='ip_addresses.txt',
        help='Text file with list of ip addresses to get weather info on'
    )
    args = parser.parse_args()
    main(args.ips)
