import os
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import xarray as xr
from alpineer.image_utils import save_image
from skimage import draw, exposure, filters, measure, restoration, util


@dataclass
class StreakData:
    """Contains data for correcting the streaks consisting of binary masks, dataframes with
    location and size properties, a directory for saving, and the shape / channel for mask
    generation.

    Args:
        shape (tuple): The shape of the image / fov.
        fov (str): The name of the fov being processed.
        streak_channel (str): The specific channel name used to create the masks.
        corrected_dir (Path): The directory used to save the corrected tiffs and data in.
        streak_mask (np.ndarray): The first binary mask indicating candidate streaks.
        streak_df (pd.DataFrame): A dataframe, containing the location, area, and eccentricity
        of each streak.
        filtered_streak_mask (np.ndarray): A binary mask with out the false streaks.
        filtered_streak_df (pd.DataFrame): A subset of the `streak_df` containing location, area
        and eccentricity values of the filtered streaks.
        boxed_streaks (np.ndarray): An optional binary mask containing an outline for each
        filtered streaks.
        corrected_streak_mask (np.ndarray): An optional binary mask containing the lines used for
        correcting the streaks.
    """

    shape: Tuple[int, int] = None
    fov: str = None
    streak_channel: str = None
    corrected_dir: Path = None
    streak_mask: np.ndarray = None
    streak_df: pd.DataFrame = None
    filtered_streak_mask: np.ndarray = None
    filtered_streak_df: pd.DataFrame = None
    boxed_streaks: np.ndarray = None
    corrected_streak_mask: np.ndarray = None


def _get_save_dir(data_dir: Path, name: str, ext: str) -> Path:
    """A helper function which generates the path where the masks and DataFrames
    are saved to.

    Args:
        data_dir (Path): The directory to save the binary masks and DataFrames.
        name (str): The field of the DataClass to be saved.
        ext (str): The file extension, either `csv` or `tiff`.

    Returns:
        Path: Returns the path where the file is saved to.
    """
    return Path(data_dir, name + f".{ext}")


def _save_streak_data(streak_data: StreakData, name: str):
    """Helper function for saving tiff binary masks and dataframes.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
        name (str): The field of the DataClass to be saved.
    """
    data_dir = streak_data.corrected_dir / f"streak_data_{streak_data.streak_channel}"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data = getattr(streak_data, name)
    st = partial(_get_save_dir, data_dir, name)

    if type(data) is np.ndarray:
        save_image(st("tiff"), data)
    elif type(data) is pd.DataFrame:
        data.to_csv(st("csv"), index=True)


def _save_streak_masks(streak_data: StreakData):
    """Saves the data in StreakData as a tiff file if it's a Numpy array, and a csv if it is a
    Pandas DataFrame. Useful for visualization and debugging.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
    """
    fields = [
        "streak_mask",
        "streak_df",
        "filtered_streak_mask",
        "filtered_streak_df",
        "boxed_streaks",
        "corrected_streak_mask",
    ]
    for field in fields:
        _save_streak_data(streak_data, name=field)


