from .base_mode import BaseMode
from ..config import VimMode


class NormalMode(BaseMode):
    """Normal mode functionality for the Vim-like editor.

    Provides methods for:
    - Entering normal mode
    - Basic editing operations
    """

    def enter_normal_mode(self) -> None:
        """Enter normal mode.

        Sets up:
        - Read-only state
        - Focus behavior
        - Mode display
        - Clears any active selection
        """
        self._setup_mode(VimMode.NORMAL)
        self.refresh()

    def delete_at_cursor(self) -> None:
        """Delete character at cursor position"""
        self.delete(
            self.cursor_location, (self.cursor_location[0], self.cursor_location[1] + 1)
        )

    def delete_before_cursor(self) -> None:
        """Delete character before cursor position"""
        if self.cursor_location[1] > 0:
            self.delete(
                (self.cursor_location[0], self.cursor_location[1] - 1),
                self.cursor_location,
            )

    def indent_line(self) -> None:
        """Indent the current line by 4 spaces.

        Maintains cursor position relative to content by:
        1. Moving cursor to line start
        2. Inserting indentation
        3. Restoring cursor position + offset
        """
        row, col = self.cursor_location
        self.cursor_location = (row, 0)
        self.insert("    ")
        # self.lines[row] = "    " + self.lines[row]
        self.cursor_location = (row, col + 4)

    def deindent_line(self) -> None:
        """Deindent the current line."""
        row, col = self.cursor_location
        if self.lines[row].startswith("    "):
            self.lines[row] = self.lines[row][4:]
            self.cursor_location = (row, col - 4)
