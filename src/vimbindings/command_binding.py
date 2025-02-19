class COMMANDMODEBINDINGS:
    def C_mode(self):
        """Configure command mode key bindings"""
        self.command_mode_bindings = {
            "enter": lambda: self.execute_command(),
            "escape": lambda: self.enter_normal_mode(),
            "backspace": lambda: self.handle_backspace(),
            "tab": lambda: self.handle_completion(),
            "up": lambda: self.cycle_history(-1),
            "down": lambda: self.cycle_history(1),
        }
