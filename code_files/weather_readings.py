from dataclasses import dataclass

@dataclass
class WeatherReading:
    date: str
    max_temp: int
    min_temp: int
    max_humidity: int
    mean_humidity: int

