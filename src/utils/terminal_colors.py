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

    # Foreground colors
    FG_BLACK = "\033[30m" if ANSI_ENABLED else ""
    FG_RED = "\033[31m" if ANSI_ENABLED else ""
    FG_GREEN = "\033[32m" if ANSI_ENABLED else ""
    FG_YELLOW = "\033[33m" if ANSI_ENABLED else ""
    FG_BLUE = "\033[34m" if ANSI_ENABLED else ""
    FG_MAGENTA = "\033[35m" if ANSI_ENABLED else ""
    FG_CYAN = "\033[36m" if ANSI_ENABLED else ""
    FG_WHITE = "\033[37m" if ANSI_ENABLED else ""

    # Background colors
    BG_BLACK = "\033[40m" if ANSI_ENABLED else ""
    BG_RED = "\033[41m" if ANSI_ENABLED else ""
    BG_GREEN = "\033[42m" if ANSI_ENABLED else ""
    BG_YELLOW = "\033[43m" if ANSI_ENABLED else ""
    BG_BLUE = "\033[44m" if ANSI_ENABLED else ""
    BG_MAGENTA = "\033[45m" if ANSI_ENABLED else ""
    BG_CYAN = "\033[46m" if ANSI_ENABLED else ""
    BG_WHITE = "\033[47m" if ANSI_ENABLED else ""

    @staticmethod
    def section_header(text: str) -> str:
        """
        Format text as a section header with high visibility.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with blue background and white text
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.BG_BLUE}{TerminalColors.FG_BLACK}{TerminalColors.BOLD} {text} {TerminalColors.RESET}"
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
            return f"{TerminalColors.BG_BLUE}{TerminalColors.FG_BLACK}{'─' * 60}{TerminalColors.RESET}"
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
            return f"{TerminalColors.FG_GREEN}✓ {text}{TerminalColors.RESET}"
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
            return f"{TerminalColors.FG_RED}✗ {text}{TerminalColors.RESET}"
        else:
            return f"✗ {text}"

    @staticmethod
    def warning(text: str) -> str:
        """
        Format text to indicate warning.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with yellow color
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_YELLOW}⚠ {text}{TerminalColors.RESET}"
        else:
            return f"⚠ {text}"

    @staticmethod
    def info(text: str) -> str:
        """
        Format text to display information.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with cyan color
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_CYAN}ℹ {text}{TerminalColors.RESET}"
        else:
            return f"ℹ {text}"

    @staticmethod
    def processing(text: str) -> str:
        """
        Format text to indicate processing status.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with magenta color
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_MAGENTA}⋯ {text}{TerminalColors.RESET}"
        else:
            return f"⋯ {text}"

    @staticmethod
    def highlight_value(text: str) -> str:
        """
        Format text to highlight a value.

        Args:
            text: The text to format

        Returns:
            str: Formatted text with yellow color and bold
        """
        if TerminalColors.ANSI_ENABLED:
            return f"{TerminalColors.FG_YELLOW}{TerminalColors.BOLD}{text}{TerminalColors.RESET}"
        else:
            return f"[{text}]"
