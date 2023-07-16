# Geospatial Python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Geocoding
from geopy.geocoders import Nominatim

# Util
from tqdm import tqdm
from time import sleep
import argparse


def geocode_with_sleep(row, geolocator) -> pd.Series:
    """
    Get coordinates from a row's state_name.
    Limited geocoding to follow Nominatim Usage Limits.

    Args:
        row: a DataFrame Row

    Returns:
        (pd.Series) The longitude and latitude from the state_name
    """

    query = row['state_name']
    sleep(2)
    location = geolocator.geocode(query)

    return pd.Series(
        [location.longitude, location.latitude],
        index=['longitude', 'latitude'])


def get_coordinates(df: pd.DataFrame, geo) -> pd.DataFrame:
    """
        A function that applies a geocoder to the input DataFrame to get
        the coordinates for each.

        Args:
            df (pd.DataFrame): A DataFrame with a state_name column

        Returns:
            (pd.DataFrame): Returns a new DataFrame with longitude and
            latitude columns
    """

    # No side effects to input df
    df = df.copy()
    df[['longitude', 'latitude']] = df.progress_apply(
        lambda x: geocode_with_sleep(x, geo),
        axis=1,
        result_type='expand')

    return df


def get_points(df: pd.DataFrame) -> pd.Series:
    """
    Get a Shapely Point Series by from a DataFrame with longitude
    and latitude columns.

    Args:
        df (pd.DataFrame): a DataFrame with longitude and latitude columns

    Returns:
        (pd.Series) A series of Shapely Points
    """

    df = df.copy()
    points = df.progress_apply(lambda row:
                               Point(row.longitude, row.latitude), axis=1)

    return points


def to_geodataframe(df: pd.DataFrame, points: pd.Series) -> gpd.GeoDataFrame:
    """
    Create a GeoDataFrame using a DataFrame and a Point Series

    Args:
        df (pd.DataFrame): DataFrame where the points series was
        derived from points (pd.Series): A Shapely Point series

    Returns
        (gpd.GeoDataFrame) A new GeoDataFrame with the Points
        Series as its geometry column
    """

    df = df.copy()

    geo_df = gpd.GeoDataFrame(df, geometry=points)
    # Change Coordinate Reference System to EPSG 4326
    geo_df.crs = {'init': 'epsg:4326'}

    return geo_df


def csv_to_geodataframe(csv) -> gpd.GeoDataFrame:
    """
        Convert a CSV with state_names into a GeoDataFrame

        Args:
            csv:

        Returns:
            (gpd.GeoDataFrame) A new GeoDataFrame based on the CSV passed.
    """

    # Instantiate Nominatim Geolocator
    geolocator = Nominatim(user_agent='http')

    df = pd.read_csv(csv)
    coord_df = get_coordinates(df, geolocator)
    points = get_points(coord_df)
    geo_df = to_geodataframe(coord_df, points)

    return geo_df


def main(csv: str, shp: str) -> None:
    # Initialize progress bar integration with Pandas
    tqdm.pandas()

    # pass csv name
    geo_df = csv_to_geodataframe(csv)
    # pass shp name
    geo_df.to_file(shp)

    print("Shp file has been created.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Convert Address CSV into GeoDataFrame")

    parser.add_argument("-c", "--csv", help="CSV File Name")
    parser.add_argument("-s", "--shp", help="SHP File Name")

    args = parser.parse_args()

    main(args.csv, args.shp)
