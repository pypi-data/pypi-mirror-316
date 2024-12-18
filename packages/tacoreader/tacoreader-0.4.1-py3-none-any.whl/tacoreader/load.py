import pathlib
import re
from typing import List, Union

import geopandas as gpd
import pandas as pd
import requests

from tacoreader import datasets, load_local, load_remote, load_utils


def load(file: Union[str, pathlib.Path, List[pathlib.Path], List[str]]) -> pd.DataFrame:
    """Load the dataframe of a tortilla file.

    Args:
        file (Union[str, pathlib.Path, List]): The path of
            the tortilla file. If the file is split into multiple
            parts, a list of paths is accepted. Also, multiple
            parts can be read by putting a asterisk (*) at the end
            of the file name. For example, "file*.tortilla". In this
            case, the function will create a list will all the partitions
            before the reading process.

    Returns:
        pd.DataFrame: The dataframe of the tortilla file.
    """

    # Check if the dataset is inside the taco foundation
    if file in datasets.datasets.keys():
        file = datasets.datasets[file]

    # Transform our snippet into a list of files
    # If it is not a snippet, it will return the same file
    file = load_utils.snippet2files(file=file)

    if isinstance(file, list):
        if load_utils.is_valid_url(file):
            dataframe = load_remote.remote_files2dataframe(file)
        else:
            dataframe = load_local.local_files2dataframe(file)
    elif isinstance(file, (str, pathlib.Path)):
        if load_utils.is_valid_url(file):
            dataframe = load_remote.remote_file2dataframe(file)
        else:
            dataframe = load_local.local_file2dataframe(file)
    else:
        raise ValueError("Invalid file type. Must be a list, string or pathlib.Path.")

    # Clean up the dataframe
    dataframe = load_utils.sort_columns_add_geometry(dataframe)

    return TortillaDataFrame(dataframe)


def lazy_load(offset: int, file: Union[str, pathlib.Path]) -> pd.DataFrame:
    """Lazy load a tortilla file.

    Useful for datasets that have tortillas as samples (tortillas inside tortillas).
    The offset is used to read a specific part of the main tortilla file.

    Args:
        offset (int): The byte offset where the reading process will start.
        file (Union[str, pathlib.Path]): The path tot the main tortilla file.

    Returns:
        pd.DataFrame: The dataframe of the tortilla file.
    """

    if load_utils.is_valid_url(file):
        dataframe = load_remote.remote_lazyfile2dataframe(offset, file)
    else:
        dataframe = load_local.local_lazyfile2dataframe(offset, file)

    # Clean up the dataframe
    dataframe = load_utils.sort_columns_add_geometry(dataframe)

    return TortillaDataFrame(dataframe)


def load_metadata(
    file: Union[str, pathlib.Path, List[pathlib.Path], List[str]]
) -> dict:
    """Load the metadata of a tortilla or taco file.

    Args:
        file (Union[str, pathlib.Path, List]): The path of
            the taco file. If the file is split into multiple
            parts, a list of paths is accepted. Also, multiple
            parts can be read by putting a asterisk (*) at the end
            of the file name. For example, "file*.tortilla". In this
            case, the function will create a list will all the partitions
            before the reading process.

    Returns:
        dict: The metadata of the taco file.
    """
    # Transform our snippet into a list of files
    # If it is not a snippet, it will return the same file
    file = load_utils.snippet2files(file=file)

    # Load the metadata
    if isinstance(file, list):
        if load_utils.is_valid_url(file):
            metadata = load_remote.remote_files2metadata(file)
        else:
            metadata = load_local.local_files2metadata(file)
    elif isinstance(file, (str, pathlib.Path)):
        if load_utils.is_valid_url(file):
            metadata = load_remote.remote_file2metadata(file)
        else:
            metadata = load_local.local_file2metadata(file)
    else:
        raise ValueError("Invalid file type. Must be a list, string or pathlib.Path.")

    return metadata



def construct_tortilla_dataframe(*args, **kwargs):
    """
    A flexible constructor for TortillaDataFrame._constructor, which falls 
    back to returning a pandas DataFrame if the operation invalidates the 
    required format.
    """
    
    try:
        # Attempt to create a TortillaDataFrame
        df = TortillaDataFrame(gpd.GeoDataFrame(*args, **kwargs))
        key_fields = [
            "tortilla:file_format", "internal:subfile", "tortilla:offset", "tortilla:length"
        ]

        # Validate required columns or metadata (modify as needed)
        if not df.columns.isin(key_fields).all():
            raise ValueError("Missing required Tortilla-specific columns.")
    except Exception:
        # Fallback to a standard pandas DataFrame if TortillaDataFrame construction fails
        df = pd.DataFrame(*args, **kwargs)

    return df



class TortillaDataFrame(gpd.GeoDataFrame):
    _metadata = []

    @property
    def _constructor(self):
        """Override the constructor to always return TortillaDataFrame."""
        return construct_tortilla_dataframe

    def __finalize__(self, other, method=None, **kwargs):
        """Finalize metadata propagation."""
        super().__finalize__(other, method=method, **kwargs)
        return self

    @staticmethod
    def get_internal_path(row):
        """
        Extract offset, length, and path from a row's internal subfile information.
        """
        pattern: re.Pattern = re.compile(r"/vsisubfile/(\d+)_(\d+),(.+)")
        offset, length, path = pattern.match(row["internal:subfile"]).groups()

        # Adjust path for curl files
        if path.startswith("/vsicurl/"):
            path = path[9:]

        return int(offset), int(length), path

    def read(self, idx):
        """
        Read data based on the row's tortilla:file_format.
        """
        row = self.iloc[idx]
        if row["tortilla:file_format"] == "TORTILLA":
            offset, length, path = self.get_internal_path(row)
            return lazy_load(row["tortilla:offset"], path)
        elif row["tortilla:file_format"] == "BYTES":
            # Obtain the offset, length and internal path
            offset, length, path = self.get_internal_path(row)

            # Fetch the bytes
            if load_utils.is_valid_url(path):
                headers = {"Range": f"bytes={offset}-{offset + length - 1}"}
                response: requests.Response = requests.get(path, headers=headers)
                return response.content
            else:
                with open(path, "rb") as f:
                    f.seek(int(offset))
                    return f.read(int(length))
        else:
            return row["internal:subfile"]
