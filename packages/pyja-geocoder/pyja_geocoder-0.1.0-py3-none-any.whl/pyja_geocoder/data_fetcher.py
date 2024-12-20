import logging
import os
import re
import zipfile

import geopandas as gpd
import numpy as np
import requests

from .constants import MLIT_URL, MLIT_SHP_FOLDER, MLIT_SHP_PREFIX

logger = logging.getLogger(__name__)


def default_data_dir():
    """
    Returns a local directory path where the shapefile will be cached.
    """
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, ".pyja_geocoder")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def download_japan_shapefile(url=MLIT_URL, data_dir=None):
    if data_dir is None:
        data_dir = default_data_dir()

    # Check if the files are present
    shp_dir = os.path.join(data_dir, MLIT_SHP_FOLDER)
    os.makedirs(shp_dir, exist_ok=True)
    shp_exts = {"shp", "shx", "dbf", "prj", "cpg"}
    shp_files = {f"{MLIT_SHP_PREFIX}.{ext}" for ext in shp_exts}
    shp_paths = {os.path.join(shp_dir, fn) for fn in shp_files}

    if not all(os.path.exists(path) for path in shp_paths):
        # Download if not present
        logger.info("Downloading MLIT shapefile from %s...", url)
        try:
            r = requests.get(url)
            r.raise_for_status()

            fname = os.path.basename(url)
            zip_path = os.path.join(data_dir, fname)
            with open(zip_path, "wb") as f:
                f.write(r.content)
        except requests.RequestException as e:
            logger.error("Failed to download MLIT shapefile: %s", e)
            logger.error(
                "Alternatively, you can download the zip file manually from %s, put it in %s, and unzip it.",
                url, data_dir,
            )
            raise e

        # Extract shapefile components
        with zipfile.ZipFile(zip_path, "r") as z:
            for info in z.infolist():
                print(info)
                if info.filename in shp_files:
                    z.extract(info, path=shp_dir)

        os.remove(zip_path)

        if not all(os.path.exists(path) for path in shp_paths):
            raise FileNotFoundError("Shapefile components not found")

        logger.info("Shapefile components downloaded and extracted.")

    return os.path.join(shp_dir, MLIT_SHP_PREFIX + ".shp")


def load_japan_shapefile(shp_path=None):
    """
    Loads the shapefile into a GeoDataFrame, downloading if necessary.
    Returns a GeoDataFrame with the Japanese city polygons.
    """
    if shp_path is None:
        shp_path = download_japan_shapefile()

    logger.debug("Loading shapefile from %s ...", shp_path)
    gdf = gpd.read_file(shp_path)
    gdf.fillna(np.nan, inplace=True)
    logger.debug("Shapefile loaded.")
    return gdf
