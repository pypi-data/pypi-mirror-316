import pandas as pd

def print_summary(message, data, num_precision=2, max_rows=10):
    """
    Print a formatted summary of data.

    Parameters:
        message (str): The message to display before the data summary.
        data (any): The data to summarize (e.g., DataFrame, list, dictionary).
        num_precision (int, optional): The number of decimal places to round numerical data. Default is 2.
        max_rows (int, optional): The maximum number of rows to display for DataFrames or large lists. Default is 10.

    Example:
        >>> print_summary("Data Summary", [1.23456, 2.34567, 3.45678])
        Data Summary:
        [1.23, 2.35, 3.46]
        ----------------------------------------
    """
    print(f"{message}:")
    
    if isinstance(data, pd.DataFrame):
        # If data is a DataFrame, show a summary of its first few rows and data types
        print(data.head(max_rows))
        print(f"Data types:\n{data.dtypes}")
    elif isinstance(data, pd.Series):
        # If data is a Series, show the first few entries
        print(data.head(max_rows))
    elif isinstance(data, (list, tuple)):
        # If data is a list or tuple, show the first few elements
        print(data[:max_rows])
    elif isinstance(data, dict):
        # If data is a dictionary, show key-value pairs
        print(dict(list(data.items())[:max_rows]))
    else:
        # For other data types (strings, numbers, etc.)
        if isinstance(data, (int, float)):
            print(f"{data:.{num_precision}f}")
        else:
            print(data)

    print("-" * 40)
