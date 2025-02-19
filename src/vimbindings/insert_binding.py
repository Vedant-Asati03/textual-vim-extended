class INSERTMODEBINDINGS:
    def I_mode(self):
        self.insert_mode_bindings = {
            "escape": lambda: self.enter_normal_mode(),
            "ctrl+h": lambda: self.delete_left(),
            "ctrl+j": lambda: self.insert("\n"),
            "ctrl+b": lambda: self.indent(),
            "ctrl+d": lambda: self.de_indent(),
            "ctrl+w": lambda: self.action_delete_word_left(),
            "ctrl+u": lambda: self.action_delete_to_start_of_line(),
            "ctrl+k": lambda: self.action_delete_to_end_of_line(),
            "ctrl+a": lambda: self.action_cursor_line_start(),
            "ctrl+e": lambda: self.action_cursor_line_end(),
        }
