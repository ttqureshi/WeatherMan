from computations import Computations

MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

class WeatherReporter:
    @staticmethod
    def generate_report_extremes(readings):
        """Generates a report summarizing weather extremes for a year."""

        h_temp, l_temp, h_humidity = Computations.compute_extreme_stats(readings)
        date_htemp = h_temp.date.split("-")
        date_ltemp = l_temp.date.split("-")
        date_hhumid = h_humidity.date.split("-")

        print(f"\n<==== Report for the year {date_htemp[0]}: ====>")
        print(f"Highest: {h_temp.max_temp}C on {MONTHS[int(date_htemp[1])]} {date_htemp[2]}")
        print(f"Lowest: {l_temp.min_temp}C on {MONTHS[int(date_ltemp[1])]} {date_ltemp[2]}")
        print(f"Humidity: {h_humidity.max_humidity}% on {MONTHS[int(date_hhumid[1])]} {date_hhumid[2]}")
        print("-------------------------------------")

    def generate_report_averages(year, month, readings):
        """Generates a report summarizing average weather statistics for a given year and month."""

        avg_max_temp, avg_min_temp, avg_mean_humidity = Computations.compute_average_stats(readings)

        print(f"\n<==== Report for the month: {MONTHS[month]} {year} ====>")
        print(f"Highest Average: {avg_max_temp:.1f}C")
        print(f"Lowest Average: {avg_min_temp:.1f}C")
        print(f"Average Mean Humidity: {avg_mean_humidity:.1f}%")
        print("-------------------------------------")

    def generate_report_barchart(year, month, readings, isInline):
        """Generates bar chart of daily highest and lowest temperatures for a given month of the year"""

        RED = "\033[91m"
        BLUE = "\033[94m"
        RESET = "\033[0m"

        print(f"\n<==== Temperature Bar Charts for {MONTHS[month]} {year} ====>")
        for reading in readings:
            high_bar = '+' * reading.max_temp
            low_bar = '+' * reading.min_temp
            day = reading.date.split('-')[-1]
            if isInline:
                print(f"{day + BLUE} {low_bar + RED} {high_bar} {BLUE}{reading.min_temp}C{RESET + ' - ' + RED}{reading.max_temp}C{RESET}")
            else:
                print(f"{day + RED} {high_bar} {reading.max_temp}C{RESET}")
                print(f"{day + BLUE} {low_bar} {reading.min_temp}C{RESET}")

