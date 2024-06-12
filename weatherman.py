import argparse
import zipfile
import os
import pandas as pd
import math

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


def extract_files(path):
    """Extracts files from a weatherfiles archive.

    Args:
        path (str): The path to the directory where the extracted files will be placed.

    Raises:
        RuntimeError: If there are any errors during extraction.
    """
    try:
        with zipfile.ZipFile("weatherfiles.zip", "r") as zip_ref:
            zip_ref.extractall(path)
    except zipfile.ZipFile as e:
        raise RuntimeError(f"Error extracting files: {e}")


def parse(path):
    """Parses weather data from TXT files within a directory.

    Args:
        path (str): The path to the directory containing the 'weatherfiles'
            subdirectory.

    Returns:
        weather_readings (dict): A dictionary where readings are stored as
            pandas dataframes.
    """
    weather_readings = {}
    dir_path = os.path.join(path, "weatherfiles")
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)

        # making the key to be of the format: '2006_Apr'
        key = filename.split("_")[2:]
        key[-1] = key[-1].split(".")[0]
        key = "_".join(key)

        df = pd.read_csv(file_path, delimiter=",")
        weather_readings[key] = df
    return weather_readings


def stats_extremes(weather_readings, year):
    """Calculates weather extremes for a specific year.

    Args:
        weather_readings (dict): A dictionary where readings are stored as
            pandas dataframes.
        year (int): The year for which to calculate weather extremes.

    Returns:
        dict: A dictionary containing the following keys:
            - 'max_temperature': The maximum temperature.
            - 'min_temperature': The minimum temperature.
            - 'max_humidity': The maximum humidity percentage.
            - 'date_max_temp': The date (PKT format) with the maximum temperature.
            - 'date_min_temp': The date (PKT format) with the minimum temperature.
            - 'date_max_humid': The date (PKT format) with the maximum humidity.
        None: If no data is found for the specified year and month.
    """
    record_found = False
    max_temperature = -100
    min_temperature = 100
    max_humidity = 0
    date_max_temp = ""
    date_min_temp = ""
    date_max_humid = ""

    for key in weather_readings.keys():
        if key.startswith(str(year)):
            record_found = True
            df = weather_readings[key]

            max_temp_index = df["Max TemperatureC"].idxmax()
            max_temp_row = df.loc[max_temp_index]
            temperature = max_temp_row["Max TemperatureC"]
            if temperature > max_temperature:
                max_temperature = temperature
                try:
                    date_max_temp = max_temp_row["PKT"]
                except:
                    date_max_temp = max_temp_row["PKST"]

            min_temp_index = df["Min TemperatureC"].idxmin()
            min_temp_row = df.loc[min_temp_index]
            temperature = min_temp_row["Min TemperatureC"]
            if temperature < min_temperature:
                min_temperature = temperature
                try:
                    date_min_temp = min_temp_row["PKT"]
                except:
                    date_min_temp = min_temp_row["PKST"]

            max_humid_index = df["Max Humidity"].idxmax()
            max_humid_row = df.loc[max_humid_index]
            humidity = max_humid_row["Max Humidity"]
            if humidity > max_humidity:
                max_humidity = humidity
                try:
                    date_max_humid = max_humid_row["PKT"]
                except:
                    date_max_humid = max_humid_row["PKST"]

    if record_found:
        results = {
            "max_temperature": max_temperature,
            "min_temperature": min_temperature,
            "max_humidity": max_humidity,
            "date_max_temp": date_max_temp,
            "date_min_temp": date_min_temp,
            "date_max_humid": date_max_humid,
        }
        return results
    else:
        return None


def generate_report_extremes(weather_readings, year):
    """Generates a report summarizing weather extremes for a year."""

    extremes = stats_extremes(weather_readings, year)
    print(f"\n***** Report for the year {year}: *****")
    if extremes is not None:
        date_max_temp = extremes["date_max_temp"].split("-")
        date_min_temp = extremes["date_min_temp"].split("-")
        date_humidity = extremes["date_max_humid"].split("-")

        print(
            f"Highest: {extremes['max_temperature']}C on {MONTHS[int(date_max_temp[1])]} {date_max_temp[2]}"
        )
        print(
            f"Lowest: {extremes['min_temperature']}C on {MONTHS[int(date_min_temp[1])]} {date_min_temp[2]}"
        )
        print(
            f"Humidity: {extremes['max_humidity']}% on {MONTHS[int(date_humidity[1])]} {date_humidity[2]}"
        )
    else:
        print("Sorry! No records found against your input")
    print("-------------------------------------")


