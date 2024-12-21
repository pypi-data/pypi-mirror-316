# Copyright (C) 2024 Andrea Raffo <andrea.raffo@ibv.uio.no>
#
# SPDX-License-Identifier: MIT

import os

import h5py
import hictkpy
import numpy as np

from . import IO


def _raise_invalid_bin_type_except(f: hictkpy.File):
    raise RuntimeError(f"Only files with a uniform bin size are supported, found \"{f.attributes()['bin-type']}\".")


def cmap_loading(path: os.PathLike, resolution: int):
    try:
        if not isinstance(resolution, int):
            raise TypeError("resolution must be an integer.")

        if resolution <= 0:
            raise ValueError("resolution must be greater than zero.")

        if hictkpy.is_scool_file(path):
            raise RuntimeError(".scool files are not currently supported.")
        if hictkpy.is_cooler(path):
            f = hictkpy.File(path)
            if f.resolution() == 0:
                _raise_invalid_bin_type_except(f)
            if f.resolution() != resolution:
                raise RuntimeError(f"expected {resolution} resolution, found {f.resolution()}.")
        else:
            f = hictkpy.MultiResFile(path)[resolution]
    except RuntimeError as e:
        raise RuntimeError(f'error opening file "{path}"') from e

    if f.attributes().get("bin-type", "fixed") != "fixed":
        _raise_invalid_bin_type_except(f)

    # Retrieve metadata:
    chr_starts = [0]  # left ends of each chromosome  (in matrix coordinates)
    chr_ends = []  # right ends of each chromosome (in matrix coordinates)
    chr_sizes = []  # integer bp lengths, one per chromosome
    for bp_length in f.chromosomes().values():
        chr_sizes.append(bp_length)
        chr_ends.append(chr_starts[-1] + int(np.ceil(bp_length / resolution)))
        chr_starts.append(chr_ends[-1])
        # print(f"{chr_starts[-2]}-{chr_ends[-1]}-{chr_sizes[-1]}")
    chr_starts.pop(-1)

    return f, chr_starts, chr_ends, chr_sizes


def chromosomes_to_study(chromosomes, length_in_bp, min_size_allowed):
    # Extract the list of chromosomes:
    chr_ids = list(range(len(chromosomes)))
    c_pairs = list(zip(chr_ids, chromosomes))

    # Remove overly-short chromosomes:
    surviving_indices = [i for i, e in enumerate(length_in_bp) if e > min_size_allowed]
    deleted_indices = [i for i, e in enumerate(length_in_bp) if e <= min_size_allowed]
    if len(deleted_indices) > 0:
        print(
            f"{IO.ANSI.RED}ATT: The following chromosomes are discarded because shorter than --min-chrom-size = "
            f"{min_size_allowed} bp: {[chromosomes[i] for i in deleted_indices]}{IO.ANSI.ENDC}"
        )
        c_pairs = [c_pairs[i] for i in surviving_indices]

        # If there is no chromosome left, exit:
        if len(c_pairs) == 0:
            raise ValueError(f"\nNo chromosome is long enough... decrease the parameter --min-chrom-size")

    return c_pairs


def define_RoI(where_roi, chr_start, chr_end, resolution):
    # Region of Interest (RoI) in genomic and matrix coordinates:
    if where_roi == "middle":
        RoI_length = 2000000
        e1 = ((chr_end - chr_start) * resolution - RoI_length) / 2
        e2 = e1 + RoI_length
        RoI = dict()
        RoI["genomic"] = [int(e1), int(e2), int(e1), int(e2)]  # genomic coordinates
        RoI["matrix"] = [int(roi / resolution) for roi in RoI["genomic"]]  # matrix coordinates
    elif where_roi == "start":
        RoI_length = 2000000
        e1 = 0
        e2 = e1 + RoI_length
        RoI = dict()
        RoI["genomic"] = [int(e1), int(e2), int(e1), int(e2)]  # genomic coordinates
        RoI["matrix"] = [int(roi / resolution) for roi in RoI["genomic"]]  # matrix coordinates
    else:
        RoI = None

    return RoI


# Define a function to visit groups and save terminal group names in a list
def save_terminal_groups(name, obj):
    group_names = []
    if isinstance(obj, h5py.Group):
        has_subgroups = any(isinstance(child_obj, h5py.Group) for _, child_obj in obj.items())
        if not has_subgroups:
            group_names.append(name)
    return group_names


# Define a function to visit datasets and save their names in a list
def save_all_datasets(name, obj):
    dataset_names = []
    if isinstance(obj, h5py.Dataset):  # check if obj is a group or dataset
        dataset_names.append(name)
    return dataset_names
