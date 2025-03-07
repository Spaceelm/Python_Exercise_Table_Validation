"""
Terminal color and formatting utilities.

This module provides functions for enhancing terminal output visibility
during testing and validation processes with colorized text.
"""
import os
import platform
import sys


class TerminalColors:
    """
    Class providing terminal color and formatting capabilities.

    This class contains constants and methods to format terminal output
    with colors and styles for better visibility during testing.
    """

    # Detect if running on Windows
    IS_WINDOWS = platform.system() == "Windows"
    
    # Enable ANSI colors in Windows 10+ if colorama is available
    if IS_WINDOWS:
        try:
            import colorama
            colorama.init()
            ANSI_ENABLED = True
        except ImportError:
            ANSI_ENABLED = False
    else:
        ANSI_ENABLED = True

    # ANSI color codes
    RESET = "\033[0m" if ANSI_ENABLED else ""
    BOLD = "\033[1m" if ANSI_ENABLED else ""
    UNDERLINE = "\033[4m" if ANSI_ENABLED else ""

    # Foreground colors - reduced set
    FG_RED = "\033[31m" if ANSI_ENABLED else ""
    FG_GREEN = "\033[32m" if ANSI_ENABLED else ""  
    FG_BLUE = "\033[34m" if ANSI_ENABLED else ""   # Used only for progress bars
    FG_GRAY = "\033[90m" if ANSI_ENABLED else ""   # For less important info

    # Background colors - limited use
    BG_GRAY = "\033[100m" if ANSI_ENABLED else ""  # For section headers

    @staticmethod
    def section_header(text: str) -> str:
        """
        Format text as a section header with high visibility.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with gray background and white text
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.BG_GRAY}{TerminalColors.BOLD} {text} {TerminalColors.RESET}"
        else:
            return f"### {text} ###"

    @staticmethod
    def section_end() -> str:
        """
        Format text to mark the end of a section.

        Returns:
            str: Formatted text to mark end of section
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_GRAY}{'─' * 60}{TerminalColors.RESET}"
        else:
            return f"{'─' * 60}"

    @staticmethod
    def success(text: str) -> str:
        """
        Format text to indicate success.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with green color
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_GREEN}✓ {TerminalColors.BOLD}{text}{TerminalColors.RESET}"
        else:
            return f"✓ {text}"

    @staticmethod
    def error(text: str) -> str:
        """
        Format text to indicate error.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with red color
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_RED}✗ {TerminalColors.BOLD}{text}{TerminalColors.RESET}"
        else:
            return f"✗ {text}"

    @staticmethod
    def warning(text: str) -> str:
        """
        Format text to indicate warning.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with red color (less bold than error)
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_RED}⚠ {text}{TerminalColors.RESET}"
        else:
            return f"⚠ {text}"

    @staticmethod
    def info(text: str) -> str:
        """
        Format text to display information.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with gray color for less emphasis
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_GRAY}ℹ {text}{TerminalColors.RESET}"
        else:
            return f"ℹ {text}"

    @staticmethod
    def processing(text: str) -> str:
        """
        Format text to indicate processing status.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with gray color
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_GRAY}⋯ {text}{TerminalColors.RESET}"
        else:
            return f"⋯ {text}"

    @staticmethod
    def highlight_value(text: str) -> str:
        """
        Format text to highlight a value.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with bold
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.BOLD}{text}{TerminalColors.RESET}"
        else:
            return f"[{text}]"
