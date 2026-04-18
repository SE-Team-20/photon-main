# constants.py
# Centralized UI / Asset constants
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


# =========================================================
# Base Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SFX_DIR = ASSETS_DIR / "sound"
CONFIG_DIR = BASE_DIR / "config"

# =========================================================
# Image File Paths
# =========================================================
LOGO = Path(IMAGES_DIR / "logo.jpg").as_posix()
def logo_icon():
    """Return the cached logo pixmap (created on first call)."""
    if not hasattr(logo_icon, "_cached"):
        logo_icon._cached = QPixmap(LOGO).scaled(
            240, 184,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    return logo_icon._cached
BLURRED_LOGO = Path(IMAGES_DIR / "blurredlogo.jpg").as_posix()

DBINIT_PATH = CONFIG_DIR / "database.ini"
DBINIT_SEC = "postgresql"


# =========================================================
# Network
# =========================================================

SOCKET_BROADCAST = "7500"
SOCKET_RECEIVE = "7501"
RECIEVE_INPUT = "0.0.0.0"
BROADCAST_INPUT = "127.0.0.1"

CODE_GAMESTART = "202"
CODE_GAMEEND = "221"

CODE_BASESCORE_RED = "53"
CODE_BASESCORE_GREEN = "43"

# =========================================================
# Database
# =========================================================
NEW_CODENAME_ADDED = 0
EXISTING_CODENAME_UPDATED = 1
CODENAME_ALREADY_EXISTS = 2
ERROR_OCCURRED = 3
CODENAME_CHANGE_ATTEMPT_MATCHES_EXISTING = 4
COOL_GUY_EMOJI = f"\U0001F60E"

# =========================================================
# Gameplay
# =========================================================

MAX_NUM_PLAYER = 15
MAX_NUM_PLAYER_MINUSONE = 14
NUM_TEAM = 2

SCORE_BASE = 100
PENALTY_BASE = 0

SCORE_TAKEDOWN = 10
PENALTY_TAKEDOWN = -10

BASE_EQUIP_ID = 100

# =========================================================
# Colors (Hex / RGB)
# =========================================================

SEMI_TRANSPARENT_BLACK = "rgba(0, 0, 0, 180)"
RED = "rgba(100, 0, 0, 150)"
GREEN = "rgba(0, 100, 0, 150)"
DARK_GREY = "#555555"
DEEP_RED = "#b30000"
LIGHT_RED = "#e60000"
COLOR_SCORE_FLASH = "#ffee00"
COLOR_EQUIP_LABEL = "#00c8ff"
BLUR_RADIUS = 15
DROPSHADOW_OFFSET_AMOUNT = (0, 5)
SHADOW_COLOR = (0, 0, 0, 160)
CONTENT_MARGINS = (0, 0, 0, 0)

# Neon palette
NEON_CYAN = "#00ffff"
NEON_RED_BRIGHT = "#ff3333"
NEON_GREEN_BRIGHT = "#00ff55"
NEON_BLUE = "#0088ff"
NEON_YELLOW = "#ffee00"

BLURRED_LOGO_BACKGROUND = f"""
                border-image: url('{BLURRED_LOGO}');
                background-position: center;
        """

# =========================================================
# Window / Layout
# =========================================================
VERTICAL_SPACING = 12
COOL_FONT = f"font-family: 'Orbitron', 'Courier New'; font-size: 13px; font-weight: bold; background-color: #000a14; color: {NEON_CYAN};"
RED_TEAM_BACKGROUND = f"font-family: 'Courier New', monospace; font-size: 12px; font-weight: bold; color: #ffcccc; background-color: rgba(70, 0, 0, 140); border: 1px solid {NEON_RED_BRIGHT}; border-radius: 2px;"
GREEN_TEAM_BACKGROUND = f"font-family: 'Courier New', monospace; font-size: 12px; font-weight: bold; color: #ccffdd; background-color: rgba(0, 55, 0, 140); border: 1px solid {NEON_GREEN_BRIGHT}; border-radius: 2px;"
HORIZONTAL_SPACING = 20
NETWORK_SECTION_HEIGHT = 30
NETWORK_SECTION_SPACING = 20
ASPECT_RATIO = 4/5
BUTTON_DIMENSIONS = 60
X_ORIGIN = "(QGuiApplication.primaryScreen().availableGeometry().width() - eval(WINDOW_WIDTH)) // 2"
Y_ORIGIN = "(QGuiApplication.primaryScreen().availableGeometry().height() - eval(WINDOW_HEIGHT)) // 2"
WINDOW_WIDTH = "QGuiApplication.primaryScreen().availableGeometry().width() * ASPECT_RATIO"
WINDOW_HEIGHT = "QGuiApplication.primaryScreen().availableGeometry().height() * ASPECT_RATIO"
WINDOW_STAYS_ON_TOP = True
def window_stays_on_top(self, enable):
    if enable:
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
    else:
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
    self.show()

# =========================================================
# UI Styles
# =========================================================
STYLE_CONFIG_WINDOW = f"""
    #ConfigWindow {{
        background-color: #000a14;
    }}
    QLabel {{
        color: {NEON_CYAN};
        font-family: 'Orbitron', 'Courier New', monospace;
        font-size: 14px;
        letter-spacing: 1px;
    }}
    QLineEdit {{
        background-color: rgba(0, 15, 35, 220);
        border: 1px solid {NEON_CYAN};
        border-radius: 3px;
        padding: 8px;
        color: {NEON_CYAN};
        font-family: 'Orbitron', 'Courier New', monospace;
        font-size: 13px;
        min-width: 220px;
    }}
    QLineEdit:focus {{
        border: 2px solid {NEON_BLUE};
    }}
    QPushButton {{
        background-color: rgba(180, 0, 0, 200);
        border: 2px solid {NEON_RED_BRIGHT};
        padding: 10px 25px;
        border-radius: 3px;
        font-weight: bold;
        font-size: 15px;
        font-family: 'Orbitron', 'Courier New', monospace;
        color: white;
        letter-spacing: 2px;
    }}
    QPushButton:hover {{
        background-color: rgba(220, 0, 0, 230);
        border: 2px solid white;
        color: {NEON_YELLOW};
    }}
"""
STYLE_CONFIG_TITLE = f"font-size: 24px; font-weight: bold; color: {NEON_CYAN}; font-family: 'Orbitron', 'Courier New'; letter-spacing: 3px;"
STYLE_ACTION_BUTTON = f"""
    background-color: rgba(0, 30, 80, 200);
    border: 2px solid {NEON_BLUE};
    border-radius: 4px;
    padding: 5px;
    font-weight: bold;
    font-size: 13px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    color: {NEON_CYAN};
    letter-spacing: 1px;
"""
STYLE_TEAM_LABEL_ENTRY_RED = f"""
    color: white;
    font-weight: bold;
    font-size: 32px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(150, 0, 0, 200);
    border: 3px solid {NEON_RED_BRIGHT};
    border-radius: 3px;
    padding: 8px 20px;
    margin: 8px;
    letter-spacing: 5px;
"""
STYLE_TEAM_LABEL_ENTRY_GREEN = f"""
    color: white;
    font-weight: bold;
    font-size: 32px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(0, 110, 0, 200);
    border: 3px solid {NEON_GREEN_BRIGHT};
    border-radius: 3px;
    padding: 8px 20px;
    margin: 8px;
    letter-spacing: 5px;
"""
STYLE_TEAM_LABEL_PLAY_RED = f"""
    color: white;
    font-weight: bold;
    font-size: 20px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(150, 0, 0, 200);
    border-bottom: 2px solid {NEON_RED_BRIGHT};
    padding: 6px 15px;
    letter-spacing: 4px;
"""
STYLE_TEAM_LABEL_PLAY_GREEN = f"""
    color: white;
    font-weight: bold;
    font-size: 20px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(0, 110, 0, 200);
    border-bottom: 2px solid {NEON_GREEN_BRIGHT};
    padding: 6px 15px;
    letter-spacing: 4px;
"""
STYLE_SEMI_TRANSPARENT_CONTAINER = f"background-color: rgba(0, 6, 20, 210); border: 2px solid {NEON_CYAN}; border-radius: 3px;"
STYLE_TEAM_SCORE_LABEL = f"color: {NEON_CYAN}; font-weight: bold; font-size: 16px; font-family: 'Orbitron', 'Courier New'; letter-spacing: 1px; padding: 5px;"
STYLE_TEAM_SCORE_LABEL_FLASH = f"color: {NEON_YELLOW}; font-weight: bold; font-size: 18px; font-family: 'Orbitron', 'Courier New'; letter-spacing: 1px; padding: 5px;"
# Team-specific total bar styles used in PlayActionWindow score labels
STYLE_TEAM_SCORE_LABEL_RED = f"""
    color: white;
    font-weight: bold;
    font-size: 15px;
    font-family: 'Orbitron', 'Courier New';
    background-color: rgba(160, 0, 0, 210);
    border-top: 2px solid {NEON_RED_BRIGHT};
    border-bottom: 2px solid {NEON_RED_BRIGHT};
    padding: 5px 10px;
    letter-spacing: 2px;
"""
STYLE_TEAM_SCORE_LABEL_GREEN = f"""
    color: white;
    font-weight: bold;
    font-size: 15px;
    font-family: 'Orbitron', 'Courier New';
    background-color: rgba(0, 120, 0, 210);
    border-top: 2px solid {NEON_GREEN_BRIGHT};
    border-bottom: 2px solid {NEON_GREEN_BRIGHT};
    padding: 5px 10px;
    letter-spacing: 2px;
"""
STYLE_TEAM_SCORE_LABEL_FLASH_RED = f"""
    color: {NEON_YELLOW};
    font-weight: bold;
    font-size: 17px;
    font-family: 'Orbitron', 'Courier New';
    background-color: rgba(210, 30, 0, 230);
    border-top: 2px solid {NEON_YELLOW};
    border-bottom: 2px solid {NEON_YELLOW};
    padding: 5px 10px;
    letter-spacing: 2px;
"""
STYLE_TEAM_SCORE_LABEL_FLASH_GREEN = f"""
    color: {NEON_YELLOW};
    font-weight: bold;
    font-size: 17px;
    font-family: 'Orbitron', 'Courier New';
    background-color: rgba(0, 160, 30, 230);
    border-top: 2px solid {NEON_YELLOW};
    border-bottom: 2px solid {NEON_YELLOW};
    padding: 5px 10px;
    letter-spacing: 2px;
"""
STYLE_SECTION_LABEL = f"color: {NEON_CYAN}; font-weight: bold; font-size: 18px; font-family: 'Orbitron', 'Courier New'; letter-spacing: 2px;"
STYLE_TIMER_DISPLAY = f"color: {NEON_YELLOW}; font-size: 52px; font-weight: bold; font-family: 'Orbitron', 'Courier New'; letter-spacing: 6px;"
STYLE_GRID_HEADER = f"color: white; font-weight: bold; font-size: 11px; font-family: 'Orbitron', 'Courier New'; letter-spacing: 1px; background-color: rgba(0, 40, 80, 200); padding: 3px 2px;"
STYLE_PLAYER_LABEL = "color: #ddeeff; font-size: 12px; font-family: 'Courier New', monospace;"
STYLE_PLAYER_LABEL_ALT = "color: #ddeeff; font-size: 12px; font-family: 'Courier New', monospace; background-color: rgba(255, 255, 255, 6);"
STYLE_EQUIP_LABEL = "color: rgba(0, 200, 255, 200); font-size: 12px; font-weight: bold; font-family: 'Courier New', monospace;"
STYLE_EQUIP_LABEL_ALT = "color: rgba(0, 200, 255, 200); font-size: 12px; font-weight: bold; font-family: 'Courier New', monospace; background-color: rgba(255, 255, 255, 6);"
STYLE_SCORE_LABEL = f"color: {NEON_YELLOW}; font-size: 14px; font-weight: bold; font-family: 'Orbitron', 'Courier New';"
STYLE_SCORE_LABEL_ALT = f"color: {NEON_YELLOW}; font-size: 14px; font-weight: bold; font-family: 'Orbitron', 'Courier New'; background-color: rgba(255, 255, 255, 6);"
STYLE_PLAYER_INDEX_LABEL = f"color: {NEON_CYAN}; font-weight: bold; font-family: 'Courier New'; font-size: 11px;"
STYLE_HIT_FEED_LIST = f"""
    QListWidget {{
        background-color: rgba(0, 6, 20, 160);
        color: {NEON_CYAN};
        font-size: 12px;
        font-family: 'Courier New', monospace;
        border: none;
        border-radius: 2px;
    }}
    QListWidget::item {{
        padding: 3px 5px;
        border-bottom: 1px solid rgba(0, 255, 255, 20);
    }}
    QListWidget::item:selected {{
        background-color: rgba(0, 50, 80, 200);
    }}
"""

# =========================================================
# Panel Paint Constants
# =========================================================
# Near-black fill with a subtle team tint — dark like the reference image panels
COLOR_PANEL_BG_RED = (12, 0, 0, 235)
COLOR_PANEL_BG_GREEN = (0, 14, 0, 235)
COLOR_PANEL_GLOW_RED = (255, 40, 40)
COLOR_PANEL_GLOW_GREEN = (40, 255, 100)
# Layers: outer glow fades in → innermost is a solid bright border line
PANEL_GLOW_LAYERS = [(8, 8), (5, 22), (3, 65), (2, 255)]
PANEL_BORDER_RADIUS = 3
PANEL_CORNER_MARK_SIZE = 16

# =========================================================
# Layout Sizes
# =========================================================
PANEL_WIDTH_RATIO = 0.48
PANEL_HEIGHT_RATIO = 0.6
ACTION_BUTTON_WIDTH = 120
ACTION_BUTTON_HEIGHT = 60
PLAYER_ID_FIELD_WIDTH = 35
FIELD_HEIGHT = 28
CODENAME_FIELD_WIDTH = 140
PLAYER_INDEX_LABEL_WIDTH = 70
BASEICON_SIZE = 32

# =========================================================
# Timing
# =========================================================
FLASH_INTERVAL_MS = 500
TIMER_INTERVAL_MS = 1000
MUSIC_START_THRESHOLD = 16
COUNTDOWN_READY_SECONDS = 30
GAME_DURATION_SECONDS = 360
DEV_GAME_DURATION_SECONDS = 30

APP_NAME = "Photon Main"
