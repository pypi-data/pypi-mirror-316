import os, glob
from argparse import ArgumentParser
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


def distance(point1, point2):
    """Calculate the Euclidean distance between two 3D points."""
    return np.linalg.norm(np.array(point1) - np.array(point2))


def angle_between_points(point1, point2, point3):
    """Calculate the angle (in radians) between three points in 3D space.

    Args:
        point1 (np.ndarray): Coordinates of the first point [x1, y1, z1].
        point2 (np.ndarray): Coordinates of the second point (vertex) [x2, y2, z2].
        point3 (np.ndarray): Coordinates of the third point [x3, y3, z3].

    Returns:
        float: Angle in radians between the three points.
    """
    # Create vectors from point2 to point1 and point2 to point3
    vector1 = point1 - point2
    vector2 = point3 - point2

    # Calculate the dot product and magnitudes of the vectors
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    # Calculate the angle using the cosine formula
    cos_theta = dot_product / (magnitude1 * magnitude2)

    # Return the angle in radians
    return np.arccos(np.clip(cos_theta, -1.0, 1.0))


def order_circle_coordinates(current_coord, all_coords):
    """
    Orders coordinates in a circular manner starting from the minimum coordinates.

    Parameters:
    min_coords (ndarray): Array of minimum coordinates to start ordering from.
    all_coords (list of ndarray): List of arrays containing coordinates to order.

    Returns:
    list: Ordered circle coordinates.
    """
    circle_coords = [current_coord]
    for coords in all_coords:
        circle_coords.append(
            coords[np.argmin(cdist(current_coord.reshape(1, 3), coords))]
        )

    ordered_circle_coords = []
    current = circle_coords[0]
    idx = 0
    while len(circle_coords) > 0:
        ordered_circle_coords.append(current)
        circle_coords.pop(idx)
        if len(circle_coords) == 0:
            break
        old = current
        current = circle_coords[
            np.argmin(
                cdist(
                    np.array(old).reshape(1, 3), np.array(circle_coords).reshape(-1, 3)
                )
            )
        ]
        idx = np.argmin(
            cdist(np.array(old).reshape(1, 3), np.array(circle_coords).reshape(-1, 3))
        )

    return ordered_circle_coords


def estimate_circularity():

    parser = ArgumentParser(
        description="Estimate the circularity of an axoneme/partial axoneme by using angles between edges."
    )
    parser.add_argument(
        "input_directory",
        help="Input directory containing .csv files with invidually segmented axonemes; this directory is outputted by `segment_axonemes.py`.",
    )

    args = parser.parse_args()

    input_directory = args.input_directory
    csvs = sorted(glob.glob(f"{input_directory}/*.csv"))

    for i, csv in enumerate(csvs):

        df = pd.read_csv(csv)
        all_coords = [
            df.loc[df.label == label][["x", "y", "z"]].values
            for label in sorted(np.unique(df.label.values))
        ]
        regular_angle = np.pi - (2 * np.pi / 9)

        def score_function(x):
            """
            Output a circularity score according to the supplied function. Larger values correspond to lower circularity values, and the absolute largest acceptable mean is 40º.
            """
            return 1 + (x / (x - (4 * np.pi / 9)))

        min_coords_idx = np.argmin([len(coords) for coords in all_coords])
        min_coords = all_coords.pop(min_coords_idx)
        maes = list()
        for coord in min_coords:
            ordered_circle_coords = order_circle_coordinates(coord, all_coords)

            if len(ordered_circle_coords) >= 5 and len(ordered_circle_coords) < 9:
                ordered = np.array(ordered_circle_coords)

                errors = 0
                for k in np.arange(ordered.shape[0] - 3):
                    current_angle = angle_between_points(
                        ordered[k], ordered[k + 1], ordered[k + 2]
                    )
                    errors += np.abs(regular_angle - current_angle)
                maes.append(errors / ordered.shape[0])

            elif len(ordered_circle_coords) == 9:
                ordered = np.vstack([ordered_circle_coords, ordered_circle_coords[0]])

                errors = 0
                for k in np.arange(ordered.shape[0] - 3):
                    current_angle = angle_between_points(
                        ordered[k], ordered[k + 1], ordered[k + 2]
                    )
                    errors += np.abs(regular_angle - current_angle)
                maes.append(errors / ordered.shape[0])

            else:
                pass

        if np.unique(df.label.values).shape[0] >= 5:
            print(
                f"There are {np.unique(df.label.values).shape[0]} doublets in {os.path.split(csv)[-1]}!\nCircularity: {score_function(np.array(maes).mean())}"
            )


if __name__ == "__main__":
    estimate_circularity()
