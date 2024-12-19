#!/usr/bin/env python
"""
A script that compares reading images with cv2 and tifffile for speed.
"""

import os
import time
import cv2
import numpy as np
import tifffile
import imageio.v3 as imageio
import skimage.io


def main():
    # Get all DAPI .tif file names in the directory
    file_path = "/mnt/HDSCA_Development/data/0B58703"
    file_names = [os.path.join(file_path, f"Tile{i:06d}.tif") for i in range(100, 200)]

    print(f"Number of files: {len(file_names)}")
    # cv2
    start = time.time()
    cv2_results = []
    for file_name in file_names:
        img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
        # Check that we are getting the same results
        cv2_results.append(np.mean(img))
        # Print on the same line over and over
        # print(f"cv2: {os.path.basename(file_name)}")
    end = time.time()
    print(f"cv2: {end - start}")

    # tifffile
    start = time.time()
    tifffile_results = []
    for file_name in file_names:
        img = tifffile.imread(file_name)
        # Check that we are getting the same results
        tifffile_results.append(np.mean(img))
        # Print on the same line over and over
        # print(f"tifffile: {os.path.dirname(file_name)}", end="\r")
    end = time.time()
    print(f"tifffile: {end - start}")

    # imageio
    start = time.time()
    imageio_results = []
    for file_name in file_names:
        img = imageio.imread(file_name)
        # Check that we are getting the same results
        imageio_results.append(np.mean(img))
        # Print on the same line over and over
        # print(f"imageio: {os.path.dirname(file_name)}", end="\r")
    end = time.time()
    print(f"imageio: {end - start}")

    # skimage
    start = time.time()
    skimage_results = []
    for file_name in file_names:
        img = skimage.io.imread(file_name)
        # Check that we are getting the same results
        skimage_results.append(np.mean(img))
        # Print on the same line over and over
        # print(f"skimage: {os.path.dirname(file_name)}", end="\r")
    end = time.time()
    print(f"skimage: {end - start}")

    # Check that we are getting the same results
    assert cv2_results == tifffile_results
    assert cv2_results == imageio_results
    assert cv2_results == skimage_results


if __name__ == "__main__":
    main()
