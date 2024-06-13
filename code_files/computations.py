class Computations:
    @staticmethod
    def compute_extreme_stats(readings):
        """Computes the extreme weather statistics for a particular year

        Args:
            readings (list): The list of WeatherReading objects of the given year

        Returns:
            highest_temp: Highest temperature throughout the year
            lowest_temp: Lowest temperature throughout the year
            highest_humidity: Highest humidity throughout the year
        """
        highest_temp = max(readings, key=lambda r: r.max_temp)
        lowest_temp = min(readings, key=lambda r: r.min_temp)
        highest_humidity = max(readings, key=lambda r: r.max_humidity)
        return highest_temp, lowest_temp, highest_humidity
    
    @staticmethod
    def compute_average_stats(readings):
        """Computes the average weather statistics for a particular month of the year

        Args:
            readings (list): The list of WeatherReading objects of the given month of the year

        Returns:
            avg_max_temp: Average Highest temperature of the month
            avg_min_temp: Average Lowest temperature of the month
            avg_mean_humidity: Average mean humidity of the month
        """
        total_max_temp = sum(r.max_temp for r in readings)
        total_min_temp = sum(r.min_temp for r in readings)
        total_mean_humidity = sum(r.mean_humidity for r in readings)

        count = len(readings)
        avg_max_temp = total_max_temp / count
        avg_min_temp = total_min_temp / count
        avg_mean_humidity = total_mean_humidity / count

        return avg_max_temp, avg_min_temp, avg_mean_humidity

