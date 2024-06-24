import argparse
from datetime import datetime
from code_files.weather_parser import WeatherParser
from code_files.weather_reporter import WeatherReporter
from code_files.report_calculator import ReportCalculator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("extract_to", type=str, help='Directory to extract the results to.')
    parser.add_argument("-e", "--yearly_report", type=lambda e: datetime.strptime(e, '%Y'), help='Extreme weather stats for a year (format: YYYY).')
    parser.add_argument("-a", "--monthly_report", type=lambda a: datetime.strptime(a, '%Y/%m'), help='Year & Month for average weather stats (format: YYYY/MM)')
    parser.add_argument("-c", "--temp_chart", type=lambda c: datetime.strptime(c, '%Y/%m'), help='Year & Month for daily temperature chart (format: YYYY/MM)')
    parser.add_argument("--inline", action="store_true", help="One bar chart for highest and lowest temp on each day")

    args = parser.parse_args()

    parser = WeatherParser(args.extract_to)
    parser.extract_zip()
    parser.parse_all_files()

    if args.yearly_report:
        yearly_readings = [
            r for r in parser.weather_readings if r.date.startswith(args.yearly_report.strftime('%Y'))
        ]
        if yearly_readings:
            weather_extremes = ReportCalculator.compute_extreme_stats(yearly_readings)
            WeatherReporter.generate_report_extremes(weather_extremes)
        else:
            print(f"No record found to show WEATHER EXTREMES agaisnt your input")

    if args.monthly_report:
        year = args.monthly_report.strftime('%Y')
        month = int(args.monthly_report.strftime('%m'))
        monthly_readings = [
            r for r in parser.weather_readings if r.date.startswith(f"{year}-{month}")
        ]
        if monthly_readings:
            avg_max_temp, avg_min_temp, avg_mean_humidity = (
                ReportCalculator.compute_average_stats(monthly_readings)
            )
            WeatherReporter.generate_report_averages(
                year, month, avg_max_temp, avg_min_temp, avg_mean_humidity
            )
        else:
            print(f"No record found to show AVERAGE STATS against your input")

    if args.temp_chart:
        year = args.temp_chart.strftime('%Y')
        month = int(args.temp_chart.strftime('%m'))
        monthly_readings = [
            r for r in parser.weather_readings if r.date.startswith(f"{year}-{month}")
        ]

        if monthly_readings:
            for reading in monthly_readings:
                if reading.max_temp and reading.min_temp:
                    high_bar = "+" * reading.max_temp
                    low_bar = "+" * reading.min_temp
                    date = reading.date.split("-")
                    WeatherReporter.generate_report_barchart(
                        date, high_bar, low_bar, args.inline
                    )
        else:
            print(f"No record found to plot CHARTS against your input")