def stats_averages(weather_readings, year, month):
    """Calculates average highest temperature, average lowest temperature,
    and average mean humidity for a given year and month.

    Args:
        weather_readings (dict): A dictionary where readings are stored as
            pandas dataframes.
        year (int): The year for which to calculate averages.
        month (int): The month (1-12) for which to calculate averages.

    Returns:
        dict: A dictionary containing the following keys if data is found for the
            specified year and month:
            - 'avg_highest_temp': Average of the daily maximum temperatures in °C.
            - 'avg_lowest_temp': Average of the daily minimum temperatures in °C.
            - 'avg_mean_humidity': Average of the daily mean humidity values.
        None: If no data is found for the specified year and month.
    """
    record_found = False
    mon = MONTHS[month][:3]
    year_month = str(year) + "_" + mon
    for key in weather_readings.keys():
        if key == year_month:
            record_found = True
            avg_highest_temp = weather_readings[key]["Max TemperatureC"].mean()
            avg_lowest_temp = weather_readings[key]["Min TemperatureC"].mean()
            avg_mean_humidity = weather_readings[key][" Mean Humidity"].mean()
            break

    if record_found:
        results = {
            "avg_highest_temp": avg_highest_temp,
            "avg_lowest_temp": avg_lowest_temp,
            "avg_mean_humidity": avg_mean_humidity,
        }
        return results
    return None


def generate_report_averages(weather_readings, year, month):
    """Generates a report summarizing average weather statistics for a given year and month."""

    averages = stats_averages(weather_readings, year, month)
    print(f"\n***** Report for the month: {MONTHS[month]} {year} *****")
    if averages is not None:
        print(f"Highest Average: {averages['avg_highest_temp']}C")
        print(f"Lowest Average: {averages['avg_lowest_temp']}C")
        print(f"Average Mean Humidity: {averages['avg_mean_humidity']}%")
    else:
        print("Sorry! No records found against your input")
    print("-------------------------------------")


def generate_chart(weather_readings, year, month):
    RED = "\033[91m"
    BLUE = "\033[94m"
    RESET = "\033[0m"

    record_found = False
    mon = MONTHS[month][:3]
    year_month = str(year) + "_" + mon
    for key in weather_readings.keys():
        if key == year_month:
            record_found = True
            print(f"\n{MONTHS[month]} {year}")
            for _, row in weather_readings[key].iterrows():
                try:
                    date = row['PKT'].split("-")
                except:
                    date = row['PKST'].split("-")
                
                if not math.isnan(row['Max TemperatureC']): 
                    temp_high = int(row['Max TemperatureC'])
                    temp_low = int(row['Min TemperatureC'])

                    print(f"{date[-1]} {RED + ('+' * temp_high) + RESET} {temp_high}C")
                    print(f"{date[-1]} {BLUE + ('+' * temp_low) + RESET} {temp_low}C")
            break
    if not record_found:
        print("Sorry! No records found against your input")
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("extract_path")
    parser.add_argument("-e", "--extremes")
    parser.add_argument("-a", "--averages")
    parser.add_argument("-c", "--chart")

    args = parser.parse_args()

    extract_files(args.extract_path)
    weather_readings = parse(args.extract_path)

    if args.extremes is not None:
        year = int(args.extremes)
        generate_report_extremes(weather_readings, year)

    if args.averages is not None:
        inp = args.averages.split("/")
        year = int(inp[0])
        month = int(inp[1])
        generate_report_averages(weather_readings, year, month)

    if args.chart is not None:
        inp = args.chart.split("/")
        year = int(inp[0])
        month = int(inp[1])
        generate_chart(weather_readings, year, month)
