import os
import zipfile

import geopandas as gpd
import numpy as np
import requests
from tqdm import tqdm

from .constants import MLIT_SHP_FOLDER, MLIT_SHP_PREFIX, MLIT_URL


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
        try:
            r = requests.get(url, stream=True)
            total = int(r.headers.get("content-length", 0))

            fname = os.path.basename(url)
            zip_path = os.path.join(data_dir, fname)
            with open(zip_path, "wb") as f, tqdm(
                total=total,
                unit="B",
                unit_scale=True,
                desc="Downloading MLIT shapefile",
            ) as pbar:
                for chunk in r.iter_content(chunk_size=8192):
                    pbar.update(len(chunk))
                    f.write(chunk)

        except requests.RequestException as e:
            error_msg = (
                f"{e}\n"
                f"Alternatively, you can download the zip file manually "
                f"from {url} and put it in {data_dir}, then unzip it."
            )
            raise FileNotFoundError(error_msg) from e

        # Extract shapefile components
        with zipfile.ZipFile(zip_path, "r") as z:
            for info in z.infolist():
                if info.filename in shp_files:
                    z.extract(info, path=shp_dir)

        os.remove(zip_path)

        if not all(os.path.exists(path) for path in shp_paths):
            raise FileNotFoundError("Shapefile components not found")

    return os.path.join(shp_dir, MLIT_SHP_PREFIX + ".shp")


def load_japan_shapefile(shp_path=None):
    """
    Loads the shapefile into a GeoDataFrame, downloading if necessary.
    Returns a GeoDataFrame with the Japanese city polygons.
    """
    if shp_path is None:
        shp_path = download_japan_shapefile()

    gdf = gpd.read_file(shp_path)
    gdf.fillna(np.nan, inplace=True)
    return gdf
