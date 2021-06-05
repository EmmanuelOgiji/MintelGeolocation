import argparse
import logging

from utils import get_location, get_weather_info, build_output

logger = logging.getLogger()
logging.basicConfig(level="DEBUG")
logger.setLevel("DEBUG")


def main(ips):
    """
    Main function which gets location and weather info from IP addresses
    :param ips: list of ip-addresses
    """
    outputs = []
    for ip in ips:
        location = get_location(ip)
        weather_info = get_weather_info(
            longitude=location.longitude,
            latitude=location.latitude
        )
        output = build_output(location, weather_info, ip)
        outputs.append(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ips', dest='ips', default='82.37.140.136',
        help='Comma separated list of ip addresses to get weather info on'
    )
    args = parser.parse_args()
    ip_addresses = args.ips.split(',')
    main(ip_addresses)
