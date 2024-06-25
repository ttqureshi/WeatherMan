import os
import sys
import unittest
from tempfile import NamedTemporaryFile

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from code_files.weather_parser import WeatherParser
from code_files.weather_readings import WeatherReading

SAMPLE_DATA = """PKT,Max TemperatureC,Mean TemperatureC,Min TemperatureC,Dew PointC,MeanDew PointC,Min DewpointC,Max Humidity, Mean Humidity, Min Humidity, Max Sea Level PressurehPa, Mean Sea Level PressurehPa, Min Sea Level PressurehPa, Max VisibilityKm, Mean VisibilityKm, Min VisibilitykM, Max Wind SpeedKm/h, Mean Wind SpeedKm/h, Max Gust SpeedKm/h,Precipitationmm, CloudCover, Events,WindDirDegrees
2012-2-1,9,6,3,-4,-5,-7,36,34,31,,,,10.0,7.0,4.0,11,8,,0.0,,,-1
2012-2-2,12,8,5,0,-4,-7,47,34,24,,,,10.0,7.0,4.0,18,12,,0.0,8,,-1
2012-2-3,2,1,-2,0,-3,-6,100,71,33,,,,4.0,2.0,0.1,11,4,,13.0,8,Snow,-1
2012-2-4,0,-0,-2,-4,-4,-5,76,74,71,,,,0.1,0.1,0.1,7,5,,48.0,8,Snow,-1
2012-2-5,3,0,-3,-0,-3,-6,87,77,70,,,,10.0,6.0,0.1,4,1,,15.0,8,Snow,-1
"""

class TestWeatherParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_file = NamedTemporaryFile(
            delete=False,
            mode="w",
            newline="",
            suffix=".txt",
        )
        cls.temp_file_name = cls.temp_file.name
        cls.temp_file.write(SAMPLE_DATA)
        cls.temp_file_path = os.path.join(os.getcwd(), cls.temp_file_name)
        cls.temp_file.close()
        cls.weather_parser = WeatherParser()
        cls.weather_parser.parse_weather_file(cls.temp_file_name)
    
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.temp_file_name)
    
    def test_parse_weather_file_total_readings(self):
        self.assertEqual(len(self.weather_parser.weather_readings), 5)
    
    def test_parse_weather_file_values(self):
        self.assertEqual(self.weather_parser.weather_readings[0], WeatherReading('2012-2-1',9,3,36,34))
        self.assertEqual(self.weather_parser.weather_readings[1], WeatherReading('2012-2-2',12,5,47,34))
        self.assertEqual(self.weather_parser.weather_readings[2], WeatherReading('2012-2-3',2,-2,100,71))
        self.assertEqual(self.weather_parser.weather_readings[3], WeatherReading('2012-2-4',0,-2,76,74))
        self.assertEqual(self.weather_parser.weather_readings[4], WeatherReading('2012-2-5',3,-3,87,77))

    
if __name__ == "__main__":
    unittest.main()
