from dataclasses import dataclass


class WeatherReading:
    def __init__(self, date, max_temp, min_temp, max_humidity, mean_humidity):
        self.date = date
        self.max_temp = self.validate_reading(max_temp)
        self.min_temp = self.validate_reading(min_temp)
        self.max_humidity = self.validate_reading(max_humidity)
        self.mean_humidity = self.validate_reading(mean_humidity)
    
    def __eq__(self, other):
        return self.date == other.date and \
                self.max_temp == other.max_temp and \
                self.min_temp == other.min_temp and \
                self.max_humidity == other.max_humidity and \
                self.mean_humidity == other.mean_humidity

    @staticmethod
    def validate_reading(value):
        if value: # if value is empty ''
            return int(value)
        elif value == 0: # if value is 0
            return value


@dataclass
class WeatherExtremes:
    highest_temp: int
    lowest_temp: int
    highest_humidity: int
    date_htemp: list
    date_ltemp: list
    date_hhumid: list
