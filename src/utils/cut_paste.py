from textual.widgets.text_area import Selection


class ManageEditorsClipboard:
    def yank_selection(self) -> None:
        """Copy selected text to editor clipboard."""
        if self.selected_text:
            self.clipboard = self.selected_text
        self.selection = Selection()

    def paste_after_selection(self) -> None:
        """Paste from editor clipboard."""
        if self.clipboard:
            self.insert(self.clipboard)
        self.enter_normal_mode()

    def paste_before_selection(self) -> None:
        """ """
        if self.clipboard:
            row, col = self.cursor_location
            self.cursor_location = row, col - 1
            self.insert(self.clipboard)
        self.enter_normal_mode()

    def delete_selection(self) -> None:
        """Delete the current selection."""
        self.action_delete_left()
        self.selection = Selection(self.cursor_location, self.cursor_location)
        self.enter_normal_mode()
