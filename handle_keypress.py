from textual.events import Key


class HandleKeyPress:
    current_sequence = ""

    def on_key(self, event: Key) -> None:
        """Handles keypress events and builds Vim-like key sequences."""
        key_pressed = event.character
        self.current_sequence += key_pressed
        # if key_pressed:

            # await self.process_sequence()
    #
    # async def process_sequence(self) -> None:
    #     """Process the current key sequence and trigger actions like Vim."""
    #     message_widget = self.query_one("#message", Static)
        #
        # if self.current_sequence == "gg":
        #     message_widget.update("You pressed 'gg'. Moving to the top!")
        #     self.reset_sequence()
        #
        # elif self.current_sequence == "g":
        #     message_widget.update("You pressed 'g'. Waiting for the next key...")
        #
        # else:
        #     message_widget.update(f"Unknown sequence: '{self.current_sequence}'")
        #     self.reset_sequence()
