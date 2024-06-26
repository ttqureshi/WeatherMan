import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from code_files.weather_app import ReportCalculator, WeatherReading, WeatherExtremes

weather_reading1 = WeatherReading("2012-2-1", 9, 3, 36, 34)
weather_reading2 = WeatherReading("2012-2-2", 12, 5, 47, 34)
weather_reading3 = WeatherReading("2012-2-3", 2, -2, 100, 71)
weather_reading4 = WeatherReading("2012-2-4", 0, -2, 76, 74)
weather_reading5 = WeatherReading("2012-2-5", 3, -3, 87, 77)


class TestReportCalculator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readings = [
            weather_reading1,
            weather_reading2,
            weather_reading3,
            weather_reading4,
            weather_reading5,
        ]
        cls.report_calculator = ReportCalculator(cls.readings)

    @classmethod
    def tearDownClass(cls):
        del cls.readings
        del cls.report_calculator

    def test_compute_extreme_stats(self):
        """Test the compute_extreme_stats method of the ReportCalculator class.

        The purpose of this test is to ensure that the compute_extreme_stats method correctly
        calculates the weather extremes based on the input data.
        """
        self.weather_extremes = WeatherExtremes(
            12, -3, 100, ["2012", "2", "2"], ["2012", "2", "5"], ["2012", "2", "3"]
        )
        self.assertEqual(
            self.weather_extremes, self.report_calculator.compute_extreme_stats()
        )

    def test_compute_average_stats(self):
        """Test the compute_average_stats method of the ReportCalculator class.

        This test sets up expected values for the avg_max_temp, avg_min_temp and
        avg_mean_humidity. It then calls the compute_average_stats method of the
        ReportCalculator class and asserts that the returned values match the
        expected values.
        """
        self.avg_max_temp = 5.2
        self.avg_min_temp = 0.2
        self.avg_mean_humidity = 58
        self.result = (self.avg_max_temp, self.avg_min_temp, self.avg_mean_humidity)

        self.assertEqual(self.report_calculator.compute_average_stats(), self.result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
