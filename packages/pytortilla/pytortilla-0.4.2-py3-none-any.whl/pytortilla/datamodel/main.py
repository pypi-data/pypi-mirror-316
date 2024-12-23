import datetime
import pathlib
from typing import Optional, Union, Literal, Callable, List
from tqdm import tqdm

import pandas as pd
import numpy as np
import pydantic
import concurrent.futures

from pytortilla.datamodel import utils


class STAC(pydantic.BaseModel):
    """SpatioTemporal Asset Catalog (STAC) metadata."""

    crs: str
    raster_shape: tuple[int, int]
    geotransform: tuple[float, float, float, float, float, float]
    centroid: Optional[str] = None
    time_start: Union[datetime.datetime, int]
    time_end: Optional[Union[datetime.datetime, int]] = None

    @pydantic.model_validator(mode="after")
    def check_times(cls, values):
        """Validates that the time_start is before time_end."""
        # If time_start is a datetime object, convert it to a timestamp
        if isinstance(values.time_start, datetime.datetime):
            values.time_start = values.time_start.timestamp()

        # If time_end is a datetime object, convert it to a timestamp
        if values.time_end is not None:
            if isinstance(values.time_end, datetime.datetime):
                values.time_end = values.time_end.timestamp()

            if values.time_start > values.time_end:
                raise ValueError(
                    f"Invalid times: {values.time_start} > {values.time_end}"
                )

        return values


class RAI(pydantic.BaseModel):
    """Metadata for Responsible AI (RAI) objectives."""

    populationdensity: Optional[Union[int, float]] = None
    female: Optional[Union[int, float]] = None
    womenreproducibleage: Optional[Union[int, float]] = None
    children: Optional[Union[int, float]] = None
    youth: Optional[Union[int, float]] = None
    elderly: Optional[Union[int, float]] = None


class Sample(pydantic.BaseModel):
    """A sample with STAC and RAI metadata."""

    id: str
    file_format: utils.GDAL_FILES
    path: pathlib.Path
    data_split: Optional[Literal["train", "validation", "test"]] = None 
    stac_data: Optional[STAC] = None
    rai_data: Optional[RAI] = None

    class Config:
        extra = "allow"

    def export_metadata(self):
        """
        Exports metadata as a dictionary, including STAC and RAI attributes, and any extra fields.
        """
        # If crs, raster_shape and geotransform are not provided, then create the stac:centroid
        if self.stac_data is not None:
            if self.stac_data.centroid is None:
                if (
                    self.stac_data.crs is not None
                    and self.stac_data.geotransform is not None
                    and self.stac_data.raster_shape is not None
                ):
                    self.stac_data.centroid = utils.raster_centroid(
                        crs=self.stac_data.crs,
                        geotransform=self.stac_data.geotransform,
                        raster_shape=self.stac_data.raster_shape,
                    )

        # Gather core metadata
        metadata = {
            "internal:path": str(self.path.resolve()),
            "tortilla:id": self.id,
            "tortilla:file_format": self.file_format,
            "tortilla:data_split": self.data_split,
            "tortilla:offset": 0,
            "tortilla:length": self.path.stat().st_size,
        }

        # Add STAC metadata if available
        if self.stac_data:
            metadata.update({
                "stac:crs": self.stac_data.crs,
                "stac:geotransform": self.stac_data.geotransform,
                "stac:raster_shape": self.stac_data.raster_shape,
                "stac:time_start": self.stac_data.time_start,
                "stac:time_end": self.stac_data.time_end,
                "stac:centroid": self.stac_data.centroid,
            })

        # Add RAI metadata if available
        if self.rai_data:
            metadata.update({
                "rai:populationdensity": self.rai_data.populationdensity,
                "rai:female": self.rai_data.female,
                "rai:womenreproducibleage": self.rai_data.womenreproducibleage,
                "rai:children": self.rai_data.children,
                "rai:youth": self.rai_data.youth,
                "rai:elderly": self.rai_data.elderly,
            })

        # Merge with additional metadata and remove None values
        metadata.update(
            {k: v for k, v in self.model_dump(
                exclude={"id", "path", "stac_data", "rai_data", "file_format", "data_split"},
                by_alias=True,
            ).items() if v is not None}
        )

        return metadata


class Samples(pydantic.BaseModel):
    samples: list[Sample]

    @pydantic.model_validator(mode="after")
    def check_samples(cls, values):
        """
        Validates that the samples have unique IDs and path exists.
        """        
        # Check if the ids are unique
        ids = [sample.id for sample in values.samples]
        if len(ids) != len(set(ids)):
            raise ValueError("The samples must have unique IDs.")
        
        # Check if the paths exist
        for sample in values.samples:
            if not sample.path.exists():
                raise FileNotFoundError(f"Path does not exist: {sample.path}")

        return values

    @staticmethod
    def process_chunk(chunk):
        return [sample.export_metadata() for sample in chunk]
    
    def export_metadata(self, nworkers: int=4, chunk_size: int=1000) -> pd.DataFrame:
        """
        Export metadata from samples in parallel.

        Args:
            samples (list): List of sample objects with `export_metadata` method.
            max_workers (int): Number of parallel workers.

        Returns:
            pd.DataFrame: DataFrame containing metadata.
        """

        chunks = np.array_split(self.samples, max(1, len(self.samples) // chunk_size))
        with concurrent.futures.ProcessPoolExecutor(max_workers=nworkers) as executor:
            results = executor.map(Samples.process_chunk, chunks)

        # Flatten results
        return pd.DataFrame([item for sublist in results for item in sublist])
    
    def deep_validator(self, read_function: Callable, max_workers: int = 4) -> List[str]:
        """
        Return a list of files that failed when trying to read them
        
        Args:
            read_function (Callable): Function to read a file.
            max_workers (int): Number of parallel threads.
        
        Returns:
            List[str]: List of file paths that failed to read.
        """
        # Get the paths of the samples
        internal_paths = [sample.path for sample in self.samples]

        def validate_file(file_path):
            try:
                read_function(file_path)
                return None  # Return None if the file was successfully read
            except Exception:
                return file_path  # Return the file path if it failed
        

        # Use ThreadPoolExecutor to parallelize the validation
        failed_files = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Use tqdm to display progress
            for result in tqdm(
                executor.map(validate_file, internal_paths),
                total=len(internal_paths),
                desc="Validating files",
            ):
                if result is not None:
                    failed_files.append(result)

        return failed_files