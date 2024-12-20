import matplotlib.pyplot as plt
import numpy as np
import pytest
from src.datalib.visualization.simple_plots import bar_chart, histogram, scatter_plot

def test_bar_chart():
    data = [1, 2, 3]
    labels = ["A", "B", "C"]
    bar_chart(data, labels, title="Test Bar Chart")

def test_histogram():
    data = [1, 2, 2, 3, 3, 3]
    histogram(data, bins=3, title="Test Histogram")

def test_scatter_plot():
    x = [1, 2, 3]
    y = [4, 5, 6]
    scatter_plot(x, y, title="Test Scatter Plot")