def _make_binary_mask(
    input_image: np.ndarray,
    gaussian_sigma: float = 5.00,
    gamma: float = 4.0,
    gamma_gain: float = 1.00,
    log_gain: float = 1.00,
    pmin: int = 2,
    pmax: int = 98,
    threshold: float = 0.35,
    wavelet: str = "db2",
    mode: str = "soft",
    rescale_sigma: bool = True,
) -> np.ndarray:
    """Performs a series of denoiseing, filtering, and exposure adjustments to create a binary
    mask for the given input image.

    Args:
        input_image (np.ndarray): The image to perform the streak masking on.
        gaussian_sigma (float, optional): Parameter for `skimage.filters.gaussian`. Defaults to
        5.00.
        gamma (float, optional): Parameter for `skimage.exposure.adjust_gamma`. Defaults to 3.80.
        gamma_gain (float, optional): Parameter for `skimage.exposure.adjust_gamma`. Defaults to
        0.10.
        log_gain (float, optional): Parameter for `skimage.exposure.adjust_log`. Defaults to 1.00.
        pmin (int, optional): Lower bound for the `np.percentile` threshold, used for rescaling
        the intensity. Defaults to 2.
        pmax (int, optional): Upper bound for the `np.percentile` threshold, used for rescaling
        the intensity. Defaults to 98.
        threshold (float, optional): The lower bound for pixel values used to create a binary mask.
        Defaults to 0.35.
        wavelet (str): The type of wavelet to perform and can be any of the options
        `pywt.wavelist` outputs. Defaults to "db2".
        mode (str): An optional argument to choose the type of denoising performed. Its noted that
        choosing soft thresholding given additive noise finds the best approximation of the
        original image. Defaults to "soft".
        rescale_sigma (bool): If False, no rescaling of the user-provided `sigma` will be
        performed. The default of `True` rescales `sigma` appropriately if the image is rescaled
        internally. Defaults to "True".


    Returns:
        np.ndarray: The binary mask containing all of the candidate strokes.
    """
    input_image = restoration.denoise_wavelet(
        input_image, wavelet=wavelet, mode=mode, rescale_sigma=rescale_sigma
    )
    # Rescale the intensity using percentile ranges
    pmin_v, pmax_v = np.percentile(input_image, (pmin, pmax))
    input_image = exposure.rescale_intensity(input_image, in_range=(pmin_v, pmax_v))

    # Laplace filter to get the streaks
    input_image = filters.laplace(input_image, ksize=3)
    input_image = exposure.rescale_intensity(input_image, out_range=(0, 1))

    # Smoothing
    input_image = filters.gaussian(input_image, sigma=(0, gaussian_sigma))  # (y, x)

    # Exposure Adjustments
    input_image = exposure.adjust_gamma(input_image, gamma=gamma, gain=gamma_gain)
    input_image = exposure.adjust_log(input_image, gain=log_gain, inv=True)
    input_image = exposure.rescale_intensity(input_image, out_range=(0, 1))

    # apply threshold
    binary_mask = input_image > threshold

    return binary_mask


def _make_mask_dataframe(streak_data: StreakData, min_length: int = 70) -> None:
    """Converts the binary mask created by `_make_binary_mask` into a dataframe for
    processing. The streaks are labeled, pixel information (min_row, min_col, max_row, max_col)
    is evaluated and streak lengths / areas are calculated. In addition the `min_length` argument
    allows the user to filter out streaks shorter than it.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
        min_length (int): The lower threshold for filtering streaks in pixels. Defaults to 70.
        eccentricity_value (float): The threshold to filter out eccentricities lower than this
    """
    # Label all the candidate streaks
    labeled_streaks = measure.label(streak_data.streak_mask, connectivity=2, return_num=False)

    # if streaks detected, filter dataframe
    if len(np.unique(labeled_streaks)) > 1:
        # Gather properties of all the candidate streaks using regionprops.
        region_properties = measure.regionprops_table(
            label_image=labeled_streaks,
            cache=True,
            properties=[
                "label",
                "bbox",
                "eccentricity",
                "area",
            ],
        )

        # Convert dictionary of region properties to DataFrame.
        streak_data.streak_df = pd.DataFrame(region_properties)

        # Rename the bounding box columns.
        streak_data.streak_df.rename(
            {
                "bbox-0": "min_row",
                "bbox-1": "min_col",
                "bbox-2": "max_row",
                "bbox-3": "max_col",
                "area": "length",
            },
            axis="columns",
            inplace=True,
        )
        # Give the index column a name.
        streak_data.streak_df.index.names = ["index"]

        # Filter out eccentricities that are less than 0.99999 (only keep straight lines)
        # Filter out small areas (small lines)
        eccentricity_value = 0.9999999
        streak_data.filtered_streak_df = streak_data.streak_df.query(
            f"eccentricity > {eccentricity_value} and length > {min_length}"
        )
    else:
        # otherwise, make a blank df
        blank_df = pd.DataFrame({"min_row": [], "min_col": [], "max_row": [], "max_col": []})
        streak_data.filtered_streak_df = blank_df


