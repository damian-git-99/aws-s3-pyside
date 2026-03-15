"""Configuration management module with SQLite persistence.

This module provides persistent configuration storage using SQLite,
compatible with both development and PyInstaller builds.
"""

from src.config.config_manager import ConfigManager

__all__ = ['ConfigManager']
