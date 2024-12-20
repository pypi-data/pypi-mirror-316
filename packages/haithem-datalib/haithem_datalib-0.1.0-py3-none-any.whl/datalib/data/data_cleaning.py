import pandas as pd

def normalize_column(dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Normalize a specific column in the DataFrame to a range of [0, 1].

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.
        column (str): The name of the column to normalize.

    Returns:
        pd.DataFrame: The DataFrame with the normalized column.

    Raises:
        ValueError: If the specified column does not exist.

    Example:
        >>> df = pd.DataFrame({'value': [10, 20, 30]})
        >>> normalized_df = normalize_column(df, 'value')
        >>> print(normalized_df)
    """
    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    dataframe[column] = (dataframe[column] - dataframe[column].min()) / (dataframe[column].max() - dataframe[column].min())
    return dataframe

def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
    """
    Handles missing values in a DataFrame based on the specified strategy.

    Parameters:
    - df (pd.DataFrame): The input DataFrame with potential missing values.
    - strategy (str): The strategy to handle missing values. Options are 'mean', 'median', or 'drop'. Default is 'mean'.

    Returns:
    - pd.DataFrame: The DataFrame with missing values handled according to the specified strategy.

    Raises:
    - ValueError: If an unsupported strategy is provided.
    """
    if strategy == 'mean':
        df.fillna(df.mean(), inplace=True)
    elif strategy == 'median':
        df.fillna(df.median(), inplace=True)
    elif strategy == 'drop':
        df.dropna(inplace=True)
    else:
        raise ValueError("Stratégie non supportée")  # French message for unsupported strategy
    return df