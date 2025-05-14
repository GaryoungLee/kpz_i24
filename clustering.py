import numpy as np
import pandas as pd
from scipy.ndimage import label
from scipy.stats import linregress
from collections import Counter


def estimate_fisher_exponent(time_space_matrix, threshold, num_binning = 20, cutoff_percentage = 0.6):

    structure = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    eligible_cells_lower = time_space_matrix < threshold
    clustered_cells_lower, _ = label(eligible_cells_lower, structure=structure)
    cluster_sizes = Counter(clustered_cells_lower.ravel())


    del cluster_sizes[0]
    cluster_sizes_list = [size for size in cluster_sizes.values() if size >= 5]
   
   
    # Survival function
    cluster_size_counts = Counter(cluster_sizes_list)
    cluster_sizes, counts = zip(*cluster_size_counts.items())
    cluster_sizes = np.array(cluster_sizes)
    
    counts = np.array(counts)
    indices = np.argsort(cluster_sizes)
    
    sorted_sizes = cluster_sizes[indices]
    sorted_counts = counts[indices]
    cumulative_counts = np.cumsum(sorted_counts[::-1])[::-1]

    # Binning in log-space
    log_bins = np.logspace(np.log10(min(sorted_sizes)), np.log10(max(sorted_sizes)), num=num_binning)
    binned_data = []
    for j in range(len(log_bins) - 1):
        in_bin = (sorted_sizes >= log_bins[j]) & (sorted_sizes < log_bins[j + 1])
        if np.any(in_bin):
            mean_size = np.mean(sorted_sizes[in_bin])
            mean_count = np.mean(cumulative_counts[in_bin])
            binned_data.append((mean_size, mean_count))

    binned_data = np.array(binned_data)
    binned_sizes = binned_data[:, 0]
    binned_survivals = binned_data[:, 1]

    # Log-log regression
    e_index = int(num_binning * cutoff_percentage)
    log_sizes = np.log(binned_sizes[:e_index+1])
    log_survivals = np.log(binned_survivals[:e_index+1])
    slope, intercept, _, _, std_err = linregress(log_sizes, log_survivals)
    
    
    return slope, std_err, intercept, clustered_cells_lower, sorted_sizes, cumulative_counts