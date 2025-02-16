from .base_mode import BaseMode
from ..config import VimMode


class CommandMode(BaseMode):
    """Command mode for executing Ex commands.

    Handles colon commands like :w, :q, :wq, etc.
    Maintains command history and provides command completion.
    """

    command_buffer: str = ""
    command_history: list[str] = []

    def enter_command_mode(self) -> None:
        """Enter command mode and initialize command input."""
        self._setup_mode(VimMode.COMMAND)
        self.command_buffer = ":"
        self._update_subtitle()  # This will now show ":" in subtitle
        self.refresh()

    def _update_subtitle(self) -> None:
        """Update command input in subtitle bar."""
        self.border_subtitle += self.command_buffer
        self.refresh()

    def handle_backspace(self) -> None:
        """Handle backspace in command buffer."""
        if len(self.command_buffer) > 1:  # Keep the initial ":"
            self.command_buffer = self.command_buffer[:-1]
            self._update_subtitle()

    def execute_command(self) -> None:
        """Execute the current command in buffer."""
        cmd = self.command_buffer[1:]  # Remove leading :

        self._update_subtitle()  # Update display before executing

        if cmd == "w":
            self.save_file()
        elif cmd == "q":
            self.quit()
        elif cmd == "wq":
            self.save_file()
            self.quit()
        elif cmd.startswith("set"):
            self.handle_set_command(cmd[4:])

        self.command_history.append(self.command_buffer)
        self.command_buffer = ""
        self.enter_normal_mode()

    def handle_set_command(self, option: str) -> None:
        """Handle :set commands for editor options."""
        option = option.strip()
        if option in ["number", "nu"]:
            self.show_line_numbers = True
        elif option in ["nonumber", "nonu"]:
            self.show_line_numbers = False

    def save_file(self) -> None:
        """Save current buffer to file."""
        # Implement file saving logic
        pass

    def quit(self) -> None:
        """Exit the editor."""
        # Implement quit logic
        self.app.exit()
