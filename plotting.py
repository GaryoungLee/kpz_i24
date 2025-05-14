import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def colormapForHeatmap(lowerC ="#ffcccc" , midC ="#520052", upperC="#d6e0ff"):
# Define custom divergent colormap: light blue -> dark blue -> light blue

    custom_divergent = LinearSegmentedColormap.from_list(
        "blue_divergent",
        [lowerC, lowerC, lowerC, midC,upperC, upperC, upperC],
        N=40
    )
    return custom_divergent

def colorList():
    colorList = ["#ea5545", "#f46a9b", "#ffbf2e", "#87bc45", "#27aeef",   "#b33dc6"]

    return colorList

def colormapDiscrete():
    random_colors_rgb = np.random.rand(4096, 3)
    random_colors_rgb[0] = (1,1,1)
    custom_cmap = plt.matplotlib.colors.ListedColormap(random_colors_rgb)
    return custom_cmap