import pandas as pd

def load_speed_matrix(csv_path):
    df = pd.read_csv(csv_path)
    time_space_matrix = df.pivot(index='x', columns='t', values='speed')

    # subset the matrix if the quality of certain time range is low: e.g., starting from 1000th column
    time_space_matrix = time_space_matrix.iloc[: 1000:]

    return time_space_matrix