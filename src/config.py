"""Editor mode configuration and constants.

Defines the available modes and their configurations including:
- Mode types (Normal, Insert, Visual)
- Visual indicators (titles, colors)
- Mode-specific behaviors (read-only states)
"""

from enum import Enum
from dataclasses import dataclass


@dataclass
class ModeConfig:
    """Configuration for editor modes.

    Attributes:
        title: Display name shown in editor UI
        read_only: Whether mode allows text modification
        bg_color: Background color for mode indicator
    """

    subtitle: str
    read_only: bool
    bg_color: str


class VimMode(str, Enum):
    """Available editor modes.

    Supported modes:
    - NORMAL: Default mode for navigation and commands
    - INSERT: Text input mode
    - VISUAL: Character-based selection
    - VISUAL_LINE: Line-based selection
    - VISUAL_BLOCK: Rectangular selection
    - COMMAND: Command input mode
    """

    NORMAL = "normal"
    INSERT = "insert"
    VISUAL = "visual"
    VISUAL_LINE = "v_line"
    VISUAL_BLOCK = "v_block"
    COMMAND = "command"


MODE_CONFIGS = {
    VimMode.NORMAL: ModeConfig("NORMAL", True, "#98C379"),
    VimMode.INSERT: ModeConfig("INSERT", False, "#E8B86D"),
    VimMode.VISUAL: ModeConfig("VISUAL", True, "#6EACDA"),
    VimMode.VISUAL_LINE: ModeConfig("V-LINE", True, "#6EACDA"),
    VimMode.VISUAL_BLOCK: ModeConfig("V-BLOCK", True, "#6EACDA"),
    VimMode.COMMAND: ModeConfig(":", True, "#E06C75"),
}
