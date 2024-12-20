# pyja_geocoder

**pyja_geocoder** is a Python package for reverse geocoding in Japan. It uses vectorized operations with GeoPandas to efficiently map latitude and longitude coordinates to corresponding Japanese city attributes, based on official shapefile data provided by MLIT (Ministry of Land, Infrastructure, Transport, and Tourism).

## Features

- **Batch Processing**: Reverse geocode multiple coordinates simultaneously using a DataFrame.
- **Single Point Geocoding**: Reverse geocode a single latitude/longitude coordinate.
- **Efficient Spatial Operations**: Leverages GeoPandas and spatial indexing for fast lookups.

## Installation

### Install from PyPI

```bash
pip install pyja-geocoder
```

### Install from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pyja_geocoder.git
   cd pyja_geocoder
   ```

2. Install the package:
   ```bash
   pip install .
   ```

## Usage

### Import the Package

```python
from pyja_geocoder import reverse_geocode_from_df, reverse_geocode_from_points, reverse_geocode_single
```

### Reverse Geocode a Single Point

```python
lat, lon = 35.6895, 139.6917  # Latitude and longitude for Tokyo
city, citycode = reverse_geocode_single(lat, lon)
print("City:", city)
print("City Code:", citycode)
```

### Reverse Geocode a List of Points

```python
points = [(35.6895, 139.6917), (34.6937, 135.5022)]  # Tokyo and Osaka
result_df = reverse_geocode_from_points(points)
print(result_df)
```

### Reverse Geocode a DataFrame of Points

```python
import pandas as pd

df = pd.DataFrame({"latitude": [35.6895, 34.6937], "longitude": [139.6917, 135.5022]})
result_df = reverse_geocode_from_df(df)
print(result_df)
```

### Load the Default Shapefile

The package uses the official MLIT shapefile for geocoding. The data will be downloaded and cached automatically if not already present.

```python
from pyja_geocoder import load_japan_shapefile

gdf = load_japan_shapefile()  # Load the MLIT shapefile as a GeoDataFrame
```


## Data Source

The shapefile used by this package is sourced from MLIT (Ministry of Land, Infrastructure, Transport, and Tourism). The latest data can be accessed [here](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-2024.html).
