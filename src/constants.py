# constants.py
# Centralized UI / Asset constants
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


# =========================================================
# Base Paths
# =========================================================

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Assets
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
# BACKGROUND = IMAGES_DIR / "background.jpg"
# DEFAULT_AVATAR = IMAGES_DIR / "default_avatar.png"

# Example UI images
# BUTTON_START = IMAGES_DIR / "btn_start.png"
# BUTTON_STOP = IMAGES_DIR / "btn_stop.png"

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

# Global theme
# COLOR_PRIMARY = "#2E3440"
# COLOR_SECONDARY = "#3B4252"
# COLOR_ACCENT = "#88C0D0"

# Backgrounds
SEMI_TRANSPARENT_BLACK = "rgba(0, 0, 0, 180)"
RED = "rgba(100, 0, 0, 150)"
GREEN = "rgba(0, 100, 0, 150)"
DARK_GREY = "#555555"
DEEP_RED = "#b30000"
LIGHT_RED = "#e60000"
COLOR_SCORE_FLASH = "#ffffaa"
COLOR_EQUIP_LABEL = "#cccccc"
BLUR_RADIUS = 15
DROPSHADOW_OFFSET_AMOUNT = (0, 5)
SHADOW_COLOR = (0, 0, 0, 160)
CONTENT_MARGINS = (0, 0, 0, 0)
BLURRED_LOGO_BACKGROUND = f"""
                border-image: url('{BLURRED_LOGO}');
                background-position: center;
        """
# COLOR_BG_MAIN = "#ECEFF4"
# COLOR_BG_DARK = "#2E3440"
# COLOR_BG_WIDGET = "#FFFFFF"

# Text
# COLOR_TEXT_MAIN = "#2E3440"
# COLOR_TEXT_LIGHT = "#D8DEE9"
# COLOR_TEXT_DISABLED = "#A0A0A0"

# Status
# COLOR_SUCCESS = "#A3BE8C"
# COLOR_WARNING = "#EBCB8B"
# COLOR_ERROR = "#BF616A"

# =========================================================
# Window / Layout
# =========================================================
VERTICAL_SPACING = 12
COOL_FONT = "font-family: 'Courier New'; font-size: 16px; font-weight: bold; background-color: teal;"
RED_TEAM_BACKGROUND = "font-family: 'Courier New'; font-size: 14px; font-weight: bold; color: black; background-color: rgba(160, 0, 96, 64);"
GREEN_TEAM_BACKGROUND = "font-family: 'Courier New'; font-size: 14px; font-weight: bold; color: black; background-color: rgba(0, 128, 128, 64);"
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
# WINDOW_WIDTH = 1200
# WINDOW_HEIGHT = 800

# MIN_WIDTH = 800
# MIN_HEIGHT = 600

# PADDING_SMALL = 8
# PADDING_MEDIUM = 16
# PADDING_LARGE = 24

# =========================================================
# Fonts
# =========================================================

# FONT_FAMILY = "Segoe UI"
# FONT_SIZE_SMALL = 10
# FONT_SIZE_NORMAL = 12
# FONT_SIZE_LARGE = 16
# FONT_SIZE_TITLE = 24

# =========================================================
# Timing / Animation
# =========================================================

# ANIMATION_FAST = 100      # ms
# ANIMATION_NORMAL = 250
# ANIMATION_SLOW = 500

# =========================================================
# Misc
# =========================================================

# =========================================================
# UI Styles
# =========================================================
STYLE_CONFIG_WINDOW = f"""
    #ConfigWindow {{
        background-color: black;
    }}
    QLabel {{
        color: white;
        font-family: Arial;
        font-size: 14px;
    }}
    QLineEdit {{
        background-color: {SEMI_TRANSPARENT_BLACK};
        border: 1px solid {DARK_GREY};
        padding: 8px;
        border-radius: 6px;
        color: white;
        font-size: 14px;
        min-width: 220px;
    }}
    QPushButton {{
        background-color: {DEEP_RED};
        padding: 10px 25px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 16px;
        color: white;
    }}
    QPushButton:hover {{
        background-color: {LIGHT_RED};
    }}
"""
STYLE_ACTION_BUTTON = """
    background-color: rgba(40, 110, 230, 150);
    border-radius: 20px;
    padding: 5px;
    font-weight: bold;
    font-size: 13px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    color: white;
"""
STYLE_TEAM_LABEL_ENTRY_RED = """
    color: white;
    font-weight: bold;
    font-size: 36px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(100, 0, 0, 150);
    border-radius: 20px;
    padding: 10px 20px;
    margin: 10px;
"""
STYLE_TEAM_LABEL_ENTRY_GREEN = """
    color: white;
    font-weight: bold;
    font-size: 36px;
    font-family: 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(0, 100, 0, 150);
    border-radius: 20px;
    padding: 10px 20px;
    margin: 10px;
"""
STYLE_TEAM_LABEL_PLAY_RED = """
    color: white;
    font-weight: bold;
    font-size: 24px;
    font-family: 'Audiowide', 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(100, 0, 0, 150);
    border-radius: 15px;
    padding: 5px 15px;
    margin: 5px;
"""
STYLE_TEAM_LABEL_PLAY_GREEN = """
    color: white;
    font-weight: bold;
    font-size: 24px;
    font-family: 'Audiowide', 'Orbitron', 'Courier New', sans-serif;
    background-color: rgba(0, 100, 0, 150);
    border-radius: 15px;
    padding: 5px 15px;
    margin: 5px;
"""
STYLE_SEMI_TRANSPARENT_CONTAINER = "background-color: rgba(0, 0, 0, 127); border-radius: 15px;"
STYLE_TEAM_SCORE_LABEL = "color: white; font-weight: bold; font-size: 18px; font-family: 'Orbitron', 'Courier New';"
STYLE_TEAM_SCORE_LABEL_FLASH = f"color: {COLOR_SCORE_FLASH}; font-weight: bold; font-size: 18px; font-family: 'Orbitron', 'Courier New';"
STYLE_SECTION_LABEL = "color: white; font-weight: bold; font-size: 18px; font-family: 'Orbitron';"
STYLE_TIMER_DISPLAY = f"color: {COLOR_SCORE_FLASH}; font-size: 36px; font-weight: bold; font-family: 'Orbitron';"
STYLE_GRID_HEADER = "color: white; font-weight: bold; font-size: 12px;"
STYLE_PLAYER_LABEL = "color: white; font-size: 12px;"
STYLE_EQUIP_LABEL = f"color: {COLOR_EQUIP_LABEL}; font-size: 12px; font-weight: bold;"
STYLE_SCORE_LABEL = f"color: {COLOR_SCORE_FLASH}; font-size: 14px; font-weight: bold;"
STYLE_PLAYER_INDEX_LABEL = "color: black; font-weight: bold;"
STYLE_HIT_FEED_LIST = """
    QListWidget {
        background-color: transparent;
        color: white;
        font-size: 14px;
        font-family: 'Courier New';
        border: none;
    }
    QListWidget::item {
        padding: 2px;
    }
"""

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
# VERSION = "1.0.1"