def _make_filtered_mask(streak_data: StreakData) -> None:
    """Visualization Utility. Uses the filtered streak dataframe to create a binary mask, where
    1 indicates the pixels that will get corrected. This mask can be later saved and used for
    visualization purposes.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
    """
    streak_data.filtered_streak_mask = np.zeros(shape=streak_data.shape, dtype=np.uint8)
    for region in streak_data.filtered_streak_df.itertuples():
        streak_data.filtered_streak_mask[
            region.min_row : region.max_row, region.min_col : region.max_col
        ] = 1


def _make_box_outline(streak_data: StreakData) -> None:
    """Visualization Utility. Creates a box outline for each binary streak using the filtered
    streak dataframe. Outlines the streaks that will get corrected. This mask can be later saved
    and used for visualization purposes.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
    """
    padded_image = np.pad(
        np.zeros(shape=streak_data.shape, dtype=np.uint8), pad_width=(1, 1), mode="edge"
    )
    for region in streak_data.filtered_streak_df.itertuples():
        y, x = draw.rectangle_perimeter(
            start=(region.min_row + 1, region.min_col + 1),
            end=(region.max_row, region.max_col),
            clip=True,
            shape=streak_data.shape,
        )
        padded_image[y, x] = 1
    streak_data.boxed_streaks = util.crop(padded_image, crop_width=(1, 1))


def _make_correction_mask(streak_data: StreakData) -> None:
    """Visualization Utility. Creates the correction mask for each binary streak using the
    filtered streak DataFrame. Marks pixels which will be used for the correction method.
    This mask can be later saved and used for visualization purposes.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
    """
    padded_image = np.pad(
        np.zeros(shape=streak_data.shape, dtype=np.uint8), pad_width=(1, 1), mode="edge"
    )

    for region in streak_data.filtered_streak_df.itertuples():
        padded_image[region.min_row, region.min_col + 1 : region.max_col + 1] = np.ones(
            shape=(region.max_col - region.min_col)
        )
        padded_image[region.max_row + 1, region.min_col + 1 : region.max_col + 1] = np.ones(
            shape=(region.max_col - region.min_col)
        )

    streak_data.corrected_streak_mask = util.crop(padded_image, crop_width=(1, 1))


def _correct_streaks(streak_data: StreakData, input_image: np.ndarray) -> np.ndarray:
    """Corrects the streaks for the input image. Uses masks in the streak_data Dataclass.
    Performs the correction by averaging the pixels above and below the streak.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
        input_image (np.ndarray): The channel which is being corrected.

    Returns:
        np.ndarray: The corrected image.
    """
    # Pad the image for edge cases.
    padded_image = np.pad(input_image.copy(), pad_width=(1, 1), mode="edge")
    corrected_image = padded_image.copy()
    # Correct each streak
    for region in streak_data.filtered_streak_df.itertuples():
        corrected_image[region.max_row, region.min_col : region.max_col] = _correct_mean_alg(
            padded_image,
            region.min_row,
            region.max_row,
            region.min_col,
            region.max_col,
        )
    # Crop and return the 'unpadded' image.
    return util.crop(corrected_image, crop_width=(1, 1), copy=True)


def _correct_mean_alg(
    input_image: np.ndarray, min_row: int, max_row: int, min_col: int, max_col: int
) -> np.ndarray:
    """Performs streak-wise correction by: setting the value of each pixel in the streak to the
    mean of pixel above and below it.

    Args:
        input_image (np.ndarray): The channel to be corrected.
        min_row (int): The minimum row index of the streak. The y location where the streak
        starts.
        max_row (int): The maximum row index of the streak. The y location where the streak ends.
        min_col (int): The minimum column index of the streak. The x location where the streak
        starts.
        max_col (int): The maximum column index of the streak. The x location where the streak
        ends.

    Returns:
        np.ndarray: Returns the corrected streak.
    """
    streak_corrected: np.ndarray = np.mean(
        [
            # Row above
            input_image[min_row, min_col + 1 : max_col + 1],
            # Row below
            input_image[max_row + 1, min_col + 1 : max_col + 1],
        ],
        axis=0,
        dtype=input_image.dtype,
    )

    return streak_corrected


