import os
import tempfile
from unittest import TestCase, mock
from unittest.mock import MagicMock

from src.data_objects import Location, WeatherInfo
from src.utils import (
    get_location,
    get_weather_info,
    build_output_dict,
    get_ips_from_file
)


class UnitTests(TestCase):
    @mock.patch('src.utils.requests.Session.get')
    def test_location_info(self, mock_get):
        mock_get().json = MagicMock(return_value=MockResponses.location_mock)
        location_obj = get_location("8.8.8.8")
        expected = dict(
            city="Montreal",
            longitude=-73.5493,
            latitude=45.6085,
            country="Canada",
            region="Quebec"
        )
        self.assertDictEqual(location_obj.__dict__, expected)

    @mock.patch('src.utils.requests.Session.get')
    def test_weather_info(self, mock_get):
        mock_get().json = MagicMock(return_value=MockResponses.weather_mock)
        weather_obj = get_weather_info("-3.3443", "55.9548")
        expected = dict(
            temp=18.17,
            min_temp=16.67,
            max_temp=19,
            pressure=1021,
            humidity=55,
        )
        self.assertDictEqual(weather_obj.__dict__, expected)

    def test_build_output_dict(self):
        location_obj = Location(MockResponses.location_mock)
        weather_obj = WeatherInfo(MockResponses.weather_mock)
        expected = dict(
            IPAddress="8.8.8.8",
            City="Montreal",
            Longitude=-73.5493,
            Latitude=45.6085,
            Country="Canada",
            Region="Quebec",
            Temperature=18.17,
            MinTemperature=16.67,
            MaxTemperature=19,
            Humidity=55,
            Pressure=1021
        )

        output_dict = build_output_dict(
            location=location_obj,
            weather_info=weather_obj,
            ip="8.8.8.8"
        )

        self.assertDictEqual(output_dict, expected)

    def test_get_ips_from_file(self):
        fd, path = tempfile.mkstemp()
        with open(fd, 'w') as tmp:
            tmp.write('1.1.1.1\n')
            tmp.write('1.2.3.4\n')

        ips = get_ips_from_file(path)
        os.remove(path)

        self.assertListEqual(ips, ['1.1.1.1', '1.2.3.4'])


class MockResponses:
    location_mock = {
        "query": "24.48.0.1",
        "status": "success",
        "country": "Canada",
        "countryCode": "CA",
        "region": "QC",
        "regionName": "Quebec",
        "city": "Montreal",
        "zip": "H1K",
        "lat": 45.6085,
        "lon": -73.5493,
        "timezone": "America/Toronto",
        "isp": "Le Groupe Videotron Ltee",
        "org": "Videotron Ltee",
        "as": "AS5769 Videotron Telecom Ltee"
    }

    weather_mock = {
        "message": "accurate",
        "cod": "200",
        "count": 1,
        "list": [
            {
                "id": 2635334,
                "name": "Turnhouse",
                "coord": {
                    "lat": 55.9548,
                    "lon": -3.3443
                },
                "main": {
                    "temp": 18.17,
                    "feels_like": 17.48,
                    "temp_min": 16.67,
                    "temp_max": 19,
                    "pressure": 1021,
                    "humidity": 55
                },
                "dt": 1622901972,
                "wind": {
                    "speed": 3.6,
                    "deg": 260
                },
                "sys": {
                    "country": "GB"
                },
                "rain": None,
                "snow": None,
                "clouds": {
                    "all": 75
                },
                "weather": [
                    {
                        "id": 803,
                        "main": "Clouds",
                        "description": "broken clouds",
                        "icon": "04d"
                    }
                ]
            }
        ]
    }
