class HandleVisualMode:

    def enter_visual_block_mode(self, block_visual_mode: bool = False) -> None:
        """Enter visual block mode."""
        self.border_subtitle = "V-BLOCK"
        self.styles.border_subtitle_background = "#6EACDA"
        self.mode = "v_block"

        if block_visual_mode:
            ...

        self.refresh()

    def enter_visual_line_mode(self, linewise_visual_mode: bool = False) -> None:
        """Enter visual line mode."""
        self.border_subtitle = "V-LINE"
        self.styles.border_subtitle_background = "#6EACDA"
        self.mode = "v_line"

        if linewise_visual_mode:
            self.select_line(self.cursor_location[0])

        self.refresh()

    def enter_visual_mode(self, ) -> None:
        """Enter visual mode and set the selection start."""
        self.selection_start = self.cursor_location
        self.border_subtitle = "VISUAL"
        self.styles.border_subtitle_background = "#6EACDA"
        self.mode = "visual"

        self.refresh()
