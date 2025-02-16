"""Base functionality for editor modes.

Provides common setup and state management used by all editor modes.
"""

from ..config import VimMode, MODE_CONFIGS


class BaseMode:
    """Foundation for all editor modes.

    Handles common mode setup tasks:
    - Setting read-only state
    - Configuring focus behavior
    - Setting visual indicators (title, colors)
    - Managing mode transitions
    """

    def _setup_mode(self, mode: VimMode) -> None:
        """Configure editor state for a mode transition.

        Args:
            mode: Target mode to switch to

        Sets up:
        - Read-only state (only INSERT mode is writable)
        - Focus behavior
        - Visual indicators (title, background color)
        - Mode-specific configurations
        """
        config = MODE_CONFIGS[mode]
        self.mode = mode

        self.read_only = mode != VimMode.INSERT
        self.can_focus = True
        self.border_subtitle = config.subtitle
        self.styles.border_subtitle_background = config.bg_color
