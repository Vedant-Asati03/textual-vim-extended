from mode_types import VimMode, MODE_CONFIGS

class HandleNormalMode:

    def enter_normal_mode(self) -> None:
        config = MODE_CONFIGS[VimMode.NORMAL]
        self.read_only = config.read_only
        self.can_focus = not config.read_only
        self.border_subtitle = config.title
        self.styles.border_subtitle_background = config.bg_color
        self.mode = VimMode.NORMAL
        self.refresh()
