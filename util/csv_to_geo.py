# Geospatial Python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Geocoding
from geopy.geocoders import Nominatim

# Util
from tqdm import tqdm
from time import sleep


# Initialize progress bar integration with Pandas
tqdm.pandas()

# Instantiate Nominatim Geolocator
geolocator = Nominatim(user_agent='http')


def geocode_with_sleep(row) -> pd.Series:
    """
    Get coordinates from a row's state_name.
    Limited geocoding to follow Nominatim Usage Limits.

    Args:
        row: a DataFrame Row

    Returns:
        (pd.Series) The longitude and latitude from the state_name
    """

    query = row['state_name']
    sleep(1)
    location = geolocator.geocode(query)

    return pd.Series(
        [location.longitude, location.latitude],
        index=['longitude', 'latitude'])


def get_coordinates(df: pd.DataFrame) -> pd.DataFrame:
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
        geocode_with_sleep,
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

    df = pd.read_csv(csv)
    coord_df = get_coordinates(df)
    points = get_points(coord_df)
    geo_df = to_geodataframe(coord_df, points)

    return geo_df


def save_geodataframe():
    pass


def main():
    pass
    # tqdm
    # nominatim
    # csv to geodf
    # geodf to saved file


if __name__ == '__main__':
    main()