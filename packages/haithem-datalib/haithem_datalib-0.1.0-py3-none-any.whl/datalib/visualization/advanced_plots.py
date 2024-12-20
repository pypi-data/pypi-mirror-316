import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def correlation_matrix(dataframe: pd.DataFrame, columns: list = None, annot: bool = True, cmap: str = "coolwarm", figsize: tuple = (10, 8)) -> None:
    """
    Display a correlation matrix as a heatmap.

    Parameters:
        dataframe (pd.DataFrame): The input DataFrame.
        columns (list, optional): List of column names to include in the correlation matrix. Default is None (all numeric columns).
        annot (bool, optional): Whether to annotate the heatmap with correlation values. Default is True.
        cmap (str, optional): Colormap to use for the heatmap. Default is "coolwarm".
        figsize (tuple, optional): Size of the figure. Default is (10, 8).

    Raises:
        ValueError: If no numeric columns are available for correlation.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        >>>     "A": [1, 2, 3],
        >>>     "B": [4, 5, 6],
        >>>     "C": [7, 8, 9]
        >>> })
        >>> correlation_matrix(df)
    """
    if columns:
        missing_columns = [col for col in columns if col not in dataframe.columns]
        if missing_columns:
            raise ValueError(f"The following columns do not exist in the DataFrame: {missing_columns}")
        df_corr = dataframe[columns].select_dtypes(include=[float, int])
    else:
        df_corr = dataframe.select_dtypes(include=[float, int])
    
    if df_corr.empty:
        raise ValueError("No numeric columns available for correlation.")

    corr = df_corr.corr()
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot, cmap=cmap)
    plt.title("Correlation Matrix")
    plt.show()
