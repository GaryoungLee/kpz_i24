from utils import load_speed_matrix
from boxcount import estimate_fractal_dimension
from plotting import colormapForHeatmap, colorList, colormapDiscrete
from clustering import estimate_fisher_exponent 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os


## ploting params ##
plt.rcParams['font.family'] ='Arial'
myColorList =  colorList()
myColorMapH = colormapForHeatmap()
myColorMapD = colormapDiscrete()


## fixed params ##
dateList = [ '11-22', '11-28', '11-29', '11-30', '12-01', '12-02']
laneList = [1,2,3,4]
dx = 0.02
dt = 2

# params
date = dateList[0]     # parse from dateList
lane_number = 1        # from 1 to 4 or use laneList
threshold = 11         # mph
aspect_ratio = 4       # H : W = 1 : 4


# Example path to your CSV file
csv_path = f"data/imputeOnly_{date}_WB_lane{lane_number}_dx{dx}_dt{dt}.csv"  # <- Replace with your actual file path

# Load matrix
time_space_matrix = load_speed_matrix(csv_path)

# Estimate Delay Fractal Dimension
D, D_std_err = estimate_fractal_dimension(time_space_matrix, threshold, aspect_ratio, target ='delay')
print(f"Delay fractal dimension is {D:.2f} ({D_std_err:.2f}) on {date} lane {lane_number} at speed threshold of {threshold} mph")

# Estimate Cutoff Fractal Dimension
Df, Df_std_err = estimate_fractal_dimension(time_space_matrix, threshold, aspect_ratio, target ='cutoff')
print(f"Cutoff fractal dimension is {Df:.2f} ({Df_std_err:.2f}) on {date} lane {lane_number} at speed threshold of {threshold} mph")

# Estimate Fisher Exponent tau
tau, tau_std_err, intercept, clustered_cells, sizes, cumcounts = estimate_fisher_exponent(time_space_matrix, threshold, num_binning = 20, cutoff_percentage = 0.6)
print(f"Fisher Exponent is {tau:.2f} ({tau_std_err:.2f}) on {date} lane {lane_number} at speed threshold of {threshold} mph")




#### Example Plots ####
directory_path = "figs"
try:
    os.makedirs(directory_path)
    print(f"Directory '{directory_path}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_path}' already exists.")
except OSError as e:
    print(f"Error creating directory '{directory_path}': {e}")

# Time space diagram and clusters 
fig, ax = plt.subplots(figsize=(8, 2))
plt.matshow(time_space_matrix, cmap=plt.cm.RdYlGn, vmin=0, vmax=80, aspect='auto')
ax.xaxis.tick_bottom()
ax.set_xticks([    ])
ax.set_yticks([    ])
ax.set_xlabel('Time')
ax.set_ylabel('Space')
ax.set_title(f'{date} lane {lane_number}')
fig.tight_layout()
file_name = f'TS_{date}_lane{lane_number}'
plt.savefig(f'{directory_path}/{file_name}.png', dpi=200)
print(f'Saved Figure {file_name}.png')
plt.close()

fig, ax = plt.subplots(figsize=(8, 2))
plt.matshow(clustered_cells, cmap=myColorMapD, aspect='auto')
ax.xaxis.tick_bottom()
ax.set_xticks([    ])
ax.set_yticks([    ])
ax.set_xlabel('Time')
ax.set_ylabel('Space')
ax.set_title(f'threshold {threshold}')
fig.tight_layout()
file_name = f'Cluster_{date}_lane{lane_number}_thres{threshold}'
plt.savefig(f'{directory_path}/{file_name}.png', dpi=200)
print(f'Saved Figure {file_name}.png')
plt.close()

