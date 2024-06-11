import argparse
import zipfile
import os
import pandas as pd

MONTHS = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
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
    """
    max_temperature = -100
    min_temperature = 100
    max_humidity = 0
    date_max_temp = ""
    date_min_temp = ""
    date_max_humid = ""

    for key in weather_readings.keys():
        if key.startswith(str(year)):
            df = weather_readings[key]

            max_temp_index = df["Max TemperatureC"].idxmax()
            max_temp_row = df.loc[max_temp_index]
            temperature = max_temp_row["Max TemperatureC"]
            if temperature > max_temperature:
                max_temperature = temperature
                date_max_temp = max_temp_row["PKT"]

            min_temp_index = df["Min TemperatureC"].idxmin()
            min_temp_row = df.loc[min_temp_index]
            temperature = min_temp_row["Min TemperatureC"]
            if temperature < min_temperature:
                min_temperature = temperature
                date_min_temp = min_temp_row["PKT"]

            max_humid_index = df["Max Humidity"].idxmax()
            max_humid_row = df.loc[max_humid_index]
            humidity = max_humid_row["Max Humidity"]
            if humidity > max_humidity:
                max_humidity = humidity
                date_max_humid = max_humid_row["PKT"]

    results = {
        "max_temperature": max_temperature,
        "min_temperature": min_temperature,
        "max_humidity": max_humidity,
        "date_max_temp": date_max_temp,
        "date_min_temp": date_min_temp,
        "date_max_humid": date_max_humid,
    }
    return results


def generate_report_extremes(weather_readings, year):
    """Generates a report summarizing weather extremes for a year.

    This function takes the results of `stats_extremes` for a given year and
    formats them into a well-defined report.

    Args:
        weather_readings (dict): A dictionary where readings are stored as
            pandas dataframes.
        year (int): The year for which the report is generated.

    Returns:
        None
    """
    extremes = stats_extremes(weather_readings, year)
    date_max_temp = extremes["date_max_temp"].split("-")
    date_min_temp = extremes["date_min_temp"].split("-")
    date_humidity = extremes["date_max_humid"].split("-")

    print(
        f"""Highest: {extremes["max_temperature"]}C on {MONTHS[int(date_max_temp[1])]} {date_max_temp[2]}\nLowest: {extremes["min_temperature"]}C on {MONTHS[int(date_min_temp[1])]} {date_min_temp[2]}\nHumidity: {extremes["max_humidity"]}% on {MONTHS[int(date_humidity[1])]} {date_humidity[2]}
        """
    )


def stats_averages(weather_readings, year, month):
    pass


def stats_chart(weather_readings, year, month):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("extract_path")
    parser.add_argument("-e", "--extremes")
    parser.add_argument("-a", "--averages")
    parser.add_argument("-c", "--chart")

    args = parser.parse_args()

    extract_files(args.extract_path)
    weather_readings = parse(args.extract_path)
    # print(weather_readings["2006_Apr"].head())
    # cols = weather_readings["2006_Apr"].columns
    # print(cols)

    if args.extremes is not None:
        year = int(args.extremes)
        generate_report_extremes(weather_readings, year)

    if args.averages is not None:
        inp = args.averages.split("/")
        year = int(inp[0])
        month = int(inp[1])
        stats_averages(weather_readings, year, month)

    if args.chart is not None:
        inp = args.averages.split("/")
        year = int(inp[0])
        month = int(inp[1])
        stats_chart(weather_readings, year, month)
