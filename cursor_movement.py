class HandleCursorMovement:

    def cursor_location_cache(self):
        """Return the current cursor location."""
        current_location = self.cursor_location
        return current_location

    def jump_backwards_to_end_of_word(self):
        """Move the cursor to the end of the previous word."""
        char_to_jump = self.cursor_location[1] - self.get_cursor_word_left_location()[1]

        if char_to_jump > 1:
            self.action_cursor_word_left()
            self.action_cursor_word_left()
            self.action_cursor_word_right()

        else:
            self.action_cursor_word_left()
            self.action_cursor_word_left()

    def indent(self):
        """Indent the current line."""
        cached_location = self.cursor_location_cache()
        self.move_to_line_start()
        self.insert_text("    ")
        cached_location = (cached_location[0], cached_location[1] + 4)
        self.cursor_location = cached_location

    def de_indent(self):
        """Move the cursor one character to the left."""
        row, col = self.cursor_location
        if col > 0:
            self.cursor_location = (row, col - 4)

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
