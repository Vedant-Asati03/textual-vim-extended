from mode_types import VimMode, MODE_CONFIGS, ModeConfig

class HandleVisualMode:
    def enter_visual_mode(self) -> None:
        """Enter visual mode and set the selection start."""
        config = MODE_CONFIGS[VimMode.VISUAL]
        self._setup_mode(config)
        self.selection_start = self.cursor_location
        self.mode = VimMode.VISUAL
        self.refresh()

    def enter_visual_line_mode(self, linewise_visual_mode: bool = False) -> None:
        """Enter visual line mode."""
        config = MODE_CONFIGS[VimMode.VISUAL_LINE]
        self._setup_mode(config)
        self.mode = VimMode.VISUAL_LINE

        if linewise_visual_mode:
            self.select_line(self.cursor_location[0])
        self.refresh()

    def enter_visual_block_mode(self, block_visual_mode: bool = False) -> None:
        """Enter visual block mode."""
        config = MODE_CONFIGS[VimMode.VISUAL_BLOCK]
        self._setup_mode(config)
        self.mode = VimMode.VISUAL_BLOCK
        self.refresh()

    def _setup_mode(self, config: 'ModeConfig') -> None:
        """Common setup for visual modes."""
        self.read_only = config.read_only
        self.can_focus = not config.read_only
        self.border_subtitle = config.title
        self.styles.border_subtitle_background = config.bg_color

    def select_line(self, row: int) -> None:
        """Select an entire line."""
        start = (row, 0)
        end = (row, len(self.lines[row]))
        self.select(start, end)

    def delete_selection(self) -> None:
        """Delete the current selection and enter normal mode."""
        if self.selected_text:
            self.cut()
            self.enter_normal_mode()
    
    def yank_selection(self) -> None:
        """Copy the current selection and enter normal mode."""
        if self.selected_text:
            self.copy()
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
