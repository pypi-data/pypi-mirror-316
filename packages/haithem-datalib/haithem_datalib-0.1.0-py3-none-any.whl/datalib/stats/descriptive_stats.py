import pandas as pd


def calculate_median(dataframe: pd.DataFrame, column: str, dropna: bool = True) -> float:
    """
    Calculate the median of a specific column.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.
        column (str): The column for which to calculate the median.
        dropna (bool, optional): Whether to ignore NaN values. Default is True.

    Returns:
        float: The median of the column.

    Raises:
        ValueError: If the column does not exist or contains no numeric data.

    Example:
        >>> df = pd.DataFrame({'value': [1, 2, 3, None]})
        >>> calculate_median(df, 'value')
        2.0
    """
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    return dataframe[column].median(skipna=dropna)

def calculate_mode(dataframe: pd.DataFrame, column: str) -> float:
    """
    Calculate the mode of a specific column.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.
        column (str): The column for which to calculate the mode.

    Returns:
        float: The mode of the column.

    Raises:
        ValueError: If the column does not exist or contains no numeric data.

    Example:
        >>> df = pd.DataFrame({'value': [1, 2, 2, 3]})
        >>> calculate_mode(df, 'value')
        2.0
    """
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    mode = dataframe[column].mode()
    if mode.empty:
        raise ValueError(f"No mode found for column '{column}'.")
    return mode[0]


def calculate_mean(dataframe: pd.DataFrame, column: str) -> float:
    """
    Calculates the mean of a specified column in the DataFrame.

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - column (str): The column name to calculate the mean for.

    Returns:
    - float: The mean of the column, or 0 if the DataFrame is empty.
    """
    if dataframe.empty:
        return 0
    return dataframe[column].mean()

def calculate_std_dev(dataframe: pd.DataFrame, column: str) -> float:
    """
    Calculates the standard deviation of a specified column in the DataFrame.

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - column (str): The column name to calculate the standard deviation for.

    Returns:
    - float: The standard deviation of the column, or 0 if there's only one value in the column.
    """
    if len(dataframe[column]) == 1:
        return 0
    return dataframe[column].std()

def calculate_correlation(dataframe: pd.DataFrame, col1: str, col2: str) -> float:
    """
    Calculates the correlation between two specified columns in the DataFrame.

    Parameters:
    - dataframe (pd.DataFrame): The input DataFrame.
    - col1 (str): The first column name.
    - col2 (str): The second column name.

    Returns:
    - float: The correlation coefficient, or None if the DataFrame is empty or columns don't exist.
    """
    if dataframe.empty or col1 not in dataframe or col2 not in dataframe:
        return None
    return dataframe[col1].corr(dataframe[col2])