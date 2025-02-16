class VISUALMODEBINDINGS:
    def V_mode(self):
        self.visual_mode_bindings = {
            "escape": lambda: self.enter_normal_mode(),
            "ctrl+v": lambda: self.enter_visual_block_mode(block_visual_mode=True),
            "v": lambda: self.enter_normal_mode(),
            "V": lambda: self.enter_visual_line_mode(linewise_visual_mode=True),
            "h": lambda: self.action_cursor_left(True),
            "l": lambda: self.action_cursor_right(True),
            "k": lambda: self.action_cursor_up(True),
            "j": lambda: self.action_cursor_down(True),
            "d": lambda: self.delete_selection(),
            "y": lambda: self.yank_selection(),
            "c": lambda: self.change_selection(),
            ">": lambda: self.indent_selection(),
            "<": lambda: self.unindent_selection(),
            "~": lambda: self.toggle_case_selection(),
            "u": lambda: self.lowercase_selection(),
            "U": lambda: self.uppercase_selection(),
            "p": lambda: self.paste_over_selection(),
            "o": lambda: self.swap_selection_ends(),
            "gg": lambda: self.action_go_first_line(True),
            "G": lambda: self.action_go_last_line(True),
            "$": lambda: self.action_cursor_line_end(True),
            "^": lambda: self.action_cursor_line_start(True),
            "w": lambda: self.word_right(True),
            "b": lambda: self.word_left(True),
        }

        self.visual_line_mode_bindings = {
            "escape": lambda: self.enter_normal_mode(),
            "V": lambda: self.enter_normal_mode(),
            "v": lambda: self.enter_visual_mode(),
            "ctrl+v": lambda: self.enter_visual_block_mode(block_visual_mode=True),
            "k": lambda: self.action_cursor_up(True),
            "j": lambda: self.action_cursor_down(True),
            "h": lambda: self.action_cursor_left(),
            "l": lambda: self.action_cursor_right(),
            "d": lambda: self.delete_selection(),
            "y": lambda: self.yank_selection(),
            "c": lambda: self.change_selection(),
            ">": lambda: self.indent_selection(),
            "<": lambda: self.unindent_selection(),
            "~": lambda: self.toggle_case_selection(),
            "u": lambda: self.lowercase_selection(),
            "U": lambda: self.uppercase_selection(),
            "p": lambda: self.paste_over_selection(),
            "gg": lambda: self.action_go_first_line(True),
            "G": lambda: self.action_go_last_line(True),
        }

        self.visual_block_mode_bindings = {
            "escape": lambda: self.enter_normal_mode(),
            "V": lambda: self.enter_visual_line_mode(linewise_visual_mode=True),
            "v": lambda: self.enter_visual_mode(),
            "ctrl+v": lambda: self.enter_normal_mode(),
            "h": lambda: self.action_cursor_left(True),
            "l": lambda: self.action_cursor_right(True),
            "k": lambda: self.action_cursor_up(True),
            "j": lambda: self.action_cursor_down(True),
            "d": lambda: self.delete_block_selection(),
            "y": lambda: self.yank_block_selection(),
            "c": lambda: self.change_block_selection(),
            "I": lambda: self.insert_block_selection(),
            "A": lambda: self.append_block_selection(),
            ">": lambda: self.indent_selection(),
            "<": lambda: self.unindent_selection(),
            "~": lambda: self.toggle_case_selection(),
            "u": lambda: self.lowercase_selection(),
            "U": lambda: self.uppercase_selection(),
            "o": lambda: self.swap_selection_ends(),
            "gg": lambda: self.action_go_first_line(True),
            "G": lambda: self.action_go_last_line(True),
            "$": lambda: self.action_cursor_line_end(True),
            "^": lambda: self.action_cursor_line_start(True),
            "w": lambda: self.word_right(True),
            "b": lambda: self.word_left(True),
            "0": lambda: self.action_cursor_line_start(True),
            "%": lambda: self.goto_matching_bracket(True),
        }
