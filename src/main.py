import argparse
import logging

import pandas

from utils import (
    get_location,
    get_weather_info,
    build_output_dict,
    get_ips_from_file
)

logger = logging.getLogger()
logging.basicConfig(level="DEBUG")
logger.setLevel("DEBUG")


def main(ip_address_path):
    """
    Main function which gets location and weather info from IP addresses
    :param ip_address_path: path to text file with list of ip addresses
    """

    outputs = []
    ips = get_ips_from_file(ip_address_path)
    for ip in ips:
        location = get_location(ip)
        weather_info = get_weather_info(
            longitude=location.longitude,
            latitude=location.latitude
        )
        output = build_output_dict(location, weather_info, ip)
        outputs.append(output)
    print(pandas.DataFrame(outputs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ips', dest='ips', default='ip_addresses.txt',
        help='Text file with list of ip addresses to get weather info on'
    )
    args = parser.parse_args()
    main(args.ips)
