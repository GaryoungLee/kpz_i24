import numpy as np
import pandas as pd
from scipy.ndimage import label
from scipy.stats import linregress
from collections import Counter


# Functions of box-counting methods with consideration of aspect ratio 
# if height: width = 1:1 , typical square box

def fixed_grid_boxcount(binary_matrix, box_height, box_width):
    """
    Count the number of rectangular boxes of size (height, width) that contain at least one True value.
    Excludes edge cases where the remaining region is smaller than height or width.
    """
    rows, cols = binary_matrix.shape
    count = 0
    
    for i in range(0, rows, box_height):
        for j in range(0, cols, box_width):
            if np.any(binary_matrix[i:min(i+box_height, rows), j:min(j+box_width, cols)]):
                count += 1
    return count


def sliding_grid_boxcount(binary_matrix, box_height, box_width, step_fraction=0.5):
    """
    Sliding grid box counting.
    binary_matrix: 2D array (True/False)
    box_height, box_width: dimensions of box
    step_fraction: fraction of box size to slide (e.g., 0.5 means 50% overlap)
    """
    rows, cols = binary_matrix.shape
    row_step = max(int(box_height * step_fraction), 1)
    col_step = max(int(box_width * step_fraction), 1)

    counts = []

    for row_shift in range(0, box_height, row_step):
        for col_shift in range(0, box_width, col_step):
            count = 0
            for i in range(row_shift, rows, box_height):
                for j in range(col_shift, cols, box_width):
                    box = binary_matrix[i:min(i+box_height, rows), j:min(j+box_width, cols)]
                    if np.any(box):
                        count += 1
            counts.append(count)

    return np.mean(counts)



def estimate_fractal_dimension(time_space_matrix, threshold, aspect_ratio, target ='delay'):

    structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    eligible_cells_lower = time_space_matrix < threshold
    clustered_cells_lower, _ = label(eligible_cells_lower, structure=structure)
    cluster_sizes = Counter(clustered_cells_lower.ravel())
    
    if target == 'delay':
    
        # Exclude clusters smaller or equal to 5 cells, also exclude background (value 0)
        binary_matrix = np.isin(clustered_cells_lower, [cl_id for cl_id, size in cluster_sizes.items() if size >= 5 and cl_id != 0])

    elif target == 'cutoff':
        id_size_map = {cl_id: size for cl_id, size in cluster_sizes.items() if cl_id != 0 and size >= 5}
        sizes = np.array(list(id_size_map.values()))

        if len(sizes) < 10:
            print("Too few clusters. Returning None.")
            return None

        # 1. log-scale cutoff target
        log_s_min = np.log(min(sizes))
        log_s_max = np.log(max(sizes))
        log_cutoff = log_s_min + 0.60 * (log_s_max - log_s_min)  # 0.60: defined cutoff clusters in cluster size distribution 
        target_size = np.exp(log_cutoff)

        # 2. closest cluster to target_size
        selected_id = min(id_size_map.keys(), key=lambda cl_id: abs(id_size_map[cl_id] - target_size))
        binary_matrix = (clustered_cells_lower == selected_id).astype(int)

    else: 
        print("error: target should be either 'delay' or 'cutoff'")
    
    box_sizes = [1, 2, 4, 8, 16, 32, 64, 128]
    counts = []

    for size in box_sizes:
        height = size
        width = max(int(size * aspect_ratio), 1)
        counts.append(sliding_grid_boxcount(binary_matrix, height, width))

    log_box_sizes = np.log(box_sizes)
    log_counts = np.log(counts)

    slope, intercept, r_value, p_value, std_err = linregress(log_box_sizes, log_counts)


    return slope, std_err
