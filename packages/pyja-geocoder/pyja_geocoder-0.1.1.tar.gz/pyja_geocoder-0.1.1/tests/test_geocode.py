import pandas as pd
import pytest

from pyja_geocoder.data_fetcher import load_japan_shapefile
from pyja_geocoder.geocode import (
    CITY_COLS,
    CITYCODE_COL,
    reverse_geocode_from_points,
    reverse_geocode_single,
    reverse_geocode_from_df,
    reverse_geocode_from_gdf,
    delete_cache,
)


@pytest.fixture(scope="module")
def polygons_gdf():
    # Load the polygons once for the test session
    return load_japan_shapefile()


def test_reverse_geocode_from_gdf(polygons_gdf):
    test_gdf = polygons_gdf[["geometry"]].copy()
    test_gdf["geometry"] = test_gdf.representative_point()

    result = reverse_geocode_from_gdf(test_gdf)
    target = polygons_gdf[CITY_COLS + [CITYCODE_COL]]
    assert result.equals(target)


def test_reverse_geocode_from_df(polygons_gdf):
    lat = polygons_gdf.geometry.representative_point().y
    lng = polygons_gdf.geometry.representative_point().x
    test_df = pd.DataFrame({"latitude": lat, "longitude": lng})
    result = reverse_geocode_from_df(test_df, crs=polygons_gdf.crs)
    target = polygons_gdf[CITY_COLS + [CITYCODE_COL]]
    assert result.equals(target)


def test_reverse_geocode_from_df_4326(polygons_gdf):
    crs = "EPSG:4326"

    lat_4326 = polygons_gdf.geometry.to_crs(crs).representative_point().y
    lng_4326 = polygons_gdf.geometry.to_crs(crs).representative_point().x
    test_df_4326 = pd.DataFrame({"latitude": lat_4326, "longitude": lng_4326})
    result_4326 = reverse_geocode_from_df(test_df_4326, crs=crs)
    target = polygons_gdf[CITY_COLS + [CITYCODE_COL]]
    assert result_4326.equals(target)


def test_reverse_geocode_from_points(polygons_gdf):
    # Take the first polygon from the GeoDataFrame
    test_points = polygons_gdf.representative_point()
    test_points = test_points.apply(lambda p: (p.y, p.x)).values.tolist()

    # Call the reverse geocoding function
    result = reverse_geocode_from_points(test_points)
    target = polygons_gdf[CITY_COLS + [CITYCODE_COL]]
    assert result.equals(target)


def test_reverse_geocode_from_points_4326(polygons_gdf):
    crs = "EPSG:4326"
    test_points = polygons_gdf.geometry.to_crs(crs).representative_point()
    test_points = test_points.apply(lambda p: (p.y, p.x)).values.tolist()
    result = reverse_geocode_from_points(test_points, crs=crs)
    target = polygons_gdf[CITY_COLS + [CITYCODE_COL]]
    assert result.equals(target)


def test_reverse_geocode_single(polygons_gdf):
    target = polygons_gdf.sample(1)
    test_point = target.representative_point().values[0]
    target_city = target.iloc[0][CITY_COLS].values
    target_citycode = target.iloc[0][CITYCODE_COL]

    city, citycode = reverse_geocode_single(test_point.y, test_point.x)
    assert city.tolist() == target_city.tolist()
    assert citycode == target_citycode


def test_reverse_geocode_single_4326(polygons_gdf):
    crs = "EPSG:4326"
    target = polygons_gdf.sample(1)
    test_point = target.geometry.to_crs(crs).representative_point().values[0]
    target_city = target.iloc[0][CITY_COLS].values
    target_citycode = target.iloc[0][CITYCODE_COL]
    city, citycode = reverse_geocode_single(test_point.y, test_point.x, crs=crs)
    assert city.tolist() == target_city.tolist()
    assert citycode == target_citycode


def test_delete_cache():
    delete_cache()
