from enum import Enum
from dataclasses import dataclass

@dataclass
class ModeConfig:
    """Configuration for a VIM mode."""
    title: str
    read_only: bool
    bg_color: str

class VimMode(str, Enum):
    """Available VIM modes."""
    NORMAL = "normal"
    INSERT = "insert"
    VISUAL = "visual"
    VISUAL_LINE = "v_line"
    VISUAL_BLOCK = "v_block"

MODE_CONFIGS = {
    VimMode.NORMAL: ModeConfig(
        title="NORMAL",
        read_only=True,
        bg_color="#98C379"
    ),
    VimMode.INSERT: ModeConfig(
        title="INSERT",
        read_only=False,
        bg_color="#E8B86D"
    ),
    VimMode.VISUAL: ModeConfig(
        title="VISUAL",
        read_only=True,
        bg_color="#6EACDA"
    ),
    VimMode.VISUAL_LINE: ModeConfig(
        title="V-LINE",
        read_only=True,
        bg_color="#6EACDA"
    ),
    VimMode.VISUAL_BLOCK: ModeConfig(
        title="V-BLOCK",
        read_only=True,
        bg_color="#6EACDA"
    )
}
