import csv
import os
import zipfile

from code_files.weather_readings import WeatherReading


class WeatherParser:
    def __init__(self, extract_to=None):
        self.extract_to = extract_to
        self.weather_readings = []

    def extract_zip(self):
        """Extracts files from a weatherfiles archive.

        Args:
            extract_to (str): The path to the directory where the extracted files will be placed.
        """
        with zipfile.ZipFile("weatherfiles.zip", "r") as zip_ref:
            zip_ref.extractall(self.extract_to)

    def parse_weather_file(self, path):
        """Parses a TXT file containing weather data.

        This method reads a TXT file at the specified path and populates the
        weather_readings list of the class with WeatherReading objects. Each
        object represents a day's weather data.
        """
        with open(path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = row[list(row.keys())[0]]
                max_temp = row["Max TemperatureC"]
                min_temp = row["Min TemperatureC"]
                max_humidity = row["Max Humidity"]
                mean_humidity = row[" Mean Humidity"]

                reading = WeatherReading(
                    date, max_temp, min_temp, max_humidity, mean_humidity
                )
                self.weather_readings.append(reading)

    def parse_all_files(self):
        """Parses all weather data files in the 'weatherfiles' directory."""

        dir_path = os.path.join(self.extract_to, "weatherfiles")
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            self.parse_weather_file(file_path)
