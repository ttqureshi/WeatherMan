from code_files.weather_readings import WeatherExtremes


class ReportCalculator:
    def __init__(self, readings):
        self.readings = readings
    
    def compute_extreme_stats(self):
        """Computes the extreme weather statistics for a particular year"""
        
        highest_temp_reading = max(
            self.readings,
            key=lambda r: r.max_temp if r.max_temp is not None else float("-inf"),
        )
        lowest_temp_reading = min(
            self.readings,
            key=lambda r: r.min_temp if r.min_temp is not None else float("inf"),
        )
        highest_humidity_reading = max(
            self.readings,
            key=lambda r: (
                r.max_humidity if r.max_humidity is not None else float("-inf")
            ),
        )

        weather_extremes = WeatherExtremes(
            highest_temp=highest_temp_reading.max_temp,
            lowest_temp=lowest_temp_reading.min_temp,
            highest_humidity=highest_humidity_reading.max_humidity,
            date_htemp=highest_temp_reading.date.split("-"),
            date_ltemp=lowest_temp_reading.date.split("-"),
            date_hhumid=highest_humidity_reading.date.split("-"),
        )

        return weather_extremes

    def compute_average_stats(self):
        """Computes the average weather statistics for a particular month of the year"""

        total_max_temp = sum(r.max_temp for r in self.readings if r.max_temp)
        total_min_temp = sum(r.min_temp for r in self.readings if r.min_temp)
        total_mean_humidity = sum(r.mean_humidity for r in self.readings if r.mean_humidity)

        count = len(self.readings)
        avg_max_temp = total_max_temp / count
        avg_min_temp = total_min_temp / count
        avg_mean_humidity = total_mean_humidity / count

        return avg_max_temp, avg_min_temp, avg_mean_humidity
