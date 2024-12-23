"""
Module for generating visualizations.
"""
import matplotlib.pyplot as plt

def plot_bar(data, labels, title="Bar Plot"):
    """Creates a bar plot."""
    plt.bar(labels, data)
    plt.title(title)
    plt.show()


def plot_histogram(data, title="Histogram"):
    """Creates a histogram."""
    plt.hist(data)
    plt.title(title)
    plt.show()
