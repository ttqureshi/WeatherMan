import argparse
from file_parser import Parser
from weather_reporter import WeatherReporter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('extract_to', type=str)
    parser.add_argument('-e', '--extremes', type=int)
    parser.add_argument('-a', '--averages', type=str)
    parser.add_argument('-c', '--chart', type=str)
    parser.add_argument('--inline', action='store_true')

    args = parser.parse_args()

    parser = Parser(args.extract_to)
    parser.extract_zip()
    parser.parse_all_files()

    if args.extremes:
        yearly_readings = [r for r in parser.weather_readings if r.date.startswith(str(args.extremes))]
        WeatherReporter.generate_report_extremes(yearly_readings)
    
    if args.averages:
        year, month = map(int, args.averages.split('/'))
        monthly_readings = [r for r in parser.weather_readings if r.date.startswith(f"{year}-{month}")]
        WeatherReporter.generate_report_averages(year, month, monthly_readings)

    if args.chart:
        year, month = map(int, args.chart.split('/'))
        monthly_readings = [r for r in parser.weather_readings if r.date.startswith(f"{year}-{month}")]
        WeatherReporter.generate_report_barchart(year, month, monthly_readings, args.inline)
    

