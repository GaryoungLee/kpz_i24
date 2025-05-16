# Fractal Analysis of Traffic Congestion

This repository provides a modular Python framework to analyze traffic congestion using fractal theory. 


Reference : Lee, G., Jha, A., Wiesenfeld, K., & Laval, J. (2025) Cracking the Code of Traffic Congestion: Criticality and KPZ Universality in Real-World Traffic. 

This research leverages I24 Motion dataset. 
The raw dataset and documents can be accessed below. 

https://i24motion.org/access_data

https://github.com/I24-MOTION

Reference: Gloudemans, D., Wang, Y., Ji, J., Zachar, G., Barbour, W., Hall, E., Cebelak, M., Smith, L. and Work, D.B., 2023. I-24 MOTION: An instrument for freeway traffic science. Transportation Research Part C: Emerging Technologies, 155, p.104311.



## 📁 Project Structure

```
kpz_i24/
├── 📁 data                     # Processed data from I24 Motion dataset
├── 📁 figs                     # Where figures are saved
├── __init__.py                 # Makes the folder a package
├── boxcount.py                 # Fractal dimension estimation via box-counting
├── clustering.py               # Cluster labeling and Fisher exponent estimation
├── plotting.py                 # Visualization helpers
├── utils.py                    # Data loading utilities
└── main.py                     # Main script to run experiments and generate figures
```

## Update Note

(May 15, 2025) The repository will be updated with better explanations / codes to process raw data / additional codes for supplementary text.



## 🔧 Requirements

Install dependencies with:

```bash
pip install numpy pandas matplotlib seaborn scipy
```



## 📥 Input Format

CSV files must contain:
- `x`: spatial coordinate (e.g., km or miles)
- `t`: time (e.g., seconds)
- `speed`: instantaneous speed

**Example filename:**
```
imputeOnly_11-29_WB_lane1_dx0.02_dt2.csv
```




## 🚀 How to Run

Edit the CSV path in `main.py`:

```python
csv_path = f"data/imputeOnly_{date}_WB_lane{lane_number}_dx{dx}_dt{dt}.csv"
```

Then run the main analysis:

```bash
python main.py
```

The script performs the following:
- Loads the spatiotemporal speed matrix
- Estimates the delay and cutoff fractal dimension
- Computes the Fisher exponent from cluster size distribution
- Loops through different thresholds and dates
- Saves plots to the `figs/` directory



## 📊 Output

Plots saved in the `figs/` folder include:

- **Time-space speed diagram**
- **Clustered region matrix**
- **Fisher exponent log-log survival plot**
- **Delay Fractal dimension vs. threshold curves (per day)**
- **Heatmap of D vs. date and threshold**



## 📘 Key Concepts

- **Fractal Dimension**: Captures spatial irregularity and scaling behavior of congestion.
- **Fisher Exponent (τ)**: Describes the power-law decay of cluster size distributions.
- **Box-Counting Method**: Estimates fractal dimension using varying box sizes.
- **Cluster Labeling**: 4-connectivity method applied to low-speed cells.

---


