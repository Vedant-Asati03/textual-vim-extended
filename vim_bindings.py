from textual.events import Key
from textual.widgets import TextArea
from rich.style import Style

from custom_css import CSS
from insert_mode import HandleInsertMode
from normal_mode import HandleNormalMode
from visual_mode import HandleVisualMode
from cursor_movement import HandleCursorMovement


class HandleVimBindings(TextArea, CSS, HandleCursorMovement, HandleInsertMode, HandleNormalMode, HandleVisualMode):
    read_only: bool = True
    mode: str = "normal"
    current_sequence: str = ""  # For multi-key sequences

    def reset_sequence(self) -> None:
        """Resets the current key sequence after it's processed."""
        self.current_sequence = ""

    def handle_mode_switch(self, event):
        """Handles key bindings for different modes."""
        
        # Normal mode bindings
        if self.read_only and self.mode == "normal":
            self.current_sequence += event.key  # Accumulate key presses

            if self.current_sequence in self.normal_mode_bindings:
                # If the current sequence matches a valid binding, trigger it
                self.normal_mode_bindings[self.current_sequence]()
                self.reset_sequence()
                event.prevent_default()
            else:
                # If the sequence gets too long or invalid, reset it
                if len(self.current_sequence) > 2:
                    self.reset_sequence()

        # Visual Mode Bindings
        elif self.read_only and self.mode == "visual":
            if event.key in self.visual_mode_bindings:
                self.visual_mode_bindings[event.key]()
                event.prevent_default()

        # Visual Line Mode Bindings
        elif self.read_only and self.mode == "v_line":
            if event.key in self.visual_line_mode_bindings:
                self.visual_line_mode_bindings[event.key]()
                event.prevent_default()

        # Visual Block Mode Bindings
        elif self.read_only and self.mode == "v_block":
            if event.key in self.visual_block_mode_bindings:
                self.visual_block_mode_bindings[event.key]()
                event.prevent_default()

        # Insert Mode Bindings
        else:
            if event.key in self.insert_mode_bindings:
                self.insert_mode_bindings[event.key]()
                event.prevent_default()

    async def on_key(self, event: Key) -> None:
        """Capture key presses and handle multi-key sequences."""
        self.set_custom_css()  # Apply custom CSS styling

        # Define key bindings for normal, visual, and insert modes
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
            "gg": lambda: self.move_cursor((0, 0)),  # Go to top of document
            "G": lambda: self.move_cursor((len(self.text.splitlines()), 0)),  # Go to bottom
            "0": lambda: self.action_cursor_line_start(),
            "u": lambda: self.action_undo(),
            "ctrl+r": lambda: self.action_redo(),
            "H": lambda: self.move_to_top_of_screen(),
            "L": lambda: self.move_to_bot_of_screen(),
            "M": lambda: self.move_to_mid_of_screen(),
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
            "ctrl+w": lambda: self.delete_word_before_cursor(),
            "ctrl+j": lambda: self.insert_text("\n"),
            "ctrl+b": lambda: self.indent(),
            "ctrl+d": lambda: self.de_indent(),
        }

        # Handle multi-key sequences and mode switching
        self.handle_mode_switch(event)

        # Update cursor position information (optional UI feedback)
        row, col = self.cursor_location
        self.border_title = f"{event.key} |{row + 1}:{col + 1}|"


