class HandleNormalMode:

    def enter_normal_mode(self) -> None:
        self.read_only = True
        self.can_focus = False
        self.border_subtitle = "NORMAL"
        self.styles.border_subtitle_background = "#97BE5A"
        self.mode = "normal"
        self.refresh()
