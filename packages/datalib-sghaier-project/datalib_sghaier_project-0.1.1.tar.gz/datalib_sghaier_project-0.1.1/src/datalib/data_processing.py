"""
Module for data manipulation tasks.
"""
import pandas as pd

def load_csv(filepath):
    """Loads a CSV file into a pandas DataFrame."""
    return pd.read_csv(filepath)


def save_csv(df, filepath):
    """Saves a pandas DataFrame to a CSV file."""
    df.to_csv(filepath, index=False)
