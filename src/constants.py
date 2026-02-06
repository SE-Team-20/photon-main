# constants.py
# Centralized UI / Asset constants

from pathlib import Path

# =========================================================
# Base Paths
# =========================================================

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Assets
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SFX_DIR = ASSETS_DIR / "sound"

# =========================================================
# Image File Paths
# =========================================================

LOGO = IMAGES_DIR / "logo.jpg"
# BACKGROUND = IMAGES_DIR / "background.jpg"
# DEFAULT_AVATAR = IMAGES_DIR / "default_avatar.png"

# Example UI images
# BUTTON_START = IMAGES_DIR / "btn_start.png"
# BUTTON_STOP = IMAGES_DIR / "btn_stop.png"

# =========================================================
# Colors (Hex / RGB)
# =========================================================

# Global theme
# COLOR_PRIMARY = "#2E3440"
# COLOR_SECONDARY = "#3B4252"
# COLOR_ACCENT = "#88C0D0"

# Backgrounds
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

APP_NAME = "Photon Main"
# VERSION = "1.0.0"
