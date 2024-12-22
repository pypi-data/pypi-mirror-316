import os
import glob
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from argparse import ArgumentParser


def load_coordinates(file_path):
    # Load coordinates
    coords = pd.read_csv(
        file_path, delim_whitespace=True, header=None, names=["z", "x", "y"]
    )
    coords = coords[["x", "y", "z"]]  # Reorder columns to x, y, z
    return coords


def build_strict_mutual_network(adjacency_list):
    """
    Build a network with a stricter criterion: only recognize a contact if the
    nearest neighbors are mutual (both nodes have each other as neighbors).
    """
    strict_adj_list = {}

    for node, neighbors in adjacency_list.items():
        strict_adj_list[node] = set()
        for neighbor in neighbors:
            if node in adjacency_list.get(neighbor, []):
                strict_adj_list[node].add(neighbor)
                if neighbor not in strict_adj_list:
                    strict_adj_list[neighbor] = set()
                strict_adj_list[neighbor].add(node)

    def dfs(node, visited, cluster):
        visited.add(node)
        cluster.add(node)
        for neighbor in strict_adj_list[node]:
            if neighbor not in visited:
                dfs(neighbor, visited, cluster)

    visited = set()
    clusters = []

    for node in strict_adj_list:
        if node not in visited:
            cluster = set()
            dfs(node, visited, cluster)
            clusters.append(cluster)

    return clusters


def segment(coord_files, tomogram, output_dir, verbose=False):
    if verbose:
        print("Segmenting axonemes...")
    coords = [load_coordinates(coord_file).values for coord_file in coord_files]

    min_dist_dict = {}
    for i in range(len(coords)):
        avg_dists = []
        for j in range(len(coords)):
            if i == j:
                avg_dists.append(np.inf)
            else:
                avg_dists.append(np.min(cdist(coords[i], coords[j])))
        min_dist_dict[i] = (np.argmin(avg_dists), np.argpartition(avg_dists, 1)[1])

    clusters = build_strict_mutual_network(min_dist_dict)
    if verbose:
        print(clusters)

    for idx, cluster in enumerate(clusters):
        cluster_list = [coord_files[x] for x in list(cluster)]
        xs, ys, zs, labels = [], [], [], []
        for i, doublet in enumerate(cluster_list):
            xyz = load_coordinates(doublet).values
            xs.extend(xyz[:, 0])
            ys.extend(xyz[:, 1])
            zs.extend(xyz[:, 2])
            labels.extend([f"doublet{i + 1}"] * xyz.shape[0])
        tmp_df = pd.DataFrame({"label": labels, "x": xs, "y": ys, "z": zs})
        os.makedirs(output_dir, exist_ok=True)
        tmp_df.to_csv(
            os.path.join(output_dir, f"axoneme_{tomogram}_{idx + 1}.csv"), index=False
        )
    return clusters


def segment_axonemes():
    parser = ArgumentParser(description="Segment axonemes from .coords files.")
    parser.add_argument(
        "input_directory",
        help="Input directory containing .coords files w/ doublet picks.",
    )
    parser.add_argument(
        "--output_directory",
        help="Output directory name containing .csv files with individually segemnted axonemes; this directory is stored in the given input directory.",
        default=None,
    )
    parser.add_argument(
        "--verbose",
        help="Print verbose output.",
        action='store_true'
    )
    args = parser.parse_args()

    input_directory = args.input_directory
    output_directory = (
        os.path.join(input_directory, "segmented")
        if args.output_directory is None
        else os.path.join(input_directory, args.output_directory)
    )
    verbose = args.verbose


    coord_files = sorted(glob.glob(os.path.join(input_directory, "*coords")))
    if not coord_files and verbose:
        print(f"No .coords files found in directory: {input_directory}")
        return

    tomogram_names = [
        (
            os.path.split(f)[-1].split("_")[1]
            if len(os.path.split(f)[-1].split("_")) == 4
            else "_".join(os.path.split(f)[-1].split("_")[1:3])
        )
        for f in coord_files
    ]
    tomogram_ids = np.unique(tomogram_names)

    for tomogram in tomogram_ids:
        if verbose:
            print(f"Processing tomogram {tomogram}")
        tomo_files = sorted(
            glob.glob(os.path.join(input_directory, f"*_{tomogram}_*coords"))
        )
        tomo_files = [
            f
            for f in tomo_files
            if len(os.path.split(f)[-1].split("_"))
            == (4 + len(tomogram.split("_")) - 1)
        ]

        if len(tomo_files) < 2:
            continue
        segment(tomo_files, tomogram, output_directory, verbose=verbose)


if __name__ == "__main__":
    segment_axonemes()
