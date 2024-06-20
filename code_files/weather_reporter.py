from code_files.constants import Colors, MonthsMapping


class WeatherReporter:
    @staticmethod
    def generate_report_extremes(weather_extremes):
        """Generates a report summarizing weather extremes for a year."""

        print(f"\n<==== Report for the year {weather_extremes.date_htemp[0]}: ====>")
        print(
            f"Highest: {weather_extremes.highest_temp}C on "
            f"{MonthsMapping.MONTHS[int(weather_extremes.date_htemp[1])]} "
            f"{weather_extremes.date_htemp[2]}"
        )
        print(
            f"Lowest: {weather_extremes.lowest_temp}C on "
            f"{MonthsMapping.MONTHS[int(weather_extremes.date_ltemp[1])]} "
            f"{weather_extremes.date_ltemp[2]}"
        )
        print(
            f"Humidity: {weather_extremes.highest_humidity}% on "
            f"{MonthsMapping.MONTHS[int(weather_extremes.date_hhumid[1])]} "
            f"{weather_extremes.date_hhumid[2]}"
        )
        print("-------------------------------------")

    def generate_report_averages(year, month, avg_max_temp, avg_min_temp, avg_mean_humidity):
        """Generates a report summarizing average weather statistics for a given year and month."""

        print(f"\n<==== Report for the month: {MonthsMapping.MONTHS[month]} {year} ====>")
        print(f"Highest Average: {avg_max_temp:.1f}C")
        print(f"Lowest Average: {avg_min_temp:.1f}C")
        print(f"Average Mean Humidity: {avg_mean_humidity:.1f}%")
        print("-------------------------------------")

    def generate_report_barchart(date, high_bar, low_bar, isInline):
        """Generates bar chart of daily highest and lowest temperatures for a given month of the year"""

        if isInline:
            print(f"{date[-1]}{Colors.BLUE} {low_bar}{Colors.RED} {high_bar} "
                f"{Colors.BLUE}{len(low_bar)}C{Colors.RESET} - "
                f"{Colors.RED}{len(high_bar)}C{Colors.RESET}")
        else:
            print(f"{date[-1] + Colors.RED} {high_bar} {len(high_bar)}C{Colors.RESET}")
            print(f"{date[-1] + Colors.BLUE} {low_bar} {len(low_bar)}C{Colors.RESET}")
