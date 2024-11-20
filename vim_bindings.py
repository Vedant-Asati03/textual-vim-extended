from textual.events import Key
from textual.widgets import TextArea
from mode_types import VimMode, MODE_CONFIGS

from custom_css import CSS
from insert_mode import HandleInsertMode
from normal_mode import HandleNormalMode
from visual_mode import HandleVisualMode
from cursor_movement import HandleCursorMovement


class HandleVimBindings(
    TextArea,
    CSS,
    HandleCursorMovement,
    HandleInsertMode,
    HandleNormalMode,
    HandleVisualMode,
):
    read_only: bool = True
    mode: VimMode = VimMode.NORMAL
    current_sequence: str = ""

    def reset_sequence(self) -> None:
        """Resets the current key sequence after it's processed."""
        self.current_sequence = ""

    def handle_mode_switch(self, event):
        """Handles key bindings for different modes."""
        if self.read_only and self.mode == VimMode.NORMAL:
            self.current_sequence += event.key

            # Check for number prefix for repeat commands
            if self.current_sequence.isdigit():
                return event.prevent_default()

            if self.current_sequence in self.normal_mode_bindings:
                repeat = 1
                if any(c.isdigit() for c in self.current_sequence):
                    digits = ''.join(filter(str.isdigit, self.current_sequence))
                    repeat = int(digits) if digits else 1
                
                for _ in range(repeat):
                    self.normal_mode_bindings[self.current_sequence]()
                self.reset_sequence()
                event.prevent_default()
            else:
                if len(self.current_sequence) > 3:  # Allow for longer sequences
                    self.reset_sequence()

        elif self.read_only and self.mode == VimMode.VISUAL:
            if event.key in self.visual_mode_bindings:
                self.visual_mode_bindings[event.key]()
                event.prevent_default()

        elif self.read_only and self.mode == VimMode.VISUAL_LINE:
            if event.key in self.visual_line_mode_bindings:
                self.visual_line_mode_bindings[event.key]()
                event.prevent_default()

        elif self.read_only and self.mode == VimMode.VISUAL_BLOCK:
            if event.key in self.visual_block_mode_bindings:
                self.visual_block_mode_bindings[event.key]()
                event.prevent_default()

        else:
            if event.key in self.insert_mode_bindings:
                self.insert_mode_bindings[event.key]()
                event.prevent_default()

    def delete_at_cursor(self) -> None:
        """Delete character at cursor position"""
        self.delete(self.cursor_location, (self.cursor_location[0], self.cursor_location[1] + 1))
    
    def delete_before_cursor(self) -> None:
        """Delete character before cursor position"""
        if self.cursor_location[1] > 0:
            self.delete(
                (self.cursor_location[0], self.cursor_location[1] - 1),
                self.cursor_location
            )
    
    def delete_current_line(self) -> None:
        """Delete the current line"""
        row = self.cursor_location[0]
        self.delete((row, 0), (row + 1, 0))

    async def on_key(self, event: Key) -> None:
        """Capture key presses and handle multi-key sequences."""
        self.set_custom_css()

        self.normal_mode_bindings = {
            "backspace": lambda: self.action_cursor_left(),
            "v": lambda: self.enter_visual_mode(),
            "V": lambda: self.enter_visual_line_mode(linewise_visual_mode=True),
            "ctrl+v": lambda: self.enter_visual_block_mode(block_visual_mode=True),
            "i": lambda: self.enter_insert_mode(at_cursor=True),
            "I": lambda: self.enter_insert_mode(at_line_start=True),
            "a": lambda: self.enter_insert_mode(after_cursor=True),
            "A": lambda: self.enter_insert_mode(after_line=True),
            "o": lambda: self.enter_insert_mode(new_line_below=True),
            "O": lambda: self.enter_insert_mode(new_line_above=True),
            "h": lambda: self.action_cursor_left(),
            "l": lambda: self.action_cursor_right(),
            "k": lambda: self.action_cursor_up(),
            "j": lambda: self.action_cursor_down(),
            "w": lambda: self.action_cursor_word_right(),
            "b": lambda: self.action_cursor_word_left(),
            "ge": lambda: self.jump_backwards_to_end_of_word(),
            "gg": lambda: self.move_cursor((0, 0)),
            "G": lambda: self.move_cursor((len(self.text.splitlines()), 0)),
            "0": lambda: self.action_cursor_line_start(),
            "$": lambda: self.action_cursor_line_end(),
            "u": lambda: self.action_undo(),
            "ctrl+r": lambda: self.action_redo(),
            "H": lambda: self.move_to_top_of_screen(),
            "L": lambda: self.move_to_bot_of_screen(),
            "M": lambda: self.move_to_mid_of_screen(),
            "x": lambda: self.delete_at_cursor(),
            "X": lambda: self.delete_before_cursor(),
            "dd": lambda: self.delete_current_line(),
            "$": lambda: self.action_cursor_line_end(),
            "circumflex_accent": lambda: self.move_to_first_non_blank(),
            "%": lambda: self.move_to_matching_bracket(),
        }

        self.visual_mode_bindings = {
            "escape": lambda: self.enter_normal_mode(),
            "ctrl+v": lambda: self.enter_visual_block_mode(block_visual_mode=True),
            "v": lambda: self.enter_normal_mode(),
            "V": lambda: self.enter_visual_line_mode(linewise_visual_mode=True),
            "h": lambda: self.action_cursor_left(True),
            "l": lambda: self.action_cursor_right(True),
            "k": lambda: self.action_cursor_up(True),
            "j": lambda: self.action_cursor_down(True),
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
        }

        self.visual_block_mode_bindings = {
            "escape": lambda: self.enter_normal_mode(),
            "V": lambda: self.enter_visual_line_mode(linewise_visual_mode=True),
            "v": lambda: self.enter_visual_mode(),
            "ctrl+v": lambda: self.enter_normal_mode(),
        }

        self.insert_mode_bindings = {
            "escape": lambda: self.enter_normal_mode(),
            "ctrl+h": lambda: self.delete_left(),
            "ctrl+j": lambda: self.insert("\n"),
            "ctrl+b": lambda: self.indent(),
            "ctrl+d": lambda: self.de_indent(),
        }

        self.handle_mode_switch(event)

        row, col = self.cursor_location
        self.border_title = f"{event.key} |{row + 1}:{col + 1}|"
