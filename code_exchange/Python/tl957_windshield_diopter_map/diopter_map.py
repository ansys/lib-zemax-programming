# Copyright (C) 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""TL 957-style windshield diopter calculation and plotting helpers."""

import csv
import math
import os
import numpy as np
import matplotlib.pyplot as plt


def angle_between_directions(direction_1, direction_2):
    """Return the unsigned angle in radians between two unit directions."""
    dot_product = float(np.dot(direction_1, direction_2))
    return math.acos(float(np.clip(dot_product, -1.0, 1.0)))


def calculate_diopter_map(
    all_source_ray_data,
    center_source_object,
    surrounding_source_objects,
    delta_x_m,
):
    """Calculate one maximum diopter value for each corresponding ray number."""
    center_rays = all_source_ray_data[center_source_object]
    results = {}

    for ray_number, center_ray in center_rays.items():
        center_deflection = angle_between_directions(
            center_ray["first_direction"],
            center_ray["detector_direction"],
        )

        distortion_by_source = {}
        missing_sources = []

        for source_object in surrounding_source_objects:
            comparison_ray = all_source_ray_data.get(source_object, {}).get(ray_number)
            if comparison_ray is None:
                missing_sources.append(source_object)
                continue

            comparison_deflection = angle_between_directions(
                comparison_ray["first_direction"],
                comparison_ray["detector_direction"],
            )
            distortion_by_source[source_object] = abs(
                comparison_deflection - center_deflection
            )

        if missing_sources:
            print(
                f"Ray {ray_number}: skipped because source(s) "
                f"{missing_sources} have no matching detector ray."
            )
            continue

        maximum_source = max(distortion_by_source, key=distortion_by_source.get)
        maximum_distortion_rad = distortion_by_source[maximum_source]

        results[ray_number] = {
            "position": center_ray["first_position"],
            "center_deflection_rad": center_deflection,
            "distortion_by_source_rad": distortion_by_source,
            "maximum_source": maximum_source,
            "maximum_distortion_rad": maximum_distortion_rad,
            "diopter": maximum_distortion_rad / delta_x_m,
        }

    return results


def save_diopter_results_csv(diopter_results, output_path):
    """Save ray-by-ray diopter data for validation and reuse."""
    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            [
                "ray_number",
                "x",
                "y",
                "z",
                "maximum_source",
                "maximum_distortion_rad",
                "diopter_D",
            ]
        )
        for ray_number, result in diopter_results.items():
            result = diopter_results[ray_number]
            x, y, z = result["position"]
            writer.writerow(
                [
                    ray_number,
                    x,
                    y,
                    z,
                    result["maximum_source"],
                    result["maximum_distortion_rad"],
                    result["diopter"],
                ]
            )


def plot_diopter_map(
    diopter_results,
    grid_rows,
    grid_columns,
    model_folder,
):
    """Create a row x column diopter heat map and save PNG and CSV outputs."""
    diopter_map = np.full((grid_rows, grid_columns), np.nan, dtype=float)

    for ray_number, result in diopter_results.items():
        zero_based_index = ray_number - 1
        row_index = zero_based_index // grid_columns
        column_index = zero_based_index % grid_columns

        if 0 <= row_index < grid_rows and 0 <= column_index < grid_columns:
            diopter_map[row_index, column_index] = result["diopter"]

    valid_count = int(np.count_nonzero(np.isfinite(diopter_map)))
    expected_count = grid_rows * grid_columns
    print(f"Diopter grid: {valid_count} valid values out of {expected_count}.")

    # Make the displayed map horizontal.
    # diopter_map.shape returns: (number_of_rows, number_of_columns)
    if diopter_map.shape[0] > diopter_map.shape[1]:
        display_map = diopter_map.T
        x_axis_label = "Original grid row"
        y_axis_label = "Original grid column"
    else:
        display_map = diopter_map
        x_axis_label = "Grid column"
        y_axis_label = "Grid row"
    
    
    figure, axis = plt.subplots(figsize=(12, 6))
    image = axis.imshow(
        display_map,
        origin="lower",
        cmap="viridis",
        interpolation="nearest",
        aspect="equal",
    )
    colorbar = figure.colorbar(image, ax=axis)
    colorbar.set_label("Optical power [D]")
    axis.set_title("Windshield Diopter Map")
    axis.set_xlabel("Grid column")
    axis.set_ylabel("Grid row")
    axis.set_xticks(range(display_map.shape[1]))
    axis.set_yticks(range(display_map.shape[0]))
    figure.tight_layout()

    png_path = os.path.join(model_folder, "windshield_diopter_map.png")
    csv_path = os.path.join(model_folder, "windshield_diopter_map.csv")
    figure.savefig(png_path, dpi=300, bbox_inches="tight")
    save_diopter_results_csv(diopter_results, csv_path)

    print(f"Diopter map saved to: {png_path}")
    print(f"Diopter data saved to: {csv_path}")
    plt.show()
    return diopter_map
