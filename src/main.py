import argparse
import logging

try:
    from utils import (
        build_weather_data_from_locations,
        demo_groupings_aggregations_and_visualizations
    )
except(ModuleNotFoundError, ImportError):
    from .utils import (
        build_weather_data_from_locations,
        demo_groupings_aggregations_and_visualizations
    )

logger = logging.getLogger()
logging.basicConfig(level="INFO")
logger.setLevel("INFO")


def main(ip_address_path):
    """
    Main function which gets location and weather info from IP addresses
    and produces, groups, aggregates and plots
    :param ip_address_path: path to text file with list of ip addresses
    """
    build_weather_data_from_locations(ip_address_path)
    demo_groupings_aggregations_and_visualizations()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ips', dest='ips', default='ip_addresses.txt',
        help='Text file with list of ip addresses to get weather info on'
    )
    args = parser.parse_args()
    main(args.ips)