# Fisher exponent and Survival plot of cluster size distribution 
fig, ax = plt.subplots(figsize=(4, 4))
fit_x = np.linspace(min(np.log(sizes)), max(np.log(sizes)), 10)
fit_y = tau * fit_x + intercept
plt.loglog(sizes, cumcounts, 'o', mfc="white", mec="gray", alpha=0.6, )
plt.plot(np.exp(fit_x), np.exp(fit_y), 'r--', label=r'$\tau-1$ = {:.2f} ± {:.2f}'.format(-tau, tau_std_err))
ax.set_title(r" $v_c$ = {:.1f} mph".format(threshold))
ax.set_xlabel('Cluster Size s')
ax.set_ylabel('P(S > s)')
plt.legend()
fig.tight_layout()
file_name = f'tau_{date}_lane{lane_number}_thres{threshold}'
plt.savefig(f'{directory_path}/{file_name}.png', dpi=200)
print(f'Saved Figure {file_name}.png')
plt.close()


# Example plot for testing the impact of critical speed threshold v_c for all six days on the fractal dimension
threshold_range = np.arange(8,14,1) # your parameter

# select between delay and cutoff
target = 'delay'

D_dict ={}
for i, date in enumerate(dateList):
    D_dict[date]={}
    slope_list=[]
    std_err_list = []
    csv_path = f"data/imputeOnly_{date}_WB_lane{lane_number}_dx{dx}_dt{dt}.csv"
    time_space_matrix = load_speed_matrix(csv_path)
    for threshold in threshold_range:
        slope, std_err = estimate_fractal_dimension(time_space_matrix, threshold, aspect_ratio, target = target)
        slope_list.append(slope)
        std_err_list.append(std_err)
    D_dict[date]['slope'] = slope_list
    D_dict[date]['std_err'] = std_err_list


plt.figure(figsize=(4.5, 3))
for i, date in enumerate(dateList):
    slope_list = np.array(D_dict[date]['slope'])
    std_err_list = np.array(D_dict[date]['std_err'])

    lower = slope_list - std_err_list
    upper = slope_list + std_err_list

    # Line plot
    plt.plot(threshold_range, -slope_list, '-', label=date, color = myColorList[i])

    # Filled error band
    plt.fill_between(threshold_range, -upper, -lower, alpha=0.2, label=None, color = myColorList[i])
    
plt.axhline(1.5, color='black', linestyle=':', linewidth=2)

plt.xlabel("Threshold Speed (mph)")
plt.ylabel(r"Estimated $D = z$")
plt.legend(ncol = 3, loc = 'lower right', title = f'Aspect Ratio {aspect_ratio}')
plt.grid(True)
plt.ylim(1.25, 1.75)
plt.tight_layout()
file_name = f'D_aspect_ratio_{aspect_ratio}_lane{lane_number}'
plt.savefig(f'{directory_path}/{file_name}.png', dpi=200)
print(f'Saved Figure {file_name}.png')
plt.close()


### Heatmap ### 

DList = np.array([D_dict[date]['slope'] for date in dateList])
DList = np.array([-i for i in DList])

plt.figure(figsize=(5.5,3))
ax=sns.heatmap(DList, xticklabels=np.round(threshold_range, 1), yticklabels=dateList, 
                 vmin = 1.15, vmax = 1.85,
                 cmap=myColorMapH, annot=False, cbar_kws={'label': r'$D$'})
plt.xlabel("Threshold Speed (mph)" )
plt.ylabel("Date")
int_ticks = [i+0.5 for i, val in enumerate(np.round(threshold_range, 1)) if val.is_integer()]
ax.set_xticks(int_ticks)
ax.set_xticklabels(np.arange(8,14,1), rotation=0) # adjust
ax.set_yticklabels(dateList,rotation=0)
plt.grid(axis='x', color='w', linewidth=0.8, linestyle =':')
plt.tight_layout()

file_name = f"heatmap_{aspect_ratio}_lane{lane_number}"
plt.savefig(f'{directory_path}/{file_name}.png', dpi=200)
print(f'Saved Figure {file_name}.png')
plt.close()



