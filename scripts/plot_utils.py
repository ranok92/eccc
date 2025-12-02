
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def plot_dataframe_lines_with_shading(df, color_palette='viridis',
                                      alpha=0.3, title=None, xlabel=None, ylabel=None):
    """
    Plot line curves for each column in a dataframe with shaded areas between adjacent lines.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame where each column is a line to plot and index is the x-axis
    color_palette : str or list
        Name of the seaborn color palette to use or a list of colors
    figsize : tuple
        Figure size as (width, height) in inches
    alpha : float
        Transparency of the shaded areas (0 to 1)
    title : str, optional
        Plot title
    xlabel : str, optional
        Label for x-axis
    ylabel : str, optional
        Label for y-axis
    
    Returns:
    --------
    fig, ax : matplotlib figure and axis objects
    """
    # Create figure and axis
    fig, ax = plt.subplots()
    
    # Get colors from the palette
    columns = df.columns
    n_columns = len(columns)
    if isinstance(color_palette, str):
        colors = sns.color_palette(color_palette, n_columns)
    else:
        colors = color_palette
    
    colors = colors[::-1]
    # Sort columns for consistent shading
    sorted_columns = sorted(columns, key=lambda col: df[col].mean(), reverse=True)
    
    # Create x-axis values from the dataframe index
    x = df.index.values
    
    # Plot each line and shade between adjacent lines
    for i, column in enumerate(sorted_columns):
        y = df[column].values
        ax.plot(x, y, color=colors[i], alpha=alpha, label=column, linewidth=2)
        
        # If this is not the last line, shade the area between this line and the next
        if i < len(sorted_columns) - 1:
            next_column = sorted_columns[i + 1]
            next_y = df[next_column].values
            ax.fill_between(x, y, next_y, color=colors[i], alpha=alpha)
        else:
            # For the last line, shade the area between the line and zero
            ax.fill_between(x, y, 0, color=colors[i], alpha=alpha)
    
    # Set labels and title
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    if title:
        ax.set_title(title, fontsize=14)
    
    # Add a legend
    ax.legend(loc='best')
    
    # Make the plot look nicer
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.grid(True, linestyle='--')
    
    return fig, ax