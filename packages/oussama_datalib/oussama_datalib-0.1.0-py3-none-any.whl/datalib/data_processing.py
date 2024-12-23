"""
Functions for data loading, cleaning, and preprocessing.
"""
import pandas as pd

def load_csv(file_path):
    """Load a CSV file into a DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
    """
    return pd.read_csv(file_path)

def normalize_column(df, column):
    """
    Normalize a column in the DataFrame.

    Args:
        df: DataFrame containing the data.
        column: Column to normalize.
    """
    df[column] = (df[column] - df[column].mean()) / df[column].std()
    return df

def fill_missing_values(df, column, method="mean"):
    """
    Fill missing values in a column.

    Args:
        df: DataFrame containing the data.
        column: Column to fill.
        method: Method to fill values ("mean", "median", "mode").
    """
    if method == "mean":
        df[column].fillna(df[column].mean(), inplace=True)
    elif method == "median":
        df[column].fillna(df[column].median(), inplace=True)
    elif method == "mode":
        df[column].fillna(df[column].mode()[0], inplace=True)
    return df

def encode_categorical(df, column):
    """
    Encode a categorical column as integers.

    Args:
        df: DataFrame containing the data.
        column: Column to encode.
    """
    df[column] = pd.factorize(df[column])[0]
    return df

def scale_data(df, columns):
    """
    Scale numerical columns.

    Args:
        df: DataFrame containing the data.
        columns: List of columns to scale.
    """
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df