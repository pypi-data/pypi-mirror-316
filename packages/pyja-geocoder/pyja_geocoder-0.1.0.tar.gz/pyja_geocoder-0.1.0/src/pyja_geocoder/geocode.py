import logging

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from .data_fetcher import load_japan_shapefile

logger = logging.getLogger(__name__)

_POLYGON_GDF = None
_SINDEX = None

CITY_COLS = ["N03_001", "N03_002", "N03_003", "N03_004", "N03_005"]
CITYCODE_COL = "N03_007"


def load_polygons_once(shp_path=None):
    """
    Load the polygon GeoDataFrame and build the spatial index once.
    Uses a global cache to avoid repeated loading.

    :param shp_path: Optional path to the shapefile.
    :return: (GeoDataFrame, spatial_index)
    """
    global _POLYGON_GDF, _SINDEX
    if _POLYGON_GDF is None:
        _POLYGON_GDF = load_japan_shapefile(shp_path)
        _SINDEX = _POLYGON_GDF.sindex
        logger.debug("Shapefile loaded and indexed.")
    return _POLYGON_GDF, _SINDEX


def reverse_geocode_from_df(
    points_df, shp_path=None, lat_col="latitude", lon_col="longitude"
):
    """
    Vectorized reverse geocoding from a DataFrame of points.

    :param points_df: A pandas DataFrame with at least two columns: lat_col and lon_col.
    :param shp_path: Optional path to the shapefile.
    :param lat_col: Name of the latitude column in points_df.
    :param lon_col: Name of the longitude column in points_df.
    :return: GeoDataFrame of matched city attributes including city code.
    """
    polygons_gdf, _ = load_polygons_once(shp_path)
    points_gdf = gpd.GeoDataFrame(
        points_df.copy(),
        geometry=gpd.points_from_xy(points_df[lon_col], points_df[lat_col]),
        crs=polygons_gdf.crs,
    )
    return reverse_geocode_from_gdf(points_gdf, shp_path, polygons_gdf=polygons_gdf)


def reverse_geocode_from_gdf(points_gdf, shp_path=None, polygons_gdf=None):
    """
    Vectorized reverse geocoding from a GeoDataFrame of points.

    :param points_gdf: A GeoDataFrame of points (must have geometry column).
    :param shp_path: Optional path to the shapefile.
    :param polygons_gdf: Optional preloaded polygons GeoDataFrame.
    :return: DataFrame with city attributes and code.
    """
    if polygons_gdf is None:
        polygons_gdf, _ = load_polygons_once(shp_path)

    joined = gpd.sjoin(points_gdf, polygons_gdf, how="left", predicate="within")
    # Extract the columns of interest
    result = joined[CITY_COLS + [CITYCODE_COL]].copy()
    return result


def reverse_geocode_from_points(points, shp_path=None):
    """
    Reverse geocode a list of (latitude, longitude) tuples.

    :param points: A list of (lat, lon) tuples.
    :param shp_path: Optional path to the shapefile.
    :param return_df: If True, return a GeoDataFrame with the matched city attributes and codes.
    :return: DataFrame with the matched city attributes and codes.
    """
    # Convert the list of points to a DataFrame
    points_df = pd.DataFrame(points, columns=['latitude', 'longitude'])

    # Utilize the previously defined vectorized function
    return reverse_geocode_from_df(points_df, shp_path=shp_path, lat_col='latitude', lon_col='longitude')


def reverse_geocode_single(lat, lng, shp_path=None):
    """
    Reverse geocode a single lat/lon point.

    :param lat: Latitude of the point.
    :param lng: Longitude of the point.
    :param shp_path: Optional path to the shapefile.
    :return: (array of city name, city code) or (None, None) if no match found.
    """
    polygons_gdf, sindex = load_polygons_once(shp_path)
    point = Point(lng, lat)
    possible_matches_index = list(sindex.intersection(point.bounds))
    candidates = polygons_gdf.iloc[possible_matches_index]

    for _, row in candidates.iterrows():
        if row.geometry.contains(point):
            return row[CITY_COLS].values, row[CITYCODE_COL]

    return None, None
