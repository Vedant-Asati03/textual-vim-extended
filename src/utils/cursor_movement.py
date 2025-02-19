"""Custom defined cursor movements, bindings which are not available in textual for a specific cursor movemoent."""


class HandleCursorMovement:
    def cursor_location_cache(self) -> tuple[int, int]:
        """Cache and return the current cursor location."""
        return self.cursor_location

    def move_to_first_non_blank(self) -> None:
        """Move cursor to first non-blank character in line."""
        self.cursor_location = self.get_cursor_line_start_location(smart_home=True)

    def move_to_matching_bracket(self) -> None:
        """Move to matching bracket (%)."""
        self.cursor_location = self.matching_bracket_location

    def jump_backwards_to_end_of_word(self) -> None:
        """Move cursor to end of previous word (ge)."""
        row, col = self.cursor_location
        line = self.lines[row]

        # Find the previous word boundary
        text_before = line[:col]
        if not text_before.strip():
            if row > 0:
                self.move_cursor((row - 1, len(self.lines[row - 1].rstrip())))
            return

        words = text_before.rstrip().split()
        if words:
            last_word = words[-1]
            new_col = text_before.rindex(last_word) + len(last_word)
            self.move_cursor((row, new_col))

    def indent(self) -> None:
        """Indent the current line with proper cursor position maintenance."""
        row, col = self.cursor_location
        self.action_cursor_line_start()
        self.insert("    ")
        self.move_cursor((row, col + 4))

    def de_indent(self) -> None:
        """Remove one level of indentation while maintaining cursor position."""
        row, col = self.cursor_location
        line = self.lines[row]
        if line.startswith("    "):
            self.action_cursor_line_start()
            for _ in range(4):
                self.action_delete()
            new_col = max(0, col - 4)
            self.move_cursor((row, new_col))

    def move_to_mid_of_screen(self):
        """Move the cursor to the middle of the screen."""
        height = self.content_size.height
        _, cursor_location = self.selection
        target = self.navigator.get_location_at_y_offset(
            cursor_location,
            height // 2,
        )
        self.move_cursor(target)

    def move_to_top_of_screen(self) -> None:
        """Move the cursor and scroll up one page."""
        height = self.content_size.height
        _, cursor_location = self.selection
        target = self.navigator.get_location_at_y_offset(
            cursor_location,
            -(height - 1),
        )
        self.move_cursor(target)

    def move_to_bot_of_screen(self) -> None:
        """Move the cursor and scroll down one page."""
        height = self.content_size.height
        _, cursor_location = self.selection
        target = self.navigator.get_location_at_y_offset(
            cursor_location,
            (height - 1),
        )
        self.move_cursor(target)

    def left_curly_bracket(self) -> None:
        """Move cursor to previous paragraph."""
        row, _ = self.cursor_location
        