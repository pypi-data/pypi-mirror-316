import os
import shutil
from collections import Counter

from alpineer import io_utils, misc_utils

from toffy.json_utils import read_json_file, rename_duplicate_fovs, rename_missing_fovs


def merge_partial_runs(cohort_dir, run_string):
    """Combines different runs together into a single folder of FOVs.

    Args:
        cohort_dir (str): the path to the directory containing the run folders
        run_string (str): the substring that each run folder has
    """
    # create folder to hold contents of all partial runs
    output_folder = os.path.join(cohort_dir, run_string)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # get list of matching subfolders
    # TODO: list_folders does not handle cases such as "run_dup2" correctly
    # need to add a fix in to alpineer to deal with this
    partial_folders = [f for f in os.listdir(cohort_dir) if run_string in f]
    partial_folders = [partial for partial in partial_folders if partial != run_string]

    if len(partial_folders) == 0:
        raise ValueError("No matching folders found for {}".format(run_string))

    # duplicate fovs check
    fovs_by_folder = {
        partial: io_utils.list_folders(os.path.join(cohort_dir, partial))
        for partial in partial_folders
    }
    fov_names = [
        fov for partial_folder_fovs in fovs_by_folder.values() for fov in partial_folder_fovs
    ]
    duplicate_fovs = [fov for fov, count in Counter(fov_names).items() if count > 1]

    # raise error to report any duplicate fovs
    if duplicate_fovs:
        for fov in duplicate_fovs:
            runs = [run_name for run_name, run_fovs in fovs_by_folder.items() if fov in run_fovs]
            print(f"{fov}: {runs}")
        raise ValueError(
            f"The following FOV folders exist in multiple partial runs: {duplicate_fovs}\n"
            "You need to determine which folders to keep and which to delete before merging."
        )

    # loop through each partial run folder and move the fov folders
    for partial in partial_folders:
        fov_folders = io_utils.list_folders(os.path.join(cohort_dir, partial))

        # copy each fov from partial folder into output folder
        for fov in fov_folders:
            new_path = os.path.join(output_folder, fov)
            shutil.move(os.path.join(cohort_dir, partial, fov), new_path)

        # remove partial folder
        shutil.rmtree(os.path.join(cohort_dir, partial))


def combine_runs(cohort_dir):
    """Combines FOVs from different runs together, using the run name as a unique identifier.

    Args:
        cohort_dir (str): path to the directory containing individual run folders
    """
    # get all runs
    run_folders = io_utils.list_folders(cohort_dir)

    # create folder to hold all images
    output_dir = os.path.join(cohort_dir, "image_data")
    os.makedirs(output_dir)

    # loop over each run
    for run in run_folders:
        run_path = os.path.join(cohort_dir, run)

        fovs = io_utils.list_folders(run_path)
        for fov in fovs:
            shutil.move(os.path.join(run_path, fov), os.path.join(output_dir, run + "_" + fov))

        shutil.rmtree(run_path)


def rename_fov_dirs(json_run_path, default_run_dir, output_run_dir=None):
    """Renames FOV directories with default_name to have custom_name sourced from the run JSON file.

    Args:
        json_run_path (str): path to the JSON run file which contains the custom name values
        default_run_dir (str): directory containing default named FOVs
        output_run_dir (str): directory for renamed FOVs. If None, changed in place

    Raises:
        KeyError: issue reading keys from the JSON file
        ValueError: there exist default named directories that are not described in the run file
        UserWarning: not all custom names from the run file have an existing directory

    """
    io_utils.validate_paths(json_run_path)
    io_utils.validate_paths(default_run_dir)

    # check that new_dir doesn't already exist
    if output_run_dir is not None:
        if os.path.exists(output_run_dir):
            raise ValueError(f"The new directory supplied already exists: {output_run_dir}")

    run_metadata = read_json_file(json_run_path)

    # check for missing or duplicate fov names
    run_metadata = rename_missing_fovs(run_metadata)
    run_metadata = rename_duplicate_fovs(run_metadata)

    # retrieve custom names and number of scans for each fov, construct matching default names
    fov_scan = dict()
    for fov in run_metadata.get("fovs", ()):
        custom_name = fov.get("name")
        run_order = fov.get("runOrder")
        scans = fov.get("scanCount")

        # fovs with multiple scans have scan    number specified
        for scan in range(1, scans + 1):
            default_name = f"fov-{run_order}-scan-{scan}"
            name_ext = f"-{scan}" if scans > 1 else ""
            fov_scan[default_name] = custom_name + name_ext

    # retrieve current default directory names, check if already renamed
    old_dirs = io_utils.list_folders(default_run_dir, "fov")
    if len(old_dirs) == 0:
        raise ValueError(f"All FOV folders in {default_run_dir} have already been renamed")

    # check if custom fov names & scan counts match the number of existing default directories
    misc_utils.verify_in_list(
        warn=True, fovs_in_run_file=list(fov_scan.keys()), existing_fov_folders=old_dirs
    )
    misc_utils.verify_in_list(existing_fov_folders=old_dirs, fovs_in_run_file=list(fov_scan.keys()))

    # if no output specified, FOVs will be renamed inplace
    if output_run_dir is None:
        output_run_dir = default_run_dir

    # change the default directory names to custom names
    for folder in old_dirs:
        original_path = os.path.join(default_run_dir, folder)
        new_path = os.path.join(output_run_dir, fov_scan[folder])

        if output_run_dir == default_run_dir:
            # rename in place
            os.rename(original_path, new_path)
        else:
            # copy to new folder
            shutil.copytree(original_path, new_path)


def rename_fovs_in_cohort(run_names, processed_base_dir, cohort_path, bin_base_dir):
    """Renames the FOVs in each of the supplied runs.

    Args:
        run_names (list): list of runs to rename
        processed_base_dir (str): the directory containing the processed data for each
        cohort_path (str): the path to the folder where renamed FOVs will be saved
        bin_base_dir (str): the directory holding the bin files for each run
    """
    for run in run_names:
        print("Renaming FOVs in {}".format(run))
        input_dir = os.path.join(processed_base_dir, run)
        output_dir = os.path.join(cohort_path, run)
        json_path = os.path.join(bin_base_dir, run, run + ".json")
        rename_fov_dirs(
            json_run_path=json_path,
            default_run_dir=input_dir,
            output_run_dir=output_dir,
        )
