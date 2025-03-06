"""
Configuration module for tqdm progress bars.

This module contains configuration settings for tqdm progress bars used throughout the application.
"""
from tqdm import tqdm

from src.utils.terminal_colors import TerminalColors

# Configure tqdm default format with color
tqdm.monitor_interval = 0  # Disable monitor thread for better performance

# Define a custom bar format to use with tqdm instances
if TerminalColors.ANSI_ENABLED:
    custom_bar_format = "{l_bar}%s{bar}%s{r_bar}" % (
        TerminalColors.FG_BLUE,
        TerminalColors.RESET,
    )
else:
    custom_bar_format = "{l_bar}{bar}{r_bar}"  # Default format without colors
