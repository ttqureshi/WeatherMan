import argparse
import zipfile
import os
import pandas as pd


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
        weather_readings (dict): A dictionary where keys are constructed from
            year and month information in the filenames, and values are pandas
            DataFrames containing the parsed weather data.
    """
    weather_readings = {}
    dir_path = os.path.join(path, "weatherfiles")
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)

        key = filename.split("_")[2:]
        key[-1] = key[-1].split(".")[0]
        key = "_".join(key)

        df = pd.read_csv(file_path, delimiter=",")
        weather_readings[key] = df
    return weather_readings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("extract_path")
    parser.add_argument("-e", "--extremes")
    parser.add_argument("-a", "--averages")
    parser.add_argument("-c", "--chart")

    args = parser.parse_args()

    extract_files(args.extract_path)
    weather_readings = parse(args.extract_path)
    print(weather_readings["2006_Apr"].head())
