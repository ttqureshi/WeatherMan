import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from code_files.weather_app import WeatherReading


class TestWeatherReading(unittest.TestCase):
    def test_validate_reading(self):
        """Tests the functionality of validate_reading method of WeatherReading class."""

        self.assertEqual(WeatherReading.validate_reading(10), 10)
        self.assertEqual(WeatherReading.validate_reading("10"), 10)

        self.assertEqual(WeatherReading.validate_reading(-4), -4)
        self.assertEqual(WeatherReading.validate_reading("-4"), -4)

        self.assertEqual(WeatherReading.validate_reading(0), 0)
        self.assertEqual(WeatherReading.validate_reading("0"), 0)

        self.assertIsNone(WeatherReading.validate_reading(""))
        self.assertIsNone(WeatherReading.validate_reading(None))


if __name__ == "__main__":
    unittest.main()
