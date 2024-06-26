import unittest

from test_report_calculator import TestReportCalculator
from test_weather_parser import TestWeatherParser
from test_weather_readings import TestWeatherReading


def test_suite():
    """This function creates a test suite containing all the test cases
    for the ReportCalculator, WeatherParser, and WeatherReadings.
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestReportCalculator))
    suite.addTest(unittest.makeSuite(TestWeatherParser))
    suite.addTest(unittest.makeSuite(TestWeatherReading))

    runner = unittest.TextTestRunner(verbosity=2)
    print(runner.run(suite))


test_suite()
