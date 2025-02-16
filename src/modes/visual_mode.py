from .base_mode import BaseMode
from ..config import VimMode
from textual.widgets.text_area import Selection
from textual.reactive import reactive


class VisualMode(BaseMode):
    selection = reactive(Selection(), init=False, always_update=True)

    def enter_visual_mode(self) -> None:
        """Enter visual mode and set the selection start."""
        self._setup_mode(VimMode.VISUAL)
        self.selection_start = self.cursor_location
        self.refresh()

    def enter_visual_line_mode(self, linewise_visual_mode: bool = False) -> None:
        """Enter visual line mode."""
        self._setup_mode(VimMode.VISUAL_LINE)
        if linewise_visual_mode:
            self.select_line(self.cursor_location[0])
        self.refresh()

    def enter_visual_block_mode(self, block_visual_mode: bool = False) -> None:
        """Enter visual block mode."""
        self._setup_mode(VimMode.VISUAL_BLOCK)
        self.refresh()

    def select_line(self, row: int) -> None:
        """Select an entire line."""
        start = (row, 0)
        end = (row, len(self.lines[row]))
        self.select(start, end)

    def delete_selection(self) -> None:
        """Delete the current selection based on selection mode."""
        self.action_delete_left()
        self.selection = Selection()
        self.enter_normal_mode()

    def yank(self) -> None: ...

    def yank_selection(self) -> None:
        """Copy the current selection based on selection mode."""
        if not self.selection or self.selection.start == self.selection.end:
            return

        start, end = self.selection

        if self.mode == VimMode.VISUAL:
            # Standard visual mode - copy selected text
            self.copy()

        elif self.mode == VimMode.VISUAL_LINE:
            # Visual line mode - copy entire lines
            start_row = min(start[0], end[0])
            end_row = max(start[0], end[0])
            self.select((start_row, 0), (end_row + 1, 0))
            self.copy()

        elif self.mode == VimMode.VISUAL_BLOCK:
            # Visual block mode - copy block of text
            start_row, start_col = start
            end_row, end_col = end

            # Build block text
            block_text = []
            left_col = min(start_col, end_col)
            right_col = max(start_col, end_col)

            for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
                if row < len(self.lines):
                    line = self.lines[row]
                    block_line = (
                        line[left_col:right_col] if left_col < len(line) else ""
                    )
                    block_text.append(block_line)

            # Join with newlines and copy to clipboard
            self.app.clipboard = "\n".join(block_text)

        # Return to normal mode
        self.selection = Selection()  # Clear selection
        self.enter_normal_mode()

    def indent_selection(self) -> None:
        """Indent the selected lines."""
        start_row = min(self.selection[0][0], self.selection[1][0])
        end_row = max(self.selection[0][0], self.selection[1][0])

        for row in range(start_row, end_row + 1):
            self.move_cursor((row, 0))
            self.insert("    ")

        self.enter_normal_mode()

    def unindent_selection(self) -> None:
        """Remove one level of indentation from selected lines."""
        start_row = min(self.selection[0][0], self.selection[1][0])
        end_row = max(self.selection[0][0], self.selection[1][0])

        for row in range(start_row, end_row + 1):
            line = self.lines[row]
            if line.startswith("    "):
                self.move_cursor((row, 0))
                for _ in range(4):
                    self.action_delete()

        self.enter_normal_mode()

    def change_selection(self) -> None:
        """Delete the selection and enter insert mode"""
        if self.selected_text:
            self.delete_selection()
            self.enter_insert_mode()

    def toggle_case_selection(self) -> None:
        """Toggle case of selected text"""
        if self.selected_text:
            text = self.selected_text
            toggled = text.swapcase()
            self.delete_selection()
            self.insert(toggled)
            self.enter_normal_mode()

    def uppercase_selection(self) -> None:
        """Convert selection to uppercase"""
        if self.selected_text:
            text = self.selected_text
            upper = text.upper()
            self.delete_selection()
            self.insert(upper)
            self.enter_normal_mode()

    def lowercase_selection(self) -> None:
        """Convert selection to lowercase"""
        if self.selected_text:
            text = self.selected_text
            lower = text.lower()
            self.delete_selection()
            self.insert(lower)
            self.enter_normal_mode()

    def paste_over_selection(self) -> None:
        """Replace selection with clipboard contents"""
        if self.selected_text:
            self.delete_selection()
            self.paste()
            self.enter_normal_mode()

    def swap_selection_ends(self) -> None:
        """Swap the cursor between start and end of selection"""
        if self.selection:
            start, end = self.selection
            self.move_cursor(start if self.cursor_location == end else end)

    def delete_block_selection(self) -> None:
        """Delete visual block selection"""
        if self.selected_text:
            start, end = self.selection
            start_row, start_col = start
            end_row, end_col = end
            for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
                self.delete(
                    (row, min(start_col, end_col)), (row, max(start_col, end_col))
                )
            self.enter_normal_mode()

    def insert_block_selection(self) -> None:
        """Insert at the start of block selection"""
        if self.selected_text:
            start, end = self.selection
            self.move_cursor(start)
            self.enter_insert_mode()

    def append_block_selection(self) -> None:
        """Append at the end of block selection"""
        if self.selected_text:
            start, end = self.selection
            _, end_col = end
            self.move_cursor((end[0], end_col + 1))
            self.enter_insert_mode()

    def yank_block_selection(self) -> None:
        """Yank (copy) the block selection to clipboard"""
        if not self.selection or self.selection.start == self.selection.end:
            return

        start, end = self.selection
        start_row, start_col = start
        end_row, end_col = end

        block_text = []
        left_col = min(start_col, end_col)
        right_col = max(start_col, end_col)

        for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
            if row < len(self.lines):
                line = self.lines[row]
                block_line = line[left_col:right_col] if left_col < len(line) else ""
                block_text.append(block_line)

        # Join with newlines and copy to clipboard
        self.app.clipboard = "\n".join(block_text)
        self.enter_normal_mode()
