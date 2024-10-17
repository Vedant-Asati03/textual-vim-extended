from rich.style import Style


class HandleInsertMode:

    def insert_text(self, text: str):
        """Insert text at the current cursor location."""
        row, col = self.cursor_location
        lines = self.text.splitlines()

        if row < len(lines):
            lines[row] = lines[row][:col] + text + lines[row][col:]
            self.text = "\n".join(lines)
            self.cursor_location = (row, col + len(text))

    def delete_text(self, text: str):
        """Delete text at the current cursor location."""
        row, col = self.cursor_location
        lines = self.text.splitlines()

        if row < len(lines):
            lines[row] = lines[row][:col] + text + lines[row][col:]
            self.text = "\n".join(lines)
            self.cursor_location = (row, col + len(text))

    def delete_left(self):
        """Delete the character to the left of the cursor."""
        row, col = self.cursor_location
        lines = self.text.splitlines()

        if col > 0 and row < len(lines):
            lines[row] = lines[row][:col - 1] + lines[row][col:]
            self.text = "\n".join(lines)
            self.cursor_location = (row, col - 1)
        elif col == 0 and row > 0:
            prev_line_length = len(lines[row - 1])
            lines[row - 1] += lines[row]
            del lines[row]
            self.text = "\n".join(lines)
            self.cursor_location = (row - 1, prev_line_length)

    def delete_right(self):
        """Delete the character to the right of the cursor."""
        row, col = self.cursor_location
        lines = self.text.splitlines()

        if row < len(lines) and col < len(lines[row]):
            lines[row] = lines[row][:col] + lines[row][col + 1:]
            self.text = "\n".join(lines)
        elif col == len(lines[row]) and row < len(lines) - 1:
            # Join the current line with the next line
            lines[row] += lines[row + 1]
            del lines[row + 1]
            self.text = "\n".join(lines)

    def delete_word_before_cursor(self) -> None:
        row, col = self.cursor_location
        lines = self.text.splitlines()
        if row < len(lines):
            line_before_cursor = lines[row][:col]
            words = line_before_cursor.rstrip().rsplit(" ", 1)
            if len(words) > 1:
                delete_len = len(words[-1]) + 1
            else:
                delete_len = len(words[0])
            new_col = max(0, col - delete_len)
            lines[row] = lines[row][:new_col] + lines[row][col:]
            self.text = "\n".join(lines)
            self.cursor_location = (row, new_col)

    def enter_insert_mode(self, at_cursor: bool = True, at_line_start: bool = False, after_cursor: bool = False,
                          after_line: bool = False, new_line_below: bool = False, new_line_above: bool = False) -> None:
        self.read_only = False
        self.can_focus = True
        self.border_subtitle = "INSERT"
        self.styles.border_subtitle_background = "#E8B86D"

        if at_line_start:
            self.action_cursor_line_start()
        elif after_cursor:
            self.action_cursor_right()
        elif after_line:
            self.action_cursor_line_end()
        elif new_line_below:
            self.action_cursor_line_end()
            self.insert_text("\n")
            self.action_cursor_down()
        elif new_line_above:
            self.action_cursor_line_start()
            self.insert_text("\n")
            self.action_cursor_up()

        self.refresh()
