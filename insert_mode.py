from mode_types import VimMode, MODE_CONFIGS

class HandleInsertMode:
    def enter_insert_mode(self, at_cursor: bool = True, at_line_start: bool = False, 
                         after_cursor: bool = False, after_line: bool = False, 
                         new_line_below: bool = False, new_line_above: bool = False) -> None:
        """Enter insert mode with various cursor positioning options."""
        config = MODE_CONFIGS[VimMode.INSERT]
        self.read_only = config.read_only
        self.can_focus = not config.read_only
        self.border_subtitle = config.title
        self.styles.border_subtitle_background = config.bg_color
        self.mode = VimMode.INSERT

        if at_line_start:
            self.action_cursor_line_start()
        elif after_cursor:
            self.action_cursor_right()
        elif after_line:
            self.action_cursor_line_end()
        elif new_line_below:
            self.action_cursor_line_end()
            self.insert("\n")
            self.action_cursor_down()
        elif new_line_above:
            self.action_cursor_line_start()
            self.insert("\n")
            self.action_cursor_up()

        self.refresh()
