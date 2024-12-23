"""
Functions for creating various data visualizations.
"""
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar(data, x, y, title="Bar Chart", color="blue"):
    """
    Create a bar plot.

    Args:
        data: DataFrame containing the data.
        x: Column name for the x-axis.
        y: Column name for the y-axis.
        title: Title of the chart (default: "Bar Chart").
        color: Bar color (default: "blue").
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x=x, y=y, color=color)
    plt.title(title)
    plt.show()

def plot_histogram(data, column, bins=10, title="Histogram", color="green"):
    """
    Create a histogram.

    Args:
        data: DataFrame containing the data.
        column: Column to plot.
        bins: Number of bins (default: 10).
        title: Title of the chart (default: "Histogram").
        color: Bar color (default: "green").
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=bins, color=color, edgecolor="k")
    plt.title(title)
    plt.show()

def plot_correlation_matrix(data, title="Correlation Matrix", cmap="coolwarm"):
    """
    Create a correlation matrix heatmap.

    Args:
        data: DataFrame containing numerical data.
        title: Title of the heatmap (default: "Correlation Matrix").
        cmap: Colormap for the heatmap (default: "coolwarm").
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.corr(), annot=True, fmt=".2f", cmap=cmap)
    plt.title(title)
    plt.show()

def plot_scatter(data, x, y, title="Scatter Plot", color="red"):
    """
    Create a scatter plot.

    Args:
        data: DataFrame containing the data.
        x: Column name for the x-axis.
        y: Column name for the y-axis.
        title: Title of the chart (default: "Scatter Plot").
        color: Point color (default: "red").
    """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=data, x=x, y=y, color=color)
    plt.title(title)
    plt.show()
