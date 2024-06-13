import zipfile
from dataclasses import dataclass
from dataclasses import dataclass
import os
import csv
import argparse

@dataclass
class WeatherReading:
    date: str
    max_temp: int
    mean_temp: int
    min_temp: int
    max_humidity: int
    mean_humidity: int
    min_humidity: int


class Parser:
    def __init__(self, extract_to):
        self.extract_to = extract_to
        self.weather_readings = []

    def extract_zip(self, extract_to):
        """Extracts files from a weatherfiles archive.

        Args:
            path (str): The path to the directory where the extracted files will be placed.

        Raises:
            RuntimeError: If there are any errors during extraction.
        """
        try:
            with zipfile.ZipFile("weatherfiles.zip", "r") as zip_ref:
                zip_ref.extractall(extract_to)
        except zipfile.ZipFile as e:
            raise RuntimeError(f"Error extracting files: {e}")
    
    def parse_weather_file(self, path):
        """Parses a TXT file containing weather data.

        This method reads a TXT file at the specified path and populates the
        weather_readings list of the class with WeatherReading objects. Each
        object represents a day's weather data.
        """
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    reading = WeatherReading(
                        date=row[list(row.keys())[0]],
                        max_temp=int(row['Max TemperatureC']),
                        mean_temp=int(row['Mean TemperatureC']),
                        min_temp=int(row['Min TemperatureC']),
                        max_humidity=int(row['Max Humidity']),
                        mean_humidity=int(row[' Mean Humidity']),
                        min_humidity=int(row[' Min Humidity'])
                    )
                    self.weather_readings.append(reading)
                except ValueError:
                    continue
    
    def parse_all_files(self):
        """Parses all weather data files in the 'weatherfiles' directory."""
        
        dir_path = os.path.join(self.extract_to, 'weatherfiles')
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            self.parse_weather_file(file_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('extract_to', type=str)
    parser.add_argument('-e', '--extremes', type=int)
    parser.add_argument('-a', '--averages', type=str)
    parser.add_argument('-c', '--chart', type=str)

    args = parser.parse_args()

    parser = Parser(args.extract_to)
    parser.parse_all_files()
    print(parser.weather_readings[0])

    if args.extremes:
        print(args.extremes)
    
    if args.averages:
        print(args.averages)

    if args.chart:
        print(args.chart)
