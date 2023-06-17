# Dummy change
import argparse
import logging
from flask import Flask, send_file

app = Flask(__name__)

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
    logger.info(
        "Starting Flask app to show plots. This will be available on http://localhost:5000\n"
        "PLEASE DO NOT TRY TO ACCESS BY THE URL BELOW as it will not work"
    )
    app.run(port=5000, debug=False, host='0.0.0.0')


@app.route('/')
def deliver_plots():
    return send_file("figures.png", mimetype='image/png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--ips', dest='ips', default='ip_addresses.txt',
        help='Text file with list of ip addresses to get weather info on'
    )
    args = parser.parse_args()
    main(args.ips)
