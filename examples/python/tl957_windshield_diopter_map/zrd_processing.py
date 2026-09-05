"""ZRD ray-tracing and ray-direction helpers for the windshield diopter workflow."""

import os
import numpy as np


def set_source_ray_counts(the_system, zosapi, active_source, source_ray_counts):
    """Enable the requested analysis rays for one source and disable the others."""
    for source_object, number_of_rays in source_ray_counts.items():
        source = the_system.NCE.GetObjectAt(source_object)
        if source is None:
            raise ValueError(f"NCE object {source_object} was not found.")

        analysis_rays_cell = source.GetObjectCell(
            zosapi.Editors.NCE.ObjectColumn.Par2
        )
        analysis_rays_cell.IntegerValue = (
            number_of_rays if source_object == active_source else 0
        )


def run_source_ray_trace(
    the_system,
    model_folder,
    source_object,
    number_of_rays,
):
    """Run an unsplit NSC ray trace for one source and save its ZRD file."""
    zrd_filename = f"source_{source_object}_{number_of_rays}_rays.ZRD"
    zrd_full_path = os.path.join(model_folder, zrd_filename)

    ray_trace = the_system.Tools.OpenNSCRayTrace()
    ray_trace.SplitNSCRays = False
    ray_trace.ScatterNSCRays = False
    ray_trace.UsePolarization = False
    ray_trace.IgnoreErrors = True
    ray_trace.SaveRays = True
    ray_trace.SaveRaysFile = zrd_filename
    ray_trace.ClearDetectors(0)
    ray_trace.RunAndWaitForCompletion()
    ray_trace.Close()

    print(
        f"\nRay trace finished for source {source_object}, "
        f"using {number_of_rays} analysis ray(s)."
    )
    print(f"ZRD file: {zrd_full_path}")
    return zrd_full_path


def _normalize(direction):
    direction = np.asarray(direction, dtype=float)
    magnitude = np.linalg.norm(direction)
    if magnitude == 0:
        raise ValueError("A zero-length ray direction was read from the ZRD file.")
    return direction / magnitude


def read_zrd_ray_directions(
    the_system,
    zosapi,
    zrd_full_path,
    source_object,
    detector_object_number,
):
    """Read first-segment and detector-hit directions for every parent ray.

    Returned dictionary keys are ZRD ray numbers. Each value contains:
    first_position, first_direction, detector_position, detector_direction,
    wave_index, and wavelength_um.
    """
    ray_data = {}
    zrd_reader = the_system.Tools.OpenRayDatabaseReader()

    try:
        zrd_reader.ZRDFile = zrd_full_path
        zrd_reader.RunAndWaitForCompletion()

        if zrd_reader.Succeeded == 0:
            raise RuntimeError(
                f"Could not read ZRD file: {zrd_full_path}\n"
                f"{zrd_reader.ErrorMessage}"
            )

        zrd_result = zrd_reader.GetResults()
        (
            success_next_ray,
            ray_number,
            wave_index,
            wavelength_um,
            number_of_segments,
        ) = zrd_result.ReadNextResult(0, 0, 0, 0)

        while success_next_ray:
            first_position = None
            first_direction = None
            detector_position = None
            detector_direction = None
            ray_status = zosapi.Tools.RayTrace.RayStatus(0)

            segment_data = zrd_result.ReadNextSegmentFull(
                1, 2, 3, 4, 5, ray_status, 7, 8, 9, 10,
                11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                21, 22, 23, 24, 25, 26, 27, 28, 29,
            )

            while segment_data[0]:
                hit_object = segment_data[3]
                current_position = np.array(
                    [segment_data[7], segment_data[8], segment_data[9]],
                    dtype=float,
                )
                current_direction = np.array(
                    [segment_data[10], segment_data[11], segment_data[12]],
                    dtype=float,
                )

                if first_direction is None:
                    first_position = current_position.copy()
                    first_direction = current_direction.copy()

                if hit_object == detector_object_number:
                    detector_position = current_position.copy()
                    detector_direction = current_direction.copy()

                segment_data = zrd_result.ReadNextSegmentFull(
                    1, 2, 3, 4, 5, ray_status, 7, 8, 9, 10,
                    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                    21, 22, 23, 24, 25, 26, 27, 28, 29,
                )

            if first_direction is None:
                print(f"Source {source_object}, Ray {ray_number}: no segments.")
            elif detector_direction is None:
                print(
                    f"Source {source_object}, Ray {ray_number}: "
                    f"did not hit detector object {detector_object_number}."
                )
            else:
                ray_data[ray_number] = {
                    "source_object": source_object,
                    "first_position": first_position,
                    "first_direction": _normalize(first_direction),
                    "detector_position": detector_position,
                    "detector_direction": _normalize(detector_direction),
                    "wave_index": wave_index,
                    "wavelength_um": wavelength_um,
                    "number_of_segments": number_of_segments,
                }

            (
                success_next_ray,
                ray_number,
                wave_index,
                wavelength_um,
                number_of_segments,
            ) = zrd_result.ReadNextResult(0, 0, 0, 0)

    finally:
        zrd_reader.Close()

    print(f"Source {source_object}: {len(ray_data)} valid detector rays read.")
    return ray_data
