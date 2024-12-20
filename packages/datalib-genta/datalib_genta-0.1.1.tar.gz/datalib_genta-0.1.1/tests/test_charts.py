import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import pandas as pd
import matplotlib.pyplot as plt
from datalib.visualization.charts import bar_chart, scatter_plot
from datalib.visualization.advanced_viz import correlation_matrix
import numpy as np

@pytest.fixture
def sample_bar_chart_data():
    """Fixture for sample data to test bar chart."""
    return pd.DataFrame({"category": ["A", "B", "C"], "values": [10, 20, 30]})

@pytest.fixture
def sample_scatter_plot_data():
    """Fixture for sample data to test scatter plot."""
    return pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
@pytest.fixture
def sample_data():
    """Fixture for sample data."""
    # Creating a sample DataFrame for testing
    data = {
        'A': np.random.rand(10),
        'B': np.random.rand(10),
        'C': np.random.rand(10)
    }
    return pd.DataFrame(data)

def test_generate_bar_chart(sample_bar_chart_data):
    """Test the generate_bar_chart function."""
    chart = bar_chart(sample_bar_chart_data, "category", "values")
    
    # Ensure the chart is generated
    assert chart is not None, "Le graphique à barres n'a pas été généré."
    
    # Verify the chart has a 'figure' attribute, indicating a valid plot
    assert hasattr(chart, "figure"), "Le graphique n'a pas d'attribut 'figure'."
    
    # Verify the title of the bar chart
    assert chart.figure.axes[0].get_title() == "values", "Le titre du graphique à barres est incorrect."
    
    # Verify that the correct number of bars is plotted
    assert len(chart.figure.axes[0].patches) == len(sample_bar_chart_data), "Le nombre de barres affichées est incorrect."
    

def test_generate_scatter_plot(sample_scatter_plot_data):
    """Test the generate_scatter_plot function."""
    chart = scatter_plot(sample_scatter_plot_data, "x", "y")
    
    # Ensure the chart is generated
    assert chart is not None, "Le graphique de dispersion n'a pas été généré."
    
    # Verify the chart has a 'figure' attribute
    assert hasattr(chart, "figure"), "Le graphique n'a pas d'attribut 'figure'."
    
    # Verify the title of the scatter plot
    assert chart.figure.axes[0].get_title() == "Scatter Plot of x vs y", "Le titre du graphique de dispersion est incorrect."
    
    # Verify there are points plotted on the chart
    assert len(chart.figure.axes[0].collections) > 0, "Aucune donnée n'est affichée sur le graphique de dispersion."

def test_bar_chart_visualization(sample_bar_chart_data):
    """Test to visualize and manually check the bar chart."""
    chart = bar_chart(sample_bar_chart_data, "category", "values")
    
    # Show the chart (only for manual inspection during testing)
    chart.figure.show()

def test_scatter_plot_visualization(sample_scatter_plot_data):
    """Test to visualize and manually check the scatter plot."""
    chart = scatter_plot(sample_scatter_plot_data, "x", "y")
    
    # Show the chart (only for manual inspection during testing)
    chart.figure.show()

def test_correlation_matrix(sample_data):
    """Test the correlation_matrix function."""
    # Generate the correlation matrix plot
    fig = correlation_matrix(sample_data)

    # Ensure that a figure object is returned
    assert isinstance(fig, plt.Figure), "La fonction ne retourne pas une instance de matplotlib.figure.Figure."

    # Verify the title of the plot
    assert fig.axes[0].get_title() == "Correlation Matrix", "Le titre de la matrice de corrélation est incorrect."

    # Check if the figure contains two axes: one for the heatmap and one for the colorbar
    assert len(fig.axes) == 2, "La figure ne contient pas le nombre correct d'axes."

    # Check that one of the axes is the colorbar (it typically has a 'colorbar' label)
    colorbar_axis = [ax for ax in fig.axes if 'colorbar' in ax.get_label()]
    assert len(colorbar_axis) == 1, "La figure ne contient pas de colorbar."

    # Optionally, verify that the heatmap axis is of the correct type (matplotlib.axes.Axes)
    heatmap_axis = [ax for ax in fig.axes if 'colorbar' not in ax.get_label()]
    assert len(heatmap_axis) == 1, "La figure ne contient pas de graphique heatmap valide."