def save_corrected_channels(
    streak_data: StreakData,
    corrected_channels: xr.DataArray,
    data_dir: Path,
    save_streak_data=False,
) -> None:
    """Saves the corrected images in a subdirectory of `fov_dir`.

    Args:
        streak_data (StreakData): An instance of the StreakData Dataclass, holds all necessary
        data for streak correction.
        corrected_channels (xr.DataArray): The DataArray continaing the set of corrected channels.
        data_dir (Path): A directory containing the fov and all it's channels for correction.
        save_streak_data (bool): Saves the binary masks and dataframes contained in StreakData.

    """
    # Create the directory to store the corrected tiffs
    streak_data.corrected_dir = Path(data_dir, streak_data.fov + "-corrected")
    if not os.path.exists(streak_data.corrected_dir):
        os.makedirs(streak_data.corrected_dir)

    # Save the corrected tiffs
    for channel in corrected_channels.channels.values:
        img: np.ndarray = corrected_channels.loc[:, :, channel].values
        fp = Path(streak_data.corrected_dir, channel + ".tiff")
        save_image(fp, img)

    # Save streak masks
    if save_streak_data:
        _save_streak_masks(streak_data=streak_data)


def streak_correction(
    fov_data: xr.DataArray,
    streak_channel: str = "Noodle",
    visualization_masks: bool = False,
) -> Tuple[xr.DataArray, StreakData]:
    """Takes an DataArray representation of a fov and a user specified image for streak detection.
    Once all the streaks have been detected on that image, they are corrected via an averaging
    method. The function can also returns a DataClass containing various binary masks and
    dataframes which were used for filtering and correction when `visualization_masks` is True.

    Args:
        fov_data (xr.DataArray): The data structure containing all of the channels to be processed
        and corrected.
        streak_channel (str, optional): The name of the channel used (without the file extension)
        for identifying the streaks. Defaults to "Noodle".
        visualization_masks (bool, optional): If `True`, adds binary masks for visualization to
        the StreakData Dataclass which gets returned. Defaults to "False".

    Returns:
        Tuple[xr.DataArray, StreakData]: A tuple of the DataArray housing the corrected images,
        and the streak data containing masks and dataframes for analysis and visualization.
    """
    # Initialize the streak DataClass
    streak_data = StreakData()
    streak_data.streak_channel = streak_channel
    streak_data.fov = fov_data.fovs.values[0]

    fov_data = fov_data[0, ...]

    #  Get the correct channel for mask generation.
    with fov_data.loc[:, :, streak_channel] as channel_image:
        streak_data.shape = channel_image.shape
        # Create and filter the binary masks
        streak_data.streak_mask = _make_binary_mask(input_image=channel_image)
        _make_mask_dataframe(streak_data=streak_data)

    # Get the file names.
    channel_fn = fov_data.channels.values.tolist()

    # Initialize the corrected image fov dimensions.
    fov_dim_size: int = len(channel_fn)
    row_size, col_size = streak_data.shape
    cor_img_data = np.zeros(shape=(row_size, col_size, fov_dim_size), dtype=fov_data.dtype)

    # Correct streaks and add them to the np.array
    for idx, channel in enumerate(fov_data.channels.values):
        input_channel = fov_data.loc[:, :, channel]
        cor_img_data[:, :, idx] = _correct_streaks(
            streak_data=streak_data, input_image=input_channel
        )

    # Create xarray from np.array
    corrected_channels = xr.DataArray(
        data=cor_img_data,
        coords=[range(row_size), range(col_size), fov_data.channels.values],
        dims=["rows", "cols", "channels"],
    )

    # Add mask information / visualization masks
    if visualization_masks:
        _make_box_outline(streak_data=streak_data)
        _make_correction_mask(streak_data=streak_data)
        _make_filtered_mask(streak_data=streak_data)

    return (corrected_channels, streak_data)
