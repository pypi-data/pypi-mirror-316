import logging

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.ops import transform
from pyproj import Transformer

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


# delete cache
def delete_cache():
    global _POLYGON_GDF, _SINDEX
    _POLYGON_GDF = None
    _SINDEX = None


def reverse_geocode_from_df(
    points_df: pd.DataFrame,
    shp_path: str | None = None,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    crs: str = "EPSG:4326",
) -> pd.DataFrame:
    """
    Vectorized reverse geocoding from a DataFrame of points.

    :param points_df: A pandas DataFrame with at least two columns: lat_col and lon_col.
    :param shp_path: Optional path to the shapefile.
    :param lat_col: Name of the latitude column in points_df.
    :param lon_col: Name of the longitude column in points_df.
    :param crs: CRS of the points_df.
    :return: GeoDataFrame of matched city attributes including city code.
    """
    points_gdf = gpd.GeoDataFrame(
        points_df.copy(),
        geometry=gpd.points_from_xy(points_df[lon_col], points_df[lat_col]),
        crs=crs,
    )
    return reverse_geocode_from_gdf(points_gdf, shp_path)


def reverse_geocode_from_gdf(
    points_gdf: gpd.GeoDataFrame,
    shp_path: str | None = None,
) -> pd.DataFrame:
    """
    Vectorized reverse geocoding from a GeoDataFrame of points.

    :param points_gdf: A GeoDataFrame of points (must have geometry column).
    :param shp_path: Optional path to the shapefile.
    :return: DataFrame with city attributes and code.
    """
    polygons_gdf, _ = load_polygons_once(shp_path)

    points_gdf = points_gdf.to_crs(polygons_gdf.crs)

    joined = gpd.sjoin(
        points_gdf, polygons_gdf, how="left", predicate="within", rsuffix=None
    )
    # Extract the columns of interest
    result = joined[CITY_COLS + [CITYCODE_COL]].copy()
    return result


def reverse_geocode_from_points(
    points: list[tuple[float, float]],
    shp_path: str | None = None,
    crs: str = "EPSG:4326",
) -> pd.DataFrame:
    """
    Reverse geocode a list of (latitude, longitude) tuples.

    :param points: A list of (lat, lon) tuples.
    :param shp_path: Optional path to the shapefile.
    :param crs: CRS of the points.
    :return: DataFrame with the matched city attributes and codes.
    """
    # Convert the list of points to a DataFrame
    points_df = pd.DataFrame(points, columns=["latitude", "longitude"])

    # Utilize the previously defined vectorized function
    return reverse_geocode_from_df(points_df, shp_path=shp_path, crs=crs)


def reverse_geocode_single(
    lat: float,
    lng: float,
    shp_path: str | None = None,
    crs: str = "EPSG:4326",
) -> tuple[list[str] | None, str | None]:
    """
    Reverse geocode a single lat/lon point.

    :param lat: Latitude of the point.
    :param lng: Longitude of the point.
    :param shp_path: Optional path to the shapefile.
    :param crs: CRS of the point.
    :return: (array of city name, city code) or (None, None) if no match found.
    """
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise ValueError("Invalid latitude or longitude value")

    polygons_gdf, sindex = load_polygons_once(shp_path)

    point = Point(lng, lat)
    transformer = Transformer.from_crs(crs, polygons_gdf.crs, always_xy=True)
    point = transform(transformer.transform, point)

    possible_matches_index = list(sindex.intersection(point.bounds))
    candidates = polygons_gdf.iloc[possible_matches_index]

    for _, row in candidates.iterrows():
        if row.geometry.contains(point):
            return row[CITY_COLS].values, row[CITYCODE_COL]

    return None, None
