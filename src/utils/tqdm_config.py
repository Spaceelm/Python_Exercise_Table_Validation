"""
Configuration module for tqdm progress bars.

This module contains configuration settings for tqdm progress bars used throughout the application.
"""
from tqdm import tqdm
from .terminal_colors import TerminalColors

# Configure tqdm default format with color
tqdm.monitor_interval = 0  # Disable monitor thread for better performance

# Define a custom bar format to use with tqdm instances
custom_bar_format = "{l_bar}%s{bar}%s{r_bar}" % (TerminalColors.info("\u001b[34m"), "\u001b[0m")
