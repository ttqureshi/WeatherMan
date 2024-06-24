from datetime import datetime
from code_files.constants import Colors, MonthsMapping


class WeatherReporter:
    def __init__(self, weather_extremes=None, date=None, avg_max_temp=None, avg_min_temp=None, avg_mean_humidity=None, high_bar=None, low_bar=None, isInline=None):
        self.weather_extremes = weather_extremes
        self.date = date
        self.avg_max_temp = avg_max_temp
        self.avg_min_temp = avg_min_temp
        self.avg_mean_humidity = avg_mean_humidity
        self.high_bar = high_bar
        self.low_bar = low_bar
        self.isInline = isInline
    
    def generate_report_extremes(self):
        """Generates a report summarizing weather extremes for a year."""

        print(f"\n<==== Report for the year {self.weather_extremes.date_htemp[0]}: ====>")
        print(
            f"Highest: {self.weather_extremes.highest_temp}C on "
            f"{MonthsMapping.MONTHS[int(self.weather_extremes.date_htemp[1])]} "
            f"{self.weather_extremes.date_htemp[2]}"
        )
        print(
            f"Lowest: {self.weather_extremes.lowest_temp}C on "
            f"{MonthsMapping.MONTHS[int(self.weather_extremes.date_ltemp[1])]} "
            f"{self.weather_extremes.date_ltemp[2]}"
        )
        print(
            f"Humidity: {self.weather_extremes.highest_humidity}% on "
            f"{MonthsMapping.MONTHS[int(self.weather_extremes.date_hhumid[1])]} "
            f"{self.weather_extremes.date_hhumid[2]}"
        )
        print("-------------------------------------")

    def generate_report_averages(self):
        """Generates a report summarizing average weather statistics for a given year and month."""

        print(f"\n<==== Report for the month: {MonthsMapping.MONTHS[int(self.date.strftime('%m'))]} {self.date.strftime('%Y')} ====>")
        print(f"Highest Average: {self.avg_max_temp:.1f}C")
        print(f"Lowest Average: {self.avg_min_temp:.1f}C")
        print(f"Average Mean Humidity: {self.avg_mean_humidity:.1f}%")
        print("-------------------------------------")

    def generate_report_barchart(self):
        """Generates bar chart of daily highest and lowest temperatures for a given month of the year"""

        if self.isInline:
            print(f"{self.date.strftime('%d')}{Colors.BLUE} {self.low_bar}{Colors.RED} {self.high_bar} "
                f"{Colors.BLUE}{len(self.low_bar)}C{Colors.RESET} - "
                f"{Colors.RED}{len(self.high_bar)}C{Colors.RESET}")
        else:
            print(f"{self.date.strftime('%d') + Colors.RED} {self.high_bar} {len(self.high_bar)}C{Colors.RESET}")
            print(f"{self.date.strftime('%d') + Colors.BLUE} {self.low_bar} {len(self.low_bar)}C{Colors.RESET}")
