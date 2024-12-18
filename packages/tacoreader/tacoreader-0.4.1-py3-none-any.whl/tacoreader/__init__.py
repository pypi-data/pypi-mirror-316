from tacoreader.compile import compile
from tacoreader.load import load, load_metadata

import geopandas as gpd
import pandas as pd

__all__ = ["load", "compile", "load_metadata"]

__version__ = "0.4.1"



def _geodataframe_constructor_with_fallback(*args, **kwargs):
    """
    A flexible constructor for GeoDataFrame._constructor, which falls back
    to returning a DataFrame (if a certain operation does not preserve the
    geometry column)
    """
    df = gpd.GeoDataFrame(*args, **kwargs)
    geometry_cols_mask = df.dtypes == "geometry"
    if len(geometry_cols_mask) == 0 or geometry_cols_mask.sum() == 0:
        df = pd.DataFrame(df)

    return df

gpd.GeoDataFrame._constructor = _geodataframe_constructor_with_fallback