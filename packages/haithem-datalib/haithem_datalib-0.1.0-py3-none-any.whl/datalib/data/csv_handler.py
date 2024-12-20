import pandas as pd

def read_csv(file_path: str, **kwargs) -> pd.DataFrame:
    """
    Read a CSV file into a DataFrame.

    Parameters:
        file_path (str): Path to the CSV file.
        **kwargs: Additional keyword arguments passed to `pd.read_csv`.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data.

    Example:
        >>> df = read_csv("data.csv", delimiter=";")
        >>> print(df.head())
    """
    try:
        return pd.read_csv(file_path, **kwargs)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{file_path}' does not exist.")
    except Exception as e:
        raise ValueError(f"An error occurred while reading the CSV file: {e}")

def write_csv(dataframe: pd.DataFrame, file_path: str, **kwargs):
    """
    Write a DataFrame to a CSV file.

    Parameters:
        dataframe (pd.DataFrame): DataFrame to write to CSV.
        file_path (str): Path to save the CSV file.
        **kwargs: Additional keyword arguments passed to `to_csv`.

    Returns:
        None

    Example:
        >>> write_csv(df, "output.csv", sep=";")
    """
    try:
        dataframe.to_csv(file_path, index=False, **kwargs)
    except Exception as e:
        raise ValueError(f"An error occurred while writing the CSV file: {e}")

def filter_data(dataframe: pd.DataFrame, column: str, condition: str) -> pd.DataFrame:
    """
    Filter the DataFrame based on a condition applied to a column.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.
        column (str): Column name to apply the filter on.
        condition (str): Condition string compatible with `pandas.query`.

    Returns:
        pd.DataFrame: Filtered DataFrame.

    Example:
        >>> filtered_df = filter_data(df, "age", "> 30")
        >>> print(filtered_df)
    """
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    try:
        return dataframe.query(f"{column} {condition}")
    except Exception as e:
        raise ValueError(f"An error occurred while filtering data: {e}")
