import matplotlib.pyplot as plt

def bar_chart(data: list, labels: list, title: str = ""):
    """
    Creates a bar chart from the given data.

    Parameters:
    - data (list): The data values to plot.
    - labels (list): The labels for the bars.
    - title (str): The title of the chart. Default is an empty string.
    """
    fig, ax = plt.subplots()
    ax.bar(labels, data)
    ax.set_title(title)
    plt.show()

def histogram(data: list, bins: int, title: str = ""):
    """
    Creates a histogram from the given data.

    Parameters:
    - data (list): The data values to plot.
    - bins (int): The number of bins for the histogram.
    - title (str): The title of the histogram. Default is an empty string.
    """
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    ax.set_title(title)
    plt.show()

def scatter_plot(x: list, y: list, title: str = ""):
    """
    Creates a scatter plot from the given data.

    Parameters:
    - x (list): The x-axis data values.
    - y (list): The y-axis data values.
    - title (str): The title of the scatter plot. Default is an empty string.
    """
    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.set_title(title)
    plt.show()
