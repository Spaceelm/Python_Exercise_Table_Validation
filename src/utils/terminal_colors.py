"""
Terminal color and formatting utilities.

This module provides functions for enhancing terminal output visibility
during testing and validation processes with colorized text.
"""

class TerminalColors:
    """
    Class providing terminal color and formatting capabilities.
    
    This class contains constants and methods to format terminal output
    with colors and styles for better visibility during testing.
    """
    
    # ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
    # Foreground colors
    FG_BLACK = "\033[30m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[32m"
    FG_YELLOW = "\033[33m"
    FG_BLUE = "\033[34m"
    FG_MAGENTA = "\033[35m"
    FG_CYAN = "\033[36m"
    FG_WHITE = "\033[37m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    
    @staticmethod
    def section_header(text: str) -> str:
        """
        Format text as a section header with high visibility.
        
        Args:
            text: The text to format
            
        Returns:
            str: Formatted text with blue background and white text
        """
        return f"{TerminalColors.BG_BLUE}{TerminalColors.FG_WHITE}{TerminalColors.BOLD} {text} {TerminalColors.RESET}"
    
    @staticmethod
    def section_end() -> str:
        """
        Format text to mark the end of a section.
        
        Returns:
            str: Formatted text to mark end of section
        """
        return f"{TerminalColors.BG_BLUE}{TerminalColors.FG_WHITE}{'─' * 60}{TerminalColors.RESET}"
    
    @staticmethod
    def success(text: str) -> str:
        """
        Format text to indicate success.
        
        Args:
            text: The text to format
            
        Returns:
            str: Formatted text with green color
        """
        return f"{TerminalColors.FG_GREEN}✓ {text}{TerminalColors.RESET}"
    
    @staticmethod
    def error(text: str) -> str:
        """
        Format text to indicate error.
        
        Args:
            text: The text to format
            
        Returns:
            str: Formatted text with red color
        """
        return f"{TerminalColors.FG_RED}✗ {text}{TerminalColors.RESET}"
    
    @staticmethod
    def warning(text: str) -> str:
        """
        Format text to indicate warning.
        
        Args:
            text: The text to format
            
        Returns:
            str: Formatted text with yellow color
        """
        return f"{TerminalColors.FG_YELLOW}⚠ {text}{TerminalColors.RESET}"
    
    @staticmethod
    def info(text: str) -> str:
        """
        Format text to display information.
        
        Args:
            text: The text to format
            
        Returns:
            str: Formatted text with cyan color
        """
        return f"{TerminalColors.FG_CYAN}ℹ {text}{TerminalColors.RESET}"
    
    @staticmethod
    def processing(text: str) -> str:
        """
        Format text to indicate processing status.
        
        Args:
            text: The text to format
            
        Returns:
            str: Formatted text with magenta color
        """
        return f"{TerminalColors.FG_MAGENTA}⋯ {text}{TerminalColors.RESET}"
    
    @staticmethod
    def highlight_value(text: str) -> str:
        """
        Format text to highlight a value.
        
        Args:
            text: The text to format
            
        Returns:
            str: Formatted text with yellow color and bold
        """
        return f"{TerminalColors.FG_YELLOW}{TerminalColors.BOLD}{text}{TerminalColors.RESET}"